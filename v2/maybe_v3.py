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
* Class structure
* Copy unit-tests from maybe.py
"""
import category

class MaybeCategory(category.Category):
    @classmethod
    def f_apply(cls, element, function):
        if isinstance(element, Nothing):
            return Nothing()
        else:
            return Just(function(element.data))

    @classmethod
    def a_apply(cls, element, morphism):
        pass

    @classmethod
    def m_apply(cls, element, constructor):
        pass

    @classmethod
    def zero(cls, element, constructor):
        return Nothing()

    @classmethod
    def append(cls, element, other):
        if isinstance(element, Nothing):
            return Maybe(*other.data)
        elif isinstance(other, Nothing):
            return Maybe(*self.data):
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
    def __new__(cls, *values):
        """
        Dispatches to Morphism/Element classes where possible,
        as the Monad is not meant to be directly instantiatable.
        Requires instantiated Morphism and Element class properties.

        This is not *generally

        """
        if issubclass(cls, category.Element) or issubclass(cls, category.Morphism):
            self = object.__new__(cls)
        else:
            # Calls to constructor of List itself should dispatch
            if all(isinstance(elm, typing.Callable) for elm in values):
                self = object.__new__(cls.Morphism)
            else:
                if len(values) == 0:
                    self = object.__new__(Nothing)
                else:
                    self. = object.__new__(Just)
        self.__init__(*values)
        return self



class MaybeElement(category.Element, Maybe):
    """
    Used for type-checking, but not meant to be directly instantiated.
    """


class Just(MaybeElement):
    def __init__(self, data):
        self.data = (data, )


class Nothing(MaybeElement):
    def __init__(self):
        self.data = (, )


class MaybeMorphism(category.Morphism, Maybe):
    pass




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
    def is_all_types(self, obj, _is: typing.Tuple[type], _not: typing.Tuple[type]):
        if not isinstance(_is, tuple):
            _is = (_is, )
        if not isinstance(_not, tuple):
            _not = (_not, )
        for _type in _is:
            self.assertIsInstance(obj, _type)
        for _type in _not:
            self.assertNotIsInstance(obj, _type)

    def test_constructor_maybe(self):
        self.assertEqual(Maybe('xx'), Just('xx'))
        self.assertIsInstance(Maybe('xx'), Just)
        self.assertIsInstance(Maybe(), Nothing)

    def test_constructor_just(self):
        self.is_all_types(
            Just('xx'),
            (Just, Maybe, category.Element),
            _not=(Nothing, category.Morphism)
        )
        self.assertRaises(
            (AssertionError, TypeError), lambda: Just() 
        )
        self.is_all_types(
            Nothing(),
            _is=(Maybe, Nothing, category.Element),
            _not=(Just, category.Morphism),
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

    def test_f_apply_chaining(self):
        self.assertEqual(
            Maybe(img_tag1).f_apply(get('data-src')).f_apply(get('src')),
            Just(Nothing())
        )
        self.assertEqual(
            Maybe(img_tag1).f_apply(get('src')).f_apply(get('data-src')),
            Just(Nothing())
        )
    
    def test_a_apply_chaining(self):
        just_elm = Maybe(img_tag1)
        just_morph1 = Maybe(get('data-src'))
        just_morph2 = Maybe(get('src'))
        res1 = Maybe(img_tag1).a_apply(Maybe(get('data-src')))
        res2 = res1.a_apply(Maybe(get('src')))


        print()
        print("res1:", type(res1), res1)
        print("res2:", type(res2), res2)
        print()
        import ipdb
        ipdb.set_trace()
        print()
        

        self.assertEqual(
            Maybe(img_tag1).a_apply(Maybe(get('data-src'))).a_apply(Maybe(get('src')))
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

    def test_m_apply(self):
        just_elm = Maybe(img_tag1)
        constructor1 = getter_bind('src')
        constructor2 = getter_bind('data-src')
