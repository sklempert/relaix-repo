%define _CMAKE_INSTALL_PREFIX \\/usr
%define _POSTSRSD postsrsd
%define _PROJECT_NAME postsrsd
%define _CHROOT_DIR \\/var\\/lib\\/postsrsd
%define _CONFIG_DIR \\/etc\\/sysconfig
%define _SYSCONF_DIR \\/etc


Name:		postsrsd
Version:	1.1
Release:	2%{?dist}
Summary:	PostSRSd provides the Sender Rewriting Scheme (SRS) via TCP-based lookup tables for Postfix.

Group:		System Environment/Daemons
License:	GPL
URL:		https://github.com/roehling/%{name}/archive/%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
Patch0:		postsrsd-1.1-listen.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:	cmake make gcc
Requires:	postfix

%description
PostSRSd provides the Sender Rewriting Scheme (SRS) via TCP-based 
lookup tables for Postfix. SRS is needed if your mail server acts 
as forwarder.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1


%build
make %{?_smp_mflags}


%install
%{__cat} init/postsrsd.sysv-redhat.in | %{__sed} -e "s/@CMAKE_INSTALL_PREFIX@/%{_CMAKE_INSTALL_PREFIX}/g" \
	| %{__sed} -e "s/@POSTSRSD@/%{_POSTSRSD}/g" | %{__sed} -e "s/@PROJECT_NAME@/%{_PROJECT_NAME}/g" \
	| %{__sed} -e "s/@CHROOT_DIR@/%{_CHROOT_DIR}/g" \
	| %{__sed} -e "s/@SYSCONF_DIR@/%{_SYSCONF_DIR}/g" \
	| %{__sed} -e "s/@CONFIG_DIR@/%{_CONFIG_DIR}/g" > postsrsd.sysv-redhat.proc
%{__mkdir_p} %{buildroot}%{_initrddir}
%{__install} -m 0755 postsrsd.sysv-redhat.proc %{buildroot}%{_initrddir}/%{name}
%{__cat} build/postsrsd.default | %{__sed} -e "s/^CHROOT=.*$/CHROOT=%{_CHROOT_DIR}/g"  > postsrsd.default.proc
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 0644 postsrsd.default.proc %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__mkdir_p} %{buildroot}%{_sbindir}
%{__install} -m 0755 build/postsrsd %{buildroot}%{_sbindir}/%{name}
%{__mkdir_p} %{buildroot}%{_var}/lib/%{name}


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md main.cf.ex
%{_initrddir}/%{name}
%{_sbindir}/%{name}
%config %{_sysconfdir}/sysconfig/%{name}
%dir %{_var}/lib/%{name}
%attr(700, nobody, nobody) %{_var}/lib/%{name}


%pre
if [ ! -f "%{_sysconfdir}/postsrsd.secret" ]; then
	dd if=/dev/urandom bs=18 count=1 status=noxfer 2> /dev/null | base64 > %{_sysconfdir}/postsrsd.secret
	%{__chmod} 0600 %{_sysconfdir}/postsrsd.secret
fi


%post 
chkconfig --add %{name}
chkconfig %{name} on


%postun
if [ -f "%{_sysconfdir}/postsrsd.secret" ]; then 
	rm -f "%{_sysconfdir}/postsrsd.secret"
fi


%changelog
* Mon May 30 2016 sklempert@relaix.net - 1.1-2

  Adjusted to newest version and allow non local listening
* Fri Jan 3 2014 timeos@zssos.sk - 1.1

  Built from latest upstream version.
* Thu Dec 31 2013 timeos@zssos.sk - 0.1

  Initial - Built from upstream version.
