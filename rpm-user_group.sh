#!/bin/sh

[ -f /etc/sysconfig/rpm ] && . /etc/sysconfig/rpm
[ -z "$RPM_SCRIPTVERBOSITY" ] && RPM_SCRIPTVERBOSITY=5

if [ "$1" = user -o "$1" = group ]; then
	MODE=$1
else
	echo ERROR
	exit 2
fi
shift

testrm()
{
	[ "$RPM_USERDEL" != yes ] && return 1
	[ -z "$1" ] && return 2
	rpm -q --whatprovides "${MODE}($1)" >/dev/null 2>&1
	# no package Provides it (strange)
	[ $? -ne 0 ] && return 0
	# only current package Provides it
	[ `rpm -q --whatprovides "${MODE}($1)" | wc -l` -lt 2 ] && return 0
	return 1
}

if [ "$1" = "testrm" ]; then
	testrm $2
	exit $?
elif [ "$1" = del ]; then
	if testrm $2; then
		[ "$RPM_SCRIPTVERBOSITY" -lt 2 ] || echo "Removing $MODE $2"
		/usr/sbin/${MODE}del $2 || :
	fi
elif [ "$MODE" = "user" -a "$1" = "addtogroup" ]; then
	USER=$2
	GROUP=$3
	GROUPS=`id -n -G $USER | sed -e's/^[^ ]* //;s/ /,/g'`
	if ! echo ",$GROUPS," | grep -q ",$GROUP," ; then
	    [ "$RPM_SCRIPTVERBOSITY" -lt 2 ] || echo "Adding user $USER to group $GROUP"
	    usermod -G "$GROUPS,$GROUP" $USER
	fi
else
	echo ERROR
	exit 2
fi
