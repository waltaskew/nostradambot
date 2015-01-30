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

    def tokenize(self, text):
        """Return a generator yielding words appearing in the given text."""
        words = nltk.word_tokenize(text)
        words = (word.lower() for word in words)
        words = (self.lemmatizer(word) for word in words)
        words = (word for word in words if word not in self.stop_words)
        return words
