from __future__ import annotations

import random
import time
import re


class FakePackages:
    @staticmethod
    def get_command(name):
        class FakeInstallation:
            def call(self):
                self.write(f'self.write{name}: Segmentation fault\n')

        return FakeInstallation



class APTCommand:
    '''
    only supports the 'install PACKAGE' command $ 'moo'
    Any installed packages, places a 'Segfault' at /usr/bin/PACKAGE.
    '''

    def start(self, command, chan):
        self.commands = command
        self.chan = chan
        if len(command) == 1:
            self.help()
        elif len(command) > 1:
            if command[1] == '-v':
                self.version()
            elif command[1] == 'install':
                self.install(self.commands)
            elif command[1] == 'moo':
                self.moo()
            else:
                self.locked()

    def write(self, data: str) -> None:
        """
        Write a string to the user on stdout
        """
        self.chan.send(data)

    def version(self):
        self.write(
            """apt 1.0.9.8.1 for amd64 compiled on Jun 10 2015 09:42:06\r\n
            Supported modules:\r\n
            *Ver: Standard .deb\r\n
            *Pkg:  Debian dpkg interface (Priority 30)\r\n
             Pkg:  Debian APT solver interface (Priority -1000)\r\n
             S.L: 'deb' Standard Debian binary tree\r\n
             S.L: 'deb-src' Standard Debian source tree\r\n
             Idx: Debian Source Index\r\n
             Idx: Debian Package Index\r\n
             Idx: Debian Translation Index\r\n
             Idx: Debian dpkg status file\r\n
             Idx: EDSP scenario file\r\n
             """
        )
        return

    def help(self):
        self.write(
            """apt 1.0.9.8.1 for amd64 compiled on Jun 10 2015 09:42:06\r\n
            Usage: apt-get [options] command\r\n
                   apt-get [options] install|remove pkg1 [pkg2 ...]\r\n
                   apt-get [options] source pkg1 [pkg2 ...]\r\n
    
            apt-get is a simple command line interface for downloading and\r\n
            installing packages. The most frequently used commands are update\r\n
            and install.\r\n
    \r\n
            Commands:\r\n
               update - Retrieve new lists of packages\r\n
               upgrade - Perform an upgrade\r\n
               install - Install new packages (pkg is libc6 not libc6.deb)\r\n
               remove - Remove packages\r\n
               autoremove - Remove automatically all unused packages\r\n
               purge - Remove packages and config files\r\n
               source - Download source archives\r\n
               build-dep - Configure build-dependencies for source packages\r\n
               dist-upgrade - Distribution upgrade, see apt-get(8)\r\n
               dselect-upgrade - Follow dselect selections\r\n
               clean - Erase downloaded archive files\r\n
               autoclean - Erase old downloaded archive files\r\n
               check - Verify that there are no broken dependencies\r\n
               changelog - Download and display the changelog for the given package\r\n
               download - Download the binary package into the current directory\r\n
    
            Options:\r\n
              -h  This help text.\r\n
              -q  Loggable output - no progress indicator\r\n
              -qq No output except for errors\r\n
              -d  Download only - do NOT install or unpack archives\r\n
              -s  No-act. Perform ordering simulation\r\n
              -y  Assume Yes to all queries and do not prompt\r\n
              -f  Attempt to correct a system with broken dependencies in place\r\n
              -m  Attempt to continue if archives are unlocatable\r\n
              -u  Show a list of upgraded packages as well\r\n
              -b  Build the source package after fetching it\r\n
              -V  Show verbose version numbers\r\n
              -c=? Read this configuration file\r\n
              -o=? Set an arbitrary configuration option, eg -o dir::cache=/tmp\r\n
            See the apt-get(8), sources.list(5) and apt.conf(5) manual\r\n
            pages for more information and options.\r\n
                                   This APT has Super Cow Powers.\r\n"""
        )
        return

    def install(self, args):
        if len(args) <= 1:
            msg = '0 upgraded, 0 newly installed, 0 to remove and {0} not upgraded.\r\n'
            self.write(msg.format(random.randint(200, 300)))
            return

        packages = {}

        for y in [re.sub('a-zA-Z0-9', '', x) for x in self.commands[2:]]:
            packages[y] = {
                'version': '{}, {}-{}'.format(
                    random.choice([0, 1]), random.randint(1, 40), random.randint(1, 10)
                ),
                'size': random.randint(100, 900),
            }

        total_size = sum(packages[x]['size'] for x in packages)

        time.sleep(0.5 + random.random() * 1)
        self.write("Reading package lists... Done\r\n")
        time.sleep(0.5 + random.random() * 1)
        self.write("Building dependency tree\r\n")
        self.write("Reading state information... Done\r\n")
        time.sleep(0.5 + random.random() * 1)
        self.write("The following NEW packages will be installed:\r\n")
        self.write("  %s " % " ".join(packages) + "\r\n")
        self.write(
            "0 upgraded, %d newly installed, 0 to remove and 259 not upgraded.\r\n"
            % (len(packages)-1)
        )
        self.write("Need to get %s.2kB of archives.\r\n" % (total_size))
        self.write(
            "After this operation, {:.1f}kB of additional disk space will be used.\r\n".format(
                total_size * 2.2
            )
        )

        i = 1
        for p in packages:
            self.chan.send(
                "Get:%d http://ftp.debian.org stable/main %s %s [%s.2kB]\r\n"
                % (i, p, packages[p]["version"], packages[p]["size"])
            )
            i += 1
            time.sleep(0.5 + random.random() * 1)
        self.chan.send(f'Fetched {total_size}.2kB in 1s (4493B/s)\r\n')
        self.write("Reading package fields... Done\r\n")
        time.sleep(0.5 + random.random() * 1)
        self.write("Reading package status... Done\r\n")
        self.write("(Reading database ... 177887 files and directories currently installed.)\r\n")
        time.sleep(0.5 + random.random() * 1)
        for p in packages:
            self.chan.send(
                "Unpacking {} (from .../archives/{}_{}_i386.deb) ...\r\n".format(
                    p, p, packages[p]["version"]
                )
            )
            time.sleep(0.5 + random.random() * 1)
        self.write("Processing triggers for man-db ...\r\n")
        time.sleep(0.5 + random.random() * 1)
        for p in packages:
            self.chan.send("Setting up {} ({}) ...\r\n".format(p, packages[p]["version"]))
            # self.fs.mkfile("/usr/bin/%s" % p, 0, 0, random.randint(10000, 90000), 33188)
            time.sleep(0.5 + random.random() * 1)
        return

    def moo(self):
        self.write("         (__)\r\n")
        self.write("         (oo)\r\n")
        self.write("   /------\\/\r\n")
        self.write("  / |    ||\r\n")
        self.write(" *  /\\---/\\\r\n")
        self.write("    ~~   ~~\r\n")
        self.write('...."Have you mooed today?"...\r\n')
        return

    def locked(self):
        self.write(
            "E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)\r\n"
        )
        self.write("E: Unable to lock the list directory\r\n")
        return

