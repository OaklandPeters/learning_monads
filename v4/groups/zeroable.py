import typing
from abc import abstractclassmethod

from ..support.typecheckable import Interface
from ..support.methods import abstractclassproperty


Element_TV = typing.TypeVar('Element_TV')


class Zeroable(typing.Generic[Element_TV], Interface):
    """In most cases, this indicates a container that can be 'empty'."""
    @abstractclassproperty
    def zero(cls) -> Element_TV:
        return NotImplemented
