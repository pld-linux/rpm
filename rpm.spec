Summary:	Red Hat (and now also PLD) Package Manager
Summary(pl):	Aplikacja do zarz±dzania pakietami
Name:		rpm
Version:	4.0.1
Release:	1
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
License:	GPL
Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.0.x/%{name}-%{version}.tar.gz
Source1:	%{name}.groups
Source2:	%{name}.macros
Source3:	%{name}-install-tree
Source4:	%{name}-find-rpm-provides
Source5:	%{name}-macros.perl
Source6:	%{name}-find-perl-provides
Source7:	%{name}-find-perl-requires
Source8:	%{name}-find-spec-bcond
Patch0:		%{name}-rpmrc.patch
Patch1:		%{name}-find-requires.patch
Patch2:		%{name}-macros.patch
Patch3:		%{name}-arch.patch
Patch4:		%{name}-rpmpopt.patch
Patch5:		%{name}-find-provides.patch
Patch6:		%{name}-perl-macros.patch
Patch7:		%{name}-file3.31.patch
Patch8:		%{name}-exclude-examples-doc.patch
Patch9:		%{name}-db3.patch
Patch10:	%{name}-rpm-v1.patch
#Patch11:	%{name}-rpmlibprov.patch
Patch12:	%{name}-segv.patch
#Patch13:        %{name}-rpmlibprov-order.patch
Patch14:	%{name}-am_fix.patch
Patch15:	%{name}-perl-req-perlfile.patch
Patch16:	%{name}-installplatform.patch
Patch17:	%{name}-find-lang.patch
Patch18:	%{name}-cache.patch
Patch37:        %{name}-short_circuit.patch
Patch38:        %{name}-section_test.patch
BuildRequires:	gettext-devel
BuildRequires:	automake
BuildRequires:	db3-devel >= 3.1.17
BuildRequires:	bzip2-devel >= 1.0.1
BuildRequires:	gdbm-devel
BuildRequires:	zlib-devel
BuildRequires:	gettext-devel >= 0.10.38-3
BuildRequires:	libtool
BuildRequires:	automake
BuildRequires:	autoconf >= 2.13-8
%if %{!?bcond_off_static:1}%{?bcond_off_static:0}
BuildRequires:	zlib-devel >= 1.1.4
# Require static library only for static build
BuildRequires:	db3-static >= 3.1.17
BuildRequires:	bzip2-static >= 1.0.1
BuildRequires:	gdbm-static
BuildRequires:	zlib-static
%endif
BuildRequires:	zlib-static >= 1.1.4
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
nombre, versión y descripción.
RPM jest doskona³ym menad¿erem pakietów. Dziêki niemu bêdziesz móg³
%description -l pl
RPM jest doskona³ym mened¿erem pakietów. Dziêki niemu bêdziesz móg³
wchodz±cych w sk³ad pakietu, zale¿no¶ci od innych pakietów s±
przechowywane s± w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
wchodz±cych w sk³ad pakietu, zale¿no¶ci od innych pakietów, s±
przechowywane w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
%package libs
Summary:	RPM shared libraries
Summary(pl):	Biblioteki wspó³dzielone rpm-a
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Requires:	%{name} = %{version}

%description libs
RPM shared libraries.

%description -l pl libs
Biblioteki wspó³dzielone rpm-a.

do pacote, permissões dos arquivos, etc.
Summary:	Header files and libraries 
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne	
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-libs = %{version}
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	popt-devel

%description devel
The RPM packaging system includes a C library that makes it easy to
manipulate RPM packages and databases. It is intended to ease the
creation of graphical package managers and other tools that need
%description -l pl devel
Pliki nag³ówkowe i biblioteki statyczne.
graficznych mened¿erów pakietów oraz innych narzêdzi, które wymagaj±
ferramentas que precisem de conhecimento profundo de pacotes RPM.

Summary(pl):	Biblioteki statyczne rpm-a
Summary(pl):	Biblioteki statyczne RPM-a
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Summary(pt_BR):	Bibliotecas estáticas para o desenvolvimento de aplicações RPM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
%description -l pl static
Biblioteki statyczne rpm-a.
%description static -l pl
Bibliotecas estáticas para desenvolvimento.

Summary(pl):	Dodatkowe narzêdzia do zarz±dzania baz± rpm-a i pakietami
Summary(de):	Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken
Group(de):	Applikationen/Datei
Group(pl):	Aplikacje/Pliki
Summary(pl):	Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami
Group:		Applications/File
Requires:	%{name} = %{version}

%description utils
%description -l pl utils
Dodatkowe narzêdzia do zarz±dzania baz± rpm-a i pakietami.
%description utils -l pl
Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami.
Summary:	Additional utilities for check perl provides/requires in rpm packages
Summary(pl):	Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci dla skryptów perl w pakietach rpm
Summary(de):	Zusatzwerkzeuge fürs Nachsehen Perl-Abhängigkeiten in RPM-Paketen
Group(de):	Applikationen/Datei
Group(pl):	Aplikacje/Pliki
Summary(pl):	Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów perla w pakietach rpm
Requires:	perl-modules
Requires:	findutils
Additional utilities for checking perl provides/requires in rpm packages.
Additional utilities for checking perl provides/requires in rpm
%description -l pl perlprov
Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci dla skryptów perl w
%description perlprov -l pl
Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów perla w
Python para manipular pacotes e bancos de dados RPM.

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
Requires:	tar
Requires:	textutils

%description build
%description -l pl build
Skrypty pomocnicze do budowania binarnych RPMów.
%description build -l pl
construir pacotes usando o RPM.
%setup  -q
%prep
%patch1 -p1
%patch0 -p1
%patch1 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1 
%patch7 -p1 
%patch8 -p1
%patch7 -p1
#%patch10 -p1
#%patch11 -p1
%patch12 -p1
#%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch31 -p1
install %{SOURCE2} macros.pld.in
%patch38 -p1
sed -e 's/^/@pld@/' %{SOURCE2} >>platform.in
cp -f platform.in macros.pld.in
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

autoheader
autoconf
# ugly workaround for automake
sed -e 's#cpio.c $(DBLIBOBJS) depends.c#cpio.c depends.c#g' \
	lib/Makefile.am > lib/Makefile.am.new
mv lib/Makefile.am.new lib/Makefile.am
automake -a -c
sed -e 's#cpio.c depends.c#cpio.c $(DBLIBOBJS) depends.c#g' \
	lib/Makefile.in > lib/Makefile.in.new
mv lib/Makefile.in.new lib/Makefile.in
%configure \
	sed 's|@host_cpu@|%{_target_cpu}|' > macros.tmp
	--enable-v1-packages
%configure \
%{__make} %{?bcond_off_static:rpm_LDFLAGS="\\$(myLDFLAGS)"}
	--with-python


%{__make} %{?_without_static:rpm_LDFLAGS="\\$(myLDFLAGS)"}

	DESTDIR="$RPM_BUILD_ROOT" \
rm -rf $RPM_BUILD_ROOT

install macros.pld $RPM_BUILD_ROOT%{_libdir}/rpm/macros.pld
%{__make} install \
	pkgbindir="%{_bindir}"

install macros.perl $RPM_BUILD_ROOT%{_libdir}/rpm/macros.perl
install macros.python $RPM_BUILD_ROOT%{_libdir}/rpm/macros.python

install %{SOURCE8} $RPM_BUILD_ROOT%{_libdir}/rpm/find-spec-bcond
install %{SOURCE10} $RPM_BUILD_ROOT%{_libdir}/rpm/find-provides
install %{SOURCE11} $RPM_BUILD_ROOT%{_libdir}/rpm/find-requires
#%%_install_langs pl_PL:en_US
%%distribution PLD
EOF

%find_lang %{name}

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
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
%attr(755,root,root) %{_libdir}/rpm/rpmdb
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
%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librpm*.so.*.*

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
