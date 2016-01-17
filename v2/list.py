"""
Mid-refactor:
* translate List() functions to classmethods
* Change references inside List methods to proxy through objects


Next-steps:
* Put zero/append/join on both Morphism AND Object
* Make List() function as a constructor, with dispatching based on callable/not-callable
* Get something to handle nesting (a_apply?)
* EXPERIMENT: try removing the 'join' from last step of f_apply and a_apply
* EXPERIMENT: PROBABLY MORE ACCURATE: Change Object/Morphism to proxying through self.METHOD, instead of self.category.METHOD
* Get RECURSE: situated in category.py, *if-possible* ... assuming I can't get a_map to do it

amap(function, element) --> destructure 'function', and fmap each destructured func over 'element'


End goal:
* New file: category.py: category.Category, category.Object, category.Morphism
* 

"""

import category


class List(category.Category):
    """
    Serious question: should these functions refer to each other directly, or through the proxy of the element?
        Proxy:
            accumulator.append(function(elm))
        Direct:
            cls.append(accumulator, function(elm))

    """
    # @classmethod
    def f_apply(cls, element, function):
        accumulator = cls.zero(cls)
        for elm in element.data:
            accumulator = cls.append(cls, accumulator, function(elm))
        # return cls.join(cls, accumulator)
        return accumulator

    # @classmethod
    def f_map(cls, function):
        def wrapped(element):
            return cls.f_apply(cls, element, function)
        return wrapped

    def a_apply(cls, element, morphism):
        """
        morphism is a function(s) wrapped in List
        """
        accumulator = cls.zero(cls)
        for func in morphism.data:
            accumulator = cls.append(cls, accumulator, cls.f_apply(cls, element, func))
        return cls.join(cls, accumulator)

    def a_map(cls, morphism):
        def wrapped(element):
            return cls.a_apply(cls, element, morphism)
        return wrapped

    def zero(cls):
        return ListObject()

    def append(cls, element, value):
        accumulator = cls.zero(cls)
        accumulator.data = element.data + (value, )
        return accumulator

    def join(cls, element):
        """ ~ flatten """
        accumulator = cls.zero(cls)
        for elm in element.data:
            if isinstance(elm, ListBase):
                for inner_elm in elm.data:
                    accumulator = cls.append(cls, accumulator, inner_elm)
            else:
                accumulator = cls.append(cls, accumulator, elm)
        return accumulator


class ListBase:
    """
    Used for pattern-recognition. All List Objects/Morphisms are instances of this.
    Should properly just be called ~~'List'~~

    @todo: see what I can move from ListObject and ListMorphism, into this.
    """
    def __init__(self, *elements):
        self.data = elements

    category = List

    def __iter__(self):
        return iter(self.data)


class ListObject(category.Object, ListBase, metaclass=List):
# class ListObject(category.Object, ListBase):
    """
    A more structured version of this might be referenced simply List.Object
    """


class ListMorphism(category.Morphism, ListBase, metaclass=List):
# class ListMorphism(category.Morphism, ListBase):
    """
    A more structured version of this might be referenced simply List.Object
    """


#=============
# Unit-tests
#==============
import unittest

class TestList(unittest.TestCase):
    def test_zero(self):
        nul = List.zero(List)
        self.assertEqual(nul.data, tuple())

    def test_eq(self):
        one = ListObject(3, 4, 5)
        two = ListObject(*[elm+2 for elm in (1, 2, 3)])
        self.assertEqual(one, two)

    def test_f_apply(self):
        nums = (1, 2, 3)
        add2 = lambda num: num + 2
        list_o = ListObject(*nums)
        list_f = ListMorphism(add2)
        result = list_o.f_apply(add2)
        self.assertEqual(
            result.data,
            tuple([add2(elm) for elm in nums])
        )

    def test_a_map(self):
        nums = (1, 2, 3)
        add2 = lambda num: num + 2
        list_o = ListObject(*nums)
        list_f = ListMorphism(add2)
        result = list_f.a_map()(list_o)
        self.assertEqual(
            result.data,
            tuple([add2(elm) for elm in nums])
        )

    def test_call(self):
        nums = (1, 2, 3)
        add2 = lambda num: num+2
        list_o = ListObject(*nums)
        list_f = ListMorphism(add2)
        result = list_f(list_o)
        self.assertEqual(
            result.data,
            tuple([add2(elm) for elm in nums])
        )

    def test_doubler(self):
        """Different type signature of function
        constructor function::(a -> m b)
        """
        nums = (1, 2, 3)
        double = lambda obj: ListObject(obj-2, obj+2)
        list_o = ListObject(*nums)
        result = list_o.f_apply(double)
        self.assertEqual(
            result.data,
            (ListObject(-1, 3), ListObject(0, 4), ListObject(1, 5))
        )

    def test_nested(self):
        list_nested = ListObject(1, 2, ListObject(3, 4))
        add2 = lambda num: num+2
        self.assertRaises(TypeError,
            lambda : list_nested.f_apply(add2)
        )
        self.assertEqual(
            list_nested.f_apply(category.apply_recursively(add2)),
            ListObject(3, 4, ListObject(5, 6))
        )
    
    def test_a_apply(self):
        list_o = ListObject(1, 2, 3)
        list_f = ListMorphism(lambda num: num + 2, lambda num: num - 2)
        self.assertEqual(
            list_o.a_apply(list_f),
            ListObject(3, 4, 5, -1, 0, 1)
        )

    def test_compare_f_map_to_f_apply(self):
        list_o = ListObject("a", "bb", "ccc")
        repeat = lambda obj: obj+obj
        self.assertEqual(
            list_o.f_apply(repeat),
            List.f_map(List, repeat)(list_o)            
        )


    def test_compare_a_map_to_a_apply(self):
        list_o = ListObject(3, 4, 5)
        list_f = ListMorphism(lambda num: num + 2,
                              lambda num: num - 2,
                              lambda num: num * 3)
        self.assertEqual(
            list_o.a_apply(list_f),
            list_f.a_map()(list_o)
        )




if __name__ == "__main__":
    unittest.main()
