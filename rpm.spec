Summary:	Red Hat & PLD Package Manager
Summary(pl):	Aplikacja do zarz±dzania pakietami
Name:		rpm
Version:	2.5.6
Release:	2d
Group:		Base
Group(pl):	Bazowe
URL:		ftp://ftp.rpm.org/pub/rpm/dist/rpm-2.5.x
Source:		%{name}-%{version}.tar.gz
Patch0:		%{name}-config.patch
Patch1:		%{name}-rpmrc.patch
Patch2:		%{name}-glibc.patch
Patch3:		%{name}-groups.patch
Copyright:	GPL
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
%package devel
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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch1 -p1
install %{SOURCE13} macros.python.in
mv -f perl.prov perl.prov.in)
autoconf
CFLAGS=$RPM_OPT_FLAGS LDFLAGS=-s \
    ./configure \
	--prefix=/usr
make
	--with-python


%{__make} %{?_without_static:rpm_LDFLAGS="\\$(myLDFLAGS)"}
install -d $RPM_BUILD_ROOT/var/lib/rpm
install -d $RPM_BUILD_ROOT/usr/src/rpm/{SOURCES,SPECS,SRPMS,BUILD}
install -d $RPM_BUILD_ROOT/usr/src/rpm/RPMS/{$RPM_ARCH,noarch}

make installprefix="$RPM_BUILD_ROOT" install
	pkgbindir="%{_bindir}"
gzip -9fn  $RPM_BUILD_ROOT/usr/man/man8/*
bzip2 -9 RPM-PGP-KEY CHANGES groups docs/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/rpm --initdb

%files

%doc RPM-PGP-KEY.bz2 CHANGES.bz2 groups.bz2 docs/*
%postun -p /sbin/ldconfig

%attr(755,root,root) /usr/bin/gendiff
%attr(755,root,root) /usr/bin/rpm2cpio
%attr(644,root, man) /usr/man/man8/*

%attr(750,root,root) %dir /var/lib/rpm

%dir /usr/lib/rpm
%attr(755,root,root) /usr/lib/rpm/find-*
%attr(755,root,root) /usr/lib/rpm/freshen.sh
%attr(755,root,root) /usr/lib/rpm/mkinstalldirs

/usr/lib/rpm/rpm*

%dir /usr/src/rpm/RPMS
%attr(755,root,root,755) /usr/src/rpm/RPMS/*

%dir /usr/src/rpm/SRPMS
%dir /usr/src/rpm/SPECS
%dir /usr/src/rpm/BUILD
%dir /usr/src/rpm/SOURCES

%lang(cs) /usr/share/locale/cs/LC_MESSAGES/rpm.mo
%lang(de) /usr/share/locale/de/LC_MESSAGES/rpm.mo
%lang(fi) /usr/share/locale/fi/LC_MESSAGES/rpm.mo
%lang(fr) /usr/share/locale/fr/LC_MESSAGES/rpm.mo
%lang(pt) /usr/share/locale/pt*/LC_MESSAGES/rpm.mo
%lang(ru) /usr/share/locale/ru/LC_MESSAGES/rpm.mo
%lang(sk) /usr/share/locale/sk/LC_MESSAGES/rpm.mo
%lang(sv) /usr/share/locale/sv/LC_MESSAGES/rpm.mo
%lang(sr) /usr/share/locale/sr/LC_MESSAGES/rpm.mo
%lang(tr) /usr/share/locale/tr/LC_MESSAGES/rpm.mo
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%attr(755,root,root) %{_libdir}/rpm/rpmi
%attr(755,root,root) %{_libdir}/rpm/rpmt

%dir /usr/include/rpm
/usr/include/rpm/*

/usr/lib/lib*.a
%files utils
%files -n python-rpm
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
