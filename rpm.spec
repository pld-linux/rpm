Summary:     Red Hat Package Manager
Summary(pl): Aplikacja do zarz±dzania pakietami
Name:        rpm
Version:     2.5.5
Release:     1
Group:       Utilities/System
Source:      ftp://ftp.rpm.org/pub/rpm/dist/rpm-2.5.x/%{name}-%{version}.tar.gz
Patch0:      rpm.patch
Copyright:   GPL
BuildRoot:   /tmp/%{name}-%{version}-root
Conflicts:   patch < 2.5
Obsoletes:	rpm-libs
%define		pyrequires_eq() Requires:	%1 >= %py_ver %1 < %(echo `python -c "import sys; import string; ver=sys.version[:3].split('.'); ver[1]=str(int(ver[1])+1); print string.join(ver, '.')"`)
RPM is a powerful package manager, which can be used to build, install, 
query, verify, update, and uninstall individual software packages. A 
package consists of an archive of files, and package information, including 
name, version, and description.
packages. A package consists of an archive of files, and package
nombre, versión y descripción.

RPM jest programem s³u¿±cym do zarz±dzania oprogramowaniem (menad¿erem
pakietów). Dziêki niemu bêdziesz móg³ przebudowaæ, zainstalowaæ czy
zweryfikowaæ dowolny pakiet. Informacje dotycz±ce ka¿dego pakietu s±
przechowywane w bazie danych i dostêpne tylko dla administratora systemu.
przechowywane w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
%package devel
Summary:     Header files and libraries for programs that manipulate rpm packages
Summary(pl): Pliki nag³ówkowe i biblioteki statyczne
Group:       Development/Libraries
Requires:    %{name} = %{version}
Requires:	%{name} = %{version}
Requires:	popt-devel

%description devel
The RPM packaging system includes a C library that makes it easy to
manipulate RPM packages and databases. It is intended to ease the
creation of graphical package managers and other tools that need
%description -l pl devel
RPM to tak¿e 
Pliki nag³ówkowe i biblioteki statyczne.
graficznych mened¿erów pakietów oraz innych narzêdzi, które wymagaj±
construir pacotes usando o RPM.
%setup -q
%patch0 -p1
install %{SOURCE13} macros.python.in
mv -f perl.prov perl.prov.in)
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr
make
	--with-python


install -d $RPM_BUILD_ROOT/{var/lib/rpm,usr/src/rpm/{SOURCES,SPECS,RPMS/{$RPM_ARCH,noarch},SRPMS,BUILD}}
make installprefix="$RPM_BUILD_ROOT" install
	pkgbindir="%{_bindir}"
%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/rpm --initdb

%files
%defattr(644, root, root, 755)
%doc RPM-PGP-KEY CHANGES groups docs/*
%attr(755, root, root) /bin/rpm
%attr(755, root, root) /usr/bin/*
%dir /usr/lib/rpm
%attr(755, root, root) /usr/lib/rpm/find-*
%attr(755, root, root) /usr/lib/rpm/freshen.sh
%attr(755, root, root) /usr/lib/rpm/mkinstalldirs
/usr/lib/rpm/rpmrc
/usr/lib/rpm/rpmpopt
%attr(644, root,  man) /usr/man/man8/*
%attr(700, root, root) %dir /var/lib/rpm
/usr/src/rpm
%lang(cs) /usr/share/locale/cs/LC_MESSAGES/rpm.mo
%lang(de) /usr/share/locale/de/LC_MESSAGES/rpm.mo
%lang(fi) /usr/share/locale/fi/LC_MESSAGES/rpm.mo
%lang(fr) /usr/share/locale/fr/LC_MESSAGES/rpm.mo
%lang(pt) /usr/share/locale/pt*/LC_MESSAGES/rpm.mo
%lang(ru) /usr/share/locale/ru/LC_MESSAGES/rpm.mo
%lang(sk) /usr/share/locale/sk/LC_MESSAGES/rpm.mo
%lang(sr) /usr/share/locale/sr/LC_MESSAGES/rpm.mo
%lang(sv) /usr/share/locale/sv/LC_MESSAGES/rpm.mo
%lang(tr) /usr/share/locale/tr/LC_MESSAGES/rpm.mo
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%attr(755,root,root) %{_libdir}/rpm/rpmi
%defattr(644, root, root, 755)
/usr/include/rpm
/usr/lib/lib*.a
%files utils
%files -n python-rpm
* Tue Sep 01 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.5.2-3]
- added pl translation.

* Sun Aug 30 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [2.5.2-2]
- fixed tr.po,
- added -q %setup parameter,
- changed Buildroot to /tmp/%%{name}-%%{version}-root,
- added using %%{name} and %%{version} in Source,
- added %lang macros for /usr/share/locale/*/LC_MESSAGES/rpm.mo files,
- added %attr and %defattr macros in %files (allow build package from
  non-root account).
Revision 1.79  2000/02/17 03:42:17  kloczek
- release 25,
- added "Conflicts: /usr/bin/id" and rebuilded in enviroment with id in
  /bin.
