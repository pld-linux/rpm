#include <sys/types.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <db.h>

typedef struct {			/* XXX: Globals. */
	const char *progname;		/* Program name. */
	char	*hdrbuf;		/* Input file header. */
	u_long	lineno;			/* Input file line number. */
	u_long	origline;		/* Original file line number. */
	int	endodata;		/* Reached the end of a database. */
	int	endofile;		/* Reached the end of the input. */
	int	version;		/* Input version. */
	char	*home;			/* Env home. */
	char	*passwd;		/* Env passwd. */
	int	private;		/* Private env. */
	u_int32_t cache;		/* Env cache size. */
} LDG;

int	db_init __P((DB_ENV *, char *, u_int32_t, int *));
int	env_create __P((DB_ENV **, LDG *));
int	main __P((int, char *[]));
int	usage __P((void));
int	version_check __P((void));

const char *progname = "rpmdb_reset";

int
main(argc, argv)
	int argc;
	char *argv[];
{
	enum { NOTSET, FILEID_RESET, LSN_RESET, STANDARD_LOAD } mode;
	extern char *optarg;
	extern int optind;
	DB_ENV	*dbenv;
	LDG ldg;
	int ch, exitval, ret;

	if ((exitval = version_check()) != 0)
		goto done;

	ldg.progname = progname;
	ldg.lineno = 0;
	ldg.endodata = ldg.endofile = 0;
	ldg.version = 1;
	ldg.cache = (1024 * 1024);
	ldg.hdrbuf = NULL;
	ldg.home = NULL;
	ldg.passwd = NULL;

	mode = NOTSET;
	exitval = 0;

	/*
	 * There are two modes for db_load: -r and everything else.  The -r
	 * option zeroes out the database LSN's or resets the file ID, it
	 * doesn't really "load" a new database.  The functionality is in
	 * db_load because we don't have a better place to put it, and we
	 * don't want to create a new utility for just that functionality.
	 */
	while ((ch = getopt(argc, argv, "h:r:V")) != EOF)
		switch (ch) {
		case 'h':
			ldg.home = optarg;
			break;
		case 'r':
			if (strcmp(optarg, "lsn") == 0)
				mode = LSN_RESET;
			else if (strcmp(optarg, "fileid") == 0)
				mode = FILEID_RESET;
			else {
				exitval = usage();
				goto done;
			}
			break;
		case 'V':
			printf("%s\n", db_version(NULL, NULL, NULL));
			return (EXIT_SUCCESS);
		case '?':
		default:
			exitval = usage();
			goto done;
		}
	argc -= optind;
	argv += optind;

	if (argc != 1 || mode == NOTSET) {
		exitval = usage();
		goto done;
	}

	/*
	 * Create an environment object initialized for error reporting, and
	 * then open it.
	 */
	if (env_create(&dbenv, &ldg) != 0)
		goto err;

	/* If we're resetting the LSNs, that's an entirely separate path. */
	switch (mode) {
	case FILEID_RESET:
		exitval = dbenv->fileid_reset(dbenv, argv[0], 0);
		break;
	case LSN_RESET:
		exitval = dbenv->lsn_reset(dbenv, argv[0], 0);
		break;
	default:
		break;
	}

	if (0) {
err:		exitval = 1;
	}
	if ((ret = dbenv->close(dbenv, 0)) != 0) {
		exitval = 1;
		fprintf(stderr,
		    "%s: dbenv->close: %s\n", ldg.progname, db_strerror(ret));
	}

	if (ldg.passwd != NULL)
		free(ldg.passwd);

done:
	return (exitval);
}

/*
 * env_create --
 *	Create the environment and initialize it for error reporting.
 */
int
env_create(dbenvp, ldg)
	DB_ENV **dbenvp;
	LDG *ldg;
{
	DB_ENV *dbenv;
	int ret;

	if ((ret = db_env_create(dbenvp, 0)) != 0) {
		fprintf(stderr, "%s: db_env_create: %s\n",
		    ldg->progname, db_strerror(ret));
		return (ret);
	}
	dbenv = *dbenvp;
	dbenv->set_errfile(dbenv, stderr);
	dbenv->set_errpfx(dbenv, ldg->progname);
	if (ldg->passwd != NULL && (ret = dbenv->set_encrypt(dbenv,
	    ldg->passwd, DB_ENCRYPT_AES)) != 0) {
		dbenv->err(dbenv, ret, "set_passwd");
		return (ret);
	}
	if ((ret = db_init(dbenv, ldg->home, ldg->cache, &ldg->private)) != 0)
		return (ret);
	dbenv->app_private = ldg;

	return (0);
}

/*
 * db_init --
 *	Initialize the environment.
 */
int
db_init(dbenv, home, cache, is_private)
	DB_ENV *dbenv;
	char *home;
	u_int32_t cache;
	int *is_private;
{
	u_int32_t flags;
	int ret;

	*is_private = 0;
	/* We may be loading into a live environment.  Try and join. */
	flags = DB_USE_ENVIRON |
	    DB_INIT_LOCK | DB_INIT_LOG | DB_INIT_MPOOL | DB_INIT_TXN;
	if ((ret = dbenv->open(dbenv, home, flags, 0)) == 0)
		return (0);
	if (ret == DB_VERSION_MISMATCH)
		goto err;

	/*
	 * We're trying to load a database.
	 *
	 * An environment is required because we may be trying to look at
	 * databases in directories other than the current one.  We could
	 * avoid using an environment iff the -h option wasn't specified,
	 * but that seems like more work than it's worth.
	 *
	 * No environment exists (or, at least no environment that includes
	 * an mpool region exists).  Create one, but make it private so that
	 * no files are actually created.
	 */
#define	LF_SET(f)	((flags) |= (f))
#define	LF_CLR(f)	((flags) &= ~(f))
	LF_CLR(DB_INIT_LOCK | DB_INIT_LOG | DB_INIT_TXN);
	LF_SET(DB_CREATE | DB_PRIVATE);
	*is_private = 1;
	if ((ret = dbenv->set_cachesize(dbenv, 0, cache, 1)) != 0) {
		dbenv->err(dbenv, ret, "set_cachesize");
		return (1);
	}
	if ((ret = dbenv->open(dbenv, home, flags, 0)) == 0)
		return (0);

	/* An environment is required. */
err:	dbenv->err(dbenv, ret, "DB_ENV->open");
	return (1);
}

/*
 * usage --
 *	Display the usage message.
 */
int
usage()
{
	(void)fprintf(stderr, "usage: %s %s\n\t%s %s\n",
	    progname, "[-V]",
	    progname, "-r lsn | fileid [-h home] db_file");
	return (EXIT_FAILURE);
}

int
version_check()
{
	int v_major, v_minor, v_patch;

	/* Make sure we're loaded with the right version of the DB library. */
	(void)db_version(&v_major, &v_minor, &v_patch);
	if (v_major != DB_VERSION_MAJOR || v_minor != DB_VERSION_MINOR) {
		fprintf(stderr,
		    "%s: version %d.%d doesn't match library version %d.%d\n",
		    progname, DB_VERSION_MAJOR,
		    DB_VERSION_MINOR, v_major, v_minor);
		return (EXIT_FAILURE);
	}
	return (0);
}
