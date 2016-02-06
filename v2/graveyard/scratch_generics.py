"""
Looking at how generic annotation can be accessed during inheritance

? Could this be fixed by using forward refs?
"""
import typing
import abc


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

class Expected:
    pass

class Category:
    """Placeholder"""
    @abstractclassproperty
    def Element(cls):
        return Expected
        # return NotImplemented

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

# Element = typing.TypeVar('Element')
# Morphism = typing.TypeVar('Morphism')

# class Category(typing.Generic[Element, Morphism]):
#     pass

# class Domain(Category):
#     Element = 'de'
#     Morphism = 'dm'

# class Codomain(Category):
#     Element = 'ce'
#     Morphism = 'cm'

# class AnyCategory(Category[typing.Any, typing.Callable]):
#     pass
# class ListCategory(Category[list, typing.Callable[[list], list]]):
#     pass


# Codomain = typing.TypeVar('Codomain', bound=Category)
# Domain = typing.TypeVar('Domain', bound=Category)



# Codomain = CategoryTypeVar('Codomain', bound=Category)
# Domain = CategoryTypeVar('Domain', bound=Category)
Codomain = typing.TypeVar('Codomain')
Domain = typing.TypeVar('Domain')

class Functor(typing.Generic[Codomain, Domain]):
    # @classproperty
    # def Codomain(cls):
    #     return cls.__parameters__[0]

    # @classproperty
    # def Domain(cls):
    #     return cls.__parameters__[1]

    @classmethod
    def f_map(cls, function: 'Codomain.Morphism') -> 'Domain.Morphism':
    # def f_map(cls, function: Codomain) -> Domain:
    # def f_map(cls, function: 'Codomain') -> 'Domain':
    # The PROBLEM: Codomain is a classproperty, and the getter isn't called/resolved on it
    
        return NotImplemented



class ListFunctor(Functor[AnyCategory, ListCategory]):
    """
    Waht I really want is for the forward refs on f_map to resolve themselves
    in the context of ListFunctor (which has provided values for Codomain and Domain)
    """
    pass

def resolve(cls, typevar):
    """
    result = resolve(ListFunctor, method, )
    """

def annotations_getter(cls, method_name):
    """
    Now... how to make this replace the __annotations__? Options
    (1) Look in the internals of typing.py
    (2) Run/replace on classes after construction
    (3) Somehow turn __annotations__ into a getter

    """
    method = getattr(cls, method_name)
    annotations = typing.get_type_hints(method)
    
    accumulator = dict()
    for key, value in annotations.items():
        # If it is an unfilled typevar
        if isinstance(value, typing.TypeVar):
            # Find parent with generic version of this parameter
            position = None
            for parent in cls.__mro__:
                if value in getattr(parent, '__parameters__', []):
                    position = parent.__parameters__.index(value)

            if position is None:
                raise ValueError("Could not find position in __parameters__ of parent classes")

            concrete = cls.__parameters__[position]
            accumulator[key] = concrete
        else:
            accumulator[key] = value

    return accumulator



anno = typing.get_type_hints(ListFunctor.f_map)
corrected = annotations_getter(ListFunctor, 'f_map')

print()
print("anno:", type(anno), anno)
print("corrected:", type(corrected), corrected)
print()
import ipdb
ipdb.set_trace()
print()


