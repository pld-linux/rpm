#!/bin/sh

[ -f /etc/sysconfig/rpm ] && . /etc/sysconfig/rpm
[ -z "$RPM_SCRIPTVERBOSITY" ] && RPM_SCRIPTVERBOSITY=5

if [ -x /usr/bin/banner.sh ]; then
	BANNERCMD="/usr/bin/banner.sh "
	BANNERPARA="-s -M user-group.error"
else
	BANNERCMD="cat"
	BANNERPARA=""
fi

if [ "$1" = user -o "$1" = group ]; then
	MODE=$1
else
	echo ERROR
	exit 2
fi
shift

bannercmd()
{
	if [ "$BANNERCMD" = cat ]; then
		echo cat
	else
		if [ "$RPM_SCRIPTVERBOSITY" -lt 2 ]; then
			echo "$BANNERCMD -M $1"
		else
			echo "$BANNERCMD -s -M $1"
		fi
	fi
}

testrm()
{
	[ "$RPM_USERDEL" != yes ] || [ ! -x /bin/rpm ] && return 1
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
		echo "Removing $MODE $2" | `bannercmd "${MODE}del-$2"`
		/usr/sbin/${MODE}del $2 || :
		if [ -x /usr/sbin/nscd ]; then
			case "${MODE}" in
			user)
				/usr/sbin/nscd -i passwd
				;;
			group)
				/usr/sbin/nscd -i group
				;;
			esac
		fi
	fi
elif [ "$MODE" = "user" -a "$1" = "addtogroup" ]; then
	user="$2"
	group="$3"
	groups=$(id -n -G $user)
	if [[ " $groups " != *\ $group\ * ]]; then
	    echo "Adding user $user to group $group" | `bannercmd "${MODE}mod-$user"`
		for grp in $groups $group; do
			new="$new${new:+,}$grp"
		done
	    usermod -G "$new" $user
	fi
else
	echo ERROR
	exit 2
fi
