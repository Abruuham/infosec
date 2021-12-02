from __future__ import annotations

import getopt

class CatCommand:
    number = False
    line_number = 1

    def start(self, args, chan):
        self.args = args[1:]
        self.chan = chan
        self.cwd = '/'
        try:
            optlist, args = getopt.gnu_getopt(
                self.args, 'AsbEnstTuv', ['help', 'number', 'version']
            )
        except getopt.GetoptError as err:
            self.chan.send(f"cat: invalid option -- '{err.opt}'\r\nTry 'cat --help' for more information.\r\n")
            return

        for o, a in optlist:
            if o in ('--help'):
                self.help()
                return
            elif o in ('-n', '--number'):
                self.number = True
        #
        # if len(self.args) > 0:
        #     for arg in self.args:
        #         if arg == '-':
        #             self.output(self.input_data)
        #             continue
        #
        #         pname = self.resolve_path(arg, self.cwd)
        #         if self.is_dir(pname):
        #             self.chan.send(f"cat: {arg}: is a directory\r\n")
        #             continue
        #
        #         try:
        #             contents = self.file_contents(pname)
        #             if contents:
        #                 self.output(contents)
        #             else:
        #                 self.chan.send('File not found.')
        #
        #         except FileNotFoundError:
        #             self.chan.send(f"cat: {arg}: No such file or directory.\r\n")
        #     return
        # elif self.input_data is not None:
        #     self.output(self.input_data)

    def help(self):
        self.chan.send(
            """Usage: cat [OPTION]... [FILE]...
            Concatenate FILE(s) to standard output.

            With no FILE, or when FILE is -, read standard input.

                -A, --show-all           equivalent to -vET
                -b, --number-nonblank    number nonempty output lines, overrides -n
                -e                       equivalent to -vE
                -E, --show-ends          display $ at end of each line
                -n, --number             number all output lines
                -s, --squeeze-blank      suppress repeated empty output lines
                -t                       equivalent to -vT
                -T, --show-tabs          display TAB characters as ^I
                -u                       (ignored)
                -v, --show-nonprinting   use ^ and M- notation, except for LFD and TAB
                    --help     display this help and exit
                    --version  output version information and exit

            Examples:
                cat f - g  Output f's contents, then standard input, then g's contents.
                cat        Copy standard input to standard output.

            GNU coreutils online help: <http://www.gnu.org/software/coreutils/>
            Full documentation at: <http://www.gnu.org/software/coreutils/cat>
            or available locally via: info '(coreutils) cat invocation'\r\n
            """
        )

    def output(self, input):
        if input is None:
            return

        if isinstance(input, str):
            input = input.encode('utf8')
        elif isinstance(input, bytes):
            pass
        else:
            pass

        lines = input.split(b'\n')
        if lines[-1] == b'':
            lines.pop()
        for line in lines:
            if self.number:
                self.chan.send(f'{self.line_number:>6}   ')
                self.line_number += 1
            self.chan.send(line + b'\r\n')



























