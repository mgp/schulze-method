schulze-method
==============

A Python implementation of the [Schulze method](http://en.wikipedia.org/wiki/Schulze_method).

To rank candidates, call the `compute_ranks` method of the `schulze` module. This method has the following signature and Pydoc:

```python
def compute_ranks(candidate_names, weighted_ranks):
    """Returns the candidates ranked by the Schulze method.

    Parameter candidate_names is a sequence containing all the candidate names.

    Parameter weighted_ranks is a sequence of (ranks, weight) pairs.

    The first element, ranks, is a ranking of the candidates. It is an array of
    arrays so that we can express ties. For example, [[a, b], [c], [d, e]]
    represents a = b > c > d = e.

    The second element, weight, is typically the number of voters that chose
    this ranking.
    """
```

For example usage, refer to the `schulze_test` module. From the command line, you can run these tests like so:

```text
$ python -m unittest schulze_test
.....
----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK
```

