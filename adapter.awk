#!/bin/awk -f
#
# This is adapter v0.27. Adapter adapts .spec files for PLD.
#
# Copyright (C) 1999-2001 PLD-Team <feedback@pld.org.pl>
# Authors:
# 	Micha³ Kuratczyk <kura@pld.org.pl>
# 	Sebastian Zagrodzki <s.zagrodzki@mimuw.edu.pl>
# 	Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
# 	Artur Frysiak <wiget@pld.org.pl>
# 	Michal Kochanowicz <mkochano@pld.org.pl>
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

BEGIN {
	preamble = 1		# Is it part of preamble? Default - yes
	boc = 2			# Beggining of %changelog
	bod = 0			# Beggining of %description
	tw = 70        		# Descriptions width
	
	# If variable removed, then 1 (for removing it from export)
	removed["LDFLAGS"] = 0
	removed["CFLAGS"] = 0
	removed["CXXFLAGS"] = 0

	# If 1, we are inside of comment block (started with /^#%/)
	comment_block = 0
	
	# File with rpm groups
	"rpm --eval %_sourcedir" | getline groups_file
	groups_file = groups_file "/rpm.groups"
	system("cd `rpm --eval %_sourcedir`; cvs up rpm.groups >/dev/null")

	# Temporary file for changelog section
	changelog_file = ENVIRON["HOME"] "/tmp/adapter.changelog"

	# Load rpm macros
	"rpm --eval %_prefix"	| getline prefix
	"rpm --eval %_bindir"	| getline bindir
	"rpm --eval %_sbindir"	| getline sbindir
	"rpm --eval %_libdir"	| getline libdir
	"rpm --eval %_sysconfdir" | getline sysconfdir
	"rpm --eval %_datadir"	| getline datadir
	"rpm --eval %_includedir" | getline includedir
	"rpm --eval %_mandir"	| getline mandir
	"rpm --eval %_infodir"	| getline infodir
}

# There should be a comment with CVS keywords on the first line of file.
FNR == 1 {
	if (!/# \$Revision:/)	# If this line is already OK?
		print "# $" "Revision:$, " "$" "Date:$"	# No
	else {
		print $0				# Yes
		next		# It is enough for first line
	}
}

# If the latest line matched /%files/
defattr == 1 {
	if ($0 !~ /defattr/)	# If no %defattr
		print "%defattr(644,root,root,755)"	# Add it
	else
		$0 = "%defattr(644,root,root,755)"	# Correct mistakes (if any)
	defattr = 0
}

# Comments
/^#/ && (description == 0) {
	if (/This file does not like to be adapterized!/) {
		print			# print this message
		while (getline)		# print the rest of spec as it is
			print
		do_not_touch_anything = 1 # do not touch anything in END()
		exit 0
	}

	# Generally, comments are printed without touching
	sub(/[ \t]+$/, "")
	print $0
	next
}

# Remove defining _applnkdir (this macro has been included in rpm-3.0.4)
/^%define/ {
	if ($2 == "_applnkdir")
		next
	if ($2 == "date")
		date = 1
}

################
# %description #
################
/^%description/, (/^%[a-z]+/ && !/^%description/) {
	preamble = 0

	if (/^%description/) {
		bod++
		format_line = ""
		format_indent = -1
	}

	# Define _prefix and _mandir if it is X11 application
	if (/^%description$/ && x11 == 1) {
		print "%define\t\t_prefix\t\t/usr/X11R6"
		print "%define\t\t_mandir\t\t%{_prefix}/man\n"
		prefix = "/usr/X11R6"
		x11 = 2
	}
	
	# Format description
	if (description == 1 && !/^%[a-z]+/ && !/^%description/) {
		if (/^[ \t]*$/) {
			format_flush(format_line, format_indent)
			print ""
			format_line = ""
			format_indent = -1
		} else if (/^[ \t]*[-\*][ \t]*/) {
			format_flush(format_line, format_indent)
			match($0, /^[ \t]*/)	
			format_indent = RLENGTH
			match($0, /^[ \t]*[-\*][ \t]/)
			format_line = substr($0, RLENGTH)
		} else 
			format_line = format_line " " $0
		next
	}
 
	if (/^%[a-z]+/ && (!/^%description/ || bod == 2)) {
		if (NF > 3 && $2 == "-l") {
			ll = $1
			for (i = 4; i <= NF; i++)
				ll = ll " " $i
			$0 = ll " -l " $3
		}
		format_flush(format_line, format_indent)
		if (bod == 2) {
			bod = 1
			description = 1
		} else {
			bod = 0
			description = 0
		}
	} else
		description = 1
}

#########
# %prep #
#########
/^%prep/, (/^%[a-z]+$/ && !/^%prep/) {
	preamble = 0
	
	# Add '-q' to %setup
	if (/^%setup/ && !/-q/)
		sub(/^%setup/, "%setup -q")
}

##########
# %build #
##########
/^%build/, (/^%[a-z]+$/ && !/^%build/) {
	preamble = 0

	use_macros()
	
	if (/^automake$/)
		sub(/$/, " -a -c")

	if (/LDFLAGS/) {
		if (/LDFLAGS="-s"/) {
			removed["LDFLAGS"] = 1
			next
		} else {
			split($0, tmp, "LDFLAGS=")
			count = split(tmp[2], flags, "\"")
			if (flags[1] != "" && flags[1] !~ "!?debug") {
				sub(/-s[" ]?/, "%{rpmldflags} ", flags[1])
				$0 = tmp[1] line[1] "LDFLAGS=" flags[1] "\""
				for (i = 2; i < count; i++)
					$0 = $0 flags[i] "\""
			}
		}
	}

	if (/CFLAGS=/)
		if (cflags("CFLAGS") == 0)
			next

	if (/CXXFLAGS=/)
		if (cflags("CXXFLAGS") == 0)
			next
	
	if (/^export /) {
		if (removed["LDFLAGS"])
			sub(" LDFLAGS", "")
		if (removed["CFLAGS"])
			sub(" CFLAGS", "")
		if (removed["CXXFLAGS"])
			sub(" CXXFLAGS", "")
		# Is there still something?
		if (/^export[ ]*$/)
			next
	}
			
}

##########
# %clean #
##########
/^%clean/, (/^%[a-z]+$/ && !/^%clean/) {
	did_clean = 1
}

############
# %install #
############
/^%install/, (/^%[a-z]+$/ && !/^%install/) {
	
	preamble = 0
	
	if (/^[ \t]*rm([ \t]+-[rf]+)*[ \t]+\${?RPM_BUILD_ROOT}?/ && did_rmroot==0) {
		did_rmroot=1
		print "rm -rf $RPM_BUILD_ROOT"
		next
	}

	if (!/^(#?[ \t]*)$/ && !/^%install/ && did_rmroot==0) {
		print "rm -rf $RPM_BUILD_ROOT"
		did_rmroot=1
	}
	
	use_macros()
	
	# 'install -d' instead 'mkdir -p'
	if (/mkdir -p/)
		sub(/mkdir -p/, "install -d")
		
	# No '-u root' or '-g root' for 'install'
	if (/^install/ && /-[ug][ \t]*root/)
		gsub(/-[ug][ \t]*root /, "")
	
	if (/^install/ && /-m[ \t]*644/)
		gsub(/-m[ \t]*644 /, "")
	
	# No lines contain 'chown' or 'chgrp' if owner/group is 'root'
	if (($1 ~ /chown/ && $2 ~ /root\.root/) || ($1 ~ /chgrp/ && $2 ~ /root/))
		next
	
	# No lines contain 'chmod' if it sets the modes to '644'
	if ($1 ~ /chmod/ && $2 ~ /644/)
		next
}

##########
# %files #
##########
/^%files/, (/^%[a-z \-]+$/ && !/^%files/) {
	preamble = 0
	
	if ($0 ~ /^%files/)
		defattr = 1
	
	use_macros()
	use_files_macros()
}

##############
# %changelog #
##############
/^%changelog/, (/^%[a-z]+$/ && !/^%changelog/) {
	preamble = 0
	has_changelog = 1
	# There should be some CVS keywords on the first line of %changelog.
	if (boc == 1) {
		if (!/PLD Team/) {
			print "* %{date} PLD Team <feedback@pld.org.pl>" > changelog_file
			printf "All persons listed below can be reached at " > changelog_file
			print "<cvs_login>@pld.org.pl\n" > changelog_file
			print "$" "Log:$" > changelog_file
		}
		boc = 0
	}
	
	# Define date macro.
	if (boc == 2) {
		if (date == 0) {
			printf "%%define date\t%%(echo `LC_ALL=\"C\"" > changelog_file
			print " date +\"%a %b %d %Y\"`)" > changelog_file
			date = 1
		}
		boc = 1
	}

	sub(/[ \t]+$/, "")
	if (!/^%[a-z]+$/ || /changelog/)
		print > changelog_file
	else
		print
	next
}

###########
# SCRIPTS #
###########
/^%pre/, (/^%[a-z]+$/ && !/^%pre/) {
	preamble = 0
}
/^%post/, (/^%[a-z]+$/ && !/^%post/) {
	preamble = 0
}
/^%preun/, (/^%[a-z]+$/ && !/^%preun/) {
	preamble = 0
}
/^%postun/, (/^%[a-z]+$/ && !/^%postun/) {
	preamble = 0
}

#############
# PREAMBLES #
#############
preamble == 1 {
	# There should not be a space after the name of field
	# and before the colon.
	sub(/[ \t]*:/, ":")
	
	field = tolower($1)
	fieldnlower = $1
	if (field ~ /group(\([^)]+\)):/)
		next
	if (field ~ /group:/) {
		format_preamble()
		sub(/^Utilities\//,"Applications/",$2)
		sub(/^Games/,"Applications/Games",$2)
		sub(/^X11\/Games/,"X11/Applications/Games",$2)
		sub(/^X11\/GNOME\/Development\/Libraries/,"X11/Development/Libraries",$2)
		sub(/^X11\/GNOME\/Applications/,"X11/Applications",$2)
		sub(/^X11\/GNOME/,"X11/Applications",$2)
		sub(/^X11\/Utilities/,"X11/Applications",$2)
		sub(/^X11\/Games\/Strategy/,"X11/Applications/Games/Strategy",$2)
		sub(/^Shells/,"Applications/Shells",$2)

		sub(/^[^ \t]*[ \t]*/,"")
		Grupa = $0

		print "Group:\t\t" Grupa
		if (Grupa ~ /^X11/ && x11 == 0)	# Is it X11 application?
		       x11 = 1

		byl_plik_z_grupami = 0
		byl_opis_grupy = 0
		while ((getline linia_grup < groups_file) > 0) {
			byl_plik_z_grupami = 1
			if (linia_grup == Grupa) {
				byl_opis_grupy = 1
				break
			}
		}

		if (!byl_plik_z_grupami)
			print "######\t\t" groups_file ": no such file"
		else if (!byl_opis_grupy)
			print "######\t\t" "Unknown group!"
		
		close(groups_file)
		next
	}
	
	if (field ~ /packager:|distribution:|docdir:|prefix:/)
		next
	
	if (field ~ /buildroot:/)
		$0 = $1 "%{tmpdir}/%{name}-%{version}-root-%(id -u -n)"

	# Use "License" instead of "Copyright" if it is (L)GPL or BSD
	if (field ~ /copyright:/ && $2 ~ /GPL|BSD/)
		$1 = "License:"
	
	if (field ~ /name:/)
		name = $2

	if (field ~ /version:/)
		version = $2

	if (field ~ /serial:/)
		$1 = "Epoch:"

	# Use %{name} and %{version} in the filenames in "Source:"
	if (field ~ /^source/ || field ~ /patch/) {
		n = split($2, url, /\//)
		if (url[n] ~ /\.gz$/) {
			url[n+1] = ".gz" url[n+1]
			sub(/\.gz$/,"",url[n])
		}
		if (url[n] ~ /\.zip$/) {
			url[n+1] = ".zip" url[n+1]
			sub(/\.zip$/,"",url[n])
		}
		if (url[n] ~ /\.tar$/) {
			url[n+1] = ".tar" url[n+1]
			sub(/\.tar$/,"",url[n])
		}
		if (url[n] ~ /\.patch$/) {
			url[n+1] = ".patch" url[n+1]
			sub(/\.patch$/,"",url[n])
		}
		if (url[n] ~ /\.bz2$/) {
			url[n+1] = ".bz2" url[n+1]
			sub(/\.bz2$/,"",url[n])
		}
		if (url[n] ~ /\.logrotate$/) {
			url[n+1] = ".logrotate" url[n+1]
			sub(/\.logrotate$/,"",url[n])
		}
		if (url[n] ~ /\.pamd$/) {
			url[n+1] = ".pamd" url[n+1]
			sub(/\.pamd$/,"",url[n])
		}

		filename = url[n]
		url[n] = fixedsub(name, "%{name}", url[n])
		if (field ~ /source/) 
			url[n] = fixedsub(version, "%{version}", url[n])
		$2 = fixedsub(filename, url[n], $2)
	}

	if (field ~ /^source:/)
		$1 = "Source0:"	

	if (field ~ /patch:/)
		$1 = "Patch0:"
	
	format_preamble()
	
	if ($1 ~ /%define/) {
		# Do not add %define of _prefix if it already is.
	       	if ($2 ~ /^_prefix/) {
			sub("^"prefix, $3, bindir)
			sub("^"prefix, $3, sbindir)
			sub("^"prefix, $3, libdir)
			sub("^"prefix, $3, datadir)
			sub("^"prefix, $3, includedir)
			prefix = $3
			x11 = 2
		}
		if ($2 ~ /_bindir/ && !/_sbindir/)
			bindir = $3
		if ($2 ~ /_sbindir/)
			sbindir = $3
		if ($2 ~ /_libdir/)
			libdir = $3
		if ($2 ~ /_sysconfdir/)
			sysconfdir = $3
		if ($2 ~ /_datadir/)
			datadir = $3
		if ($2 ~ /_includedir/)
			includedir = $3
		if ($2 ~ /_mandir/)
			mandir = $3
		if ($2 ~ /_infodir/)
			infodir = $3
	}
}


# main()  ;-)
{
	preamble = 1
	
	sub(/[ \t]+$/, "")
	print
}


END {
	if (do_not_touch_anything)
		exit 0
	
	close(changelog_file)
	while ((getline < changelog_file) > 0)
		print
	system("rm -f " changelog_file)

	if (did_clean == 0) {
		print ""
		print "%clean"
		print "rm -rf $RPM_BUILD_ROOT"
	}

	if (date == 0) {
		print ""
		print "%define date\t%(echo `LC_ALL=\"C\" date +\"%a %b %d %Y\"`)"
	}
	
	if (has_changelog == 0)
		print "%changelog"

	if (boc > 0) {
		print "* %{date} PLD Team <feedback@pld.org.pl>"
		printf "All persons listed below can be reached at "
		print "<cvs_login>@pld.org.pl\n"
		print "$" "Log:$"
	}
}

function fixedsub(s1,s2,t,      ind) {
# substitutes fixed strings (not regexps)
        if (ind = index(t,s1))
                t = substr(t, 1, ind-1) s2 substr(t, ind+length(s1))
        return t
}

# There should be one or two tabs after the colon.
function format_preamble()
{
	sub(/:[ \t]*/, ":")
	if (match($0, /[A-Za-z0-9()#_ \t]+[ \t]*:[ \t]*/) == 1) {
		if (RLENGTH < 8)
			sub(/:/, ":\t\t")
		else
			sub(/:/, ":\t")
	}
}

# Replace directly specified directories with macros
function use_macros()
{
	gsub(bindir, "%{_bindir}")
	gsub("%{prefix}/bin", "%{_bindir}")
	if(prefix"/bin" == bindir)
		gsub("%{_prefix}/bin", "%{_bindir}")

	for (c = 1; c <= NF; c++) {
		if ($c ~ sbindir "/fix-info-dir")
			continue;
		gsub(sbindir, "%{_sbindir}", $c)
	}

	gsub("%{prefix}/sbin", "%{_sbindir}")
	if(prefix"/sbin" == sbindir)
		gsub("%{_prefix}/sbin", "%{_sbindir}")

	gsub(libdir, "%{_libdir}")
	gsub("%{prefix}/lib", "%{_libdir}")
	if(prefix"/lib" == libdir)
		gsub("%{_prefix}/lib", "%{_libdir}")

	for (c = 1; c <= NF; c++) {
		if ($c ~ sysconfdir "/{?cron.d")
			continue;
		if ($c ~ sysconfdir "/{?crontab.d")
			continue;
		if ($c ~ sysconfdir "/{?logrotate.d")
			continue;
		if ($c ~ sysconfdir "/{?pam.d")
			continue;
		if ($c ~ sysconfdir "/{?profile.d")
			continue;
		if ($c ~ sysconfdir "/{?rc.d")
			continue;
		if ($c ~ sysconfdir "/{?security")
			continue;
		if ($c ~ sysconfdir "/{?skel")
			continue;
		if ($c ~ sysconfdir "/{?sysconfig")
			continue;
		gsub(sysconfdir, "%{_sysconfdir}", $c)
	}

	gsub(datadir, "%{_datadir}")
	gsub("%{prefix}/share", "%{_datadir}")
	if(prefix"/share" == datadir)
		gsub("%{_prefix}/share", "%{_datadir}")

	gsub(includedir, "%{_includedir}")
	gsub("%{prefix}/include", "%{_includedir}")
	if(prefix"/include" == includedir)
		gsub("%{_prefix}/include", "%{_includedir}")

	gsub(mandir, "%{_mandir}")
	if ($0 !~ "%{_datadir}/manual")
		gsub("%{_datadir}/man", "%{_mandir}")
	gsub("%{_prefix}/share/man", "%{_mandir}")
	gsub("%{prefix}/share/man", "%{_mandir}")
	gsub("%{prefix}/man", "%{_mandir}")
	gsub("%{_prefix}/man", "%{_mandir}")

	gsub(infodir, "%{_infodir}")
	gsub("%{prefix}/info", "%{_infodir}")
	gsub("%{_prefix}/info", "%{_infodir}")

	gsub("%{_datadir}/aclocal", "%{_aclocaldir}")

	if (prefix != "/") {
		for (c = 1; c <= NF; c++) {
			if ($c ~ prefix "/sbin/fix-info-dir")
				continue;
			gsub(prefix, "%{_prefix}", $c)
		}
		gsub("%{prefix}", "%{_prefix}")
	}

	gsub("%{PACKAGE_VERSION}", "%{version}")
	gsub("%{PACKAGE_NAME}", "%{name}")

	gsub("%{_datadir}/gnome/apps", "%{_applnkdir}")
	gsub("%{_datadir}/applnk", "%{_applnkdir}")

	gsub("^make$", "%{__make}")
	gsub("^make ", "%{__make} ")

	gsub("/usr/src/linux", "%{_kernelsrcdir}")
	gsub("%{_prefix}/src/linux", "%{_kernelsrcdir}")
}
	
function use_files_macros()
{
	gsub("^%{_sbindir}", "%attr(755,root,root) %{_sbindir}")
	gsub("^%{_bindir}", "%attr(755,root,root) %{_bindir}")
}

function fill(ch, n, i) {
	for (i = 0; i < n; i++)
		printf("%c", ch)
}

function format_flush(line, indent, newline, word, first_word) {
	first_word = 1
	if (format_indent == -1) 
		newline = ""
	else
		newline = fill(" ", format_indent) "- "

	while (match(line, /[^\t ]+/)) {
		word = substr(line, RSTART, RLENGTH)
		if (length(newline) + length(word) + 1 > tw) {
			print newline
			
			if (format_indent == -1)
				newline = ""
			else
				newline = fill(" ", format_indent + 2)
			first_word = 1
		}

		if (first_word) {
			newline = newline word
			first_word = 0
		} else
			newline = newline " " word
			
		line = substr(line, RSTART + RLENGTH)
	}
	if (newline ~ /[^\t ]/) {
		print newline
	}
}

function cflags(var)
{
	if ($0 == var "=\"$RPM_OPT_FLAGS\"") {
		removed[var] = 1
		return 0
	}
		
	if (!/!\?debug/)
		sub("\$RPM_OPT_FLAGS", "%{rpmcflags}")
	return 1
}

