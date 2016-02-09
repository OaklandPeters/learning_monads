"""
Defines higher-kinded versions of some of the classes from typing.py.


        # NEW STRATEGY:
        # Dynamic point is inside get_type_hints, and it's interaction with _ForwardRef



Next steps:
* HKTypeVar: subclass TypeVar. Subsumes functionality of structured_forward_ref

* Annotations descriptor: To make annotations into a getter, that executes the higher-kinded type behavior. Requires moving the actual resolving/correcting step OUT of the Generic step, and into the descriptor. (GenericMeta.__new__ should instead replace the __annotations__)
* Makes notes for SEPERATE CONCERNS: 'ThisType' behavior, and structured TypeVars




Later steps:
* F-Bounded Polymorphisms for HKTypeVar(, bound=): either exposes the same structure as the bound type, or raises complaints when replaced



MOST AUTHORITATIVE REFERENCE ATM:
scratch_higher_kinded.py

"""
import typing

import corrector  # REMOVE LATER
import annotations

__all__ = (
    'HKGenericMeta',
    'HKGeneric',
    '_HKForwardRef',
    'HKTypeVar',
    'AnnotationsDescriptor',
    'Annotations',
)




class HKGenericMeta(typing.GenericMeta):
    def __new__(mcls, name, bases, namespace, *args, **kwargs):
        parameters = kwargs.get('parameters', tuple())        
        if parameters and all(not isinstance(value, typing.TypeVar) for value in parameters):
            namespace = corrector.namespace_annotations_corrector(bases, namespace, parameters)

            # Tenative
            # namespace = annotations.replace_annotations_in_namespace(namespace)

        cls = typing.GenericMeta.__new__(mcls, name, bases, namespace, *args, **kwargs)
        # cls = super().__new__(mcls, name, bases, namespace, *args, **kwargs)
        # cls = update_higher_kinded(cls)
        return cls


class HKGeneric(typing.Generic, metaclass=HKGenericMeta):
    pass


class _HKForwardRef(typing._ForwardRef):
    pass


class HKTypeVar(typing.TypeVar, _root=True):
    pass


class AnnotationsDescriptor:
    pass


class Annotations:
    pass

