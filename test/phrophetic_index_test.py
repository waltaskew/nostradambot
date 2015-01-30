import unittest

import prophetic_index


class InvertedIndexTest(unittest.TestCase):
    """Test the InvertedIndex class."""

    def test_basic_lookup(self):
        """Test insertion and lookups into the index."""
        index = prophetic_index.InvertedIndex(())
        index.add('A man, a plan, a canal - Panama', 0)
        index.add('A CANAL full of SNAKES somehow', 1)
        self.assertEqual(index.lookup('man'), [0])
        self.assertEqual(index.lookup('snake'), [1])
        self.assertEqual(index.lookup('canal'), [0, 1])
        self.assertEqual(index.lookup('carrots'), [])

    def test_basic_scoring(self):
        """Test finding best matches for some text."""
        prophecies = (
            'snakes, planes and automobiles',
            'snakes in my bonnet',
            'bees in my dresser')
        index = prophetic_index.InvertedIndex(prophecies)

        self.assertEqual(
            index.prophecy_with_most_matches_for(['snake', 'plane']),
            prophecies[0])
        self.assertEqual(
            index.prophecy_with_most_matches_for(['snake', 'bonnet']),
            prophecies[1])
        self.assertIn(
            index.prophecy_with_most_matches_for(['snake']),
            (prophecies[:2]))
        self.assertIsNone(index.prophecy_with_most_matches_for(['fire']))

    def test_smart_scoring(self):
        """Test finding fuzzy matches in the index."""
        prophecies = (
            'snakes, planes and automobiles',
            'bees in my dresser')
        index = prophetic_index.InvertedIndex(prophecies)
        self.assertEqual(index.best_prophecy_for('serpent'), prophecies[0])


if __name__ == '__main__':
    unittest.main()
