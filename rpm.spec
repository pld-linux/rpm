#
# TODO:
# - fix perl.req and perl.prov to support _noauto macros
# - use system libmagic not internal libfmagic
#
# Conditional build:
%bcond_without	static	# - build shared /bin/rpm (doesn't work at the moment)
%bcond_without	docs	# - don't generate documentation with doxygen
%bcond_without	python	# - don't build python bindings
# force_cc		- force using __cc other than "%{_target_cpu}-pld-linux-gcc"
# force_cxx		- force using __cxx other than "%{_target_cpu}-pld-linux-g++"
# force_cpp		- force using __cpp other than "%{_target_cpu}-pld-linux-gcc -E"

%include        /usr/lib/rpm/macros.python
%define snap	20031227
# versions of required libraries
%define	reqdb_ver	4.2.50-1
%define	reqpopt_ver	1.9
%define	beecrypt_ver	3.0.0-0.20030610.1
%define rpm_macros_rev	1.133
Summary:	RPM Package Manager
Summary(de):	RPM Packet-Manager
Summary(es):	Gestor de paquetes RPM
Summary(pl):	Aplikacja do zarz�dzania pakietami RPM
Summary(pt_BR):	Gerenciador de pacotes RPM
Summary(ru):	�������� ������� �� RPM
Summary(uk):	�������� ����Ԧ� צ� RPM
Name:		rpm
%define	ver	4.3
Version:	%{ver}
Release:	0.%{snap}.2.1
License:	GPL
Group:		Base
#Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.2.x/%{name}-%{version}.%{snap}.tar.gz
Source0:	ftp://distfiles.pld-linux.org/src/%{name}-%{version}.%{snap}.tar.gz
# Source0-md5:	dcfe5575c62531838be5a0bebdaf0d1e
Source1:	%{name}.groups
Source2:	%{name}.platform
Source3:	%{name}-install-tree
#Source4:	%{name}-find-rpm-provides
Source5:	%{name}-find-spec-bcond
Source6:	%{name}-find-lang
#Source7:	%{name}-find-provides
#Source8:	%{name}-find-requires
Source9:	%{name}-groups-po.awk
Source10:	%{name}-compress-doc
Source11:	%{name}-check-files
Source12:	%{name}-php-provides
Source13:	%{name}-php-requires
Source14:	%{name}.macros
#Source15:	%{name}-find-provides-wrapper
#Source16:	%{name}-find-requires-wrapper
Source30:	builder
Source31:	adapter.awk
Source32:	pldnotify.awk
Source33:	perl.prov
Patch0:		%{name}-pl.po.patch
Patch1:		%{name}-rpmrc.patch
Patch2:		%{name}-arch.patch
Patch3:		%{name}-rpmpopt.patch
Patch4:		%{name}-perl-macros.patch
Patch5:		%{name}-perl-req-perlfile.patch
Patch6:		%{name}-glob.patch
Patch7:		%{name}-noexpand.patch
Patch8:		%{name}-scripts-closefds.patch
Patch9:		%{name}-python-macros.patch
Patch10:	%{name}-gettext-in-header.patch
Patch11:	%{name}-compress-doc.patch
Patch12:	%{name}-gettext0.11.patch
Patch13:	%{name}-build.patch
Patch14:	%{name}-system_libs.patch
Patch15:	%{name}-bb-and-short-circuit.patch
Patch16:	%{name}-etc_dir.patch
Patch17:	%{name}-system_libs-more.patch
Patch18:	%{name}-php-deps.patch
Patch19:	%{name}-python-fix.patch
Patch20:	%{name}-ldconfig-always.patch
Patch21:	%{name}-perl_req.patch
Patch22:	%{name}-system_libs_more.patch
Patch23:	%{name}-python_2_3.patch
Patch24:	%{name}-no-bin-env.patch
Patch25:	%{name}-specflags.patch
Patch26:	%{name}-magic-usesystem.patch
Patch27:	%{name}-dontneedutils.patch
Patch28:	%{name}-python-beecrypt.patch
Patch29:	%{name}-man-typos.patch
Patch30:	%{name}-man-pl.patch
Patch31:	%{name}-fdClose-typo.patch
#Patch32:	%{name}-userpmdepswrappers.patch
Patch33:	%{name}-provides-dont-obsolete.patch
Patch34:	%{name}-examplesaredoc.patch
Patch35:	%{name}-po.patch
Patch36:	%{name}-amd64.patch
Patch37:	%{name}-notsc.patch
Patch38:	%{name}-hack-norpmlibdep.patch
Patch39:	%{name}-db42.patch
Patch40:	%{name}-makefile-no_myLDADD_deps.patch
Patch41:	%{name}-libdir64.patch
Patch42:	%{name}-libdir-links.patch
Patch43:	%{name}-python-libdir.patch
URL:		http://www.rpm.org/
Icon:		rpm.gif
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	beecrypt-devel >= %{beecrypt_ver}
BuildRequires:	bzip2-devel >= 1.0.1
BuildRequires:	db-devel >= %{reqdb_ver}
%{?with_docs:BuildRequires:	doxygen}
BuildRequires:	gettext-devel >= 0.11.4-2
BuildRequires:	elfutils-devel
#BuildRequires:	libmagic-devel
BuildRequires:	libtool
BuildRequires:	patch >= 2.2
BuildRequires:	popt-devel >= %{reqpopt_ver}
%{?with_python:BuildRequires:	python-devel >= 2.2}
BuildRequires:	python-modules >= 2.2
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	zlib-devel
BuildRequires:  libselinux-devel
%if %{with static}
# Require static library only for static build
BuildRequires:	beecrypt-static >= %{beecrypt_ver}
BuildRequires:	bzip2-static >= 1.0.2-5
BuildRequires:	db-static >= %{reqdb_ver}
BuildRequires:	glibc-static >= 2.2.94
BuildRequires:	elfutils-static
#BuildRequires:	libmagic-static
BuildRequires:	popt-static >= %{reqpopt_ver}
BuildRequires:	zlib-static
%endif
Requires:	popt >= %{reqpopt_ver}
Requires:	%{name}-lib = %{version}-%{release}
Conflicts:	glibc < 2.2.92
# avoid SEGV caused by mixed db versions
Conflicts:	poldek < 0.18.1-16
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_binary_payload	w9.gzdio
%define		_noPayloadPrefix 1

# don't require very fresh rpm.macros to build
%define		__gettextize gettextize --copy --force --intl ; cp -f po/Makevars{.template,}

# stabilize new build environment
%define		__cc %{?force_cc}%{!?force_cc:%{_target_cpu}-pld-linux-gcc}
%define		__cxx %{?force_cxx}%{!?force_cxx:%{_target_cpu}-pld-linux-g++}
%define		__cpp %{?force_cpp}%{!?force_cpp:%{_target_cpu}-pld-linux-gcc -E}

%define		_rpmlibdir /usr/lib/rpm

%description
RPM is a powerful package manager, which can be used to build,
install, query, verify, update, and uninstall individual software
packages. A package consists of an archive of files, and package
information, including name, version, and description.

%description -l de
RPM ist ein kr�ftiger Packet-Manager, der verwendet sein kann zur
Installation, Anfrage, Verifizierung, Aktualisierung und
Uninstallation individueller Softwarepakete. Ein Paket besteht aus
einem Archiv Dateien und Paketinformation, inklusive Name, Version und
Beschreibung.

%description -l es
RPM es un poderoso administrador de paquetes, que puede ser usado para
construir, instalar, pesquisar, verificar, actualizar y desinstalar
paquetes individuales de software. Un paquete consiste en un
almacenaje de archivos, y informaci�n sobre el paquete, incluyendo
nombre, versi�n y descripci�n.

%description -l pl
RPM jest doskona�ym programem zarz�dzaj�cym pakietami. Umo�liwia on
przebudowanie, instalacj� czy weryfikacj� dowolnego pakietu.
Informacje dotycz�ce ka�dego pakietu, takie jak jego opis, lista
plik�w wchodz�cych w sk�ad pakietu, zale�no�ci od innych pakiet�w, s�
przechowywane w bazie danych i mo�na je uzyska� za pomoc� opcji
odpytywania programu rpm.

%description -l pt_BR
RPM � um poderoso gerenciador de pacotes, que pode ser usado para
construir, instalar, pesquisar, verificar, atualizar e desinstalar
pacotes individuais de software. Um pacote consiste de um conjunto de
arquivos e informa��es adicionais, incluindo nome, vers�o e descri��o
do pacote, permiss�es dos arquivos, etc.

%description -l ru
RPM - ��� ������ �������� �������, ������� ����� ���� ����������� ���
��������, �����������, �������� (query), ��������, ���������� �
�������� ����������� �������. ����� ������� �� ��������� ������ �
��������� ����������, ���������� ��������, ������, �������� � ������
������ � ������.

%description -l uk
RPM - �� �������� �������� ����Ԧ�, �� ���� ���� ������������ ���
���������, �������æ�, ����Ԧ� (query), ����צ���, ���������� ��
��������� ���������� ����Ԧ�. ����� ����������� � ��������� ��Ȧ�� ��
�������ϧ �������æ�, �� ͦ����� �����, ���Ӧ�, ���� �� ����
�������æ� ��� �����.

%package devel
Summary:	Header files for rpm libraries
Summary(de):	Header-Dateien f�r rpm Libraries
Summary(es):	Archivos de inclusi�n y bibliotecas para programas de manipulaci�n de paquetes rpm
Summary(pl):	Pliki nag��wkowe bibliotek rpm
Summary(pt_BR):	Arquivos de inclus�o e bibliotecas para programas de manipula��o de pacotes RPM
Summary(ru):	������ � ���������� ��� ��������, ���������� � rpm-��������
Summary(uk):	������ �� ¦�̦����� ��� �������, �� �������� � �������� rpm
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}
Requires:	beecrypt-devel >= %{beecrypt_ver}
Requires:	bzip2-devel
Requires:	db-devel
Requires:	elfutils-devel
Requires:	libselinux-devel
Requires:	popt-devel >= %{reqpopt_ver}
Requires:	zlib-devel

%description devel
The RPM packaging system includes C libraries that make it easy to
manipulate RPM packages and databases. They are intended to ease the
creation of graphical package managers and other tools that need
intimate knowledge of RPM packages. This package contains header files
for these libraries.

%description devel -l de
Der RPM-Packensystem enth�lt eine C-Library, die macht es einfach
RPM-Pakete und Dateibanken zu manipulieren. Er eignet sich f�r
Vereinfachung des Schaffens grafischer Paket-Manager und anderer
Werkzeuge, die intime Kenntnis von RPM-Paketen brauchen.

%description devel -l es
El sistema de empaquetado RPM incluye una biblioteca C que vuelve
f�cil la manipulaci�n de paquetes y bases de datos RPM. Su objetivo es
facilitar la creaci�n de administradores gr�ficos de paquetes y otras
herramientas que necesiten un conocimiento profundo de paquetes RPM.

%description devel -l pl
System RPM zawiera biblioteki C, kt�re u�atwiaj� manipulowanie
pakietami RPM oraz bazami danych. W zamiarze ma to upro�ci� tworzenie
graficznych program�w zarz�dzaj�cych pakietami oraz innych narz�dzi,
kt�re wymagaj� szczeg�owej wiedzy na temat pakiet�w RPM. Ten pakiet
zawiera pliki nag��wkowe wspomnianych bibliotek.

%description devel -l pt_BR
O sistema de empacotamento RPM inclui uma biblioteca C que torna f�cil
a manipula��o de pacotes e bases de dados RPM. Seu objetivo �
facilitar a cria��o de gerenciadores gr�ficos de pacotes e outras
ferramentas que precisem de conhecimento profundo de pacotes RPM.

%description devel -l ru
������� ���������� �������� RPM �������� ���������� C, �������
�������� ����������� �������� RPM � ���������������� ������ ������.
��� ���������� ������������� ��� ���������� �������� �����������
�������� ���������� � ������ ������, ������� ���������� �������� �
�������� RPM.

%description devel -l uk
������� ��������� �������� RPM ͦ����� ¦�̦����� C, ����� �����դ
������ � �������� RPM �� צ���צ����� ������ �����. �� ¦�̦�����
���������� ��� ���������� ��������� ���Ʀ���� �������� �������Ҧ� ��
����� ���̦�, �� �������� � �������� RPM.

%package static
Summary:	RPM static libraries
Summary(de):	RPMs statische Libraries
Summary(pl):	Biblioteki statyczne RPM-a
Summary(pt_BR):	Bibliotecas est�ticas para o desenvolvimento de aplica��es RPM
Summary(ru):	����������� ���������� ��� ��������, ���������� � rpm-��������
Summary(uk):	�������� ¦�̦����� ��� �������, �� �������� � �������� rpm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	beecrypt-static >= %{beecrypt_ver}
Requires:	bzip2-static
Requires:	db-static
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
Bibliotecas est�ticas para desenvolvimento.

%description static -l ru
������� ���������� �������� RPM �������� ���������� C, �������
�������� ����������� �������� RPM � ���������������� ������ ������.
��� ����������� ���������� RPM.

%description static -l uk
������� ��������� �������� RPM ͦ����� ¦�̦����� C, ����� �����դ
������ � �������� RPM �� צ���צ����� ������ �����. �� ��������
¦�̦����� RPM.

%package utils
Summary:	Additional utilities for managing rpm packages and database
Summary(de):	Zusatzwerkzeuge f�r Verwaltung RPM-Pakete und Datenbanken
Summary(pl):	Dodatkowe narz�dzia do zarz�dzania baz� RPM-a i pakietami
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	popt >= %{reqpopt_ver}

%description utils
Additional utilities for managing rpm packages and database.

%description utils -l de
Zusatzwerkzeuge f�r Verwaltung RPM-Pakete und Datenbanken.

%description utils -l pl
Dodatkowe narz�dzia do zarz�dzania baz� RPM-a i pakietami.

%package utils-perl
Summary:	Additional utilities for managing rpm packages and database
Summary(de):	Zusatzwerkzeuge f�r Verwaltung RPM-Pakete und Datenbanken
Summary(pl):	Dodatkowe narz�dzia do zarz�dzania baz� RPM-a i pakietami
Group:		Applications/File
Requires:	%{name}-utils = %{version}-%{release}
Requires:	popt >= %{reqpopt_ver}

%description utils-perl
Additional utilities for managing rpm packages and database.

%description utils-perl -l de
Zusatzwerkzeuge f�r Verwaltung RPM-Pakete und Datenbanken.

%description utils-perl -l pl
Dodatkowe narz�dzia do zarz�dzania baz� RPM-a i pakietami.

%package utils-static
Summary:	Static rpm utilities
Summary(pl):	Statyczne narz�dzia rpm
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils-static
Static rpm utilities for repairing system in case something with
shared libraries used by rpm become broken. Currently it contains rpmi
binary, which can be used to install/upgrade/remove packages without
using shared libraries (well, in fact with exception of NSS modules).

%description utils-static -l pl
Statyczne narz�dzia rpm do naprawy systemu w przypadku zepsucia czego�
zwi�zanego z bibliotekami wsp�dzielonymi u�ywanymi przez rpm-a.
Aktualnie pakiet zawiera binark� rpmi, kt�r� mo�na u�y� do instalacji,
uaktualniania lub usuwania pakiet�w bez udzia�u bibliotek statycznych
(z wyj�tkiem modu��w NSS).

%package perlprov
Summary:	Additional utilities for checking perl provides/requires in rpm packages
Summary(de):	Zusatzwerkzeuge f�rs Nachsehen Perl-Abh�ngigkeiten in RPM-Paketen
Summary(pl):	Dodatkowe narz�dzia do sprawdzenia zale�no�ci skrypt�w perla w pakietach rpm
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	perl-devel
Requires:	perl-modules

%description perlprov
Additional utilities for checking perl provides/requires in rpm
packages.

%description perlprov -l de
Zusatzwerkzeuge f�rs Nachsehen Perl-Abh�ngigkeiten in RPM-Paketen.

%description perlprov -l pl
Dodatkowe narz�dzia do sprawdzenia zale�no�ci skrypt�w perla w
pakietach rpm.

%package pythonprov
Summary:	Python macros, which simplifies creation of rpm packages with Python software
Summary(pl):	Makra u�atwiaj�ce tworzenie pakiet�w rpm z programami napisanymi w Pythonie
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules

%description pythonprov
Python macros, which simplifies creation of rpm packages with Python
software.

%description pythonprov -l pl
Makra u�atwiaj�ce tworzenie pakiet�w rpm z programami napisanymi w
Pythonie.

%package php-pearprov
Summary:	Additional utilities for managing rpm packages and database
Summary(pl):	Dodatkowe narz�dzia do sprawdzania zale�no�ci skrypt�w php w rpm
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}

%description php-pearprov
Additional utilities for checking php pear provides/requires in rpm
packages.

%description php-pearprov -l pl
Dodatkowe narz�dzia do sprawdzenia zale�no�ci skrypt�w php pear w
pakietach rpm.

%package -n python-rpm
Summary:	Python interface to RPM library
Summary(pl):	Pythonowy interfejs do biblioteki RPM-a
Summary(pt_BR):	M�dulo Python para aplicativos que manipulam pacotes RPM
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
Pakiet rpm-python zawiera modu�, kt�ry pozwala aplikacjom napisanym w
Pythonie na u�ywanie interfejsu dostarczanego przez biblioteki RPM-a.

Pakiet ten powinien zosta� zainstalowany, je�li chcesz pisa� w
Pythonie programy manipuluj�ce pakietami i bazami danych rpm.

%description -n python-rpm -l pt_BR
O pacote rpm-python cont�m um m�dulo que permite que aplica��es
escritas em Python utilizem a interface fornecida pelas bibliotecas
RPM (RPM Package Manager).

Esse pacote deve ser instalado se voc� quiser desenvolver programas em
Python para manipular pacotes e bancos de dados RPM.

%package lib
Summary:	RPMs library
Summary(pl):	Biblioteki RPM-a
Group:		Libraries
Requires:	db >= %{reqdb_ver}
Requires:	popt >= %{reqpopt_ver}
# avoid SEGV caused by mixed db versions
Conflicts:	poldek < 0.18.1-16

%description lib
RPMs library.

%description lib -l pl
Biblioteki RPM-a.

%package build
Summary:	Scripts for building binary RPM packages
Summary(de):	Scripts f�rs Bauen bin�rer RPM-Pakete
Summary(pl):	Skrypty pomocnicze do budowania binarnych RPM-�w
Summary(pt_BR):	Scripts e programas execut�veis usados para construir pacotes
Summary(ru):	������� � �������, ����������� ��� ������ �������
Summary(uk):	������� �� ���̦��, ����Ȧ�Φ ��� �������� ����Ԧ�
Group:		Applications/File
Requires(pre):	findutils
Requires:	%{name}-utils = %{version}-%{release}
Requires:	/bin/id
Requires:	awk
Requires:	binutils
Requires:	chrpath
Requires:	diffutils
Requires:	file >= 4.01
Requires:	fileutils
Requires:	findutils
%ifarch athlon
Requires:	gcc >= 3.0.3
%else
Requires:	gcc
%endif
%ifarch amd64
Conflicts:	automake < 1:1.7.9-2
Conflicts:	libtool < 2:1.5-13
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
Provides:	rpmbuild(macros) = %{rpm_macros_rev}

%description build
Scripts for building binary RPM packages.

%description build -l de
Scripts f�rs Bauen bin�rer RPM-Pakete.

%description build -l pl
Skrypty pomocnicze do budowania binarnych RPM-�w.

%description build -l pt_BR
Este pacote cont�m scripts e programas execut�veis que s�o usados para
construir pacotes usando o RPM.

%description build -l ru
��������� ��������������� ������� � ����������� ���������, �������
������������ ��� ������ RPM'��.

%description build -l uk
������Φ�Φ ����ͦ�Φ ������� �� ���̦��, �˦ ���������������� ���
�������� RPM'��.

%package build-tools
Summary:	Scripts for managing .spec files and building RPM packages
Summary(de):	Scripts f�rs Bauen bin�rer RPM-Pakete
Summary(pl):	Skrypty pomocnicze do zarz�dznia plikami .spec i budowania RPM-�w
Summary(pt_BR):	Scripts e programas execut�veis usados para construir pacotes
Summary(ru):	������� � �������, ����������� ��� ������ �������
Summary(uk):	������� �� ���̦��, ����Ȧ�Φ ��� �������� ����Ԧ�
Group:		Applications/File
Requires:	%{name}-build = %{version}-%{release}
# these are optional
#Requires:	cvs
Requires:	wget

%description build-tools
Scripts for managing .spec files and building RPM packages.

%description build-tools -l de
Scripts f�rs Bauen RPM-Pakete.

%description build-tools -l pl
Skrypty pomocnicze do zarz�dzania plikami .spec i do budowania RPM-�w.

%description build-tools -l pt_BR
Este pacote cont�m scripts e programas execut�veis que s�o usados para
construir pacotes usando o RPM.

%description build-tools -l ru
��������� ��������������� ������� � ����������� ���������, �������
������������ ��� ������ RPM'��.

%description build-tools -l uk
������Φ�Φ ����ͦ�Φ ������� �� ���̦��, �˦ ���������������� ���
�������� RPM'��.

%prep
%setup -q
# pl.po translation
#%patch0 -p1
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
%patch11 -p1
# OBSOLETE (C)
#%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
# 1x1h MERGE WITH 14, no - OBSOLETE
#%patch22 -p1
# 3x1h OBSOLETE (already handled in quite well way)
#%patch23 -p1
%patch24 -p1
sed -e 's/^/@pld@/' %{SOURCE2} >>platform.in
cp -f platform.in macros.pld.in
echo '%%define	_perl_deps	1' > macros.perl
echo '# obsoleted file' > macros.python
echo '%%define	_php_deps	1' > macros.php
install %{SOURCE6} scripts/find-lang.sh
install %{SOURCE12} scripts/php.prov.in
install %{SOURCE13} scripts/php.req.in
install %{SOURCE33} scripts/perl.prov
cat %{SOURCE14} >> macros.in
#%patch25 -p1
%patch26 -p1
%patch27 -p1
# obsolete?
#%patch28 -p1
# OBSOLETE
#%patch29 -p1
# OBSOLETE
#%patch30 -p1
# OBSOLETE
#%patch31 -p1
#%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
# OBSOLETE
#%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
# OBSOLETE
#%patch43 -p1

cd scripts;
mv -f perl.req perl.req.in
mv -f perl.prov perl.prov.in
cd ..

rm -rf zlib libelf db db3 popt rpmdb/db.h

# generate Group translations to *.po
awk -f %{SOURCE9} %{SOURCE1}

# update macros paths
for f in doc{,/ja,/pl}/rpm.8 doc{,/ja,/pl}/rpmbuild.8 ; do
	sed -e 's@lib/rpm/redhat@lib/rpm/pld@g' $f > ${f}.tmp
	mv -f ${f}.tmp $f
done

%build
cd file
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
	%{?with_docs:--with-apidocs} \
	%{?with_python:--with-python=auto} \
	%{!?with_python:--without-python} \
	--without-db

%{__make} \
	%{!?with_static:rpm_LDFLAGS="\$(myLDFLAGS)"} \
	myLDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgbindir="%{_bindir}"

rm $RPM_BUILD_ROOT%{_rpmlibdir}/vpkg-provides*
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-{prov,req}.pl
rm $RPM_BUILD_ROOT%{_rpmlibdir}/find-{provides,requires}.perl

install macros.perl	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.perl
install macros.python	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.python
install macros.php	$RPM_BUILD_ROOT%{_rpmlibdir}/macros.php

install %{SOURCE1} doc/manual/groups
install %{SOURCE3} $RPM_BUILD_ROOT%{_rpmlibdir}/install-build-tree
install %{SOURCE5} $RPM_BUILD_ROOT%{_rpmlibdir}/find-spec-bcond
install %{SOURCE10} $RPM_BUILD_ROOT%{_rpmlibdir}/compress-doc
install %{SOURCE11} $RPM_BUILD_ROOT%{_rpmlibdir}/check-files
install scripts/find-php*	$RPM_BUILD_ROOT%{_rpmlibdir}
install scripts/php.{prov,req}	$RPM_BUILD_ROOT%{_rpmlibdir}

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

cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprovfiles <<EOF
# global list of files (name regexps) which don't generate Provides
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoprov <<EOF
# global list of capabilities (regexps) not to be used in Provides
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreqfiles <<EOF
# global list of files (name regexps) which don't generate Requires
/usr/src/examples/.*
/usr/share/doc/.*
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreq <<EOF
# global list of capabilities (regexps) not to be used in Requires
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautoreqdep <<EOF
# global list of capabilities (SONAME, perl(module), php(module) regexps)
# which don't generate dependencies on package NAMES
libGL.so.1
libGLU.so.1
libOSMesa.so.4
libglide3.so.3
libgtkmozembed.so
libgtksuperwin.so
libxpcom.so
EOF
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/noautocompressdoc <<EOF
# global list of file masks not to be compressed in DOCDIR
EOF

# for rpm -e|-U --repackage
install -d $RPM_BUILD_ROOT/var/spool/repackage

# move libs to /lib
for a in librpm-%{ver}.so librpmdb-%{ver}.so librpmio-%{ver}.so ; do
	mv -f $RPM_BUILD_ROOT%{_libdir}/$a $RPM_BUILD_ROOT/%{_lib}
	ln -s /%{_lib}/$a $RPM_BUILD_ROOT%{_libdir}/$a
done

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

%{_mandir}/man8/rpm.8*
%lang(fr) %{_mandir}/fr/man8/rpm.8*
%lang(ja) %{_mandir}/ja/man8/rpm.8*
%lang(ko) %{_mandir}/ko/man8/rpm.8*
%lang(pl) %{_mandir}/pl/man8/rpm.8*
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%lang(sk) %{_mandir}/sk/man8/rpm.8*

%dir /var/lib/rpm
%dir %attr(700,root,root) /var/spool/repackage

%dir %{_rpmlibdir}
#%attr(755,root,root) %{_rpmlibdir}/rpmd
#%attr(755,root,root) %{_rpmlibdir}/rpmk
#%attr(755,root,root) %{_rpmlibdir}/rpm[qv]

%doc %attr(755,root,root) %{_rpmlibdir}/convertrpmrc.sh

%{_rpmlibdir}/rpmrc
%{_rpmlibdir}/rpmpopt*
%{_rpmlibdir}/macros

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/librpm*-*.so
%attr(755,root,root) %{_libdir}/librpm*-*.so

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
%attr(755,root,root) %{_rpmlibdir}/http.req
%attr(755,root,root) %{_rpmlibdir}/magic.prov
%attr(755,root,root) %{_rpmlibdir}/magic.req
%attr(755,root,root) %{_rpmlibdir}/u_pkg.sh
#%attr(755,root,root) %{_rpmlibdir}/vpkg-provides.sh
#%attr(755,root,root) %{_rpmlibdir}/vpkg-provides2.sh
%attr(755,root,root) %{_rpmlibdir}/rpmb
%attr(755,root,root) %{_rpmlibdir}/rpmt
%{_rpmlibdir}/noarch-*
%ifarch i386 i486 i586 i686 athlon
%{_rpmlibdir}/i?86*
%{_rpmlibdir}/athlon*
%endif
%ifarch amd64
%{_rpmlibdir}/amd64*
%{_rpmlibdir}/x86_64*
%endif
%ifarch sparc sparc64
%{_rpmlibdir}/sparc*
%endif
%ifarch alpha
%{_rpmlibdir}/alpha*
%endif
%ifarch ppc
%{_rpmlibdir}/ppc*
%endif
# must be here for "Requires: rpm-*prov" to work
%{_rpmlibdir}/macros.perl
%{_rpmlibdir}/macros.php
# not used yet ...
%{_rpmlibdir}/sql.prov
%{_rpmlibdir}/sql.req
%{_rpmlibdir}/tcl.req
%{_rpmlibdir}/trpm

%attr(755,root,root) %{_bindir}/javadeps
%attr(755,root,root) %{_bindir}/gendiff
%attr(755,root,root) %{_bindir}/rpmbuild

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%lang(ja) %{_mandir}/ja/man8/rpmbuild.8*
%lang(pl) %{_mandir}/pl/man1/gendiff.1*
%lang(pl) %{_mandir}/pl/man8/rpmbuild.8*

%files devel
%defattr(644,root,root,755)
%{_includedir}/rpm
%{_libdir}/librpm*.la
%attr(755,root,root) %{_libdir}/librpm.so
%attr(755,root,root) %{_libdir}/librpmio.so
%attr(755,root,root) %{_libdir}/librpmdb.so
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

%files utils-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/rpmdiff*
# not here
#%%{_rpmlibdir}/rpm.daily
#%%{_rpmlibdir}/rpm.log
#%%{_rpmlibdir}/rpm.xinetd

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

%files utils-static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpm[ieu]
%attr(755,root,root) %{_rpmlibdir}/rpm[ieu]

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

%files php-pearprov
%defattr(644,root,root,755)
%attr(755,root,root) %{_rpmlibdir}/php*
%attr(755,root,root) %{_rpmlibdir}/find-php*

%if %{with python}
%files -n python-rpm
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%attr(755,root,root) %{py_sitedir}/rpmdb/*.so
%{py_sitedir}/rpmdb/*.py*
%endif

%files build-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/builder
%attr(755,root,root) %{_bindir}/adapter.awk
%attr(755,root,root) %{_bindir}/pldnotify.awk
