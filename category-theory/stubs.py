"""
This version of the typeclasses does not have the mixin methods or the utility functions included.
They definately *should* be, especially in regard to expressing those in terms of the standard magic methods.

However, this is just a stub.

@todo: Create seperate files for each typeclass
@todo: Mixin methods
@todo: Utility functions
@todo: Generic functions
@todo: Laws for each type class, in text and unit-test form.
"""

from typing import Callable, TypeVar, Generic
from abc import abstractmethod

from support_pre import abstractclassproperty, abstractclassmethod


FoldableInType = TypeVar('FoldableInType')
FoldableOutType = TypeVar('FoldableOutType')


class Foldable(Generic[FoldableInType, FoldableOutType]):
    @abstractmethod
    def foldr(self,
              function: Callable[FoldableInType, FoldableOutType],
              accumulator: FoldableOutType) -> FoldableOutType:
        return NotImplemented


MonoidElement = TypeVar('MonoidElement')


class Monoid(Generic[MonoidElement]):
    @abstractclassmethod
    def zero(cls) -> 'Monoid[MonoidElement]':
        return NotImplemented

    @abstractmethod
    def append(self, other: 'Monoid[MonoidElement]') -> 'Monoid[MonoidElement]':
        return NotImplemented


ReducibleElement = TypeVar('ReducibleElement')

class Reducible(Foldable, Monoid):

    def reduceMap(self, function: Callable[ReducibleElement, ReducibleElement]) -> 'Reducible[ReducibleElement]':
        return self.foldr(function, self.zero())

    def reduce(self):
        return self.foldr(self.append, self.zero())


class Categorized:
    @abstractclassproperty
    def Category(cls) -> 'Category':
        return NotImplemented


class Morphism(Callable, Categorized):
    @abstractclassmethod
    def __new__(cls, function: Callable):
        """Unsafe lifting operation.
        Wraps a function as a Morphism of this type.
        There is often no reasonable to gaurantee that it actually
        is a Morphism in this category"""
        return NotImplemented

    def compose(self, other) -> 'Morphism':
        return self.Category.compose(self, other)

    def __call__(self, element: 'Element') -> 'Element':
        return self.Category.call(self, element)


class Element(Categorized):
    @abstractclassmethod
    def __new__(cls, value):
        """Unsafe lifting operation.
        Wraps a function as a Morphism of this type.
        There is often no reasonable to gaurantee that it actually
        is a Morphism in this category"""
        return NotImplemented

    def apply(self, morphism: Morphism):
        return NotImplemented


class Category(Generic[Element, Morphism]):
    """
    Query: can morphisms map elements to morphisms? I suspect not.
    """
    @abstractclassproperty
    def Element(cls):
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls):
        return NotImplemented

    @classmethod
    def compose(cls, left: Morphism, right: Morphism) -> Morphism:
        """Some categories may override this, but we are providing
        a default definition, since it will be the most common one.
        When this is overridden, it is usually in an Arrow Category."""
        def wrapper(element):
            return right(left(element))
        return cls.Morphism(wrapper)

    @classmethod
    def apply(cls, element: Element, morphism: Morphism) -> Element:
        return morphism(element)

    @classmethod
    def call(cls, morphism: Morphism, element: Element) -> Element:
        return morphism(element)


Domain = TypeVar('Domain', bound=Category)
Codomain = TypeVar('Codomain', bound=Category)


class Functor(Generic[Domain, Codomain]):
    @abstractclassmethod
    def map_morphism(cls, function: Domain.Morphism) -> Codomain.Morphism:
        return NotImplemented


class Applicative(Functor):
    @abstractclassmethod
    def map_element(cls, value: Domain.Element) -> Codomain.Element:
        return NotImplemented




class Monad(Applicative):
    @abstractclassmethod
    def lift_element(cls):
        return NotImplemented

    

    @abstractclassmethod
    def bind(cls, function):
