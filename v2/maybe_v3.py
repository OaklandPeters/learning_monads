"""
Simple Version
---------------
This version is drafted in response to the realization that I was writing a too-sophisticated version of Maybe. The normal Maybe (as described in tutorials, and Haskell), does not have the 'chaining' and 'remembering the context' behaviors that I was wanting.

    Those behaviors resemble a combination monad: List of Maybe with some State aspects.

    Consequently, I'm going to write that simple version of Maybe, and come back at the complex version as a later project.


What This version DOES:
------------------------
Allows creating a chain of computations, any one of which might fail - without later steps crashing (they get set to 'Nothing' instead).

YES:
    Maybe(name) >> name_to_id >> id_to_account >> account_to_balance

What This version does NOT:
-----------------------------
Allow creating a lazy-series of alternate attempts, and then it takes the first or last one which succeeds.

NO:
    Maybe(user_record) >> id_by_name >> id_by_address >> id_by_email



First-steps:
* Update old unit-tests for the updated version(s)
* Constructor for Maybe dispatches to MaybeElement and MaybeMorphism
* Constructor for MaybeElement dispatches to JustElement and NothingElement
* Constructor for MaybeMorphism dispatches to JustMorphism and NothingMorphism
* Add __instancecheck__ and __subclasscheck__ to category.Category, and make MaybeCategory used as a metaclass. (lookup how to do this from mfpy). Hard part - do it while allowing normal 'isinstance' to work when not overridden
* Just/Nothing should override __instancecheck__ and __subclasscheck__
* Override __call__ for identity element of Morphism


Later-steps:
* Consider if check_validation can be moved into __new__ somehow (metaclass?)
* Copy-in some of the todo from the original maybe.py
* CONSIDER: making just one large __new__ type function, and having everything else proxy to it.
* In MaybeCategory() replace 'Nothing()' calls with a constructor (this is basically a 'zero()' overideable at the instance level)

Much-later steps:
* Form plan for more advanced 'TryIt' class - which must maintain context (and validate for it)
"""
import typing

import category
from category import classproperty


class MaybeCategory(category.Category):
    @classmethod
    def f_apply(cls, element, function):
        if isinstance(element, Nothing):
            return Nothing()
        else:
            return Just(function(element.data))

    @classmethod
    def a_apply(cls, element, morphism):
        if isinstance(morphism, Just):
            return element.f_apply(morphism.data)
        else:  # Nothing morphism
            return Nothing()

    @classmethod
    def m_apply(cls, element, constructor):
        if isinstance(element, Nothing):
            return Nothing()
        else:
            return constructor(element.data)

    @classmethod
    def zero(cls):
        return Nothing()

    @classmethod
    def append(cls, element, other):
        if isinstance(element, Nothing):
            return Maybe(*other.data)
        elif isinstance(other, Nothing):
            return Maybe(*self.data)
        # both are 'Just'
        # This is built to implicity use 'First' - take the left
        # This could be generalized by specifying a 'reducer' function parameter
        else:
            return Maybe(*self.data)

    @classmethod
    def join(cls, element: 'MaybeElement'):
        if isinstance(element, Just):
            if isinstance(element.data, Nothing):
                return Nothing()
            elif isinstance(element.data, Just):
                return Just(*element.data.data)
            else:
                return Just(*element.data)
        else:
            return element

    @classmethod
    def identity(cls):
        return MaybeMorphism()

    @classmethod
    def compose(cls, morphism: 'MaybeMorphism', other: 'MaybeMorphism'):
        def wrapper(*elements):
            return other(*morphism(*elements))
        return MaybeMorphism(wrapper)

    @classmethod
    def collapse(cls, morphism):
        accumulator = morphism.identity()
        for value in morphism.data:
            if isinstance(value, MaybeMorphism):
                accumulator = accumulator.append(value)
            else:
                accumulator = accumulator.append(MaybeMorphism(value))
        return accumulator


class Maybe(category.Monad):
    def __new__(cls, *data):
        """
        Delegates to Morphism/Element classes where possible,
        as the Monad is not meant to be directly instantiated.
        However, you can call 'Maybe' as a constructor.
        Requires instantiated Morphism and Element class properties.
        """
        if len(data) == 0:
            return MaybeElement.__new__(cls, *data)
        elif all(isinstance(elm, typing.Callable) for elm in data):
            return MaybeMorphism.__new__(cls, *data)
        else:
            return MaybeElement.__new__(cls, *data)

    def __init__(self, *data):
        """All subclasses presently use this one initialization function.
        Input validation can be added by defining a '_validation' classmethod
        """
        category.check_validation(type(self), *data)
        self.data = data

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
            return (self.data == other.data)
        else:
            return False

    def __repr__(self):
        return "{0}{1}".format(
            self.__class__.__name__,
            repr(self.data)
        )

    def __iter__(self):
        yield from self.data


class MaybeElement(category.Element, Maybe):
    """
    Used for type-checking, but not meant to be directly instantiated.

    Delegates to JustElement/NothingElement
    """
    def __new__(cls, *data):
        if len(data) == 0:
            return NothingElement.__new__(cls, *data)
        else:
            return JustElement.__new__(cls, *data)


class MaybeMorphism(category.Morphism, Maybe):
    """
    Delegates to JustElement/NothingElement
    """
    def __new__(cls, *data):
        if len(data) == 0:
            return NothingMorphism.__new__(cls, *data)
        else:
            return JustMorphism.__new__(cls, *data)

    #def __init__(self, *data):
    #    if not all(isinstance(value, typing.Callable) for value in data):
    #        raise TypeError("All arguments to Morphism must be callable.")
    #    super(MaybeMorphism, self).__init__(*data)


class Just(Maybe):
    def __new__(cls, *data):
        # Raise error, if not exactly one argument
        Just._validation(*data)
        if all(isinstance(elm, typing.Callable) for elm in data):
            return JustMorphism.__new__(cls, *data)
        else:
            return JustElement.__new__(cls, *data)

    @classmethod
    def _validation(cls, *data):
        if len(data) != 1:
            raise TypeError("Just() must receive exactly one argument")


class Nothing(Maybe):
    def __new__(cls, *data):
        Nothing._validation(*data)
        return NothingElement.__new__(cls, *data)

    @classmethod
    def _validation(cls, *data):
        if len(data) != 0:
            raise TypeError("Nothing() does not accept arguments.")


class JustMorphism(MaybeMorphism, Just):
    def __new__(cls, *data):
        """
        Defines it's own __new__, so it overrides it's parent's
        __new__ (the parent's can delegate - this one should not).
        """
        return object.__new__(JustMorphism)


class NothingMorphism(MaybeMorphism, Nothing):
    def __new__(cls, *data):
        return object.__new__(NothingMorphism)

    def __call__(cls, *data):
        return data

class JustElement(MaybeElement, Just):
    def __new__(cls, *data):
        return object.__new__(JustElement)


class NothingElement(MaybeElement, Nothing):
    def __new__(cls, *data):
        return object.__new__(NothingElement)



#-----------
# Unit-Tests
#-----------
import unittest

def get(index, default=None):
    def wrapper(record):
        try:
            return record[index]
        except (IndexError, KeyError, TypeError):
            return default
    return wrapper

def getter_bind(index):
    def wrapper(record):
        try:
            value = record[index]
        except (IndexError, KeyError, TypeError):
            return Nothing()
        return Just(value)
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
    def assert_is_instances(self, obj, _is, _not):
        if not isinstance(_is, tuple):
            _is = (_is, )
        if not isinstance(_not, tuple):
            _not = (_not, )
        for _type in _is:
            self.assertIsInstance(obj, _type)
        for _type in _not:
            self.assertNotIsInstance(obj, _type)

    def assert_is_subclasses(self, obj, _is, _not):
        if not isinstance(_is, tuple):
            _is = (_is, )
        if not isinstance(_not, tuple):
            _not = (_not, )
        for _type in _is:
            self.assertTrue(issubclass(obj, _type))
        for _type in _not:
            self.assertFalse(issubclass(obj, _type))

    def test_constructor_dispatching(self):
        # Convenience functions
        def is_je(obj):
            return self.assert_is_instances(obj,
                _is=(Maybe, Just, category.Element, category.Monoid),
                _not=(Nothing, category.Morphism)
            )
        def is_ne(obj):
            return self.assert_is_instances(obj,
                _is=(Maybe, Nothing, category.Element, category.Monoid),
                _not=(Just, category.Morphism)
            )
        def is_jm(obj):
            return self.assert_is_instances(obj,
                _is=(Maybe, Just, category.Morphism, category.Monoid),
                _not=(Nothing, category.Element)
            )
        def is_nm(obj):
            return self.assert_is_instances(obj,
                _is=(Maybe, Nothing, category.Morphism, category.Monoid),
                _not=(Just, category.Element)
            )

        is_ne(Maybe())
        is_je(Maybe('xx'))
        is_jm(Maybe(sorted))

        self.assertRaises(TypeError, lambda: Just())
        is_je(Just('xx'))
        is_jm(Just(sorted))

        is_ne(Nothing())
        self.assertRaises(TypeError, lambda: Nothing('xx'))
        self.assertRaises(TypeError, lambda: Nothing(sorted))

        is_ne(MaybeElement())
        is_je(MaybeElement('xx'))
        is_je(MaybeElement(sorted))

        self.assertRaises(TypeError, lambda: JustElement())
        is_je(JustElement('xx'))
        is_je(JustElement(sorted))

        is_ne(NothingElement())
        self.assertRaises(TypeError, lambda: NothingElement('xx'))
        self.assertRaises(TypeError, lambda: NothingElement(sorted))

        is_nm(MaybeMorphism())
        self.assertRaises(TypeError, lambda: MaybeMorphism('xx'))
        is_jm(MaybeMorphism(sorted))

        self.assertRaises(TypeError, lambda: JustMorphism())
        self.assertRaises(TypeError, lambda: JustMorphism('xx'))
        is_jm(JustMorphism(sorted))

        is_nm(NothingMorphism())
        self.assertRaises(TypeError, lambda: NothingMorphism('xx'))
        self.assertRaises(TypeError, lambda: NothingMorphism(sorted))

        # todo: tests for more than one argument input

    def test_subclass_structure(self):
        """ ? Which ones should be subclass of Monad ?"""
        self.assert_is_subclasses(
            JustElement,
            _is=(Maybe, Just, category.Element, category.Monoid),
            _not=(Nothing, category.Morphism)
        )
        self.assert_is_subclasses(
            NothingElement,
            _is=(Maybe, Nothing, category.Element, category.Monoid),
            _not=(Just, category.Morphism)
        )
        self.assert_is_subclasses(
            JustMorphism,
            _is=(Maybe, Just, category.Morphism, category.Monoid),
            _not=(Nothing, category.Element)
        )
        self.assert_is_subclasses(
            NothingMorphism,
            _is=(Maybe, Nothing, category.Morphism, category.Monoid),
            _not=(Just, category.Element)
        )

    #def test_constructor_maybe(self):
    #    self.assertEqual(Maybe('xx'), Just('xx'))
    #    self.assertIsInstance(Maybe('xx'), Just)
    #    self.assertIsInstance(Maybe(), Nothing)

    #def test_constructor_just(self):
    #    self.is_all_types(
    #        Just('xx'),
    #        (Just, Maybe, category.Element),
    #        _not=(Nothing, category.Morphism)
    #    )
    #    self.assertRaises(
    #        (AssertionError, TypeError), lambda: Just() 
    #    )
    #    self.is_all_types(
    #        Nothing(),
    #        _is=(Maybe, Nothing, category.Element),
    #        _not=(Just, category.Morphism),
    #    )


    #    # morph = Just(value=lambda _str: _str+_str, default=_NotPassed)
    #    # print()
    #    # print("isinstance(morph, category.Morphism):", type(isinstance(morph, category.Morphism)), isinstance(morph, category.Morphism))
    #    # print()
    #    # import ipdb
    #    # ipdb.set_trace()
    #    # print()

    #    # self.is_all_types(
    #    #     Just(lambda _str: _str+_str),
    #    #     (Maybe, Just, NotType(Nothing),
    #    #      NotType(category.Element), category.Morphism)
    #    # )

    #def test_constructor_nothing(self):
    #    self.assertEqual(Maybe.zero(), Nothing())
    #    self.assertNotEqual(Just(None), Nothing())
    #    self.assertEqual(Maybe(), Nothing())
    #    empty_just = Just(None)
    #    empty_just.data = _NotPassed
    #    self.assertEqual(empty_just, Nothing())

    #def test_iterator(self):
    #    self.assertEqual(list(iter(Nothing())), [])
    #    self.assertEqual(list(iter(Just(1))), [1])
    #    self.assertEqual(list(iter(Just(1, 2))), [1, 2])
    #    self.assertEqual(list(iter(Just(1, Just(2, 3)))), [1, 2, 3])

    #def test_append(self):
    #    this = Maybe.zero()
    #    self.assertEqual(this, Nothing())
        
    #    this = this.append(Just(1))
    #    self.assertEqual(this, Just(1))

    #    this = this.append(Just(2))
    #    self.assertEqual(this, Just(1, Just(2)))

    #    this = this.append(Just(3))
    #    self.assertEqual(this, Just(1, Just(2, Just(3))))

    #    this = this.append(Just(4, 5))
    #    self.assertEqual(this,
    #        Just(1, Just(2, Just(3, Just(4, 5)))))

    #def test_getter(self):
    #    """Tests the support function 'get', not really Maybe itself."""
    #    self.assertEqual(get('src')(img_tag1), img_tag1['src'])

    #def test_f_apply(self):
    #    maybe_j = Maybe(img_tag1)

    #    result1 = maybe_j.f_apply(get('src'))
    #    self.assertEqual(
    #        result1,
    #        Just(get('src')(img_tag1))
    #    )

    #def test_constructor_element_default(self):
    #    """Only meaningful in concjunction to f_apply/f_map"""

    #def test_f_apply_chaining(self):
    #    self.assertEqual(
    #        Maybe(img_tag1).f_apply(get('data-src')).f_apply(get('src')),
    #        Just(Nothing())
    #    )
    #    self.assertEqual(
    #        Maybe(img_tag1).f_apply(get('src')).f_apply(get('data-src')),
    #        Just(Nothing())
    #    )
    
    #def test_a_apply_chaining(self):
    #    just_elm = Maybe(img_tag1)
    #    just_morph1 = Maybe(get('data-src'))
    #    just_morph2 = Maybe(get('src'))
    #    res1 = Maybe(img_tag1).a_apply(Maybe(get('data-src')))
    #    res2 = res1.a_apply(Maybe(get('src')))


    #    print()
    #    print("res1:", type(res1), res1)
    #    print("res2:", type(res2), res2)
    #    print()
    #    import ipdb
    #    ipdb.set_trace()
    #    print()
        

    #    self.assertEqual(
    #        Maybe(img_tag1).a_apply(Maybe(get('data-src'))).a_apply(Maybe(get('src')))
    #    )

    #def test_join(self):
    #    self.assertEqual(Just('xx').join(), Just('xx'))
    #    self.assertEqual(Maybe().join(), Nothing())
    #    self.assertEqual(Just(Just('xx')).join(), Just('xx'))
    #    self.assertEqual(Just(Nothing()).join(), Nothing())
        
    #    # Handling of default
    #    self.assertEqual(
    #        Just(Just('a', default='b')).join(),
    #        Just('a', default='b')
    #    )

    #    # Edge case that I don't know what it should be
    #    self.assertEqual(Just(Nothing(), default=12).join(), Just(12))
    #    self.assertEqual(Just(Nothing(), default=Just('xx')).join(), Just('xx'))


    ## def test_a_apply(self):
    ##     result = Maybe(img_tag).a_apply(get('src')).a_apply('data_src')

    ## def test_a_apply_empty(self):
    ##     just_elm = Just('xx')
    ##     nothing_elm = Just()
    ##     just_morph = Just(lambda _str: _str+_str)
    ##     nothing_morph = Just()

    #def test_m_apply(self):
    #    just_elm = Maybe(img_tag1)
    #    constructor1 = getter_bind('src')
    #    constructor2 = getter_bind('data-src')


if __name__ == "__main__":
    unittest.main()
