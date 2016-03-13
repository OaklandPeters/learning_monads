"""
Tests the way that pedanticmethod/@abstractpedanthicmethod works.
"""
import unittest

from v4.support.methods import pedanticmethod, abstractpedanticmethod
from v4.support.typecheckable import TypeCheckableMeta, meets


class Applicative(metaclass=TypeCheckableMeta):
    @abstractpedanticmethod
    def apply(cls, element: 'Element', morphism: 'Morphism') -> 'Element':
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Applicative:
            return meets(C, cls.__abstractmethods__)
        return NotImplemented


def add3(value):
    return value + 3


class Mock:
    def __init__(self, data):
        self.data = data


class ApplicativeTestCase(unittest.TestCase):
    """Mostly verifies that TypeCheckableMeta is not interfering
    with using as an ABC

    THEN:

    confirm that this plays well with pedanticmethod
    """
    Interface = Applicative

    def assertMeets(self, Klass, value):
        self.assertTrue(issubclass(Klass, self.Interface))
        self.assertIsInstance(Klass(value), self.Interface)

    def assertApplicationEquals(self, Klass, value):
        outcome = add3(value)
        self.assertEqual(Klass(value).apply(add3), outcome)
        self.assertEqual(Klass.apply(Mock(value), add3), outcome)

    def test_instance_override_ducktype(self):
        class Klass:
            def __init__(self, data):
                self.data = data

            def apply(self, func):
                return func(self.data)

        self.assertMeets(Klass, 12)
        self.assertApplicationEquals(Klass, 12)

    def test_instance_override_inherit(self):
        class Klass(Applicative):
            def __init__(self, data):
                self.data = data

            def apply(self, func):
                return func(self.data)

        self.assertMeets(Klass, 12)
        self.assertApplicationEquals(Klass, 12)

    def test_classmethod_override_ducktype(self):
        class Klass:
            def __init__(self, data):
                self.data = data

            @classmethod
            def apply(cls, obj, func):
                return func(obj.data)

        self.assertMeets(Klass, 12)
        outcome = add3(12)
        self.assertEqual(Klass.apply(Mock(12), add3), outcome)
        self.assertEqual(Klass.apply(Klass(12), add3), outcome)
        self.assertRaises(TypeError, lambda: Klass(12).apply(add3))

    def test_classmethod_override_inherit(self):
        class Klass(Applicative):
            def __init__(self, data):
                self.data = data

            @classmethod
            def apply(cls, obj, func):
                return func(obj.data)

        self.assertMeets(Klass, 12)
        self.assertEqual(Klass.apply(Mock(12), add3), add3(12))
        self.assertEqual(Klass.apply(Klass(12), add3), add3(12))
        self.assertRaises(TypeError, lambda: Klass(12).apply(add3))


    def test_pedanticmethod_override_ducktype(self):
        class Klass(Applicative):
            def __init__(self, data):
                self.data = data

            @pedanticmethod
            def apply(cls, self, func):
                return func(self.data)

        self.assertMeets(Klass, 12)
        self.assertApplicationEquals(Klass, 12)

    def test_pedanticmethod_override_inherit(self):
        class Klass(Applicative):
            def __init__(self, data):
                self.data = data

            @pedanticmethod
            def apply(cls, self, func):
                return func(self.data)

        self.assertMeets(Klass, 12)
        self.assertApplicationEquals(Klass, 12)
