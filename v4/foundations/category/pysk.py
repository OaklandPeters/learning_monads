import typing
import functools

from .element import Element
from .morphism import Morphism
from .category import Category

from ..support.methods import classproperty, pedanticmethod


class PyskElement(Element):
    @pedanticmethod
    def apply(cls, self: 'cls.Element', function: 'cls.Morphism') -> 'cls.Element':
        return cls.Category.apply(self, function)

    @classmethod
    def is_convertiable(obj):
        return isinstance(obj, object)

    @classmethod
    def __instancecheck__(cls, instance):
        return cls.is_convertible(instance)


class PyskMorphism(Morphism):
    @pedanticmethod
    def compose(cls, self: 'cls.Morphism', function: 'cls.Morphism'):
        return cls.Category.compose(self, function)

    @pedanticmethod
    def call(cls, self: 'cls.Morphism', element: 'cls.Element') -> 'cls.Element':
        return cls.Category.call(self, element)

    @classmethod
    def is_convertible(cls, obj):
        """This should really check whether this is Callabe from a single positional argument,
        but that isn't checkable at the moment."""
        return callable(obj)

    @classmethod
    def __instancecheck__(cls, instance):
        return cls.is_convertible(instance)


class Pysk(Category):
    @staticmethod
    def _identity(value):
        return value

    @classproperty
    def identity(cls):
        return cls._identity

    @pedanticmethod
    def compose(cls, self: 'cls.Morphism', function: 'cls.Morphism'):
        @functools.wraps(self)
        def composed(element: 'cls.Element') -> 'cls.Element':
            return self(function(element))
        return composed

    @pedanticmethod
    def call(cls, self: 'cls.Morphism', element: 'cls.Element') -> 'cls.Element':
        return self(element)

    @pedanticmethod
    def apply(cls, self: 'cls.Element', function: 'cls.Morphism') -> 'cls.Element':
        return function(self)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str.format(
            "{0}({1})", self.__class__.__name__,
            _short_str(self.value)
        )

    def __repr__(self):
        return str.format(
            "{0}({1})",
            self.__class__.__name__,
            repr(self.__dict__))

    Morphism = PyskMorphism
    Element = PyskElement

    @pedanticmethod
    def is_element(cls, obj):
        return True

    @pedanticmethod
    def is_morphism(cls, obj):
        return callable(obj)

    @classproperty
    def Object(cls):
        return typing.Union[cls.Element, cls.Morphism]


PyskElement.Category = Pysk
PyskMorphism.Category = Pysk


# Internal utility functions
def _short_str(obj, max_len=30):
    """
    """
    if hasattr(obj, '__name__'):
        full = obj.__name__
    else:
        full = str(obj)
    if len(full) <= max_len:
        return full
    else:
        return full[:max_len] + " ..."
