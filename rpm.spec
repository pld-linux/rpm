#
# TODO:
# pluto_> btw. /usr/lib/rpm/find-debuginfo.sh needs fix. it extract debuginfo also from kernel modules.
# pluto_> there's a filelist=$(find $RPM_BUILD_ROOT ! -path "$RPM_BUILD_ROOT/usr/lib/debug/*.debug" -type f
# pluto_> and we need to add ! -path /lib/modules/...
# - python(abi) cap is not provided automatically because /usr/lib*/libpython2*.so.*
#   matches ELF first
# - repackaging when lzma is not installed (todo: fix digest signature of header)
#   rpmbuild computes digest when writing package to temporary file, then adds a few
#   tags (incl. digest) and writes whole package to destination file;
#   repackaging uses unchanged "immutable header" image from original rpm, also
#   preserving payload format and compressor from original rpm, _not_ current settings
#   /usr/bin/install: cannot stat `./it.gmo': No such file or directory
#   /usr/bin/install: cannot stat `./sr@Latn.gmo': No such file or directory
# - maybe? http://rpm.org/gitweb?p=rpm.git;a=commitdiff;h=cfcd1f9bd98d5d0fc46a84931984efec3b9d47e2
#
# Conditional build:
%bcond_with	static		# build static rpm+rpmi
%bcond_without	apidocs		# don't generate documentation with doxygen
%bcond_with		internal_db		# internal db (db 4.5.20)
%if "%{pld_release}" == "ac"
%bcond_without	autoreqdep	# autogenerate package name deps in addition to sonames/perl(X)
%bcond_with		nptl			# internal db: don't use process-shared POSIX mutexes (NPTL provides full interface)
%else
%bcond_with		autoreqdep	# autogenerate package name deps in addition to sonames/perl(X)
%bcond_without	nptl			# internal db: don't use process-shared POSIX mutexes (NPTL provides full interface)
%endif
%bcond_without	python		# don't build python bindings
%bcond_without	selinux		# build without selinux support
%bcond_without	system_libmagic	# don't use system libmagic
%bcond_without	suggest_tags	# build without Suggest tag (bootstrapping)
%bcond_with	neon		# build with HTTP/WebDAV support (neon library). NOTE: neon libs are in /usr!
# force_cc		- force using __cc other than "%{_target_cpu}-pld-linux-gcc"
# force_cxx		- force using __cxx other than "%{_target_cpu}-pld-linux-g++"
# force_cpp		- force using __cpp other than "%{_target_cpu}-pld-linux-gcc -E"

%ifarch sparc sparcv9 sparc64
%undefine with_apidocs
%endif

# versions of required libraries
%if "%{pld_release}" == "th"
%define	reqdb_ver	4.7.25
%else
%define	reqdb_ver	4.5.20
%endif
%define	reqpopt_ver	1.10.8
%define	beecrypt_ver	2:4.1.2-4
%define	sover		4.5
Summary:	RPM Package Manager
Summary(de.UTF-8):	RPM Packet-Manager
Summary(es.UTF-8):	Gestor de paquetes RPM
Summary(pl.UTF-8):	Aplikacja do zarządzania pakietami RPM
Summary(pt_BR.UTF-8):	Gerenciador de pacotes RPM
Summary(ru.UTF-8):	Менеджер пакетов от RPM
Summary(uk.UTF-8):	Менеджер пакетів від RPM
Name:		rpm
Version:	4.5
Release:	42
License:	LGPL
Group:		Base
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	6b4cda21de59dc250d2e33e4187fd166
Source1:	%{name}.groups
Source2:	%{name}.platform
Source3:	%{name}-install-tree
Source4:	%{name}-find-spec-bcond
Source5:	%{name}-hrmib-cache
Source6:	%{name}-groups-po.awk
Source7:	%{name}-compress-doc
Source8:	ftp://ftp.pld-linux.org/dists/th/PLD-3.0-Th-GPG-key.asc
# Source8-md5:	08b29584dd349aac9caa7610131a0a88
Source9:	ftp://ftp.pld-linux.org/dists/ac/PLD-2.0-Ac-GPG-key.asc
# Source9-md5:	8e7574d1de2fa95c2c54cd2ee03364c1
Source10:	%{name}-php-provides
Source11:	%{name}-php-requires
Source12:	%{name}.sysinfo
Source13:	perl.prov
Source14:	%{name}-user_group.sh
Source15:	%{name}.sysconfig
Source16:	%{name}-macros.java
Source17:	%{name}-java-requires
# http://svn.pld-linux.org/banner.sh/
Source18:	banner.sh
Source19:	%{name}-macros.gstreamer
Patch1000:	%{name}-new-debuginfo.patch
Patch1067:	%{name}-disable-features.patch
Patch1070:	%{name}-rpmrc-ac.patch
#Patch0:	%{name}-pl.po.patch
Patch1:		%{name}-rpmrc.patch
Patch2:		%{name}-arch.patch
Patch3:		%{name}-rpmpopt.patch
Patch4:		%{name}-perl-macros.patch
Patch6:		%{name}-noexpand.patch
Patch7:		%{name}-scripts-closefds.patch
Patch8:		%{name}-db.patch
Patch9:		%{name}-gettext-in-header.patch
Patch10:	%{name}-compress-doc.patch
Patch11:	%{name}-rpm5-patchset-8074.patch
Patch12:	%{name}-system_libs.patch
Patch13:	%{name}-unglobal.patch
Patch14:	%{name}-etc_dir.patch
Patch15:	%{name}-system_libs-more.patch
Patch17:	%{name}-ldconfig-always.patch
Patch18:	%{name}-macros-ac.patch
Patch19:	%{name}-macros-th.patch
Patch20:	%{name}-macros-ti.patch
Patch21:	%{name}-perl_req-skip_multiline.patch
Patch22:	%{name}-provides-dont-obsolete.patch
Patch23:	%{name}-pkgconfigdeps.patch
Patch24:	%{name}-po.patch
Patch25:	%{name}-link.patch
Patch26:	%{name}-notsc.patch
Patch27:	%{name}-hack-norpmlibdep.patch
Patch28:	%{name}-makefile-no_myLDADD_deps.patch
Patch29:	%{name}-perl_req-use_base.patch
Patch31:	%{name}-missing-prototypes.patch
Patch32:	%{name}-pld-autodep.patch
Patch33:	%{name}-arch-x86_64.patch
Patch34:	%{name}-epoch0.patch
Patch35:	%{name}-disable-features-ti.patch
Patch36:	%{name}-debuginfo.patch
Patch37:	%{name}-doxygen_hack.patch
Patch39:	%{name}-popt-coreutils.patch
Patch42:	%{name}-old-fileconflicts-behaviour.patch
Patch43:	%{name}-rpm5-patchset-8637.patch
Patch44:	%{name}-no-neon.patch
Patch45:	%{name}-no-sqlite.patch
Patch48:	%{name}-nopie.patch
Patch50:	%{name}-macros.patch
Patch51:	%{name}-cleanlibdirs.patch
Patch52:	%{name}-morearchs.patch
Patch53:	%{name}-chroot-hack.patch
Patch55:	%{name}-truncate-cvslog.patch
Patch56:	%{name}-rpm5-patchset-8413.patch
Patch57:	%{name}-as_needed-fix.patch
Patch58:	%{name}-repackage-wo-lzma.patch
Patch59:	%{name}-libtool-deps.patch
Patch61:	%{name}-lzma-mem.patch
Patch62:	%{name}-lzma-size_t.patch
Patch63:	%{name}-tar_as_secondary_source.patch
Patch64:	%{name}-man_pl.patch
Patch65:	%{name}-lzma-tukaani.patch
Patch66:	%{name}-v3-support.patch
Patch67:	%{name}-cleanbody.patch
Patch69:	%{name}-popt-aliases.patch
# reverse arrows patch
Patch70:	%{name}-rpm5-patchset-10061.patch
Patch71:	%{name}-installbeforeerase.patch
Patch72:	%{name}-postun-nofail.patch
Patch73:	%{name}-namespace-probe.patch
Patch74:	%{name}-noversiondir.patch
Patch75:	%{name}-rpmte-segv.patch
Patch76:	%{name}-pydebuginfo.patch
Patch77:	%{name}-dirdeps-macro.patch
Patch78:	%{name}-db3-configure.patch
Patch79:	%{name}-macros-cpp.patch
Patch80:	%{name}-link-selinux.patch
Patch81:	%{name}-db-configure.patch
Patch82:	%{name}-perl-makefile.patch
Patch83:	%{name}-nosmpflags.patch
Patch84:	%{name}-hirmib-ts.patch
Patch85:	%{name}-perl_req-heredocs_pod.patch
Patch86:	%{name}-rpmv3-support.patch
Patch87:	%{name}-mono.patch
Patch88:	%{name}-poptexecpath.patch
Patch89:	%{name}-lzma-compress-level.patch
Patch90:	%{name}-gstreamer.patch
Patch91:	%{name}-gendiff.patch
Patch92:	%{name}-set-failed-on-reopen.patch
Patch93:	%{name}-debugedit-workaround.patch
Patch94:	%{name}-shescape-memfault.patch
Patch95:	%{name}-gid-uucp.patch
Patch96:	%{name}-disable-hkp.patch
Patch97:	%{name}-sigpad.patch
Patch98:	%{name}-debugdir.patch
Patch99:	%{name}-pkgconfig.patch
Patch100:	%{name}-rpm5-debugedit.patch
Patch101:	%{name}-builddir-readlink.patch
Patch102:	pythondeps-speedup.patch
Patch103:	%{name}-lua-exit-chroot-correctly.patch
URL:		http://rpm5.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1.4
BuildRequires:	beecrypt-devel >= %{beecrypt_ver}
BuildRequires:	bzip2-devel >= 1.0.2-17
%{!?with_internal_db:BuildRequires:	db-devel >= %{reqdb_ver}}
BuildRequires:	elfutils-devel >= 0.108
BuildRequires:	gettext-devel >= 0.11.4-2
BuildRequires:	keyutils-devel
%{?with_system_libmagic:BuildRequires:	libmagic-devel}
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.18}
# needed only for AM_PROG_CXX used for CXX substitution in rpm.macros
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
%if %{with neon}
BuildRequires:	libxml2-devel
BuildRequires:	neon-devel >= 0.25.5
%endif
BuildRequires:	ossp-uuid-devel >= 1.6.2-6
BuildRequires:	patch >= 2.2
BuildRequires:	popt-devel >= %{reqpopt_ver}
%{?with_python:BuildRequires:	python-devel >= 1:2.3}
BuildRequires:	python-modules >= 1:2.3
BuildRequires:	rpm-perlprov
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 1.351
BuildRequires:	tar >= 1:1.15.1
BuildRequires:	zlib-devel >= 1.2.3.3
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
%{!?with_internal_db:BuildRequires:	db-static >= %{reqdb_ver}}
BuildRequires:	elfutils-static
BuildRequires:	glibc-static >= 2.2.94
%{?with_system_libmagic:BuildRequires:	libmagic-static}
%{?with_selinux:BuildRequires:	libselinux-static >= 1.18}
BuildRequires:	popt-static >= %{reqpopt_ver}
BuildRequires:	zlib-static >= 1.2.3.3
%endif
Requires:	%{name}-base = %{version}-%{release}
Requires:	%{name}-lib = %{version}-%{release}
Requires:	beecrypt >= %{beecrypt_ver}
Requires:	popt >= %{reqpopt_ver}
Provides:	rpm-db-ver = %{reqdb_ver}
Obsoletes:	rpm-getdeps
%{!?with_static:Obsoletes:	rpm-utils-static}
Obsoletes:	tmpwatch-rpmrepackage
Conflicts:	glibc < 2.2.92
Conflicts:	poldek < 0.21-0.20070703.00.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_binary_payload		w9.gzdio
%define		_noPayloadPrefix	1

# don't require very fresh rpm.macros to build
%define		__gettextize gettextize --copy --force --no-changelog; [ -f po/Makevars ] || cp -f po/Makevars{.template,}
%define		find_lang sh ./scripts/find-lang.sh $RPM_BUILD_ROOT
%define		ix86	i386 i486 i586 i686 athlon pentium3 pentium4
%define		ppc	ppc ppc7400 ppc7450
%define		x8664	amd64 ia32e x86_64

# stabilize new build environment
%define		__newcc %{?force_cc}%{!?force_cc:%{_target_cpu}-pld-linux-gcc}
%define		__newcxx %{?force_cxx}%{!?force_cxx:%{_target_cpu}-pld-linux-g++}
%define		__newcpp %{?force_cpp}%{!?force_cpp:%{_target_cpu}-pld-linux-gcc -E}

%define		_rpmlibdir /usr/lib/rpm

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
%{!?with_internal_db:Requires:	db >= %{reqdb_ver}}
%{?with_system_libmagic:Requires:	libmagic >= 1.15-2}
%{?with_selinux:Requires:	libselinux >= 1.18}
Requires:	ossp-uuid >= 1.6.2-4
Requires:	popt >= %{reqpopt_ver}
%{?with_internal_db:%{?with_nptl:Requires:	uname(release) >= 2.6.0}}
Requires:	zlib >= 1.2.3.3
%{?with_suggest_tags:Suggests:	xz}
Obsoletes:	rpm-libs
# avoid installing with incompatible (non-tukaani) lzma
# avoid incompatible (-M0 not supported) lzma
Conflicts:	lzma < 1:4.999.5-0.alpha.2
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
%{!?with_internal_db:Requires:	db-devel >= %{reqdb_ver}}
Requires:	elfutils-devel
Requires:	keyutils-devel
%{?with_system_libmagic:Requires:	libmagic-devel}
%{?with_selinux:Requires:	libselinux-devel}
Requires:	popt-devel >= %{reqpopt_ver}
Requires:	zlib-devel >= 1.2.3.3

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
%{!?with_internal_db:Requires:	db-static >= %{reqdb_ver}}
Requires:	elfutils-static
Requires:	keyutils-static
%{?with_system_libmagic:Requires:	libmagic-static}
Requires:	popt-static >= %{reqpopt_ver}
Requires:	zlib-static >= 1.2.3.3

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
%if "%{pld_release}" == "ac"
Conflicts:	filesystem-debuginfo < 2.0-7
%else
Conflicts:	filesystem-debuginfo < 3.0-16
%endif

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
Requires(pretrans):	findutils
Requires:	%{name}-build-macros >= 1.514
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
%if "%{pld_release}" == "ac"
%ifarch athlon
Requires:	gcc >= 3.0.3
%else
Requires:	gcc
%endif
%else
# rpmrc patch adds flags specific to gcc >= 3.4
Requires:	gcc >= 5:3.4
%endif
Requires:	glibc-devel
Requires:	grep
Requires:	gzip
Requires:	xz
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
%setup -q
%patch1000 -p1
#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1 -R
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch17 -p1
sed -e 's/^/@pld@/' %{SOURCE2} >>platform.in
echo '%%define	__perl_provides	%%{__perl} /usr/lib/rpm/perl.prov' > macros.perl
echo '%%define	__perl_requires	%%{__perl} /usr/lib/rpm/perl.req' >> macros.perl
echo '# obsoleted file' > macros.python
echo '%%define	__php_provides	/usr/lib/rpm/php.prov' > macros.php
echo '%%define	__php_requires	/usr/lib/rpm/php.req' >> macros.php
echo '%%define	__mono_provides	/usr/lib/rpm/mono-find-provides' > macros.mono
echo '%%define	__mono_requires	/usr/lib/rpm/mono-find-requires' >> macros.mono
install %{SOURCE10} scripts/php.prov
install %{SOURCE11} scripts/php.req
install %{SOURCE13} scripts/perl.prov
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch36 -p1
%patch37 -p1
%patch39 -p1
%patch42 -p1
%patch43 -p1
%patch82 -p1
%{!?with_neon:%patch44 -p1}
%patch45 -p1
%patch48 -p1
%patch50 -p1
%if "%{pld_release}" == "ac"
%patch18 -p1
%endif
%if "%{pld_release}" == "th"
%patch19 -p1
%endif
%if "%{pld_release}" == "ti"
%patch20 -p1
%patch35 -p1
%endif
%patch51 -p1
#%patch52 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch69 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p0
# having .py sources in -debuginfo needs more testing
#%patch76 -p1
%patch77 -p0
%patch79 -p1
%patch80 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch70 -p0
%patch87 -p1
%patch88 -p1
%patch89 -p1
%patch90 -p1
%patch91 -p1
%patch92 -p1
%patch93 -p1
%patch94 -p1
%patch95 -p1
%patch96 -p1
%patch97 -p1
%patch98 -p1
%patch99 -p1
%patch53 -p1
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1

mv -f po/{sr,sr@Latn}.po
rm -rf sqlite zlib popt

%if %{with internal_db}
%if %{without nptl}
sed -i -e 's,AM_PTHREADS_SHARED("POSIX/.*,:,' db/dist/aclocal/mutex.ac
%endif
%patch78 -p1
%patch81 -p1
%else
%patch15 -p1
rm -rf db3 db rpmdb/db.h
%endif

%if "%{pld_release}" == "ac"
%patch1067 -p1
%patch1070 -p1
%endif

# generate Group translations to *.po
awk -f %{SOURCE6} %{SOURCE1}

# update macros paths
for f in doc{,/ja,/pl}/rpm.8 doc{,/ja,/pl}/rpmbuild.8 ; do
	sed -e 's@lib/rpm/redhat@lib/rpm/pld@g' $f > ${f}.tmp
	mv -f ${f}.tmp $f
done

%build
%if %{with system_libmagic}
rm -rf file
%else
cd file
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd ..
%endif

%{__libtoolize}
%{__gettextize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%if %{with internal_db}
cd db3
echo -e 'AC_CONFIG_AUX_DIR(.)\nAC_PROG_LIBTOOL'> configure.ac
%{__libtoolize}
rm -f configure.ac
cd ../db
cp -f /usr/share/aclocal/libtool.m4 dist/aclocal/libtool.ac
cp -f /usr/share/automake/config.sub dist
if [ -f /usr/share/libtool/config/ltmain.sh ]; then
	cp -f /usr/share/libtool/config/ltmain.sh dist
else
	cp -f /usr/share/libtool/ltmain.sh dist
fi
cd ..
%endif

# rpm checks for CPU type at runtime, but it looks better
sed -i \
	-e 's|@host@|%{_target_cpu}-%{_target_vendor}-%{_target_os}|' \
	-e 's|@host_cpu@|%{_target_cpu}|' \
	-e 's|@host_os@|%{_target_os}|' \
	macros.in

# pass CC and CXX too in case of building with some older configure macro
# disable perl-RPM2 build, we have it in separate spec
CPPFLAGS=-I/usr/include/oosp-uuid
%configure \
	CC="%{__newcc}" \
	CXX="%{__newcxx}" \
	CPP="%{__newcpp}" \
	WITH_PERL_VERSION=no \
	%{?with_autoreqdep:--enable-adding-packages-names-in-autogenerated-dependancies} \
	--enable-shared \
	--enable-static \
	%{!?with_apidocs:--without-apidocs} \
	%{?with_python:--with-python=%{py_ver}} \
	%{!?with_python:--without-python} \
	%{!?with_selinux:--without-selinux} \
	%{?with_internal_db:--%{?with_nptl:en}%{!?with_nptl:dis}able-posixmutexes} \
	--without-db

%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CPP="%{__cpp}" \
	libdb_la=%{_libdir}/libdb.la \
	pylibdir=%{py_libdir} \
	myLDFLAGS="%{rpmldflags}" \
	staticLDFLAGS=%{?with_static:-all-static}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib},/etc/{sysconfig,tmpwatch},%{_sysconfdir}/rpm,/var/lib/banner,/var/cache/hrmib}

%if "%{pld_release}" != "ti"
install -d $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install %{SOURCE8} $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install %{SOURCE9} $RPM_BUILD_ROOT/etc/pki/rpm-gpg
%endif

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	staticLDFLAGS=%{?with_static:-all-static} \
	pylibdir=%{py_libdir} \
	pkgbindir="%{_bindir}"

cat <<'EOF' > $RPM_BUILD_ROOT/etc/tmpwatch/rpm.conf
# Cleanup 90-days old repackage files.
/var/spool/repackage 2160
EOF

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/platform
# first platform file entry can't contain regexps
%{_target_cpu}-%{_target_vendor}-linux

%ifarch x86_64
# x86_64 things
amd64-[^-]*-[Ll]inux(-gnu)?
x86_64-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch amd64
amd64-[^-]*-[Ll]inux(-gnu)?
x86_64-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch ia32e
ia32e-[^-]*-[Ll]inux(-gnu)?
x86_64-[^-]*-[Ll]inux(-gnu)?
%endif

%ifarch athlon %{x8664}
# x86 things
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
%ifarch ppc ppc64
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

rm $RPM_BUILD_ROOT%{_rpmlibdir}/vpkg-provides*
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-{prov,req}.pl
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-{provides,requires}.perl
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-lang.sh

# not installed since 4.4.8 (-tools-perl subpackage)
install -p scripts/rpmdiff scripts/rpmdiff.cgi $RPM_BUILD_ROOT%{_rpmlibdir}

cp -a macros.perl	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.perl
cp -a macros.python	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.python
cp -a macros.php	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.php
cp -a macros.mono	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.mono
cp -a %{SOURCE16}	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.java
cp -a %{SOURCE19}	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.gstreamer

install -p %{SOURCE3} $RPM_BUILD_ROOT%{_rpmlibdir}/install-build-tree
install -p %{SOURCE4} $RPM_BUILD_ROOT%{_rpmlibdir}/find-spec-bcond
install -p %{SOURCE7} $RPM_BUILD_ROOT%{_rpmlibdir}/compress-doc
install -p %{SOURCE14} $RPM_BUILD_ROOT%{_rpmlibdir}/user_group.sh
install -p %{SOURCE17} $RPM_BUILD_ROOT%{_rpmlibdir}/java-find-requires
install -p scripts/php.{prov,req}	$RPM_BUILD_ROOT%{_rpmlibdir}
install -p %{SOURCE5} $RPM_BUILD_ROOT%{_rpmlibdir}/hrmib-cache
install -p %{SOURCE18} $RPM_BUILD_ROOT%{_bindir}/banner.sh
cp -a %{SOURCE15} $RPM_BUILD_ROOT/etc/sysconfig/rpm

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Conflictname
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Dirnames
cp -a %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Filelinktos
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Obsoletename
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Providename
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Requirename

cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros <<EOF
# customized rpm macros - global for host
#
%if "%{pld_release}" == "ti"
%%distribution PLD Titanium
%else
%%distribution PLD
%endif
#
# remove or replace with file_contexts path if you want to use custom
# SELinux file contexts policy instead of one stored in packages payload
%%_install_file_context_path	%%{nil}
%%_verify_file_context_path	%%{nil}

# If non-zero, all erasures will be automagically repackaged.
#%%_repackage_all_erasures	0

# If non-zero, create debuginfo packages
#%%_enable_debug_packages	0

# Boolean (i.e. 1 == "yes", 0 == "no") that controls whether files
# marked as %doc should be installed.
#%%_excludedocs   1
EOF

cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.lang <<EOF
# Customized rpm macros - global for host
#	A colon separated list of desired locales to be installed;
#	"all" means install all locale specific files.
#
#%%_install_langs pl_PL:en_US
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
install -d $RPM_BUILD_ROOT/bin
mv $RPM_BUILD_ROOT%{_bindir}/rpm $RPM_BUILD_ROOT/bin
# move essential libs to /lib (libs that /bin/rpm links to)
for a in librpm-%{sover}.so librpmdb-%{sover}.so librpmio-%{sover}.so ; do
	mv -f $RPM_BUILD_ROOT%{_libdir}/$a $RPM_BUILD_ROOT/%{_lib}
	ln -s /%{_lib}/$a $RPM_BUILD_ROOT%{_libdir}/$a
done

# remove arch dependant macros which have no use on noarch
%{__sed} -i -e '
/{__spec_install_post_strip}/d
/{__spec_install_post_chrpath}/d
/{__spec_install_post_compress_modules}/d
' $RPM_BUILD_ROOT%{_rpmlibdir}/noarch-linux/macros

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/rpm/*.{la,a,py}

# (currently) not used or supported in PLD
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/{http.req,perldeps.pl}
# wrong location, not used anyway
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/rpm.{daily,log,xinetd}

# unpackaged in 4.4.9, reasons unknown
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/symclash.{sh,py}
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/RPM.pm
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/RPM/.packlist
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/RPM/RPM.bs
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/RPM/RPM.so
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/RPM.3pm
%{__rm} $RPM_BUILD_ROOT%{_mandir}/{,ja,pl}/man8/rpm{cache,graph}.8

%find_lang %{name}

rm -rf manual
cp -a doc/manual manual
cp -a %{SOURCE1} manual/groups
rm -f manual/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun lib -- %{name}-lib < %{version}
echo >&2 "rpm-lib upgrade: Removing /var/lib/rpm/__db* from older rpmdb version"
rm -f /var/lib/rpm/__db*
if [ -d /vservers ]; then
	echo >&2 "rpm-lib upgrade: Removing vservers apps/pkgmgmt/base/rpm/state/__* from older rpmdb version"
	rm -f /etc/vservers/*/apps/pkgmgmt/base/rpm/state/__*
fi
echo >&2 "You should rebuild your rpmdb: rpm --rebuilddb to avoid random rpmdb errors"

%triggerpostun lib -- db4.5 < %{reqdb_ver}
echo >&2 "db4.5 upgrade: Removing /var/lib/rpm/__db* from older rpmdb version"
rm -f /var/lib/rpm/__db*
if [ -d /vservers ]; then
	echo >&2 "db4.5 upgrade: Removing vservers apps/pkgmgmt/base/rpm/state/__* from older rpmdb version"
	rm -f /etc/vservers/*/apps/pkgmgmt/base/rpm/state/__*
fi
echo >&2 "You should rebuild your rpmdb: rpm --rebuilddb to avoid random rpmdb errors"

%triggerpostun -- %{name} < 4.4.9-44
%{_rpmlibdir}/hrmib-cache

%post	lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%pretrans build
find %{_rpmlibdir} -name '*-linux' -type l | xargs rm -f

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES CREDITS README manual/*

%if "%{pld_release}" != "ti"
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*.asc
%endif

%attr(755,root,root) /bin/rpm

%config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/rpm.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/macros
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/macros.lang
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

%attr(755,root,root) %{_rpmlibdir}/hrmib-cache

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
%attr(755,root,root) /%{_lib}/librpm-%{sover}.so
%attr(755,root,root) /%{_lib}/librpmdb-%{sover}.so
%attr(755,root,root) /%{_lib}/librpmio-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmbuild-%{sover}.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librpm.so
%attr(755,root,root) %{_libdir}/librpm-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmio.so
%attr(755,root,root) %{_libdir}/librpmio-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmdb.so
%attr(755,root,root) %{_libdir}/librpmdb-%{sover}.so
%attr(755,root,root) %{_libdir}/librpmbuild.so
%{_libdir}/librpm.la
%{_libdir}/librpmbuild.la
%{_libdir}/librpmdb.la
%{_libdir}/librpmio.la
%{_includedir}/rpm
%{_pkgconfigdir}/rpm.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/librpm.a
%{_libdir}/librpmbuild.a
%{_libdir}/librpmdb.a
%{_libdir}/librpmio.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpm2cpio
%attr(755,root,root) %{_bindir}/rpmdigest
%attr(755,root,root) %{_bindir}/rpmmtree
%attr(755,root,root) %{_bindir}/rpmrepo
%{!?with_system_libmagic:%attr(755,root,root) %{_bindir}/rpmfile}
%attr(755,root,root) %{_rpmlibdir}/debugedit
%attr(755,root,root) %{_rpmlibdir}/find-debuginfo.sh
%attr(755,root,root) %{_rpmlibdir}/rpmdb_loadcvt
%attr(755,root,root) %{_rpmlibdir}/rpmdeps
%attr(755,root,root) %{_rpmlibdir}/tgpg
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpmdeps.8*
%lang(ja) %{_mandir}/ja/man8/rpm2cpio.8*
%lang(ko) %{_mandir}/ko/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpm2cpio.8*
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
%attr(755,root,root) %{_rpmlibdir}/cross-build
%attr(755,root,root) %{_rpmlibdir}/find-spec-bcond
%attr(755,root,root) %{_rpmlibdir}/getpo.sh
%attr(755,root,root) %{_rpmlibdir}/install-build-tree
#%attr(755,root,root) %{_rpmlibdir}/config.*
#%attr(755,root,root) %{_rpmlibdir}/mkinstalldirs
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
%ifarch sparc sparcv9 sparc64
%{_rpmlibdir}/sparc*
%endif
%ifarch %{x8664}
%{_rpmlibdir}/amd64*
%{_rpmlibdir}/ia32e*
%{_rpmlibdir}/x86_64*
%endif
# must be here for "Requires: rpm-*prov" to work
%{_rpmlibdir}/macros.gstreamer
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
