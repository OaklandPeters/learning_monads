import unittest
import abc
import collections


from v4.foundations.category.category import Category, Morphism, Element
from v4.foundations.category.list_category import (
    ListElement, ListMorphism, ListCategory,
    SimpleListElement, SimpleListMorphism, SimpleListCategory
)



class CategoryTestCase(metaclass=abc.ABCMeta):
    """
    Intended to be inherited and overridden
    """
    Category = abc.abstractproperty(lambda self: NotImplemented)

    make_element = abc.abstractmethod(lambda self, seed=None: NotImplemented)
    make_morphism = abc.abstractmethod(lambda self, seed=None: NotImplemented)

    def test_base_classes(self):
        self.assertTrue(issubclass(self.Category, Category))
        self.assertTrue(issubclass(self.Category, Element))
        self.assertTrue(issubclass(self.Category.Element, Element))
        self.assertTrue(issubclass)

    def test_element_instance(self):
        self.assertIsInstance(self.make_morphism(), self.Category.Element)

    def test_morphism(self):
        self.assertTrue(self.Category.Morphism, collections.Callable)

    #
    #   Unfinished
    #
    def test_morphism_identity(self):
        elm = self.make_element()
        self.assertEqual(elm, self.Category.Morphism.identity(elm))

    def test_morphism_compose(self):
        pass

    def test_morphism_call(self):
        # Test three ways:
        #   (1) Classmethod: self.Category.Morphism.call(morphism, element)
        #   (2) Instancemthod: morphism.call(element)
        #   (3) Magic method on instance: morphism(element)
        pass

    def test_morphism_rshift(self):
        """Equivalent to compose"""
        pass

    def test_element_rshift(self):
        """Equivalent to apply"""
        pass

    def test_element_apply(self):
        pass


class ListCategoryPropertiesTestCase(CategoryTestCase, unittest.TestCase):

    Category = ListCategory

    _elements = (
        [],
        ['x'],
        [[]],
        [1],
        [[[]]],
        ['x', []],
        [[]]*10000  # obnoxiously huge list
    )
    def make_element(self):
        pass
        # ri = []


class ListCategoryTestCase(unittest.TestCase):

    def test_element(self):
        self.assertTrue(issubclass(ListElement, Element))
        self.assertTrue(issubclass(SimpleListElement, Element))
        self.assertIsInstance(list(), ListElement)
        self.assertIsInstance(list(), SimpleListElement)

    def test_morphism(self):
        self.assertTrue(issubclass(ListMorphism, Morphism))
        self.assertTrue(issubclass(SimpleListMorphism, Morphism))

    def test_category(self):
        self.assertTrue(issubclass(ListCategory, Category))
        self.assertTrue(issubclass(SimpleListCategory, Category))


class SimpleListCategoryTestCase(unittest.TestCase):
    pass
    # Be sure to test SimpleListCategory2
    # SimpleListCategory2 = SimpleCategory('SimpleListCategory2', list, ListCallable)

