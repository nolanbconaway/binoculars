"""Stats functions for binomial distributions with tricky/confusing math."""
from typing import Tuple, Union

import numpy as np
from scipy import stats


def binomial_jeffreys_interval(p: float, n: int, tail: str, z: float = 1.96):
    """Use compute a jeffrey's interval via beta distirbution CDF."""
    alpha = stats.norm.sf(z)
    a = n * p + 0.5
    b = n - n * p + 0.5
    if tail == "lower":
        return stats.beta.ppf(alpha, a, b)
    elif tail == "upper":
        return stats.beta.ppf(1 - alpha, a, b)
    else:
        raise ValueError("Invalid tail! Choose from: lower, upper")


def binomial_wilson_interval(p: float, n: int, tail: str, z: float = 1.96):
    """Return the wilson interval for a proportion."""
    denom = 1 + z * z / n
    if tail == "lower":
        num = p + z * z / (2 * n) - z * np.sqrt((p * (1 - p) + z * z / (4 * n)) / n)
    elif tail == "upper":
        num = p + z * z / (2 * n) + z * np.sqrt((p * (1 - p) + z * z / (4 * n)) / n)
    else:
        raise ValueError("Invalid tail! Choose from: lower, upper")
    return num / denom


def binomial_normal_interval(p: float, n: int, tail: str, z: float = 1.96):
    """Return the normal interval for a proportion."""
    se = np.sqrt((p * (1 - p)) / n)
    if tail == "lower":
        return p - z * se
    elif tail == "upper":
        return p + z * se
    else:
        raise ValueError("Invalid tail! Choose from: lower, upper")


def binomial_confidence(
    p: float, n: int, tail: str = None, z: float = 1.96, method="jeffrey"
) -> Union[float, Tuple[float]]:
    """Return a confidence interval for a binomial proportion.

    Arguments
    ---------
        p : float
            The p parameter of the binomial for the distribution.
        n : int
            The n parameter of the binomial for the distributionon,
        tail : str
            Tail of the CI to return, either lower or upper. If not provided, this function returns
            a tuple of (lower, upper). if provided, it returns a float value.
        z : float
            Optional Z critical value. Default 1.96 for 95%.
        method : str
            Optional approximation method. By default this uses Jeffrey's interval. Options:
            jeffrey, wilson, normal.

    Returns
        A tuple of (lower, upper) confidence interval values, or a single value.
    """
    if tail is not None and tail not in ("lower", "upper"):
        raise ValueError("Invalid tail! Choose from: lower, upper")

    try:
        func = {
            "jeffrey": binomial_jeffreys_interval,
            "wilson": binomial_wilson_interval,
            "normal": binomial_normal_interval,
        }[method]

    except KeyError:
        raise ValueError("Invalid method! Choose from: jeffrey, wilson, normal")

    if tail is not None:
        return func(p=p, n=n, z=z, tail=tail)

    return func(p=p, n=n, z=z, tail="lower"), func(p=p, n=n, z=z, tail="upper")
