"""

Todo:
* Make CategoryBase abstracts, and have Monoid, Morphism, and Element inherit from it

"""
import typing
from abc import abstractmethod, abstractproperty

from support_pre import classproperty


class Category(type):
    """
    Acts as both a metaclass, and as the authoritative location of all
    monadic methods for a monad-category.

    @todo: Make this an abstract
    @todo: Add *all* of the methods on this
    ... not everything on this should be abstract, if we want you to be able
    to write categories without hte full monadic structure
    """

    def __instancecheck__(cls, instance):
        if any('__instancecheck__' in klass.__dict__ for klass in cls.__mro__):
            return cls.__instancecheck__(instance)
        else:
            return type.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if any('__subclasscheck__' in klass.__dict__ for klass in cls.__mro__):
            return cls.__subclasscheck__(subclass)
        else:
            return type.__subclasscheck__(cls, subclass)


class CategoryBase:
    """
    Abstract-class for objects in a category-theoretic context. Allows
    various entities within a single category to refer to one another.
    """
    @abstractproperty
    @classproperty
    def Category(self) -> Category:
        return NotImplemented

    @abstractproperty
    @classproperty
    def Morphism(self) -> 'Morphism':
        return NotImplemented

    @abstractproperty
    @classproperty
    def Element(self) -> 'Element':
        return NotImplemented

    def in_category(self, category):
        return issubclass(self.Category, category)


class Monoid(CategoryBase):
    @classmethod
    def zero(cls):
        return cls.Category.zero()

    def append(self, element):
        # return self.Category.append(value)
        return self.Category.append(self, element)

    def join(self):
        return self.Category.join(self)


class Element(Monoid):
    """
    The 'object's within a category. Called Element (rather than 'object') to
    prevent colliding with Python's builtin 'object'.

    This class is used to seperate Elements from Morphisms in a given class,
    since the signatures of their methods should differ.

    And also, we want to be able to pattern match/distinguish functions
    from objects/elements.
    """
    @classmethod
    def lift(cls, *values):
        return cls.Element(*values)

    def f_apply(self, function):
        return self.Category.f_apply(self, function)

    def a_apply(self, morphism):
        """
        a_apply(element, morphism) --> destructures morphism (such as in List, destructures into multiple functions), and fmap's each destructured func over 'element'
        """
        return self.Category.a_apply(self, morphism)

    def m_apply(self, constructor):
        """
        Basically Haskell's 'bind'
        In this context, a constructor means a function taking
        arguments from the domain category, into the monad's category.
        constructor::(a -> m b)
        """
        return self.Category.m_apply(self, constructor)


class Morphism(Monoid):
    """
    This is used to seperate Elements from Morphisms in a given class,
    since the signatures of their methods should differ.

    And also, we want to be able to pattern match/distinguish functions
    from objects/elements.

    f_map and a_map are not meaningfully defined for this, because f_map/m_map
    expect to take a bare (non-wrapped) *single* function.

    This has monoidal structure via Identity, Compose, and Collapse. Zero/Append/Join are just proxies to these functions.
    """

    def a_map(self):
        return self.Category.a_map(self)

    def __call__(self, *args):
        return self.a_map()(self.Element(*args))

    @classmethod
    def lift(cls, *values):
        return cls.Morphism(*values)

    @classmethod
    def identity(self):
        return self.Category.identity()

    def compose(self, other: 'Morphism'):
        """
        This function is not normally *explicitly* associated with 
        """
        return self.Category.compose(self, other)

    def collpase(self):
        """
        Plays the role of collapsing the AST like structure of composed functions.
        """
        return self.Category.collapse(self)

    @classmethod
    def zero(cls):
        """Monoidal structure on morphisms (functions).
        Proxies to category.identity"""
        return cls.identity()

    def append(self, other: 'Morphism'):
        """Monoidal structure on morphisms (functions).
        Proxies to category.compose"""
        return self.Category.compose(self, other)

    def join(self):
        """Monoidal structure on morphisms (functions).
        Proxies to category.collapse"""
        return self.Category.collapse(self)

    # Utility function
    # Not directly related to Monad/Category structure
    @classmethod
    def _validation(cls, *data):
        if not all(isinstance(value, typing.Callable) for value in data):
            raise TypeError("All arguments to Morphism must be callable.")
        return data


class Monad(Monoid):
    """
    This should be an abstract
    """
    @abstractmethod
    def __init__(self, *elements):
        return NotImplemented

    @classmethod
    def f_map(cls, function):
        return self.Category.f_map(function)

    @classmethod
    def m_map(cls, constructor):
        return self.Category.m_map(constructor)
