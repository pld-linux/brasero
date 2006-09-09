#
# Conditinal build:
%bcond_without	beagle		# disable beagle search
#
Summary:	Disc burning application for GNOME
Summary(pl):	Program do wypalania dysków dla GNOME
Name:		brasero
Version:	0.4.4
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/bonfire/%{name}-%{version}.tar.bz2
# Source0-md5:	1ef6ae66677ed9136634692d8bc1cc7a
Patch0:		%{name}-desktop.patch
URL:		http://perso.wanadoo.fr/bonfire/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_beagle:BuildRequires:	beagle-devel >= 0.1.0}
BuildRequires:	dbus-glib-devel >= 0.30
BuildRequires:	gdl-devel >= 0.6.0
BuildRequires:	gnome-vfs2-devel >= 2.12.0
BuildRequires:	gstreamer-devel >= 0.10.6
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:	gtk+2-devel >= 2:2.6.0
BuildRequires:	hal-devel >= 0.5
BuildRequires:	intltool >= 0.25
BuildRequires:	libgnomeui-devel >= 2.10.0
BuildRequires:	libnotify-devel >= 0.3.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.0
BuildRequires:	nautilus-cd-burner-devel >= 2.12.0
BuildRequires:	pkgconfig
BuildRequires:	totem-devel >= 1.2.0
Requires(post,postun):	desktop-file-utils
Requires:	hal >= 0.5
Obsoletes:	bonfire
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Brasero is a CD/DVD mastering tool for the GNOME desktop.
It is designed to be simple and easy to use.

%description -l pl
Brasero jest narzêdziem do masteringu p³yt CD/DVD dla biurka
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
	%{!?with_beagle:--disable-search} \
	--disable-caches
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_iconsdir}/{gnome,hicolor}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO.tasks
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/mime/packages/%{name}.xml
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_pixmapsdir}/*.png
