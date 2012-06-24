%define	date	19990519

Summary:	Red Hat & PLD Package Manager
Summary(pl):	Aplikacja do zarz�dzania pakietami
Name:		rpm
Version:	3.0.1
Release:	7.%{date}
Group:		Base
Group(pl):	Podstawowe
Copyright:	GPL
Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-3.0.x/%{name}-%{version}.%{date}.tar.gz
Source1:	rpm.groups
Source2:	rpm.8pl
Source3:	rpm.macros
Source4:	rpm.pl.po
Source5:	rpm-backup
Source6:	rpm-backup.sh
Patch0:		rpm-rpmrc.patch
Patch1:		rpm-i18n.patch
Patch2:		rpm-find-requires.patch
Patch3:		rpm-macros.patch
Patch4:		rpm-po.patch
Patch5:		rpm-moredoc.patch
Patch6:		rpm-arch.patch
Patch7:		rpm-pld.patch
Patch37:        %{name}-short_circuit.patch
Patch38:        %{name}-section_test.patch
BuildPrereq:	bzip2-static
BuildPrereq:	gdbm-static
BuildPrereq:	zlib-static
BuildPrereq:	patch >= 2.2
BuildPrereq:	libtool
BuildPrereq:	automake
BuildPrereq:	autoconf >= 2.13-8
BuildPrereq:	gettext
Requires:	glibc >= 2.1
Requires:	/etc/cron.daily
BuildRoot:	/tmp/%{name}-%{version}-root
Obsoletes:	rpm-libs
%define		pyrequires_eq() Requires:	%1 >= %py_ver %1 < %(echo `python -c "import sys; import string; ver=sys.version[:3].split('.'); ver[1]=str(int(ver[1])+1); print string.join(ver, '.')"`)
RPM is a powerful package manager, which can be used to build, install, 
query, verify, update, and uninstall individual software packages. A 
package consists of an archive of files, and package information, including 
name, version, and description.
packages. A package consists of an archive of files, and package
nombre, versi�n y descripci�n.
RPM jest doskona�ym menad�erem pakiet�w. Dzi�ki niemu b�dziesz m�g� przebudowa�,
zainstalowa� czy zweryfikowa� dowolny pakiet. Informacje dotycz�ce ka�dego 
pakietu s� przechowywane w bazie danych i dost�pne tylko dla administratora 
systemu.
przechowywane w bazie danych i mo�na je uzyska� za pomoc� opcji
do pacote, permiss�es dos arquivos, etc.
Summary:	Header files and libraries 
Summary(pl):	Pliki nag��wkowe i biblioteki statyczne	
Summary(pl):	Pliki nag��wkowe i biblioteki statyczne
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Requires:	%{name} = %{version}
Requires:	popt-devel

%description devel
The RPM packaging system includes a C library that makes it easy to
manipulate RPM packages and databases. It is intended to ease the
creation of graphical package managers and other tools that need
%description -l pl devel
Pliki nag��wkowe i biblioteki statyczne.
graficznych mened�er�w pakiet�w oraz innych narz�dzi, kt�re wymagaj�
construir pacotes usando o RPM.
%setup  -q
%patch0 -p1 
%patch1 -p1
%patch2 -p1
%patch1 -p1
%patch4 -p1 
%patch5 -p1
%patch6 -p1 
%patch7 -p1 
%patch31 -p1
install %{SOURCE4} po/pl.po
install %{SOURCE3} macros.pld.in
install %{SOURCE13} macros.python.in
mv -f perl.prov perl.prov.in)
LDFLAGS="-s"; export LDFLAGS

( cd popt; 
%GNUconfigure
)
%GNUconfigure
%configure \
make
	--with-python


%{__make} %{?_without_static:rpm_LDFLAGS="\\$(myLDFLAGS)"}
install -d $RPM_BUILD_ROOT/var/db/{rpm,backups/rpm} \
	$RPM_BUILD_ROOT/etc/{cron.daily,sysconfig} \
	$RPM_BUILD_ROOT%{_mandir}/{ru,pl}/man8 \
	$RPM_BUILD_ROOT/etc/skel/C/rpm/{SRPMS,RPMS,SOURCES,SPECS,BUILD}

make DESTDIR="$RPM_BUILD_ROOT" pkgbindir="%{_bindir}" install

install macros.pld $RPM_BUILD_ROOT%{_prefix}/lib/rpm/macros.pld
	pkgbindir="%{_bindir}"
install rpm.8ru $RPM_BUILD_ROOT%{_mandir}/ru/man8/rpm.8
install rpm2cpio.8ru $RPM_BUILD_ROOT%{_mandir}/ru/man8/rpm2cpio.8
install %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/pl/man8/rpm.8

install %{SOURCE1} docs/groups
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig
install %{SOURCE6} $RPM_BUILD_ROOT/etc/cron.daily
install %{SOURCE8} $RPM_BUILD_ROOT%{_libdir}/rpm/find-spec-bcond
strip  $RPM_BUILD_ROOT/{bin/rpm,%{_bindir}/*} || :

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/{{ru,pl}/man8/*,man8/*} \
	RPM-PGP-KEY CHANGES docs/*

%pre
if [ -e /var/lib/rpm ] && [ ! -L /var/lib/rpm ]; then
	mkdir -p /var/db/rpm /var/db/rpm.old
	cp -ap /var/lib/rpm/* /var/db/rpm
	cp -ap /var/lib/rpm/* /var/db/rpm.old
	echo "Yours old rpm database backuped in /var/db/rpm.old" >&2
	echo "Run 'rpm --rebuilddb' to update rpm database" >&2
fi

%post
/bin/rpm --initdb
if [ -e /var/lib/rpm ] && [ ! -L /var/lib/rpm ]; then
	rm -rf /var/lib/rpm/
	ln -s ../db/rpm /var/lib/rpm
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files

%doc RPM-PGP-KEY.gz CHANGES.gz docs/*
%postun -p /sbin/ldconfig

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/rpm/rpmdb
%{_mandir}/man8/*
%lang(ru) %{_mandir}/ru/man8/*
%lang(pl) %{_mandir}/pl/man8/*

%lang(cs)    %{_datadir}/locale/cs/LC_MESSAGES/rpm.mo
%lang(de)    %{_datadir}/locale/de/LC_MESSAGES/rpm.mo
%lang(fi)    %{_datadir}/locale/fi/LC_MESSAGES/rpm.mo
%lang(fr)    %{_datadir}/locale/fr/LC_MESSAGES/rpm.mo
%lang(pl)    %{_datadir}/locale/pl/LC_MESSAGES/rpm.mo
%lang(pt_BR) %{_datadir}/locale/pt_BR/LC_MESSAGES/rpm.mo
%lang(ru)    %{_datadir}/locale/ru/LC_MESSAGES/rpm.mo
%lang(sk)    %{_datadir}/locale/sk/LC_MESSAGES/rpm.mo
%lang(sr)    %{_datadir}/locale/sr/LC_MESSAGES/rpm.mo
%lang(sv)    %{_datadir}/locale/sv/LC_MESSAGES/rpm.mo
%lang(tr)    %{_datadir}/locale/tr/LC_MESSAGES/rpm.mo
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%attr(755,root,root) %dir /var/db/rpm
%attr(755,root,root) %dir /var/db/backups/rpm
%attr(750,root,root) /etc/cron.daily/rpm-backup.sh
%attr(640,root,root) /etc/sysconfig/rpm-backup

%dir /usr/lib/rpm
%attr(755,root,root) %{_prefix}/lib/rpm/find-*
%attr(755,root,root) %{_prefix}/lib/rpm/freshen.sh
%attr(755,root,root) %{_prefix}/lib/rpm/mkinstalldirs
%attr(755,root,root) %{_prefix}/lib/rpm/config.*
%attr(755,root,root) %{_prefix}/lib/rpm/getpo.sh

%{_prefix}/lib/rpm/rpm*
%{_prefix}/lib/rpm/macros*

/etc/skel/C/rpm
%attr(755,root,root) %{_libdir}/rpm/rpmb
%attr(755,root,root) %{_libdir}/rpm/rpmi
%attr(755,root,root) %{_libdir}/rpm/rpmt
%attr(755,root,root) %{_libdir}/rpm/rpme
%{_libdir}/librpm*.a
%{_libdir}/librpm*.la
%files utils
%files -n python-rpm
* Thu May 20 1999 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
  [3.0.1-6.19990519]
- spec based on version from dist tar ball (partially rewrited by me),
- pl translation by Wojtek �lusarczyk <wojtek@shadow.eu.org>,
- rewrited by Artur Frysiak <wiget@pld.org.pl>,
- patches with fixes maked by Artur Frysiak and Marcin Dalecki
  <dalecki@cs.net.pl>.

Revision 1.79  2000/02/17 03:42:17  kloczek
- release 25,
- added "Conflicts: /usr/bin/id" and rebuilded in enviroment with id in
  /bin.
