"""
"""
import typing

from ..support.typecheckable import TypeCheckableMeta
from ..support.methods import abstractpedanticmethod

from .zeroable import Zeroable
from .semigroup import SemiGroup


MonoidElement_TV = typing.TypeVar('MonoidElement')


class Monoid(SemiGroup[MonoidElement_TV], Zeroable[MonoidElement_TV]):
    """
    Abstractmethods:
        append
        zero
    """
    pass
