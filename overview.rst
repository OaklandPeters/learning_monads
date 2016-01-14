Learning Monads
=================
In incremental steps, from the ground-up. The goal is to develop them by hand, without extensive reference to Haskell. This is because many features of Haskell's monads do not transfer well outside of that language.

Such as (1) functions can be treated as indistinguishable from the data type they return (so functors can map over data as well as functions); (2) all monads map from the universal-category (Hask).

Because Haskell is built on lazy evaluation of functions, you can do one-line function defintion through composition without monads: h = fmap g f.  Monads need this property (so you can compose functions without providing their inputs).
    But Python does not have lazy evaluation. Hence, to make monads coherent, in Python, they need to be rooted on a class like Composable. This makes their fmap functions return other functions.

v1
------
Simple learning by doing. Making several common monads, without creating them in the Functor/Applicative/Monad hierarchy, and without considering them inside a category structure.

Monads to write: List, Maybe, State, Reader, Writer, IO (limit version - print output, input, etc)

Advanced monads (possibly) to make: Deferred, Continuation, Error


v2
-----
Implement the previous monads as part of the Functor/Applicative/Monad hierarchy. This may require some trasnlation, and I should see my prior work in mfpy for reference. Note - I am restricting this step of the project to monads which map from the language-universal category (Pyth, similar to Hask) ~ IE functors which map from any object in the language.

A may also want to restrict this attempt to monads which are also comonads (IE data can come out as well as be put in)... so it could rest on a monad class called 'Boxed' (similar to 'Container') which has methods 'box', 'unbox'.


v3
------
Implement Ontology rigorously.
Category, Monoid, Monad, Comonad, 
