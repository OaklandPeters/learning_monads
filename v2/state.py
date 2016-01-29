"""
Defines a context which feeds to functions a first argument
which is read-only state, such as an environment or configuration.

This will also be the basis of a later TryIt monad.

State differs from List and Maybe in that:
* It's .lift (sometimes .unit) is distinct. For List/Maybe
    lift(value) == zero().append(value)
But this is not true for State.lift(initial), whose initial defines the state applied to all later morphisms.

Resolution: I'm remaking State's Element to be objects, rather than functions (unlike pymonad's State). I suspect I can do this more easily, since I've made Element/Morphism distinct objects in this hierarchy.


> Unlike most of the other monad types, the state monad doesn’t wrap values it wraps functions. Specifically, it wraps functions which accept a single ‘state’ argument and produce a result and a new ‘state’ as a 2-tuple. The ‘state’ can be anything: simple types like integers, lists, dictionaries, custom objects/data types, whatever. The important thing is that any given chain of stateful computations all use the same type of state.

Resolution:


Next-steps:
* Better way to construct the initial element. Not sure what the data element should be set to... 
* Move typedefs to top
* Make _injector an assigned property, not 

Later-steps:
* Arguments Category/Monad - a generalization of this, which will be used as a parent class once written. The two differences are (1) an explicit injector function (these are morphisms in the Arguments monad) so new values do not have to be prepended as the first positional argument, and Arguments has (Any) as values and (Arguments->Arguments) as morphisms
* CONSIDER: would this be more easily written as the category of Arguments? And the morphisms would be arguments-transforming functions, and this state injector would simply be one Functor/Monad in that? NOTE: this would be a validation of the fact that the Category would be different than the monad.

Much-Later-steps:
* This can be reworked to be a sub-category in the category of Arguments - which will make it much more potent (since it can )

"""
import typing
from typing import Callable, Tuple, TypeVar


import category
from support_pre import NotPassed, classproperty



#
#   Typedefs
#
StateType = typing.TypeVar('StateType', category.Monad)
Value = typing.TypeVar('Value', typing.Any)
Injector = typing.Callable[Value, Tuple]
InjectorBinder = Callable[State, Injector]


class NotSpecifiedType:
    """If 'None' were subclassable, this would be a subclass of NoneType.
    This is used as initial value for StateElement.lift's 'value' - because
    we want to be able to distinguish that initial value from the possibility
    of the user explicitly passing in 'None'
    """
NotSpecified = NotSpecifiedType()



class StateCategory(category.Category):
    """
    An arbitary decision is needed:
        This is Sequence state --> state is stored in a tuple

    BUT - this is complicated by the fact that we use an injector function
    to combine the state and some value, usually
        def _injector(value):
            return (self.state, value)

    Converting this from existing examples (pymonad):
        They have it wrap functions, and have no concept of morphisms
        I'm having it wrap data, and have a concept of morphisms
    """

    @classmethod
    def zero(cls, value, binder=bind_state_to_prepend: InjectorBinder):
        injector = binder(value)
        return State

    @classmethod
    def append(cls, element, element):
        """This is going to be really hard to handle,
        since it depends entirely on the type of data structure
        the state is, whether a dict, sequence, or something atomic.
        
        """





class State(category.Monad, metaclass=StateCategory):
    """
    img_tag1 = {'src': 'path: src', 'data-src': 'path: data-src'}
    State(state=img_tag1)
    """
    def __init__(self, ...):
        pass

    @property
    def injector(self):
        return self._injector

    def _injector(self, value):
        return (self.state, value)


    
    def _injector(self, value: Value) -> Tuple[StateType, Value]:




class StateElement(category.Element, State):
    """
    Element should carry the result of the calculation (potentially something representing 'nothing'),
    and the state.

    Complication: this should support the ability to 'lift' and only provide state.
    """
    def __init__(self, state, value=NotSpecified):
        self.state = state
        self.value = value


class StateMorphism(category.Morphism, State):
    """
    Computation, acting on state and some value.
    """
    pass






def bind_state_to_prepend(state: State) -> Callable[Value, [Tuple[State, Value]]]:
    """This is the default function, used for InjectorBinder.
    ... naming is hard."""
    def prepend_state(value: Value) -> Tuple[State, Value]:
        return (state, value)
    return prepend_state



#
#   Version of state from online example
#       bears some resemblance to the TryGet behavior
#
#
def bind(mv, mf):
    def _(env):                      # return a function of environment
        val = mv(env)                # which, when invoked with an environment, returns a value
        return mf(val)(env)          # apply the next function with the new value, and the same environment
    return _

def read(key):                       # a computation in an environment, that reads a value from the environment
    def _(env):                      # return a function of environment
        return env[key]              # which, when invoked with an environment, will look up the key in the env
    return _



#===================
# Unit-Tests
#===================
import unittest

class StateTests(unittest.TestCase):
    def test_basic(self):
        
