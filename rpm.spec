Summary:	Red Hat (and now also PLD) Package Manager
Summary(de):	Red Hat (und jetzt auch PLD) Packet-Manager
Summary(pl):	Aplikacja do zarz±dzania pakietami
Name:		rpm
Version:	4.0.2
Release:	20
License:	GPL
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.0.x/%{name}-%{version}.tar.gz
Source1:	%{name}.groups
Source2:	%{name}.macros
Source3:	%{name}-install-tree
Source4:	%{name}-find-rpm-provides
Source5:	%{name}-macros.perl
Source6:	%{name}-find-perl-provides
Source7:	%{name}-find-perl-requires
Source8:	%{name}-find-spec-bcond
Source9:	%{name}-find-lang
Source10:	%{name}-find-provides
Source11:	%{name}-find-requires
Patch0:		%{name}-rpmrc.patch
Patch1:		%{name}-macros.patch
Patch2:		%{name}-arch.patch
Patch3:		%{name}-rpmpopt.patch
Patch4:		%{name}-perl-macros.patch
Patch5:		%{name}-db3.patch
Patch6:		%{name}-segv.patch
Patch7:		%{name}-am_fix.patch
Patch8:		%{name}-perl-req-perlfile.patch
Patch9:		%{name}-installplatform.patch
Patch10:	%{name}-cache.patch
Patch11:	%{name}-suggestions.patch
Patch12:	%{name}-rh-lame.patch
Patch13:	%{name}-glob.patch
Patch14:	%{name}-header_h.patch	
Patch15:	%{name}-fast-alAddPackage.patch
Patch16:	%{name}-byKey.patch
Patch17:	%{name}-perlprov.patch
Patch37:        %{name}-short_circuit.patch
Patch38:        %{name}-section_test.patch
BuildRequires:	gettext-devel
BuildRequires:	automake
BuildRequires:	db3-devel >= 3.1.17-9
BuildRequires:	bzip2-devel >= 1.0.1
BuildRequires:	gdbm-devel
BuildRequires:	zlib-devel
BuildRequires:	gettext-devel >= 0.10.38-3
BuildRequires:	libtool
BuildRequires:	automake
BuildRequires:	autoconf >= 2.13-8
BuildRequires:	python-modules >= 2.2.1
BuildRequires:	zlib-devel >= 1.1.4
# Require static library only for static build
BuildRequires:	db3-static >= 3.1.17-9
BuildRequires:	bzip2-static >= 1.0.1
BuildRequires:	gdbm-static
BuildRequires:	zlib-static
%endif
BuildRequires:	zlib-static >= 1.1.4
Obsoletes:	rpm-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	rpm-libs
%define __find_provides %{SOURCE4}
%define _binary_payload w9.gzdio
%define		__find_provides	%{SOURCE4}
%define		pyrequires_eq() Requires:	%1 >= %py_ver %1 < %(echo `python -c "import sys; import string; ver=sys.version[:3].split('.'); ver[1]=str(int(ver[1])+1); print string.join(ver, '.')"`)

%description
RPM is a powerful package manager, which can be used to build,
install, query, verify, update, and uninstall individual software
packages. A package consists of an archive of files, and package
information, including name, version, and description.

%description -l de
RPM ist ein kräftiger Packet-Manager, der verwendet sein kann zur
Installation, Anfrage, Verifizierung, Aktualisierung und
Uninstallation individueller Softwarepakete. Ein Paket besteht aus
einem Archiv Dateien und Paketinformation, inklusive Name, Version und
nombre, versión y descripción.
RPM jest doskona³ym menad¿erem pakietów. Dziêki niemu bêdziesz móg³
%description -l pl
RPM jest doskona³ym mened¿erem pakietów. Dziêki niemu bêdziesz móg³
wchodz±cych w sk³ad pakietu, zale¿no¶ci od innych pakietów s±
przechowywane s± w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
wchodz±cych w sk³ad pakietu, zale¿no¶ci od innych pakietów, s±
przechowywane w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
do pacote, permissões dos arquivos, etc.

%package devel
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne	
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Summary(pt_BR):	Arquivos de inclusão e bibliotecas para programas de manipulação de pacotes RPM
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	popt-devel

%description devel
The RPM packaging system includes a C library that makes it easy to
manipulate RPM packages and databases. It is intended to ease the
creation of graphical package managers and other tools that need
%description -l de devel

%description devel -l de
Der RPM-Packensystem enthält eine C-Library, die macht es einfach
RPM-Pakete und Dateibanken zu manipulieren. Er eignet sich für
Vereinfachung des Schaffens grafischer Paket-Manager und anderer
%description -l pl devel
Pliki nag³ówkowe i biblioteki statyczne.
graficznych mened¿erów pakietów oraz innych narzêdzi, które wymagaj±
ferramentas que precisem de conhecimento profundo de pacotes RPM.

%package static
Summary(pl):	Biblioteki statyczne rpm-a
Summary(pl):	Biblioteki statyczne RPM-a
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Summary(pt_BR):	Bibliotecas estáticas para o desenvolvimento de aplicações RPM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
%description -l de static

%description static -l de
%description -l pl static
Biblioteki statyczne rpm-a.
%description static -l pl
Bibliotecas estáticas para desenvolvimento.

%package utils
Summary(pl):	Dodatkowe narzêdzia do zarz±dzania baz± rpm-a i pakietami
Summary(de):	Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken
Group(de):	Applikationen/Datei
Group(pl):	Aplikacje/Pliki
Summary(pl):	Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami
Group:		Applications/File
Requires:	%{name} = %{version}

%description utils
%description -l de utils

%description utils -l de
%description -l pl utils
Dodatkowe narzêdzia do zarz±dzania baz± rpm-a i pakietami.
%description utils -l pl
Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami.

%package perlprov
Summary(pl):	Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci dla skryptów perl w pakietach rpm
Summary(de):	Zusatzwerkzeuge fürs Nachsehen Perl-Abhängigkeiten in RPM-Paketen
Group(de):	Applikationen/Datei
Group(pl):	Aplikacje/Pliki
Summary(pl):	Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów perla w pakietach rpm
Requires:	perl-modules
Requires:	findutils

%description perlprov
Additional utilities for checking perl provides/requires in rpm
%description -l de perlprov

%description perlprov -l de
%description -l pl perlprov
Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci dla skryptów perl w
%description perlprov -l pl
Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów perla w
Python para manipular pacotes e bancos de dados RPM.

%package build
Summary(pl):	Skrypty pomocnicze do budowania binarnych RPMów
Summary(pl):	Skrypty pomocnicze do budowania binarnych RPM-ów
Group(de):	Applikationen/Datei
Group(pl):	Aplikacje/Pliki
Summary(pt_BR):	Scripts e programas executáveis usados para construir pacotes
Group:		Applications/File
Requires:	sh-utils
Requires:	binutils
Requires:	patch
Requires:	texinfo
Requires:	file >= 3.31
Requires:	binutils
Requires:	gcc >= 3.0.3
Requires:	gcc
Requires:	diffutils
Requires:	libtool
Requires:	glibc-devel
Requires:	sed
Requires:	sed
Requires:	tar
Requires:	textutils

%description build
%description -l de build

%description build -l de
%description -l pl build
Skrypty pomocnicze do budowania binarnych RPMów.
%description build -l pl
construir pacotes usando o RPM.
%setup  -q
%prep
%setup -q -a12
%patch0 -p1
%patch1 -p1
%patch4 -p1 
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch11 -p0
%patch12 -p0
%patch11 -p0
%patch12 -p0
%patch15 -p0
%patch16 -p0
%patch15 -p0
%patch31 -p1
install %{SOURCE2} macros.pld.in
%patch38 -p1
sed -e 's/^/@pld@/' %{SOURCE2} >>platform.in
cp -f platform.in macros.pld.in
install %{SOURCE9} scripts/find-lang.sh
install %{SOURCE13} macros.python.in
(cd scripts; 
install %{SOURCE7} scripts/find-perl-requires
install %{SOURCE9} scripts/find-lang.sh

(cd scripts;
mv -f perl.req perl.req.in
mv -f perl.prov perl.prov.in)

(cd popt;
 libtoolize --force --copy
 aclocal
 autoheader
 autoconf
 automake -a -c)
autoheader
%{__automake}
cd ..

autoheader
autoconf
# ugly workaround for automake
sed -e 's#cpio.c $(DBLIBOBJS) depends.c#cpio.c depends.c#g' \
	lib/Makefile.am > lib/Makefile.am.new
mv -f lib/Makefile.am.new lib/Makefile.am
automake -a -c
sed -e 's#cpio.c depends.c#cpio.c $(DBLIBOBJS) depends.c#g' \
	lib/Makefile.in > lib/Makefile.in.new
mv -f lib/Makefile.in.new lib/Makefile.in
%configure \
	sed 's|@host_cpu@|%{_target_cpu}|' > macros.tmp
	--enable-v1-packages
%configure \
	--enable-v1-packages \
	--with-python


%{__make} %{?_without_static:rpm_LDFLAGS="\\$(myLDFLAGS)"}

	DESTDIR="$RPM_BUILD_ROOT" \
rm -rf $RPM_BUILD_ROOT

install macros.pld $RPM_BUILD_ROOT%{_libdir}/rpm/macros.pld
%{__make} install \
	pkgbindir="%{_bindir}"

install macros.perl $RPM_BUILD_ROOT%{_libdir}/rpm/macros.perl
install macros.python $RPM_BUILD_ROOT%{_libdir}/rpm/macros.python

install %{SOURCE1} doc/manual/groups
install %{SOURCE3} $RPM_BUILD_ROOT%{_libdir}/rpm/install-build-tree
install %{SOURCE8} $RPM_BUILD_ROOT%{_libdir}/rpm/find-spec-bcond
install %{SOURCE10} $RPM_BUILD_ROOT%{_libdir}/rpm/find-provides
install %{SOURCE11} $RPM_BUILD_ROOT%{_libdir}/rpm/find-requires
install %{SOURCE15} $RPM_BUILD_ROOT%{_libdir}/rpm/compress-doc

install rpmio/ugid.h $RPM_BUILD_ROOT%{_includedir}/rpm

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros <<EOF
# customized rpm macros - global for host
#
#%%_install_langs pl_PL:en_US
%%distribution PLD
EOF

%find_lang %{name}

%post   -p /sbin/ldconfig

%clean
%clean
rm -rf $RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%attr(755,root,root) %{_libdir}/rpm/rpmdb
%attr(755,root,root) %{_libdir}/rpm/rpmq
%attr(755,root,root) %{_libdir}/rpm/rpmk
%attr(755,root,root) %{_libdir}/rpm/rpmv
%attr(755,root,root) %{_libdir}/librpm*.so.*.*
%attr(755,root,root) %{_libdir}/rpm/rpmdb
%attr(755,root,root) %{_libdir}/rpm/rpmq
%attr(755,root,root) %{_libdir}/rpm/rpmk
%attr(755,root,root) %{_libdir}/rpm/rpmv
%attr(755,root,root) %{_libdir}/librpm*.so.*.*
%{_mandir}/man8/rpm.8*
%lang(pl) %{_mandir}/pl/man8/rpm.8*
%lang(ja) %{_mandir}/ja/man8/rpm.8*
%lang(fr) %{_mandir}/fr/man8/rpm.8*
%lang(ja) %{_mandir}/ja/man8/rpm.8*
%lang(ko) %{_mandir}/ko/man8/rpm.8*
%lang(pl) %{_mandir}/pl/man8/rpm.8*
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%lang(sk) %{_mandir}/sk/man8/rpm.8*

%dir /var/lib/rpm
%dir %{_libdir}/rpm

%{_libdir}/rpm/macros.pld
%{_libdir}/rpm/noarch-linux
%{_libdir}/rpm/noarch-pld-linux
%ifarch i386 i486 i586 i686
%{_libdir}/rpm/i386-pld-linux
%endif
%ifarch i486 i586 i686
%{_libdir}/rpm/i486-pld-linux
%endif
%ifarch i586 i686
%{_libdir}/rpm/i586-pld-linux
%endif
%ifarch i686
%{_libdir}/rpm/i686-pld-linux
%{_libdir}/rpm/noarch-linux
%{_libdir}/rpm/noarch-pld-linux
%{_libdir}/rpm/sparc-pld-linux
%endif
%ifarch sparc64
%{_libdir}/rpm/sparc64-pld-linux
%{_libdir}/rpm/i?86*
%{_libdir}/rpm/athlon*
%{_libdir}/rpm/alpha-pld-linux
%ifarch sparc sparc64
%endif
%ifarch ppc
%{_libdir}/rpm/ppc*
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpmbuild
%attr(755,root,root) %{_bindir}/rpme
%attr(755,root,root) %{_bindir}/rpmi
%attr(755,root,root) %{_bindir}/rpmu
%attr(755,root,root) %{_libdir}/rpm/find-requires
%attr(755,root,root) %{_libdir}/rpm/find-provides
%attr(755,root,root) %{_libdir}/rpm/find-rpm-provides
%attr(755,root,root) %{_libdir}/rpm/find-spec-bcond
%attr(755,root,root) %{_libdir}/rpm/find-lang.sh
%attr(755,root,root) %{_libdir}/rpm/mkinstalldirs
%attr(755,root,root) %{_libdir}/rpm/getpo.sh
%attr(755,root,root) %{_libdir}/rpm/install-build-tree
%attr(755,root,root) %{_libdir}/rpm/brp-*
%attr(755,root,root) %{_libdir}/rpm/check-prereqs
%attr(755,root,root) %{_libdir}/rpm/compress-doc
%attr(755,root,root) %{_libdir}/rpm/cpanflute
%attr(755,root,root) %{_libdir}/rpm/http.req
%attr(755,root,root) %{_libdir}/rpm/magic.*
%attr(755,root,root) %{_libdir}/rpm/rpmi
%attr(755,root,root) %{_libdir}/rpm/u_pkg.sh
%attr(755,root,root) %{_libdir}/rpm/rpme
%attr(755,root,root) %{_libdir}/rpm/rpmu
%attr(755,root,root) %{_libdir}/rpm/rpmb
%attr(755,root,root) %{_libdir}/rpm/rpmi
%attr(755,root,root) %{_libdir}/rpm/rpmt
%attr(755,root,root) %{_libdir}/rpm/rpme
%attr(755,root,root) %{_libdir}/librpm*.la
%attr(755,root,root) %{_libdir}/librpm*.so
%files devel
%defattr(644,root,root,755)
%{_includedir}/rpm
%attr(755,root,root) %{_libdir}/librpm*.la
%attr(755,root,root) %{_libdir}/librpm*.so

%files static
%attr(755,root,root) %{_bindir}/*
%files utils
%defattr(644,root,root,755)
%{_mandir}/man1/*
%{_mandir}/man8/rpm2cpio.8*
%lang(ja) %{_mandir}/ja/man8/rpm2cpio.8*
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man8/rpm2cpio.8*
%lang(ko) %{_mandir}/ko/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpm2cpio.8*
%lang(ru) %{_mandir}/ru/man8/rpm2cpio.8*

%files perlprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm/perl*
%attr(755,root,root) %{_libdir}/rpm/find-perl-*
%attr(755,root,root) %{_libdir}/rpm/find-*.perl
%attr(755,root,root) %{_libdir}/rpm/find-prov.pl

%files -n python-rpm
* %{date} PLD Team <pld-list@pld.org.pl>
%{py_sitedir}/*.so
