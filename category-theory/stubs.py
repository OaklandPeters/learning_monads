"""
This version of the typeclasses does not have the mixin methods or the utility functions included.
They definately *should* be, especially in regard to expressing those in terms of the standard magic methods.

However, this is just a stub.

@todo: Create seperate files for each typeclass
@todo: Mixin methods
@todo: Utility functions
@todo: Generic functions
@todo: Laws for each type class, in text and unit-test form.
@todo: Determine if monoid should include 'join' (I don't recall if it is implied or not)
@todo: Handle the fact that Monoid is defined on 1 typevar, and foldable on 2. How to combine these in multiple inheritance?
"""

from typing import TypeVar, Generic
from abc import abstractmethod, abstractclassmethod
from collections import Callable

from support_pre import abstractclassproperty, abstractpedanticmethod, pedanticmethod



# ===============================
#     Category-theoretic
#        structures
# ===============================

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

    def apply(self, morphism: Morphism) -> 'Element':
        return NotImplemented


ElementTV = TypeVar('ElementTV', bound=Element)
MorphismTV = TypeVar('MorphismTV', bound=Morphism)


class Category(Generic[ElementTV, MorphismTV]):
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
    def compose(cls, left: MorphismTV, right: MorphismTV) -> MorphismTV:
        """Some categories may override this, but we are providing
        a default definition, since it will be the most common one.
        When this is overridden, it is usually in an Arrow Category."""
        def wrapper(element):
            return right(left(element))
        return cls.Morphism(wrapper)

    @classmethod
    def apply(cls, element: ElementTV, morphism: MorphismTV) -> ElementTV:
        return morphism(element)

    @classmethod
    def call(cls, morphism: MorphismTV, element: ElementTV) -> ElementTV:
        return morphism(element)



# ===============================
#   Functor and Monad
# ===============================

Domain = TypeVar('Domain', bound=Category)
Codomain = TypeVar('Codomain', bound=Category)
MonadCategory = TypeVar('MonadCategory', bound=Category)


class Functor(Generic[Domain, Codomain]):
    @abstractclassmethod
    def map_morphism(cls, function: 'Domain.Morphism') -> 'Codomain.Morphism':
        """fmap"""
        return NotImplemented


class Applicative(Functor):
    @abstractclassmethod
    def map_element(cls, value: 'Domain.Element') -> 'Codomain.Element':
        return NotImplemented


class MonadIn(Applicative[Domain, MonadCategory]):
    @abstractclassmethod
    def lift(cls):
        return NotImplemented


class MonadOut(Applicative[MonadCategory, Codomain]):
    @abstractpedanticmethod
    def bind(cls, self, function):
        return NotImplemented


class Monad(MonadIn[Domain, MonadCategory], MonadOut[MonadCategory, Codomain]):
    pass

#class Monad(Applicative):
#    @abstractclassmethod
#    def lift(cls):
#        return NotImplemented

#    @abstractclassmethod
#    def bind(cls, function):
#        return NotImplemented


# ===============================
#   Group-theory classes
# 
# ===============================

InType = TypeVar('InType')
OutType = TypeVar('OutType')
Element = TypeVar('Element')

class Foldable(Generic[InType, OutType]):
    @abstractpedanticmethod
    def foldr(cls,
              self: 'Foldable[InType, OutType]',
              function: Callable[[InType], OutType],
              initial: OutType) -> OutType:
        """
        The initial is also used as the accumulator."""
        return NotImplemented


class Zeroable:
    """In most cases, this indicates a container that can be 'empty'."""
    @abstractclassmethod
    def zero(cls):
        return NotImplemented


class SemiGroup(Generic[Element]):
    @abstractpedanticmethod
    def append(self, other: 'SemiGroup[Element]') -> 'SemiGroup[Element]':
        return NotImplemented


class Monoid(Zeroable, SemiGroup):
    @classmethod
    def flatten(cls, foldable: Foldable):
        """Fold a structure, using the rules of this monoid.
        Haskell calls this 'mconcat'.
        sum = lambda foldable_list_of_ints: AdditionMonoid.flatten(foldable_list_of_ints)
        """
        return foldable.foldr(cls.append, cls.zero())


class Reducable(Foldable, Zeroable):
    @pedanticmethod
    def reduce(cls, self, function):
        return cls.foldr(self, function, cls.zero())


class Joinable(Foldable, Zeroable, SemiGroup):
    @pedanticmethod
    def join(cls, self):
        """Uses the natural append operation of a monoid in a foldr.
        Haskell calls this 'fold'."""
        return cls.foldr(self, cls.append, cls.zero())


class Monoid(Zeroable, SemiGroup):
    @abstractclassmethod
    def zero(cls) -> 'Monoid[Element]':
        return NotImplemented

    @abstractmethod
    def append(self, other: 'Monoid[Element]') -> 'Monoid[Element]':
        return NotImplemented
