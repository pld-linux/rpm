#
# TODO:
# - learn find-perl-provides to use the __perl macro instead
#   of /usr/bin/perl
#
# Conditional build:
# _without_static	- build shared /bin/rpm (doesn't work at the moment)
# force_cc		- force using __cc other than "%{_target_cpu}-pld-linux-gcc"
# force_cxx		- force using __cxx other than "%{_target_cpu}-pld-linux-g++"
# force_cpp		- force using __cpp other than "%{_target_cpu}-pld-linux-gcc -E"
#
%include        /usr/lib/rpm/macros.python
%define	beecrypt_ver	2.2.0
# versions of required libraries
%define	reqdb_ver	4.1.25-1
%define	reqpopt_ver	1.7
Summary:	RPM Package Manager
Summary(de):	RPM Packet-Manager
Summary(es):	Gestor de paquetes RPM
Summary(pl):	Aplikacja do zarz±dzania pakietami RPM
Summary(pt_BR):	Gerenciador de pacotes RPM
Summary(ru):	íÅÎÅÄÖÅÒ ÐÁËÅÔÏ× ÏÔ RPM
Summary(uk):	íÅÎÅÄÖÅÒ ÐÁËÅÔ¦× ×¦Ä RPM
Name:		rpm
Version:	4.1
Release:	15.1
%define	beecrypt_rel	%{version}.%{release}
License:	GPL
Group:		Base
Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.1.x/%{name}-%{version}.tar.gz
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
Source12:	%{name}-macros.php
Source13:	%{name}-macros.python
Source14:	%{name}-groups-po.awk
Source15:	%{name}-compress-doc
Source16:	%{name}-check-files
Source17:	%{name}-php-provides
Source18:	%{name}-php-requires
Source19:	%{name}-find-php-provides
Source20:	%{name}-find-php-requires
Source30:	builder
Source31:	adapter.awk
Source32:	pldnotify.awk
Source33:	perl.prov
Patch0:		%{name}-pl.po.patch
Patch1:		%{name}-%{name}rc.patch
Patch2:		%{name}-arch.patch
Patch3:		%{name}-%{name}popt.patch
Patch4:		%{name}-perl-macros.patch
Patch5:		%{name}-perl-req-perlfile.patch
Patch6:		%{name}-cache.patch
Patch7:		%{name}-glob.patch
Patch8:		%{name}-header_h.patch
Patch9:		%{name}-fast-alAddPackage.patch
Patch10:	%{name}-byKey.patch
Patch11:	%{name}-noexpand.patch
Patch12:	%{name}-scripts-closefds.patch
Patch13:	%{name}-python-macros.patch
Patch14:	%{name}-perlprov-regonly.patch
Patch15:	%{name}-4.1-branch.patch
Patch16:	%{name}-drop-legacy-CLI.patch
Patch18:	%{name}-gettext-in-header.patch
Patch19:	%{name}-compress-doc.patch
Patch20:	%{name}-lt14d.patch
Patch21:	%{name}-gettext0.11.patch
Patch22:	%{name}-build.patch
Patch23:	%{name}-python-link.patch
Patch24:	%{name}-system_libs.patch
Patch25:	%{name}-bb-and-short-circuit.patch
Patch26:	%{name}-4.1-branch-po-updates.patch
Patch27:	%{name}-link.patch
Patch28:	%{name}-beecrypt-opt.patch
Patch29:	%{name}-python-pic.patch
Patch30:	%{name}-home_etc.patch
URL:		http://www.rpm.org/
Icon:		rpm.gif
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bzip2-devel >= 1.0.1
BuildRequires:	db-devel >= %{reqdb_ver}
BuildRequires:	doxygen
BuildRequires:	gettext-devel >= 0.11.4-2
BuildRequires:	libelf-devel
BuildRequires:	libtool
BuildRequires:	patch >= 2.2
BuildRequires:	python-devel >= 2.2
BuildRequires:	python-modules >= 2.2
BuildRequires:	rpm-pythonprov
BuildRequires:	zlib-devel
BuildRequires:	popt-devel >= %{reqpopt_ver}
%if %{!?_without_static:1}%{?_without_static:0}
# Require static library only for static build
BuildRequires:	bzip2-static >= 1.0.2-5
BuildRequires:	db-static >= %{reqdb_ver}
BuildRequires:	glibc-static >= 2.2.94
BuildRequires:	libelf-static
BuildRequires:	zlib-static
BuildRequires:	popt-static >= %{reqpopt_ver}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	glibc < 2.2.92

%define		__find_provides	%{SOURCE4}
%define		_binary_payload	w9.gzdio

# don't require very fresh rpm.macros to build
%define		__gettextize gettextize --copy --force --intl ; cp -f po/Makevars{.template,}

# stabilize new build environment
%define		__cc %{?force_cc}%{!?force_cc:%{_target_cpu}-pld-linux-gcc}
%define		__cxx %{?force_cxx}%{!?force_cxx:%{_target_cpu}-pld-linux-g++}
%define		__cpp %{?force_cpp}%{!?force_cpp:%{_target_cpu}-pld-linux-gcc -E}

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

%package devel
Summary:	Header files and libraries
Summary(de):	Header-Dateien uns Libraries
Summary(es):	Archivos de inclusión y bibliotecas para programas de manipulación de paquetes rpm
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne
Summary(pt_BR):	Arquivos de inclusão e bibliotecas para programas de manipulação de pacotes RPM
Summary(ru):	èÅÄÅÒÙ É ÂÉÂÌÉÏÔÅËÉ ÄÌÑ ÐÒÏÇÒÁÍÍ, ÒÁÂÏÔÁÀÝÉÈ Ó rpm-ÐÁËÅÔÁÍÉ
Summary(uk):	èÅÄÅÒÉ ÔÁ Â¦ÂÌ¦ÏÔÅËÉ ÄÌÑ ÐÒÏÇÒÁÍ, ÝÏ ÐÒÁÃÀÀÔØ Ú ÐÁËÅÔÁÍÉ rpm
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	bzip2-devel
Requires:	db-devel
Requires:	libelf-devel
Requires:	popt-devel >= 1.7
Requires:	zlib-devel

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
graficznych programów zarz±dzaj±cych pakietami oraz innych narzêdzi,
które wymagaj± szczegó³owej wiedzy na temat pakietów RPM.

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
Requires:	%{name}-devel = %{version}
Requires:	bzip2-static
Requires:	db-static
Requires:	libelf-static
Requires:	popt-static >= 1.7
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
Requires:	%{name} = %{version}
Requires:	popt >= 1.7

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
Requires:	%{name} = %{version}
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
Requires:	%{name} = %{version}
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
Requires:	%{name} = %{version}

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
Python para manipular pacotes e bancos de dados RPM.

%package lib
Summary:	RPMs library
Summary(pl):	Biblioteki RPM-a
Group:		Libraries
Requires:	db >= %{reqdb_ver}
Requires:	popt >= %{reqpopt_ver}

%description lib
RPMs library.

%description lib -l pl
Biblioteki RPM-a.

%package build
Summary:	Scripts for building binary RPM packages
Summary(de):	Scripts fürs Bauen binärer RPM-Pakete
Summary(pl):	Skrypty pomocnicze do budowania binarnych RPM-ów
Summary(pt_BR):	Scripts e programas executáveis usados para construir pacotes
Summary(ru):	óËÒÉÐÔÙ É ÕÔÉÌÉÔÙ, ÎÅÏÂÈÏÄÉÍÙÅ ÄÌÑ ÓÂÏÒËÉ ÐÁËÅÔÏ×
Summary(uk):	óËÒÉÐÔÉ ÔÁ ÕÔÉÌ¦ÔÉ, ÎÅÏÂÈ¦ÄÎ¦ ÄÌÑ ÐÏÂÕÄÏ×É ÐÁËÅÔ¦×
Group:		Applications/File
Requires(pre):	findutils
Requires:	%{name} = %{version}
Requires:	/bin/id
Requires:	awk
Requires:	binutils
Requires:	diffutils
Requires:	file >= 3.31
Requires:	fileutils
Requires:	findutils
%ifarch athlon
Requires:	gcc >= 3.0.3
%else
Requires:	gcc
%endif
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
Requires:	%{name}-build = %{version}
# these are optional
#Requires:	cvs
#Requires:	wget

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

%package -n beecrypt
Summary:	Crypto library
Summary(pl):	Biblioteka kryptograficzna
Version:	%{beecrypt_ver}
Release:	%{beecrypt_rel}
Epoch:		1
Group:		Libraries

%description -n beecrypt
Crypto library (modified for rpm needs).

%description -n beecrypt -l pl
Biblioteka kryptograficzna (zmodyfikowana na potrzeby rpma).

%package -n beecrypt-devel
Summary:	Crypto library - development files
Summary(pl):	Biblioteka kryptograficzna - pliki developerskie
Version:	%{beecrypt_ver}
Release:	%{beecrypt_rel}
Epoch:		1
Group:		Development/Libraries
Requires:	beecrypt = %{beecrypt_ver}

%description -n beecrypt-devel
Crypto library - development files.

%description -n beecrypt-devel -l pl
Biblioteka kryptograficzna - pliki developerskie.

%package -n beecrypt-static
Summary:	Crypto library - static version
Summary(pl):	Statyczna biblioteka kryptograficzna
Version:	%{beecrypt_ver}
Release:	%{beecrypt_rel}
Epoch:		1
Group:		Development/Libraries
Requires:	beecrypt-devel = %{beecrypt_ver}

%description -n beecrypt-static
Static version of crypto library.

%description -n beecrypt-static -l pl
Statyczna wersja biblioteki kryptograficznej.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
# not needed ? (break compilation)
#%patch6 -p1
%patch7 -p1
# needed ?
#%patch8 -p1
# rejected (needed ?)
#%patch9 -p1
# too many rejects, Pawel please check if needed and rediff
#%patch10 -p0
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch18 -p1
%patch19 -p1
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

sed -e 's/^/@pld@/' %{SOURCE2} >>platform.in
cp -f platform.in macros.pld.in
install %{SOURCE5} macros.perl.in
install %{SOURCE13} macros.python.in
install %{SOURCE12} macros.php.in
install %{SOURCE6} scripts/find-perl-provides
install %{SOURCE7} scripts/find-perl-requires
install %{SOURCE9} scripts/find-lang.sh
install %{SOURCE17} scripts/php.prov.in
install %{SOURCE18} scripts/php.req.in
install %{SOURCE19} scripts/find-php-provides
install %{SOURCE20} scripts/find-php-requires
install %{SOURCE33} scripts/perl.prov

cd scripts;
mv -f perl.req perl.req.in
mv -f perl.prov perl.prov.in
cd ..

chmod +x %{SOURCE4}
rm -rf zlib libelf db db3 popt rpmdb/db.h

%build
# generate Group translations to *.po
awk -f %{SOURCE14} %{SOURCE1}

%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd beecrypt
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd ..

rm -f missing
%{__libtoolize}
%{__gettextize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

# config.guess doesn't handle athlon, so we have to change it by hand.
# rpm checks for CPU type at runtime, but it looks better
sed -e 's|@host@|%{_target_cpu}-%{_target_vendor}-linux-gnu|'  \
	-e 's|@host_cpu@|%{_target_cpu}|'  macros.in  > macros.tmp
mv -f macros.tmp macros.in

# pass CC and CXX too in case of building with some older configure macro
%configure \
	CC="%{__cc}" CXX="%{__cxx}" CPP="%{__cpp}" \
	--enable-shared \
	--enable-static \
	--with-apidocs \
	--with-python=auto \
	--without-db

%{__make} \
	%{?_without_static:rpm_LDFLAGS="\$(myLDFLAGS)"} \
	myLDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgbindir="%{_bindir}"

install macros.perl	$RPM_BUILD_ROOT%{_libdir}/rpm/macros.perl
install macros.python	$RPM_BUILD_ROOT%{_libdir}/rpm/macros.python
install macros.php	$RPM_BUILD_ROOT%{_libdir}/rpm/macros.php

install %{SOURCE1} doc/manual/groups
install %{SOURCE3} $RPM_BUILD_ROOT%{_libdir}/rpm/install-build-tree
install %{SOURCE4} $RPM_BUILD_ROOT%{_libdir}/rpm/find-rpm-provides
install %{SOURCE8} $RPM_BUILD_ROOT%{_libdir}/rpm/find-spec-bcond
install %{SOURCE10} $RPM_BUILD_ROOT%{_libdir}/rpm/find-provides
install %{SOURCE11} $RPM_BUILD_ROOT%{_libdir}/rpm/find-requires
install %{SOURCE15} $RPM_BUILD_ROOT%{_libdir}/rpm/compress-doc
install %{SOURCE16} $RPM_BUILD_ROOT%{_libdir}/rpm/check-files
install scripts/find-php*	$RPM_BUILD_ROOT%{_libdir}/rpm/
install scripts/php.{prov,req}	$RPM_BUILD_ROOT%{_libdir}/rpm/

install %{SOURCE30} $RPM_BUILD_ROOT%{_bindir}/builder
install %{SOURCE31} $RPM_BUILD_ROOT%{_bindir}/adapter.awk
install %{SOURCE32} $RPM_BUILD_ROOT%{_bindir}/pldnotify.awk

install rpmio/ugid.h $RPM_BUILD_ROOT%{_includedir}/rpm

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros <<EOF
# customized rpm macros - global for host
#
#%%_install_langs pl_PL:en_US
%%distribution PLD
EOF

# for rpm -e|-U --repackage
install -d $RPM_BUILD_ROOT/var/spool/repackage

%find_lang %{name}

rm -f doc/manual/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post	lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig
%post   -n beecrypt -p /sbin/ldconfig
%postun -n beecrypt -p /sbin/ldconfig

%pre build
find /usr/lib/rpm -name '*-linux' -type l | xargs rm -f

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc RPM-PGP-KEY CHANGES doc/manual/*

%attr(755,root,root) /bin/rpm

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
%dir %attr(700,root,root) /var/spool/repackage
%dir %{_libdir}/rpm

%doc %attr(755,root,root) %{_libdir}/rpm/convertrpmrc.sh

%{_libdir}/rpm/rpmrc
%{_libdir}/rpm/rpmpopt*
%{_libdir}/rpm/macros

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librpm*-*.so

%files build
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm/compress-doc
%attr(755,root,root) %{_libdir}/rpm/cross-build
%attr(755,root,root) %{_libdir}/rpm/find-requires
%attr(755,root,root) %{_libdir}/rpm/find-provides
%attr(755,root,root) %{_libdir}/rpm/find-rpm-provides
%attr(755,root,root) %{_libdir}/rpm/find-spec-bcond
%attr(755,root,root) %{_libdir}/rpm/find-lang.sh
%attr(755,root,root) %{_libdir}/rpm/mkinstalldirs
%attr(755,root,root) %{_libdir}/rpm/config.*
%attr(755,root,root) %{_libdir}/rpm/getpo.sh
%attr(755,root,root) %{_libdir}/rpm/install-build-tree
%attr(755,root,root) %{_libdir}/rpm/brp-*
%attr(755,root,root) %{_libdir}/rpm/check-files
%attr(755,root,root) %{_libdir}/rpm/check-prereqs
%attr(755,root,root) %{_libdir}/rpm/cpanflute
%attr(755,root,root) %{_libdir}/rpm/cpanflute2
%attr(755,root,root) %{_libdir}/rpm/Specfile.pm
%attr(755,root,root) %{_libdir}/rpm/http.req
%attr(755,root,root) %{_libdir}/rpm/magic.*
%attr(755,root,root) %{_libdir}/rpm/u_pkg.sh
%attr(755,root,root) %{_libdir}/rpm/vpkg-provides.sh
%attr(755,root,root) %{_libdir}/rpm/vpkg-provides2.sh
%attr(755,root,root) %{_libdir}/rpm/rpmb
%attr(755,root,root) %{_libdir}/rpm/rpmt
%{_libdir}/rpm/noarch-*
%ifarch i386 i486 i586 i686 athlon
%{_libdir}/rpm/i?86*
%{_libdir}/rpm/athlon*
%endif
%ifarch sparc sparc64
%{_libdir}/rpm/sparc*
%endif
%ifarch alpha
%{_libdir}/rpm/alpha*
%endif
%ifarch ppc
%{_libdir}/rpm/ppc*
%endif
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

%files devel
%defattr(644,root,root,755)
%{_includedir}/rpm
%{_libdir}/librpm.la
%attr(755,root,root) %{_libdir}/librpm.so
%{_libdir}/librpmio.la
%attr(755,root,root) %{_libdir}/librpmio.so
%{_libdir}/librpmdb.la
%attr(755,root,root) %{_libdir}/librpmdb.so
%{_libdir}/librpmbuild.la
%attr(755,root,root) %{_libdir}/librpmbuild.so

%files static
%defattr(644,root,root,755)
%{_libdir}/librpm*.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpm2cpio
%attr(755,root,root) %{_libdir}/rpm/rpmdiff*
%attr(755,root,root) %{_libdir}/rpm/tgpg
%attr(755,root,root) %{_libdir}/rpm/find-debuginfo.sh
%attr(755,root,root) %{_bindir}/rpmgraph
%attr(755,root,root) %{_bindir}/rpmcache
%attr(755,root,root) %{_bindir}/striptofile
%attr(755,root,root) %{_bindir}/unstripfile
# not here
#%%{_libdir}/rpm/rpm.daily
#%%{_libdir}/rpm/rpm.log
#%%{_libdir}/rpm/rpm.xinetd
%{_libdir}/rpm/rpm2cpio.sh

%{_mandir}/man8/rpm2cpio.8*
%lang(ja) %{_mandir}/ja/man8/rpm2cpio.8*
%lang(ko) %{_mandir}/ko/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpm2cpio.8*
%lang(ru) %{_mandir}/ru/man8/rpm2cpio.8*
%{_mandir}/man8/rpmcache.8*
%{_mandir}/man8/rpmgraph.8*

%files perlprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm/perl*
%attr(755,root,root) %{_libdir}/rpm/find-perl-*
%attr(755,root,root) %{_libdir}/rpm/find-*.perl
%attr(755,root,root) %{_libdir}/rpm/find-prov.pl
%attr(755,root,root) %{_libdir}/rpm/find-req.pl
%attr(755,root,root) %{_libdir}/rpm/get_magic.pl

%{_libdir}/rpm/macros.perl

%files pythonprov
%defattr(644,root,root,755)
%{_libdir}/rpm/macros.python

%files php-pearprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm/php*
%attr(755,root,root) %{_libdir}/rpm/find-php*
%{_libdir}/rpm/macros.php

%files -n python-rpm
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%attr(755,root,root) %{py_sitedir}/rpmdb/*.so
%{py_sitedir}/rpmdb/*.py*

%files build-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/builder
%attr(755,root,root) %{_bindir}/adapter.awk
%attr(755,root,root) %{_bindir}/pldnotify.awk

%files -n beecrypt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbeecrypt.so.*.*

%files -n beecrypt-devel
%defattr(644,root,root,755)
%{_libdir}/libbeecrypt.so
%{_libdir}/libbeecrypt.la
%{_includedir}/beecrypt

%files -n beecrypt-static
%defattr(644,root,root,755)
%{_libdir}/libbeecrypt.a
