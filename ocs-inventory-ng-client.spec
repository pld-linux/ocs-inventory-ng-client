#TODO:
# - init script, and choice daemon/cron in /etc/sysconfig/ocsinventory-agent (example in debian)

Summary:	OCS-ng Inventory agent for PLD systems
Summary(pl.UTF-8):	Agent OCS-ng Inventory dla systemów PLD
Name:		ocs-inventory-ng-client
Version:	1.02
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/ocsinventory/OCSNG_UNIX_AGENT-%{version}.tar.gz
# Source0-md5:	749501586e0c634680c13000b3b2851e
Source1:        %{name}.logrotate
Source2:	%{name}.cron
Source3:        %{name}.sysconfig
URL:		http://www.ocsinventory-ng.org/
BuildRequires:	perl-devel >= 1:5.6
BuildRequires:	perl-ExtUtils-MakeMaker
Requires:	perl-Net-SSLeay
Requires:	perl-Digest-MD5
Requires:	perl-XML-Simple >= 2.12
Requires:	dmidecode
Requires:	perl-Net-IP >= 1.21
Requires:	perl-Compress-Zlib >= 1.33
Requires:	perl-XML-Simple
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCS-ng Inventory agent for PLD systems.

%description -l pl.UTF-8
Agent OCS-ng Inventory dla systemów PLD.

%prep
%setup -q -n Ocsinventory-Agent-1.0.1

# undos the source
find '(' -name '*.php' -o -name '*.inc' -o  -name '*.conf' -o  -name '*.htc' -o  -name '*.js' -o  -name '*.dtd' -o  -name '*.pm' -o  -name '*.css' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

# remove script for migration from old or make new configuration files 
mv postinst.pl postinst.pl.old
touch postinst.pl

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sysconfdir}/{sysconfig,logrotate.d,ocsinventory-agent,cron.daily}}
install -d $RPM_BUILD_ROOT{%{_var}/{log/ocsinventory-agent,lib/ocsinventory-agent},%{_bindir},%{_sbindir},/bin}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s /usr/sbin/ocsinventory-client.pl $RPM_BUILD_ROOT/bin/ocsinv
ln -s /etc/sysconfig/ocsinventory-agent $RPM_BUILD_ROOT%{_sysconfdir}/ocsinventory-agent/ocsinventory-agent
install %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ocsinventory-agent
install %SOURCE2 $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/ocsinventory-agent
install %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ocsinventory-agent

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README 
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/ocsinventory-agent
%dir %{_sysconfdir}/ocsinventory-agent
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ocsinventory-agent/ocsinventory-agent
%attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cron.daily/ocsinventory-agent
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/ocsinventory-agent
#%{_sysconfdir}/init.d/ocsinventory-agent
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /bin/ocsinv
%{_datadir}/%{name}/
%dir %{perl_vendorlib}/Ocsinventory
%{perl_vendorlib}/Ocsinventory/*.pm
%{perl_vendorlib}/Ocsinventory/*.pl
%dir %{perl_vendorlib}/Ocsinventory/LoggerBackend
%{perl_vendorlib}/Ocsinventory/LoggerBackend/*.pm
%dir %{perl_vendorlib}/Ocsinventory/Agent
%{perl_vendorlib}/Ocsinventory/Agent/*
%dir %{_var}/log/ocsinventory-agent
%{_mandir}/man1/ocsinventory-agent.1p.gz
