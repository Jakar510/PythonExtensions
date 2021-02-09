import random
import unittest

from PythonExtensions.SwitchCase import *




__all__ = [
    'SwitchCase_TestCase',
    ]

YOU_SHOULD_NOT_SEE_THIS = 'YOU_SHOULD_NOT_SEE_THIS'


class SwitchCase_TestCase(unittest.TestCase):
    class base(object):
        # id = uuid.uuid4()
        def __init__(self, _id):
            self.id = _id
        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return other.id == self.id

            return False



    class Test(base): pass



    @classmethod
    def setUpClass(cls):
        return cls()
    @classmethod
    def tearDownClass(cls):
        return cls()

    def setUp(self) -> None:
        pass
    def tearDown(self):
        pass

    def test_int(self):
        self.value = random.choice(list(range(20)))
        with SwitchVariable(self.value) as sc:
            if sc(2): self.assertEqual(2, self.value)
            if sc(3): self.assertEqual(3, self.value)
            if sc(4): self.assertEqual(4, self.value)
            if sc(5): self.assertEqual(5, self.value)
            if sc(10): self.assertEqual(10, self.value)
            if sc(11): self.assertEqual(11, self.value)
            if sc(12): self.assertEqual(12, self.value)
            if sc(13): self.assertEqual(13, self.value)
            if sc(14): self.assertEqual(14, self.value)
            if sc(15): self.assertEqual(15, self.value)

    def test_str(self):
        self.value = random.choice(list(map(str, range(20))))
        with SwitchVariable(self.value) as sc:
            if sc('2'): self.assertEqual('2', self.value)
            if sc('3'): self.assertEqual('3', self.value)
            if sc('4'): self.assertEqual('4', self.value)
            if sc('5'): self.assertEqual('5', self.value)
            if sc('10'): self.assertEqual('10', self.value)
            if sc('11'): self.assertEqual('11', self.value)
            if sc('12'): self.assertEqual('12', self.value)
            if sc('13'): self.assertEqual('13', self.value)
            if sc('14'): self.assertEqual('14', self.value)
            if sc('15'): self.assertEqual('15', self.value)


    def test_class(self):
        with SwitchSubClass(self.base) as sc:
            sc(int)
            print('example4.2 sub 1')
            sc(str)
            print('example4.2 sub 2')
            sc(type(None))
            print('example4.2 sub 3')
            sc(TypeError)
            print('example4.2 sub 4')
            sc(self.Test)  # will break here due to match found.
            print('example4.2 sub 5' + YOU_SHOULD_NOT_SEE_THIS)
            sc(int)
            print('example4.2 sub 6' + YOU_SHOULD_NOT_SEE_THIS)
            sc(dict)
            print('example4.2 sub 7' + YOU_SHOULD_NOT_SEE_THIS)
            sc(self.base)
            print('example4.2 sub 8' + YOU_SHOULD_NOT_SEE_THIS)
            sc(int)
            print('example4.2 sub 8' + YOU_SHOULD_NOT_SEE_THIS)

    def test_Instance(self):
        target3 = self.Test('Target')
        value_switcher = SwitchInstance(target3)

        with value_switcher as sc:
            if sc(1): self.assertEqual(1, target3)
            if sc(''): self.assertEqual('', target3)
            if sc(None): self.assertEqual(None, target3)
            if sc(TypeError): self.assertEqual(TypeError, target3)
            if sc(self.Test('Test')): self.assertNotEqual(self.Test('Test'), target3)
            if sc(int): self.assertEqual(int, target3)
            if sc({ }): self.assertEqual({ }, target3)
            if sc(self.base('base')): self.assertEqual(self.base('base'), target3)
            if sc(self.Test('Target')): self.assertEqual(self.Test('Target'), target3)

        with self.assertRaises(InactiveSessionError):
            value_switcher('')  # WILL though a InactiveSessionError here as it's not inside of a context manager.

