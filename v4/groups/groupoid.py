"""
"""
import typing

from ..support.typecheckable import meets_interface

from .category import Category
from .decomposable import Decomposable


Morphism = typing.TypeVar('Morphism')


class Groupoid(Category[Morphism],
               Decomposable[Morphism]):
    """A category where composed functions can be decomposed.

    X1 = compose(f1, g1)
    X2 = compose(X1, h1)

    h2, X3 = decompose(X2)
    f2, g2 = decompose(X3)

    X1 == X3
    f1 == f2
    h1 == h2
    g1 == g2

    By equality here, I mean that if given any element in the category, then the output will be the same.
    This sense of equality does not mean that we can directly compare the functions for equality.
    In Python terms, we won't generally be able to do:
        X1.__eq__(X3)
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Groupoid:
            return meets_interface(subclass, Groupoid)
        return NotImplemented
