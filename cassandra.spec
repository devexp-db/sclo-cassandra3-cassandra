%{?scl:%scl_package cassandra}
%{!?scl:%global pkg_name %{name}}

# fedora reserved UID and GID for cassandra
%global gid_uid 143

%{!?stress:%global stress 0}

%global cqlsh_version 5.0.1

%global daemon_name %{?scl_prefix}%{pkg_name}

Name:		%{?scl_prefix}cassandra
Version:	3.11.1
Release:	4%{?dist}
Summary:	Client utilities for %{pkg_name}
# Apache (v2.0) BSD (3 clause):
# ./src/java/org/apache/cassandra/utils/vint/VIntCoding.java
License:	ASL 2.0 and BSD
URL:		http://cassandra.apache.org/
Source0:	https://github.com/apache/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz
Source1:	%{pkg_name}.logrotate
Source2:	%{pkg_name}.service
# pom files are not generated but used are the ones from mavencentral
# because of orphaned maven-ant-task package doing the work in this case
Source3:	http://central.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}-all/%{version}/%{pkg_name}-all-%{version}.pom
Source4:	http://central.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}-parent/%{version}/%{pkg_name}-parent-%{version}.pom

# fix encoding, naming, classpaths and dependencies
Patch0:		%{pkg_name}-%{version}-build.patch
# airline0.7 imports fix in cassandra source, which is dependent on 0.6 version
# https://issues.apache.org/jira/browse/CASSANDRA-12994
Patch1:		%{pkg_name}-%{version}-airline0.7.patch
# modify installed scripts
Patch2:		centos-%{pkg_name}-scripts.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1340876
# remove "Open" infix from all hppc classes
# https://issues.apache.org/jira/browse/CASSANDRA-12995X
Patch3:		%{pkg_name}-%{version}-hppc.patch
# add two more parameters for SubstituteLogger constructor in slf4j
# https://issues.apache.org/jira/browse/CASSANDRA-12996
Patch5:		%{pkg_name}-%{version}-slf4j.patch
# remove thrift as it will be removed in next upstream major release
# https://github.com/apache/cassandra/commit/4881d9c308ccd6b5ca70925bf6ebedb70e7705fc
Patch7:		%{pkg_name}-%{version}-remove-thrift.patch
# https://issues.apache.org/jira/projects/CASSANDRA/issues/CASSANDRA-14173
Patch8:         %{pkg_name}-%{version}-Remove-dependencies-on-internal-JMX-classes.patch
# use Guava v24 because in Fedora 28 is not available v18
Patch9:         %{pkg_name}-%{version}-use-guava24.patch
# change mvn dependency to guava v24
Patch10:        %{pkg_name}-%{version}-use-guava24-pom.patch

# TODO
#BuildArchitectures:	noarch

Requires:	%{?scl_prefix}%{pkg_name}-python2-cqlshlib = %{version}-%{release}
Requires:	%{?scl_prefix}%{pkg_name}-java-libs = %{version}-%{release}
Requires:	%{?scl_prefix}airline
Requires:	%{?scl_prefix_java_common}atinject
Provides:	cqlsh = %{cqlsh_version}

%description
This package contains all client utilities for Cassandra. These are:
1. Command line client used to communicate with Cassandra server called cqlsh.
2. Command line interface for managing cluster called nodetool.
3. Tools for using, upgrading, and changing SSTables.

%package java-libs
Summary:	Java libraries for %{pkg_name}

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_java_common}ant
BuildRequires:	%{?scl_prefix_java_common}ecj
BuildRequires:	%{?scl_prefix}jamm
BuildRequires:	%{?scl_prefix}stream-lib
BuildRequires:	%{?scl_prefix}metrics
BuildRequires:	%{?scl_prefix}metrics-jvm
BuildRequires:	%{?scl_prefix}json_simple
BuildRequires:	%{?scl_prefix}compile-command-annotations
BuildRequires:	%{?scl_prefix}jBCrypt
BuildRequires:	%{?scl_prefix}concurrent-trees
BuildRequires:	%{?scl_prefix}logback
BuildRequires:	%{?scl_prefix}metrics-reporter-config
BuildRequires:	%{?scl_prefix}compress-lzf
BuildRequires:	%{?scl_prefix}airline
BuildRequires:	%{?scl_prefix}jmh
BuildRequires:	%{?scl_prefix}byteman
BuildRequires:	%{?scl_prefix}HdrHistogram
BuildRequires:	%{?scl_prefix}sigar-java
BuildRequires:	%{?scl_prefix}jackson
BuildRequires:	%{?scl_prefix}antlr3-tool
BuildRequires:	%{?scl_prefix}caffeine
BuildRequires:	%{?scl_prefix}hppc
BuildRequires:	%{?scl_prefix}lz4-java
BuildRequires:	%{?scl_prefix}snappy-java
BuildRequires:	%{?scl_prefix}cassandra-java-driver
BuildRequires:	%{?scl_prefix}ohc
BuildRequires:	%{?scl_prefix}ohc-core-j8
BuildRequires:	%{?scl_prefix}netty
BuildRequires:	%{?scl_prefix}jflex
BuildRequires:	%{?scl_prefix}apache-commons-math
BuildRequires:	%{?scl_prefix_maven}jna
BuildRequires:	%{?scl_prefix}guava
BuildRequires:	%{?scl_prefix}jctools
# using high-scale-lib from stephenc, no Cassandra original
#BuildRequires:	 mvn(com.boundary:high-scale-lib)
BuildRequires:	%{?scl_prefix}high-scale-lib
# using repackaging of the snowball stemmer so that it's available on Maven Central
#BuildRequires:	mvn(com.github.rholder:snowball-stemmer)
BuildRequires:	%{?scl_prefix}snowball-java
# probably won't need in the future
BuildRequires:	%{?scl_prefix}concurrentlinkedhashmap-lru
# in rh-java-common: 1.7.4, needed: 1.7.7
BuildRequires:	%{?scl_prefix_java_common}log4j-over-slf4j
# in rh-java-common: 1.7.4, needed: 1.7.7
BuildRequires:	%{?scl_prefix_java_common}jcl-over-slf4j
# in rh-java-common: 1.9.2, needed: 1.9.4
BuildRequires:	%{?scl_prefix_java_common}ant-junit
# the SCL version of the package depends on rh-maven33 collection
# TODO
#%{?scl:Requires: %%scl_require rh-maven33}
# transitive dependencies
BuildRequires:	%{?scl_prefix}stringtemplate4
BuildRequires:	%{?scl_prefix_java_common}java_cup
BuildRequires:	%{?scl_prefix_java_common}atinject
BuildRequires:	%{?scl_prefix}slf4j

# temporarly removed because they are optional and missing in fedora
# using hadoop-common instead of hadoop-core, no Cassandra original
#BuildRequires:	mvn(org.apache.hadoop:hadoop-core)
#BuildRequires:	hadoop-common
#BuildRequires:	hadoop-mapreduce

%description java-libs
All the classes required by cassandra server, nodetool, sstable tools
and stress tools.

%package server
Summary:	OpenSource database server for high-scale application

%{?scl:Requires: %scl_runtime}
Requires(pre):	shadow-utils
Requires:	%{?scl_prefix}sigar
Requires:	%{?scl_prefix}%{pkg_name}-java-libs = %{version}-%{release}
Requires:	%{?scl_prefix}jctools
Requires:	%{?scl_prefix}snakeyaml
Requires:	%{?scl_prefix}guava
Requires:	%{?scl_prefix}lz4-java
Requires:	%{?scl_prefix}json_simple
Requires:	%{?scl_prefix}snappy-java
Requires:	%{?scl_prefix}jamm
Requires:	%{?scl_prefix}sigar-java
Requires:	%{?scl_prefix}concurrentlinkedhashmap-lru
Requires:	%{?scl_prefix}metrics
Requires:	%{?scl_prefix}metrics-reporter-config
Requires:	%{?scl_prefix}logback
Requires:	%{?scl_prefix}antlr3-java
Requires:	%{?scl_prefix}slf4j
Requires:	%{?scl_prefix}jackson
Requires:	%{?scl_prefix}netty
Requires:	%{?scl_prefix}high-scale-lib
Requires:	%{?scl_prefix}stream-lib
Requires:	%{?scl_prefix}caffeine
Requires:	%{?scl_prefix}jBCrypt
Requires:	%{?scl_prefix_maven}jna
Requires:	%{?scl_prefix_java_common}apache-commons-codec
Requires:	%{?scl_prefix_java_common}apache-commons-lang3
Requires:	procps-ng
%{?scl:Requires:	nc}
%{!?scl:Requires:	nmap-ncat}
%{?systemd_ordering}
BuildRequires:	systemd

%description server
Cassandra is a partitioned row store. Rows are organized into tables with
a required primary key. Partitioning means that Cassandra can distribute your
data across multiple machines in an application-transparent matter. Cassandra
will automatically re-partition as machines are added/removed from the cluster.
Row store means that like relational databases, Cassandra organizes data by
rows and columns. The Cassandra Query Language (CQL) is a close relative of SQL.

%package parent
Summary:	Parent POM for %{pkg_name}

%description parent
Parent POM for %{pkg_name}.

# source codes of cqlshlib are not python3 compatible, therefore using python2
%package python2-cqlshlib
Summary:	Python cqlsh library for %{pkg_name}
BuildRequires:	python2-devel
BuildRequires:	Cython
Requires:	%{?scl_prefix}python2-cassandra-driver
# optional timestamps in different timezones dependency
Requires:	pytz
%{?python_provide:%python_provide python2-cqlshlib}

%description python2-cqlshlib
A python library required by the commandline client used to communicate with
%{pkg_name} server.

%if %stress
%package stress
Summary:	Stress testing utility for %{pkg_name}

%description stress
A Java-based stress testing utility for basic benchmarking and load testing a %{pkg_name} cluster.
%endif

%package javadoc
Summary:	Javadoc for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -qcn %{pkg_name}-%{version}
cp -pr %{pkg_name}-%{pkg_name}-%{version}/* .
rm -r %{pkg_name}-%{pkg_name}-%{version}

# remove thrift patch
%patch7 -p1

# remove binary and library files
find -name "*.class" -print -delete
find -name "*.jar" -print -delete
find -name "*.zip" -print -delete
#./lib/futures-2.1.6-py2.py3-none-any.zip
#./lib/six-1.7.3-py2.py3-none-any.zip
#./lib/cassandra-driver-internal-only-2.6.0c2.post.zip
find -name "*.so" -print -delete
find -name "*.dll" -print -delete
find -name "*.sl" -print -delete
find -name "*.dylib" -print -delete
rm -r lib/sigar-bin/sigar-x86-winnt.lib
find -name "*.exe" -print -delete
find -name "*.bat" -print -delete
find -name "*.pyc" -print -delete
find -name "*py.class" -print -delete

# copy pom files
mkdir build
cp -p %{SOURCE3} build/%{pkg_name}-%{version}.pom
cp -p %{SOURCE4} build/%{pkg_name}-%{version}-parent.pom

%if 0%{?fedora} >= 28
# swap guava18 to guava24
%patch9 -p1
# change mvn dependency to guava v24
%patch10 -p0
%endif

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# build jar repositories for dependencies
build-jar-repository lib antlr3
build-jar-repository lib stringtemplate4
build-jar-repository lib jsr-305
build-jar-repository lib commons-lang3
build-jar-repository lib slf4j/slf4j-api
build-jar-repository lib guava
build-jar-repository lib jamm
build-jar-repository lib stream-lib
build-jar-repository lib metrics/metrics-core
build-jar-repository lib metrics/metrics-jvm
build-jar-repository lib json_simple
build-jar-repository lib antlr3-runtime
build-jar-repository lib compile-command-annotations
# https://bugzilla.redhat.com/show_bug.cgi?id=1308556
build-jar-repository lib high-scale-lib/high-scale-lib
build-jar-repository lib cassandra-java-driver/cassandra-driver-core
build-jar-repository lib netty/netty-all
build-jar-repository lib netty/netty-common
build-jar-repository lib netty/netty-transport-native-unix-common
build-jar-repository lib netty/netty-transport-native-epoll
build-jar-repository lib lz4-java
build-jar-repository lib snappy-java
build-jar-repository lib jBCrypt
build-jar-repository lib concurrentlinkedhashmap-lru
build-jar-repository lib ohc/ohc-core
build-jar-repository lib snakeyaml
build-jar-repository lib jackson/jackson-core-asl
build-jar-repository lib jackson/jackson-mapper-asl
build-jar-repository lib ecj
build-jar-repository lib objectweb-asm/asm
build-jar-repository lib commons-math3
build-jar-repository lib concurrent-trees
build-jar-repository lib hppc
build-jar-repository lib snowball-java
build-jar-repository lib logback/logback-classic
build-jar-repository lib logback/logback-core
build-jar-repository lib metrics-reporter-config/reporter-config
build-jar-repository lib metrics-reporter-config/reporter-config-base
build-jar-repository lib joda-time
build-jar-repository lib compress-lzf
build-jar-repository lib commons-cli
build-jar-repository lib airline
build-jar-repository lib jna
build-jar-repository lib sigar
# temporarly removed because it is optional
#build-jar-repository lib hadoop/hadoop-annotations
build-jar-repository lib jflex
build-jar-repository lib java_cup
build-jar-repository lib commons-codec
build-jar-repository lib caffeine
build-jar-repository lib jctools
# test dependencies
build-jar-repository lib junit
build-jar-repository lib ant/ant
build-jar-repository lib ant/ant-junit
build-jar-repository lib hamcrest/core
build-jar-repository lib apache-commons-io
build-jar-repository lib byteman/byteman
build-jar-repository lib byteman/byteman-bmunit
build-jar-repository lib commons-collections
build-jar-repository lib jmh/jmh-core
build-jar-repository lib HdrHistogram
# binaries dependencies
build-jar-repository lib atinject
# temporarly removed because they are optional and missing in fedora
#build-jar-repository lib hadoop/hadoop-common
#build-jar-repository lib hadoop/hadoop-mapreduce-client-core
#build-jar-repository lib hadoop/hadoop-annotations

# build patch
%patch0 -p1
# airline patch
%patch1 -p1
# scripts patch
%patch2 -p1
# hppc patch
%patch3 -p1
# slf4j patch
%patch5 -p1
# internal JMX classes remove patch
%patch8 -p1

# remove hadoop
rm -r src/java/org/apache/cassandra/hadoop
sed -i '/hadoop/d' test/microbench/org/apache/cassandra/test/microbench/CompactionBench.java
# remove hadoop also from pom files
%pom_remove_dep -r org.apache.hadoop: build/%{pkg_name}-%{version}.pom

# remove shaded classifier in cassandra driver from pom files
%pom_xpath_remove "pom:dependencies/pom:dependency/pom:classifier" build/%{pkg_name}-%{version}.pom

# update dependencies in the downloaded pom files to those being actually used
%pom_change_dep com.boundary: com.github.stephenc.high-scale-lib: build/%{pkg_name}-%{version}.pom

# remove thrift dependencies from the downloaded pom files
%pom_remove_dep -r com.thinkaurelius.thrift:thrift-server build/%{pkg_name}-%{version}.pom
%pom_remove_dep -r org.apache.cassandra:cassandra-thrift build/%{pkg_name}-%{version}.pom
%pom_remove_dep -r org.apache.thrift:libthrift build/%{pkg_name}-%{version}.pom

# fix antlr dependency (remove antlr as a runtime dependency, just antlr-runtime is needed for that)
%pom_xpath_inject "pom:dependency[pom:artifactId='antlr']" "<scope>provided</scope>" build/%{pkg_name}-%{version}.pom

%mvn_package "org.apache.%{pkg_name}:%{pkg_name}-parent:pom:%{version}" parent
%if %stress
%mvn_package ":%{pkg_name}-stress" stress
%endif
%{?scl:EOF}

# If SCL, fix the path of binary in the systemd unit file and add 'scl enable' command
%{?scl:sed -i -e 's:/usr/bin:%{_bindir}:g' %{SOURCE2}}
%{?scl:sed -i -e 's:ExecStart=:ExecStart=/usr/bin/scl enable sclo-cassandra3 rh-java-common rh-maven33 -- :g' %{SOURCE2}}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
ant jar javadoc -Drelease=true
%{?scl:EOF}

# Build the cqlshlib Python module
%{?scl:scl enable %{scl} - << "EOF"}
pushd pylib
%{__python2} setup.py build
popd
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_artifact build/%{pkg_name}-%{version}-parent.pom
%mvn_artifact build/%{pkg_name}-%{version}.pom build/%{pkg_name}-%{version}.jar
%if %stress
%mvn_artifact org.apache.%{pkg_name}:%{pkg_name}-stress:%{version} build/tools/lib/%{pkg_name}-stress.jar
%endif

%mvn_install -J build/javadoc/

# Install the cqlshlib Python module
pushd pylib
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --prefix %{?_prefix}
popd
%{?scl:EOF}

# create data and log dirs
mkdir -p %{buildroot}%{_sharedstatedir}/%{pkg_name}/data
mkdir -p %{buildroot}%{_localstatedir}/log/%{pkg_name}

# install files
install -p -D -m 644 "%{SOURCE1}"  %{buildroot}%{_sysconfdir}/logrotate.d/%{pkg_name}
install -p -D -m 755 bin/%{pkg_name} %{buildroot}%{_bindir}/%{pkg_name}
install -p -D -m 755 bin/%{pkg_name}.in.sh %{buildroot}%{_datadir}/%{pkg_name}/%{pkg_name}.in.sh
install -p -D -m 755 conf/%{pkg_name}-env.sh %{buildroot}%{_datadir}/%{pkg_name}/%{pkg_name}-env.sh
install -p -D -m 644 conf/%{pkg_name}.yaml %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}.yaml
install -p -D -m 644 conf/%{pkg_name}-jaas.config %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}-jaas.config
install -p -D -m 644 conf/%{pkg_name}-topology.properties %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}-topology.properties
install -p -D -m 644 conf/%{pkg_name}-rackdc.properties %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}-rackdc.properties
install -p -D -m 644 conf/jvm.options %{buildroot}%{_sysconfdir}/%{pkg_name}/jvm.options
install -p -D -m 644 conf/logback-tools.xml %{buildroot}%{_sysconfdir}/%{pkg_name}/logback-tools.xml
install -p -D -m 644 conf/logback.xml %{buildroot}%{_sysconfdir}/%{pkg_name}/logback.xml
install -p -D -m 644 conf/metrics-reporter-config-sample.yaml %{buildroot}%{_sysconfdir}/%{pkg_name}/metrics-reporter-config-sample.yaml
install -p -D -m 440 conf/cqlshrc.sample %{buildroot}%{_sysconfdir}/%{pkg_name}/cqlshrc
install -p -D -m 644 conf/hotspot_compiler %{buildroot}%{_sysconfdir}/%{pkg_name}/hotspot_compiler
install -p -D -m 755 bin/cqlsh.py %{buildroot}%{_bindir}/cqlsh
install -p -D -m 755 bin/nodetool %{buildroot}%{_bindir}/nodetool
install -p -D -m 755 bin/sstableloader %{buildroot}%{_bindir}/sstableloader
install -p -D -m 755 bin/sstablescrub %{buildroot}%{_bindir}/sstablescrub
install -p -D -m 755 bin/sstableupgrade %{buildroot}%{_bindir}/sstableupgrade
install -p -D -m 755 bin/sstableutil %{buildroot}%{_bindir}/sstableutil
install -p -D -m 755 bin/sstableverify %{buildroot}%{_bindir}/sstableverify
install -p -D -m 755 tools/bin/sstabledump %{buildroot}%{_bindir}/sstabledump
install -p -D -m 755 tools/bin/sstableexpiredblockers %{buildroot}%{_bindir}/sstableexpiredblockers
install -p -D -m 755 tools/bin/sstablelevelreset %{buildroot}%{_bindir}/sstablelevelreset
install -p -D -m 755 tools/bin/sstablemetadata %{buildroot}%{_bindir}/sstablemetadata
install -p -D -m 755 tools/bin/sstableofflinerelevel %{buildroot}%{_bindir}/sstableofflinerelevel
install -p -D -m 755 tools/bin/sstablerepairedset %{buildroot}%{_bindir}/sstablerepairedset
install -p -D -m 755 tools/bin/sstablesplit %{buildroot}%{_bindir}/sstablesplit
%if %stress
install -p -D -m 755 tools/bin/%{pkg_name}-stress %{buildroot}%{_bindir}/%{pkg_name}-stress
install -p -D -m 755 tools/bin/%{pkg_name}-stressd %{buildroot}%{_bindir}/%{pkg_name}-stressd
%endif

# install cassandra.service
install -p -D -m 644 "%{SOURCE2}"  %{buildroot}%{_unitdir}/%{daemon_name}.service

%pre server
getent group %{pkg_name} >/dev/null || groupadd -f -g %{gid_uid} -r %{pkg_name}
if ! getent passwd %{pkg_name} >/dev/null ; then
  if ! getent passwd %{gid_uid} >/dev/null ; then
    useradd -r -u %{gid_uid} -g %{pkg_name} -d %{_root_localstatedir}/lib/%{pkg_name}/data \
      -s /sbin/nologin -c "Cassandra Database Server" %{pkg_name}
  else
    useradd -r -g %{pkg_name} -d %{_root_localstatedir}/lib/%{pkg_name}/data -s /sbin/nologin \
      -c "Cassandra Database Server" %{pkg_name}
  fi
fi
exit 0

%post server
%systemd_post %{daemon_name}.service

%preun server
%systemd_preun %{daemon_name}.service

%postun server
%systemd_postun_with_restart %{daemon_name}.service

%files
%doc README.asc CHANGES.txt NEWS.txt
%license LICENSE.txt NOTICE.txt
%attr(755, root, root) %{_bindir}/nodetool
%attr(755, root, root) %{_bindir}/sstableloader
%attr(755, root, root) %{_bindir}/sstablescrub
%attr(755, root, root) %{_bindir}/sstableupgrade
%attr(755, root, root) %{_bindir}/sstableutil
%attr(755, root, root) %{_bindir}/sstableverify
%attr(755, root, root) %{_bindir}/sstabledump
%attr(755, root, root) %{_bindir}/sstableexpiredblockers
%attr(755, root, root) %{_bindir}/sstablelevelreset
%attr(755, root, root) %{_bindir}/sstablemetadata
%attr(755, root, root) %{_bindir}/sstableofflinerelevel
%attr(755, root, root) %{_bindir}/sstablerepairedset
%attr(755, root, root) %{_bindir}/sstablesplit
%attr(755, root, root) %{_bindir}/cqlsh
%config(noreplace) %attr(440, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/cqlshrc

%files java-libs -f .mfiles
%license LICENSE.txt NOTICE.txt

%files server
%doc README.asc CHANGES.txt NEWS.txt
%license LICENSE.txt NOTICE.txt
%dir %attr(700, %{pkg_name}, %{pkg_name}) %{_sharedstatedir}/%{pkg_name}
%dir %attr(700, %{pkg_name}, %{pkg_name}) %{_sharedstatedir}/%{pkg_name}/data
%dir %attr(700, %{pkg_name}, %{pkg_name}) %{_localstatedir}/log/%{pkg_name}
%{_bindir}/%{pkg_name}
%{_datadir}/%{pkg_name}/%{pkg_name}.in.sh
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_datadir}/%{pkg_name}/%{pkg_name}-env.sh
%dir %attr(700, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/%{pkg_name}.yaml
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/%{pkg_name}-jaas.config
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/%{pkg_name}-topology.properties
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/%{pkg_name}-rackdc.properties
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/jvm.options
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/logback-tools.xml
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/logback.xml
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/metrics-reporter-config-sample.yaml
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/logrotate.d/%{pkg_name}
%config(noreplace) %attr(644, %{pkg_name}, %{pkg_name}) %{_sysconfdir}/%{pkg_name}/hotspot_compiler
%{_unitdir}/%{daemon_name}.service

%files parent -f .mfiles-parent
%license LICENSE.txt NOTICE.txt

%files python2-cqlshlib
%license LICENSE.txt NOTICE.txt
%{python2_sitearch}/cqlshlib
%{python2_sitearch}/%{pkg_name}_pylib-0.0.0-py%{python2_version}.egg-info

%if %stress
%files stress -f .mfiles-stress
%license LICENSE.txt NOTICE.txt
%attr(755, root, root) %{_bindir}/%{pkg_name}-stress
%attr(755, root, root) %{_bindir}/%{pkg_name}-stressd
%{_datadir}/%{pkg_name}/%{pkg_name}.in.sh
%endif

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%changelog
* Wed May 02 2018 Augusto Caringi <acaringi@redhat.com> - 3.11.1-4
- add cassandra-rackdc.properties conf file to ease multi-node configuration

* Wed Feb 07 2018 Jakub Janco <jjanco@redhat.com> - 3.11.1-3
- use guava v24 in f28, Remove dependencies on internal JMX classes

* Tue Feb 06 2018 Augusto Caringi <acaringi@redhat.com> - 3.11.1-2
- fix antlr dependency (remove antlr as a runtime dependency)

* Tue Jan 09 2018 Jakub Janco <jjanco@redhat.com> - 3.11.1-1
- new version

* Mon Dec 11 2017 Augusto Caringi <acaringi@redhat.com> - 3.11.0-6
- fix nodetool classpath dependency, added netty/netty-all

* Thu Nov 09 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.11.0-1
- Update to 3.11.0

* Fri Nov 03 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.9-16
- fixed homedir path
- fixed %{_sharedstatedir}/%{pkg_name} ownership/permissions

* Wed Nov 01 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.9-15
- fixed problem related to listen_address and wait_for_service script
  function (#1507524)
- remove wrong paths not included in SCL paths (#1507862)

* Thu Oct 05 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.9-14
- fixed centos specific patch

* Thu Oct 05 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.9-13
- fixed atinject dependency

* Tue Aug 22 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.9-12
- fixed runtime dependencies (requires)
- fixed service (systemd) related stuff
- apply centos specific patch

* Mon Aug 21 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.9-11
- rebuilt

* Mon Aug 21 2017 Augusto Mecking Caringi <acaringi@redhat.com> - 3.9-10
- rebuilt

* Mon Apr 10 2017 Tomas Repik <trepik@redhat.com> - 3.9-9
- scl conversion

* Mon Apr 03 2017 Tomas Repik <trepik@redhat.com> - 3.9-8
- add SchemaConstants.java and fix cassandra startup

* Tue Mar 28 2017 Tomas Repik <trepik@redhat.com> - 3.9-7
- remove thrift from 3.9 applying mainly upstream patch

* Mon Mar 20 2017 Tomas Repik <trepik@redhat.com> - 3.9-6
- require airline and change permissions for config files

* Mon Feb 20 2017 Tomas Repik <trepik@redhat.com> - 3.9-5
- require nmap-ncat for fedora and nc for scl server subpackage (rhbz#1424717)

* Tue Feb 07 2017 Tomas Repik <trepik@redhat.com> - 3.9-4
- service renamed
- nodetool include file added
- runtime dependencies for server added
- init script waits until the server is ready to accept connections

* Tue Jan 31 2017 Tomas Repik <trepik@redhat.com> - 3.9-3
- reworked the subpackage structure

* Wed Jan 18 2017 Tomas Repik <trepik@redhat.com> - 3.9-2
- fix paths so that one could run the server

* Thu Dec 01 2016 Tomas Repik <trepik@redhat.com> - 3.9-1
- initial package
