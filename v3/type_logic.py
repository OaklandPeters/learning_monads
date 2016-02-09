"""
Drafting TypeLogic, without reference to category.
In order to get the 3-category construction correct


Next-steps:
* Fixup operator: pipe: ~ compose, given that element A ~== () -> A, so: pipe  Morphism >> Morphism -> Compose, Element >> Morphism -> Apply
* Fixup operator: traverse: <<
* Consider rule: operators (1) may polymorphic on the calss of Element and Morphism, and (2) operators should lifting or fmaping the RHS arguments
* Consider making Element -> Monoid, so '+' can be used to fill in arguments


Rewrite plan:
* collapse --> traverse(cls, obj, applicative):
* Traversable: .traverse(cls, obj: CallTreeObject, functor: Applicative), , then Traversable interface stub
* Write CallTree (~FunctionMonad with only positional arguments) generalization


Call Tree  (~FunctionMonad)
Sugar for LogicalInterface
Traversable via Bisection on Isinstance/IsSubclass  (new Applicative Functors)

Functor Bisection Rule ==> Monad is Traversable by the original Applicative Functor.
Might be rephrasable as we can always lift F_D,C to F_M,C

"""
import typing
import functools

from support_pre import (
    classproperty,
    type_check, type_check_sequence,
    standard_repr, standard_str,
    TypeCheckableMeta
)
import category


class TypeLogicDomain(category.Category):
    Element = type
    Morphism = typing.Callable[[bool], bool]


class TypeLogicCodomain(category.Category):
    Element = bool
    Morphism = typing.Callable[[bool], bool]


Translator = typing.Callable[[TypeLogicDomain.Element], TypeLogicCodomain.Element]


class TypeLogic(category.Category):
    """
    Unconventional monad, in that the Domain Elements and Morphisms don't line up.
    """
    def __new__(cls, value):
        return cls.a_lift(value)

    @classmethod
    def a_lift(cls, value):
        return TypeLogicElement(value)

    @classmethod
    def f_apply(cls, function, *elements: 'Tuple[cls.Category.Element]') -> 'cls.Category.Morphism':
        return TypeLogicMorphism(function, *elements)

    @classmethod
    def f_map(cls, function):
        """This format may not be valid."""
        return TypeLogicMorphism(function)

    @classmethod
    def collapse(cls, obj: 'TypeLogicObject', translator: Translator) -> 'cls.Codomain.Element':
        """
        Use translator function (a functor?) to translate the monad structure into the Codomain.
        I suspect this is 'traverse'
        To turn functor: F_DC (domain->codomain) into F_MC (monad->codomain),
            this uses the following rule:
        def functor_lift(applicative: Applicative:
            def lifted(obj: TypeLogicObject) -> CodomainObject:
                if isinstance(obj, TypeLogicElement):
                    # Is this f_map?
                    return 
                    obj.function
                isinstance(obj, TypeLogicMorphism):
                    # Is this a_apply?
                    # Map over interior
                    return obj.function()

        """
        type_check(obj, *(TypeLogicElement, TypeLogicMorphism))
        if isinstance(obj, TypeLogicMorphism):
            return obj.function(
                *(element.collapse(translator)
                  for element in obj.elements)
            )
        elif isinstance(obj, TypeLogicElement):
            return translator(obj.value)
        else:
            raise TypeError("This should never happen.")

        #obj.function(*(element.collapse(translator) for element in obj.elements))


    #
    #   Type-checking Kruft
    #
    @classproperty
    def Domain(cls):
        return TypeLogicDomain

    @classproperty
    def Codomain(cls):
        return TypeLogicCodomain

    @classproperty
    def Category(cls):
        """This is the category of the monad itself."""
        return TypeLogic


#====================
# Sugar Methods
#====================
def Or(left: bool, right: bool) -> bool:
    return left or right

def And(left: bool, right: bool) -> bool:
    return left and right

def Not(left: bool) -> bool:
    return not left

def AndNot(left: bool, right: bool) -> bool:
    return left and not right

def Compose(left: typing.Callable, right: typing.Callable) -> typing.Callable:
    @functools.wraps(left)
    def wrapper(*args, **kwargs):
        return left(right(*args, **kwargs))
    return wrapper

def isinst(value) -> typing.Callable[[typing.Any], typing.Callable[[type], bool]]:
    def isinst_klass(klass) -> bool:
        return isinstance(value, klass)
    return isinst_klass



class TypeLogicSugar(metaclass=TypeCheckableMeta):
#class TypeLogicSugar:
    """Stub. This will have to be inherited by the Element and Morphism classes
    in order to work.
    """
    def __or__(self, right):
        return self.Category.f_apply(Or, self, self.Category.a_lift(right))

    def __and__(self, right):
        return self.Category.f_apply(And, self, self.Category.a_lift(right))

    def __sub__(self, right):
        return self.Category.f_apply(AndNot, self, self.Category.a_lift(right))
        # return cls.f_apply(And(left, cls.f_apply(Not, right) ))
    
    def __invert__(self):
        return self.Category.f_apply(Not, self.Category.a_lift(self))

    def __rshift__(self, translator: Translator):
        return self.collapse(translator)


#===================
# Monad Category
#===================
class TypeLogicMorphism(TypeLogicSugar):
    def __init__(self, function, *elements):
        type_check_sequence(elements, TypeLogicElement)
        self.function = function
        self.elements = elements

    def __str__(self):
        return standard_str(self, standard_str(self.function, self.elements))

    def __repr__(self):
        return standard_repr(self, standard_repr(self.function, self.elements))


    def f_apply(self, *elements):
        return self.Category.f_apply(self, *elements)

    def collapse(self, translator: Translator) -> bool:
        return self.Category.collapse(self, translator)

    @classproperty
    def Category(cls):
        return TypeLogic

    # Morphism specific sugar
    def __xor__(self, other: 'TypeLogicMorphism') -> 'TypeLogicMorphism':
        return self.Category.f_apply(Compose, self, self.Category.f_map(other))

    def __call__(self, *elements):
        """This is a weird definition of call. I'm not very confident about it.
        It basically provides partials/currying.
        """
        return self.Category.f_apply(self.function, *(self.elements + elements))
        #return self.Category.f_apply(self.function, *elements)



class TypeLogicElement(TypeLogicSugar):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        #return str.format("{0}({1}", self.__class__.__name__, self.value)
        return standard_repr(self, self.value)

    def __str__(self):
        return "<{0}>".format(self.value)

    def collapse(self, translator: Translator) -> bool:
        return self.Category.collapse(self, translator)
        #return translator(self.value)

    @classproperty
    def Category(cls):
        return TypeLogic


TypeLogicObject = typing.Union[TypeLogicElement, TypeLogicMorphism]


#==================
#  Traversable
#==================
class IsInstance(category.Functor[TypeLogicCategory, TypeLogicCodomain]):
    def __init__(self, value):
        self.value

    def __call__(self, klass):
        return isinstance(self.value, klass)

    # This will need some function to handle dispatching over morphism/element

    def a_lift(self):
        pass

    def f_map(self, morphism: TypeLogicMorphism) -> TypeLogicCodomain.Morphism:
        # make a boolean function
        # capturing behavior of morphism.function
        # Will have to do something to collapse .elements



#==================
#   Unit Tests
#==================
import unittest
import operator

TL = TypeLogic
Sequence = typing.Sequence
Mapping = typing.Mapping


class TypeLogicTests(unittest.TestCase):

    def test_simple(self):
        """Lifting a single class. No composition."""
        def confirm(value, klass, expected):
            self.assertEqual(
                TL.a_lift(klass).collapse(isinst(value)),
                expected
            )
        confirm("", str, True)
        confirm(12, str, False)
        class Stringy(str):
            pass
        confirm(Stringy("k"), str, True)
        confirm("", Sequence, True)
        confirm([], Sequence, True)
        confirm({}, Sequence, False)

    def test_morphism(self):
        inner = TL.f_apply(Or, TL.a_lift(Sequence), TL.a_lift(Mapping))
        self.assertEqual(inner >> isinst([]), True)
        self.assertEqual(inner >> isinst(12), False)
        self.assertEqual(inner >> isinst(""), True)

    def test_desired_syntax(self):
        checkit = (TL(Sequence) | Mapping) - str
        expected = (
            ("aa", False),
            (["aa"], True),
            ((1, 2), True),
            (12, False),
            ({'first': 'name'}, True),
        )
        for _input, result in expected:
            self.assertEqual(checkit >> isinst(_input), result)


    def test_desired_syntax_without_sugar(self):
        checkit = (
            TL.f_apply(
                AndNot,
                TL.f_apply(
                    Or,
                    TL.a_lift(Sequence),
                    TL.a_lift(Mapping)
                ),
                TL.a_lift(str)
            )
        )
        inner = TL.f_apply(Or, TL.a_lift(Sequence), TL.a_lift(Mapping))    
        expected = (
            ("aa", False),
            (["aa"], True),
            ((1, 2), True),
            (12, False),
            ({'first': 'name'}, True),
        )

        for _input, result in expected:
            self.assertEqual(checkit.collapse(isinst(_input)), result)


    def test_f_map_f_apply_equivalency(self):
        """
        Ensure
        f_map(function)(*elements) == f_apply(function, *elements)
        """
        elements = (TL.a_lift(Sequence), TL.a_lift(Mapping))
        function = Or
        fmap = TL.f_map(function)(*elements)
        fapp= TL.f_apply(function, *elements)

        for _tran in [isinst({}), isinst([]), isinst(12)]:
            self.assertEqual(fmap.collapse(_tran), fapp.collapse(_tran))




    #def test_chaining(self):
    #    t_or = TL.f_map(Or)(TL(Sequence))
    #    t_or_not = t_or ^ Not
    #    t_or_not_str = t_or_not(TL(str))


    #    print()
    #    print("t_or_not_str:", type(t_or_not_str), t_or_not_str)
    #    print()
    #    import ipdb
    #    ipdb.set_trace()
    #    print()
        

if __name__ == "__main__":
    unittest.main()
