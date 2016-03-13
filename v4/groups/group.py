"""
"""
import typing

from .monoid import Monoid
from .splitable import Splitable


GroupElement_TV = typing.TypeVar('GroupElement_TV')


class Group(Monoid[GroupElement_TV], Splitable[GroupElement_TV]):
    """A category where append functions can be inverted.

    X1 = append(f1, g1)
    X2 = append(X1, h1)

    h2, X3 = split(X2)
    f2, g2 = split(X3)

    X1 == X3
    f1 == f2
    h1 == h2
    g1 == g2

    """
    pass
