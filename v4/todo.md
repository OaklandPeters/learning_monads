
Draft Build-targets
======================
* foundations/category:
** Commit everything before major refactor
** remove foundations/category/category.py
** Example categories: list_category
** Example categories: Any, List, str, pair
* foundations/functor/functor.py
** example functors
** functor/__init__.py
** unittests for examples


Short-Term
===============
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
