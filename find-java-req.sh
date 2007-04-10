#!/bin/sh
# This script reads filenames from STDIN and outputs any relevant requires
# information that needs to be included in the package.
#
# Based on rpm-4.4.2/scripts/find-req.pl
# Authors: Elan Ruusamäe <glen@pld-linux.org>

export PATH="/sbin:/usr/sbin:/bin:/usr/bin:/usr/X11R6/bin"

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
done | sort -u
