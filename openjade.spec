Summary:	OpenJade -- DSSSL parser
Name: 		openjade
##Epoch:		1 #prepared for 1.3.1
Version: 	20000320
Release: 	1
Summary(pl):	OpenJade -- parser DSSSL
Provides:	dssslparser
Prereq:		%{_sbindir}/fix-sgml-catalog
Requires: 	sgml-common
Requires:	sgmlparser
Requires: 	opensp >= 1.4-1
URL:            http://openjade.sourceforge.net/
#Source:         http://download.sourceforge.net/openjade/%{name}-%{version}.tar.gz
Source:         %{name}-%{version}.tar.gz
Source1: 	%{name}.cat
Patch:		%{name}-DESTDIR.patch
#Patch:		jade-debian.patch
#Patch1:	jade-jumbo.patch
Copyright:      Copyright (c) 1999 The OpenJade group (free)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	opensp-devel >= 1.4-1
BuildRequires:	perl
Group:  	Applications/Publishing/SGML
Group(pl):      Aplikacje/Publikowanie/SGML

%description
Jade (James' DSSSL Engine) is an implementation of the DSSSL style language. 

%description -l pl
Jade (James' DSSSL Engine) jest implementacj± parsera DSSSL.

%package devel
Summary:	%{name} header files.
Summary(pl):	Pliki nag³ówkowe %{name}
Requires:	%{name} = %{version}
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki

%description devel

%description -l pl devel

%prep
%setup -q  
%patch -p1
#%patch1 -p1

%build

#missing files required by Makefile.am
>ChangeLog
>INSTALL
autoheader
automake --add-missing
aclocal
autoconf
LDFLAGS="-s"; export LDFLAGS
%configure \
	--enable-default-catalog=/usr/share/sgml/CATALOG:/usr/local/share/sgml/CATALOG:/etc/sgml.catalog			  			\
	--enable-default-search-path=/usr/share/sgml:/usr/local/share/sgml 

#	--prefix=%{_prefix}			\
#	--sharedstatedir=/usr/share/sgml 	\
#	--enable-http 				\
#	--enable-shared 			\
#	--disable-mif				\
#	--enable-html 				\

#	--with-gnu-ld --prefix=/usr 		\

make  

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/catalogs
install -d $RPM_BUILD_ROOT%{_libdir}

make install DESTDIR=$RPM_BUILD_ROOT

#cp -ar pubtext/* $RPM_BUILD_ROOT%{_datadir}/sgml/html
cp -a unicode $RPM_BUILD_ROOT%{_datadir}/sgml

#mv $RPM_BUILD_ROOT/usr/bin/sx $RPM_BUILD_ROOT/usr/bin/sgml2xml
#perl -pi -e 's/sx/sgml2xml/g; s/SX/SGML2XML/g;'   doc/*.htm 

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/sgml/catalogs

#install dsssl/catalog $RPM_BUILD_ROOT%{_datadir}/sgml/openjade
#install dsssl/*.dtd   $RPM_BUILD_ROOT%{_datadir}/sgml/openjade
#install dsssl/*.dsl   $RPM_BUILD_ROOT%{_datadir}/sgml/openjade

ln -s "../OpenJade" $RPM_BUILD_ROOT%{_datadir}/sgml/openjade

gzip -9nf COPYING README

%post
/sbin/ldconfig
%{_sbindir}/fix-sgml-catalog
#install-catalog --install catalogs/openjade	--version %{version}-%{release}

%preun
/sbin/ldconfig
%{_sbindir}/fix-sgml-catalog
#install-catalog --remove  catalogs/openjade	--version %{version}-%{release}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc jadedoc/ dsssl/ README.gz COPYING.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
%{_datadir}/sgml/catalogs/*
%{_datadir}/sgml/openjade
%{_datadir}/sgml/unicode
%{_datadir}/OpenJade
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/*
%lang(sv) %{_datadir}/locale/sv/LC_MESSAGES/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenJade
%{_libdir}/*.so
