%global build_options -DGENERATE_SRS_SECRET=OFF -DUSE_SELINUX=ON -DINIT_FLAVOR=systemd

%undefine __cmake_in_source_build

Name:           postsrsd
Version:        1.6
Release:        1%{?dist}
Summary:        Sender Rewriting Scheme (SRS) provider

License:        GPLv2+
URL:            https://github.com/roehling/postsrsd
Source0:        https://github.com/roehling/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:     cmake
BuildRequires:     gcc
BuildRequires:     help2man
BuildRequires:     selinux-policy-devel
%{?systemd_requires}
BuildRequires:     systemd
Requires(post):    policycoreutils
Requires(preun):   policycoreutils
Requires(postun):  policycoreutils


%description
PostSRSd provides the Sender Rewriting Scheme (SRS) via TCP-based lookup tables for Postfix.
SRS is needed if your mail server acts as forwarder.


%prep
%autosetup -n %{name}-%{version}
%if (0%{?rhel} && 0%{?rhel} < 8)
mkdir build
cd build && %cmake .. %build_options
%else
%cmake %build_options
%endif


%build
%if (0%{?rhel} && 0%{?rhel} < 8)
%make_build -C build
%else
%cmake_build
%endif


%install
%if (0%{?rhel} && 0%{?rhel} < 8)
%make_install -C build
%else
%cmake_install
%endif

# %%ghost file requires it is present in the build root
touch %{buildroot}/%{_sysconfdir}/postsrsd.secret

# proper location for systemd config
mkdir -p %{buildroot}/%{_unitdir}
mv %{buildroot}/%{_sysconfdir}/systemd/system/postsrsd.service %{buildroot}/%{_unitdir}/postsrsd.service
rm -rf %{buildroot}/%{_sysconfdir}/systemd

# chroot directory
# (also move default config which is in the way)
sed -i 's/^CHROOT=.*/CHROOT=\/run\/postsrsd/' %{buildroot}/%{_sysconfdir}/default/%{name}
sed -ri -e 's/postsrsd\/default/postsrsd.default/' \
        -e "s/(\[Install\])/RuntimeDirectory=postsrsd\nRuntimeDirectoryMode=0750\n\n\1/" %{buildroot}/%{_unitdir}/postsrsd.service


%files
%license LICENSE
%ghost %{_sysconfdir}/postsrsd.secret
%{_sysconfdir}/default/%{name}
%{_unitdir}/postsrsd.service
%{_sbindir}/postsrsd
%{_docdir}/%{name}
%{_mandir}/man8/postsrsd.8.gz
%{_datadir}/selinux/packages/%{name}/postsrsd.pp


%post
if [ "$1" -le "1" ] ; then  # first install
semodule -i %{_datadir}/selinux/packages/%{name}/postsrsd.pp || true
fixfiles -R %{name} restore || true
fi
[ -f %{_sysconfdir}/postsrsd.secret ] || dd if=/dev/urandom bs=18 count=1 2>/dev/null | base64 >%{_sysconfdir}/postsrsd.secret
# the admin may modify / restore from a backup, so better restore SELinux permissions unconditionally
restorecon %{_sysconfdir}/postsrsd.secret
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service
if [ "$1" -lt "1" ] ; then  # final removal
semodule -r postsrsd 2>/dev/null || true
fi


%postun
if [ "$1" -ge "1" ] ; then  # upgrade
semodule -i %{_datadir}/selinux/packages/%{name}/postsrsd.pp || true
fixfiles -R %{name} restore || true
fi
%systemd_postun_with_restart %{name}.service
#if [ "$1" -eq "0" ] ; then  # final removal
#fi


%changelog
* Tue Oct 06 2020 Marc Dequènes (Duck) <duck@redhat.com> - 1.6-1
- NUR
- define INIT_FLAVOR as detection does not work in build environment
- ensure build in not done in-source
- add gcc to BuildRequires (removing it was a mistake)
- add compat for EL7 around cmake_* macros

* Thu Aug 13 2020 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-10.20170118gita77bf99
- migrate to new cmake macros for out-of-source builds

* Thu Oct 05 2017 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-9.20170118gita77bf99
- use the %%ghost feature to ensure the secret file is owned by the package
- it is then not necessary to handle its removal in %%postun

* Thu Sep 28 2017 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-8.20170118gita77bf99
- Thanks Matthias Runge Mauchin for the review
- break description line too long
- build dependency on gcc is not needed

* Wed Sep 27 2017 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-7.20170118gita77bf99
- make the changelog more readable
- stop recreating buildroot, it is made clean already

* Wed Aug 23 2017 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-6.20170118gita77bf99
- remove unnecessary Requires on make
- use _sysconfdir macro
- use name macro when it makes sense
- remove unnecessary %%doc as the buildsys already populates docdir

* Tue Aug 22 2017 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-5.20170118gita77bf99
- remove %%clean section, not needed in Fedora

* Tue Aug 22 2017 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-4.20170118gita77bf99
- don't remove secret file during upgrade
- start service at the end of post scriptlet
- improve SELinux rules handling (now requires a running SELinux)

* Tue Aug 22 2017 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-3.20170118gita77bf99
- Thanks Robert-André Mauchin for the review
- snapshot is packaged to get this necessary fix: https://github.com/roehling/postsrsd/pull/65
- fixed version
- fixed source URL
- use macros for standard paths and build steps
- add missing systemd scriptlets
- specify doc and license files
- remove unnecessary Requires on base64
- remove Group information unsupported in Fedora

* Fri Apr 14 2017 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-2
- create /etc/postsrsd.secret if missing
- move systemd config into directory for packages
- move chroot directory into /run
- autocreate chroot directory

* Thu Mar 30 2017 Marc Dequènes (Duck) <duck@redhat.com> - 1.4-1
- initial packaging

