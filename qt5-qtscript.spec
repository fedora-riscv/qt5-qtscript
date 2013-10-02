
%global qt_module qtscript
%define pre alpha

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
%define docs 1

Summary: Qt5 - QtScript component
Name:    qt5-%{qt_module}
Version: 5.2.0
Release: 0.1.%{pre}%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.2/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif

# http://bugzilla.redhat.com/1005482
ExcludeArch: ppc64 ppc

BuildRequires: qt5-qtbase-devel >= %{version}

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
%{_qt5_qmake}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

## .prl file love (maybe consider just deleting these -- rex
# nuke dangling reference(s) to %%buildroot, excessive (.la-like) libs
sed -i \
  -e "/^QMAKE_PRL_BUILD_DIR/d" \
  -e "/^QMAKE_PRL_LIBS/d" \
  %{buildroot}%{_qt5_libdir}/*.prl

## unpackaged files
# .la files, die, die, die.
rm -fv %{buildroot}%{_qt5_libdir}/lib*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LGPL_EXCEPTION.txt LICENSE.GPL  LICENSE.LGPL
%{_qt5_libdir}/libQt5Script.so.5*
%{_qt5_libdir}/libQt5ScriptTools.so.5*

%files devel
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5*.so
%{_qt5_libdir}/libQt5*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtscript.qch
%{_qt5_docdir}/qtscript/
%{_qt5_docdir}/qtscripttools.qch
%{_qt5_docdir}/qtscripttools/
%endif


%changelog
* Tue Oct 01 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- update Source URL
- %%doc LGPL_EXCEPTION.txt LICENSE.GPL LICENSE.LGPL

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

