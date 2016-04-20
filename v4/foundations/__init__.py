"""
Misc notes:

* Define each abstract hierarchy one level higher than I need: Groupoid, Group, Arrow
* Collapsible - Monoid + Traversable, whereas Joinable - Monoid + Foldable
* After these are drafted, generate a dependency tree image for them
"""


# __all__ = (
#     # Category-theoretic
#     'Element',
#     'Morphism',
#     'Identifiable',
#     'Semicategory',
#     'Category',
#     'Groupoid',
#     # Walking
#     'Foldable',
#     'Traversable',
#     # Group-Theory
#     'Zeroable',
#     'Semigroup',
#     'Monoid',
#     'Group',
#     # Transformable-groups
#     'Reducable',
#     'Joinable',
#     'Collapsible',
#     # Functorial
#     'Functor',
#     'Applicative',
#     'Monad',
#     'Arrow',
# )

from .space import Space, Morphism, MorphismSugar, Element

__all__ = (
    Space, Morphism, MorphismSugar, Element
)
