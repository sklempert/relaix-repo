Name: rancid
Epoch: 1
Version: 3.5.1
Release: 5%{?dist}
Summary: Really Awesome New Cisco confIg Differ

Group: Applications/Internet
License: BSD with advertising
URL: http://www.shrubbery.net/rancid/
Source0: ftp://ftp.shrubbery.net/pub/{name}/%{name}-%{version}.tar.gz
Source1: %{name}.cron
Source2: %{name}.logrotate
Patch0: %{name}-conf.patch
Patch1: %{name}-Makefile.patch
# RelAix Patches
Patch22: %{name}-%{version}-Socket-version-check.patch
Patch23: %{name}-%{version}-foundry-flash.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: telnet
BuildRequires: automake, autoconf
BuildRequires: rsh
BuildRequires: openssh-clients
BuildRequires: expect >= 5.40
BuildRequires: cvs
BuildRequires: subversion
BuildRequires: perl
BuildRequires: iputils
BuildRequires: sendmail

Requires(pre): shadow-utils
Requires: findutils
Requires: expect >= 5.40
Requires: perl
Requires: iputils
Requires: logrotate

%description
RANCID monitors a router's (or more generally a device's) configuration, 
including software and hardware (cards, serial numbers, etc) and uses CVS 
(Concurrent Version System) or Subversion to maintain history of changes.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch22 -p0
%patch23 -p1

%build
%configure \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --bindir=%{_libexecdir}/%{name} \
    --libdir=%{perl_vendorlib} \
    --enable-conf-install
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
install -d -m 0755 %{buildroot}/%{_localstatedir}/%{name}
install -d -m 0755 %{buildroot}/%{_localstatedir}/log/%{name}
install -d -m 0755 %{buildroot}/%{_localstatedir}/log/%{name}/old
install -d -m 0755 %{buildroot}/%{_sysconfdir}/cron.d
install -d -m 0755 %{buildroot}/%{_bindir}/

#symlink some bins from %%{_libexecdir}/%%{name} to %%{_bindir}
for base in \
 %{name} %{name}-cvs %{name}-fe %{name}-run
 do
 ln -sf %{_libexecdir}/%{name}/${base} \
  %{buildroot}/%{_bindir}/${base}
done

install -D -p -m 0755 %{SOURCE1} %{buildroot}/%{_sysconfdir}/cron.d/%{name}

#Patch cron file to point to correct installation directory
sed -i 's|RANCIDBINDIR|%{_libexecdir}/%{name}|g' %{buildroot}/%{_sysconfdir}/cron.d/%{name}

install -D -p -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d %{_localstatedir}/%{name}/ -s /bin/bash \
-k /etc/skel -m -c "RANCID" %{name}
exit 0


%files
%defattr(-,root,root,-)
%doc CHANGES cloginrc.sample COPYING FAQ README README.lg Todo

#%%{_sysconfdir}-files
%attr(750,%{name},%{name}) %dir %{_sysconfdir}/%{name}
%attr(640,%{name},%{name}) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/cron.d/%{name}
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

#%%{_libexecdir}/%%{name}-files
%dir %{_libexecdir}/%{name}/
%{_libexecdir}/%{name}/*

#%%{_bindir}-files
%{_bindir}/*

#%%{_mandir}-files
%{_mandir}/*/*

#%%{_datadir}/%%{name}-files
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*

#%%{_localstatedir}-directories
%attr(750,%{name},%{name}) %dir %{_localstatedir}/log/%{name}
%attr(750,%{name},%{name}) %dir %{_localstatedir}/log/%{name}/old
%attr(750,%{name},%{name}) %dir %{_localstatedir}/%{name}/

%{perl_vendorlib}/*


%changelog
* Tue Dec 06 2016 Simon Klempert <git@klempert.net> 3.5.1-5
- Add epoch 1 to rancid package so it is newer than epel (git@klempert.net)

* Tue Dec 06 2016 Simon Klempert <git@klempert.net> 3.5.1-4
- Fix foundry flash section parsing (git@klempert.net)

* Tue Dec 06 2016 Simon Klempert <git@klempert.net> 3.5.1-3
- Fix patches (git@klempert.net)

* Tue Dec 06 2016 Simon Klempert <git@klempert.net> 3.5.1-2
- new package built with tito

* Tue Dec 06 2016 Simon Klempert <sklempert@relaix.net> -  3.5.1-1
- New Upstream Version
- Remove Socket.pm version check (this needs to be locally installed with CPAN)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 30 2015 David Brown <david.brown@pnnl.gov> - 3.2-2
- Add upstream patches

* Wed Nov 19 2014 David Brown <david.brown@pnnl.gov> - 3.2-1
- New Upstream Version
- Fix Bugzilla #1165738

* Wed Nov 19 2014 Sven Lankes <sven@lank.es> - 3.1-3
- Filter uptime of Foundry Switch Fabric Modules (fixes rhbz #1165738)

* Mon Oct 6 2014 David Brown <david.brown@pnnl.gov> - 3.1-2
- New updated version

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.3.8-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Sven Lankes <sven@lank.es> - 2.3.8-1
- New upstream release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Peter Robinson <pbrobinson@gmail.com> 2.3.6-1
- New upstream 2.3.6 release

* Tue Sep 28 2010 Peter Robinson <pbrobinson@gmail.com> 2.3.4-1
- New upstream 2.3.4 release

* Wed Jul 22 2009 Gary T. Giesen <giesen@snickers.org> 2.3.2-3
- Changed GECOS name for rancid user

* Wed Jul 22 2009 Gary T. Giesen <giesen@snickers.org> 2.3.2-2
- Added logrotate (and updated crontab to let logrotate handle log file 
  cleanup
- Removed Requires: for rsh, telnet, and openssh-clients
- Removed Requires: for cvs
- Cleaned up file permissions
- Added shell for rancid user for CVS tree creation and troubleshooting
- Patch cron file for installation path
- Removed installation of CVS root to permit SVN use
- Moved from libdir to libexecdir

* Thu Jul 16 2009 Gary T. Giesen <giesen@snickers.org> 2.3.2-1
- Updated to 2.3.2 stable
- Removed versioned expect requirement so all supported Fedora/EPEL releases
  now meet the minimum
- Spec file cleanup/style changes

* Wed Oct 08 2008 Aage Olai Johnsen <aage@thaumaturge.org> 2.3.2-0.6a8
- Some fixes (#451189)

* Tue Sep 30 2008 Aage Olai Johnsen <aage@thaumaturge.org> 2.3.2-0.5a8
- Some fixes (#451189)

* Tue Sep 30 2008 Aage Olai Johnsen <aage@thaumaturge.org> 2.3.2-0.4a8
- More fixes (#451189)
- Patched Makefiles - Supplied by Mamoru Tasaka (mtasaka@ioa.s.u-tokyo.ac.jp) 

* Tue Sep 23 2008 Aage Olai Johnsen <aage@thaumaturge.org> 2.3.2-0.3a8
- More fixes (#451189)

* Wed Jul 09 2008 Aage Olai Johnsen <aage@thaumaturge.org> 2.3.2a8-0.2a8
- Plenty of fixes (#451189)
- Patched rancid.conf-file
- Added cronjob

* Sat May 31 2008 Aage Olai Johnsen <aage@thaumaturge.org> 2.3.2a8-0.1
- Initial RPM release
