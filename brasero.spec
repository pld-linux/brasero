#
# Conditinal build:
%bcond_without	beagle		# disable beagle search
#
Summary:	Disc burning application for GNOME
Summary(pl.UTF-8):	Program do wypalania płyt dla GNOME
Name:		brasero
Version:	2.27.92
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/brasero/2.27/%{name}-%{version}.tar.bz2
# Source0-md5:	32461934eeb0ed74a3f7ea033104e998
URL:		http://www.gnome.org/projects/brasero/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.20.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-doc-utils
BuildRequires:	gstreamer-devel >= 0.10.15
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:	gtk+2-devel >= 2:2.16.0
Buildrequires:	gtk-doc >= 1.9
BuildRequires:	hal-devel >= 0.5.10
BuildRequires:	intltool >= 0.40.0
%{?with_beagle:BuildRequires:	libbeagle-devel >= 0.3.0}
BuildRequires:	libburn-devel >= 0.4.0
BuildRequires:	libisofs-devel >= 0.6.4
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	nautilus-devel >= 2.26.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	totem-pl-parser-devel >= 2.26.0
BuildRequires:	xorg-lib-libSM-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires(post,preun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hal >= 0.5.10
Suggests:	dvd+rw-tools
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
Requires:	gtk+2-devel >= 2:2.16.0
Requires:	hal-devel >= 0.5.10

%description devel
Header files for Brasero library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Brasero.

%package static
Summary:	Static Brasero library
Summary(pl.UTF-8):	Statyczna biblioteka Brasero
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Brasero library.

%description static -l pl.UTF-8
Statyczna biblioteka Brasero.

%package apidocs
Summary:	Brasero library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Brasero
Group:		Documentation
Requires:	gtk-doc-common

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
Requires:	nautilus >= 2.26.0

%description -n nautilus-extension-brasero
Adds Brasero integration to Nautilus.

%description -n nautilus-extension-brasero -l pl.UTF-8
Dodaje integrację Brasero z Nautilusem.

%prep
%setup -q
rm po/ca@valencia.po
sed -i s#^ca@valencia## po/LINGUAS

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_beagle:--disable-search} \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--disable-caches \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/brasero/plugins/lib*.{la,a}
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/*.{la,a}

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install brasero.schemas
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall brasero.schemas

%postun
%update_desktop_database_postun
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
%{_datadir}/%{name}
%{_datadir}/mime/packages/%{name}.xml
%dir %{_libdir}/brasero
%dir %{_libdir}/brasero/plugins
%attr(755,root,root) %{_libdir}/brasero/plugins/lib*.so
%{_desktopdir}/brasero-copy-medium.desktop
%{_desktopdir}/brasero.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_mandir}/man1/brasero.1*
%{_sysconfdir}/gconf/schemas/brasero.schemas

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbrasero-burn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbrasero-burn.so.0
%attr(755,root,root) %{_libdir}/libbrasero-media.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbrasero-media.so.0
%attr(755,root,root) %{_libdir}/libbrasero-utils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbrasero-utils.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbrasero-burn.so
%attr(755,root,root) %{_libdir}/libbrasero-media.so
%attr(755,root,root) %{_libdir}/libbrasero-utils.so
%{_libdir}/libbrasero-burn.la
%{_libdir}/libbrasero-media.la
%{_libdir}/libbrasero-utils.la
%{_includedir}/brasero
%{_pkgconfigdir}/libbrasero-burn.pc
%{_pkgconfigdir}/libbrasero-media.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbrasero-burn
%{_gtkdocdir}/libbrasero-media

%files -n nautilus-extension-brasero
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-2.0/libnautilus-brasero-extension.so
%{_desktopdir}/brasero-nautilus.desktop
