"""
Misc notes:

* Rename Functor/Applicative --> Constructor, Decorator, Functor
* Define each abstract hierarchy one level higher than I need: Groupoid, Group, Arrow
* Collapsible - Monoid + Traversable, whereas Joinable - Monoid + Foldable
* Lookup original paper for methods on Arrow - mentioned in the wiki article.
    Because I don't like Haskell's version
* After these are drafted, generate a dependency tree image for them
"""


__all__ = (
    # Category-theoretic
    'Element',
    'Morphism',
    'Identifiable',
    'Semicategory',
    'Category',
    'Groupoid',
    # Walking
    'Foldable',
    'Traversable',
    # Group-Theory
    'Zeroable',
    'Semigroup',
    'Monoid',
    'Group',
    # Transformable-groups
    'Reducable',
    'Joinable',
    'Collapsible',
    # Functorial
    'Functor',
    'Applicative',
    'Monad',
    'Arrow',
)
