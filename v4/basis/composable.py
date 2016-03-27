import typing

from ..support.typecheckable import TypeCheckableMeta, meets_interface
from ..support.methods import abstractpedanticmethod


Morphism_TV = typing.TypeVar('Morphism_TV')


# class Composable(typing.Generic[Morphism_TV], metaclass=TypeCheckableMeta):
class Composable(metaclass=TypeCheckableMeta):
    """
    Non-total binary function on morphisms in the space. In this case, non-total
    means that not every two morphisms can be meaningfully composed (IE their
    signatures may not match up).

    I'm pre-emptively violating strict group-theory with this function - by
    saying it is used for composing morphisms. Strict group theory would say
    that it could be any non-total binary function on elements.
    """
    @abstractpedanticmethod
    def compose(cls, self: Morphism_TV, other: Morphism_TV) -> Morphism_TV:
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Composable:
            return meets_interface(subclass, Composable)
        return NotImplemented
