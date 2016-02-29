"""
Difference in terms:
----------------------
In category-theory, what is called the *objects* in a category, we are calling the *elements* of a category - to prevent name-collusions (and confusions) with Pythons builtin 'object' class.
Note - Python's 'object' class, actually forms the 'elements' for the category of all objects representable in Python (which I'm calling Pysk).
"""
from ...support.methods import abstractpedanticmethod
from ...support.typecheckable import TypeCheckableMeta, TypeCheckable, meets

from .basis import Applicative


class Element(Applicative, TypeCheckable, metaclass=TypeCheckableMeta):
    """
    Abstract methods:
        apply
        __instancecheck__
        __subclasscheck__
    """
    def __rshift__(self, morphism: 'Morphism') -> 'Element':
        return self.apply(morphism)

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Element:
            return meets(C, cls.__abstractmethods__)
        return NotImplemented
