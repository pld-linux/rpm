#include <sys/types.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <db.h>

int	version_check __P((void));

const char *progname = "rpmdb_checkversion";		/* Program name. */

/*
 * A very simple program to check for a Berkeley DB environment mismatch.
 */
int
main(int argc, char *argv[])
{
	extern char *optarg;
	extern int optind;
	const char *data_dir, *home;
	int ch, quiet;
	DB_ENV *dbenv;
	int ret;

	if ((ret = version_check()) != 0)
		return (EXIT_FAILURE);

	/*
	 * All of the shared database files live in home, but
	 * data files will live in data_dir.
	 */
	quiet = 0;
	home = "/var/lib/rpm";
	data_dir = "/var/lib/rpm";
	while ((ch = getopt(argc, argv, "h:d:qV")) != EOF)
		switch (ch) {
		case 'h':
			home = optarg;
			break;
		case 'd':
			data_dir = optarg;
			break;
		case 'q':
			quiet = 1;
			break;
		case 'V':
			printf("%s\n", db_version(NULL, NULL, NULL));
			return (EXIT_SUCCESS);
		case '?':
		default:
			(void)fprintf(stderr, "usage: %s [-h home] [-d data_dir]\n", progname);
			return (1);
		}
	argc -= optind;
	argv += optind;

	if (argc != 0) {
		(void)fprintf(stderr, "usage: %s [-h home] [-d data_dir]\n", progname);
		return (1);
	}

	/*
	 * Create an environment object and initialize it for error
	 * reporting.
	 */
	if ((ret = db_env_create(&dbenv, 0)) != 0) {
		if (!quiet)
			fprintf(stderr, "%s: %s\n", progname, db_strerror(ret));
		return (1);
	}
	if (quiet) {
		dbenv->set_errfile(dbenv, NULL);
	} else {
		dbenv->set_errfile(dbenv, stderr);
	}
	dbenv->set_errpfx(dbenv, progname);

	/*
	 * We want to specify the shared memory buffer pool cachesize,
	 * but everything else is the default.
	 */
	if ((ret = dbenv->set_cachesize(dbenv, 0, 64 * 1024, 0)) != 0) {
		dbenv->err(dbenv, ret, "set_cachesize");
		dbenv->close(dbenv, 0);
		return (1);
	}

	/* Databases are in a subdirectory. */
	(void)dbenv->set_data_dir(dbenv, data_dir);

	/* Open the environment with full transactional support. */
	ret = dbenv->open(dbenv, home, DB_INIT_MPOOL, 0644);
	/* Close the environment handle. */
	dbenv->close(dbenv, 0);
#if 0
	if (ret == DB_VERSION_MISMATCH) {
#else
	if (ret != 0) {
#endif
		return (1);
	}

	return (0);
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
