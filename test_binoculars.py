import numpy as np
import pytest

import binoculars


@pytest.mark.parametrize("method", ["jeffrey", "wilson", "normal"])
@pytest.mark.parametrize("n", [5, 1e2, 1e3, 1e5, 1e8])
@pytest.mark.parametrize("p", [0.01, 0.5, 0.99])
def test_lower_less_upper(method, n, p):
    l, u = binoculars.binomial_confidence(p, n, method=method)
    assert l < u
    assert l < p
    assert u > p


@pytest.mark.parametrize("method", ["jeffrey", "wilson", "normal"])
@pytest.mark.parametrize("lower_n, greater_n", [(2, 3), (10, 20), (100, 200)])
def test_more_certain_with_n(method, lower_n, greater_n):
    p = 0.5
    lower_l, lower_u = binoculars.binomial_confidence(p, lower_n, method=method)
    greater_l, greater_u = binoculars.binomial_confidence(p, greater_n, method=method)
    assert lower_l < greater_l
    assert lower_u > greater_u


def test_invalid_arg_errors():
    with pytest.raises(ValueError):
        binoculars.binomial_confidence(0.1, 10, tail="NOPE")

    with pytest.raises(ValueError):
        binoculars.binomial_confidence(0.1, 10, method="NOPE")
