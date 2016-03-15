import typing

from ..support.typecheckable import Interface
from ..support.methods import abstractpedanticmethod


Element_TV = typing.TypeVar('Element_TV')


class Splitable(typing.Generic[Element_TV], Interface):
    """
    truncate is nearly always used as the inversion of compose
    """
    @abstractpedanticmethod
    def split(cls, self: 'Element_TV') -> 'typing.Tuple[Element_TV, Element_TV]':
        """
        Split an Element into two seperate Elements. In the case that this
        was a stack of wrapped Elements, the return is something like:
            first, rest = split(wrapped_Elements)
        """
        return NotImplemented
