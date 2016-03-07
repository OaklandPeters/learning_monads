Running Tests
================
learning_monads/ python3 -m unittest discover v4

test_list_category.py
    Several missing tests in categoryTestCase
    abstraction of CategoryTestCase - phase out old structure


Draft Build-targets
======================
* foundations/category:
** Commit everything before major refactor
** remove foundations/category/category.py
** Example categories: list_category
*** Unittests: test of identity and composition
*** Abstract some of the tests to work generically for a category, in terms of constructor functions for element and morphism
** Example categories: Trivial, Any, List, str, pair

* [high] Remove one of conflicting definitions: Functor.apply is defined differently in foundations/functor.Functor.apply, than it is in category/element.Element.apply. For element, I've defined it as something like the conjugate of call (apply::(Element, Morphism) -> Element), while in Functor it is used as in Haskell's Applicative typeclass (apply::(Codomain.Morphism, Codomain.Element)->Codomain.Element) 
* foundations/functor/functor.py
** example functors
** functor/__init__.py
** unittests for examples


Short-Term
===============
* [med] Decide if this is a useful distinction to make: in the context of functors, draw the following distinction - (1) morphisms in the codomain (C.a->C.b), vs (2) F(D.a->D.b) ~= (C.a -> C.b) morphisms which are the result of mapping a morphism from the domain D into codomain C via morphism F. In this construction, this might be represented via a FunctorCategory, which is a subcategory ~ subclass of the codomain C.
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
