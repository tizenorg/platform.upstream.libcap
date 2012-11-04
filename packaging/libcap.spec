Name:           libcap
Version:        2.22
Release:        1
License:        BSD-3-Clause ; GPL-2.0
Summary:        Library for Capabilities (linux-privs) Support
Url:            https://sites.google.com/site/fullycapable/
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
BuildRequires:  fdupes
BuildRequires:  libattr-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%define debug_package_requires libcap2 = %{version}-%{release}

%description
Capabilities are a measure to limit the omnipotence of the superuser.
Currently a program started by root or setuid root has the power to do
anything. Capabilities (Linux-Privs) provide a more fine-grained access
control. Without kernel patches, you can use this library to drop
capabilities within setuid binaries. If you use patches, this can be
done automatically by the kernel.

%package devel
License:        BSD-3-Clause ; GPL-2.0
Summary:        Development files for libcap
Group:          Development/Libraries/C and C++
Requires:       glibc-devel
Requires:       libcap = %{version}

%description devel
Development files (Headers, libraries for static linking, etc) for
libcap.

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install libcap-devel if you want to develop or compile applications
using libcap.

%package progs
License:        BSD-3-Clause ; GPL-2.0
Summary:        Libcap utility programs
Group:          System/Filesystems

%description progs
This package contains utility programs handling capabilities via
libcap.

%prep
%setup -q

%build
# lib=%{_lib} make %{?_smp_mflags} COPTFLAG="%{optflags}"
lib=%{_lib} make %{?_smp_mflags} DEBUG="-g %{optflags}"

%install
make install DESTDIR=%{buildroot} LIBDIR=%{buildroot}/%{_lib} MANDIR=%{buildroot}%{_mandir} RAISE_SETFCAP=no
# remove unneeded files
rm -f %{buildroot}/%{_lib}/*.*a
# move *.so file to libdir and relink
rm -f %{buildroot}/%{_lib}/*.so
mkdir -p %{buildroot}%{_libdir}
ln -s /%{_lib}/libcap.so.2 %{buildroot}%{_libdir}/libcap.so
%fdupes -s %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(755,root,root) /%{_lib}/libcap.so.*

%files progs
%defattr(-,root,root)
%{_mandir}/man1/*
%{_mandir}/man8/*
/sbin/*

%files devel
%defattr(-,root,root)
%doc License README CHANGELOG
%{_includedir}/sys/capability.h
%{_libdir}/*.so
%{_mandir}/man3/*

%changelog