#!/bin/sh
# -----------
# $Id$
# Exit codes:
#	  0 - succesful
#	  1 - help displayed
#	  2 - no spec file name in cmdl parameters
#	  3 - spec file not stored in repo
#	  4 - some source, patch or icon files not stored in repo
#	  5 - package build failed
#	  6 - spec file with errors
#	  7 - wrong source in /etc/poldek.conf
#	  8 - Failed installing buildrequirements and subrequirements
#	  9 - Requested tag already exist
#	 10 - Refused to build fractional release
#	100 - Unknown error (should not happen)

# Notes (todo):
#	- builder -u fetches current version first (well that's okay, how you compare versions if you have no old spec?)
#	- when Icon: field is present, -5 and -a5 doesn't work
#	- builder -R skips installing BR if spec is not present before builder invocation (need to run builder twice)

VERSION="\
Build package utility from PLD Linux CVS repository
v0.16 (C) 1999-2006 Free Penguins".
PATH="/bin:/usr/bin:/usr/sbin:/sbin:/usr/X11R6/bin"

COMMAND="build"
TARGET=""

SPECFILE=""
BE_VERBOSE=""
QUIET=""
CLEAN=""
DEBUG=""
NOURLS=""
NOCVS=""
NOCVSSPEC=""
NODIST=""
NOINIT=""
UPDATE=""
UPDATE5=""
ADD5=""
NO5=""
ALWAYS_CVSUP=${ALWAYS_CVSUP:-"yes"}
CVSROOT=""

# It can be used i.e. in log file naming.
# See LOGFILE example.
DATE=`date +%Y-%m-%d_%H-%M-%S`

# Example: LOGFILE='../log.$PACKAGE_NAME'
# Example: LOGFILE='../LOGS/log.$PACKAGE_NAME.$DATE'
# Yes, you can use variable name! Note _single_ quotes!
LOGFILE=''

LOGDIR=""
LOGDIROK=""
LOGDIRFAIL=""
LASTLOG_FILE=""

CHMOD="no"
CHMOD_MODE="0444"
RPMOPTS=""
RPMBUILDOPTS=""
BCOND=""
GROUP_BCONDS="no"
CVSIGNORE_DF="no"

PATCHES=""
SOURCES=""
ICONS=""
PACKAGE_RELEASE=""
PACKAGE_VERSION=""
PACKAGE_NAME=""
PROTOCOL="ftp"
WGET_RETRIES=${MAX_WGET_RETRIES:-0}
CVS_RETRIES=${MAX_CVS_RETRIES:-1000}

CVSTAG=""
RES_FILE=""

CVS_SERVER="cvs.pld-linux.org"
DISTFILES_SERVER="://distfiles.pld-linux.org"
ATTICDISTFILES_SERVER="://attic-distfiles.pld-linux.org"

DEF_NICE_LEVEL=19
SCHEDTOOL="auto"

FAIL_IF_NO_SOURCES="yes"

# let get_files skip over files which are present to get those damn files fetched
SKIP_EXISTING_FILES="no"

if [ -x /usr/bin/rpm-getdeps ]; then
	FETCH_BUILD_REQUIRES_RPMGETDEPS="yes"
else
	FETCH_BUILD_REQUIRES_RPMGETDEPS="no"
fi

# Here we load saved user environment used to
# predefine options set above, or passed to builder
# in command line.
# This one reads global system environment settings:
if [ -f ~/etc/builderrc ]; then
	. ~/etc/builderrc
fi
# And this one cascades settings using user personal
# builder settings.
# Example of ~/.builderrc:
#
#UPDATE_POLDEK_INDEXES="yes"
#FETCH_BUILD_REQUIRES="yes"
#REMOVE_BUILD_REQUIRES="force"
#GROUP_BCONDS="yes"
#LOGFILE='../LOGS/log.$PACKAGE_NAME.$DATE'
#TITLECHANGE=no
#
SU_SUDO=""
if [ -n "$HOME_ETC" ]; then
	USER_CFG="$HOME_ETC/.builderrc"
else
	USER_CFG=~/.builderrc
fi

[ -f "$USER_CFG" ] && . "$USER_CFG"

if [ "$SCHEDTOOL" = "auto" ]; then
	if [ -x /usr/bin/schedtool ] && schedtool -B -e echo >/dev/null; then
		SCHEDTOOL="schedtool -B -e"
	else
		SCHEDTOOL="no"
	fi
fi

if [ -n "$USE_PROZILLA" ]; then
	GETURI="proz --no-getch -r -P ./ -t$WGET_RETRIES $PROZILLA_OPTS"
	GETURI2="$GETURI"
	OUTFILEOPT="-O"
elif [ -n "$USE_AXEL" ]; then
	GETURI="axel -a $AXEL_OPTS"
	GETURI2="$GETURI"
	OUTFILEOPT="-o"
else
	wget --help 2>&1 | grep -q -- ' --no-check-certificate ' && WGET_OPTS="$WGET_OPTS --no-check-certificate"
	wget --help 2>&1 | grep -q -- ' --inet ' && WGET_OPTS="$WGET_OPTS --inet"
	wget --help 2>&1 | grep -q -- ' --retry-connrefused ' && WGET_OPTS="$WGET_OPTS --retry-connrefused"

	GETURI="wget --passive-ftp -c -nd -t$WGET_RETRIES $WGET_OPTS"
	GETURI2="wget -c -nd -t$WGET_RETRIES $WGET_OPTS"
	OUTFILEOPT="-O"
fi

GETLOCAL="cp -a"

if (rpm --version 2>&1 | grep -q '4.0.[0-2]'); then
	RPM="rpm"
	RPMBUILD="rpm"
else
	RPM="rpm"
	RPMBUILD="rpmbuild"
fi

POLDEK_INDEX_DIR="`$RPM --eval %_rpmdir`/"
POLDEK_CMD="$SU_SUDO /usr/bin/poldek --noask"

run_poldek()
{
	RES_FILE=~/tmp/poldek-exit-status.$RANDOM
	if [ -n "$LOGFILE" ]; then
		LOG=`eval echo $LOGFILE`
		if [ -n "$LASTLOG_FILE" ]; then
			echo "LASTLOG=$LOG" > $LASTLOG_FILE
		fi
		(${NICE_COMMAND} ${POLDEK_CMD} `while test $# -gt 0; do echo "$1 ";shift;done` ; echo $? > ${RES_FILE})|tee -a $LOG
		return $exit_pldk
	else
		(${NICE_COMMAND} ${POLDEK_CMD} `while test $# -gt 0; do echo "$1 ";shift;done` ; echo $? > ${RES_FILE}) 1>&2 >/dev/null
		return `cat ${RES_FILE}`
		rm -rf ${RES_FILE}
	fi
}

#---------------------------------------------
# functions

usage()
{
	if [ -n "$DEBUG" ]; then set -xv; fi
	echo "\
Usage: builder [-D|--debug] [-V|--version] [-a|--as_anon] [-b|-ba|--build]

[-bb|--build-binary] [-bs|--build-source] [-u|--try-upgrade]
[{-B|--branch} <branch>] [{-d|--cvsroot} <cvsroot>] [-g|--get]
[-h|--help] [--http] [{-l,--logtofile} <logfile>] [-m|--mr-proper]
[-q|--quiet] [--date <yyyy-mm-dd> [-r <cvstag>] [{-T--tag <cvstag>]
[-Tvs|--tag-version-stable] [-Tvn|--tag-version-nest]
[-Ts|--tag-stable] [-Tn|--tag-nest] [-Tv|--tag-version]
[{-Tp|--tag-prefix} <prefix>] [{-tt|--test-tag}]
[-nu|--no-urls] [-v|--verbose] [--opts <rpm opts>] [--show-bconds]
[--with/--without <feature>] [--define <macro> <value>] <package>[.spec][:cvstag]

-5, --update-md5    - update md5 comments in spec, implies -nd -ncs
-a5, --add-md5      - add md5 comments to URL sources, implies -nc -nd -ncs
-n5, --no-md5       - ignore md5 comments in spec
-D, --debug         - enable builder script debugging mode,
-debug              - produce rpm debug package (same as --opts -debug)
-V, --version       - output builder version
-a, --as_anon       - get files via pserver as cvs@$CVS_SERVER,
-b, -ba, --build    - get all files from CVS repo or HTTP/FTP and build package
                      from <package>.spec,
-bb, --build-binary - get all files from CVS repo or HTTP/FTP and build binary
                      only package from <package>.spec,
-bp, --build-prep   - execute the %prep phase of <package>.spec,
-bc                 - reserved (not implemented)
-bi                   reserved (not implemented)
-bs, --build-source - get all files from CVS repo or HTTP/FTP and only pack
                      them into src.rpm,
--short-circuit     - reserved (not implemented)
-B, --branch        - add branch
-c, --clean         - clean all temporarily created files (in BUILD, SOURCES,
                      SPECS and \$RPM_BUILD_ROOT),
-d <cvsroot>, --cvsroot <cvsroot>
                    - setup \$CVSROOT,
--define <macro> <value>
                    - define a macro <macro> with value <value>,
--nodeps            - rpm won't check any dependences
-g, --get           - get <package>.spec and all related files from CVS repo
                      or HTTP/FTP,
-h, --help          - this message,
--http              - use http instead of ftp,
-l <logfile>, --logtofile <logfile>
                    - log all to file,
-m, --mr-proper     - only remove all files related to spec file and all work
                      resources,
-nc, --no-cvs       - don't download sources from CVS, if source URL is given,
-ncs, --no-cvs-specs
                    - don't check specs in CVS
-nd, --no-distfiles - don't download from distfiles
-nm, --no-mirrors   - don't download from mirror, if source URL is given,
-nu, --no-urls      - don't try to download from FTP/HTTP location,
-ns, --no-srcs      - don't download Sources
-ns0, --no-source0  - don't download Source0
-nn, --no-net       - don't download anything from the net
--no-init           - don't initialize builder paths (SPECS and SOURCES)
-ske,
--skip-existing-files - skip existing files in get_files
--opts <rpm opts>   - additional options for rpm
-q, --quiet         - be quiet,
--date yyyy-mm-dd   - build package using resources from specified CVS date,
-r <cvstag>, --cvstag <cvstag>
                    - build package using resources from specified CVS tag,
-R, --fetch-build-requires
                    - fetch what is BuildRequired,
-RB, --remove-build-requires
                    - remove all you fetched with -R or --fetch-build-requires
                      remember, this option requires confirmation,
-FRB, --force-remove-build-requires
                    - remove all you fetched with -R or --fetch-build-requires
                      remember, this option works without confirmation,
-sd, --source-distfiles - list sources available from distfiles (intended for offline
                      operations; does not work when Icon field is present
                      but icon file is absent),
-sdp, --source-distfiles-paths - list sources available from distfiles -
                      paths relative to distfiles directory (intended for offline
                      operations; does not work when Icon field is present
                      but icon file is absent),
-sf, --source-files - list sources - bare filenames (intended for offline
                      operations; does not work when Icon field is present
                      but icon file is absent),
-sp, --source-paths - list sources - filenames with full local paths (intended for
                      offline operations; does not work when Icon field is present
                      but icon file is absent),
-su, --source-urls  - list urls - urls to sources and patches
                      intended for copying urls with spec with lots of macros in urls
-T <cvstag> , --tag <cvstag>
                    - add cvs tag <cvstag> for files,
-Tvs, --tag-version-stable
                    - add cvs tags STABLE and NAME-VERSION-RELEASE for files,
-Tvn, --tag-version-nest
                    - add cvs tags NEST and NAME-VERSION-RELEASE for files,
-Ts, --tag-stable
                    - add cvs tag STABLE for files,
-Tn, --tag-nest
                    - add cvs tag NEST for files,
-Tv, --tag-version
                    - add cvs tag NAME-VERSION-RELEASE for files,
-Tp, --tag-prefix <prefix>
                    - add <prefix> to NAME-VERSION-RELEASE tags,
-tt, --test-tag <prefix>
                    - fail if tag is already present,
-ir, --integer-release-only
                    - allow only integer and snapshot releases
-v, --verbose       - be verbose,
-u, --try-upgrade   - check version, and try to upgrade package
-un, --try-upgrade-with-float-version
                    - as above, but allow float version
-U, --update        - refetch sources, don't use distfiles, and update md5 comments
-Upi, --update-poldek-indexes
                    - refresh or make poldek package index files.
-np, --nopatch <patchnumber>
                    - don't apply <patchnumber>
--show-bconds       - show available conditional builds, which can be used
                    - with --with and/or --without switches.
--with/--without <feature>
                    - conditional build package depending on %_with_<feature>/
                      %_without_<feature> macro switch.  You may now use
                      --with feat1 feat2 feat3 --without feat4 feat5 --with feat6
                      constructions. Set GROUP_BCONDS to yes to make use of it.
--target <platform>, --target=<platform>
                     - build for platform <platform>.
--init-rpm-dir       - initialize ~/rpm directory structure
"
}

update_shell_title() {
	[ -t 1 ] || return
	local len=${COLUMNS:-80}
	local msg=$(echo "$*" | cut -c-$len)

	if [ -n "$BE_VERBOSE" ]; then
		echo >&2 "$(date +%s.%N) $*"
	fi

	if [ "x$TITLECHANGE" == "xyes" -o "x$TITLECHANGE" == "x" ]; then
		local pkg
		if [ -n "$PACKAGE_NAME" ]; then
			pkg=${PACKAGE_NAME}-${PACKAGE_VERSION}-${PACKAGE_RELEASE}
		else
			pkg=${SPECFILE}
		fi

		msg="$pkg: ${SHELL_TITLE_PREFIX:+$SHELL_TITLE_PREFIX }$msg"
		msg="$(echo $msg | tr -d '\n\r')"
		case "$TERM" in
			cygwin|xterm*)
			echo >&2 -ne "\033]1;$msg\007\033]2;$msg\007"
		;;
			screen*)
			echo >&2 -ne "\033]0;$msg\007"
		;;
		esac
	fi
}

# set TARGET from BuildArch: from SPECFILE
set_spec_target() {
	if [ -n "$SPECFILE" ] && [ -z "$TARGET" ]; then
		tmp=$(awk '/^BuildArch:/ { print $NF}' $SPECFILE)
		if [ "$tmp" ]; then
				TARGET="$tmp"
				case "$RPMBUILD" in
				"rpmbuild")
					TARGET_SWITCH="--target $TARGET" ;;
				"rpm")
					TARGET_SWITCH="--target=$TARGET" ;;
				esac
		fi
	fi
}

cache_rpm_dump () {
	 if [ -n "$DEBUG" ]; then
		  set -x;
		  set -v;
	 fi

	update_shell_title "cache_rpm_dump"
	local rpm_dump
	rpm_dump=`

	# we reset macros not to contain macros.build as all the %() macros are
	# executed here, while none of them are actually needed.
	# what we need from dump is NAME, VERSION, RELEASE and PATCHES/SOURCES.
	# at the time of this writing macros.build + macros contained 70 "%(...)" macros.
	macrofiles="/usr/lib/rpm/macros:$SPECS_DIR/.builder-rpmmacros:~/etc/.rpmmacros:~/.rpmmacros"
	dump='%{echo:dummy: PACKAGE_NAME %{name} }%dump'
	# FIXME: better ideas than .rpmrc?
	printf 'include:/usr/lib/rpm/rpmrc\nmacrofiles:%s\n' $macrofiles > .builder-rpmrc
# TODO: move these to /usr/lib/rpm/macros
	cat > .builder-rpmmacros <<'EOF'
%requires_releq_kernel_up %{nil}
%requires_releq_kernel_smp %{nil}
%requires_releq() %{nil}
%pyrequires_eq() %{nil}
%requires_eq() %{nil}
%requires_eq_to() %{nil}
%releq_kernel_up ERROR
%releq_kernel_smp ERROR
%kgcc_package ERROR
%_fontsdir ERROR
%ruby_version ERROR
%ruby_ver_requires_eq() %{nil}
%ruby_mod_ver_requires_eq() %{nil}
%__php_api_requires() %{nil}
%php_major_version ERROR
%php_api_version ERROR
%py_ver ERROR
EOF
	case "$RPMBUILD" in
	rpm)
		ARGS='-bp'
		;;
	rpmbuild)
		ARGS='--nodigest --nosignature --nobuild'
		;;
	esac
	if [ "$NOINIT" = "yes" ] ; then
		cat >> .builder-rpmmacros <<'EOF'
%_specdir ./
%_sourcedir ./
EOF
	fi
	$RPMBUILD --rcfile .builder-rpmrc $ARGS $ARGDIRS --nodeps --define "prep $dump" $BCOND $TARGET_SWITCH $SPECFILE 2>&1
	`
	if [ $? -gt 0 ]; then
		error=$(echo "$rpm_dump" | sed -ne '/^error:/,$p')
		echo "$error" >&2
		Exit_error err_build_fail;
	fi

	# make small dump cache
	rpm_dump_cache=`echo "$rpm_dump" | awk '
		$2 ~ /^SOURCEURL/ {print}
		$2 ~ /^PATCHURL/  {print}
		$2 ~ /^nosource/ {print}
		$2 ~ /^PACKAGE_/ {print}
	'`

	update_shell_title "cache_rpm_dump: OK!"
}

rpm_dump () {
	if [ -z "$rpm_dump_cache" ] ; then
		echo "internal error: cache_rpm_dump not called!" 1>&2
	fi
	echo "$rpm_dump_cache"
}

get_icons()
{
	update_shell_title "get icons"
	ICONS="`awk '/^Icon:/ {print $2}' ${SPECFILE}`"
	if [ -z "$ICONS" ]; then
		return
	fi

	rpm_dump_cache="kalasaba" NODIST="yes" UPDATE5= get_files $ICONS
}

parse_spec()
{
	update_shell_title "parsing specfile"
	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	# icons are needed for successful spec parse
	get_icons;

	cd $SPECS_DIR
	cache_rpm_dump

	if [ "$NOSRCS" != "yes" ]; then
		SOURCES="`rpm_dump | awk '/SOURCEURL[0-9]+/ {print $3}'`"
	fi

	if (rpm_dump | grep -qEi ":.*nosource.*1"); then
		FAIL_IF_NO_SOURCES="no"
	fi

	PATCHES="`rpm_dump | awk '/PATCHURL[0-9]+/ {print $3}'`"
	ICONS="`awk '/^Icon:/ {print $2}' ${SPECFILE}`"
	PACKAGE_NAME=$(rpm_dump | awk '$2 == "PACKAGE_NAME" { print $3}')
	PACKAGE_VERSION=$(rpm_dump | awk '$2 == "PACKAGE_VERSION" { print $3}')
	PACKAGE_RELEASE=$(rpm_dump | awk '$2 == "PACKAGE_RELEASE" { print $3}')

	if [ -n "$BE_VERBOSE" ]; then
		echo "- Sources :  `nourl $SOURCES`"
		if [ -n "$PATCHES" ]; then
			echo "- Patches :  `nourl $PATCHES`"
		else
			echo "- Patches :  *no patches needed*"
		fi
		if [ -n "$ICONS" ]; then
			echo "- Icon    :  `nourl $ICONS`"
		else
			echo "- Icon    :  *no package icon*"
		fi
		echo "- Name    : $PACKAGE_NAME"
		echo "- Version : $PACKAGE_VERSION"
		echo "- Release : $PACKAGE_RELEASE"
	fi

	update_shell_title "parse_spec: OK!"
}

Exit_error()
{
	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	cd "$__PWD"

	case "$1" in
		"err_no_spec_in_cmdl" )
			remove_build_requires
			echo "ERROR: spec file name not specified.";
			exit 2 ;;
		"err_no_spec_in_repo" )
			remove_build_requires
			echo "Error: spec file not stored in CVS repo.";
			exit 3 ;;
		"err_no_source_in_repo" )
			remove_build_requires
			echo "Error: some source, patch or icon files not stored in CVS repo. ($2)";
			exit 4 ;;
		"err_build_fail" )
			remove_build_requires
			echo "Error: package build failed. (${2:-no more info})";
			exit 5 ;;
		"err_no_package_data" )
			remove_build_requires
			echo "Error: couldn't get out package name/version/release from spec file."
			exit 6 ;;
		"err_tag_exists" )
			remove_build_requires
			echo "Tag ${2} already exists (spec release: ${3}).";
			exit 9 ;;
		"err_fract_rel" )
			remove_build_requires
			echo "Release ${2} not integer and not a snapshot.";
			exit 10 ;;
		"err_branch_exists" )
			remove_build_requires
			echo "Tree branch already exists (${2}).";
			exit 11 ;;

	esac
   echo "Unknown error."
   exit 100
}

init_builder()
{
	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	if [ "$NOINIT" != "yes" ] ; then
		SOURCE_DIR="`eval $RPM $RPMOPTS --eval '%{_sourcedir}'`"
		SPECS_DIR="`eval $RPM $RPMOPTS --eval '%{_specdir}'`"
	else
		SOURCE_DIR="."
		SPECS_DIR="."
	fi

	__PWD="`pwd`"
}

get_spec()
{

	update_shell_title "get_spec"

	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	cd "$SPECS_DIR"
	if [ ! -f "$SPECFILE" ]; then
		SPECFILE="`basename $SPECFILE .spec`.spec";
	fi
	if [ "$NOCVSSPEC" != "yes" ]; then

		if [ ! -s CVS/Root -a "$NOCVSSPEC" != "yes" ]; then
			echo "Warning: No CVS access defined - using local .spec file"
			NOCVSSPEC="yes"
		fi

		cvsup "$SPECFILE" || Exit_error err_no_spec_in_repo
	fi

	if [ ! -f "$SPECFILE" ]; then
		Exit_error err_no_spec_in_repo;
	fi

	if [ "$CHMOD" = "yes" -a -n "$SPECFILE" ]; then
		chmod $CHMOD_MODE $SPECFILE
	fi
	unset OPTIONS
	[ -n "$DONT_PRINT_REVISION" ] || grep -E -m 1 "^#.*Revision:.*Date" $SPECFILE

	set_spec_target
}

find_mirror()
{
	cd "$SPECS_DIR"
	local url="$1"
	if [ ! -f "mirrors" -a "$NOCVSSPEC" != "yes" ] ; then
		cvs update mirrors >&2
	fi

	IFS="|"
	local origin mirror name rest ol prefix
	while read origin mirror name rest; do
		# skip comments and empty lines
		if [ -z "$origin" ] || [[ $origin == \#* ]]; then
			continue
		fi
		ol=`echo -n "$origin"|wc -c`
		prefix="`echo -n "$url" | head -c $ol`"
		if [ "$prefix" = "$origin" ] ; then
			suffix="`echo "$url"|cut -b $((ol+1))-`"
			echo -n "$mirror$suffix"
			return 0
		fi
	done < mirrors
	echo "$url"
}

src_no ()
{
	cd $SPECS_DIR
	rpm_dump | \
	grep "SOURCEURL[0-9]*[ 	]*$1""[ 	]*$" | \
	sed -e 's/.*SOURCEURL\([0-9][0-9]*\).*/\1/' | \
	head -n 1 | xargs
}

src_md5 ()
{
	[ X"$NO5" = X"yes" ] && return
	no=$(src_no "$1")
	[ -z "$no" ] && return
	cd $SPECS_DIR
	spec_rev=$(grep $SPECFILE CVS/Entries 2>/dev/null | sed -e s:/$SPECFILE/:: -e s:/.*::)
	if [ -z "$spec_rev" ]; then
		spec_rev="$(head -n 1 $SPECFILE | sed -e 's/.*\$Revision: \([0-9.]*\).*/\1/')"
	fi
	spec="$SPECFILE[0-9.,]*,$(echo $spec_rev | sed 's/\./\\./g')"
	md5=$(grep -s -v '^#' additional-md5sums | \
	grep -E "[ 	]$(basename "$1")[ 	]+${spec}([ 	,]|\$)" | \
	sed -e 's/^\([0-9a-f]\{32\}\).*/\1/' | \
	grep -E '^[0-9a-f]{32}$')
	if [ X"$md5" = X"" ] ; then
		source_md5=`grep -i "#[ 	]*Source$no-md5[ 	]*:" $SPECFILE | sed -e 's/.*://'`
		if [ ! -z "$source_md5" ] ; then
			echo $source_md5;
		else
			# we have empty SourceX-md5, but it is still possible
			# that we have NoSourceX-md5 AND NoSource: X
			nosource_md5=`grep -i "#[	 ]*NoSource$no-md5[	 ]*:" $SPECFILE | sed -e 's/.*://'`
			if [ ! -z "$nosource_md5" -a ! X"`grep -i "^NoSource:[	 ]*$no$" $SPECFILE`" = X"" ] ; then
				echo $nosource_md5;
			fi;
		fi;
	else
		if [ $(echo "$md5" | wc -l) != 1 ] ; then
			echo "$SPECFILE: more then one entry in additional-md5sums for $1" 1>&2
		fi
		echo "$md5" | tail -n 1
	fi
}

distfiles_path ()
{
	echo "by-md5/$(src_md5 "$1" | sed -e 's|^\(.\)\(.\)|\1/\2/&|')/$(basename "$1")"
}

distfiles_url ()
{
	echo "$PROTOCOL$DISTFILES_SERVER/distfiles/$(distfiles_path "$1")"
}

distfiles_attic_url ()
{
	echo "$PROTOCOL$ATTICDISTFILES_SERVER/distfiles/Attic/$(distfiles_path "$1")"
}

good_md5 ()
{
	md5=$(src_md5 "$1")
	[ "$md5" = "" ] || \
	[ "$md5" = "$(md5sum $(nourl "$1") 2> /dev/null | sed -e 's/ .*//')" ]
}

good_size ()
{
	size="$(find $(nourl "$1") -printf "%s" 2>/dev/null)"
	[ -n "$size" -a "$size" -gt 0 ]
}

cvsignore_df ()
{
	if [ "$CVSIGNORE_DF" != "yes" ]; then
		return
	fi
	cvsignore=${SOURCE_DIR}/.cvsignore
	if ! grep -q "^$1\$" $cvsignore 2> /dev/null; then
		echo "$1" >> $cvsignore
	fi
}

cvsup()
{
	update_shell_title "cvsup"
	local OPTIONS="up "
	if [ -n "$CVSROOT" ]; then
		OPTIONS="-d $CVSROOT $OPTIONS"
	fi

	if [ -z "$CVSDATE" -a -z "$CVSTAG" ]; then
		OPTIONS="$OPTIONS -A"
	else
		if [ -n "$CVSDATE" ]; then
			OPTIONS="$OPTIONS -D $CVSDATE"
		fi
		if [ -n "$CVSTAG" ]; then
			OPTIONS="$OPTIONS -r $CVSTAG"
		fi
	fi

	local result=1
	local retries_counter=0
	if [ $# = 1 ]; then
		update_shell_title "cvsup: $*"
	else
		update_shell_title "cvsup: $# files"
	fi
	while [ "$result" != "0" -a "$retries_counter" -le "$CVS_RETRIES" ]; do
		retries_counter=$(( $retries_counter + 1 ))
		output=$(LC_ALL=C cvs $OPTIONS "$@" 2>&1)
		result=$?
		[ -n "$output" ] && echo "$output"
		if (echo "$output" | grep -qE "(Cannot connect to|connect to .* failed|Connection reset by peer|Connection timed out|Unknown host)") && [ "$result" -ne "0" -a "$retries_counter" -le "$CVS_RETRIES" ]; then
			echo "Trying again [$*]... ($retries_counter)"
			update_shell_title "cvsup: retry #$retries_counter"
			sleep 2
			continue
		else
			break
		fi
	done
	update_shell_title "cvsup: done!"
	return $result
}

get_files()
{
	update_shell_title "get_files"

	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	if [ $# -gt 0 ]; then
		cd "$SOURCE_DIR"

		if [ ! -s CVS/Root -a "$NOCVS" != "yes" ]; then
			echo "Warning: No CVS access defined for SOURCES"
			NOCVS="yes"
		fi

		local nc=0
		local get_files_cvs=""
		for i in "$@"; do
			nc=$((nc + 1))
			local cvsup=0
			SHELL_TITLE_PREFIX="get_files[$nc/$#]"
			update_shell_title "$i"
			local fp=`nourl "$i"`
			if [ -f "$fp" ] && [ "$SKIP_EXISTING_FILES" = "yes" ]; then
				continue
			fi
			if [ -n "$UPDATE5" ]; then
				if [ -n "$ADD5" ]; then
					[ "$fp" = "$i" ] && continue
					grep -qiE '^#[ 	]*Source'$(src_no $i)'-md5[ 	]*:' $SPECS_DIR/$SPECFILE && continue
				else
					grep -qiE '^#[ 	]*Source'$(src_no $i)'-md5[ 	]*:' $SPECS_DIR/$SPECFILE || continue
				fi
			fi
			FROM_DISTFILES=0
			if [ ! -f "$fp" ] || [ $ALWAYS_CVSUP = "yes" ]; then
				if echo $i | grep -vE '(http|ftp|https|cvs|svn)://' | grep -qE '\.(gz|bz2)$']; then
					echo "Warning: no URL given for $i"
				fi

				if [ -z "$NODIST" ] && [ -n "$(src_md5 "$i")" ]; then
					if good_md5 "$i" && good_size "$i"; then
						echo "$(nourl "$i") having proper md5sum already exists"
						continue
					fi
					target="$fp"
					url=$(distfiles_url "$i")
					url_attic=$(distfiles_attic_url "$i")
					FROM_DISTFILES=1
					if [ "`echo $url | grep -E '^(\.|/)'`" ]; then
						update_shell_title "${GETLOCAL%% *}: $url"
						${GETLOCAL} $url $target
					else
						if [ -z "$NOMIRRORS" ]; then
							url="`find_mirror "$url"`"
						fi
						update_shell_title "${GETURI%% *}: $url"
						${GETURI} ${OUTFILEOPT} "$target" "$url" || \
						if [ "`echo $url | grep -E 'ftp://'`" ]; then
							update_shell_title "${GETURI2%% *}: $url"
							${GETURI2} ${OUTFILEOPT} "$target" "$url"
						fi
					fi
					if ! test -s "$target"; then
						rm -f "$target"
						if [ `echo $url_attic | grep -E '^(\.|/)'` ]; then
							update_shell_title "${GETLOCAL%% *}: $url_attic"
							${GETLOCAL} $url_attic $target
						else
							if [ -z "$NOMIRRORS" ]; then
								url_attic="`find_mirror "$url_attic"`"
							fi
							update_shell_title "${GETURI%% *}: $url_attic"
							${GETURI} ${OUTFILEOPT} "$target" "$url_attic" || \
							if [ "`echo $url_attic | grep -E 'ftp://'`" ]; then
								update_shell_title "${GETURI2%% *}: $url_attic"
								${GETURI2} ${OUTFILEOPT} "$target" "$url_attic"
							fi
						fi
					fi
					if test -s "$target"; then
						cvsignore_df $target
					else
						rm -f "$target"
						FROM_DISTFILES=0
					fi
				elif [ "$NOCVS" != "yes" -a -z "$(src_md5 "$i")" ]; then
					if [ $# -gt 1 ]; then
						get_files_cvs="$get_files_cvs $fp"
						update_shell_title "$fp (will cvs up later)"
						cvsup=1
					else
						cvsup $fp
					fi
				fi

				if [ -z "$NOURLS" ] && [ ! -f "$fp" -o -n "$UPDATE" ] && [ "`echo $i | grep -E 'ftp://|http://|https://'`" ]; then
					if [ -z "$NOMIRRORS" ]; then
						im="`find_mirror "$i"`"
					else
						im="$i"
					fi
					update_shell_title "${GETURI%% *}: $im"
					${GETURI} "$im" || \
					if [ "`echo $im | grep -E 'ftp://'`" ]; then
						update_shell_title "${GETURI2%% *}: $im"
						${GETURI2} "$im"
					fi
				fi

				if [ "$cvsup" = 1 ]; then
					continue
				fi

			fi
			srcno=$(src_no $i)
			if [ ! -f "$fp" -a "$FAIL_IF_NO_SOURCES" != "no" ]; then
				Exit_error err_no_source_in_repo $i;
			elif [ -n "$UPDATE5" ] && \
				( ( [ -n "$ADD5" ] && echo $i | grep -q -E 'ftp://|http://|https://' && \
				[ -z "$(grep -E -i '^NoSource[ 	]*:[ 	]*'$i'([ 	]|$)' $SPECS_DIR/$SPECFILE)" ] ) || \
				grep -q -i -E '^#[ 	]*source'$(src_no $i)'-md5[ 	]*:' $SPECS_DIR/$SPECFILE )
			then
				echo "Updating source-$srcno md5."
				md5=$(md5sum "$fp" | cut -f1 -d' ')
				perl -i -ne '
				print unless /^\s*#\s*Source'$srcno'-md5\s*:/i;
				print "# Source'$srcno'-md5:\t'$md5'\n"
				if /^Source'$srcno'\s*:\s+/;
				' \
				$SPECS_DIR/$SPECFILE
			fi

			if good_md5 "$i" && good_size "$i"; then
				:
			elif [ "$FROM_DISTFILES" = 1 ]; then
				# wrong md5 from distfiles: remove the file and try again
				# but only once ...
				echo "MD5 sum mismatch. Trying full fetch."
				FROM_DISTFILES=2
				rm -f $target
				update_shell_title "${GETURI%% *}: $url"
				${GETURI} ${OUTFILEOPT} "$target" "$url" || \
				if [ "`echo $url | grep -E 'ftp://'`" ]; then
					update_shell_title "${GETURI2%% *}: $url"
					${GETURI2} ${OUTFILEOPT} "$target" "$url"
				fi
				if ! test -s "$target"; then
					rm -f "$target"
					update_shell_title "${GETURI%% *}: $url_attic"
					${GETURI} ${OUTFILEOPT} "$target" "$url_attic" || \
					if [ "`echo $url_attic | grep -E 'ftp://'`" ]; then
						update_shell_title "${GETURI2%% *}: $url_attic"
						${GETURI2} ${OUTFILEOPT} "$target" "$url_attic"
					fi
				fi
				test -s "$target" || rm -f "$target"
			fi

			if good_md5 "$i" && good_size "$i" ; then
				:
			else
				echo "MD5 sum mismatch or 0 size.  Use -U to refetch sources,"
				echo "or -5 to update md5 sums, if you're sure files are correct."
				Exit_error err_no_source_in_repo $i
			fi
		done
		SHELL_TITLE_PREFIX=""

		if [ "$get_files_cvs" ]; then
			cvsup $get_files_cvs
		fi

		if [ "$CHMOD" = "yes" ]; then
			CHMOD_FILES="`nourl "$@"`"
			if [ -n "$CHMOD_FILES" ]; then
				chmod $CHMOD_MODE $CHMOD_FILES
			fi
		fi
	fi
}

make_tagver() {
	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	# Check whether first character of PACKAGE_NAME is legal for tag name
	if [ -z "${PACKAGE_NAME##[_0-9]*}" -a -z "$TAG_PREFIX" ]; then
		TAG_PREFIX=tag_
	fi
	TAGVER=$TAG_PREFIX$PACKAGE_NAME-`echo $PACKAGE_VERSION | sed -e "s/\./\_/g" -e "s/@/#/g"`-`echo $PACKAGE_RELEASE | sed -e "s/\./\_/g" -e "s/@/#/g"`
	# Remove #kernel.version_release from TAGVER because tagging sources
	# could occur with different kernel-headers than kernel-headers used at build time.
	TAGVER=$(echo "$TAGVER" | sed -e 's/#.*//g')
	echo -n "$TAGVER"
}

tag_files()
{
	TAG_FILES="$@"

	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	if [ -n "$1$2$3$4$5$6$7$8$9${10}" ]; then
		echo "Version: $PACKAGE_VERSION"
		echo "Release: $PACKAGE_RELEASE"

		TAGVER=`make_tagver`

		if [ "$TAG_VERSION" = "yes" ]; then
			echo "CVS tag: $TAGVER"
		fi
		if [ -n "$TAG" ]; then
			echo "CVS tag: $TAG"
		fi

		OPTIONS="tag -F"
		if [ -n "$CVSROOT" ]; then
			OPTIONS="-d $CVSROOT $OPTIONS"
		fi

		cd "$SOURCE_DIR"
		for i in $TAG_FILES
		do
			# don't tag files stored on distfiles
			[ -n "`src_md5 $i`" ] && continue
			if [ -f "`nourl $i`" ]; then
				if [ "$TAG_VERSION" = "yes" ]; then
					cvs $OPTIONS $TAGVER `nourl $i`
				fi
				if [ -n "$TAG" ]; then
					cvs $OPTIONS $TAG `nourl $i`
				fi
			else
				Exit_error err_no_source_in_repo $i
			fi
		done

		cd "$SPECS_DIR"
		if [ "$TAG_VERSION" = "yes" ]; then
			cvs $OPTIONS $TAGVER $SPECFILE
		fi
		if [ -n "$TAG" ]; then
			cvs $OPTIONS $TAG $SPECFILE
		fi

		unset OPTIONS
	fi
}

branch_files()
{
	TAG=$1
	echo "CVS branch tag: $TAG"
	shift;

	TAG_FILES="$@"

	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	if [ -n "$1$2$3$4$5$6$7$8$9${10}" ]; then

		OPTIONS="tag -b"
		if [ -n "$CVSROOT" ]; then
			OPTIONS="-d $CVSROOT $OPTIONS"
		fi
		cd "$SOURCE_DIR"
		for i in $TAG_FILES
		do
			if [ -f `nourl $i` ]; then
				cvs $OPTIONS $TAG `nourl $i`
			else
				Exit_error err_no_source_in_repo $i
			fi
		done
		cd "$SPECS_DIR"
		cvs $OPTIONS $TAG $SPECFILE

		unset OPTIONS
	fi
}



build_package()
{
	update_shell_title "build_package"
	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	cd "$SPECS_DIR"

	if [ -n "$TRY_UPGRADE" ]; then
		update_shell_title "build_package: try_upgrade"
		if [ -n "$FLOAT_VERSION" ]; then
			TNOTIFY=`./pldnotify.awk $SPECFILE -n` || exit 1
		else
			TNOTIFY=`./pldnotify.awk $SPECFILE` || exit 1
		fi

		TNEWVER=`echo $TNOTIFY | awk '{ match($4,/\[NEW\]/); print $5 }'`

		if [ -n "$TNEWVER" ]; then
			TOLDVER=`echo $TNOTIFY | awk '{ print $3; }'`
			echo "New version found, updating spec file to version " $TNEWVER
			cp -f $SPECFILE $SPECFILE.bak
			chmod +w $SPECFILE
			eval "perl -pi -e 's/Version:\t"$TOLDVER"/Version:\t"$TNEWVER"/gs' $SPECFILE"
			eval "perl -pi -e 's/Release:\t[1-9]{0,4}/Release:\t0.1/' $SPECFILE"
			parse_spec;
			NODIST="yes" UPDATE5="yes" get_files $SOURCES $PATCHES;
			unset TOLDVER TNEWVER TNOTIFY
		fi
	fi
	cd "$SPECS_DIR"

	case "$COMMAND" in
		build )
			BUILD_SWITCH="-ba" ;;
		build-binary )
			BUILD_SWITCH="-bb" ;;
		build-source )
			BUILD_SWITCH="-bs --nodeps" ;;
		build-prep )
			BUILD_SWITCH="-bp --nodeps" ;;
	esac

	update_shell_title "build_package: $COMMAND"
	if [ -n "$LOGFILE" ]; then
		LOG=`eval echo $LOGFILE`
		if [ -d "$LOG" ]; then
			echo "Log file $LOG is a directory."
			echo "Parse error in the spec?"
			Exit_error err_build_fail;
		fi
		if [ -n "$LASTLOG_FILE" ]; then
			echo "LASTLOG=$LOG" > $LASTLOG_FILE
		fi
		RES_FILE=~/tmp/$RPMBUILD-exit-status.$RANDOM
		(time eval ${NICE_COMMAND} $RPMBUILD $BUILD_SWITCH -v $QUIET $CLEAN $RPMOPTS $RPMBUILDOPTS $BCOND $TARGET_SWITCH $SPECFILE; echo $? > $RES_FILE) 2>&1 |tee $LOG
		RETVAL=`cat $RES_FILE`
		rm $RES_FILE
		if [ -n "$LOGDIROK" ] && [ -n "$LOGDIRFAIL" ]; then
			if [ "$RETVAL" -eq "0" ]; then
				mv $LOG $LOGDIROK
			else
				mv $LOG $LOGDIRFAIL
			fi
		fi
	else
		eval ${NICE_COMMAND} $RPMBUILD $BUILD_SWITCH -v $QUIET $CLEAN $RPMOPTS $RPMBUILDOPTS $BCOND $TARGET_SWITCH $SPECFILE
		RETVAL=$?
	fi
	if [ "$RETVAL" -ne "0" ]; then
		if [ -n "$TRY_UPGRADE" ]; then
			echo "\n!!! Package with new version cannot be built automagically\n"
			mv -f $SPECFILE.bak $SPECFILE
		fi
		Exit_error err_build_fail;
	fi
	unset BUILD_SWITCH
}

nourl()
{
	echo "$@" | sed 's#\<\(ftp\|http\|https\|cvs\|svn\)://[^ ]*/##g'
}

install_required_packages()
{
	run_poldek -vi $1
	return $?
}

find_spec_bcond() {
	# taken from find-spec-bcond, but with just getting the list
	local SPEC="$1"
	# quick revert hint: '$RPMBUILD --bcond $SPEC'
	awk -F"\n" '
	/^%changelog/ { exit }
	/_with(out)?_[_a-zA-Z0-9]+/{
		match($0, /_with(out)?_[_a-zA-Z0-9]+/);
		print substr($0, RSTART, RLENGTH);
	}
	/^%bcond_with/{
		match($0, /bcond_with(out)?[ \t]+[_a-zA-Z0-9]+/);
		bcond = substr($0, RSTART +5 , RLENGTH -5);
		gsub(/[ \t]+/,"_",bcond);
		print bcond
	}' $SPEC | LC_ALL=C sort -u
}

set_bconds_values()
{
	update_shell_title "set bcond values"

	AVAIL_BCONDS_WITHOUT=""
	AVAIL_BCONDS_WITH=""
	if `grep -q ^%bcond ${SPECFILE}`; then
		BCOND_VERSION="NEW"
	elif `egrep -q ^#\ *_with ${SPECFILE}`; then
		BCOND_VERSION="OLD"
	else
		return
	fi

	local bcond_avail=$(find_spec_bcond $SPECFILE)

	# expand bconds from ~/.bcondrc
	# The file structure is like gentoo's package.use:
	# ---
	# * -selinux
	# samba -mysql -pgsql
	# w32codec-installer license_agreement
	# php +mysqli
	# ---
	if ([ -f $HOME/.bcondrc ] || ([ -n $HOME_ETC ] && [ -f $HOME_ETC/.bcondrc ])); then
		SN=${SPECFILE%%\.spec}

		local bcondrc=$HOME/.bcondrc
		[ -n $HOME_ETC ] && [ -f $HOME_ETC/.bcondrc ] && bcondrc=$HOME_ETC/.bcondrc

		while read pkg flags; do
			# ignore comments
			[[ "$pkg" == \#* ]] && continue

			# any package or current package?
			if [ "$pkg" = "*" ] || [ "$pkg" = "$PACKAGE_NAME" ] || [ "$pkg" = "$SN" ]; then
				for flag in $flags; do
					local opt=${flag#[+-]}

					# use only flags which are in this package.
					if [[ $bcond_avail = *${opt}* ]]; then
						if [[ $flag = -* ]]; then
							BCOND="$BCOND --without $opt"
						else
							BCOND="$BCOND --with $opt"
						fi
					fi
				done
			fi
		done < $bcondrc
		update_shell_title "parse ~/.bcondrc: DONE!"
	fi

	update_shell_title "parse bconds"
	case "${BCOND_VERSION}" in
		NONE)
			:
			;;
		OLD)
			echo "Warning: This spec has old style bconds. Fix it || die."
			for opt in `echo "$bcond_avail" | grep ^_without_`
			do
				AVAIL_BCOND_WITHOUT=${opt#_without_}
				if [[ "$BCOND" = *--without?${AVAIL_BCOND_WITHOUT}* ]]; then
					AVAIL_BCONDS_WITHOUT="$AVAIL_BCONDS_WITHOUT <$AVAIL_BCOND_WITHOUT>"
				else
					AVAIL_BCONDS_WITHOUT="$AVAIL_BCONDS_WITHOUT $AVAIL_BCOND_WITHOUT"
				fi
			done

			for opt in `echo "$bcond_avail" | grep ^_with_`
			do
				AVAIL_BCOND_WITH=${opt#_with_}
				if [[ "$BCOND" = *--with?${AVAIL_BCOND_WITH}* ]]; then
					AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH <$AVAIL_BCOND_WITH>"
				else
					AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH $AVAIL_BCOND_WITH"
				fi
			done
			;;
		NEW)
			local cond_type="" # with || without
			for opt in $bcond_avail; do
				case "$opt" in
					_without)
						cond_type="without"
						;;
					_with)
						cond_type="with"
						;;
					_without_*)
						AVAIL_BCOND_WITHOUT=${opt#_without_}
						if [[ "$BCOND" = *--without?${AVAIL_BCOND_WITHOUT}* ]]; then
							AVAIL_BCONDS_WITHOUT="$AVAIL_BCONDS_WITHOUT <$AVAIL_BCOND_WITHOUT>"
						else
							AVAIL_BCONDS_WITHOUT="$AVAIL_BCONDS_WITHOUT $AVAIL_BCOND_WITHOUT"
						fi
						;;
					_with_*)
						AVAIL_BCOND_WITH=${opt#_with_}
						if [[ "$BCOND" = *--with?${AVAIL_BCOND_WITH}* ]]; then
							AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH <$AVAIL_BCOND_WITH>"
						else
							AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH $AVAIL_BCOND_WITH"
						fi
						;;
					*)
						case "$cond_type" in
							with)
								cond_type=''
								AVAIL_BCOND_WITH="$opt"
								if [[ "$BCOND" = *--with?${AVAIL_BCOND_WITH}* ]]; then
									AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH <$AVAIL_BCOND_WITH>"
								else
									AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH $AVAIL_BCOND_WITH"
								fi
								;;
							without)
								cond_type=''
								AVAIL_BCOND_WITHOUT="$opt"
								if [[ "$BCOND" = *--without?${AVAIL_BCOND_WITHOUT}* ]]; then
									AVAIL_BCONDS_WITHOUT="$AVAIL_BCONDS_WITHOUT <$AVAIL_BCOND_WITHOUT>"
								else
									AVAIL_BCONDS_WITHOUT="$AVAIL_BCONDS_WITHOUT $AVAIL_BCOND_WITHOUT"
								fi
								;;
						esac
						;;
				esac
			done
			;;
	esac
}

run_sub_builder()
{
	package_name="${1}"
	update_shell_title "run_sub_builder $package_name"
	#
	# No i tutaj bym chcia³ zrobiæ sztuczn± inteligencjê, która spróbuje tego
	# pakieta zbudowaæ. Aktualnie niewiele dziala, bo generalnie nie widze do
	# konca algorytmu... Ale damy rade. :) Na razie po prostu sie wyjebie tak samo
	# jakby nie bylo tego kawalka kodu.
	#
	# Update: Poprawi³em parê rzeczy i zaczê³o generowaæ pakiety spoza zadanej listy.
	#         Jednym s³owem budowanie niespoldkowanych zale¿no¶ci dzia³a w paru przypadkach.
	#
	#
	# y0shi.

	parent_spec_name=''

	# Istnieje taki spec? ${package}.spec
	if [ -f "${SPECS_DIR}/${package}.spec" ]; then
		parent_spec_name=${package}.spec
	elif [ -f "${SPECS_DIR}/`echo ${package_name} | sed -e s,-devel.*,,g -e s,-static,,g`.spec" ]; then
		parent_spec_name="`echo ${package_name} | sed -e s,-devel.*,,g -e s,-static,,g`.spec"
	else
		for provides_line in `grep ^Provides:.*$package  ${SPECS_DIR} -R`
		do
			echo $provides_line
		done
	fi

	if [ "${parent_spec_name}" != "" ]; then
		spawn_sub_builder $parent_spec_name
	fi
	NOT_INSTALLED_PACKAGES="$NOT_INSTALLED_PACKAGES $package_name"
}

spawn_sub_builder()
{
	package_name="${1}"
	update_shell_title "spawn_sub_builder $package_name"

	sub_builder_opts=''
	if [ "${FETCH_BUILD_REQUIRES}" == "yes" ]; then
		sub_builder_opts="${sub_builder_opts} -R"
	fi
	if [ "${REMOVE_BUILD_REQUIRES}" == "nice" ]; then
		sub_builder_opts="${sub_builder_opts} -RB"
	elif [ "${REMOVE_BUILD_REQUIRES}" == "force" ]; then
		sub_builder_opts="${sub_builder_opts} -FRB"
	fi
	if [ "${UPDATE_POLDEK_INDEXES}" == "yes" ]; then
		sub_builder_opts="${sub_builder_opts} -Upi"
	fi

	cd "${SPECS_DIR}"
	./builder ${sub_builder_opts} "$@"
}

remove_build_requires()
{
	if [ "$INSTALLED_PACKAGES" != "" ]; then
		case "$REMOVE_BUILD_REQUIRES" in
			"force")
				run_poldek --noask -ve $INSTALLED_PACKAGES
				;;
			"nice")
				run_poldek --ask -ve $INSTALLED_PACKAGES
				;;
			*)
				echo You may want to manually remove following BuildRequires fetched:
				echo $INSTALLED_PACKAGES
				echo Try poldek -e \`cat `pwd`/.${SPECFILE}_INSTALLED_PACKAGES\`
				;;
		esac
	fi
}

display_bconds()
{
	if [ "$AVAIL_BCONDS_WITH" != "" ] || [ "$AVAIL_BCONDS_WITHOUT" != "" ]; then
		if [ "$BCOND" != "" ]; then
			echo -ne "\nBuilding $SPECFILE with the following conditional flags:\n"
			echo -ne "$BCOND"
		else
			echo -ne "\nNo conditional flags passed"
		fi
		echo -ne "\n\nfrom available:\n"
		echo -ne "--with   :\t$AVAIL_BCONDS_WITH\n--without:\t$AVAIL_BCONDS_WITHOUT\n\n"
	fi
}

display_branches()
{
	if [ "$NOCVSSPEC" != "yes" ]; then
		echo -ne "Available branches: "
		cvs status -v "${SPECFILE}" | awk '!/Sticky Tag:/ && /\(branch:/ { print $1 } ' | xargs
	fi
}

# checks a given list of packages/files/provides agains current rpmdb.
# outputs all dependencies whcih current rpmdb doesn't satisfy.
# input can be either STDIN or parameters
_rpm_prov_check()
{
	local DEPS

	if [ "$#" -gt 0 ]; then
		DEPS="$@"
	else
		DEPS=$(cat)
	fi

	DEPS=$(rpm -q --whatprovides $DEPS 2>&1 | awk '/^(error:|no package provides)/ { print }')

	# packages
	echo "$DEPS" | awk '/^no package provides/ { print $NF }'

	# other deps (files)
	echo "$DEPS" | awk -F: '/^error:.*No such file/{o = $2; gsub("^ file ", "", o); print o}'
}

# checks if given package/files/provides exists in rpmdb.
# inout can be either stdin or parameters
# returns packages wchi hare present in the rpmdb
_rpm_cnfl_check()
{
	local DEPS

	if [ "$#" -gt 0 ]; then
		DEPS="$@"
	else
		DEPS=$(cat)
	fi

	rpm -q --whatprovides $DEPS 2>/dev/null | awk '!/no package provides/ { print }'
}

fetch_build_requires()
{
	if [ "${FETCH_BUILD_REQUIRES}" = "yes" ]; then
		update_shell_title "fetch build requires"
		if [ "$FETCH_BUILD_REQUIRES_RPMGETDEPS" = "yes" ]; then
			local CONF=$(rpm-getdeps $BCOND $SPECFILE 2> /dev/null | awk '/^\-/ { print $3 } ' | _rpm_cnfl_check | xargs)
			local DEPS=$(rpm-getdeps $BCOND $SPECFILE 2> /dev/null | awk '/^\+/ { print $3 } ' | _rpm_prov_check | xargs)

			update_shell_title "poldek: update indexes"
			if [ -n "$CONF" ] || [ -n "$DEPS" ]; then
				$SU_SUDO /usr/bin/poldek -q --update || $SU_SUDO /usr/bin/poldek -q --upa
			fi
			if [ -n "$CONF" ]; then
				update_shell_title "uninstall conflicting packages: $CONF"
				echo "Trying to uninstall conflicting packages ($CONF):"
				$SU_SUDO /usr/bin/poldek --noask --nofollow -ev $CONF
			fi

		while [ "$DEPS" ]; do
				update_shell_title "install deps: $DEPS"
				echo "Trying to install dependencies ($DEPS):"
				local log=.${SPECFILE}_poldek.log
				$SU_SUDO /usr/bin/poldek --caplookup -uGq $DEPS | tee $log
				failed=$(awk -F: '/^error:/{print $2}' $log)
				rm -f $log
				local ok
				if [ -n "$failed" ]; then
					for package in $failed; do
						# FIXME: sanitise, deps could be not .spec files
						spawn_sub_builder -bb $package && ok="$ok $package"
					done
					DEPS="$ok"
				else
					DEPS=""
				fi
		done
			return
		fi

		echo -ne "\nAll packages installed by fetch_build_requires() are written to:\n"
		echo -ne "`pwd`/.${SPECFILE}_INSTALLED_PACKAGES\n"
		echo -ne "\nIf anything fails, you may get rid of them by executing:\n"
		echo "poldek -e \`cat `pwd`/.${SPECFILE}_INSTALLED_PACKAGES\`\n\n"
		echo > `pwd`/.${SPECFILE}_INSTALLED_PACKAGES
		for package_item in `cat $SPECFILE|grep -B100000 ^%changelog|grep -v ^#|grep BuildRequires|grep -v ^-|sed -e "s/^.*BuildRequires://g"|awk '{print $1}'|sed -e s,perl\(,perl-,g -e s,::,-,g -e s,\(.*\),,g -e s,%{,,g -e s,},,g|grep -v OpenGL-devel|sed -e s,sh-utils,coreutils,g -e s,fileutils,coreutils,g -e s,textutils,coreutils,g -e s,kgcc_package,gcc,g -e s,\),,g`
		do
			package_item="`echo $package_item|sed -e s,rpmbuild,rpm-build,g |sed -e s,__perl,perl,g |sed -e s,gasp,binutils-gasp,g -e s,binutils-binutils,binutils,g -e s,apxs,apache,g|sed -e s,apache\(EAPI\)-devel,apache-devel,g -e s,kernel-headers\(netfilter\),kernel-headers,g -e s,awk,mawk,g -e s,mmawk,mawk,g -e s,motif,openmotif,g -e s,openopenmotif,openmotif,g`"
			GO="yes"
			package=`basename "$package_item"|sed -e "s/}$//g"`
			COND_ARCH_TST="`cat $SPECFILE|grep -B1 BuildRequires|grep -B1 $package|grep ifarch|sed -e "s/^.*ifarch//g"`"
			mach=`uname -m`

			COND_TST=`cat $SPECFILE|grep BuildRequires|grep "$package"`
			if `echo $COND_TST|grep -q '^BuildRequires:'`; then
				if [ "$COND_ARCH_TST" != "" ] && [ "`echo $COND_ARCH_TST|sed -e "s/i.86/ix86/g"`" != "`echo $mach|sed -e "s/i.86/ix86/g"`" ]; then
					GO="yes"
				fi
			# bcond:
			else
				COND_NAME=`echo $COND_TST|sed -e s,:BuildRequires:.*$,,g`
				GO=""
				# %{without}
				if `echo $COND_TST|grep -q 'without_'`; then
					COND_NAME=`echo $COND_NAME|sed -e s,^.*without_,,g`
					if `echo $COND_TST|grep -q !`; then
						COND_STATE="with"
					else
						COND_STATE="wout"
					fi
					COND_WITH=`echo $AVAIL_BCONDS_WITH|grep "<$COND_NAME>"`
					COND_WITHOUT=`echo $AVAIL_BCONDS_WITHOUT|grep "<$COND_NAME>"`
					if [ -n "$COND_WITHOUT" ] || [ -z "$COND_WITH" ]; then
						COND_ARGV="wout"
					else
						COND_ARGV="with"
					fi
				# %{with}
				elif `echo $COND_TST|grep -q 'with_'`; then
					COND_NAME=`echo $COND_NAME|sed -e s,^.*with_,,g`
					if `echo $COND_TST|grep -q !`; then
						COND_STATE="wout"
					else
						COND_STATE="with"
					fi
					COND_WITH=`echo $AVAIL_BCONDS_WITH|grep "<$COND_NAME>"`
					COND_WITHOUT=`echo $AVAIL_BCONDS_WITHOUT|grep "<$COND_NAME>"`
					if [ -n "$COND_WITH" ] || [ -z "$COND_WITHOUT" ]; then
						COND_ARGV="with"
					else
						COND_ARGV="wout"
					fi
				fi
				RESULT="${COND_STATE}-${COND_ARGV}"
				case "$RESULT" in
					"with-wout" | "wout-with" )
						GO=""
						;;
					"wout-wout" | "with-with" )
						GO="yes"
						;;
					* )
						echo "Action '$RESULT' was not defined for package '$package_item'"
						GO="yes"
						;;
				esac
			fi

			if [ "$GO" = "yes" ]; then
				if [ "`rpm -q $package|sed -e "s/$package.*/$package/g"`" != "$package" ]; then
					echo "Testing if $package has subrequirements..."
					run_poldek -t -i $package --dumpn=".$package-req.txt"
					if [ -f ".$package-req.txt" ]; then
						for package_name in `cat ".$package-req.txt"|grep -v ^#`
						do
							if [ "$package_name" = "$package" ]; then
								echo -ne "Installing BuildRequired package:\t$package_name\n"
								update_shell_title "Installing BuildRequired package: ${package_name}"
								install_required_packages $package;
							else
								echo -ne "Installing (sub)Required package:\t$package_name\n"
								update_shell_title "Installing (sub)Required package: ${package_name}"
								install_required_packages $package_name;
							fi
							case $? in
								0)
									INSTALLED_PACKAGES="$package_name $INSTALLED_PACKAGES"
									echo $package_name >> `pwd`/.${SPECFILE}_INSTALLED_PACKAGES
									;;
								*)
									echo "Attempting to run spawn sub - builder..."
									echo -ne "Package installation failed:\t$package_name\n"
									run_sub_builder $package_name
									if [ $? -eq 0 ]; then
										install_required_packages $package_name;
										case $? in
											0)
												INSTALLED_PACKAGES="$package_name $INSTALLED_PACKAGES"
												echo $package_name >> `pwd`/.${SPECFILE}_INSTALLED_PACKAGES
												;;
											*)
												NOT_INSTALLED_PACKAGES="$package_name $NOT_INSTALLED_PACKAGES"
												;;
										esac
									fi
									;;
							esac
						done
						rm -f ".$package-req.txt"
					else
						echo "Attempting to run spawn sub - builder..."
						echo -ne "Package installation failed:\t$package\n"
						run_sub_builder $package
						if [ $? -eq 0 ]; then
							install_required_packages $package;
							case $? in
								0)
									INSTALLED_PACKAGES="$package_name $INSTALLED_PACKAGES"
									echo $package_name >> `pwd`/.${SPECFILE}_INSTALLED_PACKAGES
									;;
								*)
									NOT_INSTALLED_PACKAGES="$package_name $NOT_INSTALLED_PACKAGES"
									;;
							esac
						fi
					fi
				else
					echo "Package $package is already installed. BuildRequirement satisfied."
				fi
			fi
		done
		if [ "$NOT_INSTALLED_PACKAGES" != "" ]; then
			echo "Unable to install following packages and their dependencies:"
			for pkg in "$NOT_INSTALLED_PACKAGES"
			do
				echo $pkg
			done
			remove_build_requires
			exit 8
		fi
	fi
}

init_rpm_dir() {

	TOP_DIR="`eval $RPM $RPMOPTS --eval '%{_topdir}'`"
	CVSROOT=":pserver:cvs@$CVS_SERVER:/cvsroot"

	mkdir -p $TOP_DIR/{RPMS,BUILD,SRPMS}
	cd $TOP_DIR
	cvs -d $CVSROOT co SOURCES/.cvsignore SPECS/{mirrors,adapter{,.awk},fetchsrc_request,builder,repackage.sh}

	init_builder

	echo "To checkout *all* .spec files:"
   	echo "- remove $SPECS_DIR/CVS/Entries.Static"
   	echo "- run cvs up in $SPECS_DIR dir"

	echo ""
	echo "To commit with your developer account:"
   	echo "- edit $SPECS_DIR/CVS/Root"
   	echo "- edit $SOURCE_DIR/CVS/Root"
}

#---------------------------------------------
# main()

if [ "$#" = 0 ]; then
	usage;
	exit 1
fi

while test $# -gt 0
do
	case "${1}" in
		-5 | --update-md5 )
			COMMAND="get";
			NODIST="yes"
			NOCVSSPEC="yes"
			UPDATE5="yes"
			shift ;;
		-a5 | --add-md5 )
			COMMAND="get";
			NODIST="yes"
			NOCVS="yes"
			NOCVSSPEC="yes"
			UPDATE5="yes"
			ADD5="yes"
			shift ;;
		-n5 | --no-md5 )
			NO5="yes"
			shift ;;
		-D | --debug )
			DEBUG="yes"; shift ;;
		-V | --version )
			COMMAND="version"; shift ;;
		-a | --as_anon )
			CVSROOT=":pserver:cvs@$CVS_SERVER:/cvsroot"; shift ;;
		-b | -ba | --build )
			COMMAND="build"; shift ;;
		-bb | --build-binary )
			COMMAND="build-binary"; shift ;;
		-bs | --build-source )
			COMMAND="build-source"; shift ;;
		-bp | --build-prep )
			COMMAND="build-prep"; shift ;;
		-B | --branch )
			COMMAND="branch"; shift; TAG="${1}"; shift;;
		-c | --clean )
			CLEAN="--clean --rmspec --rmsource"; shift ;;
		-d | --cvsroot )
			shift; CVSROOT="${1}"; shift ;;
		-g | --get )
			COMMAND="get"; shift ;;
		-h | --help )
			COMMAND="usage"; shift ;;
		--http )
			PROTOCOL="http"; shift ;;
		-l | --logtofile )
			shift; LOGFILE="${1}"; shift ;;
		-ni| --nice )
			shift; DEF_NICE_LEVEL=${1}; shift ;;
		-ske | --skip-existing-files)
			SKIP_EXISTING_FILES="yes"; shift ;;
		-m | --mr-proper )
			COMMAND="mr-proper"; shift ;;
		-nc | --no-cvs )
			NOCVS="yes"; shift ;;
		-ncs | --no-cvs-specs )
			NOCVSSPEC="yes"; shift ;;
		-nd | --no-distfiles )
			NODIST="yes"; shift ;;
		-nm | --no-mirrors )
			NOMIRRORS="yes"; shift ;;
		-nu | --no-urls )
			NOURLS="yes"; shift ;;
		-ns | --no-srcs )
			NOSRCS="yes"; shift ;;
		-ns0 | --no-source0 )
			NOSOURCE0="yes"; shift ;;
		-nn | --no-net )
			NOCVS="yes"
			NOCVSSPEC="yes"
			NODIST="yes"
			NOMIRRORS="yes"
			NOURLS="yes"
			NOSRCS="yes"
			ALWAYS_CVSUP="no"
			shift;;
		--no-init )
			NOINIT="yes"
			shift;;
		--opts )
			shift; RPMOPTS="$RPM_OPTS ${1}"; shift ;;
		--nopatch | -np )
			shift; RPMOPTS="${RPMOPTS} --define \"patch${1} : ignoring patch${1}; exit 1; \""; shift ;;
		--with | --without )
			case $GROUP_BCONDS in
				"yes")
					COND=${1}
					shift
					while ! `echo ${1}|grep -qE '(^-|spec)'`
					do
						BCOND="$BCOND $COND $1"
						shift
					done;;
				"no")
					if [[ "$2" = *,* ]]; then
						for a in $(echo "$2" | tr , ' '); do
							BCOND="$BCOND $1 $a"
						done
					else
						BCOND="$BCOND $1 $2"
					fi
					shift 2 ;;
			esac
			;;
		--target )
			shift; TARGET="${1}"; shift ;;
		--target=* )
			TARGET=$(echo "${1}" | sed 's/^--target=//'); shift ;;
		-q | --quiet )
			QUIET="--quiet"; shift ;;
		--date )
			CVSDATE="${2}"; shift 2 ;;
		-r | --cvstag )
			shift; CVSTAG="${1}"; shift ;;
		-R | --fetch-build-requires)
			FETCH_BUILD_REQUIRES="yes"
			NOT_INSTALLED_PACKAGES=
			shift ;;
		-RB | --remove-build-requires)
			REMOVE_BUILD_REQUIRES="nice"
			shift ;;
		-FRB | --force-remove-build-requires)
			REMOVE_BUILD_REQUIRES="force"
			shift ;;
		-sd | --sources-distfiles)
			COMMAND="list-sources-distfiles"
			shift ;;
		-sdp | --sources-distfiles-paths)
			COMMAND="list-sources-distfiles-paths"
			shift ;;
		-sf | --sources-files)
			COMMAND="list-sources-files"
			shift ;;
		-sp | --sources-paths)
			COMMAND="list-sources-local-paths"
			shift ;;
		-su | --sources-urls)
			COMMAND="list-sources-urls"
			shift ;;
		-Tvs | --tag-version-stable )
			COMMAND="tag";
			TAG="STABLE"
			TAG_VERSION="yes"
			shift;;
		-Tvn | --tag-version-nest )
			COMMAND="tag";
			TAG="NEST"
			TAG_VERSION="yes"
			shift;;
		-Ts | --tag-stable )
			COMMAND="tag";
			TAG="STABLE"
			TAG_VERSION="no"
			shift;;
		-Tn | --tag-nest )
			COMMAND="tag";
			TAG="NEST"
			TAG_VERSION="no"
			shift;;
		-Tv | --tag-version )
			COMMAND="tag";
			TAG=""
			TAG_VERSION="yes"
			shift;;
		-Tp | --tag-prefix )
			TAG_PREFIX="$2"
			shift 2;;
		-tt | --test-tag )
			TEST_TAG="yes"
			shift;;
		-T | --tag )
			COMMAND="tag";
			shift
			TAG="$1"
			TAG_VERSION="no"
			shift;;
		-ir | --integer-release-only )
			INTEGER_RELEASE="yes"
			shift;;
		-U | --update )
			COMMAND="get"
			UPDATE="yes"
			NOCVSSPEC="yes"
			NODIST="yes"
			UPDATE5="yes"
			shift ;;
		-Upi | --update-poldek-indexes )
			UPDATE_POLDEK_INDEXES="yes"
			shift ;;
		--init-rpm-dir)
			COMMAND="init_rpm_dir";
			shift ;;
		-u | --try-upgrade )
			TRY_UPGRADE="1"; shift ;;
		-un | --try-upgrade-with-float-version )
			TRY_UPGRADE="1"; FLOAT_VERSION="1"; shift ;;
		-v | --verbose )
			BE_VERBOSE="1"; shift ;;
		--define)
			shift
			MACRO="${1}"
			VALUE="${2}"
			shift 2
			RPMOPTS="${RPMOPTS} --define \"${MACRO} ${VALUE}\""
			;;
		--show-bconds | -show-bconds | -print-bconds | --print-bconds | -display-bconds | --display-bconds )
			SHOW_BCONDS="yes"
			shift
			;;
		--nodeps)
			shift
			RPMOPTS="${RPMOPTS} --nodeps"
			;;
		-debug)
			RPMBUILDOPTS="${RPMBUILDOPTS} -debug"; shift ;;
		* )
			SPECFILE="${1}"
			# check if specname was passed as specname:cvstag
			if [ "${SPECFILE##*:}" != "${SPECFILE}" ]; then
				CVSTAG="${SPECFILE##*:}";
				SPECFILE="${SPECFILE%%:*}";
			fi
			shift ;;
	esac
done

if [ -n "$DEBUG" ]; then
	set -x;
	set -v;
fi

if [ -n "$TARGET" ]; then
	case "$RPMBUILD" in
		"rpmbuild")
			TARGET_SWITCH="--target $TARGET" ;;
		"rpm")
			TARGET_SWITCH="--target=$TARGET" ;;
	esac
fi

if [ "$SCHEDTOOL" != "no" ]; then
	NICE_COMMAND="$SCHEDTOOL"
else
	NICE_COMMAND="nice -n ${DEF_NICE_LEVEL}"
fi

update_shell_title "$COMMAND"
case "$COMMAND" in
	"build" | "build-binary" | "build-source" | "build-prep" )
		init_builder;
		if [ -n "$SPECFILE" ]; then
			get_spec;
			parse_spec;
			set_bconds_values;
			display_bconds;
			display_branches;
			[ X"$SHOW_BCONDS" = X"yes" ] && exit 0
			fetch_build_requires;
			if [ "$INTEGER_RELEASE" = "yes" ]; then
				echo "Checking release $PACKAGE_RELEASE..."
				if echo $PACKAGE_RELEASE | grep -q '^[^.]*\.[^.]*$' 2>/dev/null ; then
					Exit_error err_fract_rel "$PACKAGE_RELEASE"
				fi
			fi

			if [ -n "$TEST_TAG" ]; then
				TAGVER=`make_tagver`
				echo "Searching for tag $TAGVER..."
				TAGREL=$(cvs status -v $SPECFILE | grep -E "^[[:space:]]*${TAGVER}[[[:space:]]" | sed -e 's#.*(revision: ##g' -e 's#).*##g')
				if [ -n "$TAGREL" ]; then
					Exit_error err_tag_exists "$TAGVER" "$TAGREL"
				fi

				# - do not allow to build from HEAD when XX-branch exists
				TREE_PREFIX=$(echo "$TAG_PREFIX" | sed -e 's#^auto-\([a-zA-Z]\+\)-.*#\1#g')
				if [ "$TREE_PREFIX" != "$TAG_PREFIX" ]; then
					TAG_BRANCH="${TREE_PREFIX}-branch"
					TAG_STATUS=$(cvs status -v $SPECFILE | grep -Ei "${TAG_BRANCH}.+(branch: [0-9.]+)")
					if [ -n "$TAG_STATUS" -a "$CVSTAG" = "HEAD" ]; then
						Exit_error err_branch_exists "$TAG_STATUS"
					fi
				fi
			fi

			if [ -n "$NOSOURCE0" ] ; then
				SOURCES=`echo $SOURCES | xargs | sed -e 's/[^ ]*//'`
			fi
			get_files $SOURCES $PATCHES;
			build_package;
			if [ "$UPDATE_POLDEK_INDEXES" = "yes" -a "$COMMAND" != "build-prep" ]; then
				run_poldek --sdir="${POLDEK_INDEX_DIR}" --mkidxz
			fi
			remove_build_requires;
		else
			Exit_error err_no_spec_in_cmdl;
		fi
		;;
	"branch" )
		init_builder;
		if [ -n "$SPECFILE" ]; then
			get_spec;
			parse_spec;
			get_files $SOURCES $PATCHES;
			branch_files $TAG "$SOURCES $PATCHES $ICONS";
		else
			Exit_error err_no_spec_in_cmdl;
		fi
		;;
	"get" )
		init_builder;
		if [ -n "$SPECFILE" ]; then
			get_spec;
			parse_spec

			if [ -n "$NOSOURCE0" ] ; then
				SOURCES=`echo $SOURCES | xargs | sed -e 's/[^ ]*//'`
			fi
			get_files $SOURCES $PATCHES
		else
			Exit_error err_no_spec_in_cmdl;
		fi
		;;
	"tag" )
		NOURLS=1
		NODIST="yes"
		init_builder;
		if [ -n "$SPECFILE" ]; then
			get_spec;
			parse_spec;

			# don't fetch sources from remote locations
			new_SOURCES=""
			for file in $SOURCES
			do
				[ -n "`src_md5 $file`" ] && continue
				new_SOURCES="$new_SOURCES $file"
			done
			SOURCES="$new_SOURCES"
			get_files $SOURCES $PATCHES;
			tag_files "$SOURCES $PATCHES $ICONS";
		else
			Exit_error err_no_spec_in_cmdl;
		fi
		;;
	"mr-proper" )
		$RPM --clean --rmsource --rmspec --force --nodeps $SPECFILE
		;;
	"list-sources-files" )
		init_builder
		NOCVSSPEC="yes"
		DONT_PRINT_REVISION="yes"
		get_spec
		parse_spec
		SAPS="$SOURCES $PATCHES"
		for SAP in $SAPS ; do
			echo $SAP | awk '{gsub(/.*\//,"") ; print}'
		done
		;;
	"list-sources-urls" )
		init_builder
		NOCVSSPEC="yes"
		DONT_PRINT_REVISION="yes"
		get_spec
		parse_spec
		SAPS="$SOURCES $PATCHES"
		for SAP in $SAPS ; do
			echo $SAP
		done
		;;
	"list-sources-local-paths" )
		init_builder
		NOCVSSPEC="yes"
		DONT_PRINT_REVISION="yes"
		get_spec
		parse_spec
		SAPS="$SOURCES $PATCHES"
		for SAP in $SAPS ; do
			echo $SOURCE_DIR/$(echo $SAP | awk '{gsub(/.*\//,"") ; print }')
		done
		;;
	"list-sources-distfiles-paths" )
		init_builder
		NOCVSSPEC="yes"
		DONT_PRINT_REVISION="yes"
		get_spec
		parse_spec
		SAPS="$SOURCES $PATCHES"
		for SAP in $SAPS ; do
			if [ -n "$(src_md5 "$SAP")" ]; then
				distfiles_path "$SAP"
			fi
		done
		;;
	"list-sources-distfiles" )
		init_builder
		NOCVSSPEC="yes"
		DONT_PRINT_REVISION="yes"
		get_spec
		parse_spec
		SAPS="$SOURCES $PATCHES"
		for SAP in $SAPS ; do
			if [ -n "$(src_md5 "$SAP")" ]; then
				distfiles_url "$SAP"
			fi
		done
		;;
	"init_rpm_dir")
		init_rpm_dir
		;;
	"usage" )
		usage;;
	"version" )
		echo "$VERSION";;
esac
if [ -f "`pwd`/.${SPECFILE}_INSTALLED_PACKAGES" -a "$REMOVE_BUILD_REQUIRES" != "" ]; then
	rm "`pwd`/.${SPECFILE}_INSTALLED_PACKAGES"
fi
cd "$__PWD"

# vi:syntax=sh:ts=4:sw=4
