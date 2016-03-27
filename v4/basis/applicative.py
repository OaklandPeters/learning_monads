import typing

from ..support.typecheckable import TypeCheckableMeta, meets_interface
from ...support.methods import abstractpedanticmethod


Element_TV = typing.TypeVar('Element_TV')
Morphism_TV = typing.TypeVar('Morphism_TV')


# class Applicative(typing.Generic[Element_TV, Morphism_TV], metaclass=TypeCheckableMeta):
class Applicative(metaclass=TypeCheckableMeta):
    @abstractpedanticmethod
    def apply(cls, element: Element_TV, morphism: Morphism_TV) -> Element_TV:
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Applicative:
            return meets_interface(subclass, Applicative)
        return NotImplemented
