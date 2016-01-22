import typing

import category
from category import classproperty

class ListCategory(category.Category):
    """
    """
    @classmethod
    def f_apply(cls, element, function):
        accumulator = element.zero()
        for elm in element.data:
            accumulator = accumulator.append(function(elm))
        # I don't recall if f_apply/f_map should trigger flattening/join
        # return cls.join(cls, accumulator)
        return accumulator

    @classmethod
    def f_map(cls, function):
        def wrapped(element):
            return cls.f_apply(element, function)
        return wrapped

    @classmethod
    def a_apply(cls, element, morphism):
        """
        morphism is a function(s) wrapped in List
        """
        accumulator = element.zero()
        for func in morphism.data:
            accumulator = accumulator.append(element.f_apply(func))
        return accumulator.join()

    @classmethod
    def a_map(cls, morphism):
        def wrapped(element):
            return element.a_apply(morphism)
        return wrapped

    @classmethod
    def m_apply(cls, element, constructor):
        """
        Basically Haskell's 'bind'
        In this context, a constructor means a function taking
        arguments from the domain category, into the monad's category.
        constructor::(a -> m b)
        """
        return element.f_apply(constructor).join()

    @classmethod
    def m_map(cls, constructor):
        """
        """
        def wrapped(element):
            return element.m_apply(constructor)
        return wrapped

    @classmethod
    def zero(cls):
        return ListElement()

    @classmethod
    def append(cls, element, value):
        accumulator = element.zero()
        accumulator.data = element.data + (value, )
        return accumulator

    @classmethod
    def join(cls, element):
        """ ~ flatten """
        accumulator = element.zero()
        for elm in element.data:
            if isinstance(elm, List):
                for inner_elm in elm.data:
                    accumulator = accumulator.append(inner_elm)
            else:
                accumulator = accumulator.append(elm)
        return accumulator


class List(category.Monad):
    """
    Used for type-checking, pattern recognition, and it's constructor
    """
    def __new__(cls, *elements):
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
            if all(isinstance(elm, typing.Callable) for elm in elements):
                self = object.__new__(cls.Morphism)
            else:
                self = object.__new__(cls.Element)
        self.__init__(*elements)
        return self


    def __init__(self, *elements):
        self.data = elements

    @classproperty
    def Category(cls):
        return ListCategory

    @classproperty
    def Element(cls):
        return ListElement

    @classproperty
    def Morphism(cls):
        return ListMorphism

    def __iter__(self):
        return iter(self.data)

    def __eq__(self, other):
        if hasattr(other, 'Category'):
            if (issubclass(self.Category, other.Category)
                or issubclass(other.Category, self.Category)):
                return self.data == other.data
        else:
            return False

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(repr(elm) for elm in self.data)
        )


class ListElement(category.Element, List):
    """
    A more structured version of this might be referenced simply List.Element
    """


class ListMorphism(category.Morphism, List):
    """
    A more structured version of this might be referenced simply List.Element
    """


#=============
# Unit-tests
#==============
import unittest

class TestList(unittest.TestCase):
    def test_zero(self):
        nul = ListCategory.zero()
        self.assertEqual(nul.data, tuple())

    def test_eq(self):
        one = ListElement(3, 4, 5)
        two = ListElement(*[elm+2 for elm in (1, 2, 3)])
        self.assertEqual(one, two)

    def test_f_apply(self):
        nums = (1, 2, 3)
        add2 = lambda num: num + 2
        list_o = ListElement(*nums)
        list_f = ListMorphism(add2)
        result = list_o.f_apply(add2)
        self.assertEqual(
            result.data,
            tuple([add2(elm) for elm in nums])
        )

    def test_a_map(self):
        nums = (1, 2, 3)
        add2 = lambda num: num + 2
        list_o = ListElement(*nums)
        list_f = ListMorphism(add2)
        result = list_f.a_map()(list_o)
        self.assertEqual(
            result.data,
            tuple([add2(elm) for elm in nums])
        )

    def test_call(self):
        nums = (1, 2, 3)
        add2 = lambda num: num+2
        list_f = ListMorphism(add2)
        result = list_f(*nums)
        self.assertEqual(result, ListElement(3, 4, 5))

    def test_constructor(self):
        """Different type signature of function
        constructor function::(a -> m b)
        """
        nums = (1, 2, 3)
        double = lambda obj: ListElement(obj-2, obj+2)
        list_o = ListElement(*nums)
        result = list_o.f_apply(double)
        self.assertEqual(
            result,
            ListElement(ListElement(-1, 3), ListElement(0, 4), ListElement(1, 5))
        )

    def test_m_apply(self):
        nums = (1, 2, 3)
        double = lambda obj: ListElement(obj-2, obj+2)
        list_o = ListElement(*nums)
        result = list_o.f_apply(double)
        bound = list_o.m_apply(double)
        self.assertEqual(
            bound,
            ListElement(-1, 3, 0, 4, 1, 5)
        )
        self.assertEqual(
            result.join(),
            bound
        )

    def test_m_map(self):
        nums = (1, 2, 3)
        list_o = ListElement(*nums)
        double = lambda obj: ListElement(obj-2, obj+2)
        self.assertEqual(
            list_o.m_apply(double),
            ListCategory.m_map(double)(list_o),
        )

    def test_nested(self):
        list_nested = ListElement(1, 2, ListElement(3, 4))
        add2 = lambda num: num+2
        self.assertRaises(TypeError,
            lambda : list_nested.f_apply(add2)
        )
        self.assertEqual(
            list_nested.f_apply(category.apply_recursively(add2)),
            ListElement(3, 4, ListElement(5, 6))
        )
    
    def test_a_apply(self):
        list_o = ListElement(1, 2, 3)
        list_f = ListMorphism(lambda num: num + 2, lambda num: num - 2)
        self.assertEqual(
            list_o.a_apply(list_f),
            ListElement(3, 4, 5, -1, 0, 1)
        )

    def test_compare_f_map_to_f_apply(self):
        list_o = ListElement("a", "bb", "ccc")
        repeat = lambda obj: obj+obj
        self.assertEqual(
            list_o.f_apply(repeat),
            ListCategory.f_map(repeat)(list_o)            
        )


    def test_compare_a_map_to_a_apply(self):
        list_o = ListElement(3, 4, 5)
        list_f = ListMorphism(lambda num: num + 2,
                              lambda num: num - 2,
                              lambda num: num * 3)
        self.assertEqual(
            list_o.a_apply(list_f),
            list_f.a_map()(list_o)
        )

    def test_isinstance(self):
        list_o = ListElement('aaa', 'bbb')
        list_f = ListMorphism(sorted)
        self.assertIsInstance(list_o, List)
        self.assertIsInstance(list_o, ListElement)
        self.assertNotIsInstance(list_o, ListMorphism)
        self.assertIsInstance(list_f, List)
        self.assertIsInstance(list_f, ListMorphism)
        self.assertNotIsInstance(list_f, ListElement)

    def test_list_constructor_dispatch(self):
        list_o = List('aaa', 'bbb')
        list_f = List(sorted)
        self.assertIsInstance(list_o, ListElement)
        self.assertIsInstance(list_f, ListMorphism)        

if __name__ == "__main__":
    unittest.main()
