# TODO: build for xemacs
%bcond_with	xemacs	# Build without XEmacs support
%bcond_without	emacs	# Build without GNU Emacs support
%define		_the_name cedet
%define		_beta 3b
Summary:	Collection of Emacs development tools
Summary(pl):	Zbiór narzêdzi programistycznych dla Emacsa
Name:		emacsen-cedet-pkg
Version:	1.0
Release:	0.beta%{_beta}.1
License:	GPL
Group:		Applications/Editors/Emacs
Source0:	http://dl.sourceforge.net/%{_the_name}/%{_the_name}-%{version}beta%{_beta}.tar.gz
# Source0-md5:	f24a07c8c934596fb33a81b653edaf73
URL:		http://cedet.sf.net/
BuildRequires:	texinfo
%if %{with emacs}
BuildRequires:	emacs
%endif
%if %{with xemacs}
BuildRequires:	xemacs
%endif
Requires:	cedet-elisp-code = %{version}-%{release}
Conflicts:	xemacs-cedet-pkg
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CEDET is a collection of tools written with the end goal of creating
an advanced development environment in Emacs.

This package contains files common to both GNU Emacs and XEmacs.

%description -l pl
CEDET jest zbiorem narzêdzi stworzonych z my¶l± o utworzeniu
zaawansowanego ¶rodowiska programistycznego w Emacsie.

Ten pakiet zawiera pliki CEDET wspólne dla GNU Emacsa i XEmacsa.

%define version_of() %{expand:%%(rpm -q %1 --queryformat '%%%%{version}-%%%%{release}')}

%if %{with emacs}
%package emacs
Summary:	CEDET compiled elisp files for GNU Emacs
Summary(pl):	Skompilowany kod elisp CEDET dla GNU Emacsa
Group:		Applications/Editors/Emacs
Requires:	%{name} = %{version}-%{release}
Requires:	emacs = %{version_of emacs}
Provides:	cedet-elisp-code = %{version}-%{release}

%description emacs
This package contains compiled elisp files needed to run CEDET on GNU Emacs

%description emacs -l pl
Pakiet zawiera skompilowane pliki elisp z kodem CEDET dla GNU Emacsa.

%package emacs-el
Summary:	CEDET elisp files for GNU Emacs
Summary(pl):	Kod elisp CEDET dla GNU Emacsa
Group:		Applications/Editors/Emacs
Requires:	%{name}-emacs = %{version}-%{release}

%description emacs-el
This package contains CEDET source elisp files for GNU Emacs

%description emacs-el -l pl
Pakiet zawiera ¼ród³owe pliki elisp z kodem CEDET dla GNU Emacsa.
%endif


%if %{with xemacs}
%package xemacs
Summary:	CEDET elisp files for XEmacs
Summary(pl):	Kod elisp CEDET dla XEmacsa
Group:		Applications/Editors/Emacs
Requires:	%{name} = %{version}-%{release}
Requires:	xemacs = %{version_of xemacs}
Provides:	cedet-elisp-code = %{version}-%{release}

%description xemacs
This package contains compiled elisp files needed to run CEDET on XEmacs

%description xemacs -l pl
Pakiet zawiera skompilowane pliki elisp z kodem CEDET dla XEmacsa.

%package xemacs-el
Summary:	CEDET elisp source files for XEmacs
Summary(pl):	Kod ¼ród³owy elisp CEDET dla XEmacsa
Group:		Applications/Editors/Emacs
Requires:	%{name}-xemacs = %{version}-%{release}

%description xemacs-el
This package contains source CEDET elisp files for  XEmacs

%description xemacs-el -l pl
Pakiet zawiera pliki ¼ród³owe elisp z kodem CEDET dla XEmacsa.
%endif


%prep
%setup -q -n %{_the_name}-%{version}beta%{_beta}


%build

# Move documentation
for F in */{INSTALL,README,ChangeLog,AUTHORS,NEWS,ONEWS}; do \
	cp $F `echo $F | sed 's-\(.*\)/\(.*\)-\2.\1-'`; done

%if %{with xemacs}
mkdir _xemacs
%endif

%if %{with emacs}
mkdir _emacs
cp -a [^_]* _emacs
%{__make} -C _emacs \
	EMACS=emacs
%endif

%install

mkdir -p $RPM_BUILD_ROOT%{_infodir}

%if %{with xemacs}
%endif

%if %{with emacs}
mkdir -p $RPM_BUILD_ROOT{%{_emacs_lispdir},%{_datadir}/emacs/cedet}
cp -a _emacs/* $RPM_BUILD_ROOT%{_datadir}/emacs/cedet/
cat >$RPM_BUILD_ROOT%{_emacs_lispdir}/cedet.el <<EOF
;; Load CEDET
(load-file "%{_datadir}/emacs/cedet/common/cedet.elc")
;; Enabling SEMANTIC minor modes.  See semantic/INSTALL for more ideas.
(semantic-load-enable-code-helpers)
EOF

cd _emacs \
	&& find . -name '*.info*' -print0 \
	| xargs -0  sh -c 'install "$@" '$RPM_BUILD_ROOT%{_infodir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL* README* ChangeLog* AUTHORS* NEWS* ONEWS*
%{_infodir}/*

%if %{with emacs}
%files emacs
%defattr(644,root,root,755)
%dir %{_datadir}/emacs/%{_the_name}
%dir %{_datadir}/emacs/%{_the_name}/[a-z]*
%dir %{_datadir}/emacs/%{_the_name}/semantic/wisent
%dir %{_datadir}/emacs/%{_the_name}/semantic/bovine
%{_datadir}/emacs/%{_the_name}/common/icons
%{_datadir}/emacs/%{_the_name}/*/Project.ede
%{_datadir}/emacs/%{_the_name}/*/*.elc
%{_datadir}/emacs/%{_the_name}/*/*.wy
%{_datadir}/emacs/%{_the_name}/semantic/*/Project.ede
%{_datadir}/emacs/%{_the_name}/semantic/*/*.elc
%{_datadir}/emacs/%{_the_name}/semantic/wisent/*.wy
%{_datadir}/emacs/%{_the_name}/semantic/bovine/*.by
%{_datadir}/emacs/%{_the_name}/speedbar/*.xpm
%{_emacs_lispdir}/cedet.el

%files emacs-el
%defattr(644,root,root,755)
%{_datadir}/emacs/%{_the_name}/*/*.el
%{_datadir}/emacs/%{_the_name}/*/*/*.el
%endif

%if %{with xemacs}
%files xemacs
%defattr(644,root,root,755)
%dir %{_datadir}/xemacs-packages/lisp/%{_the_name}
%{_datadir}/xemacs-packages/lisp/%{_the_name}/*.elc
%{_datadir}/xemacs-packages/etc/%{_the_name}

%files xemacs-el
%defattr(644,root,root,755)
%{_datadir}/xemacs-packages/lisp/%{_the_name}/*.el
%endif
