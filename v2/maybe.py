"""
Next-steps:
* Change Nothing to be Just with .data = (), since this hooks the behavior of zero/append/just to the behavior of tuples
* Change inheritance, Nothing inherits from MaybeElement, but not Just
* rewrite join as a reduction. Write 'first'/'last' as arguments into join, taking advantage of chain on .default
* Change category.append : element, element
* Change list.append
* simplify conditional logic in Maybe.__new__. Preferablly by dispatching.
* Simplify structure, by making Nothing simply Maybe.zero. Have to change all statements checking, 'isinstance(element, Nothing)'


Later-steps:
* Change default to use _NotPassed
* Incorporate support functions and methods from https://hackage.haskell.org/package/base-4.8.1.0/docs/Data-Maybe.html#t:Maybe, such fromMaybe, fromJust
* Consider the handling of 'default'. In f_apply/a_apply, when element is Nothing, which should be returned: element.default or morphism.default.

PROBLEM:
This doesn't really let me write the chain of tries, where you take the first valid one.
BECAUSE, chaining f_apply on Maybe, keeps applying the later ones. Rather than stopping as soon as it has a valid one.


def get_src(img_tag):
    retrun Maybe(img_tag) >> get('src') >> get('data_src') >> get('data-srcset')
"""
import typing

import category
from category import classproperty

class _NotPassed: pass

class MaybeCategory:
    @classmethod
    def f_apply(cls, element, function, default=_NotPassed):
        """
        If element is Nothing, returns the default value, else
        applies the function to contents of element, and
        returns wrapped in a 'Just'
        """
        if default == _NotPassed:
            default = cls.zero()
        if isinstance(element, Nothing):
            return default
        else:
            return Just(function(element.data))

    @classmethod
    def f_map(cls, function, default=None):
        def wrapper(element):
            return cls.f_apply(element, function, default)

    @classmethod
    def 

    @classmethod
    def zero(cls):
        return Nothing()

    @classmethod
    def append(cls, left, right):
        """
        Hard to understand for elements which are Just
        Just(12).append('ya')  .... doesn't make sense to me
        Although Nothing.append does...
        Nothing().append('ya') ==  Just('ya')
        HAskell: 
        instance Monoid a => Monoid (Maybe a) where
          mempty = Nothing
          Nothing `mappend` m = m
          m `mappend` Nothing = m
          Just m1 `mappend` Just m2 = Just (m1 `mappend` m2)
        """

        if isinstance(left, Nothing) and isinstance(right, Nothing):
            return Nothing()
        elif isinstance(left, Nothing) and isinstance(right, Nothing):
            return Just(right.data)
        elif not isinstance(left, Nothing) and isinstance(right, Nothing):
            return Just(left.data)
        elif not isinstance(left, Nothing) and not isinstance(right, Nothing):
            return Just(left.data, default=right.data)
        else:
            raise TypeError("left: {0}, right: {1}".format(
                left.__class__.__name__, right.__class__.__name__
            ))


    @classmethod
    def join(cls, element, reducer=take_left):
        """There are more than one possible type of join.
        This one is implicitly the 'first' behavior.

        @todo: rewrite join as a reduction
        """
        if isinstance(element.data, Maybe):
            return 



class Maybe(category.Monad):
    def __new__(cls, *elements):
        """
        Dispatches to Morphism/Element classes where possible,
        as the Monad is not meant to be directly instantiatable.
        Requires instantiated Morphism and Element class properties.

        
        # Maybe.__new__
        if len(elements) > 0 and all(isinstance(elm, typing.Callable) for elm in elements):
            return cls.Morphism(*elements)
        else:
            return cls.Element(*elements)

        # Just.__new__
        if len(elements) == 0:
            self = object.__new__(Nothing)
        else:
            self = object.__new__(Just)
        self.__init__(*elements)
        return self

        """
        # This was called via Just, Nothing, or MaybeMorphism, so
        #    Defer to the __new__ for that....
        if issubclass(cls, category.Element) or issubclass(cls, category.Morphism):
            self = object.__new__(cls)
            self.__init__(*elements)
            return self
        
        elif len(elements) > 0 and all(isinstance(elm, typing.Callable) for elm in elements):
            self = object.__new__(MaybeMorphism)
            self.__init__(*elements)
            return self
        else:
            if len(elements) == 0:
                self = object.__new__(Nothing)
                self.__init__()
                return self
            else:
                self = object.__new__(Just)
                self.__init__(*elements)
                return self


    # def __init__(self, *element):
    #     self.data = element

    @classproperty
    def Category(cls):
        return MaybeCategory

    @classproperty
    def Element(cls):
        return MaybeElement

    @classproperty
    def Morphism(cls):
        return MaybeMorphism

    def __eq__(self, other):
        if (isinstance(self, Nothing) and isinstance(other, Nothing)):
            return True
        # Note: we basicaly want to check XOR here ....
        elif (isinstance(self, Nothing) or isinstance(other, Nothing)):
            return False
        else:
            if hasattr(other, 'Category'):
                if (issubclass(self.Category, other.Category)
                    or issubclass(other.Category, self.Category)):
                    return self.data == other.data
            return False

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            repr(self.data)
        )


class MaybeElement(category.Element, Maybe):
    """Exists only be base class for Just and Nothing."""

class Just(MaybeElement):
    """
    'default' forms the implicit 'or else...' inside Maybe's structure
    It is used for chaining
    """
    def __init__(self, element=None, default=None):
        self.data = element
        self.default = default

class Nothing(Just):
    # def __init__(self):
    #     self.data = None
    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

Null = Nothing()

class MaybeMorphism(category.Morphism, Maybe):

    def __init__(self, element):
        self.data = element


thing = Maybe('aa')


#-----------
# Unit-Tests
#-----------
import unittest

def get(index, default=Null):
    def wrapper(record):
        try:
            return record[index]
        except (IndexError, KeyError, TypeError):
            return default
    return wrapper

img_tag1 = {
    'src': 'path: src'
}
img_tag2 = {
    'data-src': 'path: data-src'
}
img_tag3 = {
    'src': 'path',
    'data-srcset': 'path: data-srcset'
}

class MaybeTests(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual(Maybe('xx'), Just('xx'))
        self.assertIsInstance(Maybe('xx'), Just)
        self.assertIsInstance(Maybe(), Nothing)

    def test_nothing_constructor(self):
        self.assertNotEqual(Just(None), Nothing())
        self.assertNotEqual(Just(), Nothing())

    def test_getter(self):
        """Tests the support function 'get', not really Maybe itself."""
        self.assertEqual(get('src')(img_tag1), img_tag1['src'])

    def test_f_apply(self):
        maybe_j = Maybe(img_tag1)

        result1 = maybe_j.f_apply(get('src'))
        self.assertEqual(
            result1,
            Just(get('src')(img_tag1))
        )

    def test_chaining(self):
        result = Maybe(img_tag1).f_apply(get('data-src'))

        print()
        print("result:", type(result), result)
        print()
        import ipdb
        ipdb.set_trace()
        print()
        

        self.assertEqual(
            Maybe(img_tag1).f_apply(get('data-src')).f_apply(get('src')),
            get('src')(Maybe(img_tag1))
        )
        self.assertEqual(
            Maybe(img_tag1).f_apply(get('src')).f_apply(get('data-src')),
            get('src')(Maybe(img_tag1))
        )
        
    # def test_a_apply(self):
    #     result = Maybe(img_tag).a_apply(get('src')).a_apply('data_src')

    # def test_sugar(self):        
    #     result = Maybe(img_tag) >> get('src') >> get('data_src') >> get('data-srcset')


if __name__ == "__main__":
    unittest.main()
