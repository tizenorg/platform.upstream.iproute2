Name:           iproute2
Version:        3.4.0
Release:        0
License:        GPL-2.0
Summary:        Linux network configuration utilities
Url:            http://www.linuxfoundation.org/collaborate/workgroups/networking/iproute2
Group:          Productivity/Networking/Routing
# Using GPL-2.0 instead of GPL-2.0+ because of tc_skbedit.h and tc/q_multiq.c

#DL-URL:	http://kernel.org/pub/linux/utils/net/iproute2/
#Git-Clone:	git://git.kernel.org/pub/scm/linux/kernel/git/shemminger/iproute2
Source:         %{name}-%{version}.tar.xz
Source1001: 	iproute2.manifest
BuildRequires:  bison
BuildRequires:  db4-devel
BuildRequires:  flex
BuildRequires:  libnl-devel
BuildRequires:  pkgconfig >= 0.21
BuildRequires:  xz
BuildRequires:  pkgconfig(libpng12)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(xtables)
Provides:       iproute = %{version}

%description
This package provides the tools ip, tc, and rtmon needed to use the new
and advanced routing options of the Linux kernel. The SUSE Linux
distribution has used this package for network setup since SuSE Linux
8.0.

%package -n libnetlink-devel
License:        GPL-2.0+
Summary:        A Higher Level Interface to the Netlink Service
Group:          Development/Libraries/C and C++
Provides:       libnetlink = %{version}

%description -n libnetlink-devel
libnetlink provides a higher level interface to rtnetlink(7).

%prep
%setup -q
cp %{SOURCE1001} .
find . -name *.orig -delete

%build
# build with -fPIC. For details see
# https://bugzilla.novell.com/show_bug.cgi?id=388021
./configure
xtlibdir="$(pkg-config xtables --variable=xtlibdir)";
make %{?_smp_mflags} LIBDIR=%{_libdir} CCOPTS="-D_GNU_SOURCE %{optflags} -Wstrict-prototypes -fPIC -DXT_LIB_DIR=\\\"$xtlibdir\\\""

%install
install -d %{buildroot}/{etc/,sbin/,usr/{sbin,share/man/man{3,8}}}
install -d %{buildroot}/{/usr/include,%{_libdir},/usr/share}
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} \
	MODDESTDIR="%{buildroot}/%{_libdir}/tc"
# We have m_xt
rm -f "%{buildroot}/%{_libdir}/tc/m_ipt.so"
install lib/libnetlink.a %{buildroot}/%{_libdir}
chmod -x %{buildroot}/%{_libdir}/libnetlink.a
install include/libnetlink.h %{buildroot}%{_includedir}
chmod -x %{buildroot}%{_includedir}/libnetlink.h
rm %{buildroot}%{_sbindir}/ifcfg
%remove_docs


%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%dir %{_sysconfdir}/iproute2
%config(noreplace) %{_sysconfdir}/iproute2/*
%{_libdir}/tc
%dir %{_datadir}/tc
%attr(644,root,root)%{_datadir}/tc/*


%files -n libnetlink-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/lib*

%docs_package
