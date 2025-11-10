Summary:	MuJS - lightweight, embeddable JavaScript interpreter in C
Summary(pl.UTF-8):	MuJS - lekki, osadzalny interpreter JavaScriptu napisany w C
Name:		mujs
Version:	1.3.8
Release:	1
License:	ISC
Group:		Development/Languages
Source0:	https://www.mujs.com/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	848a817a6202e5d1932331d0e77f6175
Patch0:		%{name}-shared.patch
URL:		https://www.mujs.com/
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MuJS is a lightweight JavaScript interpreter designed for embedding in
other software to extend them with scripting capabilities.

%description -l pl.UTF-8
MuJS to lekki interpreter JavaScriptu zaprojektowany do osadzania w
innych programach w celu rozszerzenia ich o obsługę skryptów.

%package devel
Summary:	Header files for MuJS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MuJS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for MuJS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MuJS.

%package static
Summary:	Static MuJS library
Summary(pl.UTF-8):	Statyczna biblioteka MuJS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MuJS library.

%description static -l pl.UTF-8
Statyczna biblioteka MuJS.

%prep
%setup -q
%patch -P0 -p1

# don't try to regenerate utfdata.h, use the one from release
touch -r utfdata.h SpecialCasing.txt UnicodeData.txt

%build
%{__make} -j1 release \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -std=c99 -Wall -Wextra -Wno-unused-parameter -Wunreachable-code" \
	LDFLAGS="%{rpmldflags}" \
	OPTIM= \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install-shared \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	libdir=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_bindir}/mujs
%attr(755,root,root) %{_bindir}/mujs-pp
%attr(755,root,root) %{_libdir}/libmujs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmujs.so.0

%files devel
%defattr(644,root,root,755)
%doc docs/*.{css,html,png,ps}
%attr(755,root,root) %{_libdir}/libmujs.so
%{_includedir}/mujs.h
%{_pkgconfigdir}/mujs.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmujs.a
