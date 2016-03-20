"""
This constrasts with my construction of Cateogry elsewhere, but this more
strictly follows the group-theory hierarchy.
"""
import typing

from ..support.typecheckable import meets_interface

from .identifiable import Identifiable
from .composable import Composable


Morphism = typing.TypeVar('Morphism')


class Category(Composable[Morphism],
               Identifiable[Morphism]):
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
