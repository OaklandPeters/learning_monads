"""
Difference in terms:
----------------------
In category-theory, what is called the *objects* in a category, we are calling the *elements* of a category - to prevent name-collusions (and confusions) with Pythons builtin 'object' class.
Note - Python's 'object' class, actually forms the 'elements' for the category of all objects representable in Python (which I'm calling Pysk).

"""
from ...support.typecheckable import TypeCheckableMeta, meets
from ...support.methods import abstractclassproperty

from .element import Element
from .morphism import Morphism


class Category(metaclass=TypeCheckableMeta):
    """
    AbstractBaseClass for categories.
    """
    @abstractclassproperty
    def Element(cls) -> Element:
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls) -> Morphism:
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Category:
            return meets(C, cls.__abstractmethods__)
        return NotImplemented


def is_in_category(obj, category):
    return isinstance(obj, category.Element) or isinstance(obj, category.Morphism)
