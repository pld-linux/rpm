%define	beecrypt_ver	2.2.0
Summary:	RPM Package Manager
Summary(de):	RPM Packet-Manager
Summary(es):	Gestor de paquetes RPM
Summary(pl):	Aplikacja do zarz±dzania pakietami RPM
Summary(pt_BR):	Gerenciador de pacotes RPM
Name:		rpm
Version:	4.0.4
Release:	0.71
License:	GPL
Group:		Base
Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.0.x/%{name}-%{version}.tar.gz
Source1:	%{name}.groups
Source2:	%{name}.macros
Source3:	%{name}-install-tree
Source4:	%{name}-find-%{name}-provides
Source5:	%{name}-macros.perl
Source6:	%{name}-find-perl-provides
Source7:	%{name}-find-perl-requires
Source8:	%{name}-find-spec-bcond
Source9:	%{name}-find-lang
Source10:	%{name}-find-provides
Source11:	%{name}-find-requires
Source12:	%{name}-non-english-man-pages.tar.bz2
Source13:	%{name}-macros.python
Source14:	%{name}-groups-po.awk
Patch0:		%{name}-%{name}rc.patch
Patch2:		%{name}-arch.patch
Patch3:		%{name}-%{name}popt.patch
Patch4:		%{name}-perl-macros.patch
Patch5:		%{name}-am_fix.patch
Patch6:		%{name}-perl-req-perlfile.patch
Patch7:		%{name}-installplatform.patch
Patch8:		%{name}-cache.patch
Patch9:		%{name}-glob.patch
Patch10:	%{name}-header_h.patch
Patch11:	%{name}-fast-alAddPackage.patch
Patch12:	%{name}-byKey.patch
Patch13:	%{name}-noexpand.patch
Patch14:	%{name}-scripts-closefds.patch
Patch15:	%{name}-python-amfix.patch
Patch16:	%{name}-non-english-man-pages.patch
Patch17:	%{name}-python-macros.patch
Patch18:	%{name}-perlprov-regonly.patch
Patch19:	%{name}-acconfig.patch
Patch20:	%{name}-db4.patch
Patch21:	%{name}-pl.po.patch
Patch22:	%{name}-drop-legacy-CLI.patch
Patch23:	%{name}-perlprov-perl5.6.patch
Patch24:	%{name}-ac25x.patch
Patch25:	%{name}-gettext-in-header.patch
Patch37:        %{name}-short_circuit.patch
Patch38:        %{name}-section_test.patch
BuildRequires:	autoconf >= 2.52
Icon:		rpm.gif
BuildRequires:	autoconf >= 2.50
BuildRequires:	db4-devel >= 4.0.14
BuildRequires:	doxygen
BuildRequires:	db1-devel >= 1.85
BuildRequires:	db3-devel >= 3.1.17-9
BuildRequires:	gettext-devel >= 0.10.38-3
BuildRequires:	python-devel >= 2.2
BuildRequires:	python-modules >= 2.2
BuildRequires:	zlib-devel
BuildRequires:	python-modules >= 2.2.1
BuildRequires:	zlib-devel >= 1.1.4
%if %{!?_without_static:1}%{?_without_static:0}
BuildRequires:	db4-static >= 4.0.14-2
BuildRequires:	db1-static >= 1.85
BuildRequires:	zlib-static
BuildRequires:	glibc-static >= 2.2.0
BuildRequires:	zlib-static >= 1.1.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	rpm-libs
Conflicts:	glibc < 2.2

%define		__find_provides	%{SOURCE4}
%define		_binary_payload	w9.gzdio

%define		py_ver		%(echo `python -c "import sys; print sys.version[:3]"`)
%define		py_prefix	%(echo `python -c "import sys; print sys.prefix"`)
%define		py_libdir	%{py_prefix}/lib/python%{py_ver}
%define		py_dyndir	%{py_libdir}/lib-dynload
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
Beschreibung.

%description -l es
RPM es un poderoso administrador de paquetes, que puede ser usado para
construir, instalar, pesquisar, verificar, actualizar y desinstalar
paquetes individuales de software. Un paquete consiste en un
almacenaje de archivos, y información sobre el paquete, incluyendo
nombre, versión y descripción.

%description -l pl
RPM jest doskona³ym mened¿erem pakietów. Dziêki niemu bêdziesz móg³
przebudowaæ, zainstalowaæ czy zweryfikowaæ dowolny pakiet. Informacje
dotycz±ce ka¿dego pakietu, takie jak jego opis, lista plików
wchodz±cych w sk³ad pakietu, zale¿no¶ci od innych pakietów, s±
przechowywane w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
odpytywania programu rpm.

%description -l pt_BR
RPM é um poderoso gerenciador de pacotes, que pode ser usado para
construir, instalar, pesquisar, verificar, atualizar e desinstalar
pacotes individuais de software. Um pacote consiste de um conjunto de
arquivos e informações adicionais, incluindo nome, versão e descrição
do pacote, permissões dos arquivos, etc.

%package devel
Summary:	Header files and libraries
Summary(de):	Header-Dateien uns Libraries
Summary(es):	Archivos de inclusión y bibliotecas para programas de manipulación de paquetes rpm
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne
Summary(pt_BR):	Arquivos de inclusão e bibliotecas para programas de manipulação de pacotes RPM
Group:		Development/Libraries
Requires:	beecrypt-devel
Requires:	db4-devel
Requires:	%{name} = %{version}
Requires:	popt-devel

%description devel
The RPM packaging system includes a C library that makes it easy to
manipulate RPM packages and databases. It is intended to ease the
creation of graphical package managers and other tools that need
intimate knowledge of RPM packages.

%description devel -l de
Der RPM-Packensystem enthält eine C-Library, die macht es einfach
RPM-Pakete und Dateibanken zu manipulieren. Er eignet sich für
Vereinfachung des Schaffens grafischer Paket-Manager und anderer
Werkzeuge, die intime Kenntnis von RPM-Paketen brauchen.

%description devel -l es
El sistema de empaquetado RPM incluye una biblioteca C que vuelve
fácil la manipulación de paquetes y bases de datos RPM. Su objetivo es
facilitar la creación de administradores gráficos de paquetes y otras
herramientas que necesiten un conocimiento profundo de paquetes RPM.

%description devel -l pl
System RPM zawiera bibliotekê C, która u³atwia manipulowanie pakietami
RPM oraz bazami danych. W zamiarze ma to upro¶ciæ tworzenie
graficznych mened¿erów pakietów oraz innych narzêdzi, które wymagaj±
szczegó³owej wiedzy na temat pakietów RPM.

%description devel -l pt_BR
O sistema de empacotamento RPM inclui uma biblioteca C que torna fácil
a manipulação de pacotes e bases de dados RPM. Seu objetivo é
facilitar a criação de gerenciadores gráficos de pacotes e outras
ferramentas que precisem de conhecimento profundo de pacotes RPM.

%package static
Summary:	RPM static libraries
Summary(de):	RPMs statische Libraries
Summary(pl):	Biblioteki statyczne RPM-a
Summary(pt_BR):	Bibliotecas estáticas para o desenvolvimento de aplicações RPM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
RPM static libraries.

%description static -l de
RPMs statische Libraries.

%description static -l pl
Biblioteki statyczne RPM-a.

%description static -l pt_BR
Bibliotecas estáticas para desenvolvimento.

%package utils
Summary:	Additional utilities for managing rpm packages and database
Summary(de):	Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken
Summary(pl):	Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami
Requires:	popt >= 1.6.4
Group:		Applications/File
Requires:	%{name} = %{version}

%description utils
Additional utilities for managing rpm packages and database.

%description utils -l de
Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken.

%description utils -l pl
Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami.

%package perlprov
Summary:	Additional utilities for checking perl provides/requires in rpm packages
Summary(de):	Zusatzwerkzeuge fürs Nachsehen Perl-Abhängigkeiten in RPM-Paketen
Summary(pl):	Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów perla w pakietach rpm
Group:		Applications/File
Requires:	perl-modules
Requires:	findutils

%description perlprov
Additional utilities for checking perl provides/requires in rpm
packages.

%description perlprov -l de
Zusatzwerkzeuge fürs Nachsehen Perl-Abhängigkeiten in RPM-Paketen.

%description perlprov -l pl
Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów perla w
pakietach rpm.

%package pythonprov
Summary:	Python macros, which simplifies creation of rpm packages with Python software
Summary(pl):	Makra u³atwiaj±ce tworzenie pakietów rpm z programami napisanymi w Pythonie
Group:		Applications/File
Requires:	%{name} = %{version}
Requires:	python-modules

%description pythonprov
Python macros, which simplifies creation of rpm packages with Python
software.

%description pythonprov -l pl
Makra u³atwiaj±ce tworzenie pakietów rpm z programami napisanymi w
Pythonie.

%package -n python-rpm
Summary:	Python interface to RPM library
Group:		Development/Languages/Python
Summary(pt_BR):	Módulo Python para aplicativos que manipulam pacotes RPM
%requires_eq	python
Requires:	%{name} = %{version}
%pyrequires_eq	python
Obsoletes:	rpm-python

%description -n python-rpm
The rpm-python package contains a module which permits applications
written in the Python programming language to use the interface
supplied by RPM (RPM Package Manager) libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.

%description -n python-rpm -l pl
Pakiet rpm-python zawiera modu³, który pozwala aplikacjom napisanym w
Pythonie na u¿ywanie interfejsu dostarczanego przez biblioteki RPM-a.

Pakiet ten powinien zostaæ zainstalowany, je¶li chcesz pisaæ w
Pythonie programy manipuluj±ce pakietami i bazami danych rpm.

%description -n python-rpm -l pt_BR
O pacote rpm-python contém um módulo que permite que aplicações
escritas em Python utilizem a interface fornecida pelas bibliotecas
RPM (RPM Package Manager).

Esse pacote deve ser instalado se você quiser desenvolver programas em
%package lib
Summary:	RPMs library
Summary(pl):	Biblioteki RPMa
Group:		Libraries

%description lib
RPMs library.

%description lib -l pl
Biblioteki RPMa.

%description -n beecrypt-static -l pl
Statyczna wersja biblioteki kryptograficznej.

%package build
Summary:        Scripts for building binary RPM packages
Summary(de):    Scripts fürs Bauen binärer RPM-Pakete
Summary(pl):    Skrypty pomocnicze do budowania binarnych RPM-ów
Summary(pt_BR): Scripts e programas executáveis usados para construir pacotes
Group:          Applications/File
Requires:       %{name} = %{version}
Requires:       /bin/id
Requires:       awk
Requires:       binutils
Requires:       diffutils
Requires:       file >= 3.31
Requires:       fileutils
Requires:       findutils
%ifarch athlon
Requires:       gcc >= 3.0.3
%else
Requires:       gcc
%endif
Requires:       glibc-devel
Requires:       grep
Requires:       gzip
Requires:       make
Requires:       patch
Requires:       popt >= 1.6.2-2
Requires:       sed
Requires:       sh-utils
Requires:       tar
Requires:       textutils
Requires:       popt >= 1.6.4

%description build
Scripts for building binary RPM packages.

%description build -l de
Scripts fürs Bauen binärer RPM-Pakete.

%description build -l pl
Skrypty pomocnicze do budowania binarnych RPM-ów.

%description build -l pt_BR
Este pacote contém scripts e programas executáveis que são usados para
construir pacotes usando o RPM.

%package -n beecrypt
Summary:	Crypto library
Summary(pl):	Biblioteka kryptograficzna
Version:	%{beecrypt_ver}
Epoch:		1
Group:		Libraries

%description -n beecrypt
Crypto library

%description -n beecrypt -l pl
Biblioteka kryptograficzna.

%package -n beecrypt-devel
Summary:	Crypto library - development files
Summary(pl):	Biblioteka kryptograficzna - pliki developerskie.
Version:	%{beecrypt_ver}
Group:		Development/Libraries
Requires:	beecrypt = %{beecrypt_ver}
Epoch:		1

%description -n beecrypt-devel
Crypto library - development files.

%description -n beecrypt-devel -l pl
Biblioteka kryptograficzna - pliki developerskie.

%package -n beecrypt-static
Summary:	Crypto library - static version
Summary(pl):	Statyczna biblioteka kryptograficzna
Version:	%{beecrypt_ver}
Group:		Development/Libraries
Requires:	beecrypt-devel = %{beecrypt_ver}
Epoch:		1

%description -n beecrypt-static
Static version of crypto library.

%description -n beecrypt-static -l pl
Statyczna wersja biblioteki kryptograficznej.

construir pacotes usando o RPM.

%prep
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch11 -p1
# too many rejects, Pawel please check if needed and rediff
#%patch12 -p0
%patch11 -p0
%patch12 -p0
%patch15 -p1
%patch16 -p1
%patch15 -p0
%patch16 -p0
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch22 -p1 -b .wiget
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch31 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1

sed -e 's/^/@pld@/' %{SOURCE2} >>platform.in
cp -f platform.in macros.pld.in
install %{SOURCE9} scripts/find-lang.sh
install %{SOURCE13} macros.python.in
install %{SOURCE6} scripts/find-perl-provides
install %{SOURCE7} scripts/find-perl-requires
install %{SOURCE9} scripts/find-lang.sh

(cd scripts;
mv -f perl.req perl.req.in
mv -f perl.prov perl.prov.in)
# generate Group translations to *.po
awk -f %{SOURCE14} %{SOURCE1}

%build
# generate Group translations to *.po
awk -f %{SOURCE14} %{SOURCE1}

cd popt
autoconf
automake -a -c -f
cd ../beecrypt
rm -f missing
libtoolize --force --copy
aclocal
autoheader
autoconf
automake -a -c -f
aclocal
autoheader
automake -a -c -f
%{__automake}
cd ..

rm -f missing
libtoolize --force --copy
autoconf
automake -a -c -f

sed -e 's#python1.5#python%{py_ver}#g' \
	python/Makefile.in > python/Makefile.in.new
sed -e 's|@host@|%{_target_cpu}-%{_target_vendor}-linux-gnu|'  \
	-e 's|@host_cpu@|%{_target_cpu}|'  macros.in  > macros.tmp
# config.guess doesn't handle athlon, so we have to change it by hand.
# rpm checks for CPU type at runtime, but it looks better
sed -e 's|@host@|%{_target_cpu}-%{_target_vendor}-linux-gnu|' macros.in | \
	sed 's|@host_cpu@|%{_target_cpu}|' > macros.tmp
	--enable-static \
	--with-apidocs \
	--with-python \
	--without-db
%configure \
%{__make} \
	%{?_without_static:rpm_LDFLAGS="\\$(myLDFLAGS)"} \
	myLDFLAGS="%{rpmldflags}"
	--with-python


%{__make} %{?_without_static:rpm_LDFLAGS="\\$(myLDFLAGS)"}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
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

# DON'T BREAK BUILD TREE!!!
# rm -f doc/manual/Makefile*

gzip -9nf RPM-PGP-KEY CHANGES doc/manual/*

%post   -n beecrypt -p /sbin/ldconfig
%postun -n beecrypt -p /sbin/ldconfig
%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig


%attr(755,root,root) %{_libdir}/rpm/rpmq
%attr(755,root,root) %{_libdir}/rpm/rpmk
%attr(755,root,root) %{_libdir}/rpm/rpmv
%attr(755,root,root) %{_libdir}/librpm*.so.*.*

%dir %{_sysconfdir}/rpm
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/rpm/macros

%{_mandir}/man8/rpm.8*
%lang(fr) %{_mandir}/fr/man8/rpm.8*
%lang(ja) %{_mandir}/ja/man8/rpm.8*
%lang(ko) %{_mandir}/ko/man8/rpm.8*
%lang(pl) %{_mandir}/pl/man8/rpm.8*
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%lang(sk) %{_mandir}/sk/man8/rpm.8*

%dir /var/lib/rpm
%dir %{_libdir}/rpm

%{_libdir}/rpm/noarch-*
%{_libdir}/rpm/rpmrc
%{_libdir}/rpm/rpmpopt*
%{_libdir}/rpm/macros
%{_libdir}/rpm/noarch-linux
%{_libdir}/rpm/noarch-pld-linux
%ifarch i386 i486 i586 i686 athlon
%{_libdir}/rpm/i?86*
%{_libdir}/rpm/athlon*
%endif
%ifarch sparc sparc64
%{_libdir}/rpm/sparc*
%endif
%ifarch alpha
%{_libdir}/rpm/alpha*
%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librpm*-*.so
%endif
%ifarch ppc
%{_libdir}/rpm/ppc*
%attr(755,root,root) %{_libdir}/rpm/cross-build
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
%attr(755,root,root) %{_libdir}/rpm/compress-doc
%attr(755,root,root) %{_libdir}/rpm/cpanflute
%attr(755,root,root) %{_libdir}/rpm/http.req
%attr(755,root,root) %{_libdir}/rpm/magic.*
%attr(755,root,root) %{_libdir}/rpm/u_pkg.sh
# not used yet ...
%{_libdir}/rpm/sql.prov
%{_libdir}/rpm/sql.req
%{_libdir}/rpm/tcl.req
%{_libdir}/rpm/trpm

%attr(755,root,root) %{_bindir}/javadeps
%attr(755,root,root) %{_bindir}/gendiff
%attr(755,root,root) %{_bindir}/rpmbuild

%{_mandir}/man1/*
%{_mandir}/man8/rpmbuild.8*
%attr(755,root,root) %{_libdir}/rpm/rpmb
%attr(755,root,root) %{_libdir}/rpm/rpmi
%attr(755,root,root) %{_libdir}/rpm/rpmt
%attr(755,root,root) %{_libdir}/rpm/rpme
%attr(755,root,root) %{_libdir}/librpm.la
%attr(755,root,root) %{_libdir}/librpm.so
%attr(755,root,root) %{_libdir}/librpmio.la
%attr(755,root,root) %{_libdir}/librpmio.so
%attr(755,root,root) %{_libdir}/librpmdb.la
%attr(755,root,root) %{_libdir}/librpmdb.so
%attr(755,root,root) %{_libdir}/librpmbuild.la
%attr(755,root,root) %{_libdir}/librpmbuild.so
%files devel
%defattr(644,root,root,755)
%{_includedir}/rpm
%attr(755,root,root) %{_libdir}/librpm*.la
%attr(755,root,root) %{_libdir}/librpm*.so

%files static
%attr(755,root,root) %{_bindir}/rpm2cpio
%attr(755,root,root) %{_libdir}/rpm/rpmdiff*
# not here
#%{_prefix}/lib/rpm/rpm.daily
#%{_prefix}/lib/rpm/rpm.log
#%{_prefix}/lib/rpm/rpm.xinetd
%{_prefix}/lib/rpm/rpm2cpio.sh
%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/javadeps
%attr(755,root,root) %{_bindir}/rpm2cpio

%{_mandir}/man8/rpm2cpio.8*
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
%attr(755,root,root) %{_libdir}/rpm/find-req.pl
%attr(755,root,root) %{_libdir}/rpm/get_magic.pl

%{_libdir}/rpm/macros.perl
# this subpackage need fix
#%files -n python-rpm
#%defattr(644,root,root,755)
#%{py_sitedir}/*.so

%files -n beecrypt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbeecrypt.so.*.*

%files -n beecrypt-devel
%defattr(644,root,root,755)
%{_prefix}/lib/libbeecrypt.so
%attr(755,root,root) %{_prefix}/lib/libbeecrypt.la
%{_includedir}/beecrypt
%{_libdir}/rpm/macros.python
%files -n beecrypt-static
%defattr(644,root,root,755)
%{_prefix}/lib/libbeecrypt.a


%files -n python-rpm
%defattr(755,root,root,755)
%{py_sitedir}/*.so
