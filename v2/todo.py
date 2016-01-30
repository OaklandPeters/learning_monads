"""
Structure refactor:
* TRY: see if I can move monadic functions off of Category, and onto Monad
* PROBLEM: Find a way to Element/Morphism only have access to the methods appropriate for whether it's in a Functor/Applicative/Monad.

Next-steps:
* Fix: a_map, m_map should return Morphism
* Simplify List.compose/Maybe.compose - to account for removing the identity function when appending ot it
* __init__ functions for v2
* test/ test/__init__
* Move all to their own directory.
* Some mechanism to run all unit-tests. Either nose or py.test, or write something in tests/all_tests.py which imports * from test_list.py, test_maybe.py and runs unittest.main()



Later steps:
* Refactor methods on Element/Morphism to refer to Functor/Applicative/Monad. Do this by placing references in the category: List.functor = ListFunctor. Requires some notion of how I want functor/applicative to be used.
* Make category.Category abstract, and define what functions it can, in terms of one another.
* Make Functor/Applicative/Monad abstract. abstract-->X_apply function. Mixin method-->X_map. abstract-->Category
* DECISION: should Category have access to Element and Morphism properties. If so, Functor/Applicative/Monad/Element/Morphism should have access to them via cls.Category.Element, cls.Category.Morphism. Creates a PROBLEM due to cyclic reference on Category (which must be defined before it's Element/Morphism, but should have a reference to them)
* Write unit-tests generic to Category, to reflect laws. As a mixin. Write after refactoring category into Functor/Applicative/Monad.
* AS A TEST: Refactor 
* HARD BUT ELEGANT: make typecheck work for zero and identity (the identity one may be tricky). This requires creating an object for Zero, and providing special behavior for Identity.
** Make Category.Zero/Category.Identity --> classproperty returning a subclass of this object. Requires caching
** Change typechecking in list.py and maybe.py, for empty Element/Morphism to isinstance(value, cls.Category.Zero)
** Write class objects ~ generics: class Identity(Generic[Category | Morphism]), class Zero(Generic[Category | Element | Monoid])
* Add in list functions to List() monad (maybe even inherit from standard Python list)
* Rework category.py to be abstract classes (Monad, etc).
* new class: 'WellBehavedMonad', which provides implementation of a number of conveniences, including the dispatching __new__, __repr__ based on .data, .iter, 
* Add '@functools.wraps()' statements to 'map' functions in list.py and maybe.py. Consider changing the naming process.
* SERIOUS THOUGHT: on clearly specifying class/validatory for ElementType and MorphismType.


Much-later steps:
* Generalize methods in category.py to take **kwargs (maybe also *args) where possible. Why? because some specific monads will make use of extra arguments. For example, some Monads will support a .join() that takes an argument (think of Maybe-like structures which have to choose between left and right).
* SUGAR: add sugar-classes to category.py, for '>>' at least. via MonadOperatorsSugarMixin
* SUGAR: generic functions for: lift, f_map, a_map, m_map. Maybe: GenericFunctionMixin
* SUGAR: generic object + typechecker + function for: Identity, Zero. Needs to be able to ask: isinstance(element, Zero(Category)). May require writing a Zero and Identity object for each Category. Should work like: Zero(Category) or Zero(Element) or Zero(Morphism).
* ADVANCED SUGAR: |infix| methods via a InfixSugarMixin
* Unit-test mixin for monoid, based on the laws here: https://hackage.haskell.org/package/base-4.8.2.0/docs/Data-Monoid.html
* Incorporate Foldable and Traversable into the Pythonic hierarchy
* Try to Rework to try to simplify the hierarchy, to merge ListCategory and List
* Make CategoryBase abstracts, and have Monoid, Morphism, and Element inherit from it
* Try to work in material to translate Transverable to Python (this might be fairly complicated)
** Possible fix: give CategoryBase a 'Domain' or some other checker function that can be used.
** Alternately... just accept that it's not true in general, although it's useful.
* Find monadic laws, and write MixinTests for them. Documentation for each test should include statement of the law. These should be used by mixing them onto the TestCase for speicifc monads. Test on ListMonadTests

Much-much-later steps:
* Consider a better reorganization of the distinction between Category and Monad. There are a few subtle factors taht produce confusion here: (1) f_apply/a_apply are associated with the Monad, and *possibly* the category specific to the monad, (2) I can see how there can be multiple Monads inside a single category (such as the relationship between Arguments and State).
** Is subclass inheritance a SOLUTION? class StateCategory(ArgumentsCategory), class StateElement(ArgumentsMorphism), class StateMorphism()


Interestingly, List.join and Maybe.join have the same join function.
... Perhaps this points to a shared structure of any monoid, who
has the property that *all* of their internal structure/data can
be captured by a single internal tuple ('.data')?
    I suspect that monads with 'context' (Tryit) will fail this.


IDEA:
to auto-generate Morphism/Element, inside the appropraite CategoryBase.
Then, these are provided at the module level as 'list.Morphism', 'list.Element'.
PROBLEM: when I want or need to override the behavior/construction, as in maybe_v3.py.
PROBLEM: providing Element/Morphism specific utility methods
ADVANTAGES: cuts down on the cruft considerably.
STRATEGY: to override the behavior, those class constructions can be made, and CACHED, inside 'ListBase.Element', etc

"""
