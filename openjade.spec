%define		snap	20020409
Summary:	OpenJade -- DSSSL parser
Summary(pl):	OpenJade -- parser DSSSL
Name:		openjade
Version:	1.4
Release:	11.%{snap}
License:	Free (Copyright (C) 1999 The OpenJade group)
Group:		Applications/Publishing/SGML
Source0:	%{name}-%{snap}.tar.gz
Patch0:		%{name}-table.patch
Patch1:		%{name}-ac25x.patch
Patch2:		%{name}-types.patch
URL:		http://openjade.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	opensp-devel >= 1.5pre5
BuildRequires:	perl
Provides:	jade
Provides:	dssslparser
Requires:	sgmlparser
Requires:	opensp >= 1.5pre5
Prereq:		sgml-common
Prereq:		/sbin/ldconfig
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
%setup -q -n %{name}-%{snap}
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
#remove CVS dirs
find . -type d -name CVS | xargs rm -rf
#missing files required by Makefile.am
touch ChangeLog
%{__gettextize}
%{__libtoolize}
aclocal
echo "#undef SIZEOF_WCHAR_T" >> acconfig.h
autoheader
%{__automake}
#aclocal
%{__autoconf}
%ifarch alpha
CXXFLAGS="-O0 %{?debug:-g}"
%endif
%configure \
	--enable-default-catalog=/etc/sgml/catalog \
	--enable-default-search-path=/usr/share/sgml

# it has /usr/share/Openjade hardcoded somewhere so it does not work
	# --datadir=%{_datadir}/sgml

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml

%{__make} install DESTDIR=$RPM_BUILD_ROOT

cp -a unicode $RPM_BUILD_ROOT%{_datadir}/sgml
ln -sf "../OpenJade" $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}-%{version}

##ln -s "../OpenJade" $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}
#install dsssl/catalog \
#	dsssl/builtins.dsl dsssl/extensions.dsl \
#	dsssl/dsssl.dtd dsssl/fot.dtd dsssl/spec.dtd dsssl/style-sheet.dtd \
#	$RPM_BUILD_ROOT%{_datadir}/sgml/%{name}-%{version}/
#grep -v SYSTEM $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}/catalog > \
#	$RPM_BUILD_ROOT%{_datadir}/sgml/%{name}/%{name}.cat


# simulate jade
ln -sf openjade $RPM_BUILD_ROOT%{_bindir}/jade

gzip -9nf COPYING README

%find_lang OpenJade

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/usr/bin/install-catalog --add /etc/sgml/dsssl-%{version}-%{release}.cat \
	%{_datadir}/sgml/%{name}-%{version}/catalog
/usr/bin/install-catalog --add /etc/sgml/jade-unicode-%{version}-%{release}.cat \
	%{_datadir}/sgml/unicode/catalog

%postun
/sbin/ldconfig
/usr/bin/install-catalog --remove /etc/sgml/dsssl-%{version}.cat \
	%{_datadir}/sgml/%{name}-%{version}/catalog
/usr/bin/install-catalog --remove /etc/sgml/jade-unicode-%{version}-%{release}.cat \
	%{_datadir}/sgml/unicode/catalog

%files -f OpenJade.lang
%defattr(644,root,root,755)
%doc jadedoc/ dsssl/ README.gz COPYING.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_datadir}/sgml/*
%{_datadir}/OpenJade

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenJade
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
