"""
Pysnickety type-checking library parts:
* typing.get_type_hints --> get_annotations
* TypeVar with __getattr__ proxying to __bound__
* __annotations__ getter descriptor version (__get__)
* TypeAlgebra: |, &, -, implementing
* General type-checker: AST based  (likely hard)
* General type-checker: eval based (likely hard)

"""
