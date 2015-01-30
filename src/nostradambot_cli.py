""""Talk to Nostradamus in a REPL!!!"""

import prophetic_index
import prophetic_parser


def main():
    """HELLO NOSTRADAMUS"""
    index = prophetic_index.InvertedIndex(prophetic_parser.get_prophecies())

    while True:
        text = raw_input("NOSTRADAMBOT CLI >>> ")
        if text:
            print(index.best_prophecy_for(text))


if __name__ == '__main__':
    main()
