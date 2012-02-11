#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_qos
%define mod_conf B36_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A quality of service module for the Apache Web Server
Name:		apache-%{mod_name}
Version:	9.28
Release:	%mkrel 5
Group:		System/Servers
License:	GPL
URL:		http://mod-qos.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/mod-qos/%{mod_name}-%{version}.tar.gz
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_qos is a quality of service module for the Apache Web Server. It implements
control mechanisms that can provide different priority to different requests
and controls server access based on available resources.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix {} \;

%build

pushd tools
%configure2_5x \
    --bindir=%{_sbindir}
%make
popd

%{_sbindir}/apxs -c -DHAVE_OPENSSL apache2/mod_qos.c -lssl -lcrypto

%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/* README.TXT
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_qos.so
%attr(0755,root,root) %{_sbindir}/*
%dir %attr(0711,apache,apache) /var/lib/%{mod_name}
