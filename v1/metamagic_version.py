#!/usr/bin/env python3
"""
Next-steps:
(1) See if I can remove need for a metaclass, by 
(2) See if I can move ListObject/ListMorphism methods onto CategoryObject/CategoryMorphism 
(3) Try to incorporate a_map and a_apply
    Which might be handling nesting
(4) EXPERIMENT: try removing the 'join' from last step of f_apply and a_apply


amap(function, element) --> destructure 'function', and fmap each destructured func over 'element'


End goal:
* New file: category.py: category.Category, category.Object, category.Morphism
* 

"""


class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class CategoryMeta(type):
    """Placeholder"""

class CategoryObject:
    """Placeholder
    @todo: Move *everything* off of ListObject, and into this.
    """
    def f_apply(self, function):
        return self.category.f_apply(self.category, self, function)

    def zero(self):
        return self.category.zero()

    def append(self, value):
        return self.category.append(self, value)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(repr(elm) for elm in self.data)
        )

class CategoryMorphism:
    """Placeholder
    @todo: Move *everything* off of ListMorphism, and into this.
    """
    def a_map(self):
        return self.category.a_map(self.category, self)

    # def __call__(self, *args, **kwargs):
    #     return self.f_map()(*args, **kwargs)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(repr(elm) for elm in self.data)
        )

    

class ListMeta(type):
    """
    Serious question: should these functions refer to each other directly, or through the proxy of the element?
        Proxy:
            accumulator.append(function(elm))
        Direct:
            cls.append(accumulator, function(elm))

    """

    def f_apply(cls, element, function):
        accumulator = cls.zero(cls)
        for elm in element.data:
            accumulator = cls.append(cls, accumulator, function(elm))
        return cls.join(cls, accumulator)

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
            # if isinstance(elm, List):
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

    # For some reason, classproperty(ListMeta) doesn't work when it's not the metaclass
    # category = classproperty(ListMeta)
    category = ListMeta


# class ListObject(CategoryObject, ListBase, metaclass=ListMeta):
class ListObject(CategoryObject, ListBase):
    pass
    # def f_apply(self, function):
    #     return self.category.f_apply(self.category, self, function)

    # def zero(self):
    #     return self.category.zero()

    # def append(self, value):
    #     return self.category.append(self, value)

    # def __repr__(self):
    #     return "{0}({1})".format(
    #         self.__class__.__name__,
    #         ", ".join(repr(elm) for elm in self.data)
    #     )


# class ListMorphism(CategoryMorphism, ListBase, metaclass=ListMeta):
class ListMorphism(CategoryMorphism, ListBase):
    """
    f_map is not meaningfully defined for this, because f_map expects
    to take a bare *single* function.
    """

    # def a_map(self):
    #     return self.category.a_map(self.category, self)

    # # def __call__(self, *args, **kwargs):
    # #     return self.f_map()(*args, **kwargs)

    # def __repr__(self):
    #     return "{0}({1})".format(
    #         self.__class__.__name__,
    #         ", ".join(repr(elm) for elm in self.data)
    #     )


#=============
# Unit-tests
#==============
import unittest

class TestList(unittest.TestCase):
    def test_zero(self):
        nul = ListMeta.zero(ListMeta)
        self.assertEqual(nul.data, tuple())

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
            (-1, 3, 0, 4, 1, 5)
        )
        # list_f = ListMorphism(double)

    # def test_nested(self):
    #     list_nested = ListObject(1, 2, ListObject(3, 4))
    #     add2 = lambda num: num+2
    #     result = list_nested.f_apply(add2)
    #     self.assertEqual(
    #         result.data,
    #         (3, 4, (5, 6))
    #     )
    #     # ... fails


    # def test_bind_single(self):
    #     _addtwo = lambda elm: elm + 2
    #     L_addtwo = lambda elm: List(_addtwo(elm))
    #     _list = List(1, 2, 3)
    #     result = _list.bind(L_addtwo)
    #     expected_data = tuple([_addtwo(elm) for elm in _list.data])
    #     self.assertEqual(result.data, expected_data)

    # def test_bind_double(self):
    #     _double = lambda elm: (elm, elm.upper())
    #     L_double = lambda elm: List(*_double(elm))
    #     _list = List('a', 'b', 'c')
    #     result = _list.bind(L_double)
    #     expected_data = tuple([sub for elm in _list for sub in _double(elm)])
    #     self.assertEqual(result.data, expected_data)





if __name__ == "__main__":
    unittest.main()
