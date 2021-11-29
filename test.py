
from __future__ import annotations

import traceback
import sys

from twisted.conch.insults import insults
from twisted.protocols.policies import TimeoutMixin
from twisted.python import failure, log

from commands import __all__

class StingerBaseProtocol(insults.TerminalProtocol, TimeoutMixin):
    """
    Base protocol for interactive and non-interactive use
    """

    commands = {}

    for c in __all__:
        try:
            module = __import__(
                f'commands.{c}', globals(), locals(), ['commands']
            )
            commands.update(module.commands)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error(
                "Failed to import command {}: {}: {}".format(
                    c,
                    e,
                    "".join(
                        traceback.format_exception(exc_type, exc_value, exc_traceback)
                    ),
                )
            )


    def __init__(self):
        self.password_input = False




