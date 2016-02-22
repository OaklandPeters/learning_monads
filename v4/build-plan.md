Build Plan
=================

1. Copy over stubs from category-theory/ to match (3)
2. Copy over stubs from til/
3. Stub support/: typecheckable.py, methods.py, represent.py
4. Stub foundations/: category.py, groups.py, foldable.py, monad.py, transform.py, using Pythonic naming
5. Consider whether to split this up into one class per file
6. Filli n foundations/ but NOT utility methods or mixin methods. Fill in utility methods/mixin-mehtods only when they are first used inside step (7 - implementing concrete monads). Be pedantic and not practical - specify every piece of info explicitly.
7. Implement concrete monads, using 3-category method: List, Maybe, State + tests. Element, Morphism, Category, Functor, Applicative, Monad. Ignore sugar operators. Revise ABCs from (6) as necessary.
8. Implement monads: Function, Arguments, Underscore + tests.
9. Write down the construction algorithm for 3-category (Bisection rule?)
10. sugar classes for operators: >>, <<, **, ^. ~composition + lift, traverse, call/apply
11. StandardCategory, StandardMorphism, StandardElement 


Consider merging: functor + applicative --> functor
    constructor + decorator --> functor
