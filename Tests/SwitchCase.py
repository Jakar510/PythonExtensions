import logging

from PythonExtensions.SwitchCase import *

BREAK = ' ---> you should not see this'
def example1(test=10):
    """
        Tests simple integers.

    :return:
    """
    print()

    with SwitchVariable(test) as sc:
        sc(2)
        print('example1 sub 1')
        sc(10)  # will break here due to match found.
        print('example1 sub 2' + BREAK) #
        sc(12)


def example2():
    """
        Tests simple strings with the catch_value_to_check keyword.
        Note that on_true is a callable function.

    :return:
    """
    print()
    test = '10'
    with SwitchVariable(test) as sc:
        on_true = lambda x: print(f'testing... {x}')

        sc(2)
        print('example2 sub 1')
        sc('1')
        print('example2 sub 2')
        sc('10')  # will break here due to match found.


def example3(*args, **kwargs):
    """
        Tests the catch_value_to_check keyword.
        Note that on_true is a callable function.

    :param args:
    :param kwargs:
    :return:
    """
    print()
    def run_test(*args, **kwargs):
        print({
                'args':   args,
                'kwargs': kwargs
                })

    test = '10'
    with SwitchCallback(test) as sc:

        sc(2, run_test)
        print('example3 sub 1')
        sc('1', run_test)  # will break here due to match found.
        print('example3 sub 2' + BREAK)
        sc('10', run_test)


def example4():
    """
        Tests the Check_Instance and Check_SubClass options.

    :return:
    """
    print()
    class base(object):
        # id = uuid.uuid4()
        def __init__(self, id):
            self.id = id
        def __eq__(self, other):
            if isinstance(other, base):
                return other.id == self.id
            return False

    class Test(base): pass


    target1 = Test('Target')
    with SwitchVariable(target1) as sc:
        sc(1)
        print('example4.1 sub 1')
        sc('')
        print('example4.1 sub 2')
        sc(None)
        print('example4.1 sub 3')
        sc(TypeError)
        print('example4.1 sub 4')
        sc(Test('Test'))  # will break here due to match found.
        print('example4.1 sub 5' + BREAK)
        sc(int)
        print('example4.1 sub 6' + BREAK)
        sc({})
        print('example4.1 sub 7' + BREAK)
        sc(Test('base'))
        print('example4.1 sub 8' + BREAK)

    print()
    target2 = base
    with SwitchSubClass(target2) as sc:
        sc(int)
        print('example4.2 sub 1')
        sc(str)
        print('example4.2 sub 2')
        sc(type(None))
        print('example4.2 sub 3')
        sc(TypeError)
        print('example4.2 sub 4')
        sc(Test)  # will break here due to match found.
        print('example4.2 sub 5' + BREAK)
        sc(int)
        print('example4.2 sub 6' + BREAK)
        sc(dict)
        print('example4.2 sub 7' + BREAK)
        sc(base)
        print('example4.2 sub 8' + BREAK)
        sc(int)
        print('example4.2 sub 8' + BREAK)

    print()
    target3 = Test('Target')
    value_switcher = SwitchInstance(target3)

    # sc.set_variable_to_check(1)
    with value_switcher as sc:
        sc(1)
        print('example4.3 sub 1')
        sc('')
        print('example4.3 sub 2')
        sc(None)
        print('example4.3 sub 3')
        sc(TypeError)
        print('example4.3 sub 4')
        sc(Test('Test'))
        print('example4.3 sub 5')
        sc(int)
        print('example4.3 sub 6')
        sc({})
        print('example4.3 sub 7')
        sc(base('base'))
        print('example4.3 sub 8')
        # will break here due NO to match found.

    try: value_switcher('')  # WILL though a InactiveSessionError here as it's not inside of a context manager.
    except Exception as e:
        logger = logging.getLogger('example4')
        logger.exception(e)
def example5():
    pass



def run_tests():
    example1()
    example2()
    example3()
    example4()
    example5()


if __name__ == '__main__':
    run_tests()

