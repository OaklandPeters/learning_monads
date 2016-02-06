"""
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

def proxy_getattr(self, name):
    return getattr(self.__bound__, name)

#
#   EVIL DIRTY HACK
#       But TypeVar won't let me subclass it, so....
#
setattr(typing.TypeVar, '__getattr__', proxy_getattr)

# def BoundedTypeVar(*args, **kwargs):
#     """
#     Improvements:
#     * first argument 'klass', and make this have the same namespace as that
#     """
#     assert 'bound' in kwargs
#     tv = typing.TypeVar(*args, **kwargs)

#     # does this need to be a classmethod?
#     # def _getattr_(self, name):
#     #     return getattr(self.__bound__, name)
#     tv.__getattr__ = proxy_getattr
#     return tv


class Category:
    """Placeholder"""
    @abstractclassproperty
    def Element(cls):
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls):
        return NotImplemented

Domain = BoundedTypeVar('Domain', bound=Category)


print()
print("Domain:", type(Domain), Domain)
print()
import ipdb
ipdb.set_trace()
print()
