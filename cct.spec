#
# CCT specfile
#
# Copyright (C) 2014 Cyril Hrubis <metan@ucw.cz>
#

Summary: Fast and efficient templating language
Name: cct
Version: 1.0.0
Release: 1
License: GPL-2.1+
Group: Devel/Tools/Other
Url: https://github.com/metan-ucw/cct
Source: cct-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}_%{version}-buildroot
BuildArch: noarch
Requires: python

%description
Fast and efficient Python based templating
language designed for generating source code.

%prep
%setup -n cct-%{version}

%build

%install
make install bindir=%{_bindir} DESTDIR="$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%{_bindir}/cct.py
%{_bindir}/cct

%changelog
* Wed Oct 22 2014 Cyril Hrubis <metan@ucw.cz>

Initial version.
