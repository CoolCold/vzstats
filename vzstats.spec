Name:		vzstats
Version:	0.5
Release:	1%{?dist}
BuildArch:	noarch
Summary:	OpenVZ stats collection daemon

Group:		Applications/System
License:	GPLv2+
URL:		http://stats.openvz.org
Source:		%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	curl

%description
This is an OpenVZ component to gather OpenVZ usage and hardware statistics,
in order to improve the project.

Statistics gathered and reported include the following:
1 Hardware info.
- CPU, disk, memory/swap.
2 Software info.
- host distribution, versions of OpenVZ components, kernel version
3 Containers info.
- number of containers existing/running/using ploop/using vswap
- OS templates of containers
For more details, check the scripts in /usr/libexec/vzstats/ directory.

All submissions are anonymous and are not including IP or MAC addresses,
hostnames etc. Global data are available at http://stats.openvz.org

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install-all DESTDIR=%{buildroot}
# Needed for %ghost in %files section below
touch %{buildroot}%{_sysconfdir}/vz/.vzstats-uuid

%files
%{_sbindir}/vzstats
%{_mandir}/man8/vzstats.8.*
%config %{_sysconfdir}/vz/vzstats.conf
%{_sysconfdir}/vz/*.crt
%ghost %config(missingok) %{_sysconfdir}/vz/.vzstats-uuid
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/*
%{_sysconfdir}/cron.monthly/*
%{_sysconfdir}/bash_completion.d/*
%doc README COPYING

%triggerin -- vzctl,vzctl-core,vzquota,ploop,ploop-lib,kernel,vzkernel,ovzkernel
%{_sbindir}/vzstats &

%changelog
* Thu Jul 11 2013 Kir Kolyshkin <kir@openvz.org> - 0.5-1
- enabled SSL when sending reports to stats.openvz.org
- removed lspci script
- bin/top-ps: add --quiet to vzctl exec
- increased curl timeout to 30s

* Thu Jun 13 2013 Kir Kolyshkin <kir@openvz.org> - 0.4-1
- added top-ps script
- fix vzversion-arch for openvz kernel names (#2596)
- make sure sbin paths are in PATH before running scripts
- exit with error if run inside CT
- increased curl timeout from 3s to 10s
- vzstats.spec: run trigger in background
- Makefile: support for configurable paths (see Makefile.paths)
- Makefile: substitute version from spec to script
- Makefile: add install-all target, use it from spec

* Fri May 10 2013 Kir Kolyshkin <kir@openvz.org> - 0.3.2-1
- fixed %triggerin
- fixed "http_proxy: unbound variable" error

* Fri May 10 2013 Kir Kolyshkin <kir@openvz.org> - 0.3.1-1
- add options --help, --view, --enable, --disable and --status
- add vzstats(8) man page
- add lsbrelease script
- improve vzlist script to work with older vzctl releases
- add proxy discovery code
- add bash_completion script

* Fri Apr 26 2013 Kir Kolyshkin <kir@openvz.org> - 0.2.1-1
- fixed compatibility with older (as of RHEL5/4) userspace
- stricter checks for scripts permission and ownership

* Wed Apr 24 2013 Kir Kolyshkin <kir@openvz.org> - 0.2-1
- first public release
- added meminfo and ostemplates scripts

* Thu Apr  4 2013 Kir Kolyshkin <kir@openvz.org> - 0.1-1
- initial packaging
