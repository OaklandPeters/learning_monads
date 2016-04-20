#!/usr/bin/env python3
"""
This bastard needs PyskSpace.
Or better yet, ArgumentsSpace


Todo:
* Put a version of psyk into concrete/pysk/
* Add cofunctor to functor.py
* Draft category.CategorySugar, to resemble my work for Pipe
* Draft ABC version of Arrow
"""
from ...foundations import space, functor, monad, arrow
from ...groups import category
from .. import pysk


class UMorphism(space.Morphism, space.MorphismSugar):
    pass


class UElement(space.Element):
    pass


class USpace(space.Space):
    Element = UElement
    Morphism = UMorphism


class UCategory(USpace, category.Category, category.CategorySugar):
    pass


class UArrow(UCategory, arrow.Arrow):
    pass


class UFunctor(functor.Functor):
    Domain = UCategory
    Codomain = pysk.PyskCategory


class UCofunctor(functor.Cofunctor):
    Domain = pysk.PyskCategory
    Codomain = UCategory


class UFunctorCategory(UFunctor, UCategory):
    pass


class UCofunctorCategory(UCofunctor, UCategory):
    pass


class UMonad(UFunctorCategory, monad.Monad):
    pass


class UComonad(UCofunctorCategory, monad.Monad):
    pass


class UContext(UMonad, UComonad, UArrow):
    pass
