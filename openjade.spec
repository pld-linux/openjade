%define		_pre	pre1
%define		_rel	13
Summary:	OpenJade - DSSSL parser
Summary(pl.UTF-8):	OpenJade - parser DSSSL
Name:		openjade
Version:	1.3.3
Release:	0.%{_pre}.%{_rel}
Epoch:		1
License:	Free (Copyright (C) 1999 The OpenJade group)
Group:		Applications/Publishing/SGML
Source0:	http://dl.sourceforge.net/openjade/%{name}-%{version}-%{_pre}.tar.gz
# Source0-md5:	cbf3d8be3e3516dcb12b751de822b48c
Patch0:		%{name}-nls-from-1.4.patch
Patch1:		%{name}-as-needed.patch
Patch2:		%{name}-gcc4.patch
Patch3:		perl-getopts.patch
URL:		http://openjade.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	libtool
BuildRequires:	opensp-devel >= 2:1.5.1
BuildRequires:	perl-base
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	sgml-common
Requires:	opensp >= 1.5-2
Requires:	sgml-common
Requires:	sgmlparser
Provides:	dssslparser
Provides:	jade
Obsoletes:	jade
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sgmldir		/usr/share/sgml
%define		_datadir	%{sgmldir}/%{name}-%{version}

%description
Jade (James' DSSSL Engine) is an implementation of the DSSSL style
language. OpenJade is successor of Jade.

%description -l pl.UTF-8
Jade (James' DSSSL Engine) jest implementacją parsera DSSSL. OpenJade
jest następcą Jade.

%package devel
Summary:	OpenJade header files
Summary(pl.UTF-8):	Pliki nagłówkowe do bibliotek OpenJade
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	/sbin/ldconfig

%description devel
Openjade header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe do bibliotek OpenJade.

%package static
Summary:	OpenJade static libraries
Summary(pl.UTF-8):	Biblioteki statyczne OpenJade
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
OpenJade static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OpenJade.

%prep
%setup -q -n %{name}-%{version}-%{_pre}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
%{__sed} -i -e 's@AM_GNU_GETTEXT.*@AM_GNU_GETTEXT([external])@' \
	config/configure.in
# fix segfault https://bugzilla.redhat.com/show_bug.cgi?id=1306162
export CXXFLAGS="%{rpmcxxflags} -fno-tree-dse"
LDFLAGS=""; export LDFLAGS
ln -sf config/configure.in .
# smr_SWITCH and OJ_SIZE_T_IS_UINT
tail -n +3349 config/aclocal.m4 | head -n 64 > acinclude.m4
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
# Ugly hack to avoid error:
# configure: error: cannot find required auxiliary files: compile missing
#
# Proper way would be to use automake which creates these files,
# but then it fails complaining that no Makefile.am exists
cd config
touch compile missing
cd ..
%configure \
	--enable-default-catalog=%{_sysconfdir}/sgml/catalog \
	--enable-default-search-path=%{_prefix}/share/sgml \
	--enable-mif \
	--enable-html \
	--enable-threads \
	--enable-splibdir=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	localedir=%{_prefix}/share/locale

# simulate jade
ln -sf openjade $RPM_BUILD_ROOT%{_bindir}/jade

# files present in openjade 1.4
install dsssl/{catalog,dsssl.dtd,extensions.dsl,fot.dtd,style-sheet.dtd} \
$RPM_BUILD_ROOT%{_datadir}
install -d $RPM_BUILD_ROOT%{_includedir}/OpenJade
install include/*.h grove/Node.h spgrove/{GroveApp,GroveBuilder}.h \
	style/{DssslApp,FOTBuilder}.h $RPM_BUILD_ROOT%{_includedir}/OpenJade

%find_lang jade

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if ! grep -q %{_sysconfdir}/sgml/openjade.cat %{_sysconfdir}/sgml/catalog ; then
%{_bindir}/install-catalog --add %{_sysconfdir}/sgml/openjade.cat \
%{_datadir}/catalog
elif grep -sq %{_prefix}/share/OpenJade/catalog %{_sysconfdir}/sgml/openjade.cat ; then
	# upgrade
%{_bindir}/install-catalog --remove %{_sysconfdir}/sgml/openjade.cat \
%{_prefix}/share/OpenJade/catalog
%{_bindir}/install-catalog --add %{_sysconfdir}/sgml/openjade.cat \
%{_datadir}/catalog
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ] ; then
%{_bindir}/install-catalog --remove %{_sysconfdir}/sgml/openjade.cat \
%{_datadir}/catalog
fi

%files -f jade.lang
%defattr(644,root,root,755)
%doc COPYING ChangeLog NEWS README doc/*.htm jadedoc
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.0
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_datadir}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/OpenJade

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
