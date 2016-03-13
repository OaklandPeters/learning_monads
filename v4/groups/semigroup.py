"""
Semigroup (used by Monoids) is very similar to Semigroupoid (used by Categories),
except for one very crucial difference. Semigroups, and therefore Monoids, are
total - meaning that their binary operation can be applied on *any* two
elements.

For example, with IntegerAddition (a monoid) you can add any two
integers together. However, in Pysk, the Category of composing Python functions,
not all functions can be composed - for example: a function on integers and a
function on strings.
"""
import typing

from ..support.typecheckable import Interface
from ..support.methods import abstractpedanticmethod


Element_TV = typing.TypeVar('Element_TV')


class SemiGroup(typing.Generic[Element_TV], Interface):
    @abstractpedanticmethod
    def append(self, other: 'Element_TV') -> 'Element_TV':
        return NotImplemented
