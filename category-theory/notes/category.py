
from typing import TypeVar, Generic
from abc import abstractclassmethod
from collections.abc import Callable

from ..python.support_pre import abstractclassproperty, abstractpedanticmethod, pedanticmethod
from ..python.typecheckable import TypeCheckableMeta


class Categorized(metaclass=TypeCheckableMeta):
    @abstractclassproperty
    def Category(cls) -> 'Category':
        return NotImplemented


class Morphism(Callable, Categorized, metaclass=TypeCheckableMeta):
    """
    Morphism needs to be able to typecheck.

    Note: because of the category laws, the Morphisms in a Category
    forms a Monoid.

    Because the Morphism should typecheck, this will likely need to override
    __instancecheck__ and __subclasscheck__

    Note: many Categories, and hence their Morphism/Elements do not correspond to directly instantiatable classes (the category might be closer to an interface or dependent type). hence, in general, we will not have a __new__ method. Instead, the ability to construct Elements/Morphisms in a category comes from Functors mapping into that category.

    """
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

    # Used for type or value checking
    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented

    @abstractclassmethod
    def __subclasscheck__(cls, subclass):
        return NotImplemented

    # Morphism forms a monoid
    @pedanticmethod
    def append(cls, self: 'Monoid', other: 'Monoid'):
        return cls.compose(self, other)

    @classmethod
    def zero(cls):
        return cls.identity()



class Element(Categorized, metaclass=TypeCheckableMeta):
    @abstractclassmethod
    def __new__(cls, value):
        """Unsafe lifting operation.
        Wraps a function as a Morphism of this type.
        There is often no reasonable to gaurantee that it actually
        is a Morphism in this category"""
        return NotImplemented

    def apply(self, morphism: Morphism) -> 'Element':
        return NotImplemented

    # Used for type or value checking
    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented

    @abstractclassmethod
    def __subclasscheck__(cls, subclass):
        return NotImplemented


ElementTV = TypeVar('ElementTV', bound=Element)
MorphismTV = TypeVar('MorphismTV', bound=Morphism)


class Category(Generic[ElementTV, MorphismTV], metaclass=TypeCheckableMeta):
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

    # Used for type or value checking
    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented

    @abstractclassmethod
    def __subclasscheck__(cls, subclass):
        return NotImplemented
