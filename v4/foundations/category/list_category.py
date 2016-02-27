"""
Example category. Doubles as unit-test of Category, Element, Morphism

One version made with StandardCategory, and one done the verbose way,
so unit-tests can work on it.
"""
from typing import Callable

from ...support.methods import classproperty, pedanticmethod

from .category import Category
from .element import Element
from .morphism import Morphism


class ListElement(list, Element):
    """
    """
    @pedanticmethod
    def apply(cls, self, morphism):
        return morphism(self)


def list_identity(_list):
    return _list

class ListMorphism(Callable[list, list], Morphism):
    @classproperty
    def identity(cls):
        return list_identity

    @pedanticmethod
    def call(cls, self, element):
        return 

    def __call__(self, element):
        return self(element)

class ListCategory(Category):
    pass



# =======================================
#     SimpleList version
#   constructed just to test simple.py
# =======================================
from .simple import SimpleCategory, SimpleElement, SimpleMorphism

SimpleListElement = SimpleElement('SimpleListElement', list)
SimpleListMorphism = SimpleMorphism('SimpleListMorphism', Callable[[list], list])
SimpleListCategory = SimpleCategory('SimpleListCategory', SimpleListElement, SimpleListMorphism)
SimpleListCategory2 = SimpleCategory('SimpleListCategory2', list, Callable[[list], list])
