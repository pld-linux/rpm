#
# TODO:
# - rebuild database after upgrading from rpm5
# - when adopting, use 4.5 ticket for checklist: https://bugs.launchpad.net/pld-linux/+bug/262985
#
# Conditional build:
%bcond_without	apidocs		# don't generate documentation with doxygen
%bcond_without	python3		# don't build python bindings
%bcond_without	plugins		# build plugins
%bcond_without	recommends_tags	# build without Recommends tag (bootstrapping)
%bcond_with	imaevm		# build with IMA/EVM support (requires libimaevm from ima-evm-utils)

%define		db_ver		5.3.28.0
%define		popt_ver	1.15
%define		openssl_ver	1.1.1d
%define		sover		9.1.0

Summary:	RPM Package Manager
Summary(de.UTF-8):	RPM Packet-Manager
Summary(es.UTF-8):	Gestor de paquetes RPM
Summary(pl.UTF-8):	Aplikacja do zarządzania pakietami RPM
Summary(pt_BR.UTF-8):	Gerenciador de pacotes RPM
Summary(ru.UTF-8):	Менеджер пакетов от RPM
Summary(uk.UTF-8):	Менеджер пакетів від RPM
Name:		rpm
Version:	4.16.0
Release:	0.1
Epoch:		1
License:	GPL v2 / LGPL v2.1
Group:		Base
Source0:	http://ftp.rpm.org/releases/rpm-4.16.x/%{name}-%{version}.tar.bz2
# Source0-md5:	434e166a812e35ef181f6dd176326920
Source1:	ftp://ftp.pld-linux.org/dists/th/PLD-3.0-Th-GPG-key.asc
# Source1-md5:	23914bb49fafe7153cee87126d966461
Source2:	macros.local
Source3:	macros.lang
Source4:	%{name}.sysconfig
Source5:	%{name}.groups
Source6:	%{name}-groups-po.awk
Source7:	%{name}-install-tree
Source8:	%{name}-hrmib-cache
Source9:	%{name}-user_group.sh
# http://svn.pld-linux.org/banner.sh/
Source10:	banner.sh
Source11:	%{name}.noautoprov
Source12:	%{name}.noautoprovfiles
Source13:	%{name}.noautoreq
Source14:	%{name}.noautoreqfiles
Source15:	perl.prov
Source16:	%{name}db_checkversion.c
Source17:	%{name}db_reset.c
Source18:	dbupgrade.sh
Patch0:		%{name}-man_pl.patch
Patch1:		%{name}-popt-aliases.patch
Patch2:		%{name}-perl-macros.patch
Patch3:		%{name}-perl-req-perlfile.patch
Patch4:		%{name}-scripts-closefds.patch
Patch6:		%{name}-perl_req-INC_dirs.patch
Patch7:		%{name}-debuginfo.patch
Patch8:		%{name}-libtool-deps.patch
Patch9:		%{name}-builddir-readlink.patch
Patch10:	%{name}-changelog_order_check_nonfatal.patch
Patch11:	%{name}-postun-nofail.patch
Patch12:	%{name}-clean-docdir.patch
Patch13:	%{name}-perl-magic.patch
Patch14:	%{name}-ignore-missing-macro-files.patch
Patch15:	x32.patch
Patch16:	rpm5-db-compat.patch
Patch17:	python-internal-build.patch
Patch18:	rpmversion.patch
Patch19:	pkgconfig.patch
Patch20:	uname-deps.patch
URL:		https://rpm.org/
BuildRequires:	db-devel >= %{db_ver}
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1.4
BuildRequires:	bzip2-devel >= 1.0.2-17
BuildRequires:	elfutils-devel >= 0.108
BuildRequires:	gettext-tools >= 0.19.2
BuildRequires:	libarchive-devel
BuildRequires:	libmagic-devel
BuildRequires:	openssl-devel >= %{openssl_ver}
%if %{with plugins}
BuildRequires:	audit-libs-devel
BuildRequires:	dbus-devel
%{?with_imaevm:BuildRequires:	libimaevm-devel >= 1.0}
BuildRequires:	libselinux-devel >= 2.1.0
%endif
# needed only for AM_PROG_CXX used for CXX substitution in rpm.macros
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	lua-devel >= 5.1
BuildRequires:	ossp-uuid-devel
BuildRequires:	patch >= 2.2
BuildRequires:	popt-devel >= %{popt_ver}
BuildRequires:	python3-modules
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	rpm-pythonprov
%endif
BuildRequires:	sqlite3-devel >= 3.22.0
BuildRequires:	tcl
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	graphviz
BuildRequires:	tetex-pdftex
%endif
Requires(posttrans):	coreutils
Requires:	%{name}-base = %{epoch}:%{version}-%{release}
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}
Requires:	rpm-pld-macros >= 1.744
Requires:	FHS >= 3.0-2
Requires:	openssl >= %{openssl_ver}
Requires:	popt >= %{popt_ver}
%if %{with recommends_tags}
Recommends:	rpm-plugin-audit
Recommends:	rpm-plugin-prioreset
Recommends:	rpm-plugin-syslog
Recommends:	rpm-plugin-systemd-inhibit
%endif
Obsoletes:	rpm-utils-perl
Obsoletes:	rpm-utils-static
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
Requires:	db >= %{db_ver}
Requires:	libmagic >= 1.15-2
Requires:	openssl >= %{openssl_ver}
Requires:	popt >= %{popt_ver}
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
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}
Requires:	bzip2-devel
Requires:	db-devel >= %{db_ver}
Requires:	elfutils-devel
Requires:	libmagic-devel
Requires:	openssl-devel >= %{openssl_ver}
%if %{with selinux}
Requires:	libselinux-devel
Requires:	libsemanage-devel
Requires:	libsepol-devel
%endif
Requires:	popt-devel >= %{popt_ver}
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
Requires:	rpm-pld-macros-build >= 1.744
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

%package perlprov
Summary:	Additional utilities for checking Perl provides/requires in RPM packages
Summary(de.UTF-8):	Zusatzwerkzeuge fürs Nachsehen Perl-Abhängigkeiten in RPM-Paketen
Summary(pl.UTF-8):	Dodatkowe narzędzia do sprawdzenia zależności skryptów Perla w pakietach RPM
Group:		Applications/File
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	perl-Encode
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
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python3
Requires:	python3-modules
Requires:	python3-setuptools

%description pythonprov
Python macros, which simplifies creation of RPM packages with Python
software.

%description pythonprov -l pl.UTF-8
Makra ułatwiające tworzenie pakietów RPM z programami napisanymi w
Pythonie.

%package -n python3-rpm
Summary:	Python 3 interface to RPM library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki RPM-a
Summary(pt_BR.UTF-8):	Módulo Python 3 para aplicativos que manipulam pacotes RPM
Group:		Development/Languages/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python3
Obsoletes:	python-rpm < 1:4.16.0
Obsoletes:	rpm-python

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
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-audit
Plugin for libaudit support

%package plugin-syslog
Summary:	Plugin for syslog functionality
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-syslog
This plugin exports RPM actions to the system log.

%package plugin-systemd-inhibit
Summary:	Plugin for systemd inhibit functionality
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-systemd-inhibit
This plugin blocks systemd from entering idle, sleep or shutdown while
an rpm transaction is running using the systemd-inhibit mechanism.

%package plugin-ima
Summary:	Plugin for IMA file signatures
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-ima
This plugin adds support for enforcing and verifying IMA file
signatures in an rpm.

%package plugin-prioreset
Summary:	Plugin for resetting scriptlet priorities for SysV init
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description plugin-prioreset
This plugin is useful on legacy SysV init systems if you run rpm
transactions with nice/ionice priorities. Should not be used on
systemd systems.

%package plugin-selinux
Summary:	Plugin for SELinux functionality
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}
Requires:	libselinux >= 2.1.0

%description plugin-selinux
Plugin for SELinux functionality.

%package sign
Summary:	Package signing support
Group:		Base
Requires:	%{name}-lib = %{epoch}:%{version}-%{release}

%description sign
This package contains support for digitally signing RPM packages.

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
%setup -q -n %{name}-%{version}%{?subver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p0
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1

install %{SOURCE15} scripts/perl.prov.in

%{__mv} -f scripts/perl.req{,.in}

# generate Group translations to *.po
awk -f %{SOURCE6} %{SOURCE5}

install %{SOURCE16} tools/rpmdb_checkversion.c
install %{SOURCE17} tools/rpmdb_reset.c

%{__sed} -i -e '1s,/usr/bin/python,%{__python3},' scripts/pythondistdeps.py

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

# rpm checks for CPU type at runtime, but it looks better
sed -i \
	-e 's|@host@|%{_target_cpu}-%{_target_vendor}-%{_target_os}|' \
	-e 's|@host_cpu@|%{_target_cpu}|' \
	-e 's|@host_os@|%{_target_os}|' \
	macros.in

%configure \
	WITH_PERL_VERSION=no \
	__GST_INSPECT=%{_bindir}/gst-inspect-1.0 \
	__GPG=%{_bindir}/gpg \
%if %{with python3}
	PYTHON=python3 \
	--enable-python \
%endif
	--disable-silent-rules \
	--enable-shared \
	--enable-bdb \
	--enable-ndb \
	--enable-sqlite \
	--enable-zstd \
	--with-crypto=openssl \
	--with-lua \
	%{?with_imaevm:--with-imaevm} \
	--with-cap \
	--with-acl \
	--with-audit \
	--with-archive \
	--with-selinux=%{!?with_plugins:no}%{?with_plugins:yes} \
	%{!?with_plugins:--disable-plugins} \
	--with-vendor=pld

%{__make}

%{__cc} %{rpmcflags} tools/rpmdb_checkversion.c -o tools/rpmdb_checkversion -ldb
%{__cc} %{rpmcflags} tools/rpmdb_reset.c -o tools/rpmdb_reset -ldb

if tools/rpmdb_checkversion -V 2>&1 | grep "t match library version"; then
	echo "Error linking rpmdb tools!"
	exit 1
fi
if tools/rpmdb_reset -V 2>&1 | grep "t match library version"; then
	echo "Error linking rpmdb tools!"
	exit 1
fi

%if %{with python3}
cd python
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/%{_lib},/etc/sysconfig,%{_sysconfdir}/{rpm,pki/rpm-gpg}} \
	$RPM_BUILD_ROOT{/var/lib/{banner,rpm},/var/cache/hrmib}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/PLD-3.0-Th-GPG-key.asc

%{__make} install \
	pkgconfigdir=%{_pkgconfigdir} \
	DESTDIR=$RPM_BUILD_ROOT

# cleanup
%ifnarch %{ix86} %{x8664} x32
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/athlon-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/geode-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/i386-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/i486-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/i586-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/i686-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/pentium3-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/pentium4-linux/macros
%endif

%ifnarch %{x8664} x32
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/amd64-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ia32e-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/x32-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/x86_64-linux/macros
%endif

%ifnarch %{ppc}
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/m68k-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc32dy4-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc64*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc8260-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc8560-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ppc*series-linux/macros
%endif

rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/aarch64-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/alpha*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/arm*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/ia64-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/mips*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/riscv64-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/s390*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/sh*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/platform/sparc*-linux/macros

%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/find-lang.sh

install -d $RPM_BUILD_ROOT%{_rpmlibdir}/pld

cp -p %{SOURCE7} $RPM_BUILD_ROOT%{_rpmlibdir}/install-build-tree
cp -p %{SOURCE9} $RPM_BUILD_ROOT%{_rpmlibdir}/user_group.sh
cp -p %{SOURCE8} $RPM_BUILD_ROOT%{_rpmlibdir}/hrmib-cache
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/rpm

cp -p %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/banner.sh

cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.lang
cp -p %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprov
cp -p %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprovfiles
cp -p %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreq
cp -p %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreqfiles

cp -p tools/rpmdb_checkversion $RPM_BUILD_ROOT%{_rpmlibdir}/
cp -p tools/rpmdb_reset $RPM_BUILD_ROOT%{_rpmlibdir}/
cp -p %{SOURCE18} $RPM_BUILD_ROOT%{_rpmlibdir}/dbupgrade.sh

# move rpm to /bin
%{__mv} $RPM_BUILD_ROOT%{_bindir}/rpm $RPM_BUILD_ROOT/bin
ln -sf /bin/rpm $RPM_BUILD_ROOT%{_bindir}/rpmquery
ln -sf /bin/rpm $RPM_BUILD_ROOT%{_bindir}/rpmverify

# move essential libs to /lib (libs that /bin/rpm links to)
for a in librpm.so librpmbuild.so librpmio.so librpmsign.so; do
	mv -f $RPM_BUILD_ROOT%{_libdir}/${a}.* $RPM_BUILD_ROOT/%{_lib}
	ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/${a}.*.*.*) $RPM_BUILD_ROOT%{_libdir}/${a}
done

#./rpmdb --macros=macros --rcfile=rpmrc --dbpath=/home/users/baggins/devel/PLD/rpm/BUILD/rpm-4.15.1/x/ --initdb

# Make sure we have bdb set a default backend
grep -qE "db_backend[[:blank:]]+bdb" $RPM_BUILD_ROOT%{_rpmlibdir}/macros

%if %{with python3}
# Remove anything that rpm make install might put there
%{__rm} -rf $RPM_BUILD_ROOT%{py3_sitedir}
cd python
%py3_install
cd ..
%endif

%{__rm} $RPM_BUILD_ROOT%{_libdir}/rpm-plugins/*.la

# wrong location, not used anyway
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/rpm.{daily,log}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%posttrans
if [ -e /var/lib/rpm/Packages ] && \
		! %{_rpmlibdir}/rpmdb_checkversion -h /var/lib/rpm -d /var/lib/rpm; then
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
	%{_rpmlibdir}/dbupgrade.sh
fi

%triggerpostun -- %{name} < 4.4.9-44
%{_rpmlibdir}/hrmib-cache

%post	lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%pretrans build
find %{_rpmlibdir} -name '*-linux' -type l | xargs rm -f

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog CREDITS README

%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/PLD-3.0-Th-GPG-key.asc

%attr(755,root,root) /bin/rpm
%attr(755,root,root) %{_bindir}/rpmdb
%attr(755,root,root) %{_bindir}/rpmkeys
%attr(755,root,root) %{_bindir}/rpmquery
%attr(755,root,root) %{_bindir}/rpmverify

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/macros
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/macros.lang

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm-misc.8*
%{?with_plugins:%{_mandir}/man8/rpm-plugins.8*}
%lang(fr) %{_mandir}/fr/man8/rpm.8*
%lang(ja) %{_mandir}/ja/man8/rpm.8*
%lang(ko) %{_mandir}/ko/man8/rpm.8*
%lang(pl) %{_mandir}/pl/man8/rpm.8*
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%lang(sk) %{_mandir}/sk/man8/rpm.8*

%dir /var/lib/rpm

# exported package NVRA (stamped with install tid)
# net-snmp hrSWInstalledName queries, bash-completions
%dir /var/cache/hrmib

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

%attr(755,root,root) %{_rpmlibdir}/hrmib-cache

%attr(755,root,root) %{_rpmlibdir}/dbupgrade.sh
%attr(755,root,root) %{_rpmlibdir}/rpmdb_checkversion
%attr(755,root,root) %{_rpmlibdir}/rpmdb_reset
%attr(755,root,root) %{_rpmlibdir}/rpmdb_dump
%attr(755,root,root) %{_rpmlibdir}/rpmdb_load

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
%attr(755,root,root) /%{_lib}/librpm.so.9
%attr(755,root,root) /%{_lib}/librpm.so.%{sover}
%attr(755,root,root) /%{_lib}/librpmbuild.so.9
%attr(755,root,root) /%{_lib}/librpmbuild.so.%{sover}
%attr(755,root,root) /%{_lib}/librpmio.so.9
%attr(755,root,root) /%{_lib}/librpmio.so.%{sover}
%attr(755,root,root) /%{_lib}/librpmsign.so.9
%attr(755,root,root) /%{_lib}/librpmsign.so.%{sover}
%{?with_plugins:%dir %{_libdir}/rpm-plugins}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librpm.so
%attr(755,root,root) %{_libdir}/librpmbuild.so
%attr(755,root,root) %{_libdir}/librpmio.so
%attr(755,root,root) %{_libdir}/librpmsign.so
%{_libdir}/librpm*.la
%{_includedir}/rpm
%{_pkgconfigdir}/*.pc

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpm2archive
%attr(755,root,root) %{_bindir}/rpm2cpio
%attr(755,root,root) %{_bindir}/rpmgraph
%attr(755,root,root) %{_rpmlibdir}/rpm2cpio.sh
%attr(755,root,root) %{_rpmlibdir}/find-debuginfo.sh
%attr(755,root,root) %{_rpmlibdir}/tgpg
%attr(755,root,root) %{_rpmlibdir}/debugedit
%attr(755,root,root) %{_rpmlibdir}/rpmdeps
%{_mandir}/man8/rpm2archive.8*
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmgraph.8*
%lang(ja) %{_mandir}/ja/man8/rpm2cpio.8*
%lang(ko) %{_mandir}/ko/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpm2cpio.8*
%lang(ru) %{_mandir}/ru/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpmdeps.8*
%lang(ja) %{_mandir}/ja/man8/rpmgraph.8*
%lang(pl) %{_mandir}/pl/man8/rpmgraph.8*

%files build
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/noauto*
%attr(755,root,root) %{_rpmlibdir}/brp-*
%attr(755,root,root) %{_rpmlibdir}/check-files
%attr(755,root,root) %{_rpmlibdir}/install-build-tree
%attr(755,root,root) %{_rpmlibdir}/elfdeps
%attr(755,root,root) %{_rpmlibdir}/libtooldeps.sh
# needs hacked pkg-config to return anything
%attr(755,root,root) %{_rpmlibdir}/pkgconfigdeps.sh
%attr(755,root,root) %{_rpmlibdir}/mkinstalldirs

%attr(755,root,root) %{_rpmlibdir}/fontconfig.prov
# must be here for "Requires: rpm-*prov" to work
#%{_rpmlibdir}/macros.d/cmake
#%{_rpmlibdir}/macros.d/gstreamer
#%{_rpmlibdir}/macros.d/libtool
#%{_rpmlibdir}/macros.d/perl
#%{_rpmlibdir}/macros.d/pkgconfig
#%{_rpmlibdir}/macros.d/python
#%{_rpmlibdir}/macros.d/selinux
#%{_rpmlibdir}/macros.d/tcl
#%{_rpmlibdir}/macros.rpmbuild

%attr(755,root,root) %{_rpmlibdir}/check-buildroot
%attr(755,root,root) %{_rpmlibdir}/check-prereqs
%attr(755,root,root) %{_rpmlibdir}/check-rpaths
%attr(755,root,root) %{_rpmlibdir}/check-rpaths-worker
%attr(755,root,root) %{_rpmlibdir}/find-provides
%attr(755,root,root) %{_rpmlibdir}/find-requires
%attr(755,root,root) %{_rpmlibdir}/ocamldeps.sh
%attr(755,root,root) %{_rpmlibdir}/script.req
%attr(755,root,root) %{_rpmlibdir}/sepdebugcrcfix

%dir %{_rpmlibdir}/fileattrs
%{_rpmlibdir}/fileattrs/debuginfo.attr
%{_rpmlibdir}/fileattrs/desktop.attr
%{_rpmlibdir}/fileattrs/elf.attr
%{_rpmlibdir}/fileattrs/font.attr
%{_rpmlibdir}/fileattrs/libtool.attr
%{_rpmlibdir}/fileattrs/metainfo.attr
%{_rpmlibdir}/fileattrs/ocaml.attr
%{_rpmlibdir}/fileattrs/perl.attr
%{_rpmlibdir}/fileattrs/perllib.attr
%{_rpmlibdir}/fileattrs/pkgconfig.attr
%{_rpmlibdir}/fileattrs/python.attr
%{_rpmlibdir}/fileattrs/pythondist.attr
%{_rpmlibdir}/fileattrs/script.attr

%attr(755,root,root) %{_bindir}/gendiff
%attr(755,root,root) %{_bindir}/rpmbuild
%attr(755,root,root) %{_bindir}/rpmspec

%{_mandir}/man1/gendiff.1*
%lang(pl) %{_mandir}/pl/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%lang(ja) %{_mandir}/ja/man8/rpmbuild.8*
%lang(pl) %{_mandir}/pl/man8/rpmbuild.8*
%{_mandir}/man8/rpmspec.8*

%files perlprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/perl.*

%files pythonprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/pythondistdeps.py

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
%attr(755,root,root) %{_libdir}/rpm-plugins/audit.so
%{_mandir}/man8/rpm-plugin-audit.8*

%files plugin-syslog
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm-plugins/syslog.so
%{_mandir}/man8/rpm-plugin-syslog.8*

%files plugin-systemd-inhibit
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm-plugins/systemd_inhibit.so
%{_mandir}/man8/rpm-plugin-systemd-inhibit.8*

%files plugin-ima
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm-plugins/ima.so
%{_mandir}/man8/rpm-plugin-ima.8*

%files plugin-prioreset
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm-plugins/prioreset.so
%{_mandir}/man8/rpm-plugin-prioreset.8*

%files plugin-selinux
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rpm-plugins/selinux.so
%{_mandir}/man8/rpm-plugin-selinux.8*
%endif

%files sign
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpmsign
%{_mandir}/man8/rpmsign.8*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/librpm/html/*
%endif
