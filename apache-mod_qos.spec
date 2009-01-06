#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_qos
%define mod_conf B36_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A quality of service module for the Apache Web Server
Name:		apache-%{mod_name}
Version:	7.11
Release:	%mkrel 2
Group:		System/Servers
License:	GPL
URL:		http://mod-qos.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/mod-qos/%{mod_name}-%{version}-src.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_qos-no_strip.diff
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_qos is a quality of service module for the Apache Web Server. It implements
control mechanisms that can provide different priority to different requests
and controls server access based on available resources.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix -U {} \;

%build

%make -C tools CFLAGS="%{optflags}"

gcc %{optflags} `apr-1-config --cppflags` `apr-1-config --includes` \
    `apr-1-config --link-ld` `pcre-config --libs` `apu-1-config --avoid-ldap --link-ld` -lcrypto \
    -o tools/qsfilter/qsfilter2 tools/qsfilter/qsfilter2.c

%{_sbindir}/apxs -c apache2/mod_qos.c
%{_sbindir}/apxs -c apache2/mod_qos_control.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}/var/lib/%{mod_name}

install -m0755 apache2/.libs/mod_qos.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0755 apache2/.libs/mod_qos_control.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -m0755 tools/qslog %{buildroot}%{_sbindir}/
install -m0755 tools/qsfilter/qsfilter2 %{buildroot}%{_sbindir}/

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/* README.TXT
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_qos.so
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_qos_control.so
%attr(0755,root,root) %{_sbindir}/qslog
%attr(0755,root,root) %{_sbindir}/qsfilter2
%dir %attr(0711,apache,apache) /var/lib/%{mod_name}
