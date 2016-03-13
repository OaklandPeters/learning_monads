import unittest
from abc import abstractclassmethod

from ..support.typecheckable import Interface


class InterfaceTestCase(unittest.TestCase):
    """
    Test if the built-in Abstract Base Class utilities work
    """
    def test_abstractclassmethod(self):

        class Zeroable(Interface):
            """In most cases, this indicates a container that can be 'empty'."""
            @abstractclassmethod
            def zero(cls):
                return NotImplemented

        class Integer(int, Zeroable):
            @classmethod
            def zero(cls):
                return cls(0)

        class Float(float):
            @classmethod
            def zero(cls):
                return cls(0.0)

        self.assertFalse(isinstance(Float, Zeroable))
        self.assertTrue(isinstance(Float(3), Zeroable))
        self.assertFalse(isinstance(Integer, Zeroable))
        self.assertTrue(isinstance(Integer(5), Zeroable))

        self.assertTrue(issubclass(Float, Zeroable))
        self.assertTrue(issubclass(Integer, Zeroable))
        self.assertRaises(AttributeError, lambda: issubclass(Float(0), Zeroable))
        self.assertRaises(AttributeError, lambda: issubclass(Integer(0), Zeroable))

