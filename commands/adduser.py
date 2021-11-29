# Copyright (c) 2010 Upi Tamminen <desaster@gmail.com>
# See the COPYRIGHT file for more information

from __future__ import annotations

import random
from typing import Optional

from twisted.internet import reactor  # type: ignore
import stinger
commands = {}

O_O, O_Q, O_P = 1, 2, 3


class Command_adduser():
    item: int
    output: list[tuple[int, str]] = [
        (O_O, "Adding user `%(username)s' ..."),
        (O_O, "Adding new group `%(username)s' (1001) ..."),
        (
            O_O,
            "Adding new user `%(username)s' (1001) with group `%(username)s' ...",
        ),
        (O_O, "Creating home directory `/home/%(username)s' ..."),
        (O_O, "Copying files from `/etc/skel' ..."),
        (O_P, "Password: "),
        (O_P, "Password again: "),
        (O_O, "Changing the user information for %(username)s"),
        (O_O, "Enter the new value, or press ENTER for the default"),
        (O_Q, "        Username []: "),
        (O_Q, "        Full Name []: "),
        (O_Q, "        Room Number []: "),
        (O_Q, "        Work Phone []: "),
        (O_Q, "        Home Phone []: "),
        (O_Q, "        Mobile Phone []: "),
        (O_Q, "        Country []: "),
        (O_Q, "        City []: "),
        (O_Q, "        Language []: "),
        (O_Q, "        Favorite movie []: "),
        (O_Q, "        Other []: "),
        (O_Q, "Is the information correct? [Y/n] "),
        (O_O, "ERROR: Some of the information you entered is invalid"),
        (O_O, "Deleting user `%(username)s' ..."),
        (O_O, "Deleting group `%(username)s' (1001) ..."),
        (O_O, "Deleting home directory `/home/%(username)s' ..."),
        (O_Q, "Try again? [Y/n] "),
    ]
    username: Optional[str] = None

    def write(self, data: str) -> None:
        """
        Write a string to the user on stdout
        """
        print(data)

    def start(self, args):
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
        if self.item == len(self.output):
            self.item = 7
            self.schedule_next()
            return

        line = self.output[self.item]
        self.write(line[1] % {"username": self.username})
        if line[0] == O_P:
            print('here: ' + str(self.item))
            self.password_input = True
            return
        if line[0] == O_Q:
            print('other here: ' + str(self.item))
            return
        else:
            self.item += 1
            self.schedule_next()

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


commands["/usr/sbin/adduser"] = Command_adduser
commands["/usr/sbin/useradd"] = Command_adduser
commands["adduser"] = Command_adduser
commands["useradd"] = Command_adduser
