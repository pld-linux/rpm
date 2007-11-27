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

#	echo >&2 "find java requires: ${jar#$RPM_BUILD_ROOT}"

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
		;;
		*.class)
			javaclassversion "$file"
		;;
		esac
	done
}

find_requires | sort -u
