"""
Stubs for convenience functions for creating versions of Category/Element/Morphism
with 'standard' level behavior. These are intended to exist just enough
to get the example functors/monads/categories done.

Right now, these are stubs - and will need to be replaced with metaclass-type
things later (augmented/standard_sugar.py).
Inspiration for those metaclasses should be drawn from typing.py.
"""
from typing import Any, Callable

# from ...support.methods import abstractclassproperty
from ...support.typecheckable import TypeCheckableMeta
from .category import Category, Element, Morphism


# ===================================
#   Metaclass approach
#
# ===================================

class SimpleBaseMeta(TypeCheckableMeta):
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

    def __init__(self, *args, **kwargs):
        pass


class SimpleMeta(SimpleBaseMeta):
    def __new__(cls, name, base=Any):
        self =  super().__new__(cls, name, tuple([Element]), {})
        self._instancechecker_data = (base, )
        self._subclasschecker_data = (base, )
        return self

    # Predefined type-checking proxies
    def __instancecheck__(cls, instance):
        # Hack: to make this play well with typing.Any, etc
        return issubclass(type(instance), cls._instancechecker_data)

    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, cls._subclasschecker_data)


class SimpleElement(SimpleBaseMeta):
    def __new__(cls, name='Element', base=Any):
        self = super().__new__(cls, name, tuple([Element]), {})
        self._instancechecker_data = (base, )
        self._subclasschecker_data = (base, )
        return self


class SimpleMorphism(SimpleBaseMeta):
    def __new__(cls, name='Morphism', base=Callable[[Any], Any]):
        self = super().__new__(cls, name, tuple([Morphism]), {})
        self._instancechecker_data = (base, )
        self._subclasschecker_data = (base, )
        return self


class SimpleCategory(SimpleBaseMeta):
    def __new__(cls, name='Category', element_type=Any, morphism_type=Callable[[Any], Any]):
        if issubclass(element_type, Element):
            element = element_type
        else:
            element = SimpleElement(name=name+'Element', base=element_type)

        if issubclass(morphism_type, Morphism):
            morphism = morphism_type
        else:
            morphism = SimpleMorphism(name=name+'Morphism', base=morphism_type)

        self = super().__new__(cls, name, tuple([Category]),
                               {'Element': element, 'Morphism': morphism})
        return self
