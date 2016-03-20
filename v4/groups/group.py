"""
"""
import typing

from ..support.typecheckable import meets_interface

from .monoid import Monoid
from .splitable import Splittable


Element = typing.TypeVar('Element')


class Group(Monoid[Element],
            Splittable[Element]):
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
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Group:
            return meets_interface(subclass, Group)
        return NotImplemented
