"""Reveal Nostradamus' prophecies"""
import random

import hippybot.decorators
import prophetic_parser


PROPHECIES = prophetic_parser.get_prophecies()
PROPHECIES_LENGTH = len(PROPHECIES)


class Plugin(object):
    """Reveal Nostradamus' prophecies"""
    global_commands = ['prophecy', 'prophesize', 'prophecize']

    @hippybot.decorators.botcmd
    def prophecy(self, mess, args):
        """Reveal Nostradamus' prophecies"""
        index = random.randrange(0, PROPHECIES_LENGTH)
        return PROPHECIES[index]

    @hippybot.decorators.botcmd
    def prophesize(self, *args, **kwargs):
        """Reveal Nostradamus' prophecies"""
        return self.prophecy(*args, **kwargs)

    @hippybot.decorators.botcmd
    def prophecize(self, *args, **kwargs):
        """Reveal Nostradamus' prophecies"""
        return self.prophecy(*args, **kwargs)
