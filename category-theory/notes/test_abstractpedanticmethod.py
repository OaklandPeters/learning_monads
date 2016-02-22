"""
Testing behavior of abstractpedanticmethod.
"""
import unittest
import abc

from support_pre import abstractpedanticmethod, pedanticmethod, standard_repr


class Addable(metaclass=abc.ABCMeta):
    def __init__(self, value):
        self.value = value

    @abstractpedanticmethod
    def add(cls, left, right: int):
        return NotImplemented

    @pedanticmethod
    def add_three(cls, one, two, three):
        return cls.adder(one, cls.adder(two, three))

    def __repr__(self):
        return standard_repr(self, self.value)

    def __eq__(self, other):
        if isinstance(other, Addable):
            return self.value == other.value
        else:
            return False


class MockValue:
    def __init__(self, value):
        self.value = value

    @classmethod
    def lift(cls, value):
        return MockValue(value)

    def __repr__(self):
        return standard_repr(self, self.value)

    def __eq__(self, other):
        if hasattr(other, 'value'):
            return self.value == other.value
        else:
            return False


class PedanticMethodTests(unittest.TestCase):

    def test_abstraction_error(self):
        class ShouldError(Addable):
            pass
        self.assertRaises(
            TypeError,
            lambda : ShouldError(12)
        )

    def test_override_abstractpedantic_with_instancemethod(self):
        """Overriding abstractpedanticmethod with an instance method
        should result 
        """
        class InstanceOverride(Addable):
            def add(self, right):
                return InstanceOverride(self.value + right)
        class MockValue:
            def __init__(self, value):
                self.value = value

        inst = InstanceOverride(1)
        self.assertEqual(inst.add(2), InstanceOverride(3))
        # Confirm that the classmethod version works
        mock = MockValue(1)
        self.assertEqual(InstanceOverride.add(mock, 2), InstanceOverride(3))
        self.assertEqual(InstanceOverride.add(InstanceOverride(2), 1), InstanceOverride(3))  
    
    def test_override_abstractpedantic_with_classmethod(self):
        """
        This should result in errors in some cases
        """
        class ClassOverride(Addable):
            @classmethod
            def add(cls, left, right):
                return ClassOverride(left.value + right)
        inst = ClassOverride(1)
        # 'add' ends up as a classmethod - not a pedantic method
        self.assertEqual(inst.add(inst, 2), ClassOverride(3))
        self.assertEqual(ClassOverride.add(inst, 2), ClassOverride(3))
        

    def test_override_abstractpedantic_with_pedanticmethod(self):
        """
        This should be the same as the instancemethod case, and producde no
        errors.
        """
        class InstanceOverride(Addable):
            @pedanticmethod
            def add(cls, self, right):
                return InstanceOverride(self.value + right)
        inst = InstanceOverride(1)
        self.assertEqual(inst.add(2), InstanceOverride(3))
        # Confirm that the classmethod version works
        mock = MockValue(1)
        self.assertEqual(InstanceOverride.add(mock, 2), InstanceOverride(3))
        self.assertEqual(InstanceOverride.add(InstanceOverride(2), 1), InstanceOverride(3))  

    def test_override_with_inheritance(self):
        class InstanceOverride(Addable):
            @classmethod
            def lift(cls, value):
                return InstanceOverride(value)

            def add(self, right):
                return self.lift(self.value + right)

        class Child(InstanceOverride):
            @classmethod
            def lift(cls, value):
                return Child(value)


        inst = Child(1)
        self.assertEqual(inst.add(2), Child(3))
        self.assertIsInstance(inst.add(2), Child)
        # Confirm that the classmethod version works
        mock = MockValue(1)
        self.assertEqual(Child.add(mock, 2), Child(3))
        self.assertIsInstance(Child.add(mock, 2), MockValue)
        self.assertEqual(Child.add(Child(2), 1), Child(3)) 
        self.assertIsInstance(Child.add(Child(2), 1), Child)

if __name__ == "__main__":
    unittest.main()
