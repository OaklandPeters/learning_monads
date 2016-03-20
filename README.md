Running Tests
================
learning_monads/ python3 -m unittest discover v4



Hierarchial Structure
========================
Currently located in v4/.

Basis
---------
* v4/basis/ : single-method abstract base classes
* Usually - this consists of a standard method name (`call`), with magic-methods being added later by sugar-classes (`__call__`).
* Important ABCs: Identifiable, Zeroable, Composable, Appendable

Space
---------
* v4/foundations/space/: Pedantic ABCs for talking about classifications of objects (elements) and functions on them (morphisms).
* This is needed for groups to be sensible.

Groups
----------
* v4/groups/: composite ABCs from group-theory, in two 'families' - total (monoids) and non-total (categories). In most cases, I use the total-family for classifying the elements of a space
* Category is the most important one (by far).

Category
-------------
* v4/foundations/category/: The group structure we will be working in most often.

Folds and Unfolds
-------------------
* v4/folds/: Methods of transforming or collapsing group-structures.
* The opposite of a fold is an unfold. Using monads involves both extensively, but unfolds are generally handled implicitly, by building up and a Syntax-Tree like object incrementally in our code.

Functor
-----------
* v4/foundations/functor/:
* Includes Functor, FunctorCategory, Monad
* Monad ~ FunctorCategory + additional rules

Arrow
------------
* v4/foundations/arrow/: Allow use to change the rules of functions in a category (morphsims).
* If a Monad is an advanced form of Category, then an Arrow is an Advanced form of Monad.
* Primarily used for control-flow, and branching/merging of data-flow.
* Can also be used to change the rules of morphisms (one input, one output) into that of Python-like functions (variable number of arguments; keyword arguments; optional arguments and default arguments).
* Arrow violates the strict {Element, Morphism} classification defined for Spaces - because some instances of an Arrow class can correspond to both and/or neither of Element/Morphism.

