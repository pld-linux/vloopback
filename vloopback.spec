#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rc	rc1
%define		_rel	0.%{_rc}.1
#
Summary:	Video4Linux Loopback Device
#Summary(pl.UTF-8):	vloopback
Name:		vloopback
Version:	1.1
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.lavrsen.dk/twiki/pub/Motion/VideoFourLinuxLoopbackDevice/%{name}-%{version}-%{_rc}.tar.gz
# Source0-md5:	d5bc4f1efff9b69c93cd6de061ca2eaa
URL:		http://www.lavrsen.dk/twiki/bin/view/Motion/VideoFourLinuxLoopbackDevice
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The video4linux device is a driver that implements a video pipe using two
video4linux devices.

#%description -l pl.UTF-8

%package -n kernel%{_alt_kernel}-misc-vloopback
Summary:	vloopback kernel module
Summary(pl.UTF-8):	vloopback
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-vloopback

#%description -n kernel%{_alt_kernel}-misc-vloopback -l pl.UTF-8

%prep
%setup -q -n %{name}-%{version}-%{_rc}
cat > Makefile <<'EOF'
obj-m := vloopback.o
EOF

%build
%build_kernel_modules -m %{name}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m %{name} -d kernel/drivers/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-vloopback
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-vloopback
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-misc-vloopback
%defattr(644,root,root,755)
%doc README
/lib/modules/%{_kernel_ver}/kernel/drivers/misc/%{name}.ko*
