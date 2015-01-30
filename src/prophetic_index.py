import itertools
import random

import nltk
import collections


class InvertedIndex(object):
    """An inverted index mapping word appearances to their prophecy id."""

    def __init__(self, prophecies, max_wordnet_recursions=10):
        self.index = collections.defaultdict(list)
        self.max_wordnet_recursions = max_wordnet_recursions

        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.stem = nltk.stem.porter.PorterStemmer().stem

        self.prophecies = prophecies
        for idx, prophecy in enumerate(prophecies):
            self.add(prophecy, idx)

    def add(self, text, prophecy_id):
        """Add the given text to our inverted index."""
        words = self.tokenize(text)
        words = set(words)
        for word in words:
            self.index[word].append(prophecy_id)

    def lookup(self, word):
        """Retrieve prophecy ids containing the given word."""
        word = self.stem(word).lower()
        return self.index[word]

    def prophecy_with_most_matches_for(self, words):
        """Find the prophecy with the most matches for the given words.

        Return the prophecy with the most matches for the list of words,
        breaking ties randomly.
        """
        prophecy_matches = collections.defaultdict(int)
        for word in words:
            prophecy_ids = self.lookup(word)
            for prophecy_id in prophecy_ids:
                prophecy_matches[prophecy_id] += 1

        if prophecy_matches:
            most_matches = -1
            best_prophecies = []
            for prophecy_id, matches in prophecy_matches.iteritems():
                if matches == most_matches:
                    best_prophecies.append(prophecy_id)
                elif matches > most_matches:
                    most_matches = matches
                    best_prophecies = [prophecy_id]
            return self.prophecies[random.choice(best_prophecies)]
        else:
            return None

    def best_prophecy_for(self, text):
        """Find the prophecy with words most similiar to the given text."""
        tokens = nltk.word_tokenize(text)
        pos_tags = nltk.tag.pos_tag(tokens)
        wordnet_pos = ((word, get_wordnet_pos(pos)) for
                       word, pos in pos_tags)
        synsets = set(itertools.chain.from_iterable(
            nltk.corpus.wordnet.synsets(word, pos=pos) for
            word, pos in wordnet_pos if pos))

        attempted_words = set()
        attempted_synsets = set()

        i = 0
        while True:
            words_to_attempt = set(itertools.chain.from_iterable(
                synset.lemma_names() for synset in synsets))
            if i == 0:
                # include the raw words on the first pass
                words_to_attempt.update(tokens)
            words_to_attempt = words_to_attempt.difference(attempted_words)

            prophecy = self.prophecy_with_most_matches_for(
                words_to_attempt)
            if prophecy is not None:
                return prophecy
            else:
                i += 1
                attempted_words.update(words_to_attempt)
                attempted_synsets.update(synsets)
                synsets = set(itertools.chain.from_iterable(
                    synset.hypernyms() + synset.hyponyms() for
                    synset in synsets))
                synsets = synsets.difference(attempted_synsets)
                if not synsets or i >= self.max_wordnet_recursions:
                    # We give up and return a random id :(
                    return random.choice(self.prophecies)

    def tokenize(self, text):
        """Return a generator yielding words appearing in the given text."""
        words = nltk.word_tokenize(text)
        words = (self.stem(word) for word in words)
        words = (word.lower() for word in words)
        words = (word for word in words if word not in self.stop_words)
        return words


def get_wordnet_pos(treebank_tag):
    """Return the wordnet POS tag given a treebank one."""
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return None
