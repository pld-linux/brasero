Summary:	Disc burning application for GNOME
Summary(pl):	Program do wypalania dysków dla GNOME
Name:		bonfire
Version:	0.3.1
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://perso.wanadoo.fr/bonfire/%{name}-%{version}.tar.bz2
# Source0-md5:	db94c7ae5ac5c27cf7d66fafc3654f4f
Patch0:		%{name}-desktop.patch
URL:		http://perso.wanadoo.fr/bonfire/
BuildRequires:	beagle-devel >= 0.1.0
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
BuildRequires:	libxml2-devel >= 2.6.0
BuildRequires:	nautilus-cd-burner-devel >= 2.12.0
BuildRequires:	pkgconfig
BuildRequires:	totem-devel >= 1.2.0
Requires(post,postun):	desktop-file-utils
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
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO.tasks
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
