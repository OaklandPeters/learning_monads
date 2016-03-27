"""
This constrasts with my construction of Cateogry elsewhere, but this more
strictly follows the group-theory hierarchy.
"""
import typing

from ..support.typecheckable import meets_interface

from ..basis.identifiable import Identifiable
from ..basis.composable import Composable
from ..foundations.space.space import Space


Morphism = typing.TypeVar('Morphism')


# Removing Generic types, until I can get that to work with metaclass=TypeCheckableMeta
# class Category(Composable[Morphism],
#                Identifiable[Morphism]):
class Category(Composable, Identifiable, Space):
    """
    The primary object we will work with - after we equip it with four more
    attributes:
        Call
        Apply
        Element
        Morphism


    Abstractmethods:
        compose
        identity
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is Category:
            return meets_interface(subclass, Category)
        return NotImplemented
