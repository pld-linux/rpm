#!/bin/sh
# -----------
# $Id$
# Exit codes:
#	0 - succesful
#	1 - help displayed
#	2 - no spec file name in cmdl parameters
#	3 - spec file not stored in repo
#	4 - some source, patch or icon files not stored in repo
#	5 - package build failed
#	6 - spec file with errors
#	7 - wrong source in /etc/poldek.conf
#  8 - Failed installing buildrequirements and subrequirements

# Notes (todo):
#	- builder -u fetches current version first
#	- tries to get new version from distfiles without new md5
#	- after fetching new version doesn't update md5
#	- doesn't get sources for specs with %include /usr/lib/rpm/macros.python
#	  when there's no rpm-pythonprov (rpm's fault, but it's ugly anyway)
#	- as above with %include /usr/lib/rpm/macros.perl and no rpm-perlprov
#	- when Icon: field is present, -5 and -a5 doesn't work

VERSION="\
Build package utility from PLD CVS repository
V 0.11 (C) 1999-2003 Free Penguins".
PATH="/bin:/usr/bin:/usr/sbin:/sbin:/usr/X11R6/bin"

COMMAND="build"

SPECFILE=""
BE_VERBOSE=""
QUIET=""
CLEAN=""
DEBUG=""
NOURLS=""
NOCVS=""
NOCVSSPEC=""
NODIST=""
UPDATE=""
UPDATE5=""
ADD5=""
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
BCOND=""
GROUP_BCONDS="no"

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

DEF_NICE_LEVEL=0

FAIL_IF_NO_SOURCES="yes"

wget --help 2>&1 | grep -q ' \-\-inet ' && WGET_OPTS="$WGET_OPTS --inet"
wget --help 2>&1 | grep -q ' \-\-retry\-connrefused ' && WGET_OPTS="$WGET_OPTS --retry-connrefused"

GETURI="wget --passive-ftp -c -nd -t$WGET_RETRIES $WGET_OPTS"
GETURI2="wget -c -nd -t$WGET_RETRIES $WGET_OPTS"
GETLOCAL="cp -a"

if (rpm --version 2>&1 | grep -q '4.0.[0-2]'); then
	RPM="rpm"
	RPMBUILD="rpm"
else
	RPM="rpm"
	RPMBUILD="rpmbuild"
fi

POLDEK_INDEX_DIR="`$RPM --eval %_rpmdir`/"
POLDEK_SOURCE="cvs"
POLDEK_CMD="/usr/bin/poldek"

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
#
if [ -n "$HOME_ETC" ]; then
	USER_CFG=$HOME_ETC/.builderrc
else
	USER_CFG=~/.builderrc
fi

[ -f $USER_CFG ] && . $USER_CFG

run_poldek()
{
	RES_FILE=~/tmp/poldek-exit-status.$RANDOM
	if [ -n "$LOGFILE" ]; then
		LOG=`eval echo $LOGFILE`
		if [ -n "$LASTLOG_FILE" ]; then
			echo "LASTLOG=$LOG" > $LASTLOG_FILE
		fi
		(nice -n ${DEF_NICE_LEVEL} ${POLDEK_CMD} `while test $# -gt 0; do echo "$1 ";shift;done` ; echo $? > ${RES_FILE})|tee $LOG
		return $exit_pldk
	else
		(nice -n ${DEF_NICE_LEVEL} ${POLDEK_CMD} `while test $# -gt 0; do echo "$1 ";shift;done` ; echo $? > ${RES_FILE}) 1>&2 >/dev/null
		return `cat ${RES_FILE}`
		rm -rf ${RES_FILE}
	fi
}

# Example grep cvs /etc/poldek.conf:
# source = cvs /home/users/yoshi/rpm/RPMS/
if [ "$UPDATE_POLDEK_INDEXES" = "yes" ]; then
	run_poldek -l -n ${POLDEK_SOURCE} 1>&2 > /dev/null
	if [ ! "$?" == "0" ]; then
		echo "Using improper source '${POLDEK_SOURCE}' in /etc/poldek.conf"
		echo "Fix it and try to continue"
		exit 7
	fi
fi

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
[{-Tp|--tag-prefix} <prefix>]
[-nu|--no-urls] [-v|--verbose] [--opts <rpm opts>]
[--with/--without <feature>] [--define <macro> <value>] <package>[.spec]
	
-5, --update-md5    - update md5 comments in spec, implies -nd -ncs
-a5, --add-md5      - add md5 comments to URL sources, implies -nc -nd -ncs
-D, --debug         - enable script debugging mode,
-V, --version       - output builder version
-a, --as_anon       - get files via pserver as cvs@$CVS_SERVER,
-b, -ba, --build    - get all files from CVS repo or HTTP/FTP and build package
                      from <package>.spec,
-bb, --build-binary - get all files from CVS repo or HTTP/FTP and build binary
                      only package from <package>.spec,
-bs, --build-source - get all files from CVS repo or HTTP/FTP and only pack
                      them into src.rpm,
-bp, --build-prep   - execute the %prep phase of <package>.spec,
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
-T <cvstag> , --tag <cvstag>
                    - add cvs tag <cvstag> for files,
-Tvs, --tag-version-stable
                    - add cvs tags STABLE and NAME-VERSION-RELESE for files,
-Tvn, --tag-version-nest
                    - add cvs tags NEST and NAME-VERSION-RELESE for files,
-Ts, --tag-stable
                    - add cvs tag STABLE for files,
-Tn, --tag-nest
                    - add cvs tag NEST for files,
-Tv, --tag-version
                    - add cvs tag NAME-VERSION-RELESE for files,
-Tp, --tag-prefix <prefix>
                    - add <prefix> to NAME-VERSION-RELEASE tags,
-v, --verbose       - be verbose,
-u, --try-upgrade   - check version, and try to upgrade package
-un, --try-upgrade-with-float-version
                    - as above, but allow float version
-U, --update        - refetch sources, don't use distfiles, and update md5 comments
-Upi, --update-poldek-indexes
                    - refresh or make poldek package index files.
--with/--without <feature>
                    - conditional build package depending on %_with_<feature>/
                      %_without_<feature> macro switch.  You may now use
                      --with feat1 feat2 feat3 --without feat4 feat5 --with feat6
                      constructions. Set GROUP_BCONDS to yes to make use of it.
"
}

cache_rpm_dump () {
rpm_dump_cache=`
	case "$RPMBUILD" in
		rpm )
			rpm -bp --nodeps --define 'prep %dump' $BCOND $SPECFILE 2>&1
			;;
		rpmbuild )
			rpmbuild --nodigest --nosignature --define 'prep %dump' $BCOND $SPECFILE 2>&1
			;;
	esac`
}

rpm_dump () {
	if [ -z "$rpm_dump_cache" ] ; then
		echo "internal error: cache_rpm_dump not called!" 1>&2
	fi
	echo "$rpm_dump_cache"
}

parse_spec()
{
	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

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
	PACKAGE_NAME="`$RPM -q --qf '%{NAME}\n' --specfile ${SPECFILE} 2> /dev/null | head -n 1`"
	PACKAGE_VERSION="`$RPM -q --qf '%{VERSION}\n' --specfile ${SPECFILE} 2> /dev/null| head -n 1`"
	PACKAGE_RELEASE="`$RPM -q --qf '%{RELEASE}\n' --specfile ${SPECFILE} 2> /dev/null | head -n 1`"

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
	esac
}

init_builder()
{
	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	SOURCE_DIR="`$RPM --eval '%{_sourcedir}'`"
	SPECS_DIR="`$RPM --eval '%{_specdir}'`"

	__PWD="`pwd`"
}

get_spec()
{
	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	if [ "$NOCVSSPEC" != "yes" ]; then
		cd $SPECS_DIR

		OPTIONS="up "

		if [ -n "$CVSROOT" ]; then
			OPTIONS="-d $CVSROOT $OPTIONS"
		else
			if [ ! -s CVS/Root -a "$NOCVSSPEC" != "yes" ]; then
				echo "warning: No cvs access defined - using local .spec file"
				NOCVSSPEC="yes"
			fi
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

		result=1
		retries_counter=0
		while [ "$result" != "0" -a "$retries_counter" -le "$CVS_RETRIES" ]
		do
			retries_counter=$(( $retries_counter + 1 ))
			output=$(LC_ALL=C cvs $OPTIONS $SPECFILE 2>&1)
			result=$?
			[ -n "$output" ] && echo "$output"
			if [ "$result" -ne "0" ]; then
				if (echo "$output" | grep -qE "(Cannot connect to|connect to .* failed|Connection reset by peer|Connection timed out|Unknown host)") && [ "$retries_counter" -le "$CVS_RETRIES" ]; then
					echo "Trying again [$SPECFILE]... ($retries_counter)"
					sleep 2
					continue
				fi
				Exit_error err_no_spec_in_repo;
			fi
		done
	fi
	if [ ! -f "$SPECFILE" ]; then
		Exit_error err_no_spec_in_repo;
	fi

	if [ "$CHMOD" = "yes" -a -n "$SPECFILE" ]; then
		chmod $CHMOD_MODE $SPECFILE
	fi
	unset OPTIONS
	grep -E -m 1 "^#.*Revision:.*Date" $SPECFILE
}

find_mirror()
{
	cd "$SPECS_DIR"
	url="$1"
	if [ ! -f "mirrors" -a "$NOCVSSPEC" != "yes" ] ; then
		cvs update mirrors >&2
	fi

	IFS="|"
	while read origin mirror name rest
	do
		ol=`echo -n "$origin"|wc -c`
		prefix="`echo -n "$url" | head -c $ol`"
		if [ "$prefix" = "$origin" ] ; then
			suffix="`echo "$url"|cut -b $ol-`"
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
	no=$(src_no "$1")
	[ -z "$no" ] && return
	cd $SPECS_DIR
	spec_rev=$(grep $SPECFILE CVS/Entries | sed -e s:/$SPECFILE/:: -e s:/.*::)
	if [ -z "$spec_rev" ]; then
		spec_rev="$(head -n 1 $SPECFILE | sed -e 's/.*\$Revision: \([0-9.]*\).*/\1/')"
	fi
	spec="$SPECFILE[0-9.,]*,$(echo $spec_rev | sed 's/\./\\./g')"
	md5=$(grep -s -v '^#' additional-md5sums | \
	grep -E "[ 	]$(basename "$1")[ 	]+${spec}([ 	,]|\$)" | \
	sed -e 's/^\([0-9a-f]\{32\}\).*/\1/' | \
	grep -E '^[0-9a-f]{32}$')
	if [ X"$md5" = X"" ] ; then
		grep -i "#[ 	]*Source$no-md5[ 	]*:" $SPECFILE | sed -e 's/.*://' | xargs
	else
		if [ $(echo "$md5" | wc -l) != 1 ] ; then
			echo "$SPECFILE: more then one entry in additional-md5sums for $1" 1>&2
		fi
		echo "$md5" | tail -n 1
	fi
}

distfiles_url ()
{
	echo "$PROTOCOL$DISTFILES_SERVER/by-md5/$(src_md5 "$1" | sed -e 's|^\(.\)\(.\)|\1/\2/&|')/$(basename "$1")"
}

distfiles_attic_url ()
{
	echo "$PROTOCOL$DISTFILES_SERVER/Attic/by-md5/$(src_md5 "$1" | sed -e 's|^\(.\)\(.\)|\1/\2/&|')/$(basename "$1")"
}

good_md5 ()
{
	md5=$(src_md5 "$1")
	[ "$md5" = "" ] || \
	[ "$md5" = "$(md5sum $(nourl "$1") 2> /dev/null | sed -e 's/ .*//')" ]
}

get_files()
{
	GET_FILES="$@"

	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	if [ -n "$1$2$3$4$5$6$7$8$9${10}" ]; then
		cd $SOURCE_DIR

		OPTIONS="up "
		if [ -n "$CVSROOT" ]; then
			OPTIONS="-d $CVSROOT $OPTIONS"
		else
			if [ ! -s CVS/Root -a "$NOCVS" != "yes" ]; then
				echo "warning: No cvs access defined for SOURCES"
				NOCVS="yes"
			fi
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
		for i in $GET_FILES
		do
			if [ -n "$UPDATE5" ]; then
				if [ -n "$ADD5" ]; then
					[ `nourl $i` = "$i" ] && continue
					grep -qiE '^#[ 	]*Source'$(src_no $i)'-md5[ 	]*:' $SPECS_DIR/$SPECFILE && continue
				else
					grep -qiE '^#[ 	]*Source'$(src_no $i)'-md5[ 	]*:' $SPECS_DIR/$SPECFILE || continue
				fi
			fi
			FROM_DISTFILES=0
			if [ ! -f `nourl $i` ] || [ $ALWAYS_CVSUP = "yes" ]; then
				if echo $i | grep -vE '(http|ftp|https|cvs|svn)://' | grep -qE '\.(gz|bz2)$']; then
					echo "Warning: no URL given for $i"
				fi

				if [ -n "$(src_md5 "$i")" ] && [ -z "$NODIST" ]; then
					if good_md5 "$i"; then
						echo "$(nourl "$i") having proper md5sum already exists"
						continue
					fi
					target=$(nourl "$i")
					url=$(distfiles_url "$i")
					url_attic=$(distfiles_attic_url "$i")
					FROM_DISTFILES=1
					if [ `echo $url | grep -E '^(\.|/)'` ]; then
						${GETLOCAL} $url $target
					else
						if [ -z "$NOMIRRORS" ]; then
							url="`find_mirror "$url"`"
						fi
						${GETURI} -O "$target" "$url" || \
						if [ `echo $url | grep -E 'ftp://'` ]; then
							${GETURI2} -O "$target" "$url"
						fi
					fi
					if ! test -s "$target"; then
						rm -f "$target"
						if [ `echo $url_attic | grep -E '^(\.|/)'` ]; then
							${GETLOCAL} $url_attic $target
						else
							if [ -z "$NOMIRRORS" ]; then
								url_attic="`find_mirror "$url_attic"`"
							fi
							${GETURI} -O "$target" "$url_attic" || \
							if [ `echo $url_attic | grep -E 'ftp://'` ]; then
								${GETURI2} -O "$target" "$url_attic"
							fi
						fi
					fi
					if ! test -s "$target"; then
						rm -f "$target"
						FROM_DISTFILES=0
					fi
				elif [ -z "$(src_md5 "$i")" -a "$NOCVS" != "yes" ]; then
					# ( echo $i | grep -qvE '(ftp|http|https)://' ); -- if CVS should be used, but URLs preferred
					result=1
					retries_counter=0
					while [ "$result" != "0" -a "$retries_counter" -le "$CVS_RETRIES" ]
					do
						retries_counter=$(( $retries_counter + 1 ))
						output=$(LC_ALL=C cvs $OPTIONS `nourl $i` 2>&1)
						result=$?
						[ -n "$output" ] && echo "$output"
						if (echo "$output" | grep -qE "(Cannot connect to|connect to .* failed|Connection reset by peer|Connection timed out|Unknown host)") && [ "$result" -ne "0" -a "$retries_counter" -le "$CVS_RETRIES" ]; then
							echo "Trying again [`nourl $i`]... ($retries_counter)"
							sleep 2
							continue
						else
							break
						fi
					done
				fi

				if [ -z "$NOURLS" ] && [ ! -f "`nourl $i`" -o -n "$UPDATE" ] && [ `echo $i | grep -E 'ftp://|http://|https://'` ]; then
					if [ -z "$NOMIRRORS" ]; then
						im="`find_mirror "$i"`"
					else
						im="$i"
					fi
					${GETURI} "$im" || \
					if [ `echo $im | grep -E 'ftp://'` ]; then
						${GETURI2} "$im"
			  		fi
				fi

			fi
			srcno=$(src_no $i)
			if [ ! -f "`nourl $i`" -a "$FAIL_IF_NO_SOURCES" != "no" ]; then
				Exit_error err_no_source_in_repo $i;
			elif [ -n "$UPDATE5" ] && \
				( ( [ -n "$ADD5" ] && echo $i | grep -q -E 'ftp://|http://|https://' && \
				[ -z "$(grep -E -i '^NoSource[ 	]*:[ 	]*'$i'([ 	]|$)' $SPECS_DIR/$SPECFILE)" ] ) || \
				grep -q -i -E '^#[ 	]*source'$(src_no $i)'-md5[ 	]*:' $SPECS_DIR/$SPECFILE )
			then
				echo "Updating source-$srcno md5."
				md5=$(md5sum `nourl $i` | cut -f1 -d' ')
				perl -i -ne '
				print unless /^\s*#\s*Source'$srcno'-md5\s*:/i;
				print "# Source'$srcno'-md5:\t'$md5'\n"
				if /^Source'$srcno'\s*:\s+/;
				' \
				$SPECS_DIR/$SPECFILE
			fi
	
			if good_md5 "$i"; then
				:
			elif [ "$FROM_DISTFILES" = 1 ]; then
				# wrong md5 from distfiles: remove the file and try again
				# but only once ...
				echo "MD5 sum mismatch. Trying full fetch."
				FROM_DISTFILES=2
				rm -f $target
				${GETURI} -O "$target" "$url" || \
				if [ `echo $url | grep -E 'ftp://'` ]; then
					${GETURI2} -O "$target" "$url"
				fi
				if ! test -s "$target"; then
					rm -f "$target"
					${GETURI} -O "$target" "$url_attic" || \
					if [ `echo $url_attic | grep -E 'ftp://'` ]; then
						${GETURI2} -O "$target" "$url_attic"
					fi
				fi
				test -s "$target" || rm -f "$target"
			fi

			if good_md5 "$i"; then
				:
			else
				echo "MD5 sum mismatch.  Use -U to refetch sources,"
				echo "or -5 to update md5 sums, if you're sure files are correct."
				Exit_error err_no_source_in_repo $i
			fi
		done

		if [ "$CHMOD" = "yes" ]; then
			CHMOD_FILES="`nourl $GET_FILES`"
			if [ -n "$CHMOD_FILES" ]; then
				chmod $CHMOD_MODE $CHMOD_FILES
			fi
		fi
		unset OPTIONS
	fi
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
		# Check whether first character of PACKAGE_NAME is legal for tag name
		if [ -z "${PACKAGE_NAME##[_0-9]*}" -a -z "$TAG_PREFIX" ]; then
			TAG_PREFIX=tag_
		fi
		TAGVER=$TAG_PREFIX$PACKAGE_NAME-`echo $PACKAGE_VERSION | sed -e "s/\./\_/g" -e "s/@/#/g"`-`echo $PACKAGE_RELEASE | sed -e "s/\./\_/g" -e "s/@/#/g"`
		# Remove #kernel.version_release from TAGVER because tagging sources
		# could occur with different kernel-headers than kernel-headers used at build time.
		TAGVER=$(echo "$TAGVER" | sed -e 's/#.*//g')
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

		cd $SOURCE_DIR
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

		cd $SPECS_DIR
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
		cd $SOURCE_DIR
		for i in $TAG_FILES
		do
			if [ -f `nourl $i` ]; then
				cvs $OPTIONS $TAG `nourl $i`
			else
				Exit_error err_no_source_in_repo $i
			fi
		done
		cd $SPECS_DIR
		cvs $OPTIONS $TAG $SPECFILE

		unset OPTIONS
	fi
}



build_package()
{
	if [ -n "$DEBUG" ]; then
		set -x;
		set -v;
	fi

	cd $SPECS_DIR

	if [ -n "$TRY_UPGRADE" ]; then
		if [ -n "$FLOAT_VERSION" ]; then
			TNOTIFY=`./pldnotify.awk $SPECFILE -n`
		else
			TNOTIFY=`./pldnotify.awk $SPECFILE`
		fi

		TNEWVER=`echo $TNOTIFY | awk '{ match($4,/\[NEW\]/); print $5 }'`

		if [ -n "$TNEWVER" ]; then
			TOLDVER=`echo $TNOTIFY | awk '{ print $3; }'`
			echo "New version found, updating spec file to version " $TNEWVER
			cp -f $SPECFILE $SPECFILE.bak
			chmod +w $SPECFILE
			eval "perl -pi -e 's/Version:\t"$TOLDVER"/Version:\t"$TNEWVER"/gs' $SPECFILE"
			eval "perl -pi -e 's/Release:\t[1-9]{0,4}/Release:\t1/' $SPECFILE"
			parse_spec;
			get_files "$SOURCES $PATCHES";
			unset TOLDVER TNEWVER TNOTIFY
		fi
	fi
	cd $SPECS_DIR

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
	if [ -n "$LOGFILE" ]; then
		LOG=`eval echo $LOGFILE`
		if [ -n "$LASTLOG_FILE" ]; then
			echo "LASTLOG=$LOG" > $LASTLOG_FILE
		fi
		RES_FILE=~/tmp/$RPMBUILD-exit-status.$RANDOM
		(time nice -n ${DEF_NICE_LEVEL} $RPMBUILD $BUILD_SWITCH -v $QUIET $CLEAN $RPMOPTS $BCOND $SPECFILE; echo $? > $RES_FILE) 2>&1 |tee $LOG
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
		eval nice -n ${DEF_NICE_LEVEL} $RPMBUILD $BUILD_SWITCH -v $QUIET $CLEAN $RPMOPTS $BCOND $SPECFILE
		RETVAL=$?
	fi
	if [ "$RETVAL" -ne "0" ]; then
		if [ -n "$TRY_UPGRADE" ]; then
			echo "\n!!! Package with new version cannot be build automagically\n"
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

set_bconds_values()
{
	AVAIL_BCONDS_WITHOUT=""
	AVAIL_BCONDS_WITH=""
	if `grep -q ^%bcond ${SPECFILE}`; then
		BCOND_VERSION="NEW"
	elif `grep -q bcond ${SPECFILE}`; then
		BCOND_VERSION="OLD"
	else
		BCOND_VERSION="NONE"
	fi
	case "${BCOND_VERSION}" in
		 NONE)
		 	:
			;;
		 OLD)
			echo "Warning: This spec has old style bconds. Fix it || die."
			for opt in `$RPMBUILD --bcond $SPECFILE |grep ^_without_`
			do
				AVAIL_BCOND_WITHOUT=`echo $opt|sed -e "s/^_without_//g"`
				if `echo $BCOND|grep -q -- "--without $AVAIL_BCOND_WITHOUT"`;then
					AVAIL_BCONDS_WITHOUT="$AVAIL_BCONDS_WITHOUT <$AVAIL_BCOND_WITHOUT>"
				else
					AVAIL_BCONDS_WITHOUT="$AVAIL_BCONDS_WITHOUT $AVAIL_BCOND_WITHOUT"
				fi
			done
		
			for opt in `$RPMBUILD --bcond $SPECFILE |grep ^_with_`
			do
				AVAIL_BCOND_WITH=`echo $opt|sed -e "s/^_with_//g"`
				if `echo $BCOND|grep -q -- "--with $AVAIL_BCOND_WITH"`;then
					AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH <$AVAIL_BCOND_WITH>"
				else
					AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH $AVAIL_BCOND_WITH"
				fi
			done
			;;
		NEW)
			cond_type="" # with || without
			for opt in `$RPMBUILD --bcond $SPECFILE`
			do
				case "$opt" in
					_without)
						cond_type="without"
						;;
					_with)
						cond_type="with"
						;;
					*)
						case "$cond_type" in
							with)
								cond_type=''
								AVAIL_BCOND_WITH="$opt"
								if `echo $BCOND|grep -q -- "--with $AVAIL_BCOND_WITH"`;then
									AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH <$AVAIL_BCOND_WITH>"
								else
									AVAIL_BCONDS_WITH="$AVAIL_BCONDS_WITH $AVAIL_BCOND_WITH"
								fi
							 	;;
							without)
								cond_type=''
								AVAIL_BCOND_WITHOUT="$opt"
								if `echo $BCOND|grep -q -- "--without $AVAIL_BCOND_WITHOUT"`;then
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
	echo -ne "Package installation failed:\t$package_name\n"
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
	if [ -f "${SPECS_DIR}${package}.spec" ]; then
		parent_spec_name=${package}.spec
	elif [ -f "${SPECS_DIR}`echo ${package_name}|sed -e s,-devel.*,,g -e s,-static,,g`.spec" ]; then
		parent_spec_name="`echo ${package_name}|sed -e s,-devel.*,,g -e s,-static,,g`.spec"
	else
		for provides_line in `grep ^Provides:.*$package  ${SPECS_DIR} -R`
		do
			echo $provides_line
		done
	fi

	if [ "${parent_spec_name}" != "" ]; then
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
		./builder ${sub_builder_opts} ${parent_spec_name}
	fi
	NOT_INSTALLED_PACKAGES="$NOT_INSTALLED_PACKAGES $package_name"
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
		echo -ne "We are going to build $SPECFILE with the following conditional flags:\n"
		if [ "$BCOND" != "" ]; then
			echo -ne "$BCOND"
		else
			echo -ne "No --with || --without conditions passed to $0!"
		fi
		echo -ne "\n\nfrom available:\n\n"
		echo -ne "--with   :\t$AVAIL_BCONDS_WITH\n--without:\t$AVAIL_BCONDS_WITHOUT\n\n"
	fi
}

fetch_build_requires()
{
	if [ "${FETCH_BUILD_REQUIRES}" == "yes" ]; then
		echo -ne "\nAll packages installed by fetch_build_requires() are written to:\n"
		echo -ne "`pwd`/.${SPECFILE}_INSTALLED_PACKAGES\n"
		echo -ne "\nIf anything fails, you may get rid of them by executing:\n"
		echo "poldek -e \`cat `pwd`/.${SPECFILE}_INSTALLED_PACKAGES\`\n\n"
		echo > `pwd`/.${SPECFILE}_INSTALLED_PACKAGES
		for package_item in `cat $SPECFILE|grep -B100000 ^%changelog|grep -v ^#|grep BuildRequires|grep -v ^-|sed -e "s/^.*BuildRequires://g"|awk '{print $1}'|sed -e s,perl\(,perl-,g -e s,::,-,g -e s,\(.*\),,g -e s,%{,,g -e s,},,g|grep -v OpenGL-devel|sed -e s,sh-utils,coreutils,g -e s,fileutils,coreutils,g -e s,kgcc_package,gcc,g -e s,\),,g`
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
					COND_NAME=`echo $COND_NAME|sed -e s,^.*_without_,,g`
					if `echo $COND_TST|grep -q !`; then
						COND_STATE="with"
					else
						COND_STATE="wout"
					fi
					if `echo $AVAIL_BCONDS_WITHOUT|grep -q "<$COND_NAME>"`; then
						COND_ARGV="wout"
					else
						COND_ARGV="with"
					fi
				# %{with}
				elif `echo $COND_TST|grep -q 'with_'`; then
					COND_NAME=`echo $COND_NAME|sed -e s,^.*_with_,,g`
					if `echo $COND_TST|grep -q !`; then
						COND_STATE="wout"
					else
						COND_STATE="with"
					fi					
					if `echo $AVAIL_BCONDS_WITH|grep -q "<$COND_NAME>"`; then
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
								export PROMPT_COMMAND=`echo -ne "\033]0;${SPECFILE}: Installing BuildRequired package: ${package_name}\007"`
								install_required_packages $package;
							else
								echo -ne "Installing (sub)Required package:\t$package_name\n"
								export PROMPT_COMMAND=`echo -ne "\033]0;${SPECFILE}: Installing (sub)Required package: ${package_name}\007"`
								install_required_packages $package_name;
							fi
							case $? in
								0)
									INSTALLED_PACKAGES="$package_name $INSTALLED_PACKAGES"
									echo $package_name >> `pwd`/.${SPECFILE}_INSTALLED_PACKAGES
									;;
								*)
									echo "Attempting to run spawn sub - builder..."
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
		export PROMPT_COMMAND=`echo -ne "\033]0;${SPECFILE}\007"`
		if [ "$NOT_INSTALLED_PACKAGES" != "" ]; then
			echo "Nie uda³o siê zainstalowaæ nastêpuj±cych pakietów i ich zale¿no¶ci:"
			for pkg in "$NOT_INSTALLED_PACKAGES"
			do
				echo $pkg
			done
			remove_build_requires
			exit 8
		fi
	fi
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
		--opts )
			shift; RPMOPTS="${1}"; shift ;;
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
					BCOND="$BCOND $1 $2" ; shift 2 ;;
			esac
			;;
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
		-T | --tag )
			COMMAND="tag";
			shift
			TAG="$1"
			TAG_VERSION="no"
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
		--nodeps)
			shift
			RPMOPTS="${RPMOPTS} --nodeps"
			;;
		* )
			SPECFILE="`basename ${1} .spec`.spec";
			export PROMPT_COMMAND=`echo -ne "\033]0;${SPECFILE}\007"`
			shift ;;
	esac
done

if [ -n "$DEBUG" ]; then
	set -x;
	set -v;
fi

case "$COMMAND" in
	"build" | "build-binary" | "build-source" | "build-prep" )
		init_builder;
		if [ -n "$SPECFILE" ]; then
		get_spec;
		set_bconds_values;
		display_bconds;
		fetch_build_requires;
		parse_spec;

		if [ -n "$FAIL_IF_CHANGED_BUT_NOT_BUMPED" ]; then
			TAGVER=$PACKAGE_NAME-`echo $PACKAGE_VERSION | sed -e "s/\./\_/g" -e "s/@/#/g"`-`echo $PACKAGE_RELEASE | sed -e "s/\./\_/g" -e "s/@/#/g"`
			CURTAGREL=$(cvs status $SPECFILE | grep "Working revision:" | awk '{ print $3 }')
			TAGREL=$(cvs status -v $SPECFILE | grep -E "^[[:space:]]*${TAGVER}[[[:space:]]" | sed -e 's#.*(revision: ##g' -e 's#).*##g')

			if [ -n "$TAGREL" -a "$TAGREL" != "$CURTAGREL" ]; then
				Exit_error err_build_fail "not bumped ver-rel - was already used in rev $TAGREL"
			fi
		fi

		if [ -n "$ICONS" ]; then
			get_files $ICONS;
			parse_spec;
		fi
		if [ -n "$NOSOURCE0" ] ; then
			SOURCES=`echo $SOURCES | xargs | sed -e 's/[^ ]*//'`
		fi
		get_files "$SOURCES $PATCHES";
		build_package;
		if [ "$UPDATE_POLDEK_INDEXES" = "yes" ]; then
			run_poldek --sn ${POLDEK_SOURCE} --mkidx="${POLDEK_INDEX_DIR}/packages.dir.gz"
			run_poldek --sn ${POLDEK_SOURCE} --up
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
			if [ -n "$ICONS" ]; then
				get_files $ICONS
				parse_spec;
			fi
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
			parse_spec;
			if [ -n "$ICONS" ]; then
				get_files $ICONS
				parse_spec;
			fi
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
		NODIST=1
		init_builder;
		if [ -n "$SPECFILE" ]; then
			get_spec;
			parse_spec;
			if [ -n "$ICONS" ]; then
				get_files $ICONS
				parse_spec;
			fi
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
	"usage" )
		usage;;
	"version" )
		echo "$VERSION";;
esac
test -f `pwd`/.${SPECFILE}_INSTALLED_PACKAGES && rm `pwd`/.${SPECFILE}_INSTALLED_PACKAGES
cd "$__PWD"

# vi:syntax=sh:ts=3:sw=4
