%define		pre	1
Summary:	OpenJade -- DSSSL parser
Summary(pl):	OpenJade -- parser DSSSL
Name:		openjade
Version:	1.3.3
Release:	0.pre%{pre}.1
Epoch:		1
License:	Free (Copyright (C) 1999 The OpenJade group)
Group:		Applications/Publishing/SGML
# Source0-md5:	cbf3d8be3e3516dcb12b751de822b48c
Source0:	http://download.sourceforge.net/openjade/%{name}-%{version}-pre%{pre}.tar.gz
URL:		http://openjade.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	opensp-devel >= 1:1.5-3
BuildRequires:	perl
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	sgml-common
Requires:	opensp >= 1.5-2
Requires:	sgml-common
Requires:	sgmlparser
Provides:	jade
Provides:	dssslparser
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	jade

%description
Jade (James' DSSSL Engine) is an implementation of the DSSSL style
language. OpenJade is successor of Jade.

%description -l pl
Jade (James' DSSSL Engine) jest implementacj± parsera DSSSL. OpenJade
jest nastêpc± Jade.

%package devel
Summary:	OpenJade header files
Summary(pl):	Pliki nag³ówkowe do bibliotek OpenJade
Group:		Development/Libraries
Prereq:		/sbin/ldconfig
Requires:	%{name} = %{version}

%description devel
Openjade header files.

%description devel -l pl
Pliki nag³ówkowe do bibliotek OpenJade.

%package static
Summary:	OpenJade static libraries
Summary(pl):	Biblioteki statyczne OpenJade
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
OpenJade static libraries.

%description static -l pl
Biblioteki statyczne OpenJade.

%prep
%setup -q -n openjade-%{version}-pre%{pre}

%build
#remove CVS dirs
find . -type d -name CVS -exec rm -rf {} \;
#missing files required by Makefile.am
LDFLAGS=""; export LDFLAGS
%configure \
	--enable-default-catalog=/etc/sgml/catalog \
	--enable-default-search-path=/usr/share/sgml \
	--enable-mif \
	--enable-html \
	--enable-threads \
	--enable-splibdir=%{_libdir}

# it has /usr/share/Openjade hardcoded somewhere so it does not work
	# --datadir=%{_datadir}/sgml

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml

%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	pkgdocdir=%{_defaultdocdir}/%{name}-%{version} 

ln -sf "../OpenJade" $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}-%{version}

# simulate jade
ln -sf openjade $RPM_BUILD_ROOT%{_bindir}/jade

%find_lang jade

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if ! grep -q /etc/sgml/openjade.cat /etc/sgml/catalog ; then
	/usr/bin/install-catalog --add /etc/sgml/openjade.cat \
		%{_datadir}/OpenJade/catalog
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ] ; then
	/usr/bin/install-catalog --remove /etc/sgml/openjade.cat \
		%{_datadir}/OpenJade/catalog
fi

%files -f jade.lang
%defattr(644,root,root,755)
%doc %{_defaultdocdir}/%{name}-%{version}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_datadir}/sgml/*
%{_datadir}/OpenJade

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenJade
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
