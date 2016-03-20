import typing

from ..support.typecheckable import TypeCheckableMeta, meets_interface
from ..support.methods import abstractpedanticmethod


Element_TV = typing.TypeVar('Element_TV')


class Appendable(typing.Generic[Element_TV], metaclass=TypeCheckableMeta):
    """
    Binary function which is total in the elements of the space.
    What this means is that it can operate on any two elements defined
    in that space, and returns another element inside the same space.
    """
    @abstractpedanticmethod
    def append(cls, self: Element_TV, other: Element_TV) -> Element_TV:
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Appendable:
            return meets_interface(subclass, Appendable)
        return NotImplemented
