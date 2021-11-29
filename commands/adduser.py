# Copyright (c) 2010 Upi Tamminen <desaster@gmail.com>
# See the COPYRIGHT file for more information

from __future__ import annotations

import random
import time

from typing import Optional
import sys

from twisted.internet import reactor  # type: ignore
commands = {}

UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = '\x7f'.encode()

O_O, O_Q, O_P = 1, 2, 3
sys.setrecursionlimit(1000000)

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
        (O_Q, "        Username []: "),
        (O_Q, "        \r\nFull Name []: "),
        (O_Q, "        \r\nRoom Number []: "),
        (O_Q, "        \r\nWork Phone []: "),
        (O_Q, "        \r\nHome Phone []: "),
        (O_Q, "        \r\nMobile Phone []: "),
        (O_Q, "        \r\nCountry []: "),
        (O_Q, "        \r\nCity []: "),
        (O_Q, "        \r\nLanguage []: "),
        (O_Q, "        \r\nFavorite movie []: "),
        (O_Q, "        \r\nOther []: "),
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
                    self.chan.send(transport)
                    command += transport.decode('utf-8')

        elif self.item >= 9 and self.item <= 20:
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
        else:
            self.chan.send(data)

    def start(self, args, chan, transport):
        self.chan = chan
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

    def do_output(self):
        while self.item < 26:
            if self.item == len(self.output):
                self.item = 7
                # self.schedule_next()

            line = self.output[self.item]
            time.sleep(0.5 + random.random() * 1)
            self.write(line[1] % {"username": self.username})
            self.item += 1
                # self.schedule_next()

    def schedule_next(self):
        self.scheduled = reactor.callLater(0.5 + random.random() * 1, self.do_output())

    def lineReceived(self, line):
        if self.item + 1 == len(self.output) and line.strip() in ("n", "no"):
            self.exit()
            return
        elif self.item == 20 and line.strip() not in ("y", "yes"):
            self.item = 7
            self.write("Ok, starting over\n")
        elif not len(line) and self.output[self.item][0] == O_Q:
            self.write("Must enter a value!\n")
        else:
            self.item += 1
        self.schedule_next()
        self.password_input = False
