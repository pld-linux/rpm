Summary:	Red Hat & PLD Package Manager
Summary(pl):	Aplikacja do zarz±dzania pakietami
Name:		rpm
Version:	3.0.1
Release:	15
Group:		Base
Group(pl):	Podstawowe
Copyright:	GPL
Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-3.0.x/%{name}-%{version}.tar.gz
Source1:	rpm.groups
Source2:	rpm.8pl
Source3:	rpm.macros
Source4:	rpm.pl.po
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
do pacote, permissões dos arquivos, etc.
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
install -d $RPM_BUILD_ROOT/var/db/rpm \
	$RPM_BUILD_ROOT%{_mandir}/{ru,pl}/man8

make DESTDIR="$RPM_BUILD_ROOT" pkgbindir="%{_bindir}" install

install macros.pld $RPM_BUILD_ROOT%{_prefix}/lib/rpm/macros.pld
	pkgbindir="%{_bindir}"
install rpm.8ru $RPM_BUILD_ROOT%{_mandir}/ru/man8/rpm.8
install rpm2cpio.8ru $RPM_BUILD_ROOT%{_mandir}/ru/man8/rpm2cpio.8
install %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/pl/man8/rpm.8

install %{SOURCE1} docs/groups
install %{SOURCE8} $RPM_BUILD_ROOT%{_libdir}/rpm/find-spec-bcond
strip  $RPM_BUILD_ROOT/{bin/rpm,%{_bindir}/*} || :

#%%_install_langs pl_PL:en_US
%%distribution PLD
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

rm -rf $RPM_BUILD_ROOT

%doc RPM-PGP-KEY.gz CHANGES.gz docs/*
%postun -p /sbin/ldconfig

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/rpm/rpmdb
%{_mandir}/man8/*
%lang(ru) %{_mandir}/ru/man8/*
%lang(pl) %{_mandir}/pl/man8/*
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%attr(755,root,root) %dir /var/db/rpm

%dir /usr/lib/rpm
%attr(755,root,root) %{_libdir}/rpm/find-*
%attr(755,root,root) %{_libdir}/rpm/freshen.sh
%attr(755,root,root) %{_libdir}/rpm/find-requires
%attr(755,root,root) %{_libdir}/rpm/find-provides
%attr(755,root,root) %{_libdir}/rpm/find-rpm-provides

%{_libdir}/rpm/rpm*
%{_libdir}/rpm/macros*
%attr(755,root,root) %{_libdir}/rpm/rpmb
%attr(755,root,root) %{_libdir}/rpm/rpmi
%attr(755,root,root) %{_libdir}/rpm/rpmt
%attr(755,root,root) %{_libdir}/rpm/rpme
%{_libdir}/librpm*.a
%{_libdir}/librpm*.la
%files utils
%files -n python-rpm
* Thu May 20 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [3.0.1-6.19990519]
- spec based on version from dist tar ball (partially rewrited by me),
- pl translation by Wojtek ¦lusarczyk <wojtek@shadow.eu.org>,
- rewrited by Artur Frysiak <wiget@pld.org.pl>,
- patches with fixes maked by Artur Frysiak and Marcin Dalecki
  <dalecki@cs.net.pl>.

Revision 1.79  2000/02/17 03:42:17  kloczek
- release 25,
- added "Conflicts: /usr/bin/id" and rebuilded in enviroment with id in
  /bin.
