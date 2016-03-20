from collections import Callable


from ...support.typecheckable import Interface
from ...support.methods import pedanticmethod, abstractpedanticmethod, abstractclassproperty


class Morphism(Callable, Interface):
    @abstractpedanticmethod
    def call(cls, self: 'Morphism', element: 'Element') -> 'Element':
        return NotImplemented


