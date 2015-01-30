import itertools
import random

import nltk
import collections


class InvertedIndex(object):
    """An inverted index mapping word appearances to their prophecy id."""

    def __init__(self, max_wordnet_recursions=10):
        self.index = collections.defaultdict(list)
        self.max_wordnet_recursions = max_wordnet_recursions
        self.prophecy_ids = set()

        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.stem = nltk.stem.porter.PorterStemmer().stem

    def add(self, text, prophecy_id):
        """Add the given text to our inverted index."""
        self.prophecy_ids.add(prophecy_id)
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

        Return the prophecy id with the most matches for the list of words,
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
            return random.choice(best_prophecies)
        else:
            return None

    def best_prophecy_for(self, text):
        """Find the prophecy with words most similiar to the given text."""
        tokens = nltk.word_tokenize(text)
        search_words = [self.stem(word.lower()) for word in tokens]
        prophecy_id = self.prophecy_with_most_matches_for(search_words)
        if prophecy_id is not None:
            return prophecy_id
        else:
            # We expand our search into related words using wordnet
            pos_tags = nltk.tag.pos_tag(search_words)
            wordnet_pos = ((word, get_wordnet_pos(pos)) for
                           word, pos in pos_tags)
            synsets = set(itertools.chain.from_iterable(
                nltk.corpus.wordnet.synsets(word, pos=pos) for
                word, pos in wordnet_pos if pos))

            attempted_words = set(search_words)
            attempted_synsets = set()

            i = 0
            while synsets and i < self.max_wordnet_recursions:
                i = i + 1

                words_to_attempt = set(itertools.chain.from_iterable(
                    synset.lemma_names() for synset in synsets))
                words_to_attempt = words_to_attempt.difference(attempted_words)

                prophecy_id = self.prophecy_with_most_matches_for(
                    words_to_attempt)
                if prophecy_id is not None:
                    return prophecy_id
                else:
                    attempted_words.update(words_to_attempt)
                    attempted_synsets.update(synsets)
                    synsets = set(itertools.chain.from_iterable(
                        synset.hypernyms() + synset.hyponyms() for
                        synset in synsets))
                    synsets = synsets.difference(attempted_synsets)
            # We give up and return a random id :(
            return random.choice(self.prophecy_ids)

    def tokenize(self, text):
        """Return a generator yielding words appearing in the given text."""
        words = nltk.word_tokenize(text)
        words = (word.lower() for word in words)
        words = (self.stem(word) for word in words)
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
