Summary:	OpenJade -- DSSSL parser
Summary(pl):	OpenJade -- parser DSSSL
Name:		openjade
Version:	1.4
Release:	7.20000320
License:	free (Copyright (c) 1999 The OpenJade group)
Group:		Applications/Publishing/SGML
Group(de):	Applikationen/Publizieren/SGML
Group(pl):	Aplikacje/Publikowanie/SGML
Source0:	%{name}-20000320.tar.gz
Patch0:		%{name}-DESTDIR.patch
URL:		http://openjade.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	opensp-devel
BuildRequires:	perl
Provides:	jade
Provides:	dssslparser
Requires:	sgml-common
Requires:	sgmlparser
Requires:	opensp >= 1.4-9
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
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
Prereq:		/sbin/ldconfig
Requires:	%{name} = %{version}

%description devel
Openjade header files.

%description -l pl devel
Pliki nag³ówkowe do bibliotek OpenJade.

%package static
Summary:	OpenJade static libraries
Summary(pl):	Biblioteki statyczne OpenJade
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
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
libtoolize --copy --force
aclocal
echo "#undef SIZEOF_WCHAR_T" >> acconfig.h
autoheader
automake -a -c
#aclocal
autoconf
%ifarch alpha
CXXFLAGS="-O0"
export CXXFLAGS
%endif
%configure \
	--enable-default-catalog=/etc/sgml/catalog \
	--enable-default-search-path=/usr/share/sgml \


# it has /usr/share/Openjade hardcoded somewhere so it des not work
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
/usr/bin/install-catalog --add /etc/sgml/dsssl-%{version}.cat \
	%{_datadir}/sgml/%{name}-%{version}/catalog

%postun
/sbin/ldconfig
# Do not remove if upgrade
if [ "$1" = "0" ]; then
	/usr/bin/install-catalog --remove /etc/sgml/dsssl-%{version}.cat \
		%{_datadir}/sgml/%{name}-%{version}/catalog
fi

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
