"""
First-steps:
* Tests for a_apply; test_a_apply_empty
* test_join
* a_apply/a_map
* m_apply/m_map
* Tests for a_map
* Tests for m_apply
* Tests for m_map
* Tests for append, join for 
* Signature for Maybe.__init__(self, value=(,), default=_NotPassed). Get MaybeElement/MaybeMorphism to defer to it.
* MaybeCategory.first, .last. Recursive join() operations.
* test_join_first(), test_join_last()
* Maybe         -->   (MaybeElement, MaybeMorphism)
* Maybe  -|sugar|->   (Just, Nothing)



Next-steps:
* Cleanup repetition in Maybe.__new__
* Change Nothing to be Just with .data = (), since this hooks the behavior of zero/append/just to the behavior of tuples
* Change inheritance, Nothing inherits from MaybeElement, but not Just
* rewrite join as a reduction. Write 'first'/'last' as arguments into join, taking advantage of chain on .default
* simplify conditional logic in Maybe.__new__. Preferablly by dispatching.
* Simplify structure, by making Nothing simply Maybe.zero. Have to change all statements checking, 'isinstance(element, Nothing)'
* Have classes for type-product of (Just, Nothing) and (Element, Morphism). So Maybe-->(Just, Nothing)-->(JustElement, NothingElement, JustMorphism, NothingMorphism)
** OR MAYBE: Make 'Nothing' just be sugar over an empty Just(), with an override for __instancecheck__, __subclasscheck__, and __new__. ? Should Just.__new__
** The idea here is to have the only data type be 'MaybeElement'/'MaybeMorphism', and have Just/Nothing simply be used for type-checking and constructors.
* Cleanup __repr__ functions. Better display for _NotPassed, and simpler display for Nothing(). Since Nothing() should only be sugar around MaybeElement, handle this behavior in Maybe.__repr__


Later-steps:
* Change default to use _NotPassed
* Incorporate support functions and methods from https://hackage.haskell.org/package/base-4.8.1.0/docs/Data-Maybe.html#t:Maybe, such fromMaybe, fromJust
* Consider the handling of 'default'. In f_apply/a_apply, when element is Nothing, which should be returned: element.default or morphism.default.


BEWARE: Potentially recursive process with .join(), for elements which are Nothing, if it's data is set to Nothing.  a = Nothing(), b = Nothing(), a.data = b, b.data = a
BUGCHECK THIS
    ... this is actually rationanl behavior, because it's like a looped list




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
        return wrapper

    @classmethod
    def a_apply(cls, element, morphism: 'MaybeMorphism'):

        # unwrap the morphism somehow
        if isinstance(morphism, Nothing):
            pass


        # what should be Just('x').a_apply(Nothing()) ?
        # By analogy with List(), it would be 

        return accumulator.join()

    @classmethod
    def a_map(cls, morphism: 'MaybeMorphism'):
        def wrapper(element: 'MaybeElement'):
            return cls.a_apply(element, morphism)
        return wrapper

    @classmethod
    def zero(cls):
        return Nothing()

    @classmethod
    def append(cls, left: 'Maybe', right: 'Maybe'):
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

        @todo: FUTURE - have the while/recurse process keep a memory to prevent loops
        """
        if not isinstance(left, Maybe):
            raise TypeError("left must be 'Maybe', not "+left.__class__.__name__)
        
        return cls._append(left, right)

    @classmethod
    def _append(cls, left: 'Any', right: 'Maybe'):
        """Recursive utility function for .append() method"""
        if isinstance(left, Just):
            return Just(left.data, cls._append(left.default, right))
        else:
            return right

    @classmethod
    def join(cls, element: 'Maybe'):
        """

        Complication, to properly chain/nest Maybe via default
            Maybe('a', default=Maybe('b', default=Maybe('c', default='d')))

        data
            | non-monad --> no changes
            | Nothing --> 
            | Just --> destructure

        """
        # element.data is a Just: Just(Just('x')).join()
        if isinstance(element.data, Just) and not isinstance(element.data, Nothing):
            return Maybe(element.data.data, element.data.default)
        # Since .data is nothing, fallback to default
        elif isinstance(element.data, Nothing):
            return Maybe(element.default).join()
        # .data is normal non-Maybe-monad value --> no changes
        else:
            return Maybe(element.data, element.default)


class Maybe(category.Monad):
    def __new__(cls, value=_NotPassed, default=_NotPassed):
        """
        Dispatches to Morphism/Element classes where possible,
        as the Monad is not meant to be directly instantiatable.
        Requires instantiated Morphism and Element class properties.

        
        ?? What about condition that: value=_NotPassed and default=*actual-value*?

        """
        # If this was called via Just(), Nothing(), or MaybeMorphism(),
        #    (as oppsed to Maybe())
        #    then set the class equal to that
        if issubclass(cls, category.Element) or issubclass(cls, category.Morphism):
            self = object.__new__(cls)
            self.__init__(value, default=default)
            return self
        
        # Treat as Nothing()
        elif value is _NotPassed:
            self = object.__new__(Nothing)
            self.__init__(value, default=default)
            return self

        # Treat as Morphism
        elif isinstance(value, typing.Callable):
            self = object.__new__(MaybeMorphism)
            self.__init__(value, default=default)
            return self

        # Treat as Just
        else:
            self = object.__new__(Just)
            self.__init__(value, default=default)
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
        if isinstance(other, Maybe):
            return (self.data == other.data) and (self.default == other.default)
        else:
            return None

    def __repr__(self):
        return "{0}({1}, default={2})".format(
            self.__class__.__name__,
            repr(self.data),
            repr(self.default)
        )

    def __iter__(self):
        if self.data is not _NotPassed:
            yield self.data
        # yield self.data
        if isinstance(self.default, Maybe):
            yield from self.default
        else:
            # yield self.default
            if self.default is not _NotPassed:
                yield self.default



class MaybeElement(category.Element, Maybe):
    """Exists only be base class for Just and Nothing."""


class Just(MaybeElement):
    """
    'default' forms the implicit 'or else...' inside Maybe's structure
    It is used for chaining
    """
    def __init__(self, value=_NotPassed, default=_NotPassed):
        if value is _NotPassed:
            raise TypeError("No value provided to Just( )")
        self.data = value
        self.default = default


class Nothing(MaybeElement):
    def __init__(self, value=_NotPassed, default=_NotPassed):
        if value is not _NotPassed:
            raise TypeError("Nothing() should not have a value provided.")
        # ? assert default is _NotPassed
        # ... for now I'll let a default be specified for Nothing
        self.data = value
        self.default = default


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


class NotKlassMeta(type):
    def __instancecheck__(self, value):
        return not isinstance(value, self._klass)
    @classmethod
    def __subclasscheck__(cls, subclass):
        return not issubclass(value, cls._klass)

class NotType:
    """Sugar/Convenience for type-checking the opposite of types."""
    def __new__(cls, _klass):
        class NotKlass(metaclass=NotKlassMeta):
            pass
        NotKlass._klass = _klass
        NotKlass.__name__ = 'Not_' + _klass.__name__
        return NotKlass



class MaybeTests(unittest.TestCase):
    def is_all_types(self, obj, _types: typing.Tuple[type]):
        if not isinstance(_types, tuple):
            _types = (_types, )
        for _type in _types:
            self.assertIsInstance(obj, _type)

    def test_constructor_maybe(self):
        self.assertEqual(Maybe('xx'), Just('xx'))
        self.assertIsInstance(Maybe('xx'), Just)
        self.assertIsInstance(Maybe(), Nothing)

    def test_constructor_just(self):
        self.is_all_types(
            Just('xx'), (Just, Maybe, NotType(Nothing),
                         category.Element, NotType(category.Morphism))
        )
        self.assertRaises(
            (AssertionError, TypeError), lambda: Just() 
        )
        self.is_all_types(
            Nothing(), (Maybe, NotType(Just), Nothing, 
                     category.Element, NotType(category.Morphism))
        )


        # morph = Just(value=lambda _str: _str+_str, default=_NotPassed)
        # print()
        # print("isinstance(morph, category.Morphism):", type(isinstance(morph, category.Morphism)), isinstance(morph, category.Morphism))
        # print()
        # import ipdb
        # ipdb.set_trace()
        # print()

        # self.is_all_types(
        #     Just(lambda _str: _str+_str),
        #     (Maybe, Just, NotType(Nothing),
        #      NotType(category.Element), category.Morphism)
        # )

    def test_constructor_nothing(self):
        self.assertEqual(Maybe.zero(), Nothing())
        self.assertNotEqual(Just(None), Nothing())
        self.assertEqual(Maybe(), Nothing())
        empty_just = Just(None)
        empty_just.data = _NotPassed
        self.assertEqual(empty_just, Nothing())

    def test_iterator(self):
        self.assertEqual(list(iter(Nothing())), [])
        self.assertEqual(list(iter(Just(1))), [1])
        self.assertEqual(list(iter(Just(1, 2))), [1, 2])
        self.assertEqual(list(iter(Just(1, Just(2, 3)))), [1, 2, 3])

    def test_append(self):
        this = Maybe.zero()
        self.assertEqual(this, Nothing())
        
        this = this.append(Just(1))
        self.assertEqual(this, Just(1))

        this = this.append(Just(2))
        self.assertEqual(this, Just(1, Just(2)))

        this = this.append(Just(3))
        self.assertEqual(this, Just(1, Just(2, Just(3))))

        this = this.append(Just(4, 5))
        self.assertEqual(this,
            Just(1, Just(2, Just(3, Just(4, 5)))))

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

    def test_constructor_element_default(self):
        """Only meaningful in concjunction to f_apply/f_map"""

    def test_chaining(self):
        self.assertEqual(
            Maybe(img_tag1).f_apply(get('data-src')).f_apply(get('src')),
            Just(Nothing())
        )
        self.assertEqual(
            Maybe(img_tag1).f_apply(get('src')).f_apply(get('data-src')),
            Just(Nothing())
        )
    
    def test_join(self):
        self.assertEqual(Just('xx').join(), Just('xx'))
        self.assertEqual(Maybe().join(), Nothing())
        self.assertEqual(Just(Just('xx')).join(), Just('xx'))
        self.assertEqual(Just(Nothing()).join(), Nothing())
        
        # Handling of default
        self.assertEqual(
            Just(Just('a', default='b')).join(),
            Just('a', default='b')
        )

        # Edge case that I don't know what it should be
        self.assertEqual(Just(Nothing(), default=12).join(), Just(12))
        self.assertEqual(Just(Nothing(), default=Just('xx')).join(), Just('xx'))


    # def test_a_apply(self):
    #     result = Maybe(img_tag).a_apply(get('src')).a_apply('data_src')

    # def test_a_apply_empty(self):
    #     just_elm = Just('xx')
    #     nothing_elm = Just()
    #     just_morph = Just(lambda _str: _str+_str)
    #     nothing_morph = Just()





if __name__ == "__main__":
    unittest.main()
