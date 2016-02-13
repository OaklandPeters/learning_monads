Incremental version strategy
================================
v1
------
New function: get_attribute_type_hints(cls, method) - to make this work, need at least two new objects: HKTypeVar and HKForwardRef. HKTypeVar is responsible for (1) being replaced on methods of subclasses (2) structured access and (3) maybe, checking validity of access for F-Bounded Polymorphism. HKForwardRef is necessary for allowing cls/self reference.

v2:
---------
Replicate the functionality from get_attribute_type_hints(cls, method) inside typing.get_type_hints, which 



Trying to Solve
===================
(1) Structured references on TypeVar. Domain.Element
(1.1) Refinement: F-Bounded Polymorphism: This can be checked relative to the boundary class, allowing Exceptions to be thrown. Or maybe, to provide type-hints.
(2) Class and/or Self reference in TypeVar.
(3) Integrating or merging ForwardRef with TypeVar



# NEW STRATEGY:
# Dynamic point is inside get_type_hints, and it's interaction with _ForwardRef

* Several version of higher kinded TypeVar
* One corresponding to the behavior of HKGeneric



* Draft _HKForwardRef, which uses a lambdas
* Requires putting the class/instance information into _HKForwardRef's purview somehow. Uses HKGeneric


Relevant part of typign.get_type_hints:
        if isinstance(value, str):
            value = _ForwardRef(value)
        value = _eval_type(value, globalns, localns)


* HKTypeVar treatment will have to occur to attributes on the class, as well as values in the __annotations__ of methods
