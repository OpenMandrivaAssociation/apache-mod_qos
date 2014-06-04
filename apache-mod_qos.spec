#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_qos
%define mod_conf B36_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A quality of service module for the Apache Web Server
Name:		apache-%{mod_name}
Version:	10.30
Release:	2
Group:		System/Servers
License:	GPLv2+
URL:		http://mod-qos.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/mod-qos/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	dos2unix
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
BuildRequires:	pcre-devel
BuildRequires:	libpng-devel

%description
mod_qos is a quality of service module for the Apache Web Server. It implements
control mechanisms that can provide different priority to different requests
and controls server access based on available resources.

%prep

%setup -q -n %{mod_name}-%{version}
cp %{SOURCE1} %{mod_conf}

find -type f -exec dos2unix {} \;

%build

pushd tools
autoreconf -fi
%configure2_5x \
    --bindir=%{_sbindir}
make
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
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%doc doc/* README.TXT
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_qos.so
%attr(0755,root,root) %{_sbindir}/*
%dir %attr(0711,apache,apache) /var/lib/%{mod_name}
