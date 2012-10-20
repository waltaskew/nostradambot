"""Reveal Nostradamus' prophecies"""
import random

import hippybot.decorators
import prophetic_parser


PROPHECIES = prophetic_parser.get_prophecies()
PROPHECIES_LENGTH = len(PROPHECIES)


class Plugin(object):
    """Reveal Nostradamus' prophecies"""
    global_commands = ['prophecy']
    command_aliases = {'prophecize': 'prophecy'}

    @hippybot.decorators.botcmd
    def prophecy(self, mess, args):
        """Reveal Nostradamus' prophecies"""
        index = random.randrange(0, PROPHECIES_LENGTH)
        return PROPHECIES[index]

    @hippybot.decorators.directcmd
    def hello(self, mess, args):
        """Reveal Nostradamus' prophecies"""
        index = random.randrange(0, PROPHECIES_LENGTH)
        return PROPHECIES[index]
