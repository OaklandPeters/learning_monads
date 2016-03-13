import typing

from ..support.typecheckable import Interface
from ..support.methods import abstractpedanticmethod


Morphism_TV = typing.TypeVar('Morphism_TV')


class Decomposable(typing.Generic[Morphism_TV], Interface):
    """
    decompose is nearly always used as the inversion of compose
    """
    @abstractpedanticmethod
    def decompose(cls, self: 'Morphism_TV') -> 'typing.Tuple[Morphism_TV, Morphism_TV]':
        """
        Decompose a morphism into two seperate morphisms. In the case that this
        was a stack of wrapped morphisms, the return is something like:
            first, rest = decompose(wrapped_morphisms)
        """
        return NotImplemented
