Summary:	Red Hat & PLD Package Manager
Summary(pl):	Aplikacja do zarz±dzania pakietami
Name:		rpm
Version:	3.0.5
Release:	10
Group:		Base
Group(pl):	Podstawowe
License:	GPL
Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-3.0.x/%{name}-%{version}.tar.gz
Source1:	rpm.groups
Source2:	rpm.macros
Source3:	rpm-remove-unneeded-elf-sections
Source5:	rpm-install-tree
Patch0:		rpm-rpmrc.patch
Patch1:		rpm-find-requires.patch
Patch2:		rpm-macros.patch
Patch3:		rpm-arch.patch
Patch4:		rpm-rpmpopt.patch
Patch5:		rpm-find-provides.patch
Patch6:		rpm-perl-macros.patch
Patch7:		rpm-find-lang-all-name.patch
Patch8:		rpm-file3.31.patch
Patch9:		rpm-find-lang-name-matching.patch
Patch10:	rpm-exclude-examples-doc.patch
Patch11:	rpm-db3.patch
Patch37:        %{name}-short_circuit.patch
Patch38:        %{name}-section_test.patch
BuildRequires:	bzip2-static >= 1.0.1
BuildRequires:	gdbm-static
BuildRequires:	zlib-static
BuildRequires:	gettext-devel >= 0.10.38-3
BuildRequires:	libtool
BuildRequires:	automake
BuildRequires:	autoconf >= 2.13-8
BuildRequires:	gettext-devel
BuildRequires:	db3-devel
Requires:	glibc >= 2.1
BuildRequires:	zlib-static >= 1.1.4
Obsoletes:	rpm-libs
%define		pyrequires_eq() Requires:	%1 >= %py_ver %1 < %(echo `python -c "import sys; import string; ver=sys.version[:3].split('.'); ver[1]=str(int(ver[1])+1); print string.join(ver, '.')"`)
RPM is a powerful package manager, which can be used to build, install, 
query, verify, update, and uninstall individual software packages. A 
package consists of an archive of files, and package information, including 
name, version, and description.
packages. A package consists of an archive of files, and package
nombre, versión y descripción.
RPM jest doskona³ym menad¿erem pakietów. Dziêki niemu bêdziesz móg³ przebudowaæ,
zainstalowaæ czy zweryfikowaæ dowolny pakiet. 
Informacje dotycz±ce ka¿dego pakietu, takie jak jego opis, lista plików
wchodz±cych w sk³ad pakietu, zalezno¶ci od innych pakietów
s± przechowywane s± w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
wchodz±cych w sk³ad pakietu, zale¿no¶ci od innych pakietów, s±
przechowywane w bazie danych i mo¿na je uzyskaæ za pomoc± opcji
%package libs
Summary:	RPM shared libraries
Summary(pl):	Biblioteki wspó³dzielone rpm-a
Group:		Libraries
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
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-libs = %{version}
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
Group(pl):	Programowanie/Biblioteki
Summary(pt_BR):	Bibliotecas estáticas para o desenvolvimento de aplicações RPM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
%description -l pl static
Biblioteki statyczne rpm-a.
%description static -l pl
Bibliotecas estáticas para desenvolvimento.

Summary(pl):	Dodatkowe narzêdzia do zarz±dzanai baz± rpm-a i pakietami
Group:		Utilities/File
Group(pl):	Narzêdzia/Pliki
Summary(pl):	Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami
Group:		Applications/File
Requires:	%{name} = %{version}

%description utils
%description -l pl utils
Dodatkowe narzêdzia do zarz±dzanai baz± rpm-a i pakietami.
%description utils -l pl
Dodatkowe narzêdzia do zarz±dzania baz± RPM-a i pakietami.
Summary:	Additional utilities for check perl provides/requires in rpm packages
Summary(pl):	Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci dla skryptów perl w pakietach rpm
Group:		Utilities/File
Group(pl):	Narzêdzia/Pliki
Summary(pl):	Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów perla w pakietach rpm
Requires:	perl-modules
Requires:	findutils
Additional utilities for check perl provides/requires in rpm packages.
Additional utilities for checking perl provides/requires in rpm
%description -l pl perlprov
Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci dla skryptów perl 
w pakietach rpm.
Dodatkowe narzêdzia do sprawdzenia zale¿no¶ci skryptów perla w
Python para manipular pacotes e bancos de dados RPM.

Summary(pl):	Skrypty pomocnicze do budowania binarnych RPMów
Group:		Utilities/File
Group(pl):	Narzêdzia/Pliki
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
%patch10 -p1
%patch11 -p1
%patch31 -p1
install %{SOURCE2} macros.pld.in
install %{SOURCE13} macros.python.in
(cd scripts; 
mv perl.req perl.req.in
mv perl.prov perl.prov.in)

mv -f perl.prov perl.prov.in)
LDFLAGS="-s"; export LDFLAGS

(cd popt;
 libtoolize --force --copy
 aclocal
 autoheader
 automake --add-missing --gnu
 autoconf)
autoheader
%{__automake}

autoheader
automake --add-missing --gnu
autoconf
%configure \
	--enable-shared
%configure \
%{__make}
	--with-python


%{__make} %{?_without_static:rpm_LDFLAGS="\\$(myLDFLAGS)"}
install -d $RPM_BUILD_ROOT/var/lib/rpm \
	$RPM_BUILD_ROOT%{_mandir}/{ru,pl}/man8

%{__make} DESTDIR="$RPM_BUILD_ROOT" pkgbindir="%{_bindir}" install

install macros.pld $RPM_BUILD_ROOT%{_libdir}/rpm/macros.pld
%{__make} install \
install %{SOURCE3} $RPM_BUILD_ROOT%{_libdir}/rpm/remove-unneeded-elf-sections
install %{SOURCE5} $RPM_BUILD_ROOT%{_libdir}/rpm/install-build-tree
	pkgbindir="%{_bindir}"

install %{SOURCE8} $RPM_BUILD_ROOT%{_libdir}/rpm/find-spec-bcond
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*

#%%_install_langs pl_PL:en_US
%%distribution PLD
EOF

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/{{ja,ru,pl}/man8/*,man8/*} \
	RPM-PGP-KEY CHANGES doc/manual/*

%pre
if [ -L /var/lib/rpm ]; then
	echo "WARNING: upgrade cannot be done because /var/state/rpm is symlink"
	exit 1
fi
if [ ! -d /var/lib/rpm ]; then 
	if [ -e /var/state/rpm ] && [ ! -L /var/state/rpm ]; then
		mkdir -p /var/lib/rpm
		cp -ap /var/state/rpm/* /var/lib/rpm
		rm -rf /var/state/rpm
		ln -sf /var/lib/rpm /var/state/rpm
		echo "RPM Database moved from /var/state/rpm to /var/lib/rpm" 1>&2
		echo "Run second time upgradeing rpm package for complete operation" 1>&2
		exit 1
	fi
	if [ -e /var/db/rpm ] && [ ! -L /var/db/rpm ]; then
		mkdir -p /var/lib/rpm
		cp -ap /var/db/rpm/* /var/lib/rpm
		rm -rf /var/db/rpm
		ln -sf /var/lib/rpm /var/db/rpm
		echo "RPM Database moved from /var/db/rpm to /var/lib/rpm" 1>&2
		echo "Run second time upgradeing rpm package for complete operation" 1>&2
		exit 1
	fi
fi

%post
if [ -L /var/lib/rpm ]; then
	rm -rf /var/lib/rpm
fi
if [ -L /var/db/rpm ]; then
	rm -rf /var/db/rpm
fi
if [ ! -f /var/lib/rpm/packages.rpm ]; then
	/bin/rpm --initdb
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
%clean
%clean
rm -rf $RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%attr(755,root,root) %{_libdir}/rpm/rpmdb
%attr(755,root,root) %{_libdir}/librpm*.so.*.*
%{_mandir}/man8/rpm.8*
%lang(pl) %{_mandir}/pl/man8/rpm.8*
%lang(ja) %{_mandir}/ja/man8/rpm.8*
%lang(ja) %{_mandir}/ja/man8/rpm.8*
%lang(ko) %{_mandir}/ko/man8/rpm.8*
%dir /usr/lib/rpm
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%lang(sk) %{_mandir}/sk/man8/rpm.8*

%dir /var/lib/rpm
%{_libdir}/rpm/rpmpopt

%{_libdir}/rpm/macros.pld

%ifarch ppc
%{_libdir}/rpm/ppc*
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpmbuild
%attr(755,root,root) %{_bindir}/rpmu
%attr(755,root,root) %{_libdir}/rpm/find-requires
%attr(755,root,root) %{_libdir}/rpm/find-provides
%attr(755,root,root) %{_libdir}/rpm/find-rpm-provides
%attr(755,root,root) %{_libdir}/rpm/find-spec-bcond
%attr(755,root,root) %{_libdir}/rpm/remove-unneeded-elf-sections
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
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man8/rpm2cpio.8*
%lang(ko) %{_mandir}/ko/man8/rpm2cpio.8*
%lang(pl) %{_mandir}/pl/man8/rpm2cpio.8*
%lang(ru) %{_mandir}/ru/man8/rpm2cpio.8*
%attr(755,root,root) %{_libdir}/rpm/find-perl-*
%attr(755,root,root) %{_libdir}/rpm/find-*.perl
%attr(755,root,root) %{_libdir}/rpm/find-prov.pl

%files -n python-rpm
* %{date} PLD Team <pld-list@pld.org.pl>
%{py_sitedir}/*.so
