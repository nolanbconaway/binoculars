import numpy as np
import pytest

import binoculars


@pytest.mark.parametrize("method", ["jeffrey", "wilson", "normal"])
@pytest.mark.parametrize("n", [5, 1e2, 1e3, 1e5, 1e8])
@pytest.mark.parametrize("p", [0.01, 0.5, 0.99])
def test_lower_less_upper(method, n, p):
    """Test the obvious things. lower < p < upper.

    I also added some quick tests of the tail selector.
    """
    l, u = binoculars.binomial_confidence(p, n, method=method)
    assert l < u
    assert l < p
    assert u > p

    assert l == binoculars.binomial_confidence(p, n, method=method, tail="lower")
    assert u == binoculars.binomial_confidence(p, n, method=method, tail="upper")


@pytest.mark.parametrize("method", ["jeffrey", "wilson", "normal"])
@pytest.mark.parametrize("lower_n, greater_n", [(2, 3), (10, 20), (100, 200)])
def test_more_certain_with_n(method, lower_n, greater_n):
    """Test that certainty diminishes with greater N."""
    p = 0.5
    lower_l, lower_u = binoculars.binomial_confidence(p, lower_n, method=method)
    greater_l, greater_u = binoculars.binomial_confidence(p, greater_n, method=method)
    assert lower_l < greater_l
    assert lower_u > greater_u


@pytest.mark.parametrize("method", ["jeffrey", "wilson", "normal"])
@pytest.mark.parametrize("lower_z, greater_z", [(1, 1.01), (1.96, 2.58)])
def test_z_certainty(method, lower_z, greater_z):
    """Test that the interval tightens with lower Z"""
    p, N = 0.5, 100
    lower_l, lower_u = binoculars.binomial_confidence(p, N, method=method, z=lower_z)
    greater_l, greater_u = binoculars.binomial_confidence(
        p, N, method=method, z=greater_z
    )
    assert lower_l > greater_l
    assert lower_u < greater_u


@pytest.mark.parametrize("method", ["jeffrey", "wilson", "normal"])
def test_invalid_tail_error(method):
    with pytest.raises(ValueError):
        binoculars.binomial_confidence(0.1, 10, tail="NOPE", method=method)


def test_invalid_method_error():
    with pytest.raises(ValueError):
        binoculars.binomial_confidence(0.1, 10, method="NOPE")
