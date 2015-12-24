#
# Conditional build:
%bcond_without	ocaml		# OCaml plugin (requires ocaml_opt support)
%bcond_without	perl		# Perl plugin
%bcond_without	python		# Python plugin
%bcond_with	vddk		# VMware VDDK plugin [needs proprietary VDDK]
#
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
# no ocaml_opt support
%undefine	with_ocaml
%endif
Summary:	Toolkit for creating NBD servers
Summary(pl.UTF-8):	Narzędzia do tworzenia serwerów NBD
Name:		nbdkit
Version:	1.1.11
Release:	2
License:	BSD
Group:		Applications/System
Source0:	http://libguestfs.org/download/nbdkit/%{name}-%{version}.tar.gz
# Source0-md5:	c03d66a7ad5f7f08a171d6845dc28c48
URL:		http://libguestfs.org/
BuildRequires:	curl-devel
BuildRequires:	libguestfs-devel
BuildRequires:	libvirt-devel
%{?with_ocaml:BuildRequires:	ocaml >= 4.02.2}
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel >= 2}
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# depends on symbols from nbdkit binary and ocaml ABI
%define		skip_post_check_so	libnbdkitocaml.so.*

%description
NBD is a protocol for accessing Block Devices (hard disks and
disk-like things) over a Network.

'nbdkit' is a toolkit for creating NBD servers.

%description -l pl.UTF-8
NBD (Network Block Device) to protokół sieciowego dostępu do urządzeń
blokowych (dysków twardych i podobnego osprzętu).

nbdkit to zestaw narzędzi do tworzenia serwerów NBD.

%package plugin-curl
Summary:	curl plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka curl dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-curl
curl plugin for nbdkit.

%description plugin-curl -l pl.UTF-8
Wtyczka curl dla nbdkitu.

%package plugin-guestfs
Summary:	guestfs plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka guestfs dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-guestfs
guestfs plugin for nbdkit.

%description plugin-guestfs -l pl.UTF-8
Wtyczka guestfs dla nbdkitu.

%package plugin-libvirt
Summary:	libvirt plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka libvirt dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-libvirt
libvirt plugin for nbdkit.

%description plugin-libvirt -l pl.UTF-8
Wtyczka libvirt dla nbdkitu.

%package plugin-ocaml
Summary:	OCaml embed plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka wbudowanego OCamla dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-runtime

%description plugin-ocaml
OCaml embed plugin for nbdkit.

%description plugin-ocaml -l pl.UTF-8
Wtyczka wbudowanego OCamla dla nbdkitu.

%package plugin-perl
Summary:	Perl embed plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka wbudowanego Perla dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-perl
Perl embed plugin for nbdkit.

%description plugin-perl -l pl.UTF-8
Wtyczka wbudowanego Perla dla nbdkitu.

%package plugin-python
Summary:	Python embed plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka wbudowanego Pythona dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-python
Python embed plugin for nbdkit.

%description plugin-python -l pl.UTF-8
Wtyczka wbudowanego Pythona dla nbdkitu.

%package plugin-vddk
Summary:	VMware VDDK plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka VMware VDDK dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-vddk
VMware VDDK plugin for nbdkit.

%description plugin-vddk -l pl.UTF-8
Wtyczka VMware VDDK dla nbdkitu.

%package devel
Summary:	Header file for nbdkit plugins
Summary(pl.UTF-8):	Plik nagłówkowy dla wtyczek nbdkit
Group:		Development/Libraries
# doesn't require base

%description devel
Header file for nbdkit plugins.

%description devel -l pl.UTF-8
Plik nagłówkowy dla wtyczek nbdkit.

%prep
%setup -q

%build
%configure \
	GUESTFISH=no \
	%{!?with_ocaml:--disable-ocaml} \
	%{!?with_perl:--disable-perl} \
	%{!?with_python:--disable-python} \
	--disable-static \
	%{?with_vddk:--with-vddk}

%{__make} \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/nbdkit/plugins/*.la
%if %{with ocaml}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnbdkitocaml.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	plugin-ocaml -p /sbin/ldconfig
%postun	plugin-ocaml -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README TODO
%attr(755,root,root) %{_sbindir}/nbdkit
%dir %{_libdir}/nbdkit
%dir %{_libdir}/nbdkit/plugins
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-example1-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-example2-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-example3-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-file-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-gzip-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-streaming-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-xz-plugin.so
%{_mandir}/man1/nbdkit.1*
%{_mandir}/man1/nbdkit-example1-plugin.1*
%{_mandir}/man1/nbdkit-example2-plugin.1*
%{_mandir}/man1/nbdkit-example3-plugin.1*
%{_mandir}/man1/nbdkit-file-plugin.1*
%{_mandir}/man1/nbdkit-gzip-plugin.1*
%{_mandir}/man1/nbdkit-streaming-plugin.1*
%{_mandir}/man1/nbdkit-xz-plugin.1*

%files plugin-curl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-curl-plugin.so
%{_mandir}/man1/nbdkit-curl-plugin.1*

%files plugin-guestfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-guestfs-plugin.so
%{_mandir}/man1/nbdkit-guestfs-plugin.1*

%files plugin-libvirt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-libvirt-plugin.so
%{_mandir}/man1/nbdkit-libvirt-plugin.1*

%if %{with ocaml}
%files plugin-ocaml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnbdkitocaml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnbdkitocaml.so.0
%attr(755,root,root) %{_libdir}/libnbdkitocaml.so
%{_libdir}/ocaml/NBDKit.cm[ix]
%{_libdir}/ocaml/NBDKit.mli
%{_libdir}/ocaml/NBDKit.o
%{_mandir}/man3/nbdkit-ocaml-plugin.3*
%endif

%if %{with perl}
%files plugin-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-perl-plugin.so
%{_mandir}/man3/nbdkit-perl-plugin.3*
%endif

%if %{with python}
%files plugin-python
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-python-plugin.so
%{_mandir}/man3/nbdkit-python-plugin.3*
%endif

%if %{with vddk}
%files plugin-vddk
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-vddk-plugin.so
%{_mandir}/man1/nbdkit-vddk-plugin.1*
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/nbdkit-plugin.h
%{_mandir}/man3/nbdkit-plugin.3*
