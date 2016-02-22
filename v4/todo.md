

Short-Term
===============
* [med] Maybe - have constructor for StandardCategory establish links upward for Element.Category = NewCategory, Morphism.Category=NewCategory
* [high] Test new form of: StandardMeta.__instancecheck__, which uses ._instancecheck_data


Medium-Term
================
* [med] typecheckable.py: ABC class TypeCheckable(metaclass=TypeCheckableMeta), used to confirm that objects are intended to be typecheckable (or are types)
* [low] standard.py: validate element/morphism inputs as TypeCheckable
