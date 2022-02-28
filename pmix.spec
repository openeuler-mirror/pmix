Name:           pmix
Version:        3.1.6
Release:        1
Summary:        Process Management Interface Exascale (PMIx)
License:        BSD
URL:            https://pmix.org
Source0:        https://github.com/openpmix/openpmix/releases/download/v%{version}/pmix-%{version}.tar.bz2
Patch0000:      correct-the-help-information.patch

%ifarch riscv64
Patch0001:      extend_test_timeout.patch
%endif

BuildRequires:  autoconf automake flex hwloc-devel libevent-devel libtool munge-devel perl-interpreter

%description
PMI has been used for quite some time as a means of exchanging wireup information needed
for interprocess communication.

%package        devel
Summary:        Development files for pmix
Requires:       pmix = %{version}-%{release}
%description    devel
Libraries and header files for developing with pmix.

%package        pmi
Summary:        Pmix implementation of libpmi and libpmi2
Requires:       pmix = %{version}-%{release}
Conflicts:      slurm-pmi
%description    pmi
The pmix implementation of the libpmi and libpmi2 backward-compatibility libraries.

%package        pmi-devel
Summary:        Development files for pmix-pmi
Requires:       pmix-pmi = %{version}-%{release}
Conflicts:      slurm-pmi-devel
%description    pmi-devel
The development files for the libpmi and libpmi2 backward-compatibility libraries.

%package        tools
Summary:        Pmix tools
Requires:       pmix = %{version}-%{release}
%description    tools
Contains for use with PMIx-based RMs and language-based starters (e.g., mpirun).

%prep
%autosetup -n pmix-%{version} -p1
find src -name \*.l -print -exec touch --no-create {} \;

%build
%{_builddir}/pmix-%{version}/autogen.pl
%configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}/pmix --disable-static \
  --disable-silent-rules --enable-shared --enable-pmi-backward-compatibility --with-munge

%make_build

%check
%make_build check

%install
%make_install
%delete_la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%doc LICENSE README
%dir %{_datadir}/pmix
%dir %{_libdir}/pmix
%dir %{_sysconfdir}/pmix
%config(noreplace) %{_sysconfdir}/pmix/*.conf
%{_datadir}/pmix/*.txt
%{_libdir}/{libmca_common_dstore.so.1*,libpmix.so.2*,pmix/*.so}

%files devel
%{_datadir}/pmix/*.supp
%{_includedir}/pmix*.h
%{_libdir}/{libmca_common_dstore.so,libpmix.so}

%files pmi
%{_libdir}/{libpmi.so.1*,libpmi2.so.1*}

%files pmi-devel
%{_includedir}/{pmi,pmi2}.h
%{_libdir}/{libpmi.so,libpmi2.so}

%files tools
%{_bindir}/*

%changelog
* Tue Mar 1 2022 lvxiaoqian <xiaoqian@nj.iscas.ac.cn> - 3.1.6-1
- update to 3.1.6

* Mon Dec 13 2021 lvxiaoqian <xiaoqian@nj.iscas.ac.cn> - 3.1.4-4
- extend test timeout for riscv

* Sat Sep 18 2021 caodongxia <caodongxia@huawei.com> - 3.1.4-3
- Correct the help information

* Wed Mar 4 2020 Ling Yang <lingyang2@huawei.com> - 3.1.4-2
- Package Init
