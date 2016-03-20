"""
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
    """
    Morphism needs to be able to typecheck.

    Note: because of the category laws, the Morphisms in a Category
    forms a Monoid.

    Because the Morphism should typecheck, 
    """
    @abstractclassmethod
    def __new__(cls, function: Callable):
        """Unsafe lifting operation.
        Wraps a function as a Morphism of this type.
        There is often no reasonable way to gaurantee that it actually
        is a Morphism in this category"""
        return NotImplemented

    @abstractpedanticmethod
    def compose(cls, self, other) -> 'Morphism':
        return NotImplemented

    @abstractclassmethod
    def identity(cls) -> 'Morphism':
        """Return the identity morphism for this category.
        For various reasons, we are not making this a property."""
        return NotImplemented

    @abstractpedanticmethod
    def call(cls, self: 'Morphism', element: 'Element'):
        """Can't be written automatically, because it would depend on the way
        that the functinos are stored inside the Morphism class."""
        return NotImplemented

    def __call__(self, element: 'Element') -> 'Element':
        return self.call(element)

    # Morphism forms a monoid
    @pedanticmethod
    def append(cls, self: 'Monoid', other: 'Monoid'):
        return cls.compose(self, other)

    @classmethod
    def zero(cls):
        return cls.identity()

def _identity(element):
    return element

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
    """
    > In Haskell, the Monoid typeclass (not to be confused with Monad) is a class for types which have a single most natural operation for combining values, together with a value which doesn't do anything when you combine it with others (this is called the identity element). It is closely related to the Foldable class, and indeed you can think of a Monoid instance declaration for a type m as precisely what you need in order to fold up a list of values of m.
    """
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

"""

class Foldable
