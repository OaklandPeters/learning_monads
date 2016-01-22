"""
To-do:
* Record notes on functions
* Draft some basic unit-tests, inspired from list.py
"""
import category

class StreamCategory(category.Category):
    pass


class Stream(category.Monad):
    def __init__(self, *elements):
        self.data = elements

    def __iter__(self):
        return iter(self.data)
