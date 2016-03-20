"""
When using Categories in relation to OOP, we will usually be using a FunctorCategory.
This Functor will map from the base 

For the OOP approach, the Functor almost always maps: Any --> class we are building
Where the FunctorCategory itself will be the class we are building

MONADS
----------
Monads will generally be written as FunctorCategory + extra structure.
"""
from .functor import Functor
from ..category.category import Category


class FunctorCategory(Functor, Category):
    """
    A category, equipped with a canonical set of constructors/decorators.
    Classes in OOP langauges are often written this way.

    In practical terms, this allows the Category define __init__/__new__ behavior for the
    category as reasonable defaults, while still allowing alternate constructors to exist
    (such as when mapping from a different Category).


    """


def promote(codomain: 'FunctorCategory', obj: 'Any') -> 'codomain.Element|codomain.Morphism':
    """
    An equivalent way to write this:
        if Domain.is_morphism(obj):
            return Codomain.decorate(obj)
        elif Domain.is_element(obj):
            return Codomain.construct(obj)
        ... assuming that Pysk can type-check on Element/Morphism even when obj is not actually wrapped by Pysk
    """
    domain = getattr(obj, 'Category', Pysk)
    assert issubclass(domain, Category)

    if isinstance(obj, domain.Morphism):
        return codomain.Morphism(obj)
    elif isinstance(obj, domain.Element):
        return codomain.Element(obj)
    else:
        raise TypeError(str.format(
            "Object of type '{0}' is not Element or Morphism of Domain Category '{1}'",
            obj.__class__.__name__, domain.__name__
        ))
