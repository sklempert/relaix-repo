%define debug_package          %{nil}
%define dir_sav_install        /opt/sophos-av
%define name_daemon            savdid

Name: savdi
Version: 2.4.0
Release: 4
Group: System Environment/Daemons
URL: https://www.sophos.com/
License: Copyright 2000-2015 Sophos Limited. All rights reserved
Source0: %{name}-24-linux-64bit.tar
Source1: savdid.init
Source2: savdid.service
Summary: Sophos Anti-Virus Dynamic Interface
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: no
Requires: glibc savinstpkg
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
%else
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig, initscripts
Requires(postun): initscripts
%endif

%description
Sophos Anti-Virus Dynamic Interface

%prep
%setup -q -n savdi-install

%build
:

%install
%{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir} -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
%{__mkdir} -p ${RPM_BUILD_ROOT}/%{_libdir}
%{__mkdir} -p ${RPM_BUILD_ROOT}%{_mandir}/man1
%{__mkdir} -p ${RPM_BUILD_ROOT}%{dir_sav_install}/%{name}

%{__install} -m 0755 %{name_daemon} ${RPM_BUILD_ROOT}%{dir_sav_install}/%{name}/
%{__install} -m 0644 %{name_daemon}.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/
%{__install} -m 0644 %{name_daemon}lang_en.txt ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
%{__install} -D -m0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name_daemon}.service
%else
%{__mkdir} -p ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d
%{__install} -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name_daemon}
%endif

%{__ln_s} %{dir_sav_install}/%{_lib}/libssp.so.0 ${RPM_BUILD_ROOT}/%{_libdir}/libssp.so.0
%{__ln_s} %{dir_sav_install}/%{_lib}/libsavi.so.3 ${RPM_BUILD_ROOT}/%{_libdir}/libsavi.so.3

%clean
%{__rm} -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc readsavdi_eng.txt savdi_licence_en.txt EULA.rtf
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name_daemon}.conf
%{_sysconfdir}/%{name}/%{name_daemon}lang_en.txt
%dir %{dir_sav_install}/%{name}
%{dir_sav_install}/%{name}/%{name_daemon}
%{_libdir}/libssp.so.0
%{_libdir}/libsavi.so.3
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
%{_unitdir}/%{name_daemon}.service
%else
%{_sysconfdir}/init.d/%{name_daemon}
%endif

%post
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
%systemd_post %{name_daemon}.service
%else
/sbin/chkconfig --add %{name_daemon} || :
%endif

%preun
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
%systemd_preun %{name_daemon}.service
%else
if [ $1 -eq 0 ]; then
    %{_initrddir}/%{name_daemon} stop &>/dev/null || :
    /sbin/chkconfig --del %{name_daemon} || :
fi
%endif

%postun
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
%systemd_postun_with_restart %{name_daemon}.service
%else
%{_initrddir}/%{name_daemon} condrestart &>/dev/null || :
%endif

%changelog
* Sun Nov 01 2020 Simon Klempert <git@klempert.net> 2.4.0-4
- Fix systemd unitfile (git@klempert.net)
- Create sytemd service for savdi (git@klempert.net)

* Sat Oct 31 2020 Matthias Hensler <matthias@wspse.de> 2.4.0-3
- fix build for EL8

* Sat Oct 01 2016 Simon Klempert <git@klempert.net> 2.4.0-2
- Set correct savdi version (git@klempert.net)

* Sat Oct 01 2016 Simon Klempert <git@klempert.net> 2.3.0-1
- new package built with tito

* Sat Jun 11 2016 nazx <jjj@nazx.jp> - 2.3.0
- Initial release

