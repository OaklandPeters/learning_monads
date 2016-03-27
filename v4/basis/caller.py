import typing

from ..support.typecheckable import TypeCheckableMeta, meets_interface
from ...support.methods import abstractpedanticmethod


Element_TV = typing.TypeVar('Element_TV')
Morphism_TV = typing.TypeVar('Morphism_TV')


# class Caller(typing.Generic[Element_TV, Morphism_TV], metaclass=TypeCheckableMeta):
class Caller(metaclass=TypeCheckableMeta):
    @abstractpedanticmethod
    def call(cls, self: Morphism_TV, element: Element_TV) -> Element_TV:
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Caller:
            return meets_interface(subclass, Caller)
        return NotImplemented
