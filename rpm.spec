#
# TODO:
# - when adopting, use 4.5 ticket for checklist: https://bugs.launchpad.net/pld-linux/+bug/262985
#
# Conditional build:
%bcond_without	apidocs		# Doxygen based API documentation
%bcond_without	python3		# Python (3) bindings
%bcond_without	plugins		# plugins (all, including: audit, imaevm, selinux, dbus)
%bcond_without	recommends_tags	# use of Recommends tag (disable for bootstrapping)
%bcond_with	imaevm		# IMA/EVM signing support (requires libimaevm from ima-evm-utils)
%bcond_without	audit		# audit plugin
%bcond_without	selinux		# SELinux plugin
%bcond_without	dbus		# dbus announce and systemd inhibit plugins
%bcond_without	fsverity	# fsverity plugin
%bcond_without	sequoia		# Sequoia OpenPGP (replaces rpmpgp_legacy)

%define		popt_ver	1.15

%if "%{_rpmversion}" >= "4.12" && "%{_rpmversion}" < "5"
%define	with_recommends_tags	1
%endif

%if %{without plugins}
%undefine	with_audit
%undefine	with_selinux
%undefine	with_dbus
%endif
Summary:	RPM Package Manager
Summary(de.UTF-8):	RPM Packet-Manager
Summary(es.UTF-8):	Gestor de paquetes RPM
Summary(pl.UTF-8):	Aplikacja do zarządzania pakietami RPM
Summary(pt_BR.UTF-8):	Gerenciador de pacotes RPM
Summary(ru.UTF-8):	Менеджер пакетов от RPM
Summary(uk.UTF-8):	Менеджер пакетів від RPM
Name:		rpm
Version:	4.20.0
Release:	10
Epoch:		1
License:	GPL v2 / LGPL v2.1
Group:		Base
Source0:	http://ftp.rpm.org/releases/rpm-4.20.x/%{name}-%{version}.tar.bz2
# Source0-md5:	6aee0b0b66b40e1eb04b6c3b7d87cf9f
Source1:	ftp://ftp.pld-linux.org/dists/th/PLD-3.0-Th-GPG-key.asc
# Source1-md5:	23914bb49fafe7153cee87126d966461
Source100:	https://github.com/rpm-software-management/rpmpgp_legacy/archive/1.1/rpmpgp_legacy-1.1.tar.gz
# Source100-md5:	cd07ad8a90c963998491ca02d9f50a3d
Source2:	macros.local
Source3:	macros.lang
Source4:	%{name}.sysconfig
Source5:	%{name}.groups
Source6:	%{name}-groups-po.awk
Source7:	%{name}-install-tree
Source9:	%{name}-user_group.sh
# http://svn.pld-linux.org/banner.sh/
Source10:	banner.sh
Source11:	%{name}.noautoprov
Source12:	%{name}.noautoprovfiles
Source13:	%{name}.noautoreq
Source14:	%{name}.noautoreqfiles
Source16:	libtooldeps.sh
Source17:	libtool.attr
Patch0:		%{name}-popt-aliases.patch
Patch3:		%{name}-scripts-closefds.patch
Patch4:		%{name}-dir-macros-relative.patch
Patch6:		%{name}-debuginfo.patch
Patch7:		%{name}-changelog_order_check_nonfatal.patch
Patch8:		%{name}-postun-nofail.patch
Patch9:		%{name}-clean-docdir.patch
Patch10:	%{name}-perl-magic.patch
Patch11:	%{name}-ignore-missing-macro-files.patch
Patch12:	x32.patch
Patch13:	rpm5-db-compat.patch
Patch15:	missing-macros.patch
Patch16:	pkgconfig.patch
Patch17:	uname-deps.patch
Patch18:	arm_abi.patch
Patch19:	ix86-platforms.patch
Patch20:	shortcircuited-deps.patch
Patch21:	cpuinfo-deps.patch
Patch22:	rpmio-read-proc-files.patch
Patch23:	allow-at-in-ver-rel.patch
Patch24:	default-patch-flags.patch
Patch25:	missing-ghost-terminate-build.patch
Patch26:	missing-doc-terminate-build.patch
Patch27:	noexpand.patch
Patch28:	skip-symlinks.patch
Patch29:	build-locale.patch
Patch30:	no-exe-for-elf-req.patch
Patch31:	check-valid-arch-early.patch
URL:		https://rpm.org/
BuildRequires:	acl-devel
%{?with_audit:BuildRequires:	audit-libs-devel}
BuildRequires:	bzip2-devel >= 1.0.2-17
BuildRequires:	bubblewrap
BuildRequires:	cmake >= 3.18
%{?with_plugins:BuildRequires:	dbus-devel >= 1.3}
BuildRequires:	elfutils-devel >= 0.159
BuildRequires:	gettext-tools >= 0.19.2
%{?with_imaevm:BuildRequires:	ima-evm-utils-devel >= 1.0}
BuildRequires:	libarchive-devel
BuildRequires:	libcap-devel
%{?with_fsverity:BuildRequires:	libfsverity-devel}
BuildRequires:	libgcrypt-devel
BuildRequires:	libgomp-devel >= 6:4.5
BuildRequires:	libmagic-devel
%{?with_selinux:BuildRequires:	libselinux-devel >= 2.1.0}
# needed only for AM_PROG_CXX used for CXX substitution in rpm.macros
BuildRequires:	libstdc++-devel
BuildRequires:	lua-devel >= 5.2
BuildRequires:	patch >= 2.2
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= %{popt_ver}
BuildRequires:	python3-modules >= 1:3.2
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.750
%endif
BuildRequires:	readline-devel
%{?with_sequoia:BuildRequires:	rpm-sequoia-devel >= 1.4.0}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	sqlite3-devel >= 3.22.0
BuildRequires:	tcl
BuildRequires:	xz-devel
BuildRequires:	zlib-devel >= 1.0.5
BuildRequires:	zstd-devel >= 1.3.8
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	graphviz
BuildRequires:	tetex-pdftex
%endif
Requires(posttrans):	coreutils
Requires:	%{name}-base = %{epoch}:%{version}-%{release}
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}
Requires:	FHS >= 3.0-2
Requires:	libgcrypt
Requires:	popt >= %{popt_ver}
Requires:	rpm-pld-macros >= 2.002
%if %{with recommends_tags}
Recommends:	rpm-plugin-audit
Recommends:	rpm-plugin-prioreset
Recommends:	rpm-plugin-syslog
Recommends:	rpm-plugin-systemd-inhibit
%endif
Obsoletes:	rpm-utils-perl < 1:4.15
Obsoletes:	rpm-utils-static < 1:4.15
Conflicts:	glibc < 2.2.92
# db4.6 poldek needed
Conflicts:	poldek < 0.21-0.20070703.00.3
# segfaults with lzma 0.42.2
Conflicts:	lzma-libs < 4.999.3
Conflicts:	util-vserver < 0.30.216-1.pre3034.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_binary_payload		w9.gzdio

# don't require very fresh rpm.macros to build
%define		find_lang sh ./scripts/find-lang.sh $RPM_BUILD_ROOT
%define		ix86	i386 i486 i586 i686 athlon geode pentium3 pentium4
%define		ppc	ppc ppc7400 ppc7450
%define		x8664	amd64 ia32e x86_64

%define		_rpmlibdir /usr/lib/rpm

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
Obsoletes:	rpm-scripts < 4.4
Obsoletes:	vserver-rpm < 1

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
Requires:	elfutils-libs >= 0.159
Requires:	libmagic >= 1.15-2
Requires:	popt >= %{popt_ver}
Requires:	sqlite3-libs >= 3.22.0
Requires:	zlib >= 1.0.5
Requires:	zstd >= 1.3.8
Obsoletes:	rpm-libs < 4.0.2-4
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
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}
Requires:	acl-devel
%{?with_audit:Requires:	audit-libs-devel}
Requires:	bzip2-devel
Requires:	elfutils-devel >= 0.159
Requires:	libcap-devel
Requires:	libgcrypt-devel
Requires:	libgomp-devel >= 6:4.5
Requires:	libmagic-devel
%if %{with selinux}
Requires:	libselinux-devel
Requires:	libsemanage-devel
Requires:	libsepol-devel
%endif
Requires:	lua-devel >= 5.2
Requires:	popt-devel >= %{popt_ver}
Requires:	sqlite3-devel >= 3.22.0
Requires:	xz-devel
Requires:	zlib-devel >= 1.0.5
Requires:	zstd-devel >= 1.3.8
Obsoletes:	rpm-static < 1:4.15

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

%package utils
Summary:	Additional utilities for managing RPM packages and database
Summary(de.UTF-8):	Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken
Summary(pl.UTF-8):	Dodatkowe narzędzia do zarządzania bazą RPM-a i pakietami
Group:		Applications/File
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	popt >= %{popt_ver}
%if %{with recommends_tags}
Recommends:	bzip2
Recommends:	gzip
%endif
Conflicts:	filesystem-debuginfo < 3.0-16

%description utils
Additional utilities for managing RPM packages and database.

%description utils -l de.UTF-8
Zusatzwerkzeuge für Verwaltung RPM-Pakete und Datenbanken.

%description utils -l pl.UTF-8
Dodatkowe narzędzia do zarządzania bazą RPM-a i pakietami.

%package build
Summary:	Scripts for building binary RPM packages
Summary(de.UTF-8):	Scripts fürs Bauen binärer RPM-Pakete
Summary(pl.UTF-8):	Skrypty pomocnicze do budowania binarnych RPM-ów
Summary(pt_BR.UTF-8):	Scripts e programas executáveis usados para construir pacotes
Summary(ru.UTF-8):	Скрипты и утилиты, необходимые для сборки пакетов
Summary(uk.UTF-8):	Скрипти та утиліти, необхідні для побудови пакетів
Group:		Applications/File
Requires(pretrans):	coreutils
Requires(pretrans):	findutils
Requires:	%{name}-utils = %{epoch}:%{version}-%{release}
Requires:	/bin/id
Requires:	awk
Requires:	bzip2
Requires:	chrpath >= 0.10-4
Requires:	cpio
Requires:	debugedit
Requires:	diffutils
Requires:	elfutils
Requires:	file >= 4.17
Requires:	fileutils
Requires:	findutils
Requires:	rpm-pld-macros-build >= 1.744
Requires:	gcc
Requires:	glibc-devel
Requires:	grep
Requires:	gzip
Requires:	make
Requires:	patch
Requires:	sed >= 4.0
Requires:	sh-utils
Requires:	tar >= 1:1.22
Requires:	textutils
Requires:	which
Requires:	xz
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

%package -n python3-rpm
Summary:	Python 3 interface to RPM library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki RPM-a
Summary(pt_BR.UTF-8):	Módulo Python 3 para aplicativos que manipulam pacotes RPM
Group:		Development/Languages/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python3
Obsoletes:	python-rpm < 1:4.16.0
Obsoletes:	rpm-python < 4.0.2-50

%description -n python3-rpm
The python3-rpm package contains a module which permits applications
written in the Python 3 programming language to use the interface
supplied by RPM (RPM Package Manager) libraries.

This package should be installed if you want to develop Python 3
programs that will manipulate RPM packages and databases.

%description -n python3-rpm -l pl.UTF-8
Pakiet python3-rpm zawiera moduł, który pozwala aplikacjom napisanym w
Pythonie 3 na używanie interfejsu dostarczanego przez biblioteki
RPM-a.

Pakiet ten powinien zostać zainstalowany, jeśli chcesz pisać w
Pythonie 3 programy manipulujące pakietami i bazami danych rpm.

%description -n python3-rpm -l pt_BR.UTF-8
O pacote python3-rpm contém um módulo que permite que aplicações
escritas em Python 3 utilizem a interface fornecida pelas bibliotecas
RPM (RPM Package Manager).

Esse pacote deve ser instalado se você quiser desenvolver programas em
Python 3 para manipular pacotes e bancos de dados RPM.

%package plugin-audit
Summary:	Plugin for logging audit events on package operations
Summary(pl.UTF-8):	Wtyczka do logowania zdarzeń audytowych przy operacjach na pakietach
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-audit
Plugin for libaudit support.

%description plugin-audit -l pl.UTF-8
Wtyczka do obsługi libaudit.

%package plugin-syslog
Summary:	Plugin for syslog functionality
Summary(pl.UTF-8):	Wtyczka do funkcjonalności sysloga
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-syslog
This plugin exports RPM actions to the system log.

%description plugin-syslog -l pl.UTF-8
Ta wtyczka eksportuje akcje RPM-a do logu systemowego.

%package plugin-systemd-inhibit
Summary:	Plugin for systemd inhibit functionality
Summary(pl.UTF-8):	Wtyczka do funkcjonalności systemd inhibit
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}
Requires:	dbus >= 1.3

%description plugin-systemd-inhibit
This plugin blocks systemd from entering idle, sleep or shutdown while
an rpm transaction is running using the systemd-inhibit mechanism.

%description plugin-systemd-inhibit -l pl.UTF-8
Ta wtyczka blokuje systemd przed wejściem w stan bezczynności (idle),
uśpienia (sleep) lub zamykania (shutdown) podczas trwania transakcji
RPM-a, korzystając z mechanizmu systemd-inhibit.

%package plugin-ima
Summary:	Plugin for IMA file signatures
Summary(pl.UTF-8):	Wtyczka do sygnatur plików IMA
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-ima
This plugin adds support for enforcing and verifying IMA file
signatures in an rpm.

%description plugin-ima -l pl.UTF-8
Ta wtyczka dodaje obsługę wymuszania i weryfikacji podpisów plików IMA
w RPM-ie.

%package plugin-prioreset
Summary:	Plugin for resetting scriptlet priorities for SysV init
Summary(pl.UTF-8):	Wtyczka do resetowania priorytetu skryptletów przy inicie SysV
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-prioreset
This plugin is useful on legacy SysV init systems if you run rpm
transactions with nice/ionice priorities. Should not be used on
systemd systems.

%description plugin-prioreset -l pl.UTF-8
Ta wtyczka jest przydatna w systemach ze starym procesem init w wersji
SysV, jeżeli transakcje RPM-a są uruchamiane z priorytetami
nice/ionice. Nie powinna być używana w systemach z systemd.

%package plugin-selinux
Summary:	Plugin for SELinux functionality
Summary(pl.UTF-8):	Wtyczka do funkcjonalności SELinux
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}
Requires:	libselinux >= 2.1.0

%description plugin-selinux
Plugin for SELinux functionality.

%description plugin-selinux -l pl.UTF-8
Wtyczka do funkcjonalności SELinux.

%package plugin-fsverity
Summary:	Plugin for fsverity file signatures
Summary(pl.UTF-8):	Wtyczka do sygnatur plików fsverity
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-fsverity
Plugin for fsverity file signatures.

%description plugin-fsverity -l pl.UTF-8
Wtyczka do sygnatur plików fsverity.

%package plugin-fapolicyd
Summary:	Plugin for fapolicyd support
Summary(pl.UTF-8):	Wtyczka do obsługi fapolicyd
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-fapolicyd
Plugin for fapolicyd support.

See https://people.redhat.com/sgrubb/fapolicyd/ for information about
the fapolicyd daemon.

%description plugin-fapolicyd -l pl.UTF-8
Wtyczka do obsługi fapolicyd.

Informacje na temat demona fapolicyd można znaleźć pod adresem
<https://people.redhat.com/sgrubb/fapolicyd/>.

%package plugin-dbus-announce
Summary:	Plugin for announcing transactions on the DBUS
Summary(pl.UTF-8):	Wtyczka ogłaszająca transakcje przez DBUS
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-dbus-announce
The plugin announces basic information about rpm transactions to the
system DBUS - like packages installed or removed. Other programs can
subscribe to the signals to get notified when packages on the system
change.

%description plugin-dbus-announce -l pl.UTF-8
Ta wtyczka ogłasza przez podstawowe szynę systemową DBUS informacje o
transakcjach RPM-a, takie jak pakiety, które są instalowane lub
usuwane. Inne programy mogą zasubskrybować sygnały powiadamiające o
zmianach w pakietach systemowych.

%package plugin-unshare
Summary:	Plugin for scriptlet isolation with Linux namespaces
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-unshare
This plugin allows using various Linux-specific namespace-related
technologies inside transactions, such as to harden and limit
scriptlet access to resources.

%package sign
Summary:	Package signing support
Summary(pl.UTF-8):	Obsługa podpisywania pakietów
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description sign
This package contains support for digitally signing RPM packages.

%description sign -l pl.UTF-8
Ten pakiet zawiera obsługę cyfrowego podpisywania pakietów RPM.

%package apidocs
Summary:	RPM API documentation and guides
Summary(pl.UTF-8):	Documentacja API RPM-a i przewodniki
Group:		Documentation
BuildArch:	noarch

%description apidocs
Documentation for RPM API and guides in HTML format generated from rpm
sources by doxygen.

%description apidocs -l pl.UTF-8
Dokumentacja API RPM-a oraz przewodniki w formacie HTML generowane ze
źrodeł RPM-a przez doxygen.

%prep
%setup -q -a100 -n %{name}-%{version}%{?subver}
%patch -P 0 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 6 -p1
%patch -P 7 -p1
%patch -P 8 -p1
%patch -P 9 -p1
%patch -P 10 -p1
%patch -P 11 -p1
%patch -P 12 -p1
%patch -P 13 -p1
%patch -P 15 -p1
%patch -P 16 -p1
%patch -P 17 -p1
%patch -P 18 -p1
%patch -P 19 -p1
%patch -P 20 -p1
%patch -P 21 -p1
%patch -P 22 -p1
%patch -P 23 -p1
%patch -P 24 -p1
%patch -P 25 -p1
%patch -P 26 -p1
%patch -P 27 -p1
%patch -P 28 -p1
%patch -P 29 -p1
%patch -P 30 -p1
%patch -P 31 -p1

# generate Group translations to *.po
awk -f %{SOURCE6} %{SOURCE5}

ln -s ../rpmpgp_legacy-1.1 rpmio/rpmpgp_legacy

# rpm checks for CPU type at runtime, but it looks better
%{__sed} -i \
	-e 's|@host@|%{_target_cpu}-%{_target_vendor}-%{_target_os}|' \
	-e 's|@host_cpu@|%{_target_cpu}|' \
	-e 's|@host_os@|%{_target_os}|' \
	macros.in

# Use fully qualified names for CC and CXX
__CC=$(which $(cc -dumpmachine)-gcc 2>/dev/null)
__CXX=$(which $(c++ -dumpmachine)-g++ 2>/dev/null)
%{__sed} -i -e "s|@__CC@|$__CC|" -e "s|@__CXX@|$__CXX|" macros.in

%build
mkdir -p build-cmake
cd build-cmake
%cmake ../ \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir} \
	%{cmake_on_off python3 ENABLE_PYTHON} \
	%{cmake_on_off plugins ENABLE_PLUGINS} \
	%{cmake_on_off audit WITH_AUDIT} \
	%{cmake_on_off imaevm WITH_IMAEVM} \
	%{cmake_on_off selinux WITH_SELINUX} \
	%{cmake_on_off dbus WITH_DBUS} \
	%{cmake_on_off fsverity WITH_FSVERITY} \
	%{cmake_on_off apidocs WITH_DOXYGEN} \
	%{cmake_on_off sequoia WITH_SEQUOIA} \
	%{!?with_sequoia:-DWITH_LEGACY_OPENPGP=ON} \
	-DMKTREE_BACKEND=rootfs \
	-DENABLE_SQLITE=ON \
	-DENABLE_NDB=ON \
	-DENABLE_BDB_RO=ON \
	-DWITH_CAP=ON \
	-DWITH_FAPOLICYD=ON \
	-DWITH_ACL=ON \
	-DWITH_ARCHIVE=ON \
	-DWITH_ZSTD=ON \
	-DRPM_VENDOR=pld

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/%{_lib},/etc/sysconfig,%{_sysconfdir}/{rpm,pki/rpm-gpg}} \
	$RPM_BUILD_ROOT/var/lib/{banner,rpm}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/PLD-3.0-Th-GPG-key.asc

%{__make} -C build-cmake install \
	pkgconfigdir=%{_pkgconfigdir} \
	DESTDIR=$RPM_BUILD_ROOT

# these will be packaged separately
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

# cleanup
%ifnarch %{ix86} %{x8664} x32
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/athlon-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/geode-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/i386-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/i486-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/i586-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/i686-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/pentium3-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/pentium4-linux/macros
%endif

%ifnarch %{x8664} x32
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/amd64-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ia32e-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/x32-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/x86_64-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/x86_64_v2-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/x86_64_v3-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/x86_64_v4-linux/macros
%endif

%ifnarch %{ppc}
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/m68k-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc32dy4-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc64*-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc8260-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc8560-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc*series-linux/macros
%endif

%ifnarch aarch64
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/aarch64-linux/macros
%endif

%ifnarch %{arm}
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/arm*-linux/macros
%endif

%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/alpha*-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ia64-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/loongarch64-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/mips*-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/riscv64-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/s390*-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/sh*-linux/macros
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/platform/sparc*-linux/macros

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/platform
%ifarch x32
%{_target_cpu}-%{_target_vendor}-linux-gnux32
%else
%{_target_cpu}-%{_target_vendor}-linux
%endif
EOF

%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/find-lang.sh

install -d $RPM_BUILD_ROOT%{_rpmlibdir}/pld

cp -p %{SOURCE7} $RPM_BUILD_ROOT%{_rpmlibdir}/install-build-tree
cp -p %{SOURCE9} $RPM_BUILD_ROOT%{_rpmlibdir}/user_group.sh
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/rpm

cp -p %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/banner.sh

cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.lang
cp -p %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprov
cp -p %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprovfiles
cp -p %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreq
cp -p %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreqfiles

cp -p %{SOURCE16} $RPM_BUILD_ROOT%{_rpmlibdir}/libtooldeps.sh
cp -p %{SOURCE17} $RPM_BUILD_ROOT%{_rpmlibdir}/fileattrs/libtool.attr

# move rpm to /bin
%{__mv} $RPM_BUILD_ROOT%{_bindir}/rpm $RPM_BUILD_ROOT/bin
ln -sf /bin/rpm $RPM_BUILD_ROOT%{_bindir}/rpmquery
ln -sf /bin/rpm $RPM_BUILD_ROOT%{_bindir}/rpmverify

# move essential libs to /lib (libs that /bin/rpm links to)
for a in librpm.so librpmbuild.so librpmio.so librpmsign.so; do
	mv -f $RPM_BUILD_ROOT%{_libdir}/${a}.* $RPM_BUILD_ROOT/%{_lib}
	ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/${a}.*.*.*) $RPM_BUILD_ROOT%{_libdir}/${a}
done

# init an empty database for %ghost'ing for all supported backends
for be in sqlite bdb ndb; do
	build-cmake/tools/rpmdb \
		--macros=$RPM_BUILD_ROOT%{_rpmlibdir}/macros \
		--rcfile=$RPM_BUILD_ROOT%{_rpmlibdir}/rpmrc \
		--dbpath=${PWD}/${be} \
		--define "_db_backend ${be}" \
		--initdb
	cp -va ${be}/. $RPM_BUILD_ROOT/var/lib/rpm/
done

%if %{with python3}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

# wrong location, not used anyway
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/rpm.{daily,log}

# unsupported locale
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%posttrans
if [ -e /var/lib/rpm/Packages ]; then
	if [ ! -e /var/lib/rpm.rpmbackup-%{version}-%{release} ] && \
			/bin/cp -a /var/lib/rpm /var/lib/rpm.rpmbackup-%{version}-%{release}; then
		echo
		echo "Backup of the rpm database has been created in /var/lib/rpm.rpmbackup-%{version}-%{release}"
		echo
	fi
	echo
	echo 'If poldek aborts after migration with rpmdb error, this is expected behaviour,'
	echo 'you should ignore it and restart poldek'
	echo
	%{__rm} -rf /var/lib/rpm/log >/dev/null 2>/dev/null || :
	%{__rm} -rf /var/lib/rpm/tmp >/dev/null 2>/dev/null || :
	# Unlock database for rebuild, safe since this is posttrans
	%{__rm} -f /var/lib/rpm/.rpm.lock >/dev/null 2>/dev/null || :
	if ! /usr/bin/rpmdb --rebuilddb; then
		echo
		echo "rpm database conversion failed!"
		echo "You have to run '/usr/bin/rpmdb --rebuilddb' manually"
		echo
		exit 1
	fi
fi

%post
if [ -d /var/cache/hrmib ]; then
	%{__rm} -rf /var/cache/hrmib
	echo "HR-MIB is not supported by this rpm version."
	echo "/var/cache/hrmib has been removed."
fi

%post	lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%pretrans build
find %{_rpmlibdir} -name '*-linux' -type l | xargs rm -f

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog CREDITS README docs/manual

%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/PLD-3.0-Th-GPG-key.asc

%attr(755,root,root) /bin/rpm
%attr(755,root,root) %{_bindir}/rpmdb
%attr(755,root,root) %{_bindir}/rpmkeys
%attr(755,root,root) %{_bindir}/rpmquery
%attr(755,root,root) %{_bindir}/rpmsort
%attr(755,root,root) %{_bindir}/rpmverify

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/macros
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/macros.lang
# this is ok to be replaced
%config %verify(not md5 mtime size) %{_sysconfdir}/rpm/platform

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpmsort.8*
%{_mandir}/man8/rpm-misc.8*
%{?with_plugins:%{_mandir}/man8/rpm-plugins.8*}

%dir /var/lib/rpm
%ghost %config(missingok,noreplace) /var/lib/rpm/*
%ghost /var/lib/rpm/.*.lock

%{_rpmlibdir}/rpmpopt*
%{_rpmlibdir}/rpmrc
%{_rpmlibdir}/macros
%dir %{_rpmlibdir}/macros.d
%dir %{_rpmlibdir}/platform
%{_rpmlibdir}/platform/noarch-*
%ifarch %{ix86} %{x8664} x32
%{_rpmlibdir}/platform/athlon*
%{_rpmlibdir}/platform/geode*
%{_rpmlibdir}/platform/i?86*
%{_rpmlibdir}/platform/pentium*
%endif
%ifarch %{x8664} x32
%{_rpmlibdir}/platform/amd64*
%{_rpmlibdir}/platform/ia32e*
%{_rpmlibdir}/platform/x86_64*
%{_rpmlibdir}/platform/x32*
%endif
%ifarch alpha
%{_rpmlibdir}/platform/alpha*
%endif
%ifarch aarch64
%{_rpmlibdir}/platform/aarch64*
%endif
%ifarch %{arm}
%{_rpmlibdir}/platform/arm*
%endif
%ifarch ia64
%{_rpmlibdir}/platform/ia64*
%endif
%ifarch mips mipsel mips64 mips64el
%{_rpmlibdir}/platform/mips*
%endif
%ifarch %{ppc}
%{_rpmlibdir}/platform/ppc*
%endif
%ifarch sparc sparc64
%{_rpmlibdir}/platform/sparc*
%endif

%dir %{_rpmlibdir}/pld

%attr(755,root,root) %{_rpmlibdir}/rpmdb_dump
%attr(755,root,root) %{_rpmlibdir}/rpmdb_load
%attr(755,root,root) %{_rpmlibdir}/rpmdump

# valgrind suppression file for rpm
%{_rpmlibdir}/rpm.supp

%files base
%defattr(644,root,root,755)
%dir %{_sysconfdir}/rpm
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rpm
%dir %{_rpmlibdir}
%attr(755,root,root) %{_bindir}/banner.sh
%attr(755,root,root) %{_rpmlibdir}/user_group.sh
%dir /var/lib/banner

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %ghost /%{_lib}/librpm.so.10
%attr(755,root,root) /%{_lib}/librpm.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/librpmbuild.so.10
%attr(755,root,root) /%{_lib}/librpmbuild.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/librpmio.so.10
%attr(755,root,root) /%{_lib}/librpmio.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/librpmsign.so.10
%attr(755,root,root) /%{_lib}/librpmsign.so.*.*.*
%{?with_plugins:%dir %{_libdir}/rpm-plugins}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librpm.so
%attr(755,root,root) %{_libdir}/librpmbuild.so
%attr(755,root,root) %{_libdir}/librpmio.so
%attr(755,root,root) %{_libdir}/librpmsign.so
%{_includedir}/rpm
%{_pkgconfigdir}/rpm.pc
%{_libdir}/cmake/rpm

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpm2archive
%attr(755,root,root) %{_bindir}/rpm2cpio
%attr(755,root,root) %{_bindir}/rpmgraph
%attr(755,root,root) %{_rpmlibdir}/rpm2cpio.sh
%attr(755,root,root) %{_rpmlibdir}/tgpg
%attr(755,root,root) %{_rpmlibdir}/rpmdeps
%{_mandir}/man8/rpm2archive.8*
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmgraph.8*

%files build
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/noauto*
%attr(755,root,root) %{_rpmlibdir}/brp-*
%attr(755,root,root) %{_rpmlibdir}/check-files
%attr(755,root,root) %{_rpmlibdir}/install-build-tree
%attr(755,root,root) %{_rpmlibdir}/elfdeps
%attr(755,root,root) %{_rpmlibdir}/libtooldeps.sh
%attr(755,root,root) %{_rpmlibdir}/pkgconfigdeps.sh
%attr(755,root,root) %{_rpmlibdir}/fontconfig.prov
%attr(755,root,root) %{_rpmlibdir}/check-buildroot
%attr(755,root,root) %{_rpmlibdir}/check-prereqs
%attr(755,root,root) %{_rpmlibdir}/check-rpaths
%attr(755,root,root) %{_rpmlibdir}/check-rpaths-worker
%attr(755,root,root) %{_rpmlibdir}/find-provides
%attr(755,root,root) %{_rpmlibdir}/find-requires
%attr(755,root,root) %{_rpmlibdir}/ocamldeps.sh
%attr(755,root,root) %{_rpmlibdir}/rpm_macros_provides.sh
%attr(755,root,root) %{_rpmlibdir}/rpmuncompress
%attr(755,root,root) %{_rpmlibdir}/script.req
%attr(755,root,root) %{_rpmlibdir}/sysusers.sh

%dir %{_rpmlibdir}/fileattrs
%{_rpmlibdir}/fileattrs/debuginfo.attr
%{_rpmlibdir}/fileattrs/desktop.attr
%{_rpmlibdir}/fileattrs/elf.attr
%{_rpmlibdir}/fileattrs/font.attr
%{_rpmlibdir}/fileattrs/libtool.attr
%{_rpmlibdir}/fileattrs/metainfo.attr
%{_rpmlibdir}/fileattrs/ocaml.attr
%{_rpmlibdir}/fileattrs/pkgconfig.attr
%{_rpmlibdir}/fileattrs/rpm_lua.attr
%{_rpmlibdir}/fileattrs/rpm_macro.attr
%{_rpmlibdir}/fileattrs/script.attr
%{_rpmlibdir}/fileattrs/sysusers.attr
%{_rpmlibdir}/fileattrs/usergroup.attr

%attr(755,root,root) %{_bindir}/gendiff
%attr(755,root,root) %{_bindir}/rpmbuild
%attr(755,root,root) %{_bindir}/rpmlua
%attr(755,root,root) %{_bindir}/rpmspec

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmlua.8*
%{_mandir}/man8/rpmspec.8*

%if %{with python3}
%files -n python3-rpm
%defattr(644,root,root,755)
%dir %{py3_sitedir}/rpm
%attr(755,root,root) %{py3_sitedir}/rpm/*.so
%{py3_sitedir}/rpm/*.py
%{py3_sitedir}/rpm-%{version}-py*.egg-info
%{py3_sitedir}/rpm/__pycache__
%endif

%if %{with plugins}
%files plugin-audit
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.d/macros.transaction_audit
%attr(755,root,root) %{_libdir}/rpm-plugins/audit.so
%{_mandir}/man8/rpm-plugin-audit.8*

%files plugin-syslog
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.d/macros.transaction_syslog
%attr(755,root,root) %{_libdir}/rpm-plugins/syslog.so
%{_mandir}/man8/rpm-plugin-syslog.8*

%if %{with dbus}
%files plugin-systemd-inhibit
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.d/macros.transaction_systemd_inhibit
%attr(755,root,root) %{_libdir}/rpm-plugins/systemd_inhibit.so
%{_mandir}/man8/rpm-plugin-systemd-inhibit.8*
%endif

%if %{with imaevm}
%files plugin-ima
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm-plugins/ima.so
%{_mandir}/man8/rpm-plugin-ima.8*
%endif

%files plugin-prioreset
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.d/macros.transaction_prioreset
%attr(755,root,root) %{_libdir}/rpm-plugins/prioreset.so
%{_mandir}/man8/rpm-plugin-prioreset.8*

%files plugin-selinux
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.d/macros.transaction_selinux
%attr(755,root,root) %{_libdir}/rpm-plugins/selinux.so
%{_mandir}/man8/rpm-plugin-selinux.8*

%if %{with fsverity}
%files plugin-fsverity
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.d/macros.transaction_fsverity
%attr(755,root,root) %{_libdir}/rpm-plugins/fsverity.so
%endif

%files plugin-fapolicyd
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.d/macros.transaction_fapolicyd
%attr(755,root,root) %{_libdir}/rpm-plugins/fapolicyd.so
%{_mandir}/man8/rpm-plugin-fapolicyd.8*

%if %{with dbus}
%files plugin-dbus-announce
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.d/macros.transaction_dbus_announce
%attr(755,root,root) %{_libdir}/rpm-plugins/dbus_announce.so
%{_mandir}/man8/rpm-plugin-dbus-announce.8*
%{_datadir}/dbus-1/system.d/org.rpm.conf
%endif
%endif

%files plugin-unshare
%defattr(644,root,root,755)
%{_rpmlibdir}/macros.d/macros.transaction_unshare
%attr(755,root,root) %{_libdir}/rpm-plugins/unshare.so
%{_mandir}/man8/rpm-plugin-unshare.8*


%files sign
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpmsign
%{_mandir}/man8/rpmsign.8*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/*
%endif
