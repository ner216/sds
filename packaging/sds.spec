%define debug_package %{nil}
%define _build_id_links none

Name:           sds
Version:        2.0.0
Release:        1%{?dist}
Summary:        Self-contained SDS Application
License:        MIT
Source0:        %{name}-%{version}.tar.gz

# Tells RPM not to look for system python/qt dependencies
AutoReqProv:    no

%description
A cross-platform password manager.

%prep
%setup -q

%install
# Install the main app bundle to /opt
mkdir -p %{buildroot}/opt/%{name}
cp -rp * %{buildroot}/opt/%{name}/

# Create the symlink in /usr/bin
mkdir -p %{buildroot}%{_bindir}
ln -s ../../opt/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

# Install the Desktop File
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 sds.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
/opt/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Mon Apr 13 2026 Nolan <you@example.com> - 2.0.0-1
- Initial complete Fat RPM build
