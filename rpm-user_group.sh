#!/bin/sh

[ -f /etc/sysconfig/rpm ] && . /etc/sysconfig/rpm
[ -z "$RPM_SCRIPTVERBOSITY" ] && RPM_SCRIPTVERBOSITY=5

# aborts program abnormally
die() {
	local rc=${2:-1}
	if [ "$1" ]; then
		echo >&2 "ERROR: $1"
	else
		echo >&2 "ERROR"
	fi
	exit $rc
}

bannercmd() {
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

testrm() {
	local mode=$1
	local name=$2

	[ "$RPM_USERDEL" != yes ] || [ ! -x /bin/rpm ] && return 1
	[ -z "$name" ] && return 2
	rpm -q --whatprovides "$mode($name)" >/dev/null 2>&1
	# no package Provides it (strange)
	[ $? -ne 0 ] && return 0
	# only current package Provides it
	[ $(rpm -q --whatprovides "$mode($name)" | wc -l) -lt 2 ] && return 0
	return 1
}

groupremove() {
	local name="$1"
	local gid=$(getgid "$name" 2>/dev/null)

	echo "Removing group $name" | $(bannercmd "groupdel-$name")
	/usr/sbin/groupdel $name || :

	# flush nscd cache
	[ ! -x /usr/sbin/nscd ] || /usr/sbin/nscd -i group
}

userremove() {
	local uid=$(id -un "$name" 2>/dev/null)

	echo "Removing user $name" | $(bannercmd "userdel-$name")
	/usr/sbin/userdel $name || :

	# flush nscd cache
	[ ! -x /usr/sbin/nscd ] || /usr/sbin/nscd -i passwd
}

remove() {
	local mode=$1
	local name=$2
	if ! testrm $mode $name; then
		return
	fi

	${mode}remove $name
}

addtogroup() {
	local user="$1"
	local group="$2"
	local uid=$(id -un "$user" 2>/dev/null)
	local gid=$(getgid "$group" 2>/dev/null)

	if [ -z "$gid" ]; then
		if [ "$quiet" ]; then
			return
		else
			die "group $group does not exist"
		fi
	fi

	if [ -z "$uid" ]; then
		if [ "$quiet" ]; then
			return
		else
			die "user $user does not exist"
		fi
	fi

	groups=$(id -n -G $user)
	if [[ " $groups " != *\ $group\ * ]]; then
		echo "Adding user $user to group $group" | $(bannercmd "${MODE}mod-$user")
		for grp in $groups $group; do
			new="$new${new:+,}$grp"
		done
		usermod -G "$new" $user
	fi
}

if [ -x /usr/bin/banner.sh ]; then
	BANNERCMD="/usr/bin/banner.sh "
	BANNERPARA="-s -M user-group.error"
else
	BANNERCMD="cat"
	BANNERPARA=""
fi

if [ "$1" = user -o "$1" = group ]; then
	MODE=$1
	shift
else
	die "Invalid usage"
fi

# quiet mode cames from $ENV
quiet=$quiet

case "$1" in
testrm)
	testrm $MODE $2
	exit $?
	;;

del)
	remove $MODE $2
	exit $?
	;;

addtogroup)
	if [ "$MODE" = "user" ]; then
		if [ -z "$2" -o -z "$3" ]; then
			die "Invalid usage"
		fi
		addtogroup $2 $3
	fi
	;;
*)
	die "Invalid usage" 2
esac
