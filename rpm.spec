Summary:     Red Hat Package Manager
Name:        rpm
Version:     2.5.2
Release:     2
Group:       Utilities/System
Source:      ftp://ftp.rpm.org/pub/rpm/dist/rpm-2.5.x/%{name}-%{version}.tar.gz
Patch0:      rpm.patch
Copyright:   GPL
BuildRoot:   /var/tmp/%{name}-%{version}-root
Conflicts:   patch < 2.5
Obsoletes:	rpm-libs
%define		pyrequires_eq() Requires:	%1 >= %py_ver %1 < %(echo `python -c "import sys; import string; ver=sys.version[:3].split('.'); ver[1]=str(int(ver[1])+1); print string.join(ver, '.')"`)
RPM is a powerful package manager, which can be used to build, install, 
query, verify, update, and uninstall individual software packages. A 
package consists of an archive of files, and package information, including 
name, version, and description.
packages. A package consists of an archive of files, and package
%package devel
Summary:     Header files and libraries for programs that manipulate rpm packages
Group:       Development/Libraries
Requires:	%{name} = %{version}
Requires:	popt-devel

%description devel
The RPM packaging system includes a C library that makes it easy to
manipulate RPM packages and databases. It is intended to ease the
creation of graphical package managers and other tools that need
construir pacotes usando o RPM.
%setup -q
%patch0 -p1
install %{SOURCE13} macros.python.in
mv -f perl.prov perl.prov.in)
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr
make
	--with-python


install -d $RPM_BUILD_ROOT/usr/{lib,src/redhat{SOURCES,SPECS,RPMS/{$RPM_ARCH,noarch},SRPMS,BUILD}}
make installprefix="$RPM_BUILD_ROOT" install
	pkgbindir="%{_bindir}"
%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/rpm --initdb

%files
%deffattr(644, root, root, 755)
%doc RPM-PGP-KEY CHANGES groups docs/*
%attr(755, root, root) /bin/rpm
%attr(755, root, root) /usr/bin/*
%attr(644, root,  man) /usr/man/man8/*
/usr/lib/rpm
%dir /usr/src/redhat
%lang(cz) /usr/share/locale/cz/LC_MESSAGES/rpm.mo
%lang(de) /usr/share/locale/cz/LC_MESSAGES/rpm.mo
%lang(fi) /usr/share/locale/cz/LC_MESSAGES/rpm.mo
%lang(fr) /usr/share/locale/cz/LC_MESSAGES/rpm.mo
%lang(pt) /usr/share/locale/pt-br/LC_MESSAGES/rpm.mo
%lang(sv) /usr/share/locale/sv/LC_MESSAGES/rpm.mo
%lang(tr) /usr/share/locale/tr/LC_MESSAGES/rpm.mo
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%attr(755,root,root) %{_libdir}/rpm/rpmi
%deffattr(644, root, root, 755)
/usr/include/rpm
/usr/lib/librpm.a
/usr/lib/librpmbuild.a
%files utils
%files -n python-rpm
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
