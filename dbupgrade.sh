#!/bin/sh

ROOTDIR=
if [ "$1" = "-r" ]; then
	shift
	ROOTDIR="$1"

	if [ ! -d "$ROOTDIR" ]; then
		echo "Specified root directory ($ROOTDIR) does not exist!"
		echo "Bailing out!"
		exit
	fi
fi

if ! /usr/lib/rpm/rpmdb_reset -r lsn "$ROOTDIR"/var/lib/rpm/Packages ; then
	echo
	echo "rpm database conversion failed!"
	echo
	echo "You have to run:"
	echo
	echo "	/usr/lib/rpm/rpmdb_reset -r lsn /var/lib/rpm/Packages"
	echo "	/bin/rm -f /var/lib/rpm/__db.00*"
	echo "	/bin/rm -f /var/lib/rpm/log/*"
	echo "	/usr/bin/rpmdb --rebuilddb"
	echo
else
	/bin/rm --interactive=never -f "$ROOTDIR"/var/lib/rpm/__db.00* >/dev/null 2>/dev/null || :
	/bin/rm --interactive=never -f "$ROOTDIR"/var/lib/rpm/log/* >/dev/null 2>/dev/null || :

	if ! /usr/bin/rpmdb --rebuilddb ${ROOTDIR:+--root="$ROOTDIR"}; then
		echo
		echo "rpm database conversion failed!"
		echo "You have to run /usr/bin/rpmdb manually"
		echo
	fi
fi
