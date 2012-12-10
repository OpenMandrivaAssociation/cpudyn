%define debug_package   %nil
%define name cpudyn
%define version 1.0.1
%define release %mkrel 6

Summary: A tools to control CPU frequency
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://mnm.uib.es/gallir/cpudyn/download/%{name}-%{version}.tar.bz2
Source1: %{name}.initscript
License: GPL
Group: System/Kernel and hardware
Url: http://mnm.uib.es/~gallir/cpudyn/
ExclusiveArch: %ix86 ppc x86_64
Requires(pre): rpm-helper
Requires(post): rpm-helper
Patch0:		cpudyn-printf-format.patch

%description
This program control the speed in Intel SpeedStep, Pentium 4 Mobile
and PowerPC machines with the cpufreq compiled in the kernel.

It allows to reduce cpu speed in order to save battery and reduce 
temperature of the processor. It can also put the drive on standby mode.

Tested with 2.4, Pentium 3 Speedstep Laptop (Dell Latitude),
Pentium 4 Mobile Laptop (Dell Inspiron), AMD Power Now, Apple iBook,
IBM Thinkpad. cpudyn is just a user space program, so it will work on
every processor supported by the kernel's cpufreq driver.

%prep
%setup -q -n %name
%patch0 -p0

%build
%make CFLAGS="$RPM_OPT_FLAGS"

%install
mkdir -p %buildroot{%_sbindir,%_mandir/man8,%_sysconfdir/sysconfig,%_initrddir}
cp cpudynd %buildroot%_sbindir/cpudynd
#bzip2 cpudynd.8
cp cpudynd.8 %buildroot%_mandir/man8/

install -m 755 %SOURCE1 %buildroot%_initrddir/%name

cat > %buildroot/%_sysconfdir/sysconfig/%name <<EOF
# see man 8 cpudynd  for details
OPTS="-i 1 -p 0.5 0.90"
EOF

%files
%_sbindir/cpudynd
%_mandir/man8/cpudynd*
%config(noreplace) %_sysconfdir/sysconfig/%{name}
%config(noreplace) %_initrddir/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}
