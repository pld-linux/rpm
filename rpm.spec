#
# TODO:
# - python(abi) cap is not provided automatically (because /usr/bin/python matches
#   ELF first; it should be provided by python-libs not binary anyway)
# - consider using system libmagic not internal libfmagic
#   (but internal has different method of passing output)
# 
# Conditional build:
%bcond_with	static		# build static rpmi (not supported at the moment)
%bcond_without	apidocs		# don't generate documentation with doxygen
%bcond_with	autoreqdep	# autogenerate package name deps in addition to sonames/perl(X)
%bcond_without	python		# don't build python bindings
%bcond_without	selinux		# build without selinux support
# force_cc		- force using __cc other than "%{_target_cpu}-pld-linux-gcc"
# force_cxx		- force using __cxx other than "%{_target_cpu}-pld-linux-g++"
# force_cpp		- force using __cpp other than "%{_target_cpu}-pld-linux-gcc -E"

# versions of required libraries
%define	reqdb_ver	4.3.27-1
%define	reqpopt_ver	1.10.1
%define	beecrypt_ver	2:4.1.0
%define	rpm_macros_rev	1.213
Summary:	RPM Package Manager
Summary(de):	RPM Packet-Manager
Summary(es):	Gestor de paquetes RPM
Summary(pl):	Aplikacja do zarz±dzania pakietami RPM
Summary(pt_BR):	Gerenciador de pacotes RPM
Summary(ru):	íÅÎÅÄÖÅÒ ÐÁËÅÔÏ× ÏÔ RPM
Summary(uk):	íÅÎÅÄÖÅÒ ÐÁËÅÔ¦× ×¦Ä RPM
Name:		rpm
%define	sover	4.4
Version:	4.4.1
Release:	1.10
License:	GPL
Group:		Base
Source0:	ftp://jbj.org/pub/rpm-4.4.x/%{name}-%{version}.tar.gz
# Source0-md5:	90ded9047b1b69d918c6c7c7b56fd7a9
Source1:	%{name}.groups
Source2:	%{name}.platform
Source3:	%{name}-install-tree
Source4:	%{name}-find-spec-bcond
Source5:	%{name}-find-lang
Source6:	%{name}-groups-po.awk
Source7:	%{name}-compress-doc
Source8:	%{name}-check-files
Source9:	%{name}-php-provides
Source10:	%{name}-php-requires
Source11:	%{name}.macros
Source12:	perl.prov
Source13:	%{name}-user_group.sh
Source14:	%{name}.sysconfig
Source30:	builder
Source31:	adapter.awk
Source32:	pldnotify.awk
# http://svn.pld-linux.org/banner.sh/
Source33:	banner.sh
Patch0:		%{name}-pl.po.patch
Patch1:		%{name}-rpmrc.patch
Patch2:		%{name}-arch.patch
Patch3:		%{name}-rpmpopt.patch
Patch4:		%{name}-perl-macros.patch
Patch5:		%{name}-perl-req-perlfile.patch
Patch6:		%{name}-noexpand.patch
Patch7:		%{name}-scripts-closefds.patch
Patch8:		%{name}-python-macros.patch
Patch9:		%{name}-gettext-in-header.patch
Patch10:	%{name}-compress-doc.patch
Patch11:	%{name}-build.patch
Patch12:	%{name}-system_libs.patch
Patch13:	%{name}-bb-and-short-circuit.patch
Patch14:	%{name}-etc_dir.patch
Patch15:	%{name}-system_libs-more.patch
Patch16:	%{name}-php-deps.patch
Patch17:	%{name}-ldconfig-always.patch
Patch18:	%{name}-perl_req.patch
Patch19:	%{name}-no-bin-env.patch
Patch20:	%{name}-magic-usesystem.patch
Patch21:	%{name}-dontneedutils.patch
Patch22:	%{name}-provides-dont-obsolete.patch
Patch23:	%{name}-examplesaredoc.patch
Patch24:	%{name}-po.patch
Patch25:	%{name}-getcwd.patch
Patch26:	%{name}-notsc.patch
Patch27:	%{name}-hack-norpmlibdep.patch
Patch28:	%{name}-makefile-no_myLDADD_deps.patch
Patch29:	%{name}-libdir64.patch
Patch30:	%{name}-libdir-links.patch
Patch31:	%{name}-missing-prototypes.patch
Patch32:	%{name}-pld-autodep.patch
Patch33:	%{name}-rpmsq.patch
Patch34:	%{name}-epoch0.patch
Patch35:	%{name}-perl_req-INC_dirs.patch
Patch36:	%{name}-debuginfo.patch
Patch37:	%{name}-doxygen_hack.patch
Patch38:	%{name}-gcc4.patch
Patch39:	%{name}-pythondeps.patch
Patch40:	%{name}-print-requires.patch
Patch41:	%{name}-reduce-stack-usage.patch
URL:		http://www.rpm.org/
Icon:		rpm.gif
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	beecrypt-devel >= %{beecrypt_ver}
BuildRequires:	bzip2-devel >= 1.0.1
BuildRequires:	db-devel >= %{reqdb_ver}
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	elfutils-devel
BuildRequires:	findutils
BuildRequires:	gettext-devel >= 0.11.4-2
#BuildRequires:	libmagic-devel
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.18}
# needed only for AM_PROG_CXX used for CXX substitution in rpm.macros
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	neon-devel >= 0.24.7-3
BuildRequires:	patch >= 2.2
BuildRequires:	popt-devel >= %{reqpopt_ver}
%{?with_python:BuildRequires:	python-devel >= 2.2}
BuildRequires:	python-modules >= 2.2
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	zlib-devel
%if %{with static}
# Require static library only for static build
BuildRequires:	beecrypt-static >= %{beecrypt_ver}
BuildRequires:	bzip2-static >= 1.0.2-5
BuildRequires:	db-static >= %{reqdb_ver}
BuildRequires:	glibc-static >= 2.2.94
BuildRequires:	elfutils-static
#BuildRequires:	libmagic-static
%{?with_selinux:BuildRequires:	libselinux-static >= 1.18}
BuildRequires:	popt-static >= %{reqpopt_ver}
BuildRequires:	zlib-static
%endif
Requires:	beecrypt >= %{beecrypt_ver}
Requires:	popt >= %{reqpopt_ver}
Requires:	%{name}-lib = %{version}-%{release}
%{!?with_static:Obsoletes:	rpm-utils-static}
Conflicts:	glibc < 2.2.92
# avoid SEGV caused by mixed db versions
Conflicts:	poldek < 0.18.1-16
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_binary_payload		w9.gzdio
%define		_noPayloadPrefix	1

# don't require very fresh rpm.macros to build
%define		__gettextize gettextize --copy --force --intl ; cp -f po/Makevars{.template,}
%define		ix86	i386 i486 i586 i686 athlon pentium3 pentium4
%define		x8664	amd64 ia32e x86_64

# stabilize new build environment
%define		__newcc %{?force_cc}%{!?force_cc:%{_target_cpu}-pld-linux-gcc}
%define		__newcxx %{?force_cxx}%{!?force_cxx:%{_target_cpu}-pld-linux-g++}
%define		__newcpp %{?force_cpp}%{!?force_cpp:%{_target_cpu}-pld-linux-gcc -E}

%define		_rpmlibdir /usr/lib/rpm

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
RPM jest doskona³ym programem zarz±dzaj±cym pakietami. Umo¿liwia on
przebudowanie, instalacjê czy weryfikacjê dowolnego pakietu.
Informacje dotycz±ce ka¿dego pakietu, takie jak jego opis, lista
plików wchodz±cych w sk³ad pakietu, zale¿no¶ci od innych pakietów, s±
przechowywane w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
odpytywania programu rpm.

%description -l pt_BR
RPM é um poderoso gerenciador de pacotes, que pode ser usado para
construir, instalar, pesquisar, verificar, atualizar e desinstalar
pacotes individuais de software. Um pacote consiste de um conjunto de
arquivos e informações adicionais, incluindo nome, versão e descrição
do pacote, permissões dos arquivos, etc.

%description -l ru
RPM - ÜÔÏ ÍÏÝÎÙÊ ÍÅÎÅÄÖÅÒ ÐÁËÅÔÏ×, ËÏÔÏÒÙÊ ÍÏÖÅÔ ÂÙÔØ ÉÓÐÏÌØÚÏ×ÁÎ ÄÌÑ
ÓÏÚÄÁÎÉÑ, ÉÎÓÔÁÌÌÑÃÉÉ, ÚÁÐÒÏÓÏ× (query), ÐÒÏ×ÅÒËÉ, ÏÂÎÏ×ÌÅÎÉÑ É
ÕÄÁÌÅÎÉÑ ÐÒÏÇÒÁÍÍÎÙÈ ÐÁËÅÔÏ×. ðÁËÅÔ ÓÏÓÔÏÉÔ ÉÚ ÆÁÊÌÏ×ÏÇÏ ÁÒÈÉ×Á É
ÓÌÕÖÅÂÎÏÊ ÉÎÆÏÒÍÁÃÉÉ, ×ËÌÀÞÁÀÝÅÊ ÎÁÚ×ÁÎÉÅ, ×ÅÒÓÉÀ, ÏÐÉÓÁÎÉÅ É ÄÒÕÇÉÅ
ÄÁÎÎÙÅ Ï ÐÁËÅÔÅ.

%description -l uk
RPM - ÃÅ ÐÏÔÕÖÎÉÊ ÍÅÎÅÄÖÅÒ ÐÁËÅÔ¦×, ÝÏ ÍÏÖÅ ÂÕÔÉ ×ÉËÏÒÉÓÔÁÎÉÊ ÄÌÑ
ÓÔ×ÏÒÅÎÎÑ, ¦ÎÓÔÁÌÑÃ¦§, ÚÁÐÉÔ¦× (query), ÐÅÒÅ×¦ÒËÉ, ÐÏÎÏ×ÌÅÎÎÑ ÔÁ
×ÉÄÁÌÅÎÎÑ ÐÒÏÇÒÁÍÎÉÈ ÐÁËÅÔ¦×. ðÁËÅÔ ÓËÌÁÄÁ¤ÔØÓÑ Ú ÆÁÊÌÏ×ÏÇÏ ÁÒÈ¦×Õ ÔÁ
ÓÌÕÖÂÏ×Ï§ ¦ÎÆÏÒÍÁÃ¦§, ÝÏ Í¦ÓÔÉÔØ ÎÁÚ×Õ, ×ÅÒÓ¦À, ÏÐÉÓ ÔÁ ¦ÎÛÕ
¦ÎÆÏÒÍÁÃ¦À ÐÒÏ ÐÁËÅÔ.

%package lib
Summary:	RPMs library
Summary(pl):	Biblioteki RPM-a
Group:		Libraries
Requires:	db >= %{reqdb_ver}
%{?with_selinux:BuildRequires:	libselinux >= 1.18}
Requires:	popt >= %{reqpopt_ver}
# avoid SEGV caused by mixed db versions
Conflicts:	poldek < 0.18.1-16

%description lib
RPMs library.

%description lib -l pl
Biblioteki RPM-a.

%package devel
Summary:	Header files for rpm libraries
Summary(de):	Header-Dateien für rpm Libraries
Summary(es):	Archivos de inclusión y bibliotecas para programas de manipulación de paquetes rpm
Summary(pl):	Pliki nag³ówkowe bibliotek rpm
Summary(pt_BR):	Arquivos de inclusão e bibliotecas para programas de manipulação de pacotes RPM
Summary(ru):	èÅÄÅÒÙ É ÂÉÂÌÉÏÔÅËÉ ÄÌÑ ÐÒÏÇÒÁÍÍ, ÒÁÂÏÔÁÀÝÉÈ Ó rpm-ÐÁËÅÔÁÍÉ
Summary(uk):	èÅÄÅÒÉ ÔÁ Â¦ÂÌ¦ÏÔÅËÉ ÄÌÑ ÐÒÏÇÒÁÍ, ÝÏ ÐÒÁÃÀÀÔØ Ú ÐÁËÅÔÁÍÉ rpm
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}
Requires:	beecrypt-devel >= %{beecrypt_ver}
Requires:	bzip2-devel
Requires:	db-devel >= %{reqdb_ver}
Requires:	elfutils-devel
%{?with_selinux:Requires:	libselinux-devel}
Requires:	popt-devel >= %{reqpopt_ver}
Requires:	zlib-devel

%description devel
The RPM packaging system includes C libraries that make it easy to
manipulate RPM packages and databases. They are intended to ease the
creation of graphical package managers and other tools that need
intimate knowledge of RPM packages. This package contains header files
for these libraries.

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
System RPM zawiera biblioteki C, które u³atwiaj± manipulowanie
pakietami RPM oraz bazami danych. W zamiarze ma to upro¶ciæ tworzenie
graficznych programów zarz±dzaj±cych pakietami oraz innych narzêdzi,
które wymagaj± szczegó³owej wiedzy na temat pakietów RPM. Ten pakiet
zawiera pliki nag³ówkowe wspomnianych bibliotek.

%description devel -l pt_BR
O sistema de empacotamento RPM inclui uma biblioteca C que torna fácil
a manipulação de pacotes e bases de dados RPM. Seu objetivo é
facilitar a criação de gerenciadores gráficos de pacotes e outras
ferramentas que precisem de conhecimento profundo de pacotes RPM.

%description devel -l ru
óÉÓÔÅÍÁ ÕÐÒÁ×ÌÅÎÉÑ ÐÁËÅÔÁÍÉ RPM ÓÏÄÅÒÖÉÔ ÂÉÂÌÉÏÔÅËÕ C, ËÏÔÏÒÁÑ
ÕÐÒÏÝÁÅÔ ÍÁÎÉÐÕÌÑÃÉÀ ÐÁËÅÔÁÍÉ RPM É ÓÏÏÔ×ÅÔÓÔ×ÕÀÝÉÍÉ ÂÁÚÁÍÉ ÄÁÎÎÙÈ.
üÔÁ ÂÉÂÌÉÏÔÅËÁ ÐÒÅÄÎÁÚÎÁÞÅÎÁ ÄÌÑ ÏÂÌÅÇÞÅÎÉÑ ÓÏÚÄÁÎÉÑ ÇÒÁÆÉÞÅÓËÉÈ
ÐÁËÅÔÎÙÈ ÍÅÎÅÄÖÅÒÏ× É ÄÒÕÇÉÈ ÕÔÉÌÉÔ, ËÏÔÏÒÙÍ ÎÅÏÂÈÏÄÉÍÏ ÒÁÂÏÔÁÔØ Ó
ÐÁËÅÔÁÍÉ RPM.

%description devel -l uk
óÉÓÔÅÍÁ ËÅÒÕ×ÁÎÎÑ ÐÁËÅÔÁÍÉ RPM Í¦ÓÔÉÔØ Â¦ÂÌ¦ÏÔÅËÕ C, ËÏÔÒÁ ÓÐÒÏÝÕ¤
ÒÏÂÏÔÕ Ú ÐÁËÅÔÁÍÉ RPM ÔÁ ×¦ÄÐÏ×¦ÄÎÉÍÉ ÂÁÚÁÍÉ ÄÁÎÉÈ. ãÑ Â¦ÂÌ¦ÏÔÅËÁ
ÐÒÉÚÎÁÞÅÎÁ ÄÌÑ ÐÏÌÅÇÛÅÎÎÑ ÓÔ×ÏÒÅÎÎÑ ÇÒÁÆ¦ÞÎÉÈ ÐÁËÅÔÎÉÈ ÍÅÎÅÄÖÅÒ¦× ÔÁ
¦ÎÛÉÈ ÕÔÉÌ¦Ô, ÝÏ ÐÒÁÃÀÀÔØ Ú ÐÁËÅÔÁÍÉ RPM.

%package static
Summary:	RPM static libraries
Summary(de):	RPMs statische Libraries
Summary(pl):	Biblioteki statyczne RPM-a
Summary(pt_BR):	Bibliotecas estáticas para o desenvolvimento de aplicações RPM
Summary(ru):	óÔÁÔÉÞÅÓËÁÑ ÂÉÂÌÉÏÔÅËÁ ÄÌÑ ÐÒÏÇÒÁÍÍ, ÒÁÂÏÔÁÀÝÉÈ Ó rpm-ÐÁËÅÔÁÍÉ
Summary(uk):	óÔÁÔÉÞÎÁ Â¦ÂÌ¦ÏÔÅËÁ ÄÌÑ ÐÒÏÇÒÁÍ, ÝÏ ÐÒÁÃÀÀÔØ Ú ÐÁËÅÔÁÍÉ rpm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	beecrypt-static >= %{beecrypt_ver}
Requires:	bzip2-static
Requires:	db-static >= %{reqdb_ver}
Requires:	elfutils-static
Requires:	popt-static >= %{reqpopt_ver}
Requires:	zlib-static

%description static
RPM static libraries.

%description static -l de
RPMs statische Libraries.

%description static -l pl
Biblioteki statyczne RPM-a.

%description static -l pt_BR
Bibliotecas estáticas para desenvolvimento.

%description static -l ru
óÉÓÔÅÍÁ ÕÐÒÁ×ÌÅÎÉÑ ÐÁËÅÔÁÍÉ RPM ÓÏÄÅÒÖÉÔ ÂÉÂÌÉÏÔÅËÕ C, ËÏÔÏÒÁÑ
ÕÐÒÏÝÁÅÔ ÍÁÎÉÐÕÌÑÃÉÀ ÐÁËÅÔÁÍÉ RPM É ÓÏÏÔ×ÅÔÓÔ×ÕÀÝÉÍÉ ÂÁÚÁÍÉ ÄÁÎÎÙÈ.
üÔÏ ÓÔÁÔÉÞÅÓËÁÑ ÂÉÂÌÉÏÔÅËÁ RPM.

%description static -l uk
óÉÓÔÅÍÁ ËÅÒÕ×ÁÎÎÑ ÐÁËÅÔÁÍÉ RPM Í¦ÓÔÉÔØ Â¦ÂÌ¦ÏÔÅËÕ C, ËÏÔÒÁ ÓÐÒÏÝÕ¤
ÒÏÂÏÔÕ Ú ÐÁËÅÔÁÍÉ RPM ÔÁ ×¦ÄÐÏ×¦ÄÎÉÍÉ ÂÁÚÁÍÉ ÄÁÎÉÈ. ãÅ ÓÔÁÔÉÞÎÁ
Â¦ÂÌ¦ÏÔÅËÁ RPM.

%package utils
Summary:	Additional utilities for managing rpm packages and database
Summary(de):	Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken
Summary(pl):	Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	popt >= %{reqpopt_ver}

%description utils
Additional utilities for managing rpm packages and database.

%description utils -l de
Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken.

%description utils -l pl
Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami.

%package utils-perl
Summary:	Additional utilities for managing rpm packages and database
Summary(de):	Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken
Summary(pl):	Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami
Group:		Applications/File
Requires:	%{name}-utils = %{version}-%{release}
Requires:	popt >= %{reqpopt_ver}

%description utils-perl
Additional utilities for managing rpm packages and database.

%description utils-perl -l de
Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken.

%description utils-perl -l pl
Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami.

%package utils-static
Summary:	Static rpm utilities
Summary(pl):	Statyczne narzêdzia rpm
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils-static
Static rpm utilities for repairing system in case something with
shared libraries used by rpm become broken. Currently it contains rpmi
binary, which can be used to install/upgrade/remove packages without
using shared libraries (well, in fact with exception of NSS modules).

%description utils-static -l pl
Statyczne narzêdzia rpm do naprawy systemu w przypadku zepsucia czego¶
zwi±zanego z bibliotekami wspó³dzielonymi u¿ywanymi przez rpm-a.
Aktualnie pakiet zawiera binarkê rpmi, któr± mo¿na u¿yæ do instalacji,
uaktualniania lub usuwania pakietów bez udzia³u bibliotek statycznych
(z wyj±tkiem modu³ów NSS).

%package build
Summary:	Scripts for building binary RPM packages
Summary(de):	Scripts fürs Bauen binärer RPM-Pakete
Summary(pl):	Skrypty pomocnicze do budowania binarnych RPM-ów
Summary(pt_BR):	Scripts e programas executáveis usados para construir pacotes
Summary(ru):	óËÒÉÐÔÙ É ÕÔÉÌÉÔÙ, ÎÅÏÂÈÏÄÉÍÙÅ ÄÌÑ ÓÂÏÒËÉ ÐÁËÅÔÏ×
Summary(uk):	óËÒÉÐÔÉ ÔÁ ÕÔÉÌ¦ÔÉ, ÎÅÏÂÈ¦ÄÎ¦ ÄÌÑ ÐÏÂÕÄÏ×É ÐÁËÅÔ¦×
Group:		Applications/File
Requires(pre):	findutils
Requires:	%{name}-utils = %{version}-%{release}
Requires:	/bin/id
Requires:	awk
Requires:	binutils
Requires:	bzip2
Requires:	chrpath >= 0.10-4
Requires:	cpio
Requires:	diffutils
Requires:	elfutils
Requires:	file >= 4.13-2
Requires:	fileutils
Requires:	findutils
# because of -fvisibility... related fixes
Requires:	gcc >= 5:4.0.1-0.20050514.2
Requires:	glibc-devel
Requires:	grep
Requires:	gzip
Requires:	make
Requires:	patch
Requires:	popt >= 1.7
Requires:	sed
Requires:	sh-utils
Requires:	tar
Requires:	textutils
Provides:	rpmbuild(macros) = %{rpm_macros_rev}
Provides:	rpmbuild(noauto) = 3
%ifarch %{x8664}
Conflicts:	automake < 1:1.7.9-2
Conflicts:	libtool < 2:1.5-13
%endif

%description build
Scripts for building binary RPM packages.

%description build -l de
Scripts fürs Bauen binärer RPM-Pakete.

%description build -l pl
Skrypty pomocnicze do budowania binarnych RPM-ów.

%description build -l pt_BR
Este pacote contém scripts e programas executáveis que são usados para
construir pacotes usando o RPM.

%description build -l ru
òÁÚÌÉÞÎÙÅ ×ÓÐÏÍÏÇÁÔÅÌØÎÙÅ ÓËÒÉÐÔÙ É ÉÓÐÏÌÎÑÅÍÙÅ ÐÒÏÇÒÁÍÍÙ, ËÏÔÏÒÙÅ
ÉÓÐÏÌØÚÕÀÔÓÑ ÄÌÑ ÓÂÏÒËÉ RPM'Ï×.

%description build -l uk
ò¦ÚÎÏÍÁÎ¦ÔÎ¦ ÄÏÐÏÍ¦ÖÎ¦ ÓËÒÉÐÔÉ ÔÁ ÕÔÉÌ¦ÔÉ, ÑË¦ ×ÉËÏÒÉÓÔÏ×ÕÀÔØÓÑ ÄÌÑ
ÐÏÂÕÄÏ×É RPM'¦×.

%package build-tools
Summary:	Scripts for managing .spec files and building RPM packages
Summary(de):	Scripts fürs Bauen binärer RPM-Pakete
Summary(pl):	Skrypty pomocnicze do zarz±dznia plikami .spec i budowania RPM-ów
Summary(pt_BR):	Scripts e programas executáveis usados para construir pacotes
Summary(ru):	óËÒÉÐÔÙ É ÕÔÉÌÉÔÙ, ÎÅÏÂÈÏÄÉÍÙÅ ÄÌÑ ÓÂÏÒËÉ ÐÁËÅÔÏ×
Summary(uk):	óËÒÉÐÔÉ ÔÁ ÕÔÉÌ¦ÔÉ, ÎÅÏÂÈ¦ÄÎ¦ ÄÌÑ ÐÏÂÕÄÏ×É ÐÁËÅÔ¦×
Group:		Applications/File
Requires:	%{name}-build = %{version}-%{release}
# these are optional
#Requires:	cvs
Requires:	wget

%description build-tools
Scripts for managing .spec files and building RPM packages.

%description build-tools -l de
Scripts fürs Bauen RPM-Pakete.

%description build-tools -l pl
Skrypty pomocnicze do zarz±dzania plikami .spec i do budowania RPM-ów.

%description build-tools -l pt_BR
Este pacote contém scripts e programas executáveis que são usados para
construir pacotes usando o RPM.

%description build-tools -l ru
òÁÚÌÉÞÎÙÅ ×ÓÐÏÍÏÇÁÔÅÌØÎÙÅ ÓËÒÉÐÔÙ É ÉÓÐÏÌÎÑÅÍÙÅ ÐÒÏÇÒÁÍÍÙ, ËÏÔÏÒÙÅ
ÉÓÐÏÌØÚÕÀÔÓÑ ÄÌÑ ÓÂÏÒËÉ RPM'Ï×.

%description build-tools -l uk
ò¦ÚÎÏÍÁÎ¦ÔÎ¦ ÄÏÐÏÍ¦ÖÎ¦ ÓËÒÉÐÔÉ ÔÁ ÕÔÉÌ¦ÔÉ, ÑË¦ ×ÉËÏÒÉÓÔÏ×ÕÀÔØÓÑ ÄÌÑ
ÐÏÂÕÄÏ×É RPM'¦×.

%package perlprov
Summary:	Additional utilities for checking perl provides/requires in rpm packages
Summary(de):	Zusatzwerkzeuge fürs Nachsehen Perl-Abhängigkeiten in RPM-Paketen
Summary(pl):	Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów perla w pakietach rpm
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	perl-devel
Requires:	perl-modules

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
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules

%description pythonprov
Python macros, which simplifies creation of rpm packages with Python
software.

%description pythonprov -l pl
Makra u³atwiaj±ce tworzenie pakietów rpm z programami napisanymi w
Pythonie.

%package php-pearprov
Summary:	Additional utilities for managing rpm packages and database
Summary(pl):	Dodatkowe narzêdzia do sprawdzania zale¿no¶ci skryptów php w rpm
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}

%description php-pearprov
Additional utilities for checking php pear provides/requires in rpm
packages.

%description php-pearprov -l pl
Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów php pear w
pakietach rpm.

%package -n python-rpm
Summary:	Python interface to RPM library
Summary(pl):	Pythonowy interfejs do biblioteki RPM-a
Summary(pt_BR):	Módulo Python para aplicativos que manipulam pacotes RPM
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
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
Python para manipular pacotes e bancos de dados RPM.

%package apidocs
Summary:	RPM API documentation and guides
Summary(pl):	Documentacja API RPM-a i przewodniki
Group:		Documentation	

%description apidocs
Documentation for RPM API and guides in HTML format generated
from rpm sources by doxygen.

%description apidocs -l pl
Dokumentacja API RPM-a oraz przewodniki w formacie HTML generowane
ze ¼rode³ RPM-a przez doxygen.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
# temporarily moved after patch0 - messes too much in pl.po
#%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
# home-etc FIXME
#%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
sed -e 's/^/@pld@/' %{SOURCE2} >>platform.in
cp -f platform.in macros.pld.in
echo '%%define	__perl_provides	%%{__perl} /usr/lib/rpm/perl.prov' > macros.perl
echo '%%define	__perl_requires	%%{__perl} /usr/lib/rpm/perl.req' >> macros.perl
echo '# obsoleted file' > macros.python
echo '%%define	__php_provides	/usr/lib/rpm/php.prov' > macros.php
echo '%%define	__php_requires	/usr/lib/rpm/php.req' >> macros.php
install %{SOURCE5} scripts/find-lang.sh
install %{SOURCE9} scripts/php.prov.in
install %{SOURCE10} scripts/php.req.in
install %{SOURCE12} scripts/perl.prov
cat %{SOURCE11} >> macros.in
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p0
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch0 -p1
%patch3 -p1

cd scripts;
mv -f perl.req perl.req.in
mv -f perl.prov perl.prov.in
cd ..

mv -f po/{no,nb}.po
mv -f po/{sr,sr@Latn}.po

rm -rf neon zlib libelf db db3 popt rpmdb/db.h

# generate Group translations to *.po
awk -f %{SOURCE6} %{SOURCE1}

# update macros paths
for f in doc{,/ja,/pl}/rpm.8 doc{,/ja,/pl}/rpmbuild.8 ; do
	sed -e 's@lib/rpm/redhat@lib/rpm/pld@g' $f > ${f}.tmp
	mv -f ${f}.tmp $f
done

# ... and make some cleanings
rm -fr $(find ./ -type d -name CVS )
rm -f  $(find ./ -type f -name ".cvsignore" )

%build
cd file
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd ..

%{__libtoolize}
%{__gettextize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

# config.guess doesn't handle athlon, so we have to change it by hand.
# rpm checks for CPU type at runtime, but it looks better
sed -e 's|@host@|%{_target_cpu}-%{_target_vendor}-linux-gnu|' \
	-e 's|@host_cpu@|%{_target_cpu}|' macros.in > macros.tmp
mv -f macros.tmp macros.in

# pass CC and CXX too in case of building with some older configure macro
%configure \
	CC="%{__newcc}" \
	CXX="%{__newcxx}" \
	CPP="%{__newcpp}" \
	--enable-shared \
	--enable-static \
	%{?with_apidoc:--with-apidocs} \
	%{?with_pkgnameinautoreq:--enable-adding-packages-names-in-autogenerated-dependancies} \
	%{?with_python:--with-python=auto} \
	%{!?with_python:--without-python} \
	%{!?with_selinux:--without-selinux} \
	--without-db

# file_LDFLAGS, debugedit_LDADD - no need to link "file" and "debugedit" statically
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CPP="%{__cpp}" \
	pylibdir=%{py_libdir} \
	myLDFLAGS="%{rpmldflags}" \
	file_LDFLAGS= \
	debugedit_LDADD="\$(WITH_LIBELF_LIB) -lpopt"

#	%{!?with_static:rpm_LDFLAGS="\$(myLDFLAGS)"} \
%{?with_apidocs:%{__make} doxygen}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib},/etc/sysconfig,%{_sysconfdir}/rpm}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pylibdir=%{py_libdir} \
	pkgbindir="%{_bindir}"

rm $RPM_BUILD_ROOT%{_rpmlibdir}/vpkg-provides*
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-{prov,req}.pl
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-{provides,requires}.perl

install macros.perl	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.perl
install macros.python	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.python
install macros.php	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.php

install %{SOURCE1} doc/manual/groups
install %{SOURCE3} $RPM_BUILD_ROOT%{_rpmlibdir}/install-build-tree
install %{SOURCE4} $RPM_BUILD_ROOT%{_rpmlibdir}/find-spec-bcond
install %{SOURCE7} $RPM_BUILD_ROOT%{_rpmlibdir}/compress-doc
install %{SOURCE8} $RPM_BUILD_ROOT%{_rpmlibdir}/check-files
install %{SOURCE13} $RPM_BUILD_ROOT%{_rpmlibdir}/user_group.sh
install scripts/find-php*	$RPM_BUILD_ROOT%{_rpmlibdir}
install scripts/php.{prov,req}	$RPM_BUILD_ROOT%{_rpmlibdir}
install %{SOURCE14} $RPM_BUILD_ROOT/etc/sysconfig/rpm

install %{SOURCE30} $RPM_BUILD_ROOT%{_bindir}/builder
install %{SOURCE31} $RPM_BUILD_ROOT%{_bindir}/adapter.awk
install %{SOURCE32} $RPM_BUILD_ROOT%{_bindir}/pldnotify.awk
install %{SOURCE33} $RPM_BUILD_ROOT%{_bindir}/banner.sh

install rpmio/ugid.h $RPM_BUILD_ROOT%{_includedir}/rpm

%ifarch %{ix86}
ix86re=$(echo "(%{ix86})"|sed 's/ /|/g')
perl -p -i -e 's/^(buildarchtranslate: '"$ix86re"': ).*/\1%{_target_cpu}/' \
	$RPM_BUILD_ROOT%{_rpmlibdir}/rpmrc
%endif

cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros <<EOF
# customized rpm macros - global for host
#
#%%_install_langs pl_PL:en_US
%%distribution PLD
#
# remove or replace with file_contexts path if you want to use custom
# SELinux file contexts policy instead of one stored in packages payload
%%_install_file_context_path	%%{nil}
%%_verify_file_context_path	%%{nil}
EOF

cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprovfiles <<EOF
# global list of files (regexps) which don't generate Provides
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprov <<EOF
# global list of script capabilities (regexps) not to be used in Provides
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreqfiles <<EOF
# global list of files (regexps) which don't generate Requires
^/usr/src/examples/
^/usr/share/doc/
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreq <<EOF
# global list of script capabilities (regexps) not to be used in Requires
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreqdep <<EOF
# global list of capabilities (SONAME, perl(module), php(module) regexps)
# which don't generate dependencies on package NAMES
# -- OpenGL implementation
^libGL.so.1
^libGLU.so.1
^libOSMesa.so
# -- Glide
^libglide3.so.3
# -- mozilla
^libgtkmozembed.so
^libgtksuperwin.so
^libxpcom.so
# -- X11 implementation
^libFS.so
^libI810XvMC.so
^libICE.so
^libSM.so
^libX11.so
^libXRes.so
^libXTrap.so
^libXaw.so
^libXcomposite.so
^libXcursor.so
^libXdamage.so
^libXdmcp.so
^libXevie.so
^libXext.so
^libXfixes.so
^libXfont.so
^libXfontcache.so
^libXft.so
^libXi.so
^libXinerama.so
^libXmu.so
^libXmuu.so
^libXp.so
^libXpm.so
^libXrandr.so
^libXrender.so
^libXss.so
^libXt.so
^libXtst.so
^libXv.so
^libXvMC.so
^libXxf86dga.so
^libXxf86misc.so
^libXxf86rush.so
^libXxf86vm.so
^libdps.so
^libdpstk.so
^libfontenc.so
^libpsres.so
^libxkbfile.so
^libxkbui.so
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautocompressdoc <<EOF
# global list of file masks not to be compressed in DOCDIR
EOF

# for rpm -e|-U --repackage
install -d $RPM_BUILD_ROOT/var/{spool/repackage,lock/rpm}
touch $RPM_BUILD_ROOT/var/lock/rpm/transaction

# move libs to /lib
for a in librpm-%{sover}.so librpmdb-%{sover}.so librpmio-%{sover}.so ; do
	mv -f $RPM_BUILD_ROOT%{_libdir}/$a $RPM_BUILD_ROOT/%{_lib}
	ln -s /%{_lib}/$a $RPM_BUILD_ROOT%{_libdir}/$a
done

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

for f in $RPM_BUILD_ROOT%{_datadir}/locale/{en_RN,eu_ES,gl,hu,ro,wa,zh,zh_CN.GB2312}/LC_MESSAGES/rpm.mo ; do
	[ "`file $f | sed -e 's/.*,//' -e 's/message.*//'`" -le 1 ] && rm -f $f
done
%find_lang %{name}

rm -rf manual
cp -a doc/manual manual
rm -f manual/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post	lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%pre build
find %{_rpmlibdir} -name '*-linux' -type l | xargs rm -f

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc RPM-PGP-KEY CHANGES manual

%attr(755,root,root) /bin/rpm
#%attr(755,root,root) %{_bindir}/rpmdb
#%attr(755,root,root) %{_bindir}/rpmquery
#%attr(755,root,root) %{_bindir}/rpmsign
#%attr(755,root,root) %{_bindir}/rpmverify

%dir %{_sysconfdir}/rpm
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/rpm/macros
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rpm

%{_mandir}/man8/rpm.8*
%lang(fr) %{_mandir}/fr/man8/rpm.8*
%lang(ja) %{_mandir}/ja/man8/rpm.8*
%lang(ko) %{_mandir}/ko/man8/rpm.8*
%lang(pl) %{_mandir}/pl/man8/rpm.8*
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%lang(sk) %{_mandir}/sk/man8/rpm.8*

%dir /var/lib/rpm
%dir %attr(700,root,root) /var/spool/repackage
%dir /var/lock/rpm
/var/lock/rpm/transaction

%dir %{_rpmlibdir}
#%attr(755,root,root) %{_rpmlibdir}/rpmd
#%{!?with_static:%attr(755,root,root) %{_rpmlibdir}/rpm[eiu]}
#%attr(755,root,root) %{_rpmlibdir}/rpmk
#%attr(755,root,root) %{_rpmlibdir}/rpm[qv]

%doc %attr(755,root,root) %{_rpmlibdir}/convertrpmrc.sh
%attr(755,root,root) %{_rpmlibdir}/user_group.sh

%attr(755,root,root) %{_bindir}/banner.sh

%{_rpmlibdir}/rpmrc
%{_rpmlibdir}/rpmpopt*
%{_rpmlibdir}/macros

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/librpm*-*.so
%attr(755,root,root) %{_libdir}/librpm*-*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/rpm
%{_libdir}/librpm*.la
%attr(755,root,root) %{_libdir}/librpm.so
%attr(755,root,root) %{_libdir}/librpm-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmio.so
%attr(755,root,root) %{_libdir}/librpmio-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmdb.so
%attr(755,root,root) %{_libdir}/librpmdb-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmbuild.so

%files static
%defattr(644,root,root,755)
%{_libdir}/librpm*.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/debugedit
%attr(755,root,root) %{_bindir}/rpm2cpio
%attr(755,root,root) %{_bindir}/rpmcache
%attr(755,root,root) %{_bindir}/rpmdeps
%attr(755,root,root) %{_bindir}/rpmgraph
%attr(755,root,root) %{_bindir}/rpmfile
%attr(755,root,root) %{_rpmlibdir}/find-debuginfo.sh
%attr(755,root,root) %{_rpmlibdir}/rpm2cpio.sh
%attr(755,root,root) %{_rpmlibdir}/tgpg
%attr(755,root,root) %{_rpmlibdir}/rpmdb_loadcvt
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmcache.8*
%{_mandir}/man8/rpmgraph.8*
%lang(ja) %{_mandir}/ja/man8/rpm2cpio.8*
%lang(ja) %{_mandir}/ja/man8/rpmcache.8*
%lang(ja) %{_mandir}/ja/man8/rpmgraph.8*
%lang(ko) %{_mandir}/ko/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpmdeps.8*
%lang(pl) %{_mandir}/pl/man8/rpmcache.8*
%lang(pl) %{_mandir}/pl/man8/rpmgraph.8*
%lang(ru) %{_mandir}/ru/man8/rpm2cpio.8*

%files utils-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/rpmdiff*
# not here
#%%{_rpmlibdir}/rpm.daily
#%%{_rpmlibdir}/rpm.log
#%%{_rpmlibdir}/rpm.xinetd

%if %{with static}
%files utils-static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpm[ieu]
%attr(755,root,root) %{_rpmlibdir}/rpm[ieu]
%endif

%files build
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/rpm/noauto*
%attr(755,root,root) %{_rpmlibdir}/compress-doc
%attr(755,root,root) %{_rpmlibdir}/cross-build
#%attr(755,root,root) %{_rpmlibdir}/find-provides
#%attr(755,root,root) %{_rpmlibdir}/find-provides-wrapper
#%attr(755,root,root) %{_rpmlibdir}/find-requires
#%attr(755,root,root) %{_rpmlibdir}/find-requires-wrapper
#%attr(755,root,root) %{_rpmlibdir}/find-rpm-provides
%attr(755,root,root) %{_rpmlibdir}/find-spec-bcond
%attr(755,root,root) %{_rpmlibdir}/find-lang.sh
%attr(755,root,root) %{_rpmlibdir}/mkinstalldirs
%attr(755,root,root) %{_rpmlibdir}/config.*
%attr(755,root,root) %{_rpmlibdir}/getpo.sh
%attr(755,root,root) %{_rpmlibdir}/install-build-tree
%attr(755,root,root) %{_rpmlibdir}/brp-*
%attr(755,root,root) %{_rpmlibdir}/check-files
%attr(755,root,root) %{_rpmlibdir}/check-prereqs
#%attr(755,root,root) %{_rpmlibdir}/cpanflute
#%attr(755,root,root) %{_rpmlibdir}/cpanflute2
#%attr(755,root,root) %{_rpmlibdir}/Specfile.pm
%attr(755,root,root) %{_rpmlibdir}/u_pkg.sh
#%attr(755,root,root) %{_rpmlibdir}/vpkg-provides.sh
#%attr(755,root,root) %{_rpmlibdir}/vpkg-provides2.sh
%attr(755,root,root) %{_rpmlibdir}/rpmb
%attr(755,root,root) %{_rpmlibdir}/rpmt
%{_rpmlibdir}/noarch-*
%ifarch %{ix86}
%{_rpmlibdir}/i?86*
%{_rpmlibdir}/pentium*
%{_rpmlibdir}/athlon*
%endif
%ifarch alpha
%{_rpmlibdir}/alpha*
%endif
%ifarch ia64
%{_rpmlibdir}/ia64*
%endif
%ifarch mips mipsel mips64 mips64el
%{_rpmlibdir}/mips*
%endif
%ifarch ppc
%{_rpmlibdir}/ppc*
%endif
%ifarch sparc sparc64
%{_rpmlibdir}/sparc*
%endif
%ifarch %{x8664}
%{_rpmlibdir}/x86_64*
%endif
# must be here for "Requires: rpm-*prov" to work
%{_rpmlibdir}/macros.perl
%{_rpmlibdir}/macros.php
# not used yet ... these six depend on perl
#%attr(755,root,root) %{_rpmlibdir}/http.req
#%attr(755,root,root) %{_rpmlibdir}/magic.prov
#%attr(755,root,root) %{_rpmlibdir}/magic.req
#%{_rpmlibdir}/sql.prov
#%{_rpmlibdir}/sql.req
#%{_rpmlibdir}/tcl.req
%{_rpmlibdir}/trpm

%attr(755,root,root) %{_bindir}/javadeps
%attr(755,root,root) %{_bindir}/gendiff
%attr(755,root,root) %{_bindir}/rpmbuild

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%lang(ja) %{_mandir}/ja/man8/rpmbuild.8*
%lang(pl) %{_mandir}/pl/man1/gendiff.1*
%lang(pl) %{_mandir}/pl/man8/rpmbuild.8*

%files build-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/builder
%attr(755,root,root) %{_bindir}/adapter.awk
%attr(755,root,root) %{_bindir}/pldnotify.awk

%files perlprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/perl.*
#%attr(755,root,root) %{_rpmlibdir}/perldeps.pl
#%attr(755,root,root) %{_rpmlibdir}/find-perl-*
#%attr(755,root,root) %{_rpmlibdir}/find-*.perl
#%attr(755,root,root) %{_rpmlibdir}/find-prov.pl
#%attr(755,root,root) %{_rpmlibdir}/find-req.pl
%attr(755,root,root) %{_rpmlibdir}/get_magic.pl

%files pythonprov
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.python
%attr(755,root,root) %{_rpmlibdir}/pythondeps.sh

%files php-pearprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/php*
%attr(755,root,root) %{_rpmlibdir}/find-php*

%if %{with python}
%files -n python-rpm
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%attr(755,root,root) %{py_sitedir}/rpm/*.so
%attr(755,root,root) %{py_sitedir}/rpm/*.py[co]
%attr(755,root,root) %{py_sitedir}/rpmdb/*.so
%{py_sitedir}/rpmdb/*.py*
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs
%endif
