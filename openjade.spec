Summary:	OpenJade -- DSSSL parser
Summary(pl):	OpenJade -- parser DSSSL
Name: 		openjade
Version: 	1.4
Release: 	3.20000320
Provides:	dssslparser
Prereq:		%{_sbindir}/fix-sgml-catalog
Requires: 	sgml-common
Requires:	sgmlparser
Requires: 	opensp >= 1.4-2
Copyright:      Copyright (c) 1999 The OpenJade group (free)
Group:  	Applications/Publishing/SGML
Group(pl):      Aplikacje/Publikowanie/SGML
#Source:         http://download.sourceforge.net/openjade/%{name}-%{version}.tar.gz
Source:         %{name}-20000320.tar.gz
Patch0:		%{name}-DESTDIR.patch
URL:            http://openjade.sourceforge.net/
BuildRequires:	opensp-devel >= 1.4-2
BuildRequires:	perl
BuildRequires:	gettext-devel
Provides:	jade
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	jade

%description
Jade (James' DSSSL Engine) is an implementation of the DSSSL style language.
OpenJade is successor of Jade.

%description -l pl
Jade (James' DSSSL Engine) jest implementacj± parsera DSSSL.
OpenJade jest nastêpc± Jade

%package devel
Summary:	OpenJade header files
Summary(pl):	Pliki nag³ówkowe do bibliotek OpenJade
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Openjade header files.

%description -l pl devel
Pliki nag³ówkowe do bibliotek OpenJade.

%package static
Summary:	OpenJade static libraries
Summary(pl):	Biblioteki statyczne OpenJade
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
OpenJade static libraries.

%description -l pl static
Biblioteki statyczne OpenJade.

%prep
%setup -q -n %{name}-20000320
%patch -p1

%build

#missing files required by Makefile.am
>ChangeLog
>INSTALL
gettextize --copy --force
autoheader
automake --add-missing
aclocal
autoconf
%ifarch alpha
CXXFLAGS="-O0"
export CXXFLAGS
%endif
LDFLAGS="-s"
export LDFLAGS 
%configure \
	--enable-default-catalog=/usr/share/sgml/CATALOG:/usr/local/share/sgml/CATALOG:/etc/sgml.catalog			  			\
	--enable-default-search-path=/usr/share/sgml:/usr/local/share/sgml
%{__make}  

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/sgml/catalogs,%{_libdir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

cp -a unicode $RPM_BUILD_ROOT%{_datadir}/sgml
ln -s "../OpenJade" $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}

grep -v SYSTEM $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}/catalog \
     > $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}/%{name}.cat
ln -s ../%{name}/%{name}.cat $RPM_BUILD_ROOT%{_datadir}/sgml/catalogs/

# simulate jade
ln -s openjade $RPM_BUILD_ROOT%{_bindir}/jade

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*
gzip -9nf COPYING README

%find_lang OpenJade

%post
/sbin/ldconfig
%{_sbindir}/fix-sgml-catalog

%preun
/sbin/ldconfig
%{_sbindir}/fix-sgml-catalog

%clean
rm -rf $RPM_BUILD_ROOT

%files -f OpenJade.lang
%defattr(644,root,root,755)
%doc jadedoc/ dsssl/ README.gz COPYING.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_datadir}/sgml/catalogs/*
%{_datadir}/sgml/openjade
%{_datadir}/sgml/unicode
%{_datadir}/OpenJade

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenJade
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la

%files static
%attr(644,root,root) %{_libdir}/lib*.a
