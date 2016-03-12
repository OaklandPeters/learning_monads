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
