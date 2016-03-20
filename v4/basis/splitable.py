import typing

from ..support.typecheckable import TypeCheckableMeta, meets_interface
from ..support.methods import abstractpedanticmethod


Element_TV = typing.TypeVar('Element_TV')


class Splittable(typing.Generic[Element_TV], metaclass=TypeCheckableMeta):
    """
    split is nearly always used as the inversion of compose
    """
    @abstractpedanticmethod
    def split(cls, self: 'Element_TV') -> 'typing.Tuple[Element_TV, Element_TV]':
        """
        Split an Element into two seperate Elements. In the case that this
        was a stack of wrapped Elements, the return is something like:
            first, rest = split(wrapped_Elements)
        """
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Splittable:
            return meets_interface(subclass, Splittable)
        return NotImplemented
