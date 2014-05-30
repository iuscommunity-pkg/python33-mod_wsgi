
%global pybasever 3.3
%global pyver 33
%global real_name mod_wsgi

# not supported by python33 in IUS currently
#%%global __os_install_post %{__python26_os_install_post}
%global __python %{_bindir}/python%{pybasever}

Name:           python%{pyver}-mod_wsgi
Version:        4.1.1
Release:        1.ius%{?dist}
Summary:        A WSGI interface for Python web applications in Apache

Group:          System Environment/Libraries
License:        ASL 2.0
Vendor:         IUS Community Project
URL:            http://modwsgi.readthedocs.org
Source0:        https://github.com/GrahamDumpleton/mod_wsgi/archive/%{version}.tar.gz
Source1:        python33-mod_wsgi.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel
BuildRequires:  python%{pyver}, python%{pyver}-devel
Provides:       %{real_name} = %{version}

Obsoletes:      mod_wsgi-python%{pyver} < 3.2-2
Provides:       mod_wsgi-python%{pyver} = %{version}-%{release}


%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -q -n %{real_name}-%{version}


%build
%configure --with-python=python%{pybasever}
make LDFLAGS="-L%{_libdir}" %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf

mv  %{buildroot}%{_libdir}/httpd/modules/mod_wsgi.so \
    %{buildroot}%{_libdir}/httpd/modules/%{name}.so

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENCE README.rst
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_libdir}/httpd/modules/%{name}.so


%changelog
* Fri May 30 2014 Ben Harper <ben.harper@rackspace.com> - 4.1.1-1.ius
- Latest sources from upstream

* Mon Oct 29 2012 Ben Harper <ben.harper@rackspace.com> - 3.4-2.ius
- correcting python33-mod_wsgi.conf
- removed %posttrans dealing with mod_wsgi-python32 specific issues

* Tue Oct 16 2012 Ben Harper <ben.harper@rackspae.com> - 3.4-1.ius
- porting from python32-mod_wsgi

* Tue Sep 04 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.4-1.ius
- Latest sources
- See if 3.4 resolves https://bugs.launchpad.net/ius/+bug/1045118

* Mon Jul 30 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.3-4.ius
- New build for python32
