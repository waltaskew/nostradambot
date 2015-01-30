"""Get a list of prophecies from the html in a directory."""


import lxml.html
import os
import re


PROPHECY_DIR = 'src/prophecy_html'
PROPHECY_SPLIT_RE = re.compile('[\n]*^[\d]+\n', flags=re.MULTILINE)


def iter_prophecy_files(prophecy_dir):
    """Return a generator yielding the text of all the files
    in @prophecy_dir.
    """
    for file_name in os.listdir(prophecy_dir):
        path = os.path.join(prophecy_dir, file_name)
        _, extension = os.path.splitext(path)
        if extension == '.html':
            yield path


def get_text(file_name):
    """Seperate the prophecy text from html noise and return the text."""
    with open(file_name, 'r') as prophetic_html:
        tree = lxml.html.parse(prophetic_html)
        root = tree.getroot()
        text = root.xpath('body/pre')[0].text_content()
        return text


def parse_prophecies(text):
    """Return a list of prophecies from a big text blob containing
    a series of them.
    """
    prophecies = PROPHECY_SPLIT_RE.split(text)
    prophecies = [prophecy.strip() for prophecy in prophecies]
    return [prophecy for prophecy in prophecies if prophecy]


def get_prophecies(prophecy_dir=PROPHECY_DIR):
    """Get a list of prophecies from the html in @prophecy_dir."""
    all_prophecies = []
    for prophecy_file in iter_prophecy_files(prophecy_dir):
        text = get_text(prophecy_file)
        all_prophecies.extend(parse_prophecies(text))
    return all_prophecies
