%define pack qtjambi-src-gpl-4.4.0_01
%define libqtjambi %mklibname qtjambi 1

Name: qtjambi
Version: 4.4.0
Release: %mkrel 3
Summary: Cross-platform, rich client application development framework for Java
Source: %{pack}.tar.gz
Patch0: qtjambi-src-gpl-4.4.0_01-dirbuild.patch
URL: https://trolltech.com/products/qt/jambi
License: GPL
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: java-rpmbuild
BuildRequires: java-devel
BuildRequires: qt4-devel >= 2:4.4.0
BuildRequires: ant
BuildRequires: ant-trax
Requires: %libqtjambi = %version
Requires: qt4-common
Requires: java

%description
Qt Jambi is a cross-platform, rich client application development framework for
Java. It includes a comprehensive class library and integrated development
tools for high-end rich client application development. To organizations
developing high performance, cross-platform desktop applications with Java, Qt
Jambi increases development efficiency, adds freedom and flexibility to Java
development, and provides the assurances of a solid, mature framework.

%files
%defattr(-,root,root,-)
%qt4plugins/qtjambi
%_jnidir/*

#-------------------------------------------------------------

%package -n %libqtjambi
Summary: Qt Jambi main libraries
Group: System/Libraries

%description -n %libqtjambi
Qt Jambi main libraries.

%files -n %libqtjambi
%defattr(-,root,root,-)
%qt4lib/*.so.*

#-------------------------------------------------------------

%package doc
Summary: Qt Jambi documentation
Group: Books/Computer books

%description doc
Qt Jambi documentation.

%files doc
%defattr(-,root,root,-)
%_docdir/qtjambi
%exclude %_docdir/qtjambi/com

#-------------------------------------------------------------

%package demo
Summary: Qt Jambi launcher demo
Group: Books/Computer books
Obsoletes: qtjambi-launcher
Requires: %name
Requires: %name-doc

%description demo
Qt Jambi launcher demo.

%files demo
%defattr(-,root,root,-)
%_bindir/qtjambi-demo
%_docdir/qtjambi/com

#-------------------------------------------------------------

%package devel
Summary: Qt Jambi devel
Group: Development/Java
Requires: %name
Requires: qt4-designer >= 4.3.1
Requires: qt4-devel >= 2:4.3.1
Requires: java-devel

%description devel
Qt Jambi devel.

%files devel
%defattr(-,root,root,-)
%_bindir/designer-qtjambi
%qt4dir/bin/juic
%qt4dir/bin/generator
%qt4include/*
%qt4plugins/designer
%qt4lib/*.so

#-------------------------------------------------------------

%prep
%setup -q -n %{pack}
%patch0 -p1 -b .build

%build
export JAVADIR=%{_jvmdir}/java
export QTDIR=%qt4dir
export QTLIBDIR=%qt4lib
export QTPLUGINDIR=%qt4plugins
export PATH=%qt4dir/bin:$PATH

ant

										
%install
rm -rf %buildroot

# Not default install yet, need do it manually.
# Will prefer use standard qt4 dir as usual
mkdir -p %buildroot/%qt4dir/bin
mkdir -p %buildroot/%qt4include
mkdir -p %buildroot/%qt4lib
mkdir -p %buildroot/%qt4plugins
mkdir -p %buildroot/%_jnidir
mkdir -p %buildroot/%_docdir/qtjambi
mkdir -p %buildroot/%_docdir/qtjambi/com/trolltech
mkdir -p %buildroot/%_bindir

# Create base jar
jar cf %buildroot/%_jnidir/qtjambi-%version.jar com/trolltech/qt com/trolltech/tools
pushd %buildroot/%_jnidir
    ln -s qtjambi-%version.jar qtjambi.jar
popd

for name in demos examples images launcher; do
	cp -a com/trolltech/$name %buildroot/%_docdir/qtjambi/com/trolltech
done
cp -a doc %buildroot/%_docdir/qtjambi
cp -a generator_example %buildroot/%_docdir/qtjambi
cp -a plugins/* %buildroot/%qt4plugins 
cp -aP lib/* %buildroot/%qt4lib
cp bin/juic generator/generator %buildroot/%qt4dir/bin
cp include/* %buildroot/%qt4include
pushd %buildroot/%_docdir/qtjambi/doc
    tar xfj %SOURCE1
popd

# DESIGNER WITH JAMBI
cat > %buildroot/%_bindir/designer-qtjambi << EOF
#!/bin/sh
# Support script to properly set environments for Designer with Jambi to run
export QTDIR=%qt4dir
export PATH=%qt4dir/bin:$PATH
export JAVADIR=%{_jvmdir}/java 
export CLASSPATH=%_jnidir/qtjambi.jar
export MOC=%qt4dir/bin/moc
export UIC=%qt4dir/bin/juic

exec %qt4dir/bin/designer-real "\$@"
EOF
chmod 0755 %buildroot/%_bindir/designer-qtjambi

# LAUNCHER
cat > %buildroot/%_bindir/qtjambi-demo << EOF
#!/bin/sh
# Support script to properly set environments for Launcher
export JAVADIR=%{_jvmdir}/jre
cd %_docdir/qtjambi/
java -Djava.library.path=%qt4lib -cp %_jnidir/qtjambi.jar:. com.trolltech.launcher.Launcher
EOF
chmod 0755 %buildroot/%_bindir/qtjambi-demo

%clean
rm -rf %buildroot

