from __future__ import annotations

from colors import bcolors


BLUE = bcolors.COLOR["BLUE"]
RESET = bcolors.COLOR["RESET_ALL"]


class LSCommand(object):

    def __int__(self, arg, chan):
        self.args = arg
        self.chan = chan

    def start(self):

        if len(self.args) <= 1:
            self.list()
            return
        else:
            if len(self.args) == 1 and self.args[1] == '--help':
                self.help()
            elif len(self.args) == 1 and self.args[1] == '-la':
                self.list_all()
                return
            else:
                self.chan.send('Try ls --help for more information.\r\n')
                return

    def list(self):
        self.chan.send(
            "binary        impossible_password.bin  shadow\r\n" +
            BLUE +
            "binaryninja   init_sat                 Shellter_Backups\r\n" +
            "Desktop       Music                    " + RESET +"sniff-2021-11-02-eth.pcap\r\n" +
            BLUE +
            "Documents     PhoneInfoga              " + RESET + "something321.exe\r\n" +
            BLUE +
            "Downloads     Pictures                 " + RESET + "something32.exe\r\n" +
            "EasyPass.exe  " + BLUE + "Public                   Templates\r\n" +
            RESET +
            "hamster.txt   rand2                    " + BLUE + "Videos\r\n"
        )
        return

    def help(self):
        self.chan.send(
            """
            Usage: ls [OPTION]... [FILE]...
            List information about the FILEs (the current directory by default).
            Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
            
            Mandatory arguments to long options are mandatory for short options too.
              -a, --all                  do not ignore entries starting with .
              -A, --almost-all           do not list implied . and ..
                  --author               with -l, print the author of each file
              -b, --escape               print C-style escapes for nongraphic characters
                  --block-size=SIZE      with -l, scale sizes by SIZE when printing them;
                                           e.g., '--block-size=M'; see SIZE format below
              -B, --ignore-backups       do not list implied entries ending with ~
              -c                         with -lt: sort by, and show, ctime (time of last
                                           modification of file status information);
                                           with -l: show ctime and sort by name;
                                           otherwise: sort by ctime, newest first
              -C                         list entries by columns
                  --color[=WHEN]         colorize the output; WHEN can be 'always' (default
                                           if omitted), 'auto', or 'never'; more info below
              -d, --directory            list directories themselves, not their contents
              -D, --dired                generate output designed for Emacs' dired mode
              -f                         do not sort, enable -aU, disable -ls --color
              -F, --classify             append indicator (one of */=>@|) to entries
                  --file-type            likewise, except do not append '*'
                  --format=WORD          across -x, commas -m, horizontal -x, long -l,
                                           single-column -1, verbose -l, vertical -C
                  --full-time            like -l --time-style=full-iso
              -g                         like -l, but do not list owner
                  --group-directories-first
                                         group directories before files;
                                           can be augmented with a --sort option, but any
                                           use of --sort=none (-U) disables grouping
              -G, --no-group             in a long listing, don't print group names
              -h, --human-readable       with -l and -s, print sizes like 1K 234M 2G etc.
                  --si                   likewise, but use powers of 1000 not 1024
              -H, --dereference-command-line
                                         follow symbolic links listed on the command line
                  --dereference-command-line-symlink-to-dir
                                         follow each command line symbolic link
                                           that points to a directory
                  --hide=PATTERN         do not list implied entries matching shell PATTERN
                                           (overridden by -a or -A)
                  --hyperlink[=WHEN]     hyperlink file names; WHEN can be 'always'
                                           (default if omitted), 'auto', or 'never'
                  --indicator-style=WORD  append indicator with style WORD to entry names:
                                           none (default), slash (-p),
                                           file-type (--file-type), classify (-F)
              -i, --inode                print the index number of each file
              -I, --ignore=PATTERN       do not list implied entries matching shell PATTERN
              -k, --kibibytes            default to 1024-byte blocks for disk usage;
                                           used only with -s and per directory totals
              -l                         use a long listing format
              -L, --dereference          when showing file information for a symbolic
                                           link, show information for the file the link
                                           references rather than for the link itself
              -m                         fill width with a comma separated list of entries
              -n, --numeric-uid-gid      like -l, but list numeric user and group IDs
              -N, --literal              print entry names without quoting
              -o                         like -l, but do not list group information
              -p, --indicator-style=slash
                                         append / indicator to directories
              -q, --hide-control-chars   print ? instead of nongraphic characters
                  --show-control-chars   show nongraphic characters as-is (the default,
                                           unless program is 'ls' and output is a terminal)
              -Q, --quote-name           enclose entry names in double quotes
                  --quoting-style=WORD   use quoting style WORD for entry names:
                                           literal, locale, shell, shell-always,
                                           shell-escape, shell-escape-always, c, escape
                                           (overrides QUOTING_STYLE environment variable)
              -r, --reverse              reverse order while sorting
              -R, --recursive            list subdirectories recursively
              -s, --size                 print the allocated size of each file, in blocks
              -S                         sort by file size, largest first
                  --sort=WORD            sort by WORD instead of name: none (-U), size (-S),
                                           time (-t), version (-v), extension (-X)
                  --time=WORD            change the default of using modification times;
                                           access time (-u): atime, access, use;
                                           change time (-c): ctime, status;
                                           birth time: birth, creation;
                                         with -l, WORD determines which time to show;
                                         with --sort=time, sort by WORD (newest first)
                  --time-style=TIME_STYLE  time/date format with -l; see TIME_STYLE below
              -t                         sort by time, newest first; see --time
              -T, --tabsize=COLS         assume tab stops at each COLS instead of 8
              -u                         with -lt: sort by, and show, access time;
                                           with -l: show access time and sort by name;
                                           otherwise: sort by access time, newest first
              -U                         do not sort; list entries in directory order
              -v                         natural sort of (version) numbers within text
              -w, --width=COLS           set output width to COLS.  0 means no limit
              -x                         list entries by lines instead of by columns
              -X                         sort alphabetically by entry extension
              -Z, --context              print any security context of each file
              -1                         list one file per line.  Avoid '\n' with -q or -b
                  --help     display this help and exit
                  --version  output version information and exit
            
            The SIZE argument is an integer and optional unit (example: 10K is 10*1024).
            Units are K,M,G,T,P,E,Z,Y (powers of 1024) or KB,MB,... (powers of 1000).
            Binary prefixes can be used, too: KiB=K, MiB=M, and so on.
            
            The TIME_STYLE argument can be full-iso, long-iso, iso, locale, or +FORMAT.
            FORMAT is interpreted like in date(1).  If FORMAT is FORMAT1<newline>FORMAT2,
            then FORMAT1 applies to non-recent files and FORMAT2 to recent files.
            TIME_STYLE prefixed with 'posix-' takes effect only outside the POSIX locale.
            Also the TIME_STYLE environment variable sets the default style to use.
            
            Using color to distinguish file types is disabled both by default and
            with --color=never.  With --color=auto, ls emits color codes only when
            standard output is connected to a terminal.  The LS_COLORS environment
            variable can change the settings.  Use the dircolors command to set it.
            
            Exit status:
             0  if OK,
             1  if minor problems (e.g., cannot access subdirectory),
             2  if serious trouble (e.g., cannot access command-line argument).
            
            GNU coreutils online help: <https://www.gnu.org/software/coreutils/>
            Full documentation <https://www.gnu.org/software/coreutils/ls>
            or available locally via: info '(coreutils) ls invocation'\r\n
            """
        )

    def list_all(self):
        self.chan.send(
            """
            total 25056
            drwxr-xr-x 31 root root     4096 Dec  1 16:48 .
            drwxr-xr-x 20 root root    36864 Nov  2 01:51 ..
            -rw-------  1 root root    33717 Dec  1 16:48 .bash_history
            -rw-r--r--  1 root root     3412 Sep 15 21:19 .bashrc
            -rw-r--r--  1 root root    16241 Jun 29  2019 binary
            drwx------  5 root root     4096 Aug 10  2019 binaryninja
            drwx------  2 root root     4096 Jun 27  2019 .BurpSuite
            drwx------ 21 root root     4096 Oct 14 16:45 .cache
            drwxr-xr-x  4 root root     4096 Sep 15 21:21 .cargo
            drwxr-xr-x 23 root root     4096 Nov  2 01:16 .config
            drwx------  3 root root     4096 Oct 14 16:45 .dbus
            drwxr-xr-x  3 root root     4096 Sep 23 21:15 Desktop
            drwxr-xr-x 11 root root     4096 Nov 27 21:45 Documents
            drwxr-xr-x  4 root root     4096 Oct 26 14:50 Downloads
            -rw-rw-rw-  1 root root   402432 Jul  4  2019 EasyPass.exe
            -rw-r--r--  1 root root    11656 Sep 27  2020 .face
            lrwxrwxrwx  1 root root       11 Sep 27  2020 .face.icon -> /root/.face
            drwxr-xr-x  3 root root     4096 Sep 23 21:06 .gem
            -rw-r--r--  1 root root       29 Nov 30 23:28 .gitconfig
            -rw-------  1 root root       69 Dec  1 02:37 .git-credentials
            drwx------  3 root root     4096 Dec  1 16:44 .gnupg
            -rw-r--r--  1 root root        0 Nov  2 02:00 hamster.txt
            -rw-------  1 root root    10804 Sep 23 20:40 .ICEauthority
            -rw-rw-rw-  1 root root     6304 Aug 10  2019 impossible_password.bin
            -rwxrw-rw-  1 root root  3315571 Aug 21  2019 init_sat
            drwx------  2 root root     4096 Oct 26 14:36 .irssi
            drwxr-xr-x  4 root root     4096 Jun 27  2019 .java
            drwx------  2 root root     4096 Oct 12 20:07 .kismet
            drwx------  3 root root     4096 May 17  2019 .local
            drwx------  5 root root     4096 Jun 27  2019 .mozilla
            drwxr-xr-x  9 root root     4096 Sep 23 21:10 .msf4
            drwxr-xr-x  2 root root     4096 May 17  2019 Music
            drwxr-xr-x 10 root root     4096 Aug 21  2019 PhoneInfoga
            drwxr-xr-x  2 root root     4096 May 17  2019 Pictures
            -rw-r--r--  1 root root      169 Sep 15 21:19 .profile
            drwxr-xr-x  2 root root     4096 May 17  2019 Public
            -rw-------  1 root root        7 Aug 21  2019 .python_history
            -rw-rw-rw-  1 root root     8800 Aug 21  2019 rand2
            drwxr-xr-x  6 root root     4096 Sep 15 21:19 .rustup
            -rw-r--r--  1 root root     1330 Jun 28  2019 shadow
            drwxr-xr-x  2 root root     4096 Oct 12 20:36 Shellter_Backups
            -rw-r--r--  1 root root 21426176 Nov  2 02:00 sniff-2021-11-02-eth.pcap
            -rw-r--r--  1 root root    78336 Oct 12 20:39 something321.exe
            -rw-r--r--  1 root root    78336 Oct 12 22:36 something32.exe
            drwx------  2 root root     4096 Sep  3  2020 .ssh
            drwxr-xr-x  2 root root     4096 May 17  2019 Templates
            drwx------  3 root root     4096 Oct 26 18:16 .tor
            -rw-r-----  1 root root        5 Dec  1 16:44 .vboxclient-clipboard.pid
            -rw-r-----  1 root root        5 Dec  1 16:44 .vboxclient-display.pid
            -rw-r-----  1 root root        4 Dec  1 16:43 .vboxclient-display-svga.pid
            -rw-r-----  1 root root        5 Dec  1 16:44 .vboxclient-draganddrop.pid
            -rw-r-----  1 root root        5 Dec  1 16:44 .vboxclient-seamless.pid
            drwxr-xr-x  2 root root     4096 May 17  2019 Videos
            drwxr-xr-x  2 root root     4096 Nov 28 17:45 .vim
            -rw-------  1 root root    23096 Dec  1 02:21 .viminfo
            -rw-r--r--  1 root root      206 Jun  1  2020 .wget-hsts
            drwxr-xr-x  4 root root     4096 Oct 12 22:34 .wine
            -rw-r--r--  1 root root       21 Sep 15 21:19 .zshenv\r\n
            """
        )
