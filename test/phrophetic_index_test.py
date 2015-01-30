import unittest

import prophetic_index


class InvertedIndexTest(unittest.TestCase):
    """Test the InvertedIndex class."""

    def test_basic_lookup(self):
        """Test insertion and lookups into the index."""
        index = prophetic_index.InvertedIndex()
        index.add('A man, a plan, a canal - Panama', 0)
        index.add('A CANAL full of SNAKES somehow', 1)
        self.assertEqual(index.lookup('man'), [0])
        self.assertEqual(index.lookup('snake'), [1])
        self.assertEqual(index.lookup('canal'), [0, 1])
        self.assertEqual(index.lookup('carrots'), [])


if __name__ == '__main__':
    unittest.main()
