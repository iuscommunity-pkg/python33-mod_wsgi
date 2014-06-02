%global pymajor 3
%global pyminor 3
%global pyver %{pymajor}.%{pyminor}
%global iusver %{pymajor}%{pyminor}
%global __python3 %{_bindir}/python%{pyver}
%global python3_sitelib  %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global srcname mod_wsgi

Name:           python%{iusver}-%{srcname}
Version:        4.1.1
Release:        1.ius%{?dist}
Summary:        A WSGI interface for Python web applications in Apache
Vendor:         IUS Community Project
Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://modwsgi.readthedocs.org
Source0:        https://github.com/GrahamDumpleton/%{srcname}/archive/%{version}.tar.gz
Source1:        %{name}.conf
BuildRequires:  httpd-devel
BuildRequires:  python%{iusver}-devel
Requires:       httpd
Requires:       python%{iusver}
Provides:       %{srcname} = %{version}


%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.


%prep
%setup -q -n %{srcname}-%{version}


%build
%configure --with-python=%{__python3}
make LDFLAGS="-L%{_libdir}" %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
mv %{buildroot}%{_libdir}/httpd/modules/{%{srcname},%{name}}.so


%clean
rm -rf %{buildroot}


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
