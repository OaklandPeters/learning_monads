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




EVEN SIMPLER
--------------
Remove JustElement/NothingElement/JustMorphism/NothingMorphism --> MaybeElement/MaybeMorphism. Just/Nothing are not instancable classes, and just exist as constructors and type-checking.


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
        accumulator = element.zero()
        # If isinstnace(element, Nothing), this will do nothing
        for value in element:
            accumulator = accumulator.append(Just(function(value)))
        return accumulator
        #if isinstance(element, Nothing):
        #    return Nothing()
        #else:
        #    return Just(function(element.data))

    @classmethod
    def a_apply(cls, element, morphism):
        accumulator = element.zero()
        # If isinstance(morphism, Nothing), then this will do nothing
        for func in morphism:
            accumulator = accumulator.append(element.f_apply(func))
        return accumulator.join()
        #
        #if isinstance(morphism, Nothing):
        #    return Nothing()
        #else:
        #    return element.f_apply(morphism.data)

    @classmethod
    def m_apply(cls, element, constructor):
        return element.f_apply(constructor).join()
        #if isinstance(element, Nothing):
        #    return Nothing()
        #else:
        #    return constructor(element.data)
        

    @classmethod
    def zero(cls):
        return Nothing()

    @classmethod
    def append(cls, element, other):
        """
         Alternate v2:
         return Maybe(*element.reducer(element, other))
         def first(self, other):
             return self
         def last(self, other):
             return other
        """
        if isinstance(element, Nothing):
            #return Maybe(*other.data)
            return element.lift(*other.data)
        elif isinstance(other, Nothing):
            #return Maybe(*element.data)
            return element.lift(*element.data)
        # both are 'Just'
        # This is built to implicity use 'First' - take the left
        # This could be generalized by specifying a 'reducer' function parameter
        # return Maybe(element.reducer(element, other))
        else:
            return element.lift(*element.data)  # take the 'left'/'first'

    @classmethod
    def join(cls, element: 'MaybeElement'):
        """
        Interestingly, these looks very much like the 'join' for list.
        ... Perhaps this points to a shared structure of any monoid, who
        has the property that *all* of their internal structure/data can
        be captured by a single internal tuple ('.data')?
        """
        accumulator = element.zero()
        for value in element:
            if isinstance(value, Maybe):
                accumulator = accumulator.append(value)
            else:
                accumulator = accumulator.append(Maybe(value))
        return accumulator

    @classmethod
    def identity(cls):
        return MaybeMorphism()

    @classmethod
    def compose(cls, morphism: 'MaybeMorphism', other: 'MaybeMorphism'):
        #def wrapper(*elements):
        #    return other(*morphism(*elements))
        #return MaybeMorphism(wrapper)
        return cls.append(morphism, other)

    @classmethod
    def collapse(cls, morphism):
        accumulator = morphism.identity()
        for value in morphism.data:
            if isinstance(value, MaybeMorphism):
                accumulator = accumulator.append(value)
            else:
                accumulator = accumulator.append(MaybeMorphism(value))
        return accumulator


class Maybe(category.Monad, metaclass=MaybeCategory):
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

    @classmethod
    def _validation(cls, *data):
        if len(data) > 1:
            raise TypeError("Maybe objects must receive 0 or 1 arguments, not "+len(data))

class MaybeElement(category.Element, Maybe):
    """

    """
    def __new__(cls, *data):
        category.check_validation(cls, *data)
        return object.__new__(MaybeElement)
        #if len(data) == 0:
        #    return NothingElement.__new__(cls, *data)
        #else:
        #    return JustElement.__new__(cls, *data)


class MaybeMorphism(category.Morphism, Maybe):
    """
    #Delegates to JustElement/NothingElement
    """
    def __new__(cls, *data):
        category.check_validation(cls, *data)
        return object.__new__(MaybeMorphism)

        #if len(data) == 0:
        #    return NothingMorphism.__new__(cls, *data)
        #else:
        #    return JustMorphism.__new__(cls, *data)

    #def __init__(self, *data):
    #    if not all(isinstance(value, typing.Callable) for value in data):
    #        raise TypeError("All arguments to Morphism must be callable.")
    #    super(MaybeMorphism, self).__init__(*data)


#class Just(Maybe):
#    def __new__(cls, *data):
#        # Raise error, if not exactly one argument
#        Just._validation(*data)
#        if all(isinstance(elm, typing.Callable) for elm in data):
#            return JustMorphism.__new__(cls, *data)
#        else:
#            return JustElement.__new__(cls, *data)

#    @classmethod
#    def _validation(cls, *data):
#        if len(data) != 1:
#            raise TypeError("Just() must receive exactly one argument")


#class Nothing(Maybe):
#    def __new__(cls, *data):
#        Nothing._validation(*data)
#        return NothingElement.__new__(cls, *data)

#    @classmethod
#    def _validation(cls, *data):
#        if len(data) != 0:
#            raise TypeError("Nothing() does not accept arguments.")


#class JustMorphism(MaybeMorphism, Just):
#    def __new__(cls, *data):
#        """
#        Defines it's own __new__, so it overrides it's parent's
#        __new__ (the parent's can delegate - this one should not).
#        """
#        return object.__new__(JustMorphism)


#class NothingMorphism(MaybeMorphism, Nothing):
#    def __new__(cls, *data):
#        return object.__new__(NothingMorphism)

#    def __call__(cls, *data):
#        return data

#class JustElement(MaybeElement, Just):
#    def __new__(cls, *data):
#        return object.__new__(JustElement)


#class NothingElement(MaybeElement, Nothing):
#    def __new__(cls, *data):
#        return object.__new__(NothingElement)





#
#   Testing Just/Nothing as convenience functions
#
#
class Just(Maybe):
    def __new__(cls, *data):
        cls._validation(*data)
        if all(isinstance(elm, typing.Callable) for elm in data):
            return MaybeMorphism(*data)
        else:
            return MaybeElement(*data)

    @classmethod
    def _validation(cls, *data):
        if len(data) != 1:
            raise TypeError("Just() must receive exactly one argument")

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, Maybe):
            if len(instance.data) == 1:
                return True
        return False

class Nothing(Maybe):
    def __new__(cls, *data):
        cls._validation(*data)
        return MaybeElement(*data)

    @classmethod
    def _validation(cls, *data):
        if len(data) != 0:
            raise TypeError("Nothing() does not accept arguments.")

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, Maybe):
            if len(instance.data) == 0:
                return True
        return False



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

        #self.assertRaises(TypeError, lambda: JustElement())
        #is_je(JustElement('xx'))
        #is_je(JustElement(sorted))

        #is_ne(NothingElement())
        #self.assertRaises(TypeError, lambda: NothingElement('xx'))
        #self.assertRaises(TypeError, lambda: NothingElement(sorted))

        is_nm(MaybeMorphism())
        self.assertRaises(TypeError, lambda: MaybeMorphism('xx'))
        is_jm(MaybeMorphism(sorted))

        #self.assertRaises(TypeError, lambda: JustMorphism())
        #self.assertRaises(TypeError, lambda: JustMorphism('xx'))
        #is_jm(JustMorphism(sorted))

        #is_nm(NothingMorphism())
        #self.assertRaises(TypeError, lambda: NothingMorphism('xx'))
        #self.assertRaises(TypeError, lambda: NothingMorphism(sorted))

        # todo: tests for more than one argument input

        self.assertRaises(TypeError, lambda: Maybe(1, 2))
        self.assertRaises(TypeError, lambda: Just(1, 2))
        #self.assertRaises(TypeError, lambda: JustMorphism(1, 2))

    def test_constructor_equality(self):
        self.assertEqual(Maybe('xx'), Just('xx'))
        
        func = lambda x: x+2
        self.assertEqual(Maybe(func), Just(func))
        self.assertEqual(Just(func), MaybeMorphism(func))
        self.assertNotEqual(Just(func), Just(lambda x: x+2))

        self.assertEqual(Maybe(sorted), Just(sorted))
        self.assertEqual(Maybe(sorted), MaybeMorphism(sorted))

        self.assertEqual(Maybe(12), Just(12))
        self.assertEqual(Maybe(12), MaybeElement(12))

        self.assertEqual(Maybe(), Nothing())
        self.assertEqual(Maybe(), MaybeElement())
        self.assertEqual(Nothing(), MaybeElement())

        self.assertNotEqual(Just(None), Nothing())
        self.assertNotEqual(Just(tuple()), Nothing())

    def test_dubious_equalities(self):
        """
        I'm not sure that I want these to be true, but they are ATM
        """
        self.assertEqual(MaybeElement(sorted), MaybeMorphism(sorted))
        self.assertEqual(MaybeElement(), MaybeMorphism())
        self.assertEqual(Nothing(), MaybeMorphism())

        empty_just = Just(None)
        empty_just.data = tuple()
        self.assertEqual(empty_just, Nothing())

    def test_constructor_nothing(self):
        self.assertEqual(Maybe.zero(), Nothing())
        self.assertNotEqual(Just(None), Nothing())
        self.assertEqual(Maybe(), Nothing())


    def test_iterator(self):
        self.assertEqual(list(iter(Nothing())), [])
        self.assertEqual(list(iter(Just(1))), [1])
        self.assertEqual(list(iter(Just((1, 2)))), [(1, 2)])
        self.assertEqual(list(iter(MaybeMorphism())), [])

    def test_append(self):
        self.assertEqual(Nothing().append(Nothing()), Nothing())
        self.assertEqual(Nothing().append(Just('xy')), Just('xy'))
        self.assertEqual(Just('xy').append(Nothing()), Just('xy'))
        self.assertEqual(Just(1).append(Just(2)), Just(1))

    #def test_getter(self):
    #    """Tests the support function 'get', not really Maybe itself."""
    #    self.assertEqual(get('src')(img_tag1), img_tag1['src'])

    def test_f_apply(self):
        maybe_j = Maybe(img_tag1)

        result1 = maybe_j.f_apply(get('src'))
        self.assertEqual(
            result1,
            Just(get('src')(img_tag1))
        )

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

    def test_join(self):
        self.assertEqual(Just('xx').join(), Just('xx'))
        self.assertEqual(Maybe().join(), Nothing())
        self.assertEqual(Just(Just('xx')).join(), Just('xx'))
        self.assertEqual(Just(Nothing()).join(), Nothing())
        
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
