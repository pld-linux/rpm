#
# TODO:
# - make key infrastructure code fallback from keyutils to plain mode in case keyctl
#   returns -ENOSYS
# - add macros for some ppc, mipsel, alpha and sparc
#
# - when adopting, use 4.5 ticket for checklist: https://bugs.launchpad.net/pld-linux/+bug/262985
#
# Conditional build:
%bcond_with	static		# build static rpm+rpmi
%bcond_without	apidocs		# don't generate documentation with doxygen
%bcond_without	python		# don't build python bindings
%bcond_without	selinux		# build without selinux support
%bcond_without	suggest_tags	# build without Suggest tag (bootstrapping)
%bcond_with	db61		# use DB 6.1 instead of 5.2
%bcond_with	db62		# use DB 6.2 instead of 5.2
%bcond_with	neon		# build with HTTP/WebDAV support (neon library)
%bcond_with	sqlite		# build with SQLite support
%bcond_with	system_lua	# use system lua
%bcond_without	system_pcre	# use system pcre
%bcond_with	keyutils	# build with keyutils support
# force_cc		- force using __cc other than "%{_target_cpu}-pld-linux-gcc"
# force_cxx		- force using __cxx other than "%{_target_cpu}-pld-linux-g++"
# force_cpp		- force using __cpp other than "%{_target_cpu}-pld-linux-gcc -E"
#

%if %{with sqlite}
# Error: /lib64/librpmio-5.4.so: undefined symbol: sqlite3_enable_load_extension
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)
%endif

# versions of required libraries
%if %{with db62}
%define		reqdb_pkg	db6.2
%define		reqdb_ver	6.2
%define		reqdb_pkgver	6.2.23
%else
%if %{with db61}
%define		reqdb_pkg	db6.1
%define		reqdb_ver	6.1
%define		reqdb_pkgver	6.1.26
%else
%define		reqdb_pkg	db5.2
%define		reqdb_ver	5.2
%define		reqdb_pkgver	5.2.36.0-4
%endif
%endif
%define		reqpopt_ver	1.15
%define		beecrypt_ver	2:4.2.0
%define		sover		5.4

Summary:	RPM Package Manager
Summary(de.UTF-8):	RPM Packet-Manager
Summary(es.UTF-8):	Gestor de paquetes RPM
Summary(pl.UTF-8):	Aplikacja do zarządzania pakietami RPM
Summary(pt_BR.UTF-8):	Gerenciador de pacotes RPM
Summary(ru.UTF-8):	Менеджер пакетов от RPM
Summary(uk.UTF-8):	Менеджер пакетів від RPM
Name:		rpm
Version:	5.4.18
Release:	0.1
License:	LGPL v2.1
Group:		Base
# http://rpm5.org/files/rpm/rpm-5.4/SNAPSHOT/rpm-5.4.18-0.20170718.src.rpm
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	4a0f6fb37be9c3657de64c9e9944a3ae
# See README.cpu-os-macros how to update cpu-os-macros.a
Source100:	cpu-os-macros.a
Source101:	README.cpu-os-macros
Source1:	%{name}.groups
Source2:	macros.pld.in
Source3:	%{name}-install-tree
Source4:	%{name}-find-spec-bcond
Source5:	%{name}-hrmib-cache
Source6:	%{name}-groups-po.awk
Source7:	%{name}-compress-doc
Source8:	%{name}-php-provides
Source9:	%{name}-php-requires
Source10:	%{name}.sysinfo
Source11:	perl.prov
Source12:	%{name}-user_group.sh
Source13:	%{name}.sysconfig
Source14:	%{name}-java-requires
# http://svn.pld-linux.org/banner.sh/
Source15:	banner.sh
Source16:	ftp://ftp.pld-linux.org/dists/th/PLD-3.0-Th-GPG-key.asc
# Source16-md5:	08b29584dd349aac9caa7610131a0a88
Source17:	%{name}-mimetypedeps
Source18:	macros.local
Source19:	%{name}.noautocompressdoc
Source20:	%{name}.noautoprov
Source21:	%{name}.noautoprovfiles
Source22:	%{name}.noautoreq
Source24:	%{name}.noautoreqfiles
Source25:	%{name}-php-requires.php
Source26:	%{name}db_checkversion.c
Source27:	macros.lang
Source28:	%{name}db_reset.c
Source29:	dbupgrade.sh
Source30:	rubygems.rb
Source31:	gem_helper.rb
Patch0:		%{name}-branch.patch
Patch1:		%{name}-man_pl.patch
Patch2:		%{name}-popt-aliases.patch
Patch3:		%{name}-nosetproctitle.patch
Patch4:		%{name}-perl-macros.patch
Patch5:		%{name}-perl-req-perlfile.patch
Patch6:		%{name}-scripts-closefds.patch
Patch7:		%{name}-php-macros.patch
Patch8:		%{name}-gettext-in-header.patch
Patch9:		%{name}-lua.patch
Patch10:	%{name}-php-deps.patch
Patch11:	%{name}-notsc.patch
Patch12:	%{name}-hack-norpmlibdep.patch
Patch13:	%{name}-dont-copy-descriptive-tags.patch
Patch14:	%{name}-perl_req-INC_dirs.patch
Patch15:	%{name}-debuginfo.patch
Patch16:	vendor-pld.patch
Patch17:	%{name}-old-fileconflicts-behaviour.patch
Patch18:	%{name}-javadeps.patch
Patch19:	i18n-string.patch
Patch20:	%{name}-libtool-deps.patch
Patch21:	%{name}-mimetype.patch
Patch22:	%{name}-sparc64.patch
Patch23:	%{name}-gendiff.patch
Patch24:	openmp.patch
Patch25:	%{name}-URPM-build-fix.patch
Patch26:	%{name}-semanage.patch
Patch27:	%{name}-helperEVR-noassert.patch
Patch28:	%{name}-unglobal.patch
Patch29:	%{name}-builddir-readlink.patch
Patch30:	%{name}-changelog_order_check_nonfatal.patch
Patch31:	%{name}-cleanbody.patch
Patch32:	%{name}-dirdeps-macro.patch
Patch33:	%{name}-installbeforeerase.patch
Patch34:	%{name}-libmagic-locale.patch
Patch35:	%{name}-namespace-compare.patch
Patch36:	%{name}-popt-coreutils.patch
Patch37:	%{name}-postun-nofail.patch
Patch38:	%{name}-DB_RDONLY.patch
Patch39:	%{name}-fix-missing-types-in-headers.patch
Patch40:	%{name}-fix--p-interpreter-and-empty-script.patch
Patch41:	%{name}-db_buffer_small.patch
Patch42:	%{name}-pattern_Release.patch
Patch43:	%{name}-fix-___build_pre-macro.patch
Patch44:	%{name}-missing-patch-file-fails-build.patch
Patch45:	%{name}-remove-misleading-missing-patch-message.patch
Patch46:	%{name}-file-magic-can-be-mixed-case.patch
Patch47:	%{name}-query-always-noisy.patch
Patch48:	%{name}-verify-ghosts-broken-logic.patch
Patch49:	%{name}-python-enable-compat-RPMSENSE.patch
Patch50:	%{name}-dont-treat-gstreamer-modules-as-font.patch
Patch51:	%{name}-gst-inspect-typo.patch
Patch52:	%{name}-null-term-ascii-digest.patch
Patch53:	%{name}-lua-enable-extra-libs.patch
Patch54:	%{name}-fix-filedigests-verify.patch
Patch55:	%{name}-disable-hmac-verify.patch
Patch56:	%{name}-macros.patch
Patch57:	%{name}-headerChecks.patch
Patch58:	%{name}-preserve-iterator.patch
Patch60:	%{name}-python-sitescriptdir.patch
Patch61:	%{name}-clean-docdir.patch
Patch62:	%{name}-DB_CONFIG.patch
Patch63:	%{name}-pythoneggs.patch
Patch64:	%{name}-fix-compress-doc.patch
Patch65:	%{name}-parseSpec-skip-empty-tags.patch
Patch66:	%{name}-rpm4compat-update.patch
Patch67:	%{name}-repackage-dont-force-max-compression.patch
Patch70:	python-%{name}sense-missingok.patch
Patch71:	%{name}-changelog-encoding.patch
Patch74:	%{name}-fix-internal-lua-build.patch
Patch75:	%{name}-double_check_file_deps.patch
Patch77:	%{name}-lua-expat.patch
Patch78:	%{name}-double_check_unpackaged_subdirs.patch
Patch79:	%{name}-rpmspec.patch

Patch81:	%{name}-perl-magic.patch
Patch82:	%{name}-5.4.15-use-DSA-sig.patch
Patch83:	%{name}-ignore-missing-macro-files.patch
Patch84:	x32.patch
Patch85:	rpm-CVE-2013-6435.patch
Patch86:	rpm-CVE-2014-8118.patch
Patch87:	%{name}-file-output-for-ELF.patch
Patch88:	%{name}-rpmtdnext.patch
Patch89:	disable-header-verification.patch
Patch90:	%{name}-cppcompat.patch
Patch91:	py-disable-fetch.patch
Patch92:	fast_python_deps.patch
Patch93:	python2_explicit.patch

# Patches imported from Mandriva

# status: ready to merge, it's already been merged on HEAD, so commiting it to rpm-5_4
# would basically just mean backporting it..
Patch1000:	%{name}-5.4.4-add-_specfile-macro.patch
# status: needs to be cleaned up and properly reviewed together with rest
# of the patches related to dependency generation
Patch1001:	%{name}-5.4.9-avoid-dependencies-on-self.patch
# status: probably ready to merge
Patch1002:	%{name}-5.4.4-pkgconfigdeps-check-path.patch
# status: probably okay to merge, but discuss on rpm-devel first
Patch1003:	%{name}-5.4.4-glob-wildcards-for-loading-macro-files.patch
# status: needs to be discussed
Patch1004:	%{name}-5.4.4-allow-installation-of-repackaged-rpms.patch
# status: ready to merge
Patch1005:	%{name}-5.4.8-dont-show-suggests-with-requires.patch
# status: ready for merge
Patch1006:	%{name}-5.4.9-strip-buildroot-away-from-duplicate-files-list.patch
# status: probably okay to merge, but discuss on rpm-devel first
Patch1007:	%{name}-5.4.10-duplicate_files_terminate_build.patch
# status: same as above
Patch1008:	%{name}-5.4.10-unpackaged_subdirs_terminate_build.patch
# mdvbz#64898
# status: uncertain, might be okay to merge, discuss on rpm-devel first
Patch1009:	%{name}-5.4.4-rpmbuild-withoutclean.patch
# no sense in having an additional dependency on 'pkgconfig' on all packages that
# have a pkgconfig file, it's not needed for them to be made useful and anything
# actuallly using pkgconfig for this purpose will pull it in as a dependency anyways...
# status: might be okay to merge, but discuss on rpm-devel first
Patch1010:	%{name}-5.4.4-drop-useless-auto-generated-pkgconfig-dependency.patch
# status: ready for merge
Patch1011:	%{name}-5.4.4-fix-rpmconstant-to-always-use-LC_CTYPE-C-for-case-conversion.patch
# $RPM_BUILD_DIR isn't necessarily the same as $PWD, it's %%{_builddir}, not
# %%{_builddir}/%%{?buildsubdir}, messing up paths in debug packages created..
# status: needs to be discussed and investigated a bit better..
Patch1012:	%{name}-5.4.4-pass-_builddir-properly-to-find-debuginfo.patch
# status: probably okay to merge, but discuss on rpm-devel first
Patch1013:	%{name}-5.4.10-files-listed-twice-terminates-build.patch
# status: probably okay to merge
Patch1014:	%{name}-5.4.9-ruby1.9-fixes.patch
# status: keep locally
Patch1015:	%{name}-5.4.9-keep-loading-script-macros.patch
# status: same as for other dep gen patches
Patch1016:	%{name}-5.4.9-update-rpmfc-when-removing-dependencies-on-self.patch
# status: idem
Patch1017:	%{name}-5.4.9-rpmfc-extract-dependencies-for-all-files.patch
# status: probably okay to merge
Patch1019:	%{name}-5.4.5-python-export-spec-macros.patch
# status: idem
Patch1020:	%{name}-5.4.9-font-provides.patch
# stauus: idem
Patch1021:	%{name}-5.4.7-kmod-dependencies.patch
# status: probably okay to merge, discuss on rpm-devel first
Patch1022:	%{name}-5.4.5-skip-dependencies-for-character-devices.patch
# status: probably okay to merge
Patch1024:	%{name}-5.4.5-rpmfc-apply-python-coloring-from-magic.patch
# status: ready
Patch1027:	%{name}-5.4.7-fix-generation-of-ruby-abi-provides.patch
# crash reproducable with 'rpm -qa --triggers'
# status: ready
Patch1028:	%{name}-5.4.7-hdrfmt-fix-unitialized-argv-element.patch
# status: same as for other dep gen patches
Patch1029:	%{name}-5.4.7-dont-consider-trigger-dependencies-as-overlapping.patch
# status: ready
Patch1030:	%{name}-5.4.7-fix-minor-memleaks.patch
# status: ready
Patch1031:	%{name}-5.4.9-mire-fix-strings-lacking-null-terminator.patch
# status: ready
Patch1032:	%{name}-5.4.9-rpmpython-fix-input.patch
# status: ready
Patch1033:	%{name}-5.4.7-no-seqid_init-on-rdonly-database.patch
# status: probably ready to merge, discuss on rpm-devel first
Patch1035:	%{name}-5.4.9-fix-verify-segfault.patch
# Due to rpmdav/neon being written in a different fashion than other rpmio clients,
# the inconsistent behaviour affects code elsewhere which expects consistent behaviour,
# with the result being that when unable to download files, neon will save error
# page as the target file.
# status: should go upstream, but uncertain about "correct" fix, ie. this is
# more of a workaround, while rewriting rpmdav code to behave consistently
# would be "the right thing to do". Yet I'm not fully able to grasp all of the
# code and don't want to spend more time just to get the API..
Patch1037:	%{name}-5.4.10-fix-neon-saving-error-pages-as-target-file.patch
# As the transaction flags for ignoring arch & os are no longer used, there's
# currently no way to ignore arch & os of packages anymore. This patch adds
# support for doing this again by defining rpm variables and overriding
# --ignorearch & --ignoreos to set these.
# status: needs to be discussed upstream before thinking about merging
Patch1038:	%{name}-5.4.10-support-ignore-arch-and-os-again.patch
# status: ready for merge
Patch1039:	%{name}-5.4.4-fix-same-package-with-epoch-possible-to-upgrade.patch
# we want that patch too, a bit of builder infrastructure relies on NOSIGNATURES
Patch1040:	%{name}-5.4.9-support-signatures-and-digest-disablers.patch
# lack insight on actual functionality, which anyways seems broken, so let's
# disable it to avoid errors from berkeley db..
# status: keep locally
Patch1041:	%{name}-5.4.9-disable-l10ndir.patch
# status: ready for merge
Patch1042:	%{name}-5.4.9-fix-rpm_qa-pattern.patch
Patch1044:	%{name}-5.4.12-fix-rpmlua-print.patch
Patch1045:	%{name}-5.4.12-fix-rpmpython-module-import-init.patch

# proyvind:
# there's a rpmdbchk tool I wrote a while back, which might help you. although
# the incidents it's able to deal with is rather limited ATM... it might help
# you out, if not and you'll be able to solve yer problem, you could take a
# stab at adding support for fixing your specific problem to the util ;)
# https://abf.io/openmandriva/rpm/raw/master/rpm-5.4.14-rpmdbchk.patch
Patch1048:	%{name}-5.4.14-rpmdbchk.patch

Patch1050:	python-libx32.patch

URL:		http://rpm5.org/
BuildRequires:	%{reqdb_pkg}-devel >= %{reqdb_pkgver}
%if %{with sqlite}
BuildRequires:	sqlite3-devel
%else
BuildRequires:	%{reqdb_pkg}-sql-devel >= %{reqdb_pkgver}
%endif
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1.4
BuildRequires:	beecrypt-devel >= %{beecrypt_ver}
BuildRequires:	bzip2-devel >= 1.0.2-17
BuildRequires:	elfutils-devel >= 0.108
BuildRequires:	gettext-tools >= 0.19.2
%{?with_keyutils:BuildRequires:	keyutils-devel}
BuildRequires:	libmagic-devel
%if %{with selinux}
BuildRequires:	libselinux-devel >= 2.1.0
BuildRequires:	libsemanage-devel >= 2.1.0
BuildRequires:	libsepol-devel >= 2.1.0
%endif
# needed only for AM_PROG_CXX used for CXX substitution in rpm.macros
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
%if %{with neon}
BuildRequires:	libxml2-devel
BuildRequires:	neon-devel >= 0.25.5
%endif
%{?with_system_lua:BuildRequires:	lua52-devel >= 5.2.2}
BuildRequires:	ossp-uuid-devel
BuildRequires:	patch >= 2.2
BuildRequires:	popt-devel >= %{reqpopt_ver}
%{?with_python:BuildRequires:	python-devel >= 1:2.3}
BuildRequires:	python-modules >= 1:2.3
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	tcl
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	ghostscript
BuildRequires:	graphviz
BuildRequires:	tetex-pdftex
%endif
%if %{with static}
# Require static library only for static build
BuildRequires:	%{reqdb_pkg}-static >= %{reqdb_pkgver}
BuildRequires:	beecrypt-static >= %{beecrypt_ver}
BuildRequires:	bzip2-static >= 1.0.2-17
BuildRequires:	elfutils-static
BuildRequires:	glibc-static >= 2.2.94
BuildRequires:	libmagic-static
%if %{with selinux}
BuildRequires:	libselinux-static >= 2.1.0
BuildRequires:	libsemanage-static >= 2.1.0
BuildRequires:	libsepol-static >= 2.1.0
%endif
BuildRequires:	popt-static >= %{reqpopt_ver}
BuildRequires:	zlib-static
%endif
Requires(posttrans):	coreutils
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
Conflicts:	util-vserver < 0.30.216-1.pre3034.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_binary_payload		w9.gzdio

# don't require very fresh rpm.macros to build
%define		__gettextize gettextize --copy --force --intl ; cp -f po/Makevars{.template,}
%define		find_lang sh ./scripts/find-lang.sh $RPM_BUILD_ROOT
%define		ix86	i386 i486 i586 i686 athlon pentium3 pentium4
%define		ppc	ppc ppc7400 ppc7450
%define		x8664	amd64 ia32e x86_64

# stabilize new build environment
%ifnarch x32
%define		__newcc %{?force_cc}%{!?force_cc:%{_target_cpu}-pld-linux-gcc}
%define		__newcxx %{?force_cxx}%{!?force_cxx:%{_target_cpu}-pld-linux-g++}
%define		__newcpp %{?force_cpp}%{!?force_cpp:%{_target_cpu}-pld-linux-gcc -E}
%else
# x32 is a very special case
%define		__newcc %{?force_cc}%{!?force_cc:x86_64-pld-linux-gnux32-gcc}
%define		__newcxx %{?force_cxx}%{!?force_cxx:x86_64-pld-linux-gnux32-g++}
%define		__newcpp %{?force_cpp}%{!?force_cpp:x86_64-pld-linux-gnux32-gcc -E}
%endif

%define		_rpmlibdir /usr/lib/rpm
%define		_noautocompressdoc	RPM-GPG-KEY

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
Requires:	%{reqdb_pkg} >= %{reqdb_pkgver}
%if %{with sqlite}
Requires:	sqlite3 >= %{sqlite_build_version}
%else
Requires:	%{reqdb_pkg}-sql >= %{reqdb_pkgver}
%endif
Requires:	beecrypt >= %{beecrypt_ver}
Requires:	libmagic >= 1.15-2
%{?with_selinux:Requires:	libselinux >= 2.1.0}
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
Requires:	%{reqdb_pkg}-devel >= %{reqdb_pkgver}
Requires:	beecrypt-devel >= %{beecrypt_ver}
Requires:	bzip2-devel
Requires:	elfutils-devel
%{?with_keyutils:Requires:	keyutils-devel}
Requires:	libmagic-devel
%if %{with selinux}
Requires:	libselinux-devel
Requires:	libsemanage-devel
Requires:	libsepol-devel
%endif
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
Requires:	%{reqdb_pkg}-static >= %{reqdb_pkgver}
Requires:	beecrypt-static >= %{beecrypt_ver}
Requires:	bzip2-static
Requires:	elfutils-static
%{?with_keyutils:Requires:	keyutils-static}
Requires:	libmagic-static
%if %{with selinux}
Requires:	libselinux-static
Requires:	libsemanage-static
Requires:	libsepol-static
%endif
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
Requires(pretrans):	coreutils
Requires(pretrans):	findutils
Requires:	%{name}-build-macros >= 1.712
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
Requires:	sed >= 4.0
Requires:	sh-utils
Requires:	tar >= 1:1.22
Requires:	textutils
Requires:	which
Requires:	xz
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
Requires:	%{name} = %{version}-%{release}
Requires:	python
Requires:	python-setuptools
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
Suggests:	php-pear-PHP_CompatInfo

%description php-pearprov
Additional utilities for checking PHP PEAR provides/requires in RPM
packages.

%description php-pearprov -l pl.UTF-8
Dodatkowe narzędzia do sprawdzenia zależności skryptów PHP PEAR w
pakietach RPM.

%package rubyprov
Summary:	Ruby tools, which simplify creation of RPM packages with Ruby software
Summary(pl.UTF-8):	Makra ułatwiające tworzenie pakietów RPM z programami napisanymi w Ruby
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	ruby
Requires:	ruby-modules
Requires:	ruby-rubygems

%description rubyprov
Ruby tools, which simplifies creation of RPM packages with Ruby
software.

%description rubyprov -l pl.UTF-8
Makra ułatwiające tworzenie pakietów RPM z programami napisanymi w
Ruby.

%package -n python-rpm
Summary:	Python interface to RPM library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki RPM-a
Summary(pt_BR.UTF-8):	Módulo Python para aplicativos que manipulam pacotes RPM
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
Documentation for RPM API and guides in HTML format generated from rpm
sources by doxygen.

%description apidocs -l pl.UTF-8
Dokumentacja API RPM-a oraz przewodniki w formacie HTML generowane ze
źrodeł RPM-a przez doxygen.

%prep
%setup -q -n %{name}-%{version}%{?subver}
install -d platform
cd platform
ar x %{SOURCE100}
cd -

#patch0 -p1
%patch1 -p1
%patch2 -p1
#%patch3 -p1 do we still want to disable setproctitle
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%{?with_system_lua:%patch9 -p1}
%patch10 -p1
%ifnarch i386 i486
# enable TSC for capable archs
%patch11 -p1
%endif
%patch12 -p1
# http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2016-March/024760.html
#%patch13 -p1 POSSIBLY SOLVED, decrypt what jbj said on SUPPORT_I18NSTRING_TYPE in ml
%patch14 -p0
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%ifarch sparc64
%patch22 -p1
%endif
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
#%patch35 -p1 rpm-namespace-compare.patch -- UPDATE!
%patch36 -p1
%patch37 -p1
%patch38 -p1
#%patch39 -p1 rpm-fix-missing-types-in-headers.patch - oudated?
%patch40 -p1
%if %{with db61} || %{with db62}
%patch41 -p1
%endif
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p0
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
#%patch57 -p1 rpm-headerChecks.patch - applied in 5.4.18 ?
%patch58 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch70 -p1
%patch71 -p1
%patch74 -p1
%patch75 -p1
%patch77 -p1
%patch78 -p1
#%patch79 -p1 rpm-rpmspec.patch - update rpm.org port

%patch81 -p0
%patch82 -p1
%patch84 -p1
#%patch85 -p1 rpm-CVE-2013-6435.patch - solved differently upstream?
%patch86 -p1
%patch87 -p1
%patch88 -p1
%patch89 -p1
%patch90 -p1
%patch91 -p1

%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1
%patch1008 -p1
%patch1009 -p1
%patch1010 -p1
%patch1011 -p1
%patch1012 -p1
%patch1013 -p1
%patch1014 -p1
%patch1015 -p1
%patch1016 -p1
%patch1017 -p1
%patch1019 -p1
%patch1020 -p1
%patch1021 -p1
%patch1022 -p1
%patch1024 -p1
%patch1027 -p1
%patch1028 -p1
%patch1029 -p1
%patch1030 -p1
%patch1031 -p1
%patch1032 -p1
%patch1033 -p1

%patch1035 -p1
%patch1037 -p1
%patch1038 -p1
%patch1039 -p1
%patch1040 -p1
# don't delete, may be useful if jbj decides to enable this again
#%patch1041 -p1
%patch1042 -p1

#%patch1044 -p1 SOLVED? need testcase to test
%patch1045 -p1

%patch1048 -p1

%patch83 -p1
%patch92 -p1
%patch93 -p1

%patch1050 -p1

install %{SOURCE2} macros/pld.in
install %{SOURCE8} scripts/php.prov.in
install %{SOURCE9} scripts/php.req.in
install %{SOURCE11} scripts/perl.prov.in
cp -p %{SOURCE30} scripts/rubygems.rb
cp -p %{SOURCE31} scripts/gem_helper.rb

%{__rm} scripts/find-php*

%{__mv} -f scripts/perl.req{,.in}

# generate Group translations to *.po
awk -f %{SOURCE6} %{SOURCE1}

install %{SOURCE26} tools/rpmdb_checkversion.c
install %{SOURCE28} tools/rpmdb_reset.c

for extlib in beecrypt neon %{?with_system_pcre:pcre} popt libtpm; do
	[ -d $extlib ] && %{__rm} -r $extlib
done

%if %{without db62}
%{__sed} -e 's/^DBXY=db62$/DBXY=db%{reqdb_ver}/' \
	 -e 's/db-6\.2/db-%{reqdb_ver}/' \
	 -e 's/db_sql-6\.2/db_sql-%{reqdb_ver}/' -i configure.ac
%endif

%build
%{__libtoolize}
#%{__autopoint}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

# rpm checks for CPU type at runtime, but it looks better
sed -i \
	-e 's|@host@|%{_target_cpu}-%{_target_vendor}-%{_target_os}|' \
	-e 's|@host_cpu@|%{_target_cpu}|' \
	-e 's|@host_os@|%{_target_os}|' \
	macros/macros.in

%{?with_system_lua:CPPFLAGS="-I/usr/include/lua51 %{rpmcppflags}"}
# pass CC and CXX too in case of building with some older configure macro
%configure \
	CC="%{__newcc}" \
	CXX="%{__newcxx}" \
	CPP="%{__newcpp}" \
	WITH_PERL_VERSION=no \
	__GST_INSPECT=%{_bindir}/gst-inspect-1.0 \
	--disable-silent-rules \
	--enable-shared \
	--enable-static \
	%{!?with_apidocs:--without-apidocs} \
	--with-usecrypto=beecrypt \
	--with-beecrypt=external \
	--with-tomcrypt=no \
	--with-bugreport="http://bugs.pld-linux.org/" \
	--with-bzip2=external \
	--with-db=external \
	--without-acl \
	--with-dbapi=db \
	--with-file=external \
	--with-keyutils=%{?with_keyutils:external}%{!?with_keyutils:no} \
	--with-libelf \
	--with-lua=%{!?with_system_lua:internal}%{?with_system_lua:external} \
	--with-lzma=external \
	--with-neon=%{?with_neon:external}%{!?with_neon:no} \
	--with-path-macros='%{_rpmlibdir}/macros:%{_rpmlibdir}/macros.d/pld:%{_rpmlibdir}/%%{_target}/macros:%{_rpmlibdir}/macros.build:%{_sysconfdir}/rpm/macros.*:%{_sysconfdir}/rpm/macros:%{_sysconfdir}/rpm/%%{_target}/macros:%{_sysconfdir}/rpm/macros.d/*.macros:~/etc/.rpmmacros:~/.rpmmacros' \
	--without-path-versioned \
	--with-pcre=%{!?with_system_pcre:internal}%{?with_system_pcre:external} \
	--with-popt=external \
	%{?with_python:--with-python=%{py_ver} --with-python-lib-dir=%{py_sitedir}} \
	%{!?with_python:--without-python} \
	--with-selinux=%{!?with_selinux:no}%{?with_selinux:external} \
	--with-semanage=%{!?with_selinux:no}%{?with_selinux:external} \
	--with-sepol=%{!?with_selinux:no}%{?with_selinux:external} \
	--with-sqlite=%{?with_sqlite:yes}%{!?with_sqlite:no} \
	--with-uuid=%{_libdir}:%{_includedir}/ossp-uuid \
	--without-sasl2 \
	--with-vendor=pld \
	--with-xz=external \
	--with-zlib=external

%{__make} -j1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CPP="%{__cpp}"

%{?with_apidocs:%{__make} apidocs}

%{__cc} %{rpmcflags} -I/usr/include/db%{reqdb_ver} tools/rpmdb_checkversion.c \
	-o tools/rpmdb_checkversion -ldb-%{reqdb_ver}
%{__cc} %{rpmcflags} -I/usr/include/db%{reqdb_ver} tools/rpmdb_reset.c \
	-o tools/rpmdb_reset -ldb-%{reqdb_ver}

if tools/rpmdb_checkversion -V 2>&1 | grep "t match library version"; then
	echo "Error linking rpmdb tools!"
	exit 1
fi
if tools/rpmdb_reset -V 2>&1 | grep "t match library version"; then
	echo "Error linking rpmdb tools!"
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,/%{_lib},/etc/sysconfig,%{_sysconfdir}/rpm} \
	$RPM_BUILD_ROOT{/var/lib/banner,/var/cache/hrmib,/etc/pki/rpm-gpg}

install %{SOURCE16} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/PLD-3.0-Th-GPG-key.asc

%{__make} -j1 install \
	pkgconfigdir=%{_pkgconfigdir} \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ht
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/no
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/pt_PT

# install platform macros
for f in platform/*macros; do
	bn=${f#*/}
	fn=${bn%.macros}/macros
	install -m644 $f -D %{buildroot}%{_rpmlibdir}/$fn
done

# cleanup
%ifnarch %{ix86} %{x8664} x32
rm $RPM_BUILD_ROOT%{_rpmlibdir}/athlon-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/i386-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/i486-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/i586-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/i686-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/pentium3-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/pentium4-linux/macros
%endif

%ifnarch %{x8664} x32
rm $RPM_BUILD_ROOT%{_rpmlibdir}/amd64-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/ia32e-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/x32-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/x86_64-linux/macros
%endif

%ifnarch %{ppc}
rm $RPM_BUILD_ROOT%{_rpmlibdir}/ppc-linux/macros
%endif

rm $RPM_BUILD_ROOT%{_rpmlibdir}/alpha*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/arm*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/ia64-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/k6-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/mips*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/ppc*series-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/ppc64*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/s390*-linux/macros
rm $RPM_BUILD_ROOT%{_rpmlibdir}/sparc*-linux/macros

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/platform
# first platform file entry can't contain regexps
%ifarch x32
%{_target_cpu}-%{_target_vendor}-linux-gnux32
%else
%{_target_cpu}-%{_target_vendor}-linux
%endif

%ifarch x86_64
x86_64-[^-]*-[Ll]inux(-gnu)?
amd64-[^-]*-[Ll]inux(-gnu)?
x32-[^-]*-[Ll]inux(-gnu(x32)?)?
%endif
%ifarch amd64
amd64-[^-]*-[Ll]inux(-gnu)?
x86_64-[^-]*-[Ll]inux(-gnu)?
x32-[^-]*-[Ll]inux(-gnu(x32)?)?
%endif
%ifarch ia32e
ia32e-[^-]*-[Ll]inux(-gnu)?
x86_64-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch x32
x32-[^-]*-[Ll]inux(-gnu(x32)?)?
x86_64-[^-]*-[Ll]inux(-gnu)?
amd64-[^-]*-[Ll]inux(-gnu)?
%endif

%ifarch athlon %{x8664} x32
athlon-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch pentium4 athlon %{x8664} x32
pentium4-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch pentium3 pentium4 athlon %{x8664} x32
pentium3-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch i686 pentium3 pentium4 athlon %{x8664} x32
i686-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch i586 i686 pentium3 pentium4 athlon %{x8664} x32
i586-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch i486 i586 i686 pentium3 pentium4 athlon %{x8664} x32
i486-[^-]*-[Ll]inux(-gnu)?
%endif
%ifarch %{ix86} %{x8664} x32
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

noarch-[^-]*-.*
EOF

# Squash Extra Blank Lines
%{__sed} -i -e '/./,/^$/!d' $RPM_BUILD_ROOT%{_sysconfdir}/rpm/platform

%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/vpkg-provides*
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/find-{prov,req}.pl
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/find-{provides,requires}.perl
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/find-lang.sh
%if %{without system_lua} && 0
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/lib/liblua.a
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/lib/liblua.la
%endif
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/mono-find-provides
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/mono-find-requires

# not installed since 4.4.8 (-tools-perl subpackage)
install scripts/rpmdiff scripts/rpmdiff.cgi $RPM_BUILD_ROOT%{_rpmlibdir}

install %{SOURCE1} doc/manual/groups
install %{SOURCE3} $RPM_BUILD_ROOT%{_rpmlibdir}/install-build-tree
install %{SOURCE4} $RPM_BUILD_ROOT%{_rpmlibdir}/find-spec-bcond
install %{SOURCE7} $RPM_BUILD_ROOT%{_rpmlibdir}/compress-doc
install %{SOURCE12} $RPM_BUILD_ROOT%{_rpmlibdir}/user_group.sh
install %{SOURCE14} $RPM_BUILD_ROOT%{_rpmlibdir}/java-find-requires
install scripts/php.{prov,req}	$RPM_BUILD_ROOT%{_rpmlibdir}
cp -p %{SOURCE25} $RPM_BUILD_ROOT%{_rpmlibdir}/php.req.php
install %{SOURCE17} $RPM_BUILD_ROOT%{_rpmlibdir}/mimetypedeps.sh
install %{SOURCE5} $RPM_BUILD_ROOT%{_rpmlibdir}/hrmib-cache
install %{SOURCE13} $RPM_BUILD_ROOT/etc/sysconfig/rpm

install %{SOURCE15} $RPM_BUILD_ROOT%{_bindir}/banner.sh

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo

install %{SOURCE18} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros
install %{SOURCE27} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.lang
install %{SOURCE19} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautocompressdoc
install %{SOURCE20} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprov
install %{SOURCE21} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprovfiles
install %{SOURCE22} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreq
install %{SOURCE24} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreqfiles

touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Conflictname
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Dirnames
install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Filelinktos
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Obsoletename
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Providename
touch $RPM_BUILD_ROOT%{_sysconfdir}/rpm/sysinfo/Requirename

install tools/rpmdb_checkversion $RPM_BUILD_ROOT%{_rpmlibdir}/bin
install tools/rpmdb_reset $RPM_BUILD_ROOT%{_rpmlibdir}/bin
install %{SOURCE29} $RPM_BUILD_ROOT%{_rpmlibdir}/bin/dbupgrade.sh

# create macro loading wrappers for backward compatibility
for m in gstreamer java mono perl php python; do
	echo "%%{load:%{_rpmlibdir}/macros.d/$m}" >$RPM_BUILD_ROOT%{_rpmlibdir}/macros.$m
done

# moved to rpm-build-macros 1.699
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/macros.d/kernel

# for rpm -e|-U --repackage
install -d $RPM_BUILD_ROOT/var/{spool/repackage,lock/rpm}
touch $RPM_BUILD_ROOT/var/lock/rpm/transaction

# move rpm to /bin
mv $RPM_BUILD_ROOT%{_bindir}/rpm $RPM_BUILD_ROOT/bin
# move essential libs to /lib (libs that /bin/rpm links to)
for a in librpm-%{sover}.so librpmdb-%{sover}.so librpmio-%{sover}.so librpmbuild-%{sover}.so librpmmisc-%{sover}.so librpmconstant-%{sover}.so; do
	mv -f $RPM_BUILD_ROOT%{_libdir}/$a $RPM_BUILD_ROOT/%{_lib}
	ln -s /%{_lib}/$a $RPM_BUILD_ROOT%{_libdir}/$a
done

# Bourne shell script vs ELF executable linked with rpm,rpmdb,rpmio
mv $RPM_BUILD_ROOT{%{_rpmlibdir},%{_bindir}}/rpm2cpio

%if %{with python}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/rpm/*.{la,py}
%endif

# wrong location, not used anyway
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/rpm.{daily,log,xinetd}
# utils dropped in 5.4 -- their manuals
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/rpmgrep.1
# script obsoleted by /usr/lib/rpm/bin/dbconvert binary
%{__rm} $RPM_BUILD_ROOT%{_rpmlibdir}/dbconvert.sh

%find_lang %{name}

%{__rm} -rf manual
cp -a doc/manual manual
%{__rm} -f manual/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# this needs to be a dir
if [ -f %{_sysconfdir}/rpm/sysinfo ]; then
	umask 022
	mv -f %{_sysconfdir}/rpm/sysinfo{,.rpmsave}
	mkdir %{_sysconfdir}/rpm/sysinfo
fi

%posttrans
if [ -e /var/lib/rpm/Packages ] && \
		! %{_rpmlibdir}/bin/rpmdb_checkversion -h /var/lib/rpm -d /var/lib/rpm; then
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
	%{_rpmlibdir}/bin/dbupgrade.sh
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

%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/PLD-3.0-Th-GPG-key.asc

%attr(755,root,root) /bin/rpm

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/macros
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpm/macros.lang
%dir %{_sysconfdir}/rpm/sysinfo
# these are ok to be replaced
%config %verify(not md5 mtime size) %{_sysconfdir}/rpm/sysinfo/*
%config %verify(not md5 mtime size) %{_sysconfdir}/rpm/platform

%{_mandir}/man8/rpm.8*
%lang(fr) %{_mandir}/fr/man8/rpm.8*
%lang(ja) %{_mandir}/ja/man8/rpm.8*
%lang(pl) %{_mandir}/pl/man8/rpm.8*
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%lang(sk) %{_mandir}/sk/man8/rpm.8*

%dir /var/lib/rpm
%dir /var/lib/rpm/log
%dir /var/lib/rpm/tmp
%config(noreplace) %verify(not md5 mtime size) /var/lib/rpm/DB_CONFIG
%dir %attr(700,root,root) /var/spool/repackage
%dir /var/lock/rpm
/var/lock/rpm/transaction

# exported package NVRA (stamped with install tid)
# net-snmp hrSWInstalledName queries, bash-completions
%dir /var/cache/hrmib

%{_rpmlibdir}/qf
%{_rpmlibdir}/rpmpopt*
%{_rpmlibdir}/macros
%dir %{_rpmlibdir}/macros.d
%{_rpmlibdir}/macros.d/pld
%{_rpmlibdir}/cpuinfo.yaml
%{_rpmlibdir}/noarch-*
%ifarch %{ix86} %{x8664} x32
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
%ifarch %{x8664} x32
%{_rpmlibdir}/amd64*
%{_rpmlibdir}/ia32e*
%{_rpmlibdir}/x86_64*
%{_rpmlibdir}/x32*
%endif

%attr(755,root,root) %{_rpmlibdir}/hrmib-cache

%dir %{_rpmlibdir}/bin
%attr(755,root,root) %{_rpmlibdir}/bin/dbconvert
%attr(755,root,root) %{_rpmlibdir}/bin/dbupgrade.sh
%attr(755,root,root) %{_rpmlibdir}/bin/rpmdb_checkversion
%attr(755,root,root) %{_rpmlibdir}/bin/rpmdb_reset
%attr(755,root,root) %{_rpmlibdir}/bin/rpmdbchk

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
%attr(755,root,root) /%{_lib}/librpmbuild-%{sover}.so
%attr(755,root,root) /%{_lib}/librpmmisc-%{sover}.so
%attr(755,root,root) /%{_lib}/librpmconstant-%{sover}.so

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
%attr(755,root,root) %{_bindir}/rpmconstant
%attr(755,root,root) %{_rpmlibdir}/find-debuginfo.sh
%attr(755,root,root) %{_rpmlibdir}/rpmdb_loadcvt
%attr(755,root,root) %{_rpmlibdir}/tgpg
%attr(755,root,root) %{_rpmlibdir}/bin/chroot
%attr(755,root,root) %{_rpmlibdir}/bin/cp
%attr(755,root,root) %{_rpmlibdir}/bin/debugedit
%attr(755,root,root) %{_rpmlibdir}/bin/find
%attr(755,root,root) %{_rpmlibdir}/bin/mgo
%attr(755,root,root) %{_rpmlibdir}/bin/mtree
%attr(755,root,root) %{_rpmlibdir}/bin/rpmcache
%attr(755,root,root) %{_rpmlibdir}/bin/rpmcmp
%attr(755,root,root) %{_rpmlibdir}/bin/rpmdeps
%attr(755,root,root) %{_rpmlibdir}/bin/rpmdigest
%if %{with selinux}
%attr(755,root,root) %{_rpmlibdir}/bin/semodule
%attr(755,root,root) %{_rpmlibdir}/bin/spooktool
%endif
%if %{without system_lua} && 0
%attr(755,root,root) %{_rpmlibdir}/bin/lua
%attr(755,root,root) %{_rpmlibdir}/bin/luac
%attr(755,root,root) %{_rpmlibdir}/bin/rpmlua
%attr(755,root,root) %{_rpmlibdir}/bin/rpmluac
%endif
%{?with_keyutils:%attr(755,root,root) %{_rpmlibdir}/bin/rpmkey}
%attr(755,root,root) %{_rpmlibdir}/bin/rpmrepo
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpmconstant.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmmtree.8*
%lang(ja) %{_mandir}/ja/man8/rpm2cpio.8*
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
%attr(755,root,root) %{_rpmlibdir}/compress-doc
%attr(755,root,root) %{_rpmlibdir}/cross-build
%attr(755,root,root) %{_rpmlibdir}/find-spec-bcond
%attr(755,root,root) %{_rpmlibdir}/getpo.sh
%attr(755,root,root) %{_rpmlibdir}/install-build-tree
%attr(755,root,root) %{_rpmlibdir}/u_pkg.sh
%attr(755,root,root) %{_rpmlibdir}/executabledeps.sh
%attr(755,root,root) %{_rpmlibdir}/libtooldeps.sh
%attr(755,root,root) %{_rpmlibdir}/mimetypedeps.sh
# needs hacked pkg-config to return anything
%attr(755,root,root) %{_rpmlibdir}/pkgconfigdeps.sh
%attr(755,root,root) %{_rpmlibdir}/bin/api-sanity-autotest.pl
%attr(755,root,root) %{_rpmlibdir}/bin/api-sanity-checker.pl
%{!?with_sqlite:%attr(755,root,root) %{_rpmlibdir}/bin/dbsql}
%attr(755,root,root) %{_rpmlibdir}/bin/install-sh
%attr(755,root,root) %{_rpmlibdir}/bin/mkinstalldirs
%attr(755,root,root) %{_rpmlibdir}/bin/pom2spec
%attr(755,root,root) %{_rpmlibdir}/bin/rpmspec
%attr(755,root,root) %{_rpmlibdir}/bin/rpmspecdump
%attr(755,root,root) %{_rpmlibdir}/bin/sqlite3
%attr(755,root,root) %{_rpmlibdir}/bin/wget
%attr(755,root,root) %{_rpmlibdir}/vcheck
# not used yet ... these six depend on perl
%attr(755,root,root) %{_rpmlibdir}/http.req
# we always used scripts provided by mono-devel, maybe move them here
#%attr(755,root,root) %{_rpmlibdir}/mono-find-provides
#%attr(755,root,root) %{_rpmlibdir}/mono-find-requires

%attr(755,root,root) %{_rpmlibdir}/fontconfig.prov
# must be here for "Requires: rpm-*prov" to work
%{_rpmlibdir}/macros.d/cmake
%{_rpmlibdir}/macros.d/gstreamer
%{_rpmlibdir}/macros.d/java
%{_rpmlibdir}/macros.d/libtool
%{_rpmlibdir}/macros.d/mono
%{_rpmlibdir}/macros.d/perl
%{_rpmlibdir}/macros.d/php
%{_rpmlibdir}/macros.d/pkgconfig
%{_rpmlibdir}/macros.d/python
%{_rpmlibdir}/macros.d/ruby
%{_rpmlibdir}/macros.d/selinux
%{_rpmlibdir}/macros.d/tcl
%{_rpmlibdir}/macros.rpmbuild
# compat wrappers
%{_rpmlibdir}/macros.gstreamer
%{_rpmlibdir}/macros.java
%{_rpmlibdir}/macros.mono
%{_rpmlibdir}/macros.perl
%{_rpmlibdir}/macros.php
%{_rpmlibdir}/macros.python

%attr(755,root,root) %{_rpmlibdir}/gstreamer.sh
%attr(755,root,root) %{_rpmlibdir}/kmod-deps.sh

%attr(755,root,root) %{_bindir}/gendiff
%attr(755,root,root) %{_bindir}/rpmbuild

%dir %{_rpmlibdir}/helpers
%attr(755,root,root) %{_rpmlibdir}/helpers/makeshlibs

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

%files rubyprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/gem_helper.rb
%attr(755,root,root) %{_rpmlibdir}/rubygems.rb

%files perlprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/perl.*
%attr(755,root,root) %{_rpmlibdir}/osgideps.pl
%attr(755,root,root) %{_rpmlibdir}/perldeps.pl

%files pythonprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/pythoneggs.py
%attr(755,root,root) %{_rpmlibdir}/pythondeps.sh

%files php-pearprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/php.prov
%attr(755,root,root) %{_rpmlibdir}/php.req
%attr(755,root,root) %{_rpmlibdir}/php.req.php

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
