"""
Sugar for groups.
Presently, this is going to clash with the way that I constructed the sugar
on categories.
"""
from ..support.methods import abstractpedanticmethod, pedanticmethod

from .semigroup import SemiGroup


class SemiGroupSugar(SemiGroup):
    @pedanticmethod
    def __add__(cls, self, right):
        return cls.append(self, right)
