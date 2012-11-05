%define with_docs 0

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
Source2:        %{name}-%{version}.tar.sign
# PATCH-FIX-UPSTREAM iproute2-libdir-1.diff status=unknown
Patch0:         iproute2-libdir-1.diff
# PATCH-??-OPENSUSE iproute2-HZ.diff status=noidea
Patch1:         iproute2-HZ.diff
BuildRequires:  bison
BuildRequires:  db4-devel
BuildRequires:  flex
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  pkgconfig >= 0.21
BuildRequires:  xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if %{with_docs}
BuildRequires:  ghostscript-x11
BuildRequires:  sgmltool
BuildRequires:  texlive-latex
%endif
%define with_xt 1
%if 0%{?with_xt}
BuildRequires:  libnl-devel
#BuildRequires:  pkgconfig(xtables) >= 1.4.11
BuildRequires:  libxtables-devel
%endif
Provides:       iproute = %{version}-%{release}

%description
This package provides the tools ip, tc, and rtmon needed to use the new
and advanced routing options of the Linux kernel. The SUSE Linux
distribution has used this package for network setup since SuSE Linux
8.0.

%package -n libnetlink-devel
License:        GPL-2.0+
Summary:        A Higher Level Interface to the Netlink Service
Group:          Development/Libraries/C and C++
Provides:       libnetlink = %{version}-%{release}

%description -n libnetlink-devel
libnetlink provides a higher level interface to rtnetlink(7).
%if %{with_docs}
%package doc
License:        GPL-2.0+
Summary:        Documentation to iproute2
Group:          Documentation
BuildArch:      noarch

%description doc
This package contains the PDF documentation from iproute2,
as well as examples and other outdated files.
%endif

%prep
%if 0%{?__xz:1}
%setup -q
%else
tar -xf "%{SOURCE0}" --use=xz;
%setup -DTq
%endif
%patch1 -P 0 -p1
find . -name *.orig -delete

%build
# build with -fPIC. For details see
# https://bugzilla.novell.com/show_bug.cgi?id=388021
./configure
xtlibdir="$(pkg-config xtables --variable=xtlibdir)";
make %{?_smp_mflags} LIBDIR=%{_libdir} CCOPTS="-D_GNU_SOURCE %{optflags} -Wstrict-prototypes -fPIC -DXT_LIB_DIR=\\\"$xtlibdir\\\""

%if %{with_docs}
cd doc
make pdf
%endif

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

%files
%defattr(-,root,root)
%doc README* COPYING
%{_sbindir}/*
%{_mandir}/man8/*
%dir %{_sysconfdir}/iproute2
%config(noreplace) %{_sysconfdir}/iproute2/*
%{_libdir}/tc
%dir %{_datadir}/tc
%attr(644,root,root)%{_datadir}/tc/*

%if %{with_docs}
%files doc
%defattr(-,root,root)
%doc doc/api-ip6-flowlabels.pdf doc/arpd.pdf doc/ip-cref.pdf
%doc doc/ip-tunnels.pdf doc/nstat.pdf doc/rtstat.pdf doc/ss.pdf
%doc examples/ ip/ifcfg ip/routef ip/routel
%endif

%files -n libnetlink-devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/libnetlink*
%{_libdir}/lib*
