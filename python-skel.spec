%bcond_with tests
%global distname $distname

Name:		python3-%{distname}
Version:	$version
Release:	0
Url:		$url
Summary:	$description
License:	Apache-2.0
Group:		Development/Libraries/Python
Source:		%{distname}-%{version}.tar.gz
BuildRequires:	python3-base >= 3.4
%if %{with tests}
BuildRequires:	python3-distutils-pytest
BuildRequires:	python3-pytest >= 3.0
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
$long_description


%prep
%setup -q -n %{distname}-%{version}


%build
python3 setup.py build


%install
python3 setup.py install --optimize=1 --prefix=%{_prefix} --root=%{buildroot}


%if %{with tests}
%check
python3 setup.py test
%endif


%files
%defattr(-,root,root)
%doc README.rst CHANGES.rst
%{python3_sitelib}/*


%changelog
