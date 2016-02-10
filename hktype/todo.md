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
