#!/bin/sh
# This script reads filenames from STDIN and outputs any relevant requires
# information that needs to be included in the package.
#
# Based on rpm-4.4.2/scripts/find-req.pl
# Authors: Elan Ruusamäe <glen@pld-linux.org>

export PATH="/sbin:/usr/sbin:/bin:/usr/bin:/usr/X11R6/bin"

IGNORE_DEPS="@"
BUILDROOT="/"

# Loop over all args
while :; do
# Break out if there are no more args
	case $# in
	0)
		break
		;;
	esac

# Get the first arg, and shuffle
	option=$1
	shift

# Make all options have two hyphens
	orig_option=$option	# Save original for error messages
	case $option in
	--*) ;;
	-*) option=-$option ;;
	esac

	case $option in
	--buildroot)
		BUILDROOT=$1
		shift
		;;
	--ignore_deps)
		IGNORE_DEPS=$1
		shift
		;;
	--help)
		echo $usage
		exit 0
		;;
	*)
		echo "$0: Unrecognized option: \"$orig_option\"; use --help for usage." >&2
		exit 1
		;;
	esac
done

javaclassversion() {
	local ver
	classver=$(file "$@" | grep -o 'compiled Java class data, version [0-9.]*' | awk '{print $NF}' | sort -u)
	[ "$classver" ] || return
	for v in $classver; do
		echo "java(ClassDataVersion) >= $v"
	done
}

javajarversion() {
	local jar="$1"

	# check only files, symlinks could point outside buildroot
	[ -f "$jar" -a ! -L "$jar" ] || return

	tmp=$(mktemp -d)
	unzip -q -d $tmp $jar >&2
	javaclassversion $(find $tmp -type f -name '*.class')
	rm -rf $tmp
}

for file in $(cat -); do
	case $file in
	*.jar)
		javajarversion "$file"
		unzip -p $file | javadeps --requires --rpmformat --keywords -
	;;
	*.class)
		javaclassversion "$file"
		javadeps --requires --rpmformat --keywords $file
	;;
	esac
done | sort -u | egrep -v \'$IGNORE_DEPS\'
