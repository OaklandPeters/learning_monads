import typing

from ..support.typecheckable import TypeCheckableMeta, meets_interface
from ..support.methods import abstractclassproperty


Morphism_TV = typing.TypeVar('Morphism_TV')


class Identifiable(typing.Generic[Morphism_TV], metaclass=TypeCheckableMeta):
    """In most cases, this indicates a container that can be 'empty'."""
    @abstractclassproperty
    def identity(cls) -> Morphism_TV:
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Identifiable:
            return meets_interface(subclass, Identifiable)
        return NotImplemented
