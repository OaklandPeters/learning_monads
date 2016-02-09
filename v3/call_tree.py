"""
Generalization of function-tree used in type_logic.py

One insight is: the monad's fmap and lift can map Morphisms/Elements into the same data-structure 'type' inside the monad. As long as they map 'out' in a way that maintains the  morphism/element distinction.
"""


class CallTreeDomain(category.Category):
    pass

class CallTreeCodomain(category.Category):
    pass

