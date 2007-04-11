#!/bin/sh
# This script reads filenames from STDIN and outputs any relevant requires
# information that needs to be included in the package.
#
# Based on rpm-4.4.2/scripts/find-req.pl
# Authors: Elan Ruusamäe <glen@pld-linux.org>

export PATH="/sbin:/usr/sbin:/bin:/usr/bin:/usr/X11R6/bin"

javaclassversion() {
	[ $# -gt 0 ] || return

	local ver
	classver=$(echo "$@" | xargs -r file | grep -o 'compiled Java class data, version [0-9.]*' | awk '{print $NF}' | sort -u)
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

FILES=$(cat -)

find_requires() {
	for file in $FILES; do
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
	done | sort -u
}

find_provides() {
	for file in $FILES; do
		case $file in
		*.jar)
			unzip -p $file | javadeps --provides --rpmformat --keywords --starprov -
		;;
		*.class)
			javadeps --provides --rpmformat --keywords --starprov $file
		;;
		esac
	done | sort -u
}

REQUIRES=$(find_requires)
PROVIDES=$(find_provides)

# This is a little magic trick to get all REQUIRES that are not
# in PROVIDES. While RPM functions correctly when such deps exist,
# they make the metadata a bit bloated.

# Filter out dups from both lists
REQUIRES=$(echo "$REQUIRES" | sort | uniq)
PROVIDES=$(echo "$PROVIDES" | sort | uniq)

#
# Get a list of elements that exist in exactly one of PROVIDES or REQUIRES
#
UNIQ=$(echo "$PROVIDES
$REQUIRES" | sort | uniq -u)

#
# Of those, only choose the ones that are in REQUIRES
#
echo "$UNIQ
$REQUIRES" | sort | uniq -d
