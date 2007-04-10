#!/bin/sh
# This script reads filenames from STDIN and outputs any relevant provides
# information that needs to be included in the package.
#
# Based on rpm-4.4.2/scripts/find-req.pl
# Authors: Elan Ruusamäe <glen@pld-linux.org>

export PATH="/sbin:/usr/sbin:/bin:/usr/bin:/usr/X11R6/bin"

for file in $(cat -); do
	case $file in
	*.jar)
		unzip -p $file | javadeps --provides --rpmformat --keywords --starprov -
	;;
	*.class)
		javadeps --provides --rpmformat --keywords --starprov $file
	;;
	esac
done | sort -u
