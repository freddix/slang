Summary:	Shared library for C like extension language
Name:		slang
Version:	2.2.4
Release:	1
Epoch:		1
License:	GPL
Group:		Libraries
Source0:	ftp://space.mit.edu/pub/davis/slang/v2.2/%{name}-%{version}.tar.bz2
# Source0-md5:	7fcfd447e378f07dd0c0bae671fe6487
Patch0:		%{name}-nodevel.patch
Patch1:		%{name}-remove_unused_terminfo_paths.patch
URL:		http://www.s-lang.org/
BuildRequires:	autoconf
BuildRequires:	automake
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	%{_prefix}/include/slang

%description
Slang (pronounced ``sssslang'') is a powerful stack based interpreter
that supports a C-like syntax. It has been designed from the beginning
to be easily embedded into a program to make it extensible. Slang also
provides a way to quickly develop and debug the application embedding
it in a safe and efficient manner. Since slang resembles C, it is easy
to recode slang procedures in C if the need arises.

%package libs
Summary:	Shared libraries for slang C like language
Group:		Libraries

%description libs
Shared libraries for slang C like language

%package devel
Summary:	header files for slang C like language
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
This package contains header files required to develop slang-based
applications. It also includes documentation to help you write
slang-based apps.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	--disable-static

%{__make} -j1 elf \
	LN="ln -sf"
%{__make} all \
	LN="ln -sf"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT	\
	LN="ln -sf"

# help rpmdeps
chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so* \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/v2/modules/*.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc slsh/doc/html/*.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/slsh.rc
%attr(755,root,root) %{_bindir}/slsh
%{_datadir}/slsh
%{_mandir}/man1/*.1*

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/v2
%dir %{_libdir}/%{name}/v2/modules
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/%{name}/v2/modules/*.so

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt doc/text/*.txt
%attr(755,root,root) %{_libdir}/libslang*.so
%{_includedir}
%{_pkgconfigdir}/slang.pc

