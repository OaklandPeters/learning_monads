"""
"""
import typing

from ..support.typecheckable import meets_interface

from .zeroable import Zeroable
from .Appendable import Appendable


Element = typing.TypeVar('MonoidElement')


class Monoid(Appendable[Element],
             Zeroable[Element]):
    """
    Abstractmethods:
        append
        zero
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Monoid:
            return meets_interface(subclass, Monoid)
        return NotImplemented
