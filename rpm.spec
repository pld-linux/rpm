#
# TODO:
# - check if we want shell autodeps: Requires: executable(ln) executable(mv)
# - %{_arch} = i686 not as used to be i386:
#   5.0.2: rpm -E '%_target_base_arch %_arch'
#          i386 i686
#   4.4.9: rpm -E '%_target_base_arch %_arch'
#          i386 i386
# - python(abi) cap is not provided automatically because /usr/lib*/libpython2*.so.*
#   matches ELF first
# - TODO: add macros for some ppc, mipsel, alpha and sparc
# - uppackaged list:
#   /usr/lib/rpm/http.req
#   /usr/lib/rpm/install-sh
#   /usr/lib/rpm/mono-find-provides
#   /usr/lib/rpm/mono-find-requires
#   /usr/lib/rpm/osgideps.pl
#   /usr/lib/rpm/perldeps.pl
#   /usr/lib/rpm/vcheck
#   /usr/share/man/man8/rpmconstant.8
#
# - headerGet() making poldek segfault http://rpm5.org/cvs/tktview?tn=38,1
# - LUA segfault - http://rpm5.org/cvs/tktview?tn=39,1
# - rpm doesn't exit when no sources/patches available http://rpm5.org/cvs/tktview?tn=40,1
#
# Conditional build:
%bcond_with	static		# build static rpm+rpmi
%bcond_with	apidocs		# don't generate documentation with doxygen
%bcond_with	autoreqdep	# autogenerate package name deps in addition to sonames/perl(X)
%bcond_without	python		# don't build python bindings
%bcond_without	selinux		# build without selinux support
%bcond_without	suggest_tags	# build without Suggest tag (bootstrapping)
%bcond_with	neon		# build with HTTP/WebDAV support (neon library)
%bcond_without	db		# BerkeleyDB
%bcond_with	sqlite		# build with SQLite support
%bcond_with	sqlite_dbapi	# default database backend is sqlite
%bcond_without	system_lua		# use system lua
# force_cc		- force using __cc other than "%{_target_cpu}-pld-linux-gcc"
# force_cxx		- force using __cxx other than "%{_target_cpu}-pld-linux-g++"
# force_cpp		- force using __cpp other than "%{_target_cpu}-pld-linux-gcc -E"
#
%if %{with sqlite_dbapi}
%define	with_sqlite	1
%endif

%if %{without db} && %{without sqlite}
%{error:Need db or sqlite}
ERROR
%endif

# versions of required libraries
%define		reqdb_ver	4.7.25
%define		reqpopt_ver	1.10.8
%define		beecrypt_ver	2:4.1.2-4
%define		sover	5.0

Summary:	RPM Package Manager
Summary(de.UTF-8):	RPM Packet-Manager
Summary(es.UTF-8):	Gestor de paquetes RPM
Summary(pl.UTF-8):	Aplikacja do zarządzania pakietami RPM
Summary(pt_BR.UTF-8):	Gerenciador de pacotes RPM
Summary(ru.UTF-8):	Менеджер пакетов от RPM
Summary(uk.UTF-8):	Менеджер пакетів від RPM
Name:		rpm
Version:	5.1.4
Release:	0.7
License:	LGPL
Group:		Base
Source0:	http://rpm5.org/files/rpm/rpm-5.1/%{name}-%{version}.tar.gz
# Source0-md5:	9a04c22ce1dffc81a7e43d39b002aaa1
Source1:	%{name}.groups
Source2:	%{name}.platform
Source3:	%{name}-install-tree
Source4:	%{name}-find-spec-bcond
Source5:	%{name}-hrmib-cache
Source6:	%{name}-groups-po.awk
Source7:	%{name}-compress-doc
Source8:	%{name}-check-files
Source9:	%{name}-php-provides
Source10:	%{name}-php-requires
Source11:	%{name}.sysinfo
Source12:	perl.prov
Source13:	%{name}-user_group.sh
Source14:	%{name}.sysconfig
Source15:	%{name}-macros.java
Source16:	%{name}-java-requires
# http://svn.pld-linux.org/banner.sh/
Source17:	banner.sh
Source18:	%{name}-pld.macros
Source19:	ftp://ftp.pld-linux.org/dists/th/PLD-3.0-Th-GPG-key.asc
# Source19-md5:  08b29584dd349aac9caa7610131a0a88
Source20:	%{name}-mimetypedeps
Source100:	%{name}-macros-athlon
Source101:	%{name}-macros-i386
Source102:	%{name}-macros-i486
Source103:	%{name}-macros-i586
Source104:	%{name}-macros-i686
Source105:	%{name}-macros-noarch
Source106:	%{name}-macros-pentium3
Source107:	%{name}-macros-pentium4
Source108:	%{name}-macros-ppc
Source109:	%{name}-macros-x86_64
Source110:	%{name}-macros-ia32e
Source111:	%{name}-macros-amd64

Patch0:		%{name}-branch.patch
Patch1:		%{name}-man_pl.patch
Patch2:		%{name}-popt-aliases.patch
Patch3:		%{name}-rpmpopt.patch
Patch4:		%{name}-perl-macros.patch
Patch5:		%{name}-perl-req-perlfile.patch
Patch6:		%{name}-noexpand.patch
Patch7:		%{name}-scripts-closefds.patch
Patch8:		%{name}-php-macros.patch
Patch9:		%{name}-gettext-in-header.patch
Patch10:	%{name}-compress-doc.patch
Patch11:	%{name}-lua.patch

Patch14:	%{name}-etc_dir.patch
Patch16:	%{name}-php-deps.patch
Patch17:	%{name}-macros.patch
Patch18:	%{name}-macros-th.patch
Patch19:	%{name}-glob.patch

Patch23:	%{name}-pkgconfigdeps.patch

Patch26:	%{name}-notsc.patch
Patch27:	%{name}-hack-norpmlibdep.patch

Patch32:	%{name}-pld-autodep.patch
Patch34:	%{name}-epoch0.patch
Patch35:	%{name}-perl_req-INC_dirs.patch
Patch36:	%{name}-debuginfo.patch
Patch37:	%{name}-doxygen_hack.patch

Patch42:	%{name}-old-fileconflicts-behaviour.patch

Patch46:	%{name}-mono.patch
Patch47:	%{name}-javadeps.patch

Patch52:	%{name}-morearchs.patch

Patch55:	%{name}-truncate-cvslog.patch

Patch59:	%{name}-libtool-deps.patch
Patch60:	%{name}-mimetype.patch
Patch61:	%{name}-sparc64.patch
URL:		http://rpm5.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1.4
BuildRequires:	beecrypt-devel >= %{beecrypt_ver}
BuildRequires:	bzip2-devel >= 1.0.2-17
%{?with_db:BuildRequires:	db-devel >= %{reqdb_ver}}
BuildRequires:	elfutils-devel >= 0.108
BuildRequires:	gettext-autopoint >= 0.11.4-2
BuildRequires:	gettext-devel >= 0.11.4-2
BuildRequires:	lzma-devel >= 4.999.3
BuildRequires:	libmagic-devel
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.18}
# needed only for AM_PROG_CXX used for CXX substitution in rpm.macros
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
%if %{with neon}
BuildRequires:	libxml2-devel
BuildRequires:	neon-devel >= 0.25.5
%endif
BuildRequires:	patch >= 2.2
BuildRequires:	popt-devel >= %{reqpopt_ver}
%{?with_system_lua:BuildRequires:	lua51-devel >= 5.1.2}
%{?with_python:BuildRequires:	python-devel >= 1:2.3}
BuildRequires:	python-modules >= 1:2.3
BuildRequires:	rpm-perlprov
%{?with_python:BuildRequires:	rpm-pythonprov}
%{?with_sqlite:BuildRequires:	sqlite3-devel}
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	graphviz
BuildRequires:	tetex-pdftex
%endif
%if %{with static}
# Require static library only for static build
BuildRequires:	beecrypt-static >= %{beecrypt_ver}
BuildRequires:	bzip2-static >= 1.0.2-17
%{?with_db:BuildRequires:	db-static >= %{reqdb_ver}}
BuildRequires:	elfutils-static
BuildRequires:	glibc-static >= 2.2.94
BuildRequires:	libmagic-static
%{?with_selinux:BuildRequires:	libselinux-static >= 1.18}
BuildRequires:	popt-static >= %{reqpopt_ver}
BuildRequires:	zlib-static
%endif
Requires:	%{name}-base = %{version}-%{release}
Requires:	%{name}-lib = %{version}-%{release}
Requires:	beecrypt >= %{beecrypt_ver}
Requires:	popt >= %{reqpopt_ver}
Provides:	rpm-db-ver = %{reqdb_ver}
Obsoletes:	rpm-getdeps
%{!?with_static:Obsoletes:	rpm-utils-static}
Conflicts:	glibc < 2.2.92
# db4.6 poldek needed
Conflicts:	poldek < 0.21-0.20070703.00.3
# segfaults with lzma 0.42.2
Conflicts:	lzma-libs < 4.999.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_binary_payload		w9.gzdio
%define		_noPayloadPrefix	1

# don't require very fresh rpm.macros to build
%define		__gettextize gettextize --copy --force --intl ; cp -f po/Makevars{.template,}
%define		find_lang sh ./scripts/find-lang.sh $RPM_BUILD_ROOT
%define		ix86	i386 i486 i586 i686 athlon pentium3 pentium4
%define		ppc	ppc ppc7400 ppc7450
%define		x8664	amd64 ia32e x86_64

# stabilize new build environment
%define		__newcc %{?force_cc}%{!?force_cc:%{_target_cpu}-pld-linux-gcc}
%define		__newcxx %{?force_cxx}%{!?force_cxx:%{_target_cpu}-pld-linux-g++}
%define		__newcpp %{?force_cpp}%{!?force_cpp:%{_target_cpu}-pld-linux-gcc -E}

%define		_rpmlibdir /usr/lib/rpm
%define		_noautocompressdoc	RPM-GPG-KEY

%define		specflags	-fno-strict-aliasing

%description
RPM is a powerful package manager, which can be used to build,
install, query, verify, update, and uninstall individual software
packages. A package consists of an archive of files, and package
information, including name, version, and description.

%description -l de.UTF-8
RPM ist ein kräftiger Packet-Manager, der verwendet sein kann zur
Installation, Anfrage, Verifizierung, Aktualisierung und
Uninstallation individueller Softwarepakete. Ein Paket besteht aus
einem Archiv Dateien und Paketinformation, inklusive Name, Version und
Beschreibung.

%description -l es.UTF-8
RPM es un poderoso administrador de paquetes, que puede ser usado para
construir, instalar, pesquisar, verificar, actualizar y desinstalar
paquetes individuales de software. Un paquete consiste en un
almacenaje de archivos, y información sobre el paquete, incluyendo
nombre, versión y descripción.

%description -l pl.UTF-8
RPM jest doskonałym programem zarządzającym pakietami. Umożliwia on
przebudowanie, instalację czy weryfikację dowolnego pakietu.
Informacje dotyczące każdego pakietu, takie jak jego opis, lista
plików wchodzących w skład pakietu, zależności od innych pakietów, są
przechowywane w bazie danych i można je uzyskać za pomocą opcji
odpytywania programu rpm.

%description -l pt_BR.UTF-8
RPM é um poderoso gerenciador de pacotes, que pode ser usado para
construir, instalar, pesquisar, verificar, atualizar e desinstalar
pacotes individuais de software. Um pacote consiste de um conjunto de
arquivos e informações adicionais, incluindo nome, versão e descrição
do pacote, permissões dos arquivos, etc.

%description -l ru.UTF-8
RPM - это мощный менеджер пакетов, который может быть использован для
создания, инсталляции, запросов (query), проверки, обновления и
удаления программных пакетов. Пакет состоит из файлового архива и
служебной информации, включающей название, версию, описание и другие
данные о пакете.

%description -l uk.UTF-8
RPM - це потужний менеджер пакетів, що може бути використаний для
створення, інсталяції, запитів (query), перевірки, поновлення та
видалення програмних пакетів. Пакет складається з файлового архіву та
службової інформації, що містить назву, версію, опис та іншу
інформацію про пакет.

%package base
Summary:	RPM base package - scripts used by rpm packages themselves
Summary(pl.UTF-8):	Podstawowy pakiet RPM - skrypty używane przez same pakiety rpm
Group:		Base
Requires:	filesystem
Obsoletes:	rpm-scripts
Obsoletes:	vserver-rpm

%description base
The RPM base package contains scripts used by rpm packages themselves.
These include:
- scripts for adding/removing groups and users needed for rpm
  packages,
- banner.sh to display %%banner messages from rpm scriptlets.

%description base -l pl.UTF-8
Pakiet podstawowy RPM zwiera skrypty używane przez same pakiety rpm.
Zawiera on:
- skrypty dodające/usuwające grupy i użytkowników dla pakietów rpm,
- banner.sh do pokazywania komunikatów %%banner dla skryptletów rpm.

%package lib
Summary:	RPMs library
Summary(pl.UTF-8):	Biblioteki RPM-a
Group:		Libraries
Requires:	beecrypt >= %{beecrypt_ver}
%{?with_db:Requires:	db >= %{reqdb_ver}}
Requires:	libmagic >= 1.15-2
%{?with_selinux:Requires:	libselinux >= 1.18}
Requires:	popt >= %{reqpopt_ver}
Obsoletes:	rpm-libs
# avoid SEGV caused by mixed db versions
Conflicts:	poldek < 0.18.1-16

%description lib
RPMs library.

%description lib -l pl.UTF-8
Biblioteki RPM-a.

%package devel
Summary:	Header files for rpm libraries
Summary(de.UTF-8):	Header-Dateien für rpm Libraries
Summary(es.UTF-8):	Archivos de inclusión y bibliotecas para programas de manipulación de paquetes rpm
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek rpm
Summary(pt_BR.UTF-8):	Arquivos de inclusão e bibliotecas para programas de manipulação de pacotes RPM
Summary(ru.UTF-8):	Хедеры и библиотеки для программ, работающих с rpm-пакетами
Summary(uk.UTF-8):	Хедери та бібліотеки для програм, що працюють з пакетами rpm
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}
Requires:	beecrypt-devel >= %{beecrypt_ver}
Requires:	bzip2-devel
%{?with_db:Requires:	db-devel >= %{reqdb_ver}}
Requires:	elfutils-devel
Requires:	libmagic-devel
%{?with_selinux:Requires:	libselinux-devel}
Requires:	popt-devel >= %{reqpopt_ver}
Requires:	zlib-devel

%description devel
The RPM packaging system includes C libraries that make it easy to
manipulate RPM packages and databases. They are intended to ease the
creation of graphical package managers and other tools that need
intimate knowledge of RPM packages. This package contains header files
for these libraries.

%description devel -l de.UTF-8
Der RPM-Packensystem enthält eine C-Library, die macht es einfach
RPM-Pakete und Dateibanken zu manipulieren. Er eignet sich für
Vereinfachung des Schaffens grafischer Paket-Manager und anderer
Werkzeuge, die intime Kenntnis von RPM-Paketen brauchen.

%description devel -l es.UTF-8
El sistema de empaquetado RPM incluye una biblioteca C que vuelve
fácil la manipulación de paquetes y bases de datos RPM. Su objetivo es
facilitar la creación de administradores gráficos de paquetes y otras
herramientas que necesiten un conocimiento profundo de paquetes RPM.

%description devel -l pl.UTF-8
System RPM zawiera biblioteki C, które ułatwiają manipulowanie
pakietami RPM oraz bazami danych. W zamiarze ma to uprościć tworzenie
graficznych programów zarządzających pakietami oraz innych narzędzi,
które wymagają szczegółowej wiedzy na temat pakietów RPM. Ten pakiet
zawiera pliki nagłówkowe wspomnianych bibliotek.

%description devel -l pt_BR.UTF-8
O sistema de empacotamento RPM inclui uma biblioteca C que torna fácil
a manipulação de pacotes e bases de dados RPM. Seu objetivo é
facilitar a criação de gerenciadores gráficos de pacotes e outras
ferramentas que precisem de conhecimento profundo de pacotes RPM.

%description devel -l ru.UTF-8
Система управления пакетами RPM содержит библиотеку C, которая
упрощает манипуляцию пакетами RPM и соответствующими базами данных.
Эта библиотека предназначена для облегчения создания графических
пакетных менеджеров и других утилит, которым необходимо работать с
пакетами RPM.

%description devel -l uk.UTF-8
Система керування пакетами RPM містить бібліотеку C, котра спрощує
роботу з пакетами RPM та відповідними базами даних. Ця бібліотека
призначена для полегшення створення графічних пакетних менеджерів та
інших утиліт, що працюють з пакетами RPM.

%package static
Summary:	RPM static libraries
Summary(de.UTF-8):	RPMs statische Libraries
Summary(pl.UTF-8):	Biblioteki statyczne RPM-a
Summary(pt_BR.UTF-8):	Bibliotecas estáticas para o desenvolvimento de aplicações RPM
Summary(ru.UTF-8):	Статическая библиотека для программ, работающих с rpm-пакетами
Summary(uk.UTF-8):	Статична бібліотека для програм, що працюють з пакетами rpm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	beecrypt-static >= %{beecrypt_ver}
Requires:	bzip2-static
%{?with_db:Requires:	db-static >= %{reqdb_ver}}
Requires:	elfutils-static
Requires:	libmagic-static
Requires:	popt-static >= %{reqpopt_ver}
Requires:	zlib-static

%description static
RPM static libraries.

%description static -l de.UTF-8
RPMs statische Libraries.

%description static -l pl.UTF-8
Biblioteki statyczne RPM-a.

%description static -l pt_BR.UTF-8
Bibliotecas estáticas para desenvolvimento.

%description static -l ru.UTF-8
Система управления пакетами RPM содержит библиотеку C, которая
упрощает манипуляцию пакетами RPM и соответствующими базами данных.
Это статическая библиотека RPM.

%description static -l uk.UTF-8
Система керування пакетами RPM містить бібліотеку C, котра спрощує
роботу з пакетами RPM та відповідними базами даних. Це статична
бібліотека RPM.

%package utils
Summary:	Additional utilities for managing RPM packages and database
Summary(de.UTF-8):	Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken
Summary(pl.UTF-8):	Dodatkowe narzędzia do zarządzania bazą RPM-a i pakietami
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	popt >= %{reqpopt_ver}
%if %{with suggest_tags}
Suggests:	bzip2
Suggests:	gzip
%endif
Conflicts:	filesystem-debuginfo < 3.0-16

%description utils
Additional utilities for managing RPM packages and database.

%description utils -l de.UTF-8
Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken.

%description utils -l pl.UTF-8
Dodatkowe narzędzia do zarządzania bazą RPM-a i pakietami.

%package utils-perl
Summary:	Additional utilities for managing RPM packages and database
Summary(de.UTF-8):	Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken
Summary(pl.UTF-8):	Dodatkowe narzędzia do zarządzania bazą RPM-a i pakietami
Group:		Applications/File
Requires:	%{name}-utils = %{version}-%{release}
Requires:	popt >= %{reqpopt_ver}

%description utils-perl
Additional utilities for managing RPM packages and database.

%description utils-perl -l de.UTF-8
Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken.

%description utils-perl -l pl.UTF-8
Dodatkowe narzędzia do zarządzania bazą RPM-a i pakietami.

%package utils-static
Summary:	Static rpm utilities
Summary(pl.UTF-8):	Statyczne narzędzia rpm
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils-static
Static rpm utilities for repairing system in case something with
shared libraries used by rpm become broken. Currently it contains rpmi
binary, which can be used to install/upgrade/remove packages without
using shared libraries (well, in fact with exception of NSS modules).

%description utils-static -l pl.UTF-8
Statyczne narzędzia rpm do naprawy systemu w przypadku zepsucia czegoś
związanego z bibliotekami współdzielonymi używanymi przez rpm-a.
Aktualnie pakiet zawiera binarkę rpmi, którą można użyć do instalacji,
uaktualniania lub usuwania pakietów bez udziału bibliotek statycznych
(z wyjątkiem modułów NSS).

%package build
Summary:	Scripts for building binary RPM packages
Summary(de.UTF-8):	Scripts fürs Bauen binärer RPM-Pakete
Summary(pl.UTF-8):	Skrypty pomocnicze do budowania binarnych RPM-ów
Summary(pt_BR.UTF-8):	Scripts e programas executáveis usados para construir pacotes
Summary(ru.UTF-8):	Скрипты и утилиты, необходимые для сборки пакетов
Summary(uk.UTF-8):	Скрипти та утиліти, необхідні для побудови пакетів
Group:		Applications/File
Requires(pre):	findutils
Requires:	%{name}-build-macros >= 1.433-2
Requires:	%{name}-utils = %{version}-%{release}
Requires:	/bin/id
Requires:	awk
Requires:	bzip2
Requires:	chrpath >= 0.10-4
Requires:	cpio
Requires:	diffutils
Requires:	elfutils
Requires:	file >= 4.17
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
Requires:	sed
Requires:	sh-utils
Requires:	tar
Requires:	textutils
Provides:	rpmbuild(monoautodeps)
Provides:	rpmbuild(noauto) = 3
%ifarch %{x8664}
Conflicts:	automake < 1:1.7.9-2
Conflicts:	libtool < 2:1.5-13
%endif

%description build
Scripts for building binary RPM packages.

%description build -l de.UTF-8
Scripts fürs Bauen binärer RPM-Pakete.

%description build -l pl.UTF-8
Skrypty pomocnicze do budowania binarnych RPM-ów.

%description build -l pt_BR.UTF-8
Este pacote contém scripts e programas executáveis que são usados para
construir pacotes usando o RPM.

%description build -l ru.UTF-8
Различные вспомогательные скрипты и исполняемые программы, которые
используются для сборки RPM'ов.

%description build -l uk.UTF-8
Різноманітні допоміжні скрипти та утиліти, які використовуються для
побудови RPM'ів.

%package javaprov
Summary:	Additional utilities for checking Java provides/requires in RPM packages
Summary(pl.UTF-8):	Dodatkowe narzędzia do sprawdzania zależności kodu w Javie w pakietach RPM
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	file
Requires:	findutils >= 1:4.2.26
Requires:	mktemp
Requires:	unzip

%description javaprov
Additional utilities for checking Java provides/requires in RPM
packages.

%description javaprov -l pl.UTF-8
Dodatkowe narzędzia do sprawdzania zależności kodu w Javie w pakietach
RPM.

%package perlprov
Summary:	Additional utilities for checking Perl provides/requires in RPM packages
Summary(de.UTF-8):	Zusatzwerkzeuge fürs Nachsehen Perl-Abhängigkeiten in RPM-Paketen
Summary(pl.UTF-8):	Dodatkowe narzędzia do sprawdzenia zależności skryptów Perla w pakietach RPM
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	perl-devel
Requires:	perl-modules

%description perlprov
Additional utilities for checking Perl provides/requires in RPM
packages.

%description perlprov -l de.UTF-8
Zusatzwerkzeuge fürs Nachsehen Perl-Abhängigkeiten in RPM-Paketen.

%description perlprov -l pl.UTF-8
Dodatkowe narzędzia do sprawdzenia zależności skryptów Perla w
pakietach RPM.

%package pythonprov
Summary:	Python macros, which simplifies creation of RPM packages with Python software
Summary(pl.UTF-8):	Makra ułatwiające tworzenie pakietów RPM z programami napisanymi w Pythonie
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	python
Requires:	python-modules

%description pythonprov
Python macros, which simplifies creation of RPM packages with Python
software.

%description pythonprov -l pl.UTF-8
Makra ułatwiające tworzenie pakietów RPM z programami napisanymi w
Pythonie.

%package php-pearprov
Summary:	Additional utilities for checking PHP PEAR provides/requires in RPM packages
Summary(pl.UTF-8):	Dodatkowe narzędzia do sprawdzania zależności skryptów php w RPM
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	sed >= 4.0

%description php-pearprov
Additional utilities for checking PHP PEAR provides/requires in RPM
packages.

%description php-pearprov -l pl.UTF-8
Dodatkowe narzędzia do sprawdzenia zależności skryptów PHP PEAR w
pakietach RPM.

%package -n python-rpm
Summary:	Python interface to RPM library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki RPM-a
Summary(pt_BR.UTF-8):	Módulo Python para aplicativos que manipulam pacotes RPM
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

%description -n python-rpm -l pl.UTF-8
Pakiet rpm-python zawiera moduł, który pozwala aplikacjom napisanym w
Pythonie na używanie interfejsu dostarczanego przez biblioteki RPM-a.

Pakiet ten powinien zostać zainstalowany, jeśli chcesz pisać w
Pythonie programy manipulujące pakietami i bazami danych rpm.

%description -n python-rpm -l pt_BR.UTF-8
O pacote rpm-python contém um módulo que permite que aplicações
escritas em Python utilizem a interface fornecida pelas bibliotecas
RPM (RPM Package Manager).

Esse pacote deve ser instalado se você quiser desenvolver programas em
Python para manipular pacotes e bancos de dados RPM.

%package apidocs
Summary:	RPM API documentation and guides
Summary(pl.UTF-8):	Documentacja API RPM-a i przewodniki
Group:		Documentation

%description apidocs
Documentation for RPM API and guides in HTML format generated from rpm
sources by doxygen.

%description apidocs -l pl.UTF-8
Dokumentacja API RPM-a oraz przewodniki w formacie HTML generowane ze
źrodeł RPM-a przez doxygen.

%prep
%setup -q -n %{name}-%{version}%{?subver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%{?with_system_lua:%patch11 -p1}
# CHECK ME - macrofiles: ~/etc could be used
#%%patch14 -p1
%patch16 -p1
echo '%%define	__perl_provides	%%{__perl} /usr/lib/rpm/perl.prov' > macros.perl
echo '%%define	__perl_requires	%%{__perl} /usr/lib/rpm/perl.req' >> macros.perl
echo '# obsoleted file' > macros.python
echo '%%define	__php_provides	/usr/lib/rpm/php.prov' > macros.php
echo '%%define	__php_requires	/usr/lib/rpm/php.req' >> macros.php
echo '%%define	__mono_provides	/usr/lib/rpm/mono-find-provides' > macros.mono
echo '%%define	__mono_requires	/usr/lib/rpm/mono-find-requires' >> macros.mono
install %{SOURCE9} scripts/php.prov.in
install %{SOURCE10} scripts/php.req.in
install %{SOURCE12} scripts/perl.prov
%patch23 -p1

%ifarch i386 i486
# disable TSC
%patch26 -p1
%endif
%patch27 -p1
%patch32 -p1
%patch34 -p1
%patch35 -p0
%patch36 -p1
%patch37 -p1
%patch42 -p1
%patch46 -p1
%patch47 -p1
# OLD COMMENTED OUT
#%%patch52 -p1 -- morearchs (rpmrc patch) adds ppc7400, ppc7400
%patch55 -p1
%patch59 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch60 -p1
%ifarch sparc64
%patch61 -p1
%endif

cd scripts
mv -f perl.req perl.req.in
mv -f perl.prov perl.prov.in
cd ..

# generate Group translations to *.po
awk -f %{SOURCE6} %{SOURCE1}

# update macros paths
#for f in doc{,/ja,/pl}/rpm.8 doc{,/ja,/pl}/rpmbuild.8 ; do
#	sed -e 's@lib/rpm/redhat@lib/rpm/pld@g' $f > ${f}.tmp
#	mv -f ${f}.tmp $f
#done

%build
%{__libtoolize}
#%{__autopoint}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

# config.guess doesn't handle athlon, so we have to change it by hand.
# rpm checks for CPU type at runtime, but it looks better
#sed -i -e 's|@host@|%{_target_cpu}-%{_target_vendor}-linux-gnu|' -e 's|@host_cpu@|%{_target_cpu}|' macros.in

%{?with_system_lua:CPPFLAGS="-I/usr/include/lua51 %{rpmcppflags}"}
# pass CC and CXX too in case of building with some older configure macro
%configure \
	CC="%{__newcc}" \
	CXX="%{__newcxx}" \
	CPP="%{__newcpp}" \
	WITH_PERL_VERSION=no \
	%{?with_autoreqdep:--enable-adding-packages-names-in-autogenerated-dependancies} \
	--enable-shared \
	--enable-static \
	%{!?with_apidocs:--without-apidocs} \
	%{?with_python:--with-python=%{py_ver} --with-python-lib-dir=%{py_sitedir}} \
	%{!?with_python:--without-python} \
	--with%{!?with_selinux:out}-selinux \
	--with-libelf \
	--with-zlib=external \
	--with-bzip2=external \
	--with-beecrypt=external \
	--with-lzma=external \
	--with-neon=%{?with_neon:external}%{!?with_neon:no} \
	--with-file=external \
	--with-popt=external \
	--with-db=%{?with_db:external}%{!?with_db:no} \
	--with-sqlite=%{?with_sqlite:external}%{!?with_sqlite:no} \
	--with-dbapi=%{!?with_sqlite_dbapi:db}%{?with_sqlite_dbapi:sqlite} \
	--with-lua=%{!?with_system_lua:internal}%{?with_system_lua:external} \
	--with-pcre=no \
	--with-keyutils=none \
	--without-path-versioned \
	--with-path-macros='%{_rpmlibdir}/macros:%{_rpmlibdir}/macros.pld:%{_rpmlibdir}/macros.build:%{_rpmlibdir}/%%{_target}/macros:%{_sysconfdir}/rpm/macros.*:%{_sysconfdir}/rpm/macros:%{_sysconfdir}/rpm/%%{_target}/macros:~/etc/rpmmacros:~/etc/.rpmmacros:~/.rpmmacros' \
	--with-bugreport="http://bugs.pld-linux.org/"

%{__make} -j1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CPP="%{__cpp}"

%{?with_apidocs:%{__make} apidocs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/%{_lib},/etc/sysconfig,%{_sysconfdir}/rpm,/var/lib/banner,/var/cache/hrmib,/etc/pki/rpm-gpg}

install %{SOURCE19} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/PLD-3.0-Th-GPG-key.asc

%{__make} install \
	pkgconfigdir=%{_pkgconfigdir} \
	DESTDIR=$RPM_BUILD_ROOT

# install ARCH macros
install -d $RPM_BUILD_ROOT%{_rpmlibdir}/noarch-linux
install %{SOURCE105} $RPM_BUILD_ROOT%{_rpmlibdir}/noarch-linux/macros

%ifarch %{ix86}
install -d $RPM_BUILD_ROOT%{_rpmlibdir}/{i386,i486,i586,i686,athlon,pentium3,pentium4}-linux
install %{SOURCE100} $RPM_BUILD_ROOT%{_rpmlibdir}/athlon-linux/macros
install %{SOURCE101} $RPM_BUILD_ROOT%{_rpmlibdir}/i386-linux/macros
install %{SOURCE102} $RPM_BUILD_ROOT%{_rpmlibdir}/i486-linux/macros
install %{SOURCE103} $RPM_BUILD_ROOT%{_rpmlibdir}/i586-linux/macros
install %{SOURCE104} $RPM_BUILD_ROOT%{_rpmlibdir}/i686-linux/macros
install %{SOURCE106} $RPM_BUILD_ROOT%{_rpmlibdir}/pentium3-linux/macros
install %{SOURCE107} $RPM_BUILD_ROOT%{_rpmlibdir}/pentium4-linux/macros
%endif

%ifarch %{x8664}
install -d $RPM_BUILD_ROOT%{_rpmlibdir}/{x86_64,ia32e,amd64}-linux
install %{SOURCE109} $RPM_BUILD_ROOT%{_rpmlibdir}/x86_64-linux/macros
install %{SOURCE110} $RPM_BUILD_ROOT%{_rpmlibdir}/ia32e-linux/macros
install %{SOURCE111} $RPM_BUILD_ROOT%{_rpmlibdir}/amd64-linux/macros
%endif

%ifarch %{ppc}
install -d $RPM_BUILD_ROOT%{_rpmlibdir}/ppc-linux
install %{SOURCE108} $RPM_BUILD_ROOT%{_rpmlibdir}/ppc-linux/macros
%endif

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/platform
# first platform file entry can't contain regexps
%{_target_cpu}-%{_target_vendor}-linux

# x86_64 things
%ifarch x86_64
x86_64-[^-]*-[Ll]inux(-gnu)?
amd64-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch amd64
amd64-[^-]*-[Ll]inux(-gnu)?
x86_64-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch ia32e
ia32e-[^-]*-[Ll]inux(-gnu)?
x86_64-[^-]*-[Ll]inux(-gnu)?
%endif

# x86 things
%ifarch athlon %{x8664}
athlon-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch pentium4 athlon %{x8664}
pentium4-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch pentium3 pentium4 athlon %{x8664}
pentium3-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch i686 pentium3 pentium4 athlon %{x8664}
i686-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch i586 i686 pentium3 pentium4 athlon %{x8664}
i586-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch i486 i586 i686 pentium3 pentium4 athlon %{x8664}
i486-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch %{ix86} %{x8664}
i386-[^-]*-[Ll]inux(-gnu)?
%endif

%ifarch alpha
alpha-[^-]*-[Ll]inux(-gnu)?
%endif

%ifarch ia64
ia64-[^-]*-[Ll]inux(-gnu)?
%endif

%ifarch ppc64
powerpc64-[^-]*-[Ll]inux(-gnu)?
ppc64-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch %{ppc} ppc64
powerpc-[^-]*-[Ll]inux(-gnu)?
ppc-[^-]*-[Ll]inux(-gnu)?
%endif

%ifarch s390x
s390x-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch s390 s390x
s390-[^-]*-[Ll]inux(-gnu)?
%endif

%ifarch sparc64
sparc64-[^-]*-[Ll]inux(-gnu)?
sparcv8-[^-]*-[Ll]inux(-gnu)?
sparcv9-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch sparcv9
sparcv8-[^-]*-[Ll]inux(-gnu)?
sparcv9-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch sparc sparcv9 sparc64
sparc-[^-]*-[Ll]inux(-gnu)?
%endif

# noarch
noarch-[^-]*-.*
EOF

%ifarch %{ppc}
#sed -e '/_target_platform/s/[%]{_target_cpu}/ppc/' \
#	-i $RPM_BUILD_ROOT%{_rpmlibdir}/ppc74[05]0-linux/macros
%endif

rm $RPM_BUILD_ROOT%{_rpmlibdir}/vpkg-provides*
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-{prov,req}.pl
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-{provides,requires}.perl
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-lang.sh

# not installed since 4.4.8 (-tools-perl subpackage)
install scripts/rpmdiff scripts/rpmdiff.cgi $RPM_BUILD_ROOT%{_rpmlibdir}

install macros.perl	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.perl
install macros.python	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.python
install macros.php	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.php
install macros.mono	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.mono
install %{SOURCE15}	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.java
install %{SOURCE18}	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.pld

install %{SOURCE1} doc/manual/groups
install %{SOURCE3} $RPM_BUILD_ROOT%{_rpmlibdir}/install-build-tree
install %{SOURCE4} $RPM_BUILD_ROOT%{_rpmlibdir}/find-spec-bcond
install %{SOURCE7} $RPM_BUILD_ROOT%{_rpmlibdir}/compress-doc
install %{SOURCE8} $RPM_BUILD_ROOT%{_rpmlibdir}/check-files
install %{SOURCE13} $RPM_BUILD_ROOT%{_rpmlibdir}/user_group.sh
install %{SOURCE16} $RPM_BUILD_ROOT%{_rpmlibdir}/java-find-requires
install scripts/find-php*	$RPM_BUILD_ROOT%{_rpmlibdir}
install scripts/php.{prov,req}	$RPM_BUILD_ROOT%{_rpmlibdir}
install %{SOURCE20} $RPM_BUILD_ROOT%{_rpmlibdir}/mimetypedeps.sh
install %{SOURCE5} $RPM_BUILD_ROOT%{_rpmlibdir}/hrmib-cache
install %{SOURCE14} $RPM_BUILD_ROOT/etc/sysconfig/rpm

install %{SOURCE17} $RPM_BUILD_ROOT%{_bindir}/banner.sh

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo

touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Conflictname
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Dirnames
install %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Filelinktos
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Obsoletename
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Providename
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Requirename

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

# If non-zero, all erasures will be automagically repackaged.
#%%_repackage_all_erasures    1
EOF

cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprovfiles <<EOF
# global list of files (regexps) which don't generate Provides
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprov <<EOF
# global list of script capabilities (regexps) not to be used in Provides
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreqfiles <<EOF
# global list of files (regexps) which don't generate Requires
^%{_examplesdir}/
^%{_docdir}/
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
# -- fam / gamin
^libfam.so.0
# -- mdns-bonjour: mDNSResponder-libs / avahi-compat-libdns_sd
^libdns_sd.so.1
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautocompressdoc <<EOF
# global list of file masks not to be compressed in DOCDIR
EOF

# for rpm -e|-U --repackage
install -d $RPM_BUILD_ROOT/var/{spool/repackage,lock/rpm}
touch $RPM_BUILD_ROOT/var/lock/rpm/transaction

# move rpm to /bin
mv $RPM_BUILD_ROOT%{_bindir}/rpm $RPM_BUILD_ROOT/bin
# move essential libs to /lib (libs that /bin/rpm links to)
for a in librpm-%{sover}.so librpmdb-%{sover}.so librpmio-%{sover}.so librpmbuild-%{sover}.so librpmmisc-%{sover}.so; do
	mv -f $RPM_BUILD_ROOT%{_libdir}/$a $RPM_BUILD_ROOT/%{_lib}
	ln -s /%{_lib}/$a $RPM_BUILD_ROOT%{_libdir}/$a
done

# Append rpm.platform contents to /usr/lib/rpm/${arch}-linux/macros
for m in $RPM_BUILD_ROOT%{_rpmlibdir}/*/macros ; do
	cat %{SOURCE2} | %{__sed} 's#@LIB@#%{_lib}#' >> $m
done
# remove arch dependant macros which have no use on noarch
%{__sed} -i -e '
/{__spec_install_post_strip}/d
/{__spec_install_post_chrpath}/d
/{__spec_install_post_compress_modules}/d
' $RPM_BUILD_ROOT%{_rpmlibdir}/noarch-linux/macros

# Bourne shell script vs ELF executable linked with rpm,rpmdb,rpmio
mv $RPM_BUILD_ROOT{%{_rpmlibdir},%{_bindir}}/rpm2cpio

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

rm $RPM_BUILD_ROOT%{py_sitedir}/rpm/*.{la,a,py}

# wrong location, not used anyway
rm $RPM_BUILD_ROOT%{_rpmlibdir}/rpm.{daily,log,xinetd}
# utils dropped in 4.4.8 -- their manuals
rm $RPM_BUILD_ROOT%{_mandir}/{,*/}/man8/rpmgraph.8
# unpackaged in 4.4.9, reasons unknown
rm $RPM_BUILD_ROOT%{_rpmlibdir}/symclash.{sh,py}

%find_lang %{name}

rm -rf manual
cp -a doc/manual manual
rm -f manual/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun lib -- %{name}-lib < %{version}
rm -f /var/lib/rpm/__db*

%pretrans
# this needs to be a dir
if [ -f %{_sysconfdir}/rpm/sysinfo ]; then
	umask 022
	mv -f %{_sysconfdir}/rpm/sysinfo{,.rpmsave}
	mkdir %{_sysconfdir}/rpm/sysinfo
fi

%triggerpostun -- %{name} < 4.4.9-44
%{_rpmlibdir}/hrmib-cache

%post	lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%pretrans build
find %{_rpmlibdir} -name '*-linux' -type l | xargs rm -f

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES CREDITS README pubkeys/JBJ-GPG-KEY manual/*

%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/PLD-3.0-Th-GPG-key.asc

%attr(755,root,root) /bin/rpm
#%attr(755,root,root) %{_bindir}/rpmdb
#%attr(755,root,root) %{_bindir}/rpmquery
#%attr(755,root,root) %{_bindir}/rpmsign
#%attr(755,root,root) %{_bindir}/rpmverify

%dir %{_sysconfdir}/rpm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/macros
%dir %{_sysconfdir}/rpm/sysinfo
# these are ok to be replaced
%config %verify(not md5 mtime size) %{_sysconfdir}/rpm/sysinfo/*
%config %verify(not md5 mtime size) %{_sysconfdir}/rpm/platform


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

# exported package NVRA (stamped with install tid)
# net-snmp hrSWInstalledName queries, bash-completions
%dir /var/cache/hrmib

#%attr(755,root,root) %{_rpmlibdir}/rpmd
#%{!?with_static:%attr(755,root,root) %{_rpmlibdir}/rpm[eiu]}
#%attr(755,root,root) %{_rpmlibdir}/rpmk
#%attr(755,root,root) %{_rpmlibdir}/rpm[qv]

%{_rpmlibdir}/rpmpopt*
%{_rpmlibdir}/macros
%{_rpmlibdir}/macros.pld

%attr(755,root,root) %{_rpmlibdir}/hrmib-cache

%files base
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rpm
%dir %{_rpmlibdir}
%attr(755,root,root) %{_bindir}/banner.sh
%attr(755,root,root) %{_rpmlibdir}/user_group.sh
%dir /var/lib/banner

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/librpm-%{sover}.so
%attr(755,root,root) /%{_lib}/librpmdb-%{sover}.so
%attr(755,root,root) /%{_lib}/librpmio-%{sover}.so
%attr(755,root,root) /%{_lib}/librpmbuild-%{sover}.so
%attr(755,root,root) /%{_lib}/librpmmisc-%{sover}.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librpm.so
%attr(755,root,root) %{_libdir}/librpm-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmbuild.so
%attr(755,root,root) %{_libdir}/librpmbuild-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmconstant.so
%attr(755,root,root) %{_libdir}/librpmconstant-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmdb.so
%attr(755,root,root) %{_libdir}/librpmdb-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmio.so
%attr(755,root,root) %{_libdir}/librpmio-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmmisc.so
%attr(755,root,root) %{_libdir}/librpmmisc-%{sover}.so
%{_libdir}/librpm*.la
%{_includedir}/rpm
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/librpm*.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpm2cpio
%attr(755,root,root) %{_bindir}/rpmcache
%attr(755,root,root) %{_bindir}/rpmconstant
%attr(755,root,root) %{_bindir}/rpmdigest
%attr(755,root,root) %{_bindir}/rpmgrep
%attr(755,root,root) %{_bindir}/rpmrepo
%attr(755,root,root) %{_bindir}/rpmmtree
%attr(755,root,root) %{_rpmlibdir}/debugedit
%attr(755,root,root) %{_rpmlibdir}/find-debuginfo.sh
%attr(755,root,root) %{_rpmlibdir}/rpmcmp
%attr(755,root,root) %{_rpmlibdir}/rpmdb_loadcvt
%attr(755,root,root) %{_rpmlibdir}/rpmdeps
%attr(755,root,root) %{_rpmlibdir}/tgpg
%{_mandir}/man1/rpmgrep.1*
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpmcache.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmmtree.8*
%lang(ja) %{_mandir}/ja/man8/rpm2cpio.8*
%lang(ja) %{_mandir}/ja/man8/rpmcache.8*
%lang(ko) %{_mandir}/ko/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpmcache.8*
%lang(pl) %{_mandir}/pl/man8/rpmdeps.8*
%lang(ru) %{_mandir}/ru/man8/rpm2cpio.8*

%files utils-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/rpmdiff*

%if %{with static}
%files utils-static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpm[ieu]
%attr(755,root,root) %{_rpmlibdir}/rpm[ieu]
%endif

%files build
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/noauto*
%attr(755,root,root) %{_rpmlibdir}/brp-*
%attr(755,root,root) %{_rpmlibdir}/check-files
# %attr(755,root,root) %{_rpmlibdir}/check-prereqs
%attr(755,root,root) %{_rpmlibdir}/compress-doc
#%attr(755,root,root) %{_rpmlibdir}/config.*
%attr(755,root,root) %{_rpmlibdir}/cross-build
%attr(755,root,root) %{_rpmlibdir}/find-spec-bcond
%attr(755,root,root) %{_rpmlibdir}/getpo.sh
%attr(755,root,root) %{_rpmlibdir}/install-build-tree
%attr(755,root,root) %{_rpmlibdir}/mkinstalldirs
%attr(755,root,root) %{_rpmlibdir}/u_pkg.sh
%attr(755,root,root) %{_rpmlibdir}/executabledeps.sh
%attr(755,root,root) %{_rpmlibdir}/libtooldeps.sh
%attr(755,root,root) %{_rpmlibdir}/mimetypedeps.sh
# needs hacked pkg-config to return anything
%attr(755,root,root) %{_rpmlibdir}/pkgconfigdeps.sh
#%attr(755,root,root) %{_rpmlibdir}/rpmb
#%attr(755,root,root) %{_rpmlibdir}/rpmt
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
%ifarch %{ppc}
%{_rpmlibdir}/ppc*
%endif
%ifarch sparc sparc64
%{_rpmlibdir}/sparc*
%endif
%ifarch %{x8664}
%{_rpmlibdir}/amd64*
%{_rpmlibdir}/ia32e*
%{_rpmlibdir}/x86_64*
%endif
# must be here for "Requires: rpm-*prov" to work
%{_rpmlibdir}/macros.java
%{_rpmlibdir}/macros.mono
%{_rpmlibdir}/macros.perl
%{_rpmlibdir}/macros.php
# not used yet ... these six depend on perl
#%attr(755,root,root) %{_rpmlibdir}/http.req
#%attr(755,root,root) %{_rpmlibdir}/magic.prov
#%attr(755,root,root) %{_rpmlibdir}/magic.req
#%{_rpmlibdir}/sql.prov
#%{_rpmlibdir}/sql.req
#%{_rpmlibdir}/tcl.req

%attr(755,root,root) %{_bindir}/gendiff
%attr(755,root,root) %{_bindir}/rpmbuild

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%lang(ja) %{_mandir}/ja/man8/rpmbuild.8*
%lang(pl) %{_mandir}/pl/man1/gendiff.1*
%lang(pl) %{_mandir}/pl/man8/rpmbuild.8*

%files javaprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/java-find-requires
# needs jar (any jdk), jcf-dump (gcc-java) to work
%attr(755,root,root) %{_rpmlibdir}/javadeps.sh

%files perlprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/perl.*
#%attr(755,root,root) %{_rpmlibdir}/perldeps.pl
#%attr(755,root,root) %{_rpmlibdir}/find-perl-*
#%attr(755,root,root) %{_rpmlibdir}/find-*.perl
#%attr(755,root,root) %{_rpmlibdir}/find-prov.pl
#%attr(755,root,root) %{_rpmlibdir}/find-req.pl
#%attr(755,root,root) %{_rpmlibdir}/get_magic.pl

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
%dir %{py_sitedir}/rpm
%attr(755,root,root) %{py_sitedir}/rpm/*.so
%{py_sitedir}/rpm/*.py[co]
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs
%endif
