""""Talk to Nostradamus in a REPL!!!"""

import prophetic_index
import prophetic_parser


def main():
    """HELLO NOSTRADAMUS"""
    prophecies = prophetic_parser.get_prophecies()
    index = prophetic_index.InvertedIndex()
    for idx, prophecy in enumerate(prophecies):
        index.add(prophecy, idx)

    while True:
        text = raw_input("NOSTRADAMBOT CLI >>> ")
        if text:
            print(prophecies[index.best_prophecy_for(text)])


if __name__ == '__main__':
    main()
