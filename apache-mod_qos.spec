#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_qos
%define mod_conf B36_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A quality of service module for the Apache Web Server
Name:		apache-%{mod_name}
Version:	10.11
Release:	1
Group:		System/Servers
License:	GPLv2+
URL:		http://mod-qos.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/mod-qos/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_qos-9.28-ssl_fix.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	dos2unix
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	libpng-devel

%description
mod_qos is a quality of service module for the Apache Web Server. It implements
control mechanisms that can provide different priority to different requests
and controls server access based on available resources.

%prep

%setup -q -n %{mod_name}-%{version}
#patch0 -p0

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix {} \;

%build

pushd tools
%configure2_5x \
    --bindir=%{_sbindir}
%make
popd

%{_bindir}/apxs -c -DHAVE_OPENSSL apache2/mod_qos.c -lssl -lcrypto

%install

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}/var/lib/%{mod_name}

install -m0755 apache2/.libs/mod_qos.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%makeinstall_std -C tools

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%files
%doc doc/* README.TXT
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_qos.so
%attr(0755,root,root) %{_sbindir}/*
%dir %attr(0711,apache,apache) /var/lib/%{mod_name}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 9.28-5mdv2012.0
+ Revision: 772750
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 9.28-4
+ Revision: 678404
- mass rebuild

* Thu Dec 02 2010 Paulo Andrade <pcpa@mandriva.com.br> 9.28-3mdv2011.0
+ Revision: 605238
- Rebuild with apr with workaround to issue with gcc type based

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 9.28-2mdv2011.0
+ Revision: 588050
- rebuild

* Tue Oct 19 2010 Oden Eriksson <oeriksson@mandriva.com> 9.28-1mdv2011.0
+ Revision: 586722
- 9.28

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 8.13-3mdv2010.1
+ Revision: 516166
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 8.13-2mdv2010.0
+ Revision: 406637
- rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 8.13-1mdv2010.0
+ Revision: 387725
- 8.13

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 7.11-2mdv2009.1
+ Revision: 326224
- rebuild

* Thu Oct 16 2008 Oden Eriksson <oeriksson@mandriva.com> 7.11-1mdv2009.1
+ Revision: 294279
- 7.11

* Sat Aug 16 2008 Oden Eriksson <oeriksson@mandriva.com> 7.5-1mdv2009.0
+ Revision: 272554
- 7.5

* Wed Aug 06 2008 Oden Eriksson <oeriksson@mandriva.com> 7.4-2mdv2009.0
+ Revision: 265123
- enhance the config a bit

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 7.4-1mdv2009.0
+ Revision: 235336
- 7.4
- fix linkage
- rebuild
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Tue May 06 2008 Oden Eriksson <oeriksson@mandriva.com> 6.7-1mdv2009.0
+ Revision: 202139
- import apache-mod_qos


* Tue May 06 2008 Oden Eriksson <oeriksson@mandriva.com> 6.7-1mdv2009.0
- initial Mandriva package
