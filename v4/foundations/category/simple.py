"""
Stubs for convenience functions for creating versions of Category/Element/Morphism
with 'standard' level behavior. These are intended to exist just enough
to get the example functors/monads/categories done.

Right now, these are stubs - and will need to be replaced with metaclass-type
things later (augmented/standard_sugar.py).
Inspiration for those metaclasses should be drawn from typing.py.
"""
from typing import Any, Callable, TypingMeta

from ...support.methods import pedanticmethod, classproperty
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

    # Predefined type-checking proxies
    def __instancecheck__(cls, instance):
        if hasattr(cls, '_instancechecker_data'):
            try:
                return isinstance(instance, cls._instancechecker_data)
            # Hack: to make this play well with typing module, Any, Union etc
            except TypeError:
                if len(cls._instancechecker_data) == 1:
                    if isinstance(cls._instancechecker_data[0], TypingMeta):
                        return issubclass(type(instance), cls._instancechecker_data)
                raise
        else:
            return TypeCheckableMeta.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if hasattr(cls, '_subclasschecker_data'):
            # _subclasschecker_data = getattr(cls, '_subclasschecker_data', (cls, ))
            # return issubclass(subclass, _subclasschecker_data)
            return issubclass(subclass, cls._subclasschecker_data)
        else:
            return TypeCheckableMeta.__subclasscheck__(cls, subclass)


class SimpleElementMixin(Element):
    @pedanticmethod
    def apply(cls, self, morphism):
        return morphism(self)


class SimpleElement(SimpleBaseMeta):
    def __new__(cls, name='Element', base=Any):
        self = super().__new__(cls, name, tuple([SimpleElementMixin]), {})
        self._instancechecker_data = (base, )
        self._subclasschecker_data = (base, )
        return self


def _identity(value):
    return value

class SimpleMorphismMixin(Morphism):
    @pedanticmethod
    def compose(cls, self, other):
        def composed(value):
            return other(self(value))
        return composed

    @pedanticmethod
    def call(cls, self, element):
        return self(element)

    @classproperty
    def identity(cls):
        return _identity


class SimpleMorphism(SimpleBaseMeta):
    def __new__(cls, name='Morphism', base=Callable[[Any], Any]):
        self = super().__new__(cls, name, tuple([SimpleMorphismMixin]), {})
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
