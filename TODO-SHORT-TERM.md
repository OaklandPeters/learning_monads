Short-Term Design Goals:
-----------------------------
I've gotten side-tracked. To refocus on productivity:

1. Fill in v4's Groups + Sugar for them

2. Return to MAybe in v5, and write an Arrow instance + Sugar, capable of expressing this:
    Maybe(f) >> g >> h << x == maybe(f, maybe(g, h))(x)

3. Use (2) inside the image-downloader example, and confirm it works.

4. Combine the new material from v5 into v4:
4.1. [IMPORTANT] The Chain/Pipe category - especially from metafuncs.py
4.1. metafunctions: generic_functions, wrapper_functions.py
4.2. The clean distinctions in heirarchy.py (functor/cofunctor/monad/comonad)
4.3. Pysk - the category
4.4. Maybe + unittests
