"""
The goal here:
To make annotations into a getter, that executes the higher-kinded type behavior.
? Where does the higher kinded execution step occur?

* Step 1 - use classic style descriptor
* Step 2 - fold behavior more specific
"""
import typing
import collections
import abc


class HigherKindedType(metaclass=abc.ABCMeta):
    """Placeholder and base-type"""
    @abc.abstractmethod
    def _apply(self, element):
        return NotImplemented



class AnnotationsDescriptor:
    """
    This will have the traits of *both* a dictionary and a getter. Basically,
    when you: cls.method.__annotations__ --> it executes some functions, which results
    in 

    TODO: Change this to be classproperty type descriptor.
    * Advanced: Make this like @pedanticmethod - support get for class & instance
    """
    def __init__(self, fget=None, fset=None, fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    #----- Descriptors
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        if self.fval is not None: #Validate, if possible
            value = self.fval(obj, value)
        self.fset(obj, value)
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

class Annotations(collections.UserDict):
    def __init__(self, owner, *args, **kwargs):
        # Feed mapping data into init for UserDict
        super().__init__(*args, **kwargs)
        self.owner = owner

    def __getitem__(self, key):
        value = self.data[key]
        if isinstance(value, HigherKindedType):
            return value._apply(self.owner)
        else:
            return value

class Thingy:
    @AnnotationsDescriptor
    def annotations(self):
        return self._annotations

