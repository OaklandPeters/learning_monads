# from typing import TypeVar, Generic, Iterable, get_type_hints
import typing
from logging import Logger


def annotations_corrector(cls, method_name):
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

def correct_method_annotations(cls, method_name):
    method = getattr(cls, method_name)
    bases = cls.__mro__
    parameters = cls.__parameters__
    return _annotations_corrector(method, bases, parameters)

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
            # for parent in cls.__mro__:
            for parent in bases:
                if value in getattr(parent, '__parameters__', []):
                    position = parent.__parameters__.index(value)
            if position is None:
                raise ValueError("Could not find position in __parameters__ of parent classes")
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
        if hasattr(value, '__annotations__'):
            annotations = typing.get_type_hints(value)
            corrected = _annotations_corrector(value, bases, parameters)            
            value.__annotations__ = corrected
    return namespace



T = typing.TypeVar('T')

class LoggedVar(typing.Generic[T]):
    def __init__(self, value: T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log('Set ' + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log('Get ' + repr(self.value))
        return self.value

    def log(self, message: str) -> None:
        self.logger.info('{}: {}'.format(self.name, message))

class MyClass(LoggedVar[int]):
    pass


class WorkingGenericMeta(typing.GenericMeta):
    def __new__(mcls, name, bases, namespace, *args, **kwargs):
        parameters = kwargs.get('parameters', tuple())        
        if parameters and all(not isinstance(value, typing.TypeVar) for value in parameters):
            namespace = namespace_annotations_corrector(bases, namespace, parameters)
        cls = typing.GenericMeta.__new__(mcls, name, bases, namespace, *args, **kwargs)
        return cls

class WorkingGeneric(typing.Generic, metaclass=WorkingGenericMeta):
    pass

class WorkingLoggedVar(WorkingGeneric[T]):
    def __init__(self, value: T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log('Set ' + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log('Get ' + repr(self.value))
        return self.value

    def log(self, message: str) -> None:
        self.logger.info('{}: {}'.format(self.name, message))


class MyWorkingClass(WorkingLoggedVar[int]):
    pass


#
#
#   THIS FIXES IT!!
#
notworking = typing.get_type_hints(MyClass.get)
working = typing.get_type_hints(MyWorkingClass.get)

print()
print("notworking:", type(notworking), notworking)
print("working:", type(working), working)
print()
import ipdb
ipdb.set_trace()
print()
