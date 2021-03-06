Name: katello-agent
Version: 1.5.3
Release: 1%{?dist}
Summary: The Katello Agent
Group:   Development/Languages
License: LGPLv2
URL:     https://fedorahosted.org/katello/
Source0: https://fedorahosted.org/releases/k/a/katello/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: rpm-python
Requires: gofer >= 1.0.12
Requires: python-gofer-qpid >= 1.0.12
Requires: python-pulp-agent-lib >= 2.4.0
Requires: pulp-rpm-handlers >= 2.4.0
Requires: subscription-manager

%description
Provides plugin for gofer, which allows communicating with Katello server
and execute scheduled actions.

%prep
%setup -q

%build
pushd src
%{__python} setup.py build
popd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/gofer/plugins
mkdir -p %{buildroot}/%{_prefix}/lib/gofer/plugins

cp etc/gofer/plugins/katelloplugin.conf %{buildroot}/%{_sysconfdir}/gofer/plugins
cp src/katello/agent/katelloplugin.py %{buildroot}/%{_prefix}/lib/gofer/plugins

mkdir -p %{buildroot}/%{_prefix}/lib/yum-plugins
cp src/yum-plugins/package_upload.py %{buildroot}/%{_prefix}/lib/yum-plugins

mkdir -p %{buildroot}/%{_sysconfdir}/yum/pluginconf.d/
cp etc/yum/pluginconf.d/package_upload.conf %{buildroot}/%{_sysconfdir}/yum/pluginconf.d/package_upload.conf

mkdir -p %{buildroot}%{_sbindir}
cp bin/katello-package-upload %{buildroot}%{_sbindir}/katello-package-upload

%clean
rm -rf %{buildroot}

%post
chkconfig goferd on
service goferd restart

%postun
LC_ALL=C service goferd status | grep 'is running' && service goferd restart

%files
%config(noreplace) %{_sysconfdir}/gofer/plugins/katelloplugin.conf
%{_prefix}/lib/gofer/plugins/katelloplugin.*
%{_sysconfdir}/yum/pluginconf.d/package_upload.conf
%attr(750, root, root) %{_sbindir}/katello-package-upload
%{_prefix}/lib/yum-plugins

%doc LICENSE

%changelog
* Tue May 20 2014 Justin Sherrill <jsherril@redhat.com> 1.5.3-1
  (jlsherrill@gmail.com)
- Fix agent requirements for pulp 2.4; catch and report errors sending the
  enabled report. (jortel@redhat.com)

* Fri May 16 2014 Justin Sherrill <jsherril@redhat.com> 1.5.2-1
- Ensure EnabledReport filters by basename. (jortel@redhat.com)
- agent requires gofer >= 1.0.10. (jortel@redhat.com)
- add unit tests. (jortel@redhat.com)
- Refit agent to work with gofer 1.0+ and pulp 2.4+. (jortel@redhat.com)

* Fri Oct 11 2013 Partha Aji <paji@redhat.com> 1.5.1-1
- Bumping package versions for 1.5 (paji@redhat.com)

* Fri Oct 11 2013 Partha Aji <paji@redhat.com> 1.4.5-1
- Implement conduit for pulp 2.3 compat (jortel@redhat.com)
- Autobuild f19 packages (paji@redhat.com)

* Wed Jul 31 2013 Partha Aji <paji@redhat.com> 1.4.4-1
- add katello-nightly-fedora19 to tito.props (msuchy@redhat.com)

* Thu Jun 06 2013 Miroslav Suchý <msuchy@redhat.com> 1.4.3-1
- 893596 - sending up baseurl of repos from katello-agent (jsherril@redhat.com)

* Sat Apr 27 2013 Mike McCune <mmccune@redhat.com> 1.4.2-1
- adding rel-eng directory for new location (mmccune@redhat.com)

* Fri Apr 12 2013 Justin Sherrill <jsherril@redhat.com> 1.4.1-1
- version bump to 1.4 (jsherril@redhat.com)

* Fri Apr 12 2013 Justin Sherrill <jsherril@redhat.com> 1.3.2-1
- remove old changelog entries (msuchy@redhat.com)
- 872528 - restart gofer after katello-agent upgrade (msuchy@redhat.com)

* Mon Jan 07 2013 Justin Sherrill <jsherril@redhat.com> 1.3.1-1
- Refit agent for pulp v2. (jortel@redhat.com)

* Fri Oct 12 2012 Lukas Zapletal <lzap+git@redhat.com> 1.1.3-1
- 

* Fri Aug 24 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.2-1
- 845643 - consistently use rpm macros (msuchy@redhat.com)

* Thu Aug 23 2012 Mike McCune <mmccune@redhat.com> 1.1.1-1
- buildroot and %%clean section is not needed (msuchy@redhat.com)
- Bumping package versions for 1.1. (msuchy@redhat.com)

* Tue Jul 31 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.6-1
- update copyright years (msuchy@redhat.com)
- point Source0 to fedorahosted.org where tar.gz are stored (msuchy@redhat.com)

* Fri Jul 27 2012 Lukas Zapletal <lzap+git@redhat.com> 1.0.5-1
- macro python_sitelib is not used anywhere, removing
- provide more descriptive description
- put plugins into correct location
- build root is not used since el6 (inclusive)
- point URL to our wiki
- %%defattr is not needed since rpm 4.4

* Wed Jun 27 2012 Lukas Zapletal <lzap+git@redhat.com> 1.0.4-1
- 828533 - changing to proper QPIDD SSL port
