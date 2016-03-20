"""
python3 -m unittest v4.tests.test_typecheckable
"""
import unittest
from abc import abstractclassmethod, abstractmethod, ABCMeta

from ..support.typecheckable import Interface, meets_interface, TypeCheckableMeta
from ..support.methods import abstractpedanticmethod, pedanticmethod


class InterfaceTestCase(unittest.TestCase):
    """
    Test if the built-in Abstract Base Class utilities work
    """
    def test_abstractclassmethod(self):

        # class Zeroable(metaclass=TypeCheckableMeta):
        class Zeroable(metaclass=ABCMeta):
            """In most cases, this indicates a container that can be 'empty'."""
            @abstractclassmethod
            def zero(cls):
                return NotImplemented

            # @abstractmethod
            # def zero(self):
            #     return NotImplemented

            @classmethod
            def __subclasshook__(cls, subclass):
                if cls is Zeroable:
                    return meets_interface(subclass, Zeroable)
                return NotImplemented

        class Integer(int, Zeroable):
            @classmethod
            def zero(cls):
                return cls(0)

        class Float(float):
            @classmethod
            def zero(cls):
                return cls(0.0)

        class Nada(str):
            pass


        self.assertFalse(isinstance(Float, Zeroable))
        self.assertFalse(isinstance(Integer, Zeroable))
        self.assertFalse(isinstance(Nada, Zeroable))

        self.assertTrue(isinstance(Float(3), Zeroable))
        self.assertTrue(isinstance(Integer(3), Zeroable))
        self.assertFalse(isinstance(Nada(3), Zeroable))

        self.assertTrue(issubclass(Float, Zeroable))
        self.assertTrue(issubclass(Integer, Zeroable))
        self.assertFalse(issubclass(Nada, Zeroable))

        self.assertFalse(issubclass(float, Zeroable))
        self.assertFalse(issubclass(int, Zeroable))
        self.assertFalse(issubclass(str, Zeroable))

        self.assertRaises(AttributeError, lambda: issubclass(Float(0), Zeroable))
        self.assertRaises(AttributeError, lambda: issubclass(Integer(0), Zeroable))
        self.assertRaises(AttributeError, lambda: issubclass(Nada(0), Zeroable))

    def test_interface_typecheck_doesnt_inherit(self):
        """
        Basically, we confirm that a class inheriting from one of our interfaces
        does not inherit the property of actually being an interface.
        """
        class Zeroable(metaclass=TypeCheckableMeta):
            """In most cases, this indicates a container that can be 'empty'."""
            @abstractclassmethod
            def zero(cls):
                return NotImplemented

            @classmethod
            def __subclasshook__(cls, subclass):
                if cls is Zeroable:
                    return meets_interface(subclass, Zeroable)
                return NotImplemented

        class Integer(int, Zeroable):
            @classmethod
            def zero(cls):
                return cls(0)

        class PositiveInteger(Integer):
            def __new__(cls, *args, **kwargs):
                self = super().__new__(cls, *args, **kwargs)
                if self <= 0:
                    raise ValueError("Integer must be positive")
                return self

        i1 = Integer(1)
        p1 = PositiveInteger(1)

        self.assertFalse(isinstance(i1, PositiveInteger))
        self.assertTrue(isinstance(p1, PositiveInteger))
        self.assertTrue(isinstance(i1, Integer))

    def test_multiple_base_interfaces(self):

        class Zeroable(metaclass=TypeCheckableMeta):
            """In most cases, this indicates a container that can be 'empty'."""
            @abstractclassmethod
            def zero(cls):
                return NotImplemented

            @classmethod
            def __subclasshook__(cls, subclass):
                if cls is Zeroable:
                    return meets_interface(subclass, Zeroable)
                return NotImplemented

        class Appendable(metaclass=TypeCheckableMeta):
            """In most cases, this indicates a container that can be 'empty'."""
            @abstractpedanticmethod
            def append(cls, self, other):
                return NotImplemented

            @classmethod
            def __subclasshook__(cls, subclass):
                if cls is Appendable:
                    return meets_interface(subclass, Appendable)
                return NotImplemented

        class Monoid(Zeroable, Appendable):
            @classmethod
            def __subclasshook__(cls, subclass):
                if cls is Monoid:
                    return meets_interface(subclass, Monoid)
                return NotImplemented

        class MonoidalString(str):
            @classmethod
            def zero(cls):
                return ""

            @pedanticmethod
            def append(cls, self, other):
                return cls(self+other)

        monoidal_string = MonoidalString("foo")
        a_string = "foo"

        self.assertTrue(issubclass(MonoidalString, Zeroable))
        self.assertTrue(issubclass(MonoidalString, Appendable))
        self.assertTrue(issubclass(MonoidalString, Monoid))

        self.assertTrue(isinstance(monoidal_string, Zeroable))
        self.assertTrue(isinstance(monoidal_string, Zeroable))
        self.assertTrue(isinstance(monoidal_string, Zeroable))

        self.assertFalse(issubclass(str, Zeroable))
        self.assertFalse(issubclass(str, Appendable))
        self.assertFalse(issubclass(str, Monoid))

        self.assertFalse(isinstance(a_string, Zeroable))
        self.assertFalse(isinstance(a_string, Zeroable))
        self.assertFalse(isinstance(a_string, Zeroable))
