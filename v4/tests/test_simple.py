import unittest
from typing import Callable, Any, Dict

from v4.foundations.category.category import Category, Morphism, Element
from v4.foundations.category.simple import SimpleElement, SimpleMorphism, SimpleCategory


class SimpleCategoryTestCase(unittest.TestCase):
    def test_element(self):
        StringElement = SimpleElement('StringElement', str)

        self.assertIsInstance("x", StringEleemnt)


        print()
        print("StringElement:", type(StringElement), StringElement)
        print()
        import ipdb
        ipdb.set_trace()
        print()
        

        self.assertTrue(isinstance(12, StringElement))
        self.assertTrue(isinstance('xx', StringElement))

    def test_category(self):
        DictCategory = SimpleCategory('DictCategory', Dict, Callable[[Dict], Dict])

        self.assertTrue(isinstance({}, DictCategory.Element))
        self.assertTrue(not isinstance(dict, DictCategory.Element))
        self.assertTrue(issubclass(dict, DictCategory.Element))
        self.assertTrue(issubclass(DictCategory.Morphism, Morphism))

        self.assertTrue(issubclass(DictCategory.Element, Element))
        self.assertTrue(issubclass(DictCategory, Category))

    def test_morphism(self):
        """I'd really like to be able to check the signature of a function, but that
        does not work currently.
        """
        IntMorphism = SimpleMorphism('IntMorphism', int)
        self.assertTrue(issubclass(IntMorphism, Morphism))
