Summary: Displays who is logged in to local network machines
Name: rwho
Version: 0.17
Release: 34%{?dist}
License: BSD
Group: System Environment/Daemons
Source: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rwho-%{version}.tar.gz
Source1: rwhod.init
Patch0: netkit-rwho-0.15-alpha.patch
Patch1: netkit-rwho-0.17-bug22014.patch
Patch2: rwho-0.17-fixbcast.patch
Patch3: rwho-0.17-fixhostname.patch
Patch4: netkit-rwho-0.17-strip.patch
Patch5: netkit-rwho-0.17-include.patch
Patch6: netkit-rwho-0.17-wd_we.patch
Patch7: netkit-rwho-0.17-time.patch
Patch8: netkit-rwho-0.17-gcc4.patch
Patch9: netkit-rwho-0.17-waitchild.patch
Requires: /sbin/chkconfig /etc/init.d
BuildRoot: %{_tmppath}/%{name}-root

%description
The rwho command displays output similar to the output of the who
command (it shows who is logged in) for all machines on the local
network running the rwho daemon.

Install the rwho command if you need to keep track of the users who
are logged in to your local network.

%prep
%setup -q -n netkit-rwho-%{version}
%patch0 -p1 -b .alpha
%patch1 -p1 -b .bug22014
%patch2 -p1 -b .fixbcast
%patch3 -p1 -b .fixhostname
%patch4 -p1 -b .strip
%patch5 -p1 -b .include
%patch6 -p1 -b .wd_we
%patch7 -p1 -b .time
%patch8 -p1 -b .gcc4
%patch9 -p1 -b .waitchild

%build
sh configure --with-c-compiler=gcc
%ifarch s390 s390x
%{__perl} -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -I../include -fPIC,;
    s,^LDFLAGS=,LDFLAGS=-pie,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG
%else
%{__perl} -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -I../include -fpic,;
    s,^LDFLAGS=,LDFLAGS=-pie,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG
%endif
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,8}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}/var/spool/rwho

make INSTALLROOT=${RPM_BUILD_ROOT} install
make INSTALLROOT=${RPM_BUILD_ROOT} install -C ruptime

install -m 755 %SOURCE1 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/rwhod

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/chkconfig --add rwhod

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del rwhod
fi

%files
%defattr(-,root,root)
%doc README
%{_bindir}/ruptime
%{_mandir}/man1/ruptime.1*
%{_bindir}/rwho
%{_mandir}/man1/rwho.1*

%{_sbindir}/rwhod
%{_mandir}/man8/rwhod.8*
/var/spool/rwho
%{_initrddir}/rwhod

%changelog
* Tue May 18 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 0.17-34
- fixed init script
- Resolves: #578425

* Fri Feb 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 0.17-33
- added README
- Related:#543948

* Fri Jan  8 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 0.17-32
- fixed rpmlint warnings
- Resolves: #543948

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.17-31.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.17-29
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.17-28
- Rebuild for selinux ppc32 issue.

* Mon Jul 23 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 0.17-27
- Fixed init script to comply with the LSB standard
- Resolves: #247049

* Tue Aug 15 2006 Harald Hoyer <harald@redhat.com> - 0.17-26
- exit daemon, if child process dies (bug #202493)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.17-25.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.17-25.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.17-25.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 17 2005 Phil Knirsch <pknirsch@redhat.com> 0.17-25
- gcc4 rebuild fixes

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 0.17-24
- bump release and rebuild with gcc 4

* Fri Oct 22 2004 Phil Knirsch <pknirsch@redhat.com> 0.17-23
- Fixed long standig bug with only 42 entries per host showing up (#27643)
- Fixed some warnings of missing prototypes.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 12 2004 Phil Knirsch <pknirsch@redhat.com> 0.17-21
- Enabled PIE for server and application.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 0.17-17
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 0.17-15
- Don't forcibly strip binaries

* Tue Jun 04 2002 Phil Knirsch <pknirsch@redhat.com>
- bumped release number and rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr  4 2001 Jakub Jelinek <jakub@redhat.com>
- don't let configure to guess compiler, it can pick up egcs

* Tue Feb 13 2001 Preston Brown <pbrown@redhat.com>
- hostname was getting null terminated incorrectly.  fixed. (#27419)

* Mon Feb  5 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- i18nize init script (#26083)

* Fri Feb  2 2001 Preston Brown <pbrown@redhat.com>
- don't bcast on virtual interfaces (#20435).  Patch from dwagoner@interTrust.com; thanks.

* Wed Dec 27 2000 Jeff Johnson <jhbj@redhat.com>
- use glibc's <protocols/rwhod.h>, internal version broken on alpha (#22014).

* Thu Aug 10 2000 Bill Nottingham <notting@redhat.com>
- fix broken init script

* Sat Aug 05 2000 Bill Nottingham <notting@redhat.com>
- condrestart fixes

* Thu Jul 20 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Preston Brown <pbrown@redhat.com>
- move initscript

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to 0.17.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Tue Dec 21 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.

* Thu Sep 09 1999 Preston Brown <pbrown@redhat.com>
- postun should have been preun.

* Thu Aug 26 1999 Jeff Johnson <jbj@redhat.com>
- fix unaligned trap on alpha.
- update to 0.15.

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Fri Apr  9 1999 Jeff Johnson <jbj@redhat.com>
- add ruptime (#2023)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- enhanced initscripts

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- added /var/spool/rwho

* Fri Oct 31 1997 Donnie Barnes <djb@redhat.com>
- fixed init script

* Tue Oct 21 1997 Erik Troan <ewt@redhat.com>
- added an init script
- uses chkconfig
- uses attr tags

* Tue Jul 15 1997 Erik Troan <ewt@redhat.com>
- initial build
