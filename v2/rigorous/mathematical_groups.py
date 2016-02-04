"""
Summary of group-like structures in mathematics (not Haskell), written as if they were Python style ABCs

    Drawn partly from: https://en.wikipedia.org/wiki/Group_(mathematics)

@todo: Could also write the laws that must be obeyed on each one.
"""

_abstract = lambda func: classmethod(abstractmethod(func))

#
# One-trick ponies
#   These are all defined as laws/additional objects obeyed in respect to the core binary method
#
#
class Operation:
    """Binary operation on elements in the structure.
    I'm calling it Compose, because that is most commonly used in monadic
    data structures, but it can anything binary (multiplication, addition, etc)
        Append makes sense on classical data strctures.
    """
    Compose = _abstract(lambda cls, left, right: NotImplemented)
    Domain = abstractclassproperty()

class Totality(Operation):
    """A function which is defined for all inputs of the right type, that is, for all of a domain.

    This is an equivalent axiom to Closure, so you only need one.
    """

class Closure(Operation):
    """Does the application of Associativity on the Elements always lead to another object in the set of Elements?
    This is an equivalent axiom to Totality, so you only need one.

    This is unrelated to the computer science concept of a 'closure'
    """

class Invertibility(Operation):
    """AKA called 'Divisibility'Can you reverse the composition operation?"""

class Associativity(Operation):
    """Binary associative operation.
    In monadic contexts, I generally call this Append.
    """

class Identity(Operation):
    Identity = _abstract(lambda cls: NotImplemented)

class Commutativity(Operation):
    """Changing the order of the oprations does not change the meaning."""



#
# Group-like structures
#
class Semicategory(Associativity):
    """
    Also called a 'semigroupoid'. Basically a Category with no Identity

    Semigroupoids generalise semigroups in the same way that small categories generalise monoids and groupoids generalise groups. Semigroupoids have applications in the structural theory of semigroups.

    Formally, a semigroupoid consists of:

        Objects: a set of things called objects.

        Morphisms: for every two objects A and B a set Mor(A,B) of things called morphisms from A to B. If f is in Mor(A,B), we write f : A → B.

        Composition: for every three objects A, B and C a binary operation Mor(A,B) × Mor(B,C) → Mor(A,C) called composition of morphisms. The composition of f : A → B and g : B → C is written as g ∘ f or gf. (Some authors write it as fg.)

        such that the following axiom holds:

        (associativity) if f : A → B, g : B → C and h : C → D then
            h ∘ (g ∘ f) = (h ∘ g) ∘ f.

    """
    pass

class Category(Associativity, Identity):
    pass

class Groupoid(Associativity, Identity, Invertibility):
    """
    A groupoid can be seen as either of:

    (1) Group with a partial function replacing the binary operation;

    (2) Category in which every morphism is invertible. A category of this sort can be viewed as augmented with a unary operation, called inverse by analogy with group theory.[1] Notice that a groupoid where there is only one object is a usual group.
    """

class Semigroup(Closure, Associativity):
    """
    """

class Monoid(Closure, Associativity, Identity):
    pass

class Group(Closure, Associativity, Identity, Invertibility):
    pass

class AbelianGroup(Closure, Associativity, Identity, Invertibility, Communtativity):
    """This is the most important classification.
    I do not know why.

    Hypothesis: This is the condition that it takes to form an 'Algebra'.
    And algebras are where everything interesting happens. They are also undecidable.
        Also - many albelian groups posses a natural topology, and form very useful topological groups.
    """
