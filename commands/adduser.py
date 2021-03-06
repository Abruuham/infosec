# Copyright (c) 2010 Upi Tamminen <desaster@gmail.com>
# See the COPYRIGHT file for more information

from __future__ import annotations

import random
import time

from typing import Optional


UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = '\x7f'.encode()

O_O, O_Q, O_P = 1, 2, 3

class Command_adduser():
    item: int
    output: list[tuple[int, str]] = [
        (O_O, "Adding user `%(username)s' ...\r\n"),
        (O_O, "Adding new group `%(username)s' (1001) ...\r\n"),
        (
            O_O,
            "Adding new user `%(username)s' (1001) with group `%(username)s' ...\r\n",
        ),
        (O_O, "Creating home directory `/home/%(username)s' ...\r\n"),
        (O_O, "Copying files from `/etc/skel' ...\r\n"),
        (O_P, "Password: "),
        (O_P, "\r\nPassword again: "),
        (O_O, "\r\nChanging the user information for %(username)s\r\n"),
        (O_O, "Enter the new value, or press ENTER for the default\r\n"),
        (O_Q, "\tUsername []: "),
        (O_Q, "\n\tFull Name []: "),
        (O_Q, "\n\tRoom Number []: "),
        (O_Q, "\n\tWork Phone []: "),
        (O_Q, "\n\tHome Phone []: "),
        (O_Q, "\n\tMobile Phone []: "),
        (O_Q, "\n\tCountry []: "),
        (O_Q, "\n\tCity []: "),
        (O_Q, "\n\tLanguage []: "),
        (O_Q, "\n\tFavorite movie []: "),
        (O_Q, "\n\tOther []: "),
        (O_Q, "\r\nIs the information correct? [Y/n] "),
        (O_O, "\r\nERROR: Some of the information you entered is invalid\r\n"),
        (O_O, "Deleting user `%(username)s' ...\r\n"),
        (O_O, "Deleting group `%(username)s' (1001) ...\r\n"),
        (O_O, "Deleting home directory `/home/%(username)s' ...\r\n"),
        (O_Q, "Try again? [Y/n] "),
    ]
    username: Optional[str] = None

    def write(self, data: str) -> None:
        """
        Write a string to the user on stdout
        """
        if self.item == 5 or self.item == 6:
            self.chan.send(data)
            command = ''
            while not command.endswith("\r"):
                transport = self.chan.recv(1024)
                # Echo input to pseudo-simulate a basic terminal
                if (
                        transport != UP_KEY
                        and transport != DOWN_KEY
                        and transport != LEFT_KEY
                        and transport != RIGHT_KEY
                        and transport != BACK_KEY
                ):
                    command += transport.decode('utf-8')

        elif 9 <= self.item <= 20:
            self.chan.send(data)
            command = ''
            while not command.endswith("\r"):
                transport = self.chan.recv(1024)
                # Echo input to pseudo-simulate a basic terminal
                if (
                        transport != UP_KEY
                        and transport != DOWN_KEY
                        and transport != LEFT_KEY
                        and transport != RIGHT_KEY
                        and transport != BACK_KEY
                ):
                    self.chan.send(transport)
                    command += transport.decode('utf-8')
                    if self.item == 20:
                        self.line_received(command)
                        command += '\r'
        else:
            self.chan.send(data)

    def start(self, args, chan, transport):
        self.chan = chan
        self.complete = False
        self.transport = transport
        self.item = 0
        self.password_input = False
        if args.startswith("-") or args.isdigit():
            pass
        self.username = args
        if self.username is None:
            self.write("adduser: Only one or two names allowed.\n")
            self.exit()
            return
        self.do_output()
        return 1

    def do_output(self):
        while self.item < 26 and self.complete is not True:
            if self.item == len(self.output):
                self.item = 7

            line = self.output[self.item]
            time.sleep(0.5 + random.random() * 1)
            self.write(line[1] % {"username": self.username})
            self.item += 1
        return 1

    def line_received(self, line):
        if self.item + 1 == len(self.output) and line.strip() in ("n", "no"):
            return
        elif self.item == 20 and line not in ("y", "yes"):
            self.item = 7
            self.write("\r\nOk, starting over\n")
            return
        elif not len(line) and self.output[self.item][0] == O_Q:
            self.write("Must enter a value!\n")
        else:
            self.item += 1
            self.complete = True
            self.chan.send('\r\n')
