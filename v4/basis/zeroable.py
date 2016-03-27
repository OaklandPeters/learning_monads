import typing

from ..support.typecheckable import TypeCheckableMeta, meets_interface
from ..support.methods import abstractclassproperty


Element_TV = typing.TypeVar('Element_TV')


# class Zeroable(typing.Generic[Element_TV], metaclass=TypeCheckableMeta):
class Zeroable(metaclass=TypeCheckableMeta):
    """In most cases, this indicates a container that can be 'empty'."""
    @abstractclassproperty
    def zero(cls) -> Element_TV:
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Zeroable:
            return meets_interface(subclass, Zeroable)
        return NotImplemented
