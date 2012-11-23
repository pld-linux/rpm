#!/bin/sh

if [ ! -x /usr/bin/db5.2_load ]; then
	echo "This script needs /usr/bin/db5.2_load to operate."
	exit
fi

if /usr/bin/db5.2_load -r lsn /var/lib/rpm/Packages ; then
	/bin/rm --interactive=never -f /var/lib/rpm/__db.00* >/dev/null 2>/dev/null || :
	/bin/rm --interactive=never -f /var/lib/rpm/log/* >/dev/null 2>/dev/null || :
else
	echo
	echo "rpm database conversion failed!"
	echo
	echo "You have to run:"
	echo
	echo "	/usr/bin/db5.2_load -r lsn /var/lib/rpm/Packages"
	echo "	/bin/rm -f /var/lib/rpm/__db.00*"
	echo "	/bin/rm -f /var/lib/rpm/log/*"
	echo "	/usr/lib/rpm/bin/dbconvert --rebuilddb"
	echo

fi

if ! /usr/lib/rpm/bin/dbconvert --rebuilddb; then
	echo
	echo "rpm database conversion failed!"
	echo "You have to run  /usr/lib/rpm/bin/dbconvert manually"
	echo
fi
