"""
Next-steps:
* IMPORTANT REWORK: Morphism IS a Monoid, but defined in terms of different functions on the category: zero --> identity, append --> compose, join --> collapse
** Apply to list.py
* Add __instancecheck__ and __subclasscheck__ to category.Category, and make ListCategory used as a metaclass. (lookup how to do this from mfpy). Hard part - do it while allowing normal 'isinstance' to work when not overridden. 
* Just/Nothing should override __instancecheck__ and __subclasscheck__
* Rework so that functions that can be defined in terms of one another ARE
** category.Category.f_map <-- f_apply
** category.Category.a_map <-- a_apply
** category.Category.m_map <-- m_apply
** m_apply in terms of f_apply and join
* Simplify List.compose/Maybe.compose - to account for removing the identity function when appending ot it


Later steps:
* Add Category method: identity, and have Morphism.zero return it
* Add in list functions to List() monad (maybe even inherit from standard Python list)
* Refactor methods on Element/Morphism to refer to Functor/Applicative/Monad. Do this by placing references in the category: List.functor = ListFunctor. Requires some notion of how I want functor/applicative to be used.
* Make category.Category abstract, and define what functions it can, in terms of one another.
* Rework category.py to be abstract classes (Monad, etc).
* new class: 'WellBehavedMonad', which provides implementation of a number of conveniences, including the dispatching __new__, __repr__ based on .data, .iter, 
* Add '@functools.wraps()' statements to 'map' functions in list.py and maybe.py. Consider changing the naming process.


Much-later steps:
* Add sugar-classes to category.py, for '>>' at least.
* Unit-test mixin for monoid, based on the laws here: https://hackage.haskell.org/package/base-4.8.2.0/docs/Data-Monoid.html
* Incorporate Foldable and Traversable into the Pythonic hierarchy
* Try to Rework to try to simplify the hierarchy, to merge ListCategory and List
* Try to work in material to translate Transverable to Python (this might be fairly complicated)
** Possible fix: give CategoryBase a 'Domain' or some other checker function that can be used.
** Alternately... just accept that it's not true in general, although it's useful.
* Find monadic laws, and write MixinTests for them. Documentation for each test should include statement of the law. These should be used by mixing them onto the TestCase for speicifc monads. Test on ListMonadTests



Interestingly, List.join and Maybe.join have the same join function.
... Perhaps this points to a shared structure of any monoid, who
has the property that *all* of their internal structure/data can
be captured by a single internal tuple ('.data')?
    I suspect that monads with 'context' (Tryit) will fail this.

"""
