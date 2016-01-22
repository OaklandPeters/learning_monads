"""
Rules and goals that should be true, no matter the form/implementation
I end up using.

Intending 'design'-goals here, rather than algebraic rules (as in Haskell).
"""


def functors_wrap(functor, function, arguments):

    wrapped = functor(function)
    result = wrapped(arguments)
    # results is the reasonable results from doing this


def chaining_functions(f: Callabe, g: Callable, x: Element, M: Monad):
    composed = M(f) >> g
    result = composed(x)
    composed(x) == M(f)

    step1 = M(f)(x)
    step2 = M(g)(step1)

    (M(f) >> g)(x) == M(g)(M(f)(x))

def chaining_value():
    """
    """
