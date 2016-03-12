"""
In our construction, we define 'Functor' as it is used in category-theory, rather than the way it is used in Haskell.

Thus, a functor is capable of translating element *and* morphisms from one category to another.


@todo: Move examples to their own files
@todo: Change as many classmethods as possible to pedanticmethods
"""
from abc import abstractclassmethod

from ...support.methods import pedanticmethod, abstractpedanticmethod, abstractclassproperty
from ...support.typecheckable import TypeCheckableMeta
from ..category import Category, Element, Morphism


class DomainTranslator:
    @abstractclassproperty
    def Domain(cls) -> 'Category':
        return NotImplemented

    @abstractclassproperty
    def Codomain(cls) -> 'Category':
        return NotImplemented


class Decorator(DomainTranslator):
    @abstractclassmethod
    def decorate(cls, function: 'Domain.Morphism') -> 'Codomain.Morphism':
        return NotImplemented


class Constructor(DomainTranslator):
    """A functor needs to have one element constructor which is considered authoritative."""
    @abstractclassmethod
    def construct(cls, element: 'Domain.Element') -> 'Codomain.Element':
        return NotImplemented


class Applicative:
    """Not haskell's Applicative at all."""
    @abstractclassmethod
    def apply(cls, function: 'Domain.Morphism', element: 'Codomain.Element') -> 'Codomain.Morphism':
        return NotImplemented


class Functor(Decorator, Constructor, Applicative):
    """Functor.
    """



    @classmethod
    def apply(cls, function: 'Domain.Morphism', element: 'Codomain.Element') -> 'Codomain.Morphism':
        return cls.decorate(function)(element)


class FunctorCategory(Functor, Category):
    """
    A category, equipped with a canonical set of constructors/decorators.
    Classes in OOP langauges are often written this way.

    In practical terms, this allows the Category define __init__/__new__ behavior for the
    category as reasonable defaults, while still allowing alternate constructors to exist
    (such as when mapping from a different Category).

    For the OOP approach, the Functor almost always maps: 

    Note: Monads will generally be written as FunctorCategories + extra structure.
    """




# ======================================
#  Inheritance patterns/mixin-routes
# ======================================
class Functor_From(Functor):
    @classmethod
    def apply(cls, function: 'Domain.Morphism', element: 'Codomain.Element') -> 'Codomain.Morphism':
        return cls.decorate(function)(element)



class Functor_FromApplicative(Constructor, Functor):
    """From apply
    """
    @classmethod
    def decorate(cls, function: 'Domain.Morphism') -> 'Codomain.Morphism':
        def wrapped(element):
            return cls.apply(function, element)
        return wrapped

    @abstractclassmethod
    def apply(cls, function: 'Domain.Morphism', element: 'Codomain.Element') -> 'Codomain.Element':
        return NotImplemented


# ======================================
#    Examples
# ======================================
class StandardCategory:
    """Stub. Will need to be a metaclass thing later."""
    def __new__(cls, element, morphism):
        class _Category(Category):
            Element = element
            Morphism = morphism
        return _Category


class ListFunctor(Functor):
    Domain = StandardCategory(Any, Callable[[Any], Any])
    Codomain = StandardCategory(list, Callable[[list], list])

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





class MaybeFunctor(Functor):
    """
    This could be constructed various ways. Haskellish is to define MaybeElement = Just|Nothing
    """
    NullType = type(None)  # for monad, this becomes Nothingelement


    @classmethod
    def apply(cls, function, element):
        if isinstance(element, cls.NullType):
            return element
        else:
            return function(element)


