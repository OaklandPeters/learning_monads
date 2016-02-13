Terminology
=====================
Terms I use here, defined linguistically (not mathematically or programmatically).


Higher Kinded Type
--------------------
* Higher kinded types are types which take other types and construct a new type
* A higher kinded type is a concept that reifies a type constructor as an actual type
* Higher kinded type == type constructor which takes type constructor as a type parameter?

[https://gist.github.com/CMCDragonkai/a5638f50c87d49f815b8]
A type constructor can be thought of in these analogies:
* like a function in the type universe
* as a type with a "hole" in it
* as a container containing type(s)
* as a generic type, parameterised over other types
* as an endofunctor in the category of types

[From Wikipedia:]
In the area of mathematical logic and computer science known as type theory, a kind is the type of a type constructor or, less commonly, the type of a higher-order type operator. A kind system is essentially a simply typed lambda calculus "one level up", endowed with a primitive type, denoted * and called "type", which is the kind of any data type which does not need any type parameters.

A kind is sometimes confusingly described as the "type of a (data) type", but it is actually more of an arity specifier. Syntactically, it is natural to consider polymorphic types to be type constructors, thus non-polymorphic types to be nullary type constructors. But all nullary constructors, thus all monomorphic types, have the same, simplest kind; namely *.
