from ...support.typecheckable import TypeCheckableMeta, meets
from ...support.methods import abstractpedanticmethod


class Applicative(metaclass=TypeCheckableMeta):
    @abstractpedanticmethod
    def apply(cls, element: 'Element', morphism: 'Morphism') -> 'Element':
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Applicative:
            return meets(C, cls.__abstractmethods__)
        return NotImplemented


class Equitable(metaclass=TypeCheckableMeta):
    """
    Almost all classes will inherit __eq__ from 'object', but many should
    actually override this anyway.
    """
    @abstractpedanticmethod
    def __eq__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Equitable:
            return meets(C, cls.__abstractmethods__)
        return NotImplemented
