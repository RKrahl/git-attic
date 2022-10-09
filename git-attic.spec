%bcond_without tests

%define gitexecdir %{_prefix}/lib/git

Name:		git-attic
Version:	$version
Release:	0
Url:		$url
Summary:	$description
License:	Apache-2.0
Group:		Development/Tools/Version Control
Source:		%{name}-%{version}.tar.gz
BuildRequires:	python3-base >= 3.5
BuildRequires:	python3-setuptools
BuildRequires:	git-core >= 2.18.0
%if %{with tests}
BuildRequires:	python3-distutils-pytest
BuildRequires:	python3-pytest >= 3.9
%endif
Requires:	git >= 2.18.0
Recommends:	man
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
$long_description


%prep
%setup -q


%build
python3 setup.py build


%install
python3 setup.py install \
	--prefix=%{_prefix} \
	--root=%{buildroot} \
	--install-scripts=%{gitexecdir}
%__mv %{buildroot}%{gitexecdir}/git-attic.py %{buildroot}%{gitexecdir}/git-attic

%__install -d -m 755 %{buildroot}%{_mandir}/man1
%__cp -p doc/man/*.1 %{buildroot}%{_mandir}/man1


%if %{with tests}
%check
python3 setup.py test
%endif


%files
%defattr(-,root,root)
%doc README.rst CHANGES.rst
%license LICENSE.txt
%{gitexecdir}/*
%exclude %{python3_sitelib}/*.egg-info
%{_mandir}/man1/*


%changelog
