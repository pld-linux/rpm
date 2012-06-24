Summary:	Red Hat & PLD Package Manager
Summary(pl):	Aplikacja do zarz�dzania pakietami
Name:		rpm
Version:	3.0.3
Release:	27
Group:		Base
Group(pl):	Podstawowe
Copyright:	GPL
Source0:	ftp://ftp.rpm.org/pub/rpm/dist/rpm-3.0.x/%{name}-%{version}.tar.gz
Source1:	rpm.groups
Source3:	rpm.macros
Source5:	rpm-install-tree
Patch0:		rpm-rpmrc.patch
Patch1:		rpm-find-requires.patch
Patch2:		rpm-macros.patch
Patch3:		rpm-arch.patch
Patch4:		rpm-pld.patch
Patch5:		rpm-rpmpopt.patch
Patch6:		rpm-findlangs.patch
Patch7:		rpm-perl-macros.patch
Patch8:		rpm-nodeps.patch
Patch9:		rpm-find-provides.patch
Patch37:        %{name}-short_circuit.patch
Patch38:        %{name}-section_test.patch
BuildRequires:	bzip2-static
BuildRequires:	gdbm-static
BuildRequires:	zlib-static
BuildRequires:	gettext-devel >= 0.10.38-3
BuildRequires:	libtool
BuildRequires:	automake
BuildRequires:	autoconf >= 2.13-8
BuildRequires:	gettext-devel
Requires:	glibc >= 2.1
BuildRoot:	/tmp/%{name}-%{version}-root
Obsoletes:	rpm-libs
%define		pyrequires_eq() Requires:	%1 >= %py_ver %1 < %(echo `python -c "import sys; import string; ver=sys.version[:3].split('.'); ver[1]=str(int(ver[1])+1); print string.join(ver, '.')"`)
RPM is a powerful package manager, which can be used to build, install, 
query, verify, update, and uninstall individual software packages. A 
package consists of an archive of files, and package information, including 
name, version, and description.
packages. A package consists of an archive of files, and package
nombre, versi�n y descripci�n.
RPM jest doskona�ym menad�erem pakiet�w. Dzi�ki niemu b�dziesz m�g� przebudowa�,
zainstalowa� czy zweryfikowa� dowolny pakiet. Informacje dotycz�ce ka�dego 
pakietu s� przechowywane w bazie danych i dost�pne tylko dla administratora 
systemu.
przechowywane w bazie danych i mo�na je uzyska� za pomoc� opcji
%package libs
Summary:	RPM shared libraries
Summary(pl):	Biblioteki wsp�dzielone rpm-a
Group:		Libraries
Group(pl):	Biblioteki
Requires:	%{name} = %{version}

%description libs
RPM shared libraries.

%description -l pl libs
Biblioteki wsp�dzielone rpm-a.

do pacote, permiss�es dos arquivos, etc.
Summary:	Header files and libraries 
Summary(pl):	Pliki nag��wkowe i biblioteki statyczne	
Summary(pl):	Pliki nag��wkowe i biblioteki statyczne
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-libs = %{version}
Requires:	%{name} = %{version}
Requires:	popt-devel

%description devel
The RPM packaging system includes a C library that makes it easy to
manipulate RPM packages and databases. It is intended to ease the
creation of graphical package managers and other tools that need
%description -l pl devel
Pliki nag��wkowe i biblioteki statyczne.
graficznych mened�er�w pakiet�w oraz innych narz�dzi, kt�re wymagaj�
ferramentas que precisem de conhecimento profundo de pacotes RPM.

Summary(pl):	Biblioteki statyczne rpm-a
Summary(pl):	Biblioteki statyczne RPM-a
Group(pl):	Programowanie/Biblioteki
Summary(pt_BR):	Bibliotecas est�ticas para o desenvolvimento de aplica��es RPM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
%description -l pl static
Biblioteki statyczne rpm-a.
%description static -l pl
Bibliotecas est�ticas para desenvolvimento.

Summary(pl):	Dodatkowe narz�dzia do zarz�dzanai baz� rpm-a i pakietami
Group:		Utilities/File
Group(pl):	Narz�dzia/Pliki
Summary(pl):	Dodatkowe narz�dzia do zarz�dzania baz� RPM-a i pakietami
Group:		Applications/File
Requires:	%{name} = %{version}

%description utils
%description -l pl utils
Dodatkowe narz�dzia do zarz�dzanai baz� rpm-a i pakietami.
%description utils -l pl
Dodatkowe narz�dzia do zarz�dzania baz� RPM-a i pakietami.
Summary:	Additional utilities for check perl provides/requires in rpm packages
Summary(pl):	Dodatkowe narz�dzia do sprawdzenia zale�no�ci dla skrypt�w perl w pakietach rpm
Group:		Utilities/File
Group(pl):	Narz�dzia/Pliki
Summary(pl):	Dodatkowe narz�dzia do sprawdzenia zale�no�ci skrypt�w perla w pakietach rpm
Requires:	perl-modules
Requires:	findutils
Additional utilities for check perl provides/requires in rpm packages.
Additional utilities for checking perl provides/requires in rpm
%description -l pl perlprov
Dodatkowe narz�dzia do sprawdzenia zale�no�ci dla skrypt�w perl 
w pakietach rpm.
Dodatkowe narz�dzia do sprawdzenia zale�no�ci skrypt�w perla w
construir pacotes usando o RPM.
%setup  -q
%patch0 -p0
%patch1 -p1
%patch0 -p1
%patch1 -p1
%patch4 -p1 
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch31 -p1
install %{SOURCE3} macros.pld.in
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
make
	--with-python


%{__make} %{?_without_static:rpm_LDFLAGS="\\$(myLDFLAGS)"}
install -d $RPM_BUILD_ROOT/var/state/rpm \
	$RPM_BUILD_ROOT%{_mandir}/{ru,pl}/man8

make DESTDIR="$RPM_BUILD_ROOT" pkgbindir="%{_bindir}" install

install macros.pld	 $RPM_BUILD_ROOT%{_libdir}/rpm/macros.pld
install macros.perl	 $RPM_BUILD_ROOT%{_libdir}/rpm/macros.perl
install -m755 %{SOURCE5} $RPM_BUILD_ROOT%{_libdir}/rpm/install-build-tree
	pkgbindir="%{_bindir}"

install %{SOURCE8} $RPM_BUILD_ROOT%{_libdir}/rpm/find-spec-bcond
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*

#%%_install_langs pl_PL:en_US
%%distribution PLD
EOF

gzip -9fn $RPM_BUILD_ROOT%{_mandir}/{{ru,pl}/man8/*,man8/*} \
	RPM-PGP-KEY CHANGES doc/manual/*

%pre
if [ -L /var/state/rpm ]; then
	echo "WARNING: upgrade cannot be done because /var/state/rpm is symlink"
	exit 1
fi
if [ ! -d /var/state/rpm ]; then 
	if [ -e /var/lib/rpm ] && [ ! -L /var/lib/rpm ]; then
		mkdir -p /var/state/rpm
		cp -ap /var/lib/rpm/* /var/state/rpm
		rm -rf /var/lib/rpm
		ln -sf /var/state/rpm /var/lib/rpm
		echo "RPM Database moved from /var/lib/rpm to /var/state/rpm" 1>&2
		echo "Run second time upgradeing rpm package for complete operation" 1>&2
		exit 1
	fi
	if [ -e /var/db/rpm ] && [ ! -L /var/db/rpm ]; then
		mkdir -p /var/state/rpm
		cp -ap /var/db/rpm/* /var/state/rpm
		rm -rf /var/db/rpm
		ln -sf /var/state/rpm /var/db/rpm
		echo "RPM Database moved from /var/db/rpm to /var/state/rpm" 1>&2
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
if [ ! -f /var/state/rpm/packages.rpm ]; then
	/bin/rpm --initdb
fi

%clean
rm -rf $RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%attr(755,root,root) %{_libdir}/rpm/rpmdb
%attr(755,root,root) %{_libdir}/librpm*.so.*.*
%{_mandir}/man8/rpm.8*
%lang(pl) %{_mandir}/pl/man8/rpm.8*
%lang(ru) %{_mandir}/ru/man8/rpm.8*
%attr(755,root,root) %dir /var/state/rpm

%dir /usr/lib/rpm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rpmbuild
%attr(755,root,root) %{_bindir}/rpmu
%attr(755,root,root) %{_libdir}/rpm/freshen.sh
%attr(755,root,root) %{_libdir}/rpm/find-requires
%attr(755,root,root) %{_libdir}/rpm/find-provides
%attr(755,root,root) %{_libdir}/rpm/find-rpm-provides
%attr(755,root,root) %{_libdir}/rpm/find-spec-bcond
%attr(755,root,root) %{_libdir}/rpm/convertrpmrc.sh

%{_libdir}/rpm/rpm*
%{_libdir}/rpm/macros
%{_libdir}/rpm/macros.pld
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
