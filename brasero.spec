#
# Conditional build:
%bcond_without	nautilus	# Nautilus extension

Summary:	Disc burning application for GNOME
Summary(pl.UTF-8):	Program do wypalania płyt dla GNOME
Name:		brasero
Version:	3.12.1
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/brasero/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	216691249053448a9f2b4ee5e118ce72
URL:		https://wiki.gnome.org/Apps/Brasero
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.30.0
BuildRequires:	glibc-misc
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	gstreamer-devel >= 1.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	intltool >= 0.50
BuildRequires:	libburn-devel >= 0.4.0
BuildRequires:	libcanberra-devel
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libisofs-devel >= 0.6.4
BuildRequires:	libnotify-devel >= 0.6.1
BuildRequires:	libtool >= 2.2
BuildRequires:	libxml2-devel >= 1:2.6.31
%{?with_nautilus:BuildRequires:	nautilus-devel >= 3.0.0}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	tar >= 1:1.22
BuildRequires:	totem-pl-parser-devel >= 2.30.0
BuildRequires:	tracker-devel >= 0.16.0
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	shared-mime-info
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hicolor-icon-theme
Suggests:	cdda2wav
Suggests:	cdrdao
Suggests:	cdrecord
Suggests:	cdrtools-readcd
Suggests:	dvd+rw-tools
Suggests:	dvdauthor
Suggests:	gstreamer-audio-effects-base
Suggests:	gstreamer-audio-effects-good
Suggests:	mkisofs
Suggests:	vcdimager
Obsoletes:	bonfire
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Brasero is a CD/DVD mastering tool for the GNOME desktop. It is
designed to be simple and easy to use.

%description -l pl.UTF-8
Brasero jest narzędziem do masteringu płyt CD/DVD dla biurka GNOME.
Jest zaprojektowany by być prostym i łatwym w obsłudze.

%package libs
Summary:	Brasero library
Summary(pl.UTF-8):	Biblioteka Brasero
Group:		X11/Libraries

%description libs
Brasero library.

%description libs -l pl.UTF-8
Biblioteka Brasero.

%package devel
Summary:	Header files for Brasero library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Brasero
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.30.0
Requires:	gtk+3-devel >= 3.0.0

%description devel
Header files for Brasero library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Brasero.

%package apidocs
Summary:	Brasero library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Brasero
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
Brasero library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Brasero.

%package -n nautilus-extension-brasero
Summary:	Brasero extension for Nautilus
Summary(pl.UTF-8):	Rozszerzenie Brasero dla Nautilusa
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus >= 3.0.0

%description -n nautilus-extension-brasero
Adds Brasero integration to Nautilus.

%description -n nautilus-extension-brasero -l pl.UTF-8
Dodaje integrację Brasero z Nautilusem.

%prep
%setup -q

%build
%{__gtkdocize}
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-caches \
	--enable-gtk-doc \
	%{!?with_nautilus:--disable-nautilus} \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/brasero3/plugins/lib*.la
%if %{with nautilus}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la
%endif

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_desktop_database_postun
%glib_compile_schemas
%update_mime_database
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post -n nautilus-extension-brasero
%update_desktop_database_post

%postun -n nautilus-extension-brasero
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/brasero
%{_datadir}/appdata/brasero.appdata.xml
%{_datadir}/%{name}
%{_datadir}/mime/packages/%{name}.xml
%dir %{_libdir}/brasero3
%dir %{_libdir}/brasero3/plugins
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-audio2cue.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-burn-uri.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-cdda2wav.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-cdrdao.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-cdrecord.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-checksum-file.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-checksum.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-dvdauthor.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-dvdcss.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-dvdrwformat.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-genisoimage.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-growisofs.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-libburn.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-libisofs.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-local-track.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-mkisofs.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-normalize.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-readcd.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-readom.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-transcode.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-vcdimager.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-vob.so
%attr(755,root,root) %{_libdir}/brasero3/plugins/libbrasero-wodim.so
%{_datadir}/GConf/gsettings/brasero.convert
%{_datadir}/glib-2.0/schemas/org.gnome.brasero.gschema.xml
%{_desktopdir}/brasero.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/scalable/apps/*.svg
%{_mandir}/man1/brasero.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbrasero-burn3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbrasero-burn3.so.1
%attr(755,root,root) %{_libdir}/libbrasero-media3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbrasero-media3.so.1
%attr(755,root,root) %{_libdir}/libbrasero-utils3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbrasero-utils3.so.1
%{_libdir}/girepository-1.0/BraseroBurn-*.typelib
%{_libdir}/girepository-1.0/BraseroMedia-*.typelib


%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbrasero-burn3.so
%attr(755,root,root) %{_libdir}/libbrasero-media3.so
%attr(755,root,root) %{_libdir}/libbrasero-utils3.so
%{_includedir}/brasero3
%{_pkgconfigdir}/libbrasero-burn3.pc
%{_pkgconfigdir}/libbrasero-media3.pc
%{_datadir}/gir-1.0/BraseroBurn-*.gir
%{_datadir}/gir-1.0/BraseroMedia-*.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbrasero-burn
%{_gtkdocdir}/libbrasero-media

%if %{with nautilus}
%files -n nautilus-extension-brasero
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/libnautilus-brasero-extension.so
%{_desktopdir}/brasero-nautilus.desktop
%endif
