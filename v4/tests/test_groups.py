import unittest
import functools

from ..support.methods import pedanticmethod, classproperty
from ..groups.category import Category


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

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str.format(
            "{0}({1})",
            self.__class__.__name__,
            repr(self.__dict__))


class GroupsTestCase(unittest.TestCase):
    def test_category(self):

        print()
        print("issubclass(Pysk, Category):", type(issubclass(Pysk, Category)), issubclass(Pysk, Category))
        print()
        import ipdb
        ipdb.set_trace()
        print()
        
