"""
Short-term-fixes:
* put this into a _structured_forward_ref_function
* Create ABC for StructuredForwardRef - with typechecker and mixin classmethods
* HIGHER-KINDED-TYPES: could do by changing them *after* cls is constructed in CleverGenericMeta

PLAN:
(1) Make Clever Resolver resolve it to an advanced type (StructuredForwardRef),
    which wraps the type and a lambda
(2) Make CleverGenericMeta, when it does replacements - also check


IMPROVEMENTS NEEDED:
    This does not affect classmethods for whatever reason.
"""
#import typing
import retyping as typing
import copy


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
    for name, value in namespace.items():
        _update_annotations(value, bases, parameters)
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



class CorrectedGenericMeta(typing.GenericMeta):
    def __new__(mcls, name, bases, namespace, *args, **kwargs):
        parameters = kwargs.get('parameters', tuple())        
        if parameters and all(not isinstance(value, typing.TypeVar) for value in parameters):
            namespace = namespace_annotations_corrector(bases, namespace, parameters)
        cls = typing.GenericMeta.__new__(mcls, name, bases, namespace, *args, **kwargs)
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
         return NotImplemented

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
    # @classproperty
    # def Codomain(cls):
    #     return cls.__parameters__[0]

    # @classproperty
    # def Domain(cls):
    #     return cls.__parameters__[1]

    # def lister(cls) -> HigherKinded("This.f_map['return']"):
    #     return NotImplemented

    # @classmethod
    # def f_map(cls, function: CF('Domain.Morphism')) -> CF('Codomain.Morphism'):
    # def f_map(cls, function: 'Codomain.Morphism') -> 'Domain.Morphism':
    def f_map(cls, function: Codomain) -> Domain:
        return NotImplemented
    # def f_map(cls, function: 'Codomain') -> 'Domain':
    # def f_map(cls, function: Domain) -> Domain:

    @classmethod
    def f_apply(cls, element: Codomain, function: Domain) -> Codomain:
    #def f_apply(cls, element: CF('Codomain.Element'), function: CF('Domain.Morphism')) -> CF('Codomain.Element'):
        return NotImplemented



class ListFunctor(Functor[AnyCategory, ListCategory]):
    """
    Waht I really want is for the forward refs on f_map to resolve themselves
    in the context of ListFunctor (which has provided values for Codomain and Domain)
    """
    pass



anno_map = typing.get_type_hints(ListFunctor.f_map)
anno_apply = typing.get_type_hints(ListFunctor.f_apply)


print()
print("anno_map:", type(anno_map), anno_map)
print("anno_apply", type(anno_apply), anno_apply)
print()
import ipdb
ipdb.set_trace()
print()
