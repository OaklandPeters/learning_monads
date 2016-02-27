"""
Ideally - concrete implementations of morphisms should be usable in two ways:
(1) by type-checking off of objects and using classmethods to transform them,
(2) by explictly wrapping functions in the morphism type.

@todo: Make this match the decorating pattern used by @classmethod -- the __func__ in particular. @functools.wraps?
    PROBLEM: I don't see a way to replicate this. @classmethod does it, but @property and @wraps does not

Ok. Serious problem. apply seems natural on Morphism, but it also seems to be the signature of a functor.

How could Functor generate the correct of Morphism?

IGNORING MONADS FOR A MOMENT:
    ListFunctor.apply(func, alist)
    list_morphism = ListFunctor(func)

    If I want this true:
    ListFunctor.decorate(func)(element) == 

    So, somehow
    ListFunctor.decorate --> ListMorphism
    in such a way that its .apply comes from the Functor, not the Morphism

class ListFunctor(Functor):
    @classmethod
    def decorate(cls, function: 'Domain.Morphism') -> 'Codomain.Morphism':
        def wrapped(element):
            return cls.apply(function, element)
        return wrapped

    @classmethod
    def construct(cls, element: 'Domain.Element') -> 'Codomain.Element':
        return list(element)

    @classmethod
    def apply(cls, function, element):
        return [function(value) for value in element]
"""
from abc import abstractclassmethod
from collections import Callable

from ...support.methods import pedanticmethod, abstractpedanticmethod, abstractclassproperty
from ...support.typecheckable import TypeCheckableMeta, TypeCheckable



class Morphism(Callable, TypeCheckable, metaclass=TypeCheckableMeta):
    """
    Morphism needs to be able to typecheck.

    Note: because of the category laws, the Morphisms in a Category
    forms a Monoid.

    Because the Morphism should typecheck, this will likely need to override
    __instancecheck__ and __subclasscheck__

    Note: many Categories, and hence their Morphism/Elements do not correspond to directly instantiatable classes (the category might be closer to an interface or dependent type). hence, in general, we will not have a __new__ method. Instead, the ability to construct Elements/Morphisms in a category comes from Functors mapping into that category.

    Inherited abstract methods:
        __call__
        __instancecheck__
        __subclasscheck__
    """
    @abstractpedanticmethod
    def compose(cls, self: 'Morphism', other: 'Morphism') -> 'Morphism':
        return NotImplemented

    @abstractclassproperty
    def identity(cls) -> 'Morphism':
        """Return the identity morphism for this category.
        For various reasons, we are not making this a property."""
        return NotImplemented

    @abstractpedanticmethod
    def call(cls, self: 'Morphism', element: 'Element') -> 'Element':
        """Can't be written automatically, because it would depend on the way
        that the functinos are stored inside the Morphism class."""
        return NotImplemented

    def __call__(self, element: 'Element') -> 'Element':
        return self.call(element)

    def __rshift__(self, morphism: 'Morphism') -> 'Morphism':
        return self.compose(morphism)
