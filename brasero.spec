# TODO: check build/functionality with new libburn+libisofs
#
# Conditinal build:
%bcond_without	beagle		# disable beagle search
#
Summary:	Disc burning application for GNOME
Summary(pl.UTF-8):	Program do wypalania płyt dla GNOME
Name:		brasero
Version:	0.8.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/brasero/0.8/%{name}-%{version}.tar.bz2
# Source0-md5:	d330593a1f4b701c015259ba80e8cb8b
URL:		http://www.gnome.org/projects/brasero/
BuildRequires:	GConf2-devel >= 2.0.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gnome-doc-utils
BuildRequires:	gstreamer-devel >= 0.10.15
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	hal-devel >= 0.5
BuildRequires:	intltool >= 0.40.0
%{?with_beagle:BuildRequires:	libbeagle-devel >= 0.3.0}
BuildRequires:	libburn-devel >= 0.4.0
BuildRequires:	libgnomeui-devel >= 2.10.0
BuildRequires:	libisofs-devel >= 0.6.4
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	pkgconfig
BuildRequires:	totem-pl-parser-devel >= 2.22.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires(post,preun):	GConf2
Requires:	hal >= 0.5
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

%prep
%setup -q

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_beagle:--disable-search} \
	--disable-caches \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
%find_lang %{name} --all-name --with-gnome --with-omf

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/mime/packages/%{name}.xml
%dir %{_libdir}/brasero
%dir %{_libdir}/brasero/plugins
%attr(755,root,root) %{_libdir}/brasero/plugins/lib*.so
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_mandir}/man1/*
%{_sysconfdir}/gconf/schemas/brasero.schemas
