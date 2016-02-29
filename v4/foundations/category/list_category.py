"""
Example category. Doubles as unit-test of Category, Element, Morphism

One version made with StandardCategory, and one done the verbose way,
so unit-tests can work on it.


THIS DOESNOT QUITE WORK
    ListMorphism.compose has no way return a composed object that is also a ListMorphism


LONG-TERM MUDDLE:
    Between structural-typed/inclusive typed Category/Element/Morphism, and actually
    instantiated class for Category

TRY:
    Using the structural one
    !! So, ListElement should probably be considered a virtual superclass of list
"""
from typing import Callable

from ...support.methods import classproperty, pedanticmethod

from .category import Category
from .element import Element
from .morphism import Morphism


ListCallable = Callable[[list], list]


class ListElement(list, Element):
    """
    """
    @pedanticmethod
    def apply(cls, self, morphism):
        return morphism(self)


def list_identity(_list):
    return _list


class ListMorphism(Morphism):
    @classproperty
    def identity(cls):
        return list_identity

    @pedanticmethod
    def call(cls, self, element):
        return self(element)

    @pedanticmethod
    def compose(cls, self, other):
        def composed(value):
            return other(self(value))
        return composed

    def __call__(self, element):
        return self(element)


class ListCategory(Category):
    Element = ListElement
    Morphism = ListMorphism


# =======================================
#     SimpleList version
#   constructed just to test simple.py
# =======================================
from .simple import SimpleCategory, SimpleElement, SimpleMorphism

SimpleListElement = SimpleElement('SimpleListElement', list)
SimpleListMorphism = SimpleMorphism('SimpleListMorphism', ListCallable)
SimpleListCategory = SimpleCategory('SimpleListCategory', SimpleListElement, SimpleListMorphism)
SimpleListCategory2 = SimpleCategory('SimpleListCategory2', list, ListCallable)
