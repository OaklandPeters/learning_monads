"""
Next-steps:
* Rework so that functions that can be defined in terms of one another ARE -- inside category.Element, and category.Morphism (such as bind in terms of fmap and join)
* new class: 'WellBehavedMonad', which provides implementation of a number of conveniences, including the dispatching __new__, __repr__ based on .data, .iter, 
* IMPORTANT: decide what/how to do with 'compose' for morphisms. Possible: zero==identity, append==compose, join==collapse

Later steps:
* Refactor methods on Element/Morphism to refer to Functor/Applicative/Monad. Do this by placing references in the category: List.functor = ListFunctor. Requires some notion of how I want functor/applicative to be used.
* Make category.Category abstract, and define what functions it can, in terms of one another.
* Rework category.py to be abstract classes (Monad, etc).


Much-later steps:
* Add sugar-classes to category.py, for '>>' at least.
* Try to Rework to try to simplify the hierarchy, to merge ListCategory and List
* Try to work in material to translate Transverable to Python (this might be fairly complicated)
** Possible fix: give CategoryBase a 'Domain' or some other checker function that can be used.
** Alternately... just accept that it's not true in general, although it's useful.

"""