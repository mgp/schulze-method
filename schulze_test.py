"""Tests for the schulze module."""

__author__ = "Michael G. Parker"
__contact__ = "http://omgitsmgp.com/"


from collections import defaultdict
import itertools
import unittest

import schulze


class SchulzeTest(unittest.TestCase):
    def _make_ranks(self, names):
        return [[name] for name in names]

    def _assert_row(self, matrix, name, expected_values):
        other_names = (other_name for other_name in 'abcde' if other_name != name)
        for other_name, expected_value in itertools.izip(other_names, expected_values):
            actual_value = matrix.get((name, other_name), 0)
            self.assertEqual(expected_value, actual_value,
                    'matrix(%s, %s)=%s, expected %s' %
                        (name, other_name, actual_value, expected_value))

    def _compute_d_wikipedia(self):
        """Computes the d array found at http://en.wikipedia.org/wiki/Schulze_method."""
        d = defaultdict(int)

        # 5 people think A > C > B > E > D.
        ranks = self._make_ranks('acbed')
        schulze._add_ranks_to_d(d, ranks, 5)
        # 5 people think A > D > E > C > B.
        ranks = self._make_ranks('adecb')
        schulze._add_ranks_to_d(d, ranks, 5)
        # 8 people think B > E > D > A > C.
        ranks = self._make_ranks('bedac')
        schulze._add_ranks_to_d(d, ranks, 8)
        # 3 people think C > A > B > E > D.
        ranks = self._make_ranks('cabed')
        schulze._add_ranks_to_d(d, ranks, 3)
        # 7 people think C > A > E > B > D.
        ranks = self._make_ranks('caebd')
        schulze._add_ranks_to_d(d, ranks, 7)
        # 2 people think C > B > A > D > E.
        ranks = self._make_ranks('cbade')
        schulze._add_ranks_to_d(d, ranks, 2)
        # 7 people think D > C > E > B > A.
        ranks = self._make_ranks('dceba')
        schulze._add_ranks_to_d(d, ranks, 7)
        # 8 people think E > B > A > D > C.
        ranks = self._make_ranks('ebadc')
        schulze._add_ranks_to_d(d, ranks, 8)

        return d

    def test_compute_d_wikipedia(self):
        """Tests computing the d array found at http://en.wikipedia.org/wiki/Schulze_method."""
        d = self._compute_d_wikipedia()

        for name in 'abcde':
            self.assertNotIn((name, name), d)
        self._assert_row(d, 'a', (20, 26, 30, 22))
        self._assert_row(d, 'b', (25, 16, 33, 18))
        self._assert_row(d, 'c', (19, 29, 17, 24))
        self._assert_row(d, 'd', (15, 12, 28, 14))
        self._assert_row(d, 'e', (23, 27, 21, 31))

    def test_compute_p_wikipedia(self):
        """Tests computing the p array found at http://en.wikipedia.org/wiki/Schulze_method."""
        d = self._compute_d_wikipedia()

        candidate_names = 'abcde'
        p = schulze._compute_p(d, candidate_names)

        for name in 'abcde':
            self.assertNotIn((name, name), p)
        self._assert_row(p, 'a', (28, 28, 30, 24))
        self._assert_row(p, 'b', (25, 28, 33, 24))
        self._assert_row(p, 'c', (25, 29, 29, 24))
        self._assert_row(p, 'd', (25, 28, 28, 24))
        self._assert_row(p, 'e', (25, 28, 28, 31))

    def test_rank_p_wikipedia(self):
        d = self._compute_d_wikipedia()
        candidate_names = 'abcde'
        p = schulze._compute_p(d, candidate_names)
        best = schulze._rank_p(candidate_names, p)

        expected_best = self._make_ranks('eacbd')
        self.assertSequenceEqual(expected_best, best)

    def test_tie(self):
        candidate_names = 'abcde'
        top = candidate_names[0:2]
        middle = candidate_names[2]
        bottom = candidate_names[3:5]
        ranks = [top, middle, bottom]
        weighted_ranks = [(ranks, 10)]
        best = schulze.compute_ranks(candidate_names, weighted_ranks)

        expected_best = [['a', 'b'], ['c'], ['d', 'e']]
        self.assertSequenceEqual(expected_best, best)

    def test_all_tie(self):
        candidate_names = 'abcde'
        ranks = [candidate_names]
        weighted_ranks = [(ranks, 10)]
        best = schulze.compute_ranks(candidate_names, weighted_ranks)

        expected_best = [['a', 'b', 'c', 'd', 'e']]
        self.assertSequenceEqual(expected_best, best)

