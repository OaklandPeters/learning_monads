import unittest
import collections

from v4.support.methods import pedanticmethod, classproperty
from v4.foundations.category.category import Category, Morphism, Element
from v4.foundations.category.basis import Equitable, Applicative


class CategoryTests(unittest.TestCase):

    def test_morphism_callable(self):
        self.assertTrue(issubclass(Morphism, collections.Callable))

    def test_element_equitable(self):
        self.assertTrue(issubclass(Element, Equitable))
        self.assertTrue(issubclass(Element, Applicative))

    def test_abstract_interface_of_category(self):
        class MockCategory:
            Element = object
            Morphism = object

        self.assertTrue(issubclass(MockCategory, Category))
        self.assertFalse(issubclass(object, Category))
        self.assertFalse(issubclass(int, Category))

    def test_abstract_interface_of_morphism(self):
        class ConcreteMorphism:
            def __init__(self, function):
                self.function = function

            @pedanticmethod
            def call(self, element):
                pass

            @pedanticmethod
            def compose(self, other):
                pass

            @classproperty
            def identity(self):
                pass

            def __call__(self, element):
                pass

            def __rshift__(self, other):
                pass

            @classmethod
            def __subclasscheck__(self, other):
                pass

            def __instancecheck__(self, other):
                pass

        self.assertTrue(issubclass(ConcreteMorphism, Morphism))
        self.assertTrue(issubclass(ConcreteMorphism, collections.abc.Callable))
        self.assertIsInstance(ConcreteMorphism(lambda: None), ConcreteMorphism)
        self.assertIsInstance(ConcreteMorphism(lambda: None), Morphism)
        self.assertIsInstance(ConcreteMorphism(lambda: None), collections.abc.Callable)

        self.assertFalse(issubclass(int, Morphism))
        self.assertFalse(issubclass(object, Morphism))
        self.assertFalse(issubclass(collections.abc.Callable, Morphism))

    def test_abstract_interface_of_element(self):
        class ConcreteElement:
            def __init__(self, data):
                self.data = data

            @pedanticmethod
            def apply(cls, self, morphism):
                pass

            @classmethod
            def __subclasscheck__(self, other):
                pass

            def __instancecheck__(self, other):
                pass

        self.assertTrue(issubclass(ConcreteElement, Element))
        self.assertIsInstance(ConcreteElement('a'), ConcreteElement)
        self.assertIsInstance(ConcreteElement('a'), Element)

        self.assertFalse(issubclass(int, Element))
        self.assertFalse(issubclass(object, Element))
        self.assertFalse(issubclass(collections.abc.Callable, Element))
