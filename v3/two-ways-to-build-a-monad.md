Background
-------------
See the 'big-problem.md' 

There are two ways to construct monad from functor > applicative > monad, the three domain method (closer to the mathematical construction of Category theory), and the two-domain method (closer to Haskell's construction). The three domain method is logically clearer when learning, but requires more work to write, and involves more terms.

Three Domain Method
---------------------
(1) Start with two categories: Domain and Codomain.
(2) Define a Functor F_f which translates functions in D into functions in C. 
(3) Define an Applicative F_a from Functor F_f, which 
