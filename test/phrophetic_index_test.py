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

    def test_basic_scoring(self):
        """Test finding best matches for some text."""
        index = prophetic_index.InvertedIndex()
        index.add('snakes, planes and automobiles', 0)
        index.add('snakes in my bonnet', 1)
        index.add('bees in my dresser', 2)

        self.assertEqual(index.best_prophecy_for(['snake', 'plane']), 0)
        self.assertEqual(index.best_prophecy_for(['snake', 'bonnet']), 1)
        for _ in range(5):
            self.assertIn(index.best_prophecy_for(['snake']), (0, 1))
        self.assertIsNone(index.best_prophecy_for(['fire']))


if __name__ == '__main__':
    unittest.main()
