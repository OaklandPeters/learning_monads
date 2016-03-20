"""
A subset of monad-related syntactic sugar operators are sensible for categories.


@todo: Write a version of the sugar for FunctorCategory, that runs promote on the right
@todo: 
"""
from .category import Category, is_in_category
from .morphism import Morphism
from .element import Element


class MorphismSugar:
    def __or__(self, right):
        assert is_in_category(right, self.category)

        if isinstance(right, Morphism):
            return self.compose(right)
        elif isinstance(right, Element):
            return self.call(right)
        else:
            raise TypeError("Grumble")


class ElementSugar:
    def __or__(self, right):
        assert is_in_category(right, self.category)

        if isinstance(right, Morphism):
            return self.apply(right)
        elif isinstance(right, Element):
            if isinstance(self, Monoid)


class CategorySugar:
    def __or__(self, right):
        assert is_in_category(right, self.category)

        if isinstance(self.)
        if callable(self.value) and callable(arg.value):
            #return self.bind(arg.value)
            return self.compose(arg)
        elif callable(self.value) and not callable(arg.value):
            #return self.map(arg.value)
            return self.call(arg)
        elif not callable(self.value) and callable(arg.value):
            return self.apply(arg)
        elif not callable(self.value) and not callable(arg.value):
            raise TypeError("Operator 'Pipe(...) >> X', X must be callable")
        else:
            raise TypeError("Case fall-through error. This should never occur")
