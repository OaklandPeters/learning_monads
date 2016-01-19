"""
Sugar-y notation on top of Python functions.
Not sure if this can support keyword arguments.

Function(myfunc)
"""
import category
from category import classproperty

class FunctionCategory(category.Category):
    pass

class Function(category.Monad):
    """Might also be called 'Composable'."""
    def __init__(self, *elements):
        self.data = elements

    @classproperty
    def Category(cls):
        return FunctionCategory

    @classproperty
    def Element(cls):
        return FunctionElement

    @classproperty
    def Morphism(cls):
        return FunctionMorphism

    def __iter__(self):
        return iter(self.data)

    def __eq__(self, other):
        if hasattr(other, 'Category'):
            if self.Category == other.Category:
                return self.data == other.data
        else:
            return False

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(repr(elm) for elm in self.data)
        )

class FunctionElement(category.Element, Function):
    pass

class FunctionMorphism(category.Morphism, Function):
    """
    Morphisms in the category of functions, are metafunctions.

    I can't image you would intentionally instantiate this.
    """


#----------
# Unittests
#----------
import unittest

class TestFunctionMonad(unittest.TestCase):
    pass
