%{?_javapackages_macros:%_javapackages_macros}
Name:          thredds
Version:       4.3.19
Release:       5.3
Summary:       Thematic Realtime Environmental Distributed Data Services (TDS)
Group:         Development/Java
# GPLv3: opendap/src/main/java/opendap/dap/parsers/DapParser.java
# LGPLv3: opendap/src/main/java/opendap/servlet/AsciiWriter.java
#         visad/src/main/java/ucar/nc2/iosp/mcidas/V5DStruct.java
#         grib/src/main/java/ucar/jpeg
# ASL: tds/src/main/java/thredds/servlet/URLEncoder.java
License:       ASL 2.0 and BSD
URL:           https://www.unidata.ucar.edu/software/tds/
# sh thredds-create-tarball.sh < VERSION >
Source0:       %{name}-%{version}-clean.tar.xz
Source1:       %{name}-create-tarball.sh

# build fix for jna 3.5.0
Patch0:        thredds-4.3.16-cdm-jna35.patch
# Replace commons-httpclient with org.apache.httpcomponents support
# see https://github.com/Unidata/thredds/tree/http4/
Patch1:        thredds-4.3.18-cdm-http4.patch
Patch2:        thredds-4.3.18-cdm-use-proper-system-environment-variables.patch

BuildRequires: java-devel

BuildRequires: mvn(com.google.protobuf:protobuf-java)
BuildRequires: mvn(com.sleepycat:je)
BuildRequires: mvn(joda-time:joda-time) >= 2.0
BuildRequires: mvn(log4j:log4j)
BuildRequires: mvn(net.java.dev.jna:jna)
BuildRequires: mvn(net.jcip:jcip-annotations)
BuildRequires: mvn(net.sf.ehcache:ehcache-core)
BuildRequires: mvn(org.apache.httpcomponents:httpclient)
BuildRequires: mvn(org.apache.httpcomponents:httpcore)
BuildRequires: mvn(org.apache.httpcomponents:httpmime)
BuildRequires: mvn(org.jdom:jdom2)
BuildRequires: mvn(org.quartz-scheduler:quartz)
BuildRequires: mvn(org.slf4j:jcl-over-slf4j)
BuildRequires: mvn(org.slf4j:slf4j-api)
BuildRequires: mvn(org.slf4j:slf4j-log4j12)

# TODO: opendap, grib, tdm, and tds modules
%if 0
BuildRequires: mvn(com.lexicalscope.jewelcli:jewelcli)
BuildRequires: mvn(commons-httpclient:commons-httpclient)
BuildRequires: mvn(edu.wisc.ssec:visad)
BuildRequires: mvn(javax.servlet:servlet-api)
BuildRequires: mvn(javax.servlet:jstl)
BuildRequires: mvn(org.jdom:jdom)
BuildRequires: mvn(org.jsoup:jsoup)
BuildRequires: mvn(org.springframework:spring-beans)
BuildRequires: mvn(org.springframework:spring-context)
BuildRequires: mvn(org.springframework:spring-core)
BuildRequires: mvn(org.springframework:spring-webmvc)
%endif

BuildRequires: maven-local

# test deps
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.slf4j:slf4j-jdk14)

BuildArch:     noarch

%description
The THREDDS (Thematic Realtime Environmental Distributed
Data Services) project is developing middle-ware to bridge the
gap between data providers and data users. The goal is to
simplify the discovery and use of scientific data and to allow
scientific publications and educational materials to reference
scientific data. The mission of THREDDS is for students,
educators and researchers to publish, contribute, find, and
interact with data relating to the Earth system in a convenient,
effective, and integrated fashion. Just as the World Wide Web and
digital-library technologies have simplified the process of
publishing and accessing multimedia documents, THREDDS is building
infrastructure needed for publishing and accessing scientific data
in a similarly convenient fashion.

%package -n netcdf-java
Summary:       Java interface to NetCDF files

%description -n netcdf-java
The NetCDF-Java Library is a Java interface to NetCDF files,
as well as to many other types of scientific data formats.

%if 0
%package -n bufr
Summary:       BUFR IOSP

%description -n bufr
Reading BUFR files with the NetCDF-java library.

%package -n grib
Summary:       GRIB IOSP and Feature Collection

%description -n grib
Decoder for the GRIB format.

%package -n tdm
Summary:       THREDDS Data Manager (TDM)

%description -n tdm
THREDDS Data Manager (TDM).
%endif

%package -n java-udunits
Summary:       Java package for decoding and encoding unit specifications

%description -n java-udunits
The ucar.units Java package is for decoding and encoding
formatted unit specifications (e.g. "m/s"), converting numeric values
between compatible units (e.g. between "m/s" and "knot"), and for
performing arithmetic operations on units (e.g. dividing one unit by
another, raising a unit to a power).

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1

# Disable unavailable build deps
%pom_disable_module visad
%pom_disable_module ncIdv
%pom_disable_module ui
%pom_disable_module tds
%pom_disable_module cdmvalidator
%pom_disable_module cdm-test
%pom_disable_module it
# thredds use customized opendap == 0.0.7 http://www.opendap.org/
%pom_disable_module opendap
# require opendap module
%pom_disable_module dts
# Unwanted ... for now ... it bundled customizzation of jj2000 see http://code.google.com/p/jj2000/
%pom_disable_module grib
%pom_disable_module tdm
%pom_disable_module wmotables
%pom_disable_module bufr
%pom_disable_module tdcommon

# Unwanted
%pom_remove_plugin :maven-source-plugin cdm

# Disable class-path in manifest
%pom_xpath_set "pom:build/pom:pluginManagement/pom:plugins/pom:plugin[pom:artifactId = 'maven-jar-plugin' ]/pom:configuration/pom:archive/pom:manifest/pom:addClasspath" false
# jna 3.0.9
%pom_xpath_set "pom:dependencies/pom:dependency[pom:artifactId = 'jna']/pom:groupId" net.java.dev.jna cdm

sed -i 's/\r//' cdm/CHANGES.txt cdm/license.txt

%build

%mvn_build -s

%install
%mvn_install

install -pm 644 cdm/target/netcdf-%{version}-tests.jar %{buildroot}%{_javadir}/%{name}/netcdf-tests.jar

%files -f .mfiles-%{name}-parent
%dir %{_javadir}/%{name}
%doc README.md cdm/license.txt

%files -n netcdf-java -f .mfiles-netcdf
%{_javadir}/%{name}/netcdf-tests.jar
%doc cdm/CHANGES.txt cdm/license.txt

%if 0
%files -n bufr -f .mfiles-bufr
%doc cdm/license.txt

%files -n grib -f .mfiles-grib
%doc cdm/license.txt

%files -n tdm -f .mfiles-tdm
%doc cdm/license.txt
%endif

%files -n java-udunits -f .mfiles-udunits
%doc cdm/license.txt

%files javadoc -f .mfiles-javadoc
%doc cdm/license.txt

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.19-4
- Rebuild to regenerate broken POMs
- Related: rhbz#1021484

* Sat Oct 19 2013 gil cattaneo <puntogil@libero.it> 4.3.19-3
- renamed sub package udunits

* Sat Oct 19 2013 gil cattaneo <puntogil@libero.it> 4.3.19-2
- fix license field

* Wed Oct 16 2013 gil cattaneo <puntogil@libero.it> 4.3.19-1
- update to 4.3.19

* Mon Sep 16 2013 gil cattaneo <puntogil@libero.it> 4.3.18-1
- update to 4.3.18

* Mon Jun 24 2013 gil cattaneo <puntogil@libero.it> 4.3.16-1
- initial rpm
