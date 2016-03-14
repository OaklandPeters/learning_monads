Running Tests
================
learning_monads/ python3 -m unittest discover v4

test_list_category.py
    Several missing tests in categoryTestCase
    abstraction of CategoryTestCase - phase out old structure


Immediate-Term
==================
I've gotten side-tracked. To refocus on productivity:

1. [high] Abstract parts of foundations/category/ into space.py: Element, Morphism, Space.Element, Space.Morphism, .call, .apply

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


Short-Term
===============
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
