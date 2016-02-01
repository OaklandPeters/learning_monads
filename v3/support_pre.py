"""
Support functions which are used by category.py, so should
be defined before class defined there, and not have references to them.
"""

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


class pedanticmethod:
    """
    Allows a method to be used as both a classmethod and an instancmethod, but in the specific (and pedantic) way so that:
        instance.method(*args, **kwargs) == klass.method(instance, *args, **kwargs)
    """
    def __init__(self, method):
        self.method = method

    def __get__(self, obj=None, objtype=None):
        @functools.wraps(self.method)
        def _wrapper(*positional, **keywords):
            if obj is not None:  # instancemethod
                return self.method(type(obj), obj, *positional, **keywords)
            else:  # classmethod
                return self.method(objtype, *positional, **keywords)
        return _wrapper


def check_validation(cls, *args, **kwargs) -> None:
    """Checks all validation functions defined on
    classes in MRO of 'cls'.
    These functions should be classmethods which raise TypeError or return None.
    """
    for klass in cls.__mro__:
        # does 'klass' define it's own '_validation' method
        if '_validation' in klass.__dict__:
            klass._validation(*args, **kwargs)


class NotPassed:
    pass


class TypeCheckableMeta(type):
    """Makes isinstance and issubclass overrideable."""

    def __instancecheck__(cls, instance):
        if any('__instancecheck__' in klass.__dict__ for klass in cls.__mro__):
            return cls.__instancecheck__(instance)
        else:
            return type.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if any('__subclasscheck__' in klass.__dict__ for klass in cls.__mro__):
            return cls.__subclasscheck__(subclass)
        else:
            return type.__subclasscheck__(cls, subclass)
