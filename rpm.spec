Summary:	Red Hat & PLD Package Manager
Summary(pl):	Aplikacja do zarz±dzania pakietami
Name:		rpm
Version:	2.92
Release:	11
Group:		Base
Group(pl):	Bazowe
Copyright:	GPL
Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-2.5.x/%{name}-%{version}.tar.gz
Source1:	rpm.groups
Source2:	rpm.8pl
Patch0:		rpm-rpmrc.patch
Patch1:		rpm-i18n.patch
Patch2:		rpm-find-requires.patch
Patch37:        %{name}-short_circuit.patch
Icon:		rpm.gif
Requires:	glibc >= 2.1
BuildRoot:	/tmp/%{name}-%{version}-root
Obsoletes:	rpm-libs
%define		pyrequires_eq() Requires:	%1 >= %py_ver %1 < %(echo `python -c "import sys; import string; ver=sys.version[:3].split('.'); ver[1]=str(int(ver[1])+1); print string.join(ver, '.')"`)
RPM is a powerful package manager, which can be used to build, install, 
query, verify, update, and uninstall individual software packages. A 
package consists of an archive of files, and package information, including 
name, version, and description.
packages. A package consists of an archive of files, and package
nombre, versión y descripción.
RPM jest doskona³ym menad¿erem pakietów. Dziêki niemu bêdziesz móg³ przebudowaæ,
zainstalowaæ czy zweryfikowaæ dowolny pakiet. Informacje dotycz±ce ka¿dego 
pakietu s± przechowywane w bazie danych i dostêpne tylko dla administratora 
systemu.
przechowywane w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
%package	devel
Summary:	Header files and libraries 
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne	
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Requires:	%{name} = %{version}
Requires:	popt-devel

%description devel
The RPM packaging system includes a C library that makes it easy to
manipulate RPM packages and databases. It is intended to ease the
creation of graphical package managers and other tools that need
%description -l pl devel
Pliki nag³ówkowe i biblioteki statyczne.
graficznych mened¿erów pakietów oraz innych narzêdzi, które wymagaj±
construir pacotes usando o RPM.
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
install %{SOURCE13} macros.python.in
mv -f perl.prov perl.prov.in)
autoconf
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure \
	--prefix=/usr \
	--disable-shared
make
	--with-python


%{__make} %{?_without_static:rpm_LDFLAGS="\\$(myLDFLAGS)"}
install -d $RPM_BUILD_ROOT/var/lib/rpm \
	$RPM_BUILD_ROOT/usr/src/rpm/{SOURCES,SPECS,SRPMS,BUILD} \
	$RPM_BUILD_ROOT/usr/src/rpm/RPMS/{$RPM_ARCH,noarch} \
	$RPM_BUILD_ROOT/usr/man/{ru,pl}/man8

make DESTDIR="$RPM_BUILD_ROOT" install
	pkgbindir="%{_bindir}"
install rpm.8ru $RPM_BUILD_ROOT/usr/man/ru/man8/rpm.8
install rpm2cpio.8ru $RPM_BUILD_ROOT/usr/man/ru/man8/rpm2cpio.8
install %{SOURCE2} $RPM_BUILD_ROOT/usr/man/pl/man8/rpm.8

install %{SOURCE1} docs/groups

gzip -9fn $RPM_BUILD_ROOT/usr/man/{ru/man8/*,man8/*} \
	RPM-PGP-KEY CHANGES docs/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/rpm --initdb
/bin/rpm --rebuilddb

%files

%doc {RPM-PGP-KEY,CHANGES}.gz docs/*
%postun -p /sbin/ldconfig

%attr(755,root,root) /usr/bin/gendiff
%attr(755,root,root) /usr/bin/rpm2cpio
%attr(755,root,root) %{_libdir}/rpm/rpmdb
/usr/man/man8/*
%lang(ru) /usr/man/ru/man8/*
%lang(pl) /usr/man/pl/man8/*

%attr(750,root,root) %dir /var/lib/rpm

%dir /usr/lib/rpm
%attr(755,root,root) /usr/lib/rpm/find-*
%attr(755,root,root) /usr/lib/rpm/freshen.sh
%attr(755,root,root) /usr/lib/rpm/mkinstalldirs

/usr/lib/rpm/rpm*
/usr/src/rpm

%lang(cs)    /usr/share/locale/cs/LC_MESSAGES/rpm.mo
%lang(de)    /usr/share/locale/de/LC_MESSAGES/rpm.mo
%lang(fi)    /usr/share/locale/fi/LC_MESSAGES/rpm.mo
%lang(fr)    /usr/share/locale/fr/LC_MESSAGES/rpm.mo
%lang(pt_BR) /usr/share/locale/pt_BR/LC_MESSAGES/rpm.mo
%lang(ru)    /usr/share/locale/ru/LC_MESSAGES/rpm.mo
#%lang(sk)    /usr/share/locale/sk/LC_MESSAGES/rpm.mo
%lang(sv)    /usr/share/locale/sv/LC_MESSAGES/rpm.mo
%lang(sr)    /usr/share/locale/sr/LC_MESSAGES/rpm.mo
%lang(tr)    /usr/share/locale/tr/LC_MESSAGES/rpm.mo
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%attr(755,root,root) %{_libdir}/rpm/rpmi
%attr(755,root,root) %{_libdir}/rpm/rpmt
/usr/include/rpm
/usr/lib/librpm*.a
%files utils
%files -n python-rpm
* Wed Mar 10 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [2.5.6-5]
- added rpm-find-requires.patch with beter finding list packages containing
  required shared libraries (Artur Frysiak <wiget@usa.net>),
- added ru man pages,
- added "Requires: glibc >= 2.1" (rpm is linked statically but it use by
  dlopen() some shared glibc libraries),
- removed man group from man pages.

* Fri Feb 19 1999 Marcin Dalecki <dalecki@cs.net.pl>
  [2.5.6-4d]
- fixed ignorance about international character sets.

* Fri Jan 15 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.5.6-1d]
- updated to latest stable version,
- added URL,
- added Group(pl) && changed gropup to Base,
- added small patch against GNU libc-2.1.

* Sun Nov 08 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.5.5-1d]
- updated to 2.5.5. 

* Tue Sep 01 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.5.2-2d]
- translation modified for pl,
- compressed man pages && documentation,
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- moved /usr/src/redhat to /usr/src/rpm.

* Sun Aug 30 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [2.5.2-2]
- fixed tr.po,
- added -q %setup parameter,
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- added using %%{name} and %%{version} in Source,
- added %lang macros for /usr/share/locale/*/LC_MESSAGES/rpm.mo files,
- added %attr and %defattr macros in %files (allow build package from
  non-root account),
- build against GNU libc-2.1.

Revision 1.79  2000/02/17 03:42:17  kloczek
- release 25,
- added "Conflicts: /usr/bin/id" and rebuilded in enviroment with id in
  /bin.
