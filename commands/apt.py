from __future__ import annotations

import random
import re

from twisted.internet import defer, reactor
from twisted.internet.defer import inlineCallbacks

commands = {}

class FakePackages:
    @staticmethod
    def get_command(name):
        class FakeInstallation:
            def call(self):
                self.print(f'print{name}: Segmentation fault\n')

        return FakeInstallation


def sleep(time, time2=None):
    d = defer.Deffered()
    if time2:
        time = random.randint(time * 100, time2 * 100) / 100.0
    reactor.callLater(time, d.callback, None)
    return d


class APTCommand:
    '''
    only supports the 'install PACKAGE' command $ 'moo'
    Any installed packages, places a 'Segfault' at /usr/bin/PACKAGE.
    '''

    def start(self, command):
        self.commands = command
        if len(command) == 1:
            self.do_help()
        elif len(command) > 1:
            if command[1] == '-v':
                self.version()
            elif command[1] == 'install':
                self.install()
            elif command[1] == 'moo':
                self.moo()
            else:
                self.locked()

    def version(self):
        self.print(
            """apt 1.0.9.8.1 for amd64 compiled on Jun 10 2015 09:42:06
            Supported modules:
            *Ver: Standard .deb
            *Pkg:  Debian dpkg interface (Priority 30)
             Pkg:  Debian APT solver interface (Priority -1000)
             S.L: 'deb' Standard Debian binary tree
             S.L: 'deb-src' Standard Debian source tree
             Idx: Debian Source Index
             Idx: Debian Package Index
             Idx: Debian Translation Index
             Idx: Debian dpkg status file
             Idx: EDSP scenario file\n
             """
        )
        return

    def help(self):
        self.print(
            """apt 1.0.9.8.1 for amd64 compiled on Jun 10 2015 09:42:06
            Usage: apt-get [options] command
                   apt-get [options] install|remove pkg1 [pkg2 ...]
                   apt-get [options] source pkg1 [pkg2 ...]
    
            apt-get is a simple command line interface for downloading and
            installing packages. The most frequently used commands are update
            and install.
    
            Commands:
               update - Retrieve new lists of packages
               upgrade - Perform an upgrade
               install - Install new packages (pkg is libc6 not libc6.deb)
               remove - Remove packages
               autoremove - Remove automatically all unused packages
               purge - Remove packages and config files
               source - Download source archives
               build-dep - Configure build-dependencies for source packages
               dist-upgrade - Distribution upgrade, see apt-get(8)
               dselect-upgrade - Follow dselect selections
               clean - Erase downloaded archive files
               autoclean - Erase old downloaded archive files
               check - Verify that there are no broken dependencies
               changelog - Download and display the changelog for the given package
               download - Download the binary package into the current directory
    
            Options:
              -h  This help text.
              -q  Loggable output - no progress indicator
              -qq No output except for errors
              -d  Download only - do NOT install or unpack archives
              -s  No-act. Perform ordering simulation
              -y  Assume Yes to all queries and do not prompt
              -f  Attempt to correct a system with broken dependencies in place
              -m  Attempt to continue if archives are unlocatable
              -u  Show a list of upgraded packages as well
              -b  Build the source package after fetching it
              -V  Show verbose version numbers
              -c=? Read this configuration file
              -o=? Set an arbitrary configuration option, eg -o dir::cache=/tmp
            See the apt-get(8), sources.list(5) and apt.conf(5) manual
            pages for more information and options.
                                   This APT has Super Cow Powers.\n"""
        )
        return

    @inlineCallbacks
    def install(self, args):
        if len(args) <=1:
            msg = '0 upgraded, 0 newly installed, 0 to remove and {0} not upgraded.\n'
            print(msg.format(random.randint(200, 300)))
            return

        packages = {}

        for y in [re.sub('a-zA-Z0-9', '', x) for x in self.commands[1:]]:
            packages[y] = {
                'version': '{}, {}-{}'.format(
                    random.choice([0, 1]), random.randint(1, 40), random.randint(1, 10)
                ),
                'size': random.randint(100, 900),
            }

        total_size = sum(packages[x]['size'] for x in packages)

        print("Reading package lists... Done\n")
        print("Building dependency tree\n")
        print("Reading state information... Done\n")
        print("The following NEW packages will be installed:\n")
        print("  %s " % " ".join(packages) + "\n")
        print(
            "0 upgraded, %d newly installed, 0 to remove and 259 not upgraded.\n"
            % len(packages)
        )
        print("Need to get %s.2kB of archives.\n" % (total_size))
        print(
            "After this operation, {:.1f}kB of additional disk space will be used.\n".format(
                total_size * 2.2
            )
        )

        i = 1
        for p in packages:
            print(
                "Get:%d http://ftp.debian.org stable/main %s %s [%s.2kB]\n"
                % (i, p, packages[p]["version"], packages[p]["size"])
            )
            i += 1
            yield sleep(1, 2)
        print(f"Fetched {total_size}.2kB in 1s (4493B/s)\n")
        print("Reading package fields... Done\n")
        yield sleep(1, 2)
        print("Reading package status... Done\n")
        print("(Reading database ... 177887 files and directories currently installed.)\n")
        yield sleep(1, 2)
        for p in packages:
            print(
                "Unpacking {} (from .../archives/{}_{}_i386.deb) ...\n".format(
                    p, p, packages[p]["version"]
                )
            )
            yield sleep(1, 2)
        print("Processing triggers for man-db ...\n")
        yield sleep(2)
        for p in packages:
            print("Setting up {} ({}) ...\n".format(p, packages[p]["version"]))
            # self.fs.mkfile("/usr/bin/%s" % p, 0, 0, random.randint(10000, 90000), 33188)
            yield sleep(2)

    def moo(self):
        print("         (__)\n")
        print("         (oo)\n")
        print("   /------\\/\n")
        print("  / |    ||\n")
        print(" *  /\\---/\\ \n")
        print("    ~~   ~~\n")
        print('...."Have you mooed today?"...\n')
        return

    def locked(self):
        print(
            "E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)\n"
        )
        print("E: Unable to lock the list directory\n")
        return
























