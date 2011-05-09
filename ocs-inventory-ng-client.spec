# TODO:
# - init script, and choice daemon/cron in /etc/sysconfig/ocsinventory-agent (example in debian)
# - check (Build)Requires 

Summary:	OCS-ng Inventory agent for PLD systems
Summary(pl.UTF-8):	Agent OCS-ng Inventory dla systemów PLD
Name:		ocs-inventory-ng-client
Version:	2.0
Release:	0.1
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://launchpad.net/ocsinventory-unix-agent/stable-2.0/2.0/+download/Ocsinventory-Agent-%{version}.tar.gz
# Source0-md5:	58d21f2a172f0692751d382995b7e6e5
Source1:	%{name}.logrotate
Source2:	%{name}.cron
Source3:	%{name}.sysconfig
URL:		http://www.ocsinventory-ng.org/
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-devel >= 1:5.6
Requires:	dmidecode
Requires:	perl-Digest-MD5
Requires:	perl-IO-Compress
Requires:	perl-Net-IP >= 1.21
Requires:	perl-Net-SSLeay
Requires:	perl-XML-Simple >= 2.12
Suggests:	dmidecode
Suggests:	nmap
Suggests:	pciutils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCS-ng Inventory agent for PLD systems.

%description -l pl.UTF-8
Agent OCS-ng Inventory dla systemów PLD.

%prep
%setup -q -n Ocsinventory-Agent-%{version}

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

ln -s %{_sbindir}/ocsinventory-client.pl $RPM_BUILD_ROOT/bin/ocsinv
ln -s /etc/sysconfig/ocsinventory-agent $RPM_BUILD_ROOT%{_sysconfdir}/ocsinventory-agent/ocsinventory-agent
install %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ocsinventory-agent
install %SOURCE2 $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/ocsinventory-agent
install %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ocsinventory-agent

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Ocsinventory/Agent/.packlist
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/ocsinventory-agent
%dir %{_sysconfdir}/ocsinventory-agent
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ocsinventory-agent/ocsinventory-agent
%attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.daily/ocsinventory-agent
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ocsinventory-agent
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
%{_mandir}/man1/*
%{_mandir}/man3/*
