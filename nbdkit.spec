# TODO:
# --enable-valgrind (valgrind extensions)?
#
# Conditional build:
%bcond_with	golang		# Go language plugin
%bcond_without	lua		# Lua language plugin
%bcond_without	ocaml		# OCaml language plugin (requires ocaml_opt support)
%bcond_without	perl		# Perl language plugin
%bcond_without	python		# Python language plugin
%bcond_without	ruby		# Ruby language plugin
%bcond_with	rust		# Rust language plugin
%bcond_without	tcl		# Tcl language plugin
%bcond_without	libblkio	# libblkio plugin (rust)
%bcond_without	vddk		# VMware VDDK plugin (x86_64 only)
#
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml
%undefine	with_golang
%endif
%ifnarch %{x8664} %{ix86} x32 aarch64 armv6hl armv7hl armv7hnl
%undefine	with_libblkio
%endif
%ifnarch %{x8664}
%undefine	with_vddk
%endif

Summary:	Toolkit for creating NBD servers
Summary(pl.UTF-8):	Narzędzia do tworzenia serwerów NBD
Name:		nbdkit
Version:	1.38.2
Release:	1
License:	BSD
Group:		Applications/System
Source0:	https://download.libguestfs.org/nbdkit/1.38-stable/%{name}-%{version}.tar.gz
# Source0-md5:	a33a75a0cc358c48ee8e478a8acf2abb
URL:		https://libguestfs.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bash-completion-devel >= 1:2.0
%{?with_rust:BuildRequires:	cargo}
BuildRequires:	curl-devel >= 8.3.1
# for mke2fs options detection (incl. -d option support)
BuildRequires:	e2fsprogs >= 1.43
BuildRequires:	e2fsprogs-devel
BuildRequires:	gnutls-devel >= 3.3.0
%{?with_golang:BuildRequires:	golang-devel}
%{?with_libblkio:BuildRequires:	libblkio-devel}
BuildRequires:	libcom_err-devel
BuildRequires:	libguestfs-devel
BuildRequires:	libnbd-devel >= 0.9.8
BuildRequires:	libselinux-devel >= 2.0.90
BuildRequires:	libssh-devel >= 0.8.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libtorrent-rasterbar-devel
BuildRequires:	libvirt-devel
%{?with_lua:BuildRequires:	lua-devel >= 5.1}
%{?with_ocaml:BuildRequires:	ocaml >= 4.02.2}
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-build >= 4.6
%{?with_ruby:BuildRequires:	ruby-devel >= 1:2.6}
BuildRequires:	sed >= 4.0
%{?with_tcl:BuildRequires:	tcl-devel >= 8.6}
BuildRequires:	xz-devel
BuildRequires:	zlib-devel >= 1.2.3.5
BuildRequires:	zstd-devel
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

%package -n bash-completion-nbdkit
Summary:	Bash completion for nbdkit commands
Summary(pl.UTF-8):	Bashowe uzupełnianie składni poleceń nbdkit
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-nbdkit
Bash completion for nbdkit commands.

%description -n bash-completion-nbdkit -l pl.UTF-8
Bashowe uzupełnianie składni poleceń nbdkit.

%package plugin-curl
Summary:	curl plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka curl dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-libs >= 8.3.1

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

%package plugin-go
Summary:	Go embed plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka wbudowanego Go dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-go
Go embed plugin for nbdkit.

%description plugin-go -l pl.UTF-8
Wtyczka wbudowanego Go dla nbdkitu.

%package plugin-lua
Summary:	Lua embed plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka wbudowanego Lua dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-lua
Lua embed plugin for nbdkit.

%description plugin-lua -l pl.UTF-8
Wtyczka wbudowanego Lua dla nbdkitu.

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

%package plugin-ruby
Summary:	Ruby embed plugin for nbdkit
Summary(pl.UTF-8):	Wtyczka wbudowanego Ruby dla nbdkitu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-ruby
Ruby embed plugin for nbdkit.

%description plugin-ruby -l pl.UTF-8
Wtyczka wbudowanego Ruby dla nbdkitu.

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

%{__sed} -i -e '/PKG_CHECK_MODULES(\[RUBY/ s/ruby/ruby-2.6/' configure.ac

# use full path, don't require /sbin in $PATH
%{__sed} -i -e 's,mke2fs -,/sbin/mke2fs -,' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	GENISOIMAGE=/usr/bin/genisoimage \
	GUESTFISH=no \
	MKISOFS=/usr/bin/mkisofs \
	%{!?with_golang:--disable-golang} \
	%{!?with_lua:--disable-lua} \
	%{!?with_ocaml:--disable-ocaml} \
	%{!?with_perl:--disable-perl} \
	%{!?with_python:--disable-python} \
	%{!?with_ruby:--disable-ruby} \
	%{!?with_rust:--disable-rust} \
	--disable-static \
	%{!?with_tcl:--disable-tcl} \
	%{!?with_libblkio:--without-libblkio} \
	%{!?with_vddk:--without-vddk}

%{__make} \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/nbdkit/filters/*.la
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
%doc LICENSE OTHER_PLUGINS README.md SECURITY TODO
%attr(755,root,root) %{_sbindir}/nbdkit
%dir %{_libdir}/nbdkit
%dir %{_libdir}/nbdkit/filters
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-blocksize-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-blocksize-policy-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-cache-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-cacheextents-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-checkwrite-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-cow-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-ddrescue-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-delay-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-error-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-evil-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-exitlast-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-exitwhen-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-exportname-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-ext2-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-extentlist-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-fua-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-gzip-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-ip-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-limit-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-log-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-luks-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-multi-conn-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-nocache-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-noextents-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-nofilter-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-noparallel-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-nozero-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-offset-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-partition-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-pause-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-protect-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-qcow2dec-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-rate-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-readahead-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-readonly-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-retry-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-retry-request-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-scan-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-stats-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-swab-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-tar-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-tls-fallback-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-truncate-filter.so
%attr(755,root,root) %{_libdir}/nbdkit/filters/nbdkit-xz-filter.so
%dir %{_libdir}/nbdkit/plugins
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-S3-plugin
%if %{with libblkio}
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-blkio-plugin.so
%endif
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-cc-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-cdi-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-data-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-eval-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-example1-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-example2-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-example3-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-example4-plugin
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-file-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-floppy-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-full-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-gcs-plugin
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-info-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-iso-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-linuxdisk-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-memory-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-nbd-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-null-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-ondemand-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-ones-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-partitioning-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-pattern-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-random-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-sh-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-sparse-random-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-split-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-ssh-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-tcl-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-tmpdisk-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-torrent-plugin.so
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-zero-plugin.so
%{_mandir}/man1/nbdkit.1*
%{_mandir}/man1/nbdkit-S3-plugin.1*
%if %{with libblkio}
%{_mandir}/man1/nbdkit-blkio-plugin.1*
%endif
%{_mandir}/man1/nbdkit-blocksize-filter.1*
%{_mandir}/man1/nbdkit-blocksize-policy-filter.1*
%{_mandir}/man1/nbdkit-cache-filter.1*
%{_mandir}/man1/nbdkit-cacheextents-filter.1*
%{_mandir}/man1/nbdkit-captive.1*
%{_mandir}/man1/nbdkit-cdi-plugin.1*
%{_mandir}/man1/nbdkit-checkwrite-filter.1*
%{_mandir}/man1/nbdkit-client.1*
%{_mandir}/man1/nbdkit-cow-filter.1*
%{_mandir}/man1/nbdkit-data-plugin.1*
%{_mandir}/man1/nbdkit-ddrescue-filter.1*
%{_mandir}/man1/nbdkit-delay-filter.1*
%{_mandir}/man1/nbdkit-error-filter.1*
%{_mandir}/man1/nbdkit-eval-plugin.1*
%{_mandir}/man1/nbdkit-evil-filter.1*
%{_mandir}/man1/nbdkit-example1-plugin.1*
%{_mandir}/man1/nbdkit-example2-plugin.1*
%{_mandir}/man1/nbdkit-example3-plugin.1*
%{_mandir}/man1/nbdkit-example4-plugin.1*
%{_mandir}/man1/nbdkit-exitlast-filter.1*
%{_mandir}/man1/nbdkit-exitwhen-filter.1*
%{_mandir}/man1/nbdkit-exportname-filter.1*
%{_mandir}/man1/nbdkit-ext2-filter.1*
%{_mandir}/man1/nbdkit-extentlist-filter.1*
%{_mandir}/man1/nbdkit-file-plugin.1*
%{_mandir}/man1/nbdkit-floppy-plugin.1*
%{_mandir}/man1/nbdkit-fua-filter.1*
%{_mandir}/man1/nbdkit-full-plugin.1*
%{_mandir}/man1/nbdkit-gcs-plugin.1*
%{_mandir}/man1/nbdkit-gzip-filter.1*
%{_mandir}/man1/nbdkit-info-plugin.1*
%{_mandir}/man1/nbdkit-ip-filter.1*
%{_mandir}/man1/nbdkit-iso-plugin.1*
%{_mandir}/man1/nbdkit-limit-filter.1*
%{_mandir}/man1/nbdkit-linuxdisk-plugin.1*
%{_mandir}/man1/nbdkit-log-filter.1*
%{_mandir}/man1/nbdkit-loop.1*
%{_mandir}/man1/nbdkit-luks-filter.1*
%{_mandir}/man1/nbdkit-memory-plugin.1*
%{_mandir}/man1/nbdkit-multi-conn-filter.1*
%{_mandir}/man1/nbdkit-nbd-plugin.1*
%{_mandir}/man1/nbdkit-nocache-filter.1*
%{_mandir}/man1/nbdkit-noextents-filter.1*
%{_mandir}/man1/nbdkit-nofilter-filter.1*
%{_mandir}/man1/nbdkit-noparallel-filter.1*
%{_mandir}/man1/nbdkit-nozero-filter.1*
%{_mandir}/man1/nbdkit-null-plugin.1*
%{_mandir}/man1/nbdkit-offset-filter.1*
%{_mandir}/man1/nbdkit-ondemand-plugin.1*
%{_mandir}/man1/nbdkit-ones-plugin.1*
%{_mandir}/man1/nbdkit-partition-filter.1*
%{_mandir}/man1/nbdkit-partitioning-plugin.1*
%{_mandir}/man1/nbdkit-pattern-plugin.1*
%{_mandir}/man1/nbdkit-pause-filter.1*
%{_mandir}/man1/nbdkit-probing.1*
%{_mandir}/man1/nbdkit-protect-filter.1*
%{_mandir}/man1/nbdkit-protocol.1*
%{_mandir}/man1/nbdkit-qcow2dec-filter.1*
%{_mandir}/man1/nbdkit-random-plugin.1*
%{_mandir}/man1/nbdkit-rate-filter.1*
%{_mandir}/man1/nbdkit-readahead-filter.1*
%{_mandir}/man1/nbdkit-readonly-filter.1*
%{_mandir}/man1/nbdkit-release-notes-1.4.1*
%{_mandir}/man1/nbdkit-release-notes-1.6.1*
%{_mandir}/man1/nbdkit-release-notes-1.8.1*
%{_mandir}/man1/nbdkit-release-notes-1.10.1*
%{_mandir}/man1/nbdkit-release-notes-1.12.1*
%{_mandir}/man1/nbdkit-release-notes-1.14.1*
%{_mandir}/man1/nbdkit-release-notes-1.16.1*
%{_mandir}/man1/nbdkit-release-notes-1.18.1*
%{_mandir}/man1/nbdkit-release-notes-1.20.1*
%{_mandir}/man1/nbdkit-release-notes-1.22.1*
%{_mandir}/man1/nbdkit-release-notes-1.24.1*
%{_mandir}/man1/nbdkit-release-notes-1.26.1*
%{_mandir}/man1/nbdkit-release-notes-1.28.1*
%{_mandir}/man1/nbdkit-release-notes-1.30.1*
%{_mandir}/man1/nbdkit-release-notes-1.32.1*
%{_mandir}/man1/nbdkit-release-notes-1.34.1*
%{_mandir}/man1/nbdkit-release-notes-1.36.1*
%{_mandir}/man1/nbdkit-release-notes-1.38.1*
%{_mandir}/man1/nbdkit-retry-filter.1*
%{_mandir}/man1/nbdkit-retry-request-filter.1*
%{_mandir}/man1/nbdkit-scan-filter.1*
%{_mandir}/man1/nbdkit-security.1*
%{_mandir}/man1/nbdkit-service.1*
%{_mandir}/man1/nbdkit-sparse-random-plugin.1*
%{_mandir}/man1/nbdkit-split-plugin.1*
%{_mandir}/man1/nbdkit-ssh-plugin.1*
%{_mandir}/man1/nbdkit-stats-filter.1*
%{_mandir}/man1/nbdkit-swab-filter.1*
%{_mandir}/man1/nbdkit-tar-filter.1*
%{_mandir}/man1/nbdkit-tls.1*
%{_mandir}/man1/nbdkit-tls-fallback-filter.1*
%{_mandir}/man1/nbdkit-tmpdisk-plugin.1*
%{_mandir}/man1/nbdkit-torrent-plugin.1*
%{_mandir}/man1/nbdkit-truncate-filter.1*
%{_mandir}/man1/nbdkit-xz-filter.1*
%{_mandir}/man1/nbdkit-zero-plugin.1*
%if %{with rust}
%{_mandir}/man3/nbdkit-rust-plugin.3*
%endif
%{_mandir}/man3/nbdkit-sh-plugin.3*
%{_mandir}/man3/nbdkit-tcl-plugin.3*

%files -n bash-completion-nbdkit
%defattr(644,root,root,755)
%{bash_compdir}/nbdkit

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

%if %{with golang}
%files plugin-go
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-golang-plugin.so
%{_mandir}/man3/nbdkit-golang-plugin.3*
%endif

%if %{with lua}
%files plugin-lua
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-lua-plugin.so
%{_mandir}/man3/nbdkit-lua-plugin.3*
%endif

%if %{with ocaml}
%files plugin-ocaml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnbdkitocaml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnbdkitocaml.so.0
%attr(755,root,root) %{_libdir}/libnbdkitocaml.so
%{_libdir}/ocaml/NBDKit.cm[ix]
%{_libdir}/ocaml/NBDKit.mli
%{_libdir}/ocaml/NBDKit.o
%{_mandir}/man3/NBDKit.3*
%{_mandir}/man3/nbdkit-ocaml-plugin.3*
%endif

%if %{with perl}
%files plugin-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-perl-plugin.so
%{_mandir}/man3/nbdkit-perl-plugin.3*
%endif

%if %{with ruby}
%files plugin-ruby
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nbdkit/plugins/nbdkit-ruby-plugin.so
%{_mandir}/man3/nbdkit-ruby-plugin.3*
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
%{_includedir}/nbd-protocol.h
%{_includedir}/nbdkit-common.h
%{_includedir}/nbdkit-filter.h
%{_includedir}/nbdkit-plugin.h
%{_includedir}/nbdkit-version.h
%{_pkgconfigdir}/nbdkit.pc
%{_mandir}/man3/nbdkit-cc-plugin.3*
%{_mandir}/man3/nbdkit-filter.3*
%{_mandir}/man3/nbdkit-plugin.3*
