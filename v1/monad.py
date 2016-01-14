#!/usr/bin/env python3

import abc
from typing import TypeVar, Generic, Callable


class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


Element = TypeVar('Element')

class Monad(Generic[Element], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def bind(self, morphism: 'Monad[Callable]'):
        """
        (m a , (a -> m b)) -> m b
        Applies a function return monadic value, to a monadic value.
        Sequences calculations

        ... we really want a convenience function which does
        List(x_value).bind(List.lift(x_function))
        """
        pass

    @classmethod
    @abc.abstractmethod
    def lift(cls, element: Element) -> 'Monad[Element]':
        """Haskell calls this 'return'. Basically the constructor."""
        pass


    @classmethod
    @abc.abstractproperty
    def zero(cls) -> 'Monad':
        return NotImplemented

    @abc.abstractmethod
    def append(self, element: Element) -> 'Monad[Element]':
        """Add some element of the domain into this monadic structure"""
        return NotImplemented


    @abc.abstractmethod
    def join(self) -> 'Monad[Element]':
        """
        Usually, very similar to flatten
        """
        return NotImplemented



