

import typing
from abc import abstractmethod


FoldableInType = typing.TypeVar('FoldableInType')
FoldableOutType = typing.TypeVar('FoldableOutType')


class Foldable:
    @abstractmethod
    def foldr(self,
              function: typing.Callable[FoldableInType, FoldableOutType],
              accumulator: FoldableOutType) -> FoldableOutType:
        return NotImplemented


class Monoid:
    @abstractclassmethod
    def zero(cls):
        return NotImplemented

    @abstractmethod
    def append(self, other):
        return NotImplemented


class Reducable(Foldable, Monoid):

    def reduceMap(self, function: Reducer) -> Reducable:
        return self.foldr(function, self.zero())

    def reduce(cls):
        return self.foldr(self.append, self.zero())


class Categorized:
    @abstractclassproperty
    def Category(cls) -> 'Category':
        return NotImplemented


class Morphism(typing.Callable, Categorized):
    @abstractclassmethod
    def __new__(cls, function: Callable):
        """Unsafe lifting operation.
        Wraps a function as a Morphism of this type.
        There is often no reasonable to gaurantee that it actually
        is a Morphism in this category"""
        return NotImplemented

    def compose(self, other) -> Morphism:
        return self.Category.compose(self, other)

    def call(self, element: Element) -> Element:
        return self.Category.call(self, element)


class Element(Categorized):
    @abstractclassmethod
    def __new__(cls, value):
        """Unsafe lifting operation.
        Wraps a function as a Morphism of this type.
        There is often no reasonable to gaurantee that it actually
        is a Morphism in this category"""
        return NotImplemtned

    def apply(self, morphism: Morphism):
        return 

class Category(typing.Generic[Element, Morphism]):
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


Domain = typing.TypeVar('Domain', bound=Category)
Codomain = typing.TypeVar('Codomain', bound=Category)


class Functor(typing.Generic[Domain, Codomain]):
    @abstractmethod
    def map(cls, function: Domain.Morphism) -> Codomain.Morphism:
        return NotImplemented


