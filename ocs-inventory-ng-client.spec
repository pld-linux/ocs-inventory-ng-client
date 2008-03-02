
Summary:	OCS-ng Inventory agent for PLD systems
Summary(pl.UTF-8):	Agent OCS-ng Inventory dla systemów PLD
Name:		ocs-inventory-ng-client
Version:	1.01
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/ocsinventory/OCSNG_LINUX_AGENT_%{version}.tar.gz
# Source0-md5:	9e5a5893cd83eb94637c34b60286dcb8
Source1:	%{name}.conf
Source2:	%{name}.adm
Source3:	%{name}.cron
Source4:	%{name}.logrotate
URL:		http://www.ocsinventory-ng.org/
BuildRequires:	perl-devel >= 1:5.6
BuildRequires:	perl-ExtUtils-MakeMaker
Requires:	perl-Net-SSLeay
Requires:	libwww-perl
Requires:	perl-Digest-MD5
Requires:	perl-XML-Simple >= 2.12
Requires:	dmidecode
Requires:	ipdiscover
Requires:	perl-Net-IP >= 1.21
Requires:	perl-Compress-Zlib >= 1.33
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCS-ng Inventory agent for PLD systems.

%description -l pl.UTF-8
Agent OCS-ng Inventory dla systemów PLD.

%prep
%setup -q -n OCSNG_LINUX_AGENT_%{version}

# undos the source
find '(' -name '*.php' -o -name '*.inc' -o  -name '*.conf' -o  -name '*.htc' -o  -name '*.js' -o  -name '*.dtd' -o  -name '*.pm' -o  -name '*.css' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%build
cd Ocsinventory
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sysconfdir}/{logrotate.d,ocsinventory-client,cron.d}}
install -d $RPM_BUILD_ROOT{%{_var}/log/ocsinventory-client,%{_bindir},%{_sbindir},/bin}

OCS_AGENT_ADMININFO_FILE="ocsinv.adm"

cd Ocsinventory
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s /usr/sbin/ocsinventory-client.pl $RPM_BUILD_ROOT/bin/ocsinv
install %SOURCE4 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ocsinventory-client
install %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/ocsinventory-client/ocsinv.conf
install %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/ocsinventory-client

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README changelogs 
#Ocsinventory/README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/ocsinventory-client
%dir %{_sysconfdir}/ocsinventory-client
%{_sysconfdir}/ocsinventory-client/ocsinv.conf
%{_sysconfdir}/cron.d/ocsinventory-client
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /bin/ocsinv
%{_datadir}/%{name}/
%dir %{perl_vendorlib}/Ocsinventory
%{perl_vendorlib}/Ocsinventory/Agent.pm
%{perl_vendorlib}/Ocsinventory/ocsinventory-client.pl
%dir %{perl_vendorlib}/Ocsinventory/Agent
%{perl_vendorlib}/Ocsinventory/Agent/*
%dir %{_var}/log/ocsinventory-client
