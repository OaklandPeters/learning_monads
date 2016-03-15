import typing
from abc import abstractclassmethod

from ..support.typecheckable import Interface
from ..support.methods import abstractclassproperty


Morphism_TV = typing.TypeVar('Morphism_TV')


class Identifiable(typing.Generic[Morphism_TV], Interface):
    """In most cases, this indicates a container that can be 'empty'."""
    @abstractclassproperty
    def identity(cls) -> Morphism_TV:
        return NotImplemented
