"""
This constrasts with my construction of Cateogry elsewhere, but this more
strictly follows the group-theory hierarchy.
"""
import typing

from .identifiable import Identifiable
from .composable import Composable


CategoryMorphism_TV = typing.TypeVar('CategoryMorphism_TV')


class Category(Composable[CategoryMorphism_TV], Identifiable[CategoryMorphism_TV]):
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
    pass
