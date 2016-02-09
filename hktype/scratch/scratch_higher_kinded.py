"""
KEY DEVELOPMENT HERE:
The ability of a type in a signature to be resolved relative to properties on the class.

class Functor(CorrectedGeneric[Codomain, Domain]):
    def f_map(cls, function: This.Domain.Comorphism) -> This.Codomain.Morphism:

ANOTHER POSSIBILITY:
IN _annotations_corrector: if higher-kinded:
    clsspace = chainmap(namespace, *bases)
    concrete = higher_kinded_func(clsspace)
... this needs to happen AFTER replacing
... this is more appropriate for static analysis

But the __annotations__ getter is more Pythonic

WRITE BOTH


Attempting to turn annotations into a getter
"""
import typing
import operator
import copy
import collections



class Annotations(dict):
    pass


class ThisType:
    """Basically the same as fn '_'
    Tryout:
    This.Domain.Morphism
    """
    def __init__(self, function=None):
        self.function = function

    @classmethod
    def _lift(cls, value):
        return cls(value)

    def _bind(self, function):
        return self._lift(lambda value: function(self(value)))

    def __getitem__(self, key):
        lambda value: value.__annotations__[key]
        return self._bind(operator.getitem(key))

    def __getattr__(self, name):
        return self._bind(operator.attrgetter(name))

    def __call__(self, value):
        if self.function == None:
            return value
        return self.function(value)
This = ThisType()


def _annotations_corrector(function, bases, parameters):
    """
    """
    annotations = typing.get_type_hints(function)    
    accumulator = dict()
    for key, value in annotations.items():
        # If it is an unfilled typevar
        if isinstance(value, typing.TypeVar):
            # Find parent with generic version of this parameter
            position = None
            for parent in bases:
                if value in getattr(parent, '__parameters__', []):
                    position = parent.__parameters__.index(value)
            if position is None:
                raise ValueError("Could not find position in __parameters__ of parent classes")

            # If this is a structured reference, resolve it
            if _is_structured_forward_ref(value):
                base = parameters[position]
                tinyns = {value._structured_forward_ref_name: parameters[position]}
                # my_lambda = "lambda {0}: {1}".format(value._structured_forward_ref_name, value._structured_forward_ref_code)
                concrete = eval(value._structured_forward_ref_code, tinyns)                
            else:
                concrete = parameters[position]

            accumulator[key] = concrete
        else:
            accumulator[key] = value
    return accumulator

def namespace_annotations_corrector(bases, namespace, parameters):
    """
    This mutates, which is annoying, but copying everything would be slow.
    """
    # Replace type-variables
    for name, value in namespace.items():
        _update_annotations(value, bases, parameters)
    # Replace higher kinded types
    return namespace

def _update_annotations(value, bases, parameters):
    if hasattr(value, '__annotations__'):
        annotations = typing.get_type_hints(value)
        corrected = _annotations_corrector(value, bases, parameters)            
        value.__annotations__ = corrected
        return value
    # wrapped functions, such as classmethods
    # NOTE: this may have to handle recursive descent
    elif hasattr(value, '__func__'):
        return _update_annotations(value.__func__, bases, parameters)

def update_higher_kinded(cls):    
    namespace = vars(cls)
    for name, value in namespace.items():
        _update_higher_kinded(name, value, cls)    
    return cls


def _update_higher_kinded(name, value, cls):
    if hasattr(value, '__annotations__'):
        annotations = typing.get_type_hints(value)
        corrected = _annotations_higher_kinded(annotations, cls)
        value.__annotations__ = corrected
        return value
    # wrapped functions, such as classmethods
    # NOTE: this may have to handle recursive descent
    elif hasattr(value, '__func__'):
        return _update_higher_kinded(name, value.__func__, cls)    

def _annotations_higher_kinded(annotations, cls):
    accumulator = Annotations()
    # If it is concrete
    if all(not isinstance(para, typing.TypeVar) for para in cls.__parameters__):
        for p_key, p_value in annotations.items():
            if isinstance(p_value, ThisType):
                accumulator[p_key] = p_value(cls)
            else:
                accumulator[p_key] = p_value
        return accumulator
    # If it still has unfilled type-variables
    else:
        return annotations


class CorrectedGenericMeta(typing.GenericMeta):
    def __new__(mcls, name, bases, namespace, *args, **kwargs):
        parameters = kwargs.get('parameters', tuple())        
        if parameters and all(not isinstance(value, typing.TypeVar) for value in parameters):
            namespace = namespace_annotations_corrector(bases, namespace, parameters)
        cls = typing.GenericMeta.__new__(mcls, name, bases, namespace, *args, **kwargs)
        cls = update_higher_kinded(cls)
        return cls

class CorrectedGeneric(typing.Generic, metaclass=CorrectedGenericMeta):
    pass





#
#
#   Testing an example
#
#
class classproperty(object):
    """Read-only."""
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class abstractclassproperty(classproperty):
    """abstract check happens in __init__, and only for classes
    descending from metaclass=abc.ABCMeta. If abstract methods have not
    been concretely implemented, will raise TypeError.
    """
    __isabstractmethod__ = True

class Category:
    """Placeholder"""
    @abstractclassproperty
    def Element(cls):
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls):
        return Expected
        # return NotImplemented

class AnyCategory(Category):
    Element = typing.Any
    Morphism = typing.Callable

class ListCategory(Category):
    Element = list
    Morphism = typing.Callable[[list], list]


Codomain = typing.TypeVar('Codomain')
Domain = typing.TypeVar('Domain')

# ElementType = typing.TypeVar('ElementType')
# MorphismType = typing.TypeVar('MorphismType')
# class Domain(CorrectedGeneric[ElementType, MorphismType]):
#     @classproperty
#     def Element(cls) -> ElementType:
#         return NotImplemented
#     @classproperty
#     def Morphism(cls) -> MorphismType:
#         return NotImplemented

def _resolver(forward_code, globalns, localns):
    if globalns is None and localns is None:
        globalns = localns = {}
    elif globalns is None:
        globalns = localns
    elif localns is None:
        localns = globalns
    return typing._type_check(
        eval(forward_code, globalns, localns),
        "Forward references must evaluate to types.")


class CleverForward(typing._ForwardRef):
    """When is the forward replaced?
    Ah, realization..., eval_type replaces the string, with a concrete type.
    That concrete type is later replaced
    """
    def _eval_type(self, globalns, localns):
        code_str = self.__forward_arg__
        parts = code_str.split('.')
        name = parts[0]


        print()
        print("localns.keys():", type(localns.keys()), localns.keys())
        print()
        import ipdb
        ipdb.set_trace()
        print()
        

        rfront = _resolver(name, globalns, localns)
        structured = structured_forward_ref(rfront, name, code_str)
        return structured
        
        # resolved = super()._eval_type(globalns, localns)
        # return resolved

def _is_structured_forward_ref(obj):
    return hasattr(obj, '_structured_forward_ref_name')

def structured_forward_ref(type_var: typing.TypeVar, name:str, code: str):
    """I might need to copy here, becuase I don't know if mutating
    klass (typing.TypeVar ~Domain) will potentially mutate other versions
    of it
    ... I would create a subclass here if they would let me subclass TypeVar ...
    """
    
    structured = copy.deepcopy(type_var)
    setattr(structured, '_structured_forward_ref_name', name)
    setattr(structured, '_structured_forward_ref_code', code)
    return structured

CF = CleverForward


class HigherKinded:
    def __init__(self, code):
        self.code = code


# class Functor(typing.Generic[Codomain, Domain]):
class Functor(CorrectedGeneric[Codomain, Domain]):
    @classproperty
    def Codomain(cls):
        return cls.__parameters__[0]

    @classproperty
    def Domain(cls):
        return cls.__parameters__[1]

    # def lister(cls) -> HigherKinded("This.f_map['return']"):
    #     return NotImplemented

    def getter(cls) -> This.Domain.Element:
        return cls.Domain.Element()

    # @classmethod
    def f_map(cls, function: CF('Domain.Morphism')) -> CF('Codomain.Morphism'):
    # def f_map(cls, function: 'Codomain.Morphism') -> 'Domain.Morphism':
    # def f_map(cls, function: Codomain) -> Domain:
    # def f_map(cls, function: 'Codomain') -> 'Domain':
    # def f_map(cls, function: Domain) -> Domain:
        return NotImplemented

    @classmethod
    def f_apply(cls, element: CF('Codomain.Element'), function: CF('Domain.Morphism')) -> CF('Codomain.Element'):
        return NotImplemented



class ListFunctor(Functor[AnyCategory, ListCategory]):
    """
    Waht I really want is for the forward refs on f_map to resolve themselves
    in the context of ListFunctor (which has provided values for Codomain and Domain)
    """
    pass


class HigherTypeVar(typing.TypeVar, _root=True):
    pass

anno_getter = typing.get_type_hints(ListFunctor.getter)
anno_map = typing.get_type_hints(ListFunctor.f_map)
anno_apply = typing.get_type_hints(ListFunctor.f_apply)


print()
print("anno_map:", type(anno_map), anno_map)
print("anno_apply", type(anno_apply), anno_apply)
print("anno_getter:", type(anno_getter), anno_getter)
print()
import ipdb
ipdb.set_trace()
print()


import unittest

class ThisTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(This(ListFunctor), ListFunctor)
        self.assertEqual(This.Domain(ListFunctor), ListFunctor.Domain)
        self.assertEqual(This.Domain.Morphism(ListFunctor), ListFunctor.Domain.Morphism)
