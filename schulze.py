"""Ranks candidates by the Schulze method.

For more information read http://en.wikipedia.org/wiki/Schulze_method.
"""

__author__ = "Michael G. Parker"
__contact__ = "http://omgitsmgp.com/"


from collections import defaultdict


def _add_remaining_ranks(d, candidate_name, remaining_ranks, weight):
    for remaining_rank in remaining_ranks:
        for other_candidate_name in remaining_rank:
            d[candidate_name, other_candidate_name] += weight


def _add_ranks_to_d(d, ranks, weight):
    for i, rank in enumerate(ranks):
        remaining_ranks = ranks[i+1:]
        for candidate_name in rank:
            _add_remaining_ranks(d, candidate_name, remaining_ranks, weight)


def _compute_d(weighted_ranks):
    """Computes the d array in the Schulze method.

    d[V,W] is the number of voters who prefer candidate V over W.
    """
    d = defaultdict(int)
    for ranks, weight in weighted_ranks:
        _add_ranks_to_d(d, ranks, weight)
    return d


def _compute_p(d, candidate_names):
    """Computes the p array in the Schulze method.

    p[V,W] is the strength of the strongest path from candidate V to W.
    """
    p = {}
    for candidate_name1 in candidate_names:
        for candidate_name2 in candidate_names:
            if candidate_name1 != candidate_name2:
                strength = d.get((candidate_name1, candidate_name2), 0)
                if strength > d.get((candidate_name2, candidate_name1), 0):
                    p[candidate_name1, candidate_name2] = strength

    for candidate_name1 in candidate_names:
        for candidate_name2 in candidate_names:
            if candidate_name1 != candidate_name2:
                for candidate_name3 in candidate_names:
                    if (candidate_name1 != candidate_name3) and (candidate_name2 != candidate_name3):
                        curr_value = p.get((candidate_name2, candidate_name3), 0)
                        new_value = min(
                                p.get((candidate_name2, candidate_name1), 0),
                                p.get((candidate_name1, candidate_name3), 0))
                        if new_value > curr_value:
                            p[candidate_name2, candidate_name3] = new_value

    return p


def _rank_p(candidate_names, p):
    """Ranks the candidates by p."""
    candidate_wins = defaultdict(list)

    for candidate_name1 in candidate_names:
        num_wins = 0

        # Compute the number of wins this candidate has over all other candidates.
        for candidate_name2 in candidate_names:
            if candidate_name1 == candidate_name2:
                continue
            candidate1_score = p.get((candidate_name1, candidate_name2), 0)
            candidate2_score = p.get((candidate_name2, candidate_name1), 0)
            if candidate1_score > candidate2_score:
                num_wins += 1

        candidate_wins[num_wins].append(candidate_name1)

    sorted_wins = sorted(candidate_wins.iterkeys(), reverse=True)
    return [candidate_wins[num_wins] for num_wins in sorted_wins]


def compute_ranks(candidate_names, weighted_ranks):
    """Returns the candidates ranked by the Schulze method.

    See http://en.wikipedia.org/wiki/Schulze_method for details.

    Parameter candidate_names is a sequence containing all the candidate names.

    Parameter weighted_ranks is a sequence of (ranks, weight) pairs.
    The first element, ranks, is a ranking of the candidates. It is an array of arrays so that we
    can express ties. For example, [[a, b], [c], [d, e]] represents a = b > c > d = e.
    The second element, weight, is typically the number of voters that chose this ranking.
    """
    d = _compute_d(weighted_ranks)
    p = _compute_p(d, candidate_names)
    return _rank_p(candidate_names, p)

