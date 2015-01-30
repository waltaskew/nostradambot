import random

import nltk
import collections


class InvertedIndex(object):
    """An inverted index mapping word appearances to their prophecy id."""

    def __init__(self):
        self.index = collections.defaultdict(list)
        self.lemmatizer = nltk.stem.WordNetLemmatizer().lemmatize
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def add(self, text, prophecy_id):
        """Add the given text to our inverted index."""
        words = self.tokenize(text)
        words = set(words)
        for word in words:
            self.index[word].append(prophecy_id)

    def lookup(self, word):
        """Retrieve prophecy ids containing the given word."""
        word = self.lemmatizer(word).lower()
        return self.index[word]

    def best_prophecy_for(self, words):
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

    def tokenize(self, text):
        """Return a generator yielding words appearing in the given text."""
        words = nltk.word_tokenize(text)
        words = (word.lower() for word in words)
        words = (self.lemmatizer(word) for word in words)
        words = (word for word in words if word not in self.stop_words)
        return words
