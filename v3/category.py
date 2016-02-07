"""
@todo: See if pedanticmethod can be composed with abstractmethod

Next-steps:
* Bring in HigherKindedTypeVar, so Domain.Morphism is sensible

CHANGE IT: see if I can prevent Category from being a metaclass. Reason: I would like Monad to be a child of Category

"""
import typing
from abc import abstractmethod, abstractproperty, ABCMeta

from support_pre import classproperty, abstractclassproperty, TypeCheckableMeta, pedanticmethod



class Morphism:
    """
    Essentially, functions which map elements within a category.

    Classes inheriting from this should use a metaclass that is a child of Category.
    In Haskell, the Identity and compose are located on Category.
    For sensibility, we locate it here on Morphism.

    Laws:
        Identity
        Composition
    """
    @abstractclassproperty
    def Category(cls):
        """This should be set by the metaclass."""
        return NotImplemented

    @abstractclassproperty
    def Identity(cls) -> 'Morphism':
        return NotImplemented

    @abstractmethod
    @pedanticmethod
    def compose(cls, self: 'Morphism', other: 'Morphism') -> 'Morphism':
        return NotImplemented

    @abstractmethod
    @pedanticmethod
    def collapse(cls, self: 'Morphism') -> 'Morphism':
        """This is hypothetical. I'm not sure it's needed or correct.
        But.... my intuition is strong about this one.
        However... I'm not sure if it should accept an element/argument or not (so it can __call__ the elements first).
            (so the signature might be differnet)
        """
        return NotImplemented

    @abstractmethod
    def __call__(self, element):
        return NotImplemented


class Identity(Morphism):
    pass


class Element:
    """
    Classes inheriting from this should use a metaclass that is a child of Category.
    """
    @abstractclassproperty
    def Category(cls):
        """This should be set by the metaclass."""
        return NotImplemented




class Category(TypeCheckableMeta):
    """Metaclass.

    Note: the metaclass's __call__ gets called just before the class's __init__... might be useful

    UNSOLVED: How to make everything implementing a category be registered as belonging to it.
        So it will have a 'Category' property

    Uncertain question: should Morphism implement identity/compose/collapse, or should Category?

    @todo: Determine if there is a way to auto-register Morphism/Element with this
    """
    def __new__(mcls, name, bases, namespace):
        cls = super(Category, mcls).__new__(mcls, name, bases, namespace)
        mcls.register(cls)
        return cls

    @classmethod
    def register(mcls, cls):
        """
        This is the work horse that makes a lot of magic happen, and it prevents
        the cyclic dependencies.

        Everything using a Category metaclass, ends up with .Category method
        pointing to the category.
        """
        cls.Category = mcls


    @abstractclassproperty
    def Morphism(mcls):
        return NotImplemented

    @abstractclassproperty
    def Element(mcls):
        return NotImplemented


class Functor(typing.Generic[Codomain, Domain]):
    """Maps functions from the Domain to the Codomain. Note, this Functor class cannot actually map elements (that requires Applicative).

    Functor is not instanced.

    NOTE: to 'lift' a morphism, use fmap

    UNSURE: Whether to require f_apply or f_map to be implemented.
        +f_map: acts as lift, so useful in more situations
        +f_apply: simpler to write
    """
    @abstractclassproperty
    def Domain(cls) -> Category:
        """Input type."""
        pass

    @abstractclassproperty
    def Codomain(cls) -> Category:
        """Output type."""
        pass


    @abstractmethod
    @classmethod
    def f_lift(cls, function: 'cls.Codomain.Morphism') -> Codomain.Element:
        """Translate a function."""

    @abstractmethod
    @pedanticmethod
    def f_apply(cls, self: Codomain.Element, function: Domain.Morphism) -> Codomain.Element:
        """Usually it is easier to write f_apply than f_map.
        """
        # return NotImplemented
        # return cls.f_map(function)()

    @abstractmethod
    @classmethod
    def f_map(cls, function: Domain.Morphism) -> Codomain.Morphism:
        """Basically 'lift' for morphism.
        Should more or less just: return Morphism(function)
        """
        return NotImplemented
        # def wrapper(element):
        #     return element.f_apply(function)
        # return cls(wrapper)



class Applicative(Functor):
    """
    NOTE: to 'lift' an element, use 'lift'
    Applicative itself is not instanced.
    """
    @abstractmethod
    @classmethod
    def lift(cls, value: cls.Domain.Element) -> cls.Codomain.Element:
        pass

    @abstractmethod
    @pedanticmethod
    def a_apply(cls, self: Codomain.Element, morphism: Codomain.Morphism) -> Codomain.Element:
        pass


class Monad(Applicative, Category):
    """
    Monad is a type of functor which itself comprises a Category. So there are three related categories:
        Domain, Codomain, and Monad categories

    NOT SURE IF: I'll have this involve Monoid for the elements or not.

    NOTE: A Monad itself is a Category. So, there are (potentially) three Categories related to a Monad. In practice, usually two of these domains are the same. For example, for Monads that are meant to be used as data-structures, such as List, the Codomain is usually the 


    REALIZATION OF PROBLEM:
        There is a schism in meaning between the methods on Applicative and Monad.
        If Applicative.a_apply return the Codomain
        And you build a Monad on top of that Applicative
        The Monad.a_apply should return the Codomain, but it feels like it should return the monadic domain.

        So there is a big problem:
            Building up Functor -> Applicative -> Monad incrementally.
    """
    @abstractmethod
    def f_map(cls, function: 'cls.Domain.Function') -> 'cls.Morphism':
        return NotImplemented

    @abstractmethod
    def f_apply(cls, element: 'cls.Element', function: 'cls.Domain.Morphism') -> 'cls.Element':
        return NotImplemented

    @abstractmethod
    def a_map(cls, function: 'cls.Morphism'):
        return NotImplemented


class MonadElement(Morphism):
    """
    Morphisms and Elements in the category of a Monad also express the monadic methods
    """
    @abstractclassproperty
    def Category(cls) -> 'Monad':
        return NotImplemented

    @


class MonadMorphism(Morphism):
    """
    Morphisms and Elements in the category of a Monad also express the monadic methods
    """
    @abstractclassproperty
    def Category(cls) -> 'Monad':
        return NotImplemented









class PoliteMonad(Monad, Category, Monoid, Fixed, Traversable, Comonad):
    """
    Extremely well-behaved monad that supports basically all the useful functionality.
    Fixed: recursive behavior
    Monoid: monadplus behavior
    Traversable/Comonad/Fixed: These bheavior smight imply one another
    """
