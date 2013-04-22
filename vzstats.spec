Name:		vzstats
Version:	0.1
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

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install install-cronjob DESTDIR=%{buildroot}
# Needed for %ghost in %files section below
touch %{buildroot}%{_sysconfdir}/vz/.vzstats-uuid

%files
%{_sbindir}/vzstats
%config %{_sysconfdir}/vz/vzstats.conf
%ghost %config(missingok) %{_sysconfdir}/vz/.vzstats-uuid
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/*
%{_sysconfdir}/cron.monthly/*
%doc README COPYING

%triggerin -p %{_sbindir}/vzstats -- vzctl,vzctl-core,vzquota,ploop,ploop-lib,kernel,vzkernel,ovzkernel

%changelog
* Thu Apr  4 2013 Kir Kolyshkin <kir@openvz.org> - 0.1-1
- initial packaging
