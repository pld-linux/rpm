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
V 0.10 (C) 1999-2001 Tomasz K³oczko".

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
ALLWAYS_CVSUP=${ALLWAYS_CVSUP:-"yes"}
if [ -s CVS/Root ]; then
    CVSROOT=$(cat CVS/Root)
else
    CVSROOT=${CVSROOT:-""}
fi
# Example: LOGFILE='../log.$PACKAGE_NAME'
# Yes, you can use variable name! Note _single_ quotes!
LOGFILE=''
CHMOD="yes"
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

DEF_NICE_LEVEL=0

FAIL_IF_NO_SOURCES="yes"

GETURI="wget --passive-ftp -c -nd -t$WGET_RETRIES"
GETURI2="wget -c -nd -t$WGET_RETRIES"

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
	[-q|--quiet] [-r <cvstag>] [{-T--tag <cvstag>]
	[-Tvs|--tag-version-stable] [-Tvn|--tag-version-nest]
	[-Ts|--tag-stable] [-Tn|--tag-nest] [-Tv|--tag-version]
	[-nu|--no-urls] [-v|--verbose] [--opts <rpm opts>]
	[--with/--without <feature>] [--define <macro> <value>] <package>.spec

	-D, --debug	- enable script debugging mode,
	-V, --version	- output builder version
	-a, --as_anon	- get files via pserver as cvs@anoncvs.pld.org.pl,
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
	-nm, --no-mirrors - don't download from mirror, if source URL is given,
	-nu, --no-urls	- don't try to download from FTP/HTTP location,
	-ns, --no-srcs  - don't downland Sources
	-ns0, --no-source0
			- don't downland Source0
	--opts <rpm opts>
			- additional options for rpm
	-q, --quiet	- be quiet,
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
	if [ -n "$CVSTAG" ]; then
	    OPTIONS="$OPTIONS -r $CVSTAG"
	else
	    OPTIONS="$OPTIONS -A"
	fi

	cvs $OPTIONS $SPECFILE
	if [ "$?" -ne "0" ]; then
	    Exit_error err_no_spec_in_repo;
	fi
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
    if [ ! -f "mirrors" ] ; then 
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
	if [ -n "$CVSTAG" ]; then
	    OPTIONS="$OPTIONS -r $CVSTAG"
	else
	    OPTIONS="$OPTIONS -A"
	fi
	for i in $GET_FILES; do
	    if [ ! -f `nourl $i` ] || [ $ALLWAYS_CVSUP = "yes" ]; then
		if echo $i | grep -vE '(http|ftp|https|cvs|svn)://' | grep -qE '\.(gz|bz2)$']; then
		    echo "Warning: no URL given for $i"
		fi
		
		if [ -z "$NOCVS" ]|| [ `echo $i | grep -vE '(ftp|http|https)://'` ]; then
		    cvs $OPTIONS `nourl $i`
		fi
		
		if [ -z "$NOURLS" ]&&[ ! -f "`nourl $i`" ] && [ `echo $i | grep -E 'ftp://|http://|https://'` ]; then
		    if [ -z "$NOMIRRORS" ] ; then 
			i="`find_mirror "$i"`"
		    fi
		    ${GETURI} "$i" || \
			if [ `echo $i | grep -E 'ftp://'` ]; then ${GETURI2} "$i" ; fi
		fi

		if [ ! -f "`nourl $i`" -a "$FAIL_IF_NO_SOURCES" != "no" ]; then
		    Exit_error err_no_source_in_repo $i;
		fi
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
	TAGVER=$PACKAGE_NAME-`echo $PACKAGE_VERSION | sed -e "s/\./\_/g"`-`echo $PACKAGE_RELEASE | sed -e "s/\./\_/g"`
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
    
	TNOTIFY=`./pldnotify.awk $SPECFILE`
	
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
	LOG=`eval echo $LOGFILE`
	eval nice -n ${DEF_NICE_LEVEL} time $RPMBUILD $BUILD_SWITCH -v $QUIET $CLEAN $RPMOPTS $BCOND $SPECFILE 2>&1 | tee $LOG
    else
	eval nice -n ${DEF_NICE_LEVEL} $RPMBUILD $BUILD_SWITCH -v $QUIET $CLEAN $RPMOPTS $BCOND $SPECFILE
    fi

    if [ "$?" -ne "0" ]; then
    
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
	-D | --debug )
	    DEBUG="yes"; shift ;;
	-V | --version )
	    COMMAND="version"; shift ;;
	-a | --as_anon )
	    CVSROOT=":pserver:cvs@anoncvs.pld.org.pl:/cvsroot"; shift ;;
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
	-ncs | --no-cvs-spec )
	    NOCVSSPEC="yes"; shift ;;
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
	-v | --verbose )
	    BE_VERBOSE="1"; shift ;;
	-u | --try-upgrade )
	    TRY_UPGRADE="1"; shift ;;
	--define)
	    shift
	    MACRO="${1}"
	    VALUE="${2}"
	    shift 2
	    RPMOPTS="${RPMOPTS} --define \"${MACRO} ${VALUE}\""
	    ;;
	* )
	    SPECFILE="${1}"; shift ;;
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
		TAGVER=$PACKAGE_NAME-`echo $PACKAGE_VERSION | sed -e "s/\./\_/g"`-`echo $PACKAGE_RELEASE | sed -e "s/\./\_/g"`
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
