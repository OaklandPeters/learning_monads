"""
Defines helpers to make working with, and defining, 
Categories, Elements, and Morphisms much easier.

The intention is that typing-like __getitem__ behavior will be used
to define standard simple categories.


DESIRE: that these work
ListElement = StandardElement[list]
ListMorphism = StandardElement[Callable[[list], list]]
class ListCategory(StandardCategory):
    Element = StandardElement[list]
    Morphism = StandardElement[Callable[[list], list]]

! To do this, look at the way that various classes & their metas work in typing.py

"""
from typing import TypeVar, Generic, TypingMeta, Final

from category import Element, Morphism, Category
from support_pre import pedanticmethod


MorphismType = TypeVar('MorphismType', bound=Morphism)
ElementType = TypeVar('ElementType', bound=Element)
CategoryType = TypeVar('CategoryType', bound=Category)


def _identity(element):
    return element


class StandardMorphismMeta(TypingMeta):
    pass
    # def __new__
    # def __repr__
    # def __getitem__()


# class StandardMorphism(Morphism, Final, metaclass=StandardMorphismMeta, _root=True):
class StandardMorphism(Morphism, Generic[MorphismType]):
    """
    The identity, compose and call functions for most Morphisms are the same.
    """
    @classmethod
    def identity(cls) -> MorphismType:
        return _identity

    @pedanticmethod
    def compose(cls, self, other):
        def composed(element):
            return other.call(self.call(element))
        return composed

    @classmethod
    def __instancecheck__(cls, instance):
        return isinstance(instance, cls._reference_type_)

    @classmethod
    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, cls._reference_type_)


class StandardElementMeta(TypingMeta):
    pass
    # def __new__
    # def __repr__
    # def __getitem__()


# class StandardElement(Morphism, Final, metaclass=StandardMorphismMeta, _root=True):
class StandardElement(Element, Generic[ElementType]):
    pass


class StandardCategoryMeta(TypingMeta):
    pass
    # def __new__
    # def __repr__
    # def __getitem__()


# class StandardCategory(Category, Final, metaclass=StandardCategoryMeta, _root=True):
class StandardCategory(Category, Generic[CategoryType]):
    pass
