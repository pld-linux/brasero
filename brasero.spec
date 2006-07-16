Summary:	Disc burning application for GNOME
Summary(pl):	Program do wypalania dysków dla GNOME
Name:		bonfire
Version:	0.4.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://dl.sourceforge.net/bonfire/%{name}-%{version}.tar.bz2
# Source0-md5:	d8c99448c696693574ab8fad5132a4de
Patch0:		%{name}-desktop.patch
URL:		http://perso.wanadoo.fr/bonfire/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.30
BuildRequires:	gdl-devel >= 0.5.0
BuildRequires:	gnome-vfs2-devel >= 2.12.0
BuildRequires:	gstreamer-devel >= 0.10.6
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:	gtk+2-devel >= 2:2.6.0
BuildRequires:	hal-devel >= 0.5
BuildRequires:	intltool >= 0.25
BuildRequires:	libgnomeui-devel >= 2.10.0
BuildRequires:	libnotify-devel >= 0.3.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	nautilus-cd-burner-devel >= 2.12.0
BuildRequires:	pkgconfig
BuildRequires:	totem-devel >= 1.2.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	shared-mime-info
Requires:	hal >= 0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bonfire is a CD/DVD mastering tool for the GNOME desktop.
It is designed to be simple and easy to use.

%description -l pl
Bonfire jest narzêdziem do masteringu p³yt CD/DVD dla biurka
GNOME. Jest zaprojektowany by byæ prostym i ³atwym w obs³udze.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_beagle:--disable-search}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	mimeicondir=%{_datadir}/icons/hicolor/48x48/mimetypes

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
update-mime-database %{_datadir}/mime >/dev/null 2>&1 ||:
gtk-update-icon-cache -ft %{_datadir}/icons/hicolor
%update_desktop_database_post

%postun
umask 022
update-mime-database %{_datadir}/mime >/dev/null 2>&1
gtk-update-icon-cache -ft %{_datadir}/icons/hicolor
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO.tasks
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/mime/packages/bonfire.xml
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/
%{_pixmapsdir}/*.png
