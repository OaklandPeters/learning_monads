import typing

from ..support.typecheckable import Interface
from ..support.methods import abstractpedanticmethod


Morphism_TV = typing.TypeVar('Morphism_TV')


class Composable(typing.Generic[Morphism_TV], Interface):
    @abstractpedanticmethod
    def compose(cls, self: Morphism_TV, other: Morphism_TV) -> Morphism_TV:
        return NotImplemented
