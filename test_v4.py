#from typing import Callable, Any, Dict
#import inspect

#from v4.foundations.category.standard import *


#StringElement = SimpleMeta('StringElement', str)
#assert(isinstance(12, StringElement) is False)
#assert(isinstance('xx', StringElement) is True)


#DictCategory = SimpleCategory('DictCategory', Dict, Callable[[Dict], Dict])

#assert(isinstance({}, DictCategory.Element) is True)
#assert(isinstance(dict, DictCategory.Element) is False)
#assert(issubclass(dict, DictCategory.Element) is True)


#def add_name(record: dict) -> dict:
#    record['name'] = 'Foobar'
#    return record
## I just realized that there isn't really a way to check
## if a function meets a signature



#print()
#print("StringElement:", type(StringElement), StringElement)
#print()
#import ipdb
#ipdb.set_trace()
#print()


import unittest

from v4.tests import test_simple

unittest.main(test_simple)
