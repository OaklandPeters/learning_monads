"""
Drafting TypeLogic, without reference to category.
In order to get the 3-category construction correct

Except, this case isn't working out at all like I thought.
"""
import typing

from support_pre import classproperty
import category


class TLCategory(category.Category):
    Element = Element
    Morphism = Morphism



class TypeLogic:
    @classproperty
    def Category(cls):
        return TypeLogicCategory

    @classmethod
    def a_lift(cls, value):
        return TLElement(value)

    @classmethod
    def f_apply(cls, function, *values):
        return TLMorphism(
            function,
            values
        )

    @classmethod
    def bind(cls, obj: TLOBject, translator: Callable[[type], bool]):
        if isinstance(obj, cls.Category.Element):
            return translator(obj.value)
        elif isinstance(obj, cls.Category.Morphism):
            return obj.
        else:
            raise RuntimeError(str.format(
                "obj should be type Element ({0}) or Morphism ({1}), not {2}",
                cls.Category.Element, cls.Category.Morphism, type(obj)
            ))




class Domain(category.Category):
    Element = type
    Morphism = typing.Callable[[bool], bool]


class Codomain(category.Category):
    Element = bool
    Morphism = typing.Callable[[bool], bool]


class TLMorphism:
    def __init__(self, function, *values):
        self.function = function
        self.elements = elements

    def __repr__(self):
        return "{0}({1}({2}))".format(
            self.__class__.__name__,
            repr(self.function),
            ", ".join(repr(elm.value) for elm in self.elements)
        )


class TypeLogicElement:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def bind(self, translator):


class TypeLogicCategory(category.Category):
    Element = TypeLogicElement
    Morphism = TypeLogicMorphism



import unittest
import operator

TL = TypeLogic
Or = lambda left, right: left or right
Not = lambda left, right: left and not right
And = lambda left, right: left and right
Sequence = typing.Sequence
Mapping = typing.Mapping

class TypeLogicTests(unittest.TestCase):
    def test_desired_syntax(self):
        
        checkit = TL(Sequence) | Mapping - str
        expected = (
            ("aa", False),
            (["aa"], True),
            ((1, 2), True),
            (12, False),
            ({'first': 'name'}, True),
        )
        for _input, result in expected:
            self.assertEqual(checkit(_input), result)


    def test_desired_syntax_without_sugar(self):
        checkit = (
            TL.f_apply(
                Not,
                TL.f_apply(
                    Or,
                    TL.a_lift(Sequence),
                    TL.a_lift(Mapping)
                ),
                str
            )
        )
        # :: type -> bool
        isit = lambda value: lambda klass: isinstance(value, klass)
        checkit_call = lambda value: checkit.bind(isit(value))
        expected = (
            ("aa", False),
            (["aa"], True),
            ((1, 2), True),
            (12, False),
            ({'first': 'name'}, True),
        )
        for _input, result in expected:
            self.assertEqual(checkit_call(_input), expected)
