Summary:	OpenJade -- SGML and DSSSL parser
Name: 		openjade
Version: 	1.3
Release: 	1
Summary(pl):	OpenJade  -- parser SGML i DSSSL
Provides:	dssslparser
Provides:	sgmlparser
Prereq:		/usr/sbin/install-catalog
Requires: 	sgml-common
Conflicts:	sp
Vendor: 	James Clark
URL: 		http://jade-cvs.avionitek.com/
Source:		ftp://peano.mathematik.uni-freiburg.de/pub/jade/%{name}-%{version}.tar.gz
Source1: 	openjade.cat
#Patch:		jade-debian.patch
#Patch1:	jade-jumbo.patch
Copyright:	(C) 1998 James Clark (free) 
BuildRoot: 	/tmp/%{name}-%{version}-root
Group:  	Applications/Publishing/SGML
Group(pl):      Aplikacje/Publikowanie/SGML


%description
Jade (James' DSSSL Engine) is an implementation of the DSSSL style language. 
Also contain SGML parser called sp (replacement of sgmls).

%description -l pl
Jade (James' DSSSL Engine) jest implementacj± parsera DSSSL.
zawiera tak¿e parser  SGML  (bêd±cy nastêpc± pisanego w C sgmls) oraz narzêdzia
do ,,normalizacji'' SGMLa (sgmlnorm),  konwersji  tego¿  do  XMLa
(sgml2xml).


%prep

%setup -q  
#%patch -p1
#%patch1 -p1

%build

./configure					\
	--prefix=%{_prefix}			\
	--sharedstatedir=/usr/share/sgml 	\
	--enable-default-catalog=/usr/share/sgml/CATALOG:/usr/local/share/sgml/CATALOG:/etc/sgml.catalog			  			\
	--enable-default-search-path=/usr/share/sgml:/usr/local/share/sgml 

#	--enable-http 				\
#	--enable-shared 			\
#	--disable-mif				\
#	--enable-html 				\

#	--with-gnu-ld --prefix=/usr 		\
make  

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/share/sgml/{catalogs,openjade,html}
install -d $RPM_BUILD_ROOT/usr/lib

make -f Makefile install prefix="$RPM_BUILD_ROOT/usr"

cp -ar pubtext/* $RPM_BUILD_ROOT/usr/share/sgml/html
cp -ar unicode $RPM_BUILD_ROOT/usr/share/sgml

#mv $RPM_BUILD_ROOT/usr/bin/sx $RPM_BUILD_ROOT/usr/bin/sgml2xml
#perl -pi -e 's/sx/sgml2xml/g; s/SX/SGML2XML/g;'   doc/*.htm 

install %{SOURCE1} $RPM_BUILD_ROOT/usr/share/sgml/catalogs

install dsssl/catalog $RPM_BUILD_ROOT/usr/share/sgml/openjade
install dsssl/*.dtd   $RPM_BUILD_ROOT/usr/share/sgml/openjade
install dsssl/*.dsl   $RPM_BUILD_ROOT/usr/share/sgml/openjade

strip $RPM_BUILD_ROOT/usr/bin/*
strip $RPM_BUILD_ROOT/usr/lib/*.so.*

%post
install-catalog --install catalogs/openjade	--version %{version}-%{release}

%preun
install-catalog --remove  catalogs/openjade	--version %{version}-%{release}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)
%doc jadedoc/ dsssl/ README COPYING VERSION
%attr(755,root,root) /usr/bin/openjade
%attr(755,root,root) /usr/lib/libostyle.so*
%attr(755,root,root) /usr/lib/libogrove.so*
%attr(755,root,root) /usr/lib/libospgrove.so*
%config /usr/share/sgml/catalogs/openjade.cat
/usr/share/sgml/openjade
%defattr(644, root, root, 755)
%attr(755,root,root) /usr/bin/os*
%attr(755,root,root) /usr/bin/onsgmls
%attr(755,root,root) /usr/lib/libosp.so*
%doc doc/*
/usr/share/*.dsl
/usr/share/sgml/html
/usr/share/sgml/unicode
