#!/bin/sh
# -----------
# $Id$
# Exit codes:
#	0 - succesful
#	1 - help dispayed
#	2 - no spec file name in cmdl parameters
#	3 - spec file not stored in repo
#	4 - some source, patch or icon files not stored in repo
#	5 - package build failed

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
if [ -s CVS/Root ]; then
    CVSROOT=$(cat CVS/Root)
else
    CVSROOT=${CVSROOT:-""}
fi
# Example: LOGFILE='../log.$PACKAGE_NAME'
# Yes, you can use variable name! Note _single_ quotes!
LOGFILE=''

LOGDIR=""
LOGDIROK=""
LOGDIRFAIL=""
LASTLOG_FILE=""
LTAG=""
CHMOD="no"
CHMOD_MODE="0444"
RPMOPTS=""
BCOND=""

PATCHES=""
SOURCES=""
ICONS=""
PACKAGE_RELEASE=""
PACKAGE_VERSION=""
PACKAGE_NAME=""
WGET_RETRIES=${MAX_WGET_RETRIES:-0}
CVS_RETRIES=${MAX_CVS_RETRIES:-1000}

CVSTAG=""
RES_FILE=""

CVS_SERVER="cvs.pld-linux.org"
DISTFILES_SERVER="ftp://distfiles.pld-linux.org"

DEF_NICE_LEVEL=0

FAIL_IF_NO_SOURCES="yes"

GETURI="wget --passive-ftp -c -nd -t$WGET_RETRIES --inet"
GETURI2="wget -c -nd -t$WGET_RETRIES --inet"
GETLOCAL="cp -a"

if (rpm --version 2>&1 | grep -q '4.0.[0-2]'); then
    RPM="rpm"
    RPMBUILD="rpm"
else
    RPM="rpm"
    RPMBUILD="rpmbuild"
fi

if [ -f ~/etc/builderrc ]; then
    . ~/etc/builderrc
elif [ -f ~/.builderrc ]; then
    . ~/.builderrc
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
	[-h|--help] [{-l,--logtofile} <logfile>] [-m|--mr-proper]
	[-q|--quiet] [--date <yyyy-mm-dd> [-r <cvstag>] [{-T--tag <cvstag>]
	[-Tvs|--tag-version-stable] [-Tvn|--tag-version-nest]
	[-Ts|--tag-stable] [-Tn|--tag-nest] [-Tv|--tag-version]
	[-nu|--no-urls] [-v|--verbose] [--opts <rpm opts>]
	[--with/--without <feature>] [--define <macro> <value>] <package>[.spec]

	-5, --update-md5
			- update md5 comments in spec, implies -nd
	-a5, --add-md5	- add md5 comments to URL sources, implies -nc -nd
	-D, --debug	- enable script debugging mode,
	-V, --version	- output builder version
	-a, --as_anon	- get files via pserver as cvs@$CVS_SERVER,
	-b, -ba,
	--build		- get all files from CVS repo or HTTP/FTP and build
			  package from <package>.spec,
	-bb, --build-binary
			- get all files from CVS repo or HTTP/FTP and build
			  binary only package from <package>.spec,
	-bs,
	--build-source	- get all files from CVS repo or HTTP/FTP and only
			  pack them into src.rpm,
	-B, --branch	- add branch
	-c, --clean	- clean all temporarily created files (in BUILD,
			  SOURCES, SPECS and \$RPM_BUILD_ROOT),
	-d <cvsroot>, --cvsroot	<cvsroot>
			- setup \$CVSROOT,
	--define <macro> <value>
			- define a macro <macro> with value <value>,
	-g, --get	- get <package>.spec and all related files from
			  CVS repo or HTTP/FTP,
	-h, --help	- this message,
	-l <logfile>, --logtofile <logfile>
			- log all to file,
	-m, --mr-proper - only remove all files related to spec file and
			  all work resources,
	-nc, --no-cvs	- don't download sources from CVS, if source URL is
			  given,
	-ncs, --no-cvs-specs
			- don't check specs in CVS
	-nd, --no-distfiles
			- don't download from distfiles
	-nm, --no-mirrors - don't download from mirror, if source URL is given,
	-nu, --no-urls	- don't try to download from FTP/HTTP location,
	-ns, --no-srcs  - don't download Sources
	-ns0, --no-source0
			- don't download Source0
	--opts <rpm opts>
			- additional options for rpm
	-q, --quiet	- be quiet,
	--date yyyy-mm-dd
			- build package using resources from specified CVS
			  date,
	-r <cvstag>, --cvstag <cvstag>
			- build package using resources from specified CVS
			  tag,
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
	-v, --verbose	- be verbose,
	-u, --try-upgrade
			- check version, and try to upgrade package
	-un, --try-upgrade-with-float-version
			- as above, but allow float version
	-U, --update
			- refetch sources, don't use distfiles, and update md5 
			  comments
	--with/--without <feature>
			- conditional build package depending on
			  %_with_<feature>/%_without_<feature> macro
			  switch
"
}

parse_spec()
{
    if [ -n "$DEBUG" ]; then
	set -x;
	set -v;
    fi

    cd $SPECS_DIR
    if [ "$NOSRCS" != "yes" ]; then
	SOURCES="`$RPMBUILD -bp  $BCOND --define 'prep %dump' $SPECFILE 2>&1 | awk '/SOURCEURL[0-9]+/ {print $3}'`"
    fi
    if ($RPMBUILD -bp  $BCOND --define 'prep %dump' $SPECFILE 2>&1 | grep -qEi ":.*nosource.*1"); then
	FAIL_IF_NO_SOURCES="no"
    fi

    PATCHES="`$RPMBUILD -bp  $BCOND --define 'prep %dump' $SPECFILE 2>&1 | awk '/PATCHURL[0-9]+/ {print $3}'`"
    ICONS="`awk '/^Icon:/ {print $2}' ${SPECFILE}`"
    PACKAGE_NAME="`$RPM -q --qf '%{NAME}\n' --specfile ${SPECFILE} 2> /dev/null | head -1`"
    PACKAGE_VERSION="`$RPM -q --qf '%{VERSION}\n' --specfile ${SPECFILE} 2> /dev/null| head -1`"
    PACKAGE_RELEASE="`$RPM -q --qf '%{RELEASE}\n' --specfile ${SPECFILE} 2> /dev/null | head -1`"

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

    cd $__PWD

    case "$1" in
    "err_no_spec_in_cmdl" )
	echo "ERROR: spec file name not specified.";
	exit 2 ;;
    "err_no_spec_in_repo" )
	echo "Error: spec file not stored in CVS repo.";
	exit 3 ;;
    "err_no_source_in_repo" )
	echo "Error: some source, patch or icon files not stored in CVS repo. ($2)";
	exit 4 ;;
    "err_build_fail" )
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

    __PWD=`pwd`
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
	while [ "$result" != "0" -a "$retries_counter" -le "$CVS_RETRIES" ]; do
	    retries_counter=$(( $retries_counter + 1 ))
	    output=$(LC_ALL=C cvs $OPTIONS $SPECFILE 2>&1)
	    result=$?
	    [ -n "$output" ] && echo "$output"
	    if [ "$result" -ne "0" ]; then
		if (echo "$output" | grep -qE "(Cannot connect to|connect to .* failed|Connection reset by peer|Connection timed out)") && [ "$retries_counter" -le "$CVS_RETRIES" ]; then
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

find_mirror(){

    cd "$SPECS_DIR"
    url="$1"
    if [ ! -f "mirrors" -a "$NOCVSSPEC" != "yes" ] ; then
	cvs update mirrors >&2
    fi

    IFS="|"
    while read origin mirror name rest; do
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
    $RPMBUILD -bp  $BCOND --define 'prep %dump' $SPECFILE 2>&1 | \
	grep "SOURCEURL[0-9]*[ 	]*$1""[ 	]*$" | \
	sed -e 's/.*SOURCEURL\([0-9][0-9]*\).*/\1/' | \
	head -1 | xargs
}

src_md5 ()
{
    no=$(src_no "$1")
    [ -z "$no" ] && return
    cd $SPECS_DIR
    spec_rev=$(grep $SPECFILE CVS/Entries | sed -e s:/$SPECFILE/:: -e s:/.*::)
    if [ -z "$spec_rev" ]; then
	spec_rev="$(head -1 $SPECFILE | sed -e 's/.*\$Revision: \([0-9.]*\).*/\1/')"
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
	echo "$md5" | tail -1
    fi
}

distfiles_url ()
{
    echo "$DISTFILES_SERVER/by-md5/$(src_md5 "$1" | sed -e 's|^\(.\)\(.\)|\1/\2/&|')/$(basename "$1")"
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
	for i in $GET_FILES; do
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
		    if [ `echo $url | grep -E '^(\.|/)'` ] ; then
			${GETLOCAL} $url $target
		    else
			if [ -z "$NOMIRRORS" ] ; then
			    url="`find_mirror "$url"`"
			fi
			${GETURI} -O "$target" "$url" || \
			    if [ `echo $url | grep -E 'ftp://'` ]; then
				${GETURI2} -O "$target" "$url"
			    fi
			test -s "$target" || rm -f "$target"
		    fi
		elif [ -z "$(src_md5 "$i")" ] && \
		     ( [ -z "$NOCVS" ] || echo $i | grep -qvE '(ftp|http|https)://' ); then
		    result=1
		    retries_counter=0
		    while [ "$result" != "0" -a "$retries_counter" -le "$CVS_RETRIES" ]; do
			retries_counter=$(( $retries_counter + 1 ))
			output=$(LC_ALL=C cvs $OPTIONS `nourl $i` 2>&1)
			result=$?
			[ -n "$output" ] && echo "$output"
			if (echo "$output" | grep -qE "(Cannot connect to|connect to .* failed|Connection reset by peer|Connection timed out)") && [ "$result" -ne "0" -a "$retries_counter" -le "$CVS_RETRIES" ]; then
				echo "Trying again [`nourl $i`]... ($retries_counter)"
				sleep 2
				continue
			else
				break
			fi
		    done
		fi

		if [ -z "$NOURLS" ] && [ ! -f "`nourl $i`" -o -n "$UPDATE" ] && [ `echo $i | grep -E 'ftp://|http://|https://'` ]; then
		    if [ -z "$NOMIRRORS" ] ; then
			im="`find_mirror "$i"`"
		    else
			im="$i"
		    fi
		    ${GETURI} "$im" || \
			if [ `echo $im | grep -E 'ftp://'` ]; then ${GETURI2} "$im" ; fi
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
	echo $PACKAGE_VERSION
	echo $PACKAGE_RELEASE
	TAGVER=$PACKAGE_NAME-`echo $PACKAGE_VERSION | sed -e "s/\./\_/g" -e "s/@/#/g"`-`echo $PACKAGE_RELEASE | sed -e "s/\./\_/g" -e "s/@/#/g"`
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
	for i in $TAG_FILES; do
	    if [ -f `nourl $i` ]; then
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
	for i in $TAG_FILES; do
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

	if [ -n "FLOAT_VERSION" ]; then
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
    esac
    if [ -n "$LOGFILE" ]; then
	if [ -n "$CVSTAG" ]; then
	    LTAG="r_`echo $CVSTAG|sed -e 's/\./_/g'`_"
	else
	    LTAG=""
	fi
	LOG=`eval echo $LOGFILE`
	if [ -n "$LASTLOG_FILE" ]; then
	    echo "LASTLOG=$LOG" > $LASTLOG_FILE
	fi
	RES_FILE=~/tmp/$RPMBUILD-exit-status.$RANDOM
	(nice -n ${DEF_NICE_LEVEL} time $RPMBUILD $BUILD_SWITCH -v $QUIET $CLEAN $RPMOPTS $BCOND $SPECFILE; echo $? > $RES_FILE) 2>&1 |tee $LOG
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
#---------------------------------------------
# main()

if [ "$#" = 0 ]; then
    usage;
    exit 1
fi

while test $# -gt 0 ; do
    case "${1}" in
	-5 | --update-md5 )
	    COMMAND="get";
	    NODIST="yes"
	    UPDATE5="yes"
	    shift ;;
	-a5 | --add-md5 )
	    COMMAND="get";
	    NODIST="yes"
	    NOCVS="yes"
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
	    BCOND="$BCOND $1 $2" ; shift 2 ;;
	-q | --quiet )
	    QUIET="--quiet"; shift ;;
	--date )
	    CVSDATE="${2}"; shift 2 ;;
	-r | --cvstag )
	    shift; CVSTAG="${1}"; shift ;;
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
	-T | --tag )
	    COMMAND="tag";
	    shift
	    TAG="$1"
	    TAG_VERSION="no"
	    shift;;
	-U | --update )
	    UPDATE="yes"
	    NODIST="yes"
	    UPDATE5="yes"
	    COMMAND="get"
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
	* )
	    SPECFILE="`basename ${1} .spec`.spec"; shift ;;
    esac
done

if [ -n "$DEBUG" ]; then
    set -x;
    set -v;
fi

case "$COMMAND" in
    "build" | "build-binary" | "build-source" )
	init_builder;
	if [ -n "$SPECFILE" ]; then
	    get_spec;
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
	init_builder;
	if [ -n "$SPECFILE" ]; then
	    get_spec;
	    parse_spec;
	    if [ -n "$ICONS" ]; then
		get_files $ICONS
		parse_spec;
	    fi
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

cd $__PWD
