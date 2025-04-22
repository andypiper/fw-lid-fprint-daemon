Name:           fw-lid-fprint-daemon
Version:        1.0
Release:        1%{?dist}
Summary:        Fingerprint toggle daemon for Framework laptops on Fedora
License:        MIT
URL:            https://github.com/andypiper/fw-lid-fprint-daemon
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       systemd

%description
Installs a persistent systemd daemon that polls the laptop lid + external displays every 15s,
masking or unmasking fprintd accordingly.

%prep
%setup -q

%build
# no build steps

%install
rm -rf %{buildroot}
# Install the daemon script
mkdir -p %{buildroot}/usr/local/bin
install -m 0755 laptop-lid-daemon.sh \
    %{buildroot}/usr/local/bin/laptop-lid-daemon.sh

# Install the service unit
mkdir -p %{buildroot}/etc/systemd/system
install -m 0644 laptop-lid-daemon.service \
    %{buildroot}/etc/systemd/system/laptop-lid-daemon.service

%files
%defattr(-,root,root,-)
/usr/local/bin/laptop-lid-daemon.sh
/etc/systemd/system/laptop-lid-daemon.service

%post
# Reload systemd and enable+start the daemon
%systemd_post fw-lid-fprint-daemon.service

%preun
%systemd_preun fw-lid-fprint-daemon.service

%postun
%systemd_postun_with_restart fw-lid-fprint-daemon.service

%changelog
* Tue Apr 22 2025 Andy Piper <andypiper@omg.lol> - 1.0-1
- Initial RPM for fingerprint toggle daemon (fw-lid-fprint-daemon)

