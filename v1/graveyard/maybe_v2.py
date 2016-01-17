#!/usr/bin/env python3
"""
Testing ground, for how I'd like this syntax to work:
name = Maybe(user).bind(
    Maybe(get('first'))
    >> get('middle')
    >> get('last')
)
MaybeX >> value = MaybeX.append()

Conclusions:
(1) Maybe(get('first')) --> Maybe would have to act as a decorator (~lazy fmap)
(2) I'd like: >> = lambda self, func: self.append(self.fmap(func))
(3) '>>' would *not* be just sugar for bind.
(4) It's not clear that: Maybe(user) >> get('first'), would be sensible, because
'>>' expects the LHS to be a function

==> I keep meeting up with the difficulties of keeping objects VS functions
distinct (A problem which Haskell side-steps)


Maybe(user).bind(get('middle')).bind(get('first')) == 'David'
Maybe(user).bind('get('last')).bind(get('first')) == 'Bowie'

"""

from typing import Callable, TypeVar, Iterator, Any

from monad import Monad, classproperty


class Maybe(Monad):
    def bind(self, maybe_function):
        result = maybe_function(self.data)
        
