#!/bin/sh
#
# Please send bug reports to pzurowski@pld-linux.org or pld-devel-* lists
#
# 2004, GPL 2+
#
# >> PLACE STANDARD GPL DISCLAIMER   H E R E .  <<
#
CONFIG=/etc/sysconfig/banner

####################################################### CONFIG ########

# default parameters
##########################

BANNERDIR="/var/lib/banner/"
# egrep regexp
EXCLUDEFILES="(rpmnew$|rpmsave$|~$)"
STDOUT="1"  # stdout by default
#STDOUT="2" # stderr by default

# config parameters
##########################

if [ -r $CONFIG ]; then
	. $CONFIG
fi


# override parameters
##########################

ALL_BANNERS=0
BANNERS=""
NOBANNERS=""
BANNER_LIST=""
CHOOSE_NEWER="no"
CHOOSE_OLDER="no"
EXCLUDE_FLAG=0
NEED_BANNER_LIST=0
NEED_MTIME_CHECK=0
NEW_APPEND=0
NEW_BANNER=""
NEW_SHOW=0

case $STDOUT in
	[1-9]) ;;
	*) STDOUT="1" ;;
esac

#################################################### FUNCTIONS ########

Usage() {
	cat << EOF
Usage:	$(basename $0) [options] [banners]
EOF
}

Help() {
	Usage
	cat << EOF
-a, --all       - all banners
-d, --delete    - delete specified banners
-e, --exclude   - exclude following banners (useful with -a)
-h, --help      - show this help
-i, --include   - cancel effect of -e (EXCLUDED banners will remain excluded)
-m, --make      - make a brand-new banner named as following parameter [1] (from stdin)
-M              - same as above, but append if file exists
-n, --names     - show names of the banners
--newer         - all choosen banners should be newer than following parameter in seconds
--older         - all choosen banners should be older than following parameter in seconds
-s, --show      - show specified banners
--stderr        - send banner to stderr instead of stdout (or other)
--stdout        - send banner to stdout instead of stderr (or other)
-u, --usage     - show short help

[1] if there is no slash ('/') in the given name default dir ($BANNERDIR) is used,
    otherwise the one that's specified
EOF
}

Unknown_para() {
	cat << EOF
Unknown parameter $1
EOF
	Help
}

check_banners_mtime() {
	BANNERS="$1"
	OLDER="$2"
	NEWER="$3"
	DATE=$(date +%s)
	for BANNER in $BANNERS;do
		STAT=$(stat -c %Y "$BANNERDIR/$BANNER")
		if [ $OLDER != "no" -a $(( $DATE - $STAT )) -lt $OLDER ]; then
			BANNER=""
		fi
		if [ $NEWER != "no" -a $(( $DATE - $STAT )) -gt $NEWER ]; then
			BANNER=""
		fi
		echo $BANNER
	done
}

delete_banners() {
	BANNERS="$1"
	rm -rf $(get_banner_location_list "$BANNER")
}

get_all_banner_list() {
	ls "$BANNERDIR" | grep -E -v "$EXCLUDEFILES"
}

get_banner_list() {
	BANNERS="$1"
	NOBANNERS="$2"
	for BANNER in $BANNERS; do
		if [ -r "$BANNERDIR/$BANNER" ]; then
			echo $NOBANNERS | grep -q $BANNER || echo $BANNER
		fi
	done
}

get_banner_location_list() {
	BANNERS="$1"
	for BANNER in $BANNERS; do
		echo "$BANNERDIR/$BANNER"
	done
}

make_banner() {
	BANNER="$1"
	SHOW="$2"
	if [ ! -d "${BANNER%/*}" ]; then
		mkdir -p "${BANNER%/*}"
	fi
	data=$(cat)
	if [ $NEW_APPEND -eq 0 ]; then
		echo "$data" > $BANNER
	else
		echo "$data" >> $BANNER
	fi
	if [ $SHOW -eq 1 ]; then
		echo "$data"
	fi
}

show_banner() {
	cat "$BANNERDIR/$1" >&$STDOUT
}

show_banners() {
	for BANNER in $*; do
		show_banner $BANNER
	done
}

######################################################### MAIN ########
while [ -n "$1" ]; do
	case "$1" in
		-a|--all)
			ALL_BANNERS=1
			;;
		-d|--delete)
			NEED_BANNER_LIST=1
			ACTION="delete"
			;;
		-e|--exclude)
			EXCLUDE_FLAG=1
			;;
		-h|--help)
			Help
			exit 0
			;;
		-i|--include)
			EXCLUDE_FLAG=0
			;;
		-m|--make|-M)
			NEED_BANNER_LIST=0
			if [[ "$2" != */* ]]; then
				NEW_BANNER="$BANNERDIR/${2##*/}"
			else
				NEW_BANNER="$2"
			fi
			ACTION="make"
			if [ "$1" = "-M" ]; then
				NEW_APPEND=1
			else
				NEW_APPEND=0
			fi
			if [ -z "$NEW_BANNER" ]; then
				Help
				exit 2
			fi
			shift
			;;
		-n|--names)
			NEED_BANNER_LIST=1
			ACTION="names"
			;;
		--newer)
			NEED_MTIME_CHECK=1
			CHOOSE_NEWER="$2"
			if [ -z "$CHOOSE_NEWER" ]; then
				Help
				exit 2
			fi
			shift
			;;
		--older)
			NEED_MTIME_CHECK=1
			CHOOSE_OLDER="$2"
			if [ -z "$CHOOSE_OLDER" ]; then
				Help
				exit 2
			fi
			shift
			;;
		-s|--show)
			NEED_BANNER_LIST=1
			NEW_SHOW=1
			ACTION="show"
			;;
		--stdout)
			STDOUT="1"
			;;
		--stderr)
			STDOUT="2"
			;;
		-u|--usage)
			Usage
			exit 0
			;;
		-*)
			Unknown_para "$1"
			exit 1
			;;
		*)
			if [ $EXCLUDE_FLAG -eq 0 ]; then
				BANNERS="$BANNERS ${1##*/}"
			else
				NOBANNERS="$NOBANNERS ${1##*/}"
			fi
			;;
	esac
	shift
done

if [ $ALL_BANNERS -ne 0 ]; then
	BANNERS=`get_all_banner_list`
fi
if [ $NEED_BANNER_LIST -ne 0 ]; then
	BANNER_LIST=`get_banner_list "$BANNERS" "$NOBANNERS"`
fi
if [ $NEED_MTIME_CHECK -ne 0 ]; then
	BANNER_LIST=`check_banners_mtime "$BANNER_LIST" "$CHOOSE_OLDER" "$CHOOSE_NEWER"`
fi

case $ACTION in
	"delete")
		delete_banners $BANNER_LIST
		;;
	"make")
		make_banner $NEW_BANNER $NEW_SHOW
		;;
	"names")
		echo $BANNER_LIST
		;;
	"show")
		show_banners $BANNER_LIST
		;;
	"")
		Help
		;;
esac
