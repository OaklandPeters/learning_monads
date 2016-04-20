Immediate-Term
==================
I've gotten side-tracked. To refocus on productivity:

2. Return to MAybe in v5, and write an Arrow instance + Sugar, capable of expressing this:
    Maybe(f) >> g >> h << x == maybe(f, maybe(g, h))(x)

3. Use (2) inside the image-downloader example, and confirm it works.

4. Combine the new material from v5 into v4:
4.1. [IMPORTANT] The Chain/Pipe category - especially from metafuncs.py
4.1. metafunctions: generic_functions, wrapper_functions.py
4.2. The clean distinctions in heirarchy.py (functor/cofunctor/monad/comonad)
4.3. Pysk - the category
4.4. Maybe + unittests
4.5. The new version of functor is better than the old version (the old version uses apply differently than I would want). Old uses it like 'Applicative', and new uses it like, 'call within the category of the element on the left'

5. Unit-tests for rax: test/ _test_maybe.py _test_underscore.py, _test_aggregate.py

5. Concrete implemntations to make the unittests run: MonoPysk, Pysk, Pipe, Maybe, Underscore, Aggregate


Structural Questions
=======================
* Should space.Element and space.Morphism maintain a link to their Space class? IOW - should each Element and Morphism correspond to exactly one Space? Subtle implication - MaybeSpace/MaybeCategory/MaybeFunctorCategory/MaybeMonad/MaybeArrow would all have different Element/Morphism classes - and this need to not be true.
**		Potential solution: making MaybeElement/MaybeMorphsim not directly instantiatabe - instead used for typechecking / as an AbstractBaseClass. Thus, Maybe- -Space/-Category/-FunctorCategory/-Monad/-Arrow would essentialy have their own versions of Element/Morphism class, but they are not written out in the module file, nor are they used as the explicit class/constructor (in Python style). For example, MaybeCategory(), MaybeArrow(), could both be used as constructors, and would return things which are recognizable as MaybeElement or MaybeMorphism, but you can't use MaybeElement() or MaybeMorphism() as a constructor directly.


Short-Term
===============
* [high] Simplify /foundations/ structure, but removing nested folders. /space/space.py --> space.py etc
* [high] Rewrite functor.py in light of the addition of space.py. Namely, Applicative is already implied now.
* [high] Sugar. CategorySugar: MorphismSugar, ElementSugar. FunctorCategorySugar/MonadSugar
* [high] Should SimpleMorphism/SimpleElement inherit from the base they are given?
* [high] Hard question: should list be considered a virtual subclass of ListElement?
* [med] Maybe - have constructor for StandardCategory establish links upward for Element.Category = NewCategory, Morphism.Category=NewCategory
* [high] Test new form of: StandardMeta.__instancecheck__, which uses ._instancecheck_data
* [high] Thin down the comments in the header comment of morphism.py


Medium-Term
================
* [med] typecheckable.py: ABC class TypeCheckable(metaclass=TypeCheckableMeta), used to confirm that objects are intended to be typecheckable (or are types)
* [low] standard.py: validate element/morphism inputs as TypeCheckable
* [low] monoid unit-tests can be easily adapted from these written for C#: https://weblogs.asp.net/dixin/category-theory-via-c-sharp-2-monoid
* [low] Write a type-checkable version of typing.Callable, but limit to the simple-to-handle case of only positional arguments. Intended to be used mostly for Morphisms. will be greatly simplified by creating an ArgumentsDict object, and a constructor for it that takes a Callable (use inspect.getargspec) 
