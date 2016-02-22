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

from ...support.methods import pedanticmethod, abstractpedanticmethod, abstractclassproperty
from ...support.typecheckable import TypeCheckableMeta


class Morphism(metaclass=TypeCheckableMeta):
    def __init__(self, function):
        self.function = function

    @abstractclassproperty
    def Category(cls):
        return NotImplemented

    @abstractpedanticmethod
    def apply(cls, function, element):
        """
        For monads, constructing this is almost definitional
        """
