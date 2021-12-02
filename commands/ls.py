from __future__ import annotations

from colors import bcolors


BLUE = bcolors.COLOR["BLUE"]
RESET = bcolors.COLOR["RESET_ALL"]


class LSCommand:

    def start(self, arg, chan):
        self.args = arg
        self.chan = chan
        if len(self.args) <= 1:
            self.list()
            return
        else:
            if len(self.args) > 1 and self.args[1] == '--help':
                self.help()
            elif len(self.args) > 1 and self.args[1] == '-la':
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
            """Usage: ls [OPTION]... [FILE]...\r
List information about the FILEs (the current directory by default).\r
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.\r\n
Mandatory arguments to long options are mandatory for short options too.\r
  -a, --all                  do not ignore entries starting with .\r
  -A, --almost-all           do not list implied . and ..\r
      --author               with -l, print the author of each file\r
  -b, --escape               print C-style escapes for nongraphic characters\r
      --block-size=SIZE      with -l, scale sizes by SIZE when printing them;\r
                               e.g., '--block-size=M'; see SIZE format below\r
  -B, --ignore-backups       do not list implied entries ending with ~\r
  -c                         with -lt: sort by, and show, ctime (time of last\r
                               modification of file status information);\r
                               with -l: show ctime and sort by name;\r
                               otherwise: sort by ctime, newest first\r
  -C                         list entries by columns\r
      --color[=WHEN]         colorize the output; WHEN can be 'always' (default\r
                               if omitted), 'auto', or 'never'; more info below\r
  -d, --directory            list directories themselves, not their contents\r
  -D, --dired                generate output designed for Emacs' dired mode\r
  -f                         do not sort, enable -aU, disable -ls --color\r
  -F, --classify             append indicator (one of */=>@|) to entries\r
      --file-type            likewise, except do not append '*'\r
      --format=WORD          across -x, commas -m, horizontal -x, long -l,\r
                               single-column -1, verbose -l, vertical -C\r
      --full-time            like -l --time-style=full-iso\r
  -g                         like -l, but do not list owner\r
      --group-directories-first\r
                             group directories before files;\r
                               can be augmented with a --sort option, but any\r
                               use of --sort=none (-U) disables grouping\r
  -G, --no-group             in a long listing, don't print group names\r
  -h, --human-readable       with -l and -s, print sizes like 1K 234M 2G etc.\r
      --si                   likewise, but use powers of 1000 not 1024\r
  -H, --dereference-command-line\r
                             follow symbolic links listed on the command line\r
      --dereference-command-line-symlink-to-dir\r
                             follow each command line symbolic link\r
                               that points to a directory\r
      --hide=PATTERN         do not list implied entries matching shell PATTERN\r
                               (overridden by -a or -A)\r
      --hyperlink[=WHEN]     hyperlink file names; WHEN can be 'always'\r
                               (default if omitted), 'auto', or 'never'\r
      --indicator-style=WORD  append indicator with style WORD to entry names:\r
                               none (default), slash (-p),\r
                               file-type (--file-type), classify (-F)\r
  -i, --inode                print the index number of each file\r
  -I, --ignore=PATTERN       do not list implied entries matching shell PATTERN\r
  -k, --kibibytes            default to 1024-byte blocks for disk usage;\r
                               used only with -s and per directory totals\r
  -l                         use a long listing format\r
  -L, --dereference          when showing file information for a symbolic\r
                               link, show information for the file the link\r
                               references rather than for the link itself\r
  -m                         fill width with a comma separated list of entries\r
  -n, --numeric-uid-gid      like -l, but list numeric user and group IDs\r
  -N, --literal              print entry names without quoting\r
  -o                         like -l, but do not list group information\r
  -p, --indicator-style=slash\r
                             append / indicator to directories\r
  -q, --hide-control-chars   print ? instead of nongraphic characters\r
      --show-control-chars   show nongraphic characters as-is (the default,\r
                               unless program is 'ls' and output is a terminal)\r
  -Q, --quote-name           enclose entry names in double quotes\r
      --quoting-style=WORD   use quoting style WORD for entry names:\r
                               literal, locale, shell, shell-always,\r
                               shell-escape, shell-escape-always, c, escape\r
                               (overrides QUOTING_STYLE environment variable)\r
  -r, --reverse              reverse order while sorting\r
  -R, --recursive            list subdirectories recursively\r
  -s, --size                 print the allocated size of each file, in blocks\r
  -S                         sort by file size, largest first\r
      --sort=WORD            sort by WORD instead of name: none (-U), size (-S),\r
                               time (-t), version (-v), extension (-X)\r
      --time=WORD            change the default of using modification times;\r
                               access time (-u): atime, access, use;\r
                               change time (-c): ctime, status;\r
                               birth time: birth, creation;\r
                             with -l, WORD determines which time to show;\r
                             with --sort=time, sort by WORD (newest first)\r
      --time-style=TIME_STYLE  time/date format with -l; see TIME_STYLE below\r
  -t                         sort by time, newest first; see --time\r
  -T, --tabsize=COLS         assume tab stops at each COLS instead of 8\r
  -u                         with -lt: sort by, and show, access time;\r
                               with -l: show access time and sort by name;\r
                               otherwise: sort by access time, newest first\r
  -U                         do not sort; list entries in directory order\r
  -v                         natural sort of (version) numbers within text\r
  -w, --width=COLS           set output width to COLS.  0 means no limit\r
  -x                         list entries by lines instead of by columns\r
  -X                         sort alphabetically by entry extension\r
  -Z, --context              print any security context of each file\r
  -1                         list one file per line.  Avoid '\\n' with -q or -b\r
      --help     display this help and exit\r
      --version  output version information and exit\r

The SIZE argument is an integer and optional unit (example: 10K is 10*1024).\r
Units are K,M,G,T,P,E,Z,Y (powers of 1024) or KB,MB,... (powers of 1000).\r
Binary prefixes can be used, too: KiB=K, MiB=M, and so on.\r

The TIME_STYLE argument can be full-iso, long-iso, iso, locale, or +FORMAT.\r
FORMAT is interpreted like in date(1).  If FORMAT is FORMAT1<newline>FORMAT2,\r
then FORMAT1 applies to non-recent files and FORMAT2 to recent files.\r
TIME_STYLE prefixed with 'posix-' takes effect only outside the POSIX locale.\r
Also the TIME_STYLE environment variable sets the default style to use.\r

Using color to distinguish file types is disabled both by default and\r
with --color=never.  With --color=auto, ls emits color codes only when\r
standard output is connected to a terminal.  The LS_COLORS environment\r
variable can change the settings.  Use the dircolors command to set it.\r\n
Exit status:\r
 0  if OK,\r
 1  if minor problems (e.g., cannot access subdirectory),\r
 2  if serious trouble (e.g., cannot access command-line argument).\r\n
GNU coreutils online help: <https://www.gnu.org/software/coreutils/>\r
Full documentation <https://www.gnu.org/software/coreutils/ls>\r
or available locally via: info '(coreutils) ls invocation'\r\n
"""
        )

    def list_all(self):
        self.chan.send(
            """total 25056\r
drwxr-xr-x 31 root root     4096 Dec  1 16:48 .\r
drwxr-xr-x 20 root root    36864 Nov  2 01:51 ..\r
-rw-------  1 root root    33717 Dec  1 16:48 .bash_history\r
-rw-r--r--  1 root root     3412 Sep 15 21:19 .bashrc\r
-rw-r--r--  1 root root    16241 Jun 29  2019 binary\r
drwx------  5 root root     4096 Aug 10  2019 binaryninja\r
drwx------  2 root root     4096 Jun 27  2019 .BurpSuite\r
drwx------ 21 root root     4096 Oct 14 16:45 .cache\r
drwxr-xr-x  4 root root     4096 Sep 15 21:21 .cargo\r
drwxr-xr-x 23 root root     4096 Nov  2 01:16 .config\r
drwx------  3 root root     4096 Oct 14 16:45 .dbus\r
drwxr-xr-x  3 root root     4096 Sep 23 21:15 Desktop\r
drwxr-xr-x 11 root root     4096 Nov 27 21:45 Documents\r
drwxr-xr-x  4 root root     4096 Oct 26 14:50 Downloads\r
-rw-rw-rw-  1 root root   402432 Jul  4  2019 EasyPass.exe\r
-rw-r--r--  1 root root    11656 Sep 27  2020 .face\r
lrwxrwxrwx  1 root root       11 Sep 27  2020 .face.icon -> /root/.face\r
drwxr-xr-x  3 root root     4096 Sep 23 21:06 .gem\r
-rw-r--r--  1 root root       29 Nov 30 23:28 .gitconfig\r
-rw-------  1 root root       69 Dec  1 02:37 .git-credentials\r
drwx------  3 root root     4096 Dec  1 16:44 .gnupg\r
-rw-r--r--  1 root root        0 Nov  2 02:00 hamster.txt\r
-rw-------  1 root root    10804 Sep 23 20:40 .ICEauthority\r
-rw-rw-rw-  1 root root     6304 Aug 10  2019 impossible_password.bin\r
-rwxrw-rw-  1 root root  3315571 Aug 21  2019 init_sat\r
drwx------  2 root root     4096 Oct 26 14:36 .irssi\r
drwxr-xr-x  4 root root     4096 Jun 27  2019 .java\r
drwx------  2 root root     4096 Oct 12 20:07 .kismet\r
drwx------  3 root root     4096 May 17  2019 .local\r
drwx------  5 root root     4096 Jun 27  2019 .mozilla\r
drwxr-xr-x  9 root root     4096 Sep 23 21:10 .msf4\r
drwxr-xr-x  2 root root     4096 May 17  2019 Music\r
drwxr-xr-x 10 root root     4096 Aug 21  2019 PhoneInfoga\r
drwxr-xr-x  2 root root     4096 May 17  2019 Pictures\r
-rw-r--r--  1 root root      169 Sep 15 21:19 .profile\r
drwxr-xr-x  2 root root     4096 May 17  2019 Public\r
-rw-------  1 root root        7 Aug 21  2019 .python_history\r
-rw-rw-rw-  1 root root     8800 Aug 21  2019 rand2\r
drwxr-xr-x  6 root root     4096 Sep 15 21:19 .rustup\r
-rw-r--r--  1 root root     1330 Jun 28  2019 shadow\r
drwxr-xr-x  2 root root     4096 Oct 12 20:36 Shellter_Backups\r
-rw-r--r--  1 root root 21426176 Nov  2 02:00 sniff-2021-11-02-eth.pcap\r
-rw-r--r--  1 root root    78336 Oct 12 20:39 something321.exe\r
-rw-r--r--  1 root root    78336 Oct 12 22:36 something32.exe\r
drwx------  2 root root     4096 Sep  3  2020 .ssh\r
drwxr-xr-x  2 root root     4096 May 17  2019 Templates\r
drwx------  3 root root     4096 Oct 26 18:16 .tor\r
-rw-r-----  1 root root        5 Dec  1 16:44 .vboxclient-clipboard.pid\r
-rw-r-----  1 root root        5 Dec  1 16:44 .vboxclient-display.pid\r
-rw-r-----  1 root root        4 Dec  1 16:43 .vboxclient-display-svga.pid\r
-rw-r-----  1 root root        5 Dec  1 16:44 .vboxclient-draganddrop.pid\r
-rw-r-----  1 root root        5 Dec  1 16:44 .vboxclient-seamless.pid\r
drwxr-xr-x  2 root root     4096 May 17  2019 Videos\r
drwxr-xr-x  2 root root     4096 Nov 28 17:45 .vim\r
-rw-------  1 root root    23096 Dec  1 02:21 .viminfo\r
-rw-r--r--  1 root root      206 Jun  1  2020 .wget-hsts\r
drwxr-xr-x  4 root root     4096 Oct 12 22:34 .wine\r
-rw-r--r--  1 root root       21 Sep 15 21:19 .zshenv\r\n
"""
        )
