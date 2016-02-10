import typing

import support_pre
import hktyping
import higher_kinded as hk






# @todo: Replace typing with hktyping
Domain = hktyping.HKTypeVar('Domain')
Codomain = hktyping.HKTypeVar('Codomain')

class Category:
    """Placeholder"""
    @support_pre.abstractclassproperty
    def Element(cls):
        return NotImplemented

    @support_pre.abstractclassproperty
    def Morphism(cls):
        return Expected
        # return NotImplemented

class AnyCategory(Category):
    Element = typing.Any
    Morphism = typing.Callable

class ListCategory(Category):
    Element = list
    Morphism = typing.Callable[[list], list]



CF = hk.CleverForward

class Functor(hktyping.HKGeneric[Domain, Codomain]):
    def f_apply(cls, element: CF('Codomain.Element'), function: CF('Domain.Morphism')) -> CF('Codomain.Element'):
        pass

class ListFunctor(Functor[AnyCategory, ListCategory]):
    pass



print()
print("ListFunctor.__parameters__:", type(ListFunctor.__parameters__), ListFunctor.__parameters__)
print()
import ipdb
ipdb.set_trace()
print()

