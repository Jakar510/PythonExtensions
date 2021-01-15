import logging

from .switcher import SwitchCase

def example1(test=10):
    """
        Tests simple integers.

    :return:
    """
    print()

    with SwitchCase(test) as sc:
        sc(2, on_true=print, on_true_args=('test 1',))
        print('example1 sub 1')
        sc(10, on_true=print, on_true_args=('test 2',))  # will break here due to match found.
        print('example1 sub 2')
        sc(12, on_true=print, on_true_args=('test 3',))


def example2():
    """
        Tests simple strings with the catch_value_to_check keyword.
        Note that on_true is a callable function.

    :return:
    """
    print()
    test = '10'
    with SwitchCase(test, catch_value_to_check=True) as sc:
        on_true = lambda x: print(f'testing... {x}')

        sc(2, on_true=on_true)
        print('example2 sub 1')
        sc('1', on_true=on_true)
        print('example2 sub 2')
        sc('10', on_true=on_true)  # will break here due to match found.


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
        return {
                'args':   args,
                'kwargs': kwargs
                }
    test = '10'
    switcher = SwitchCase(test, catch_value_to_check=True)
    with switcher as sc:
        on_true = lambda x: run_test(x, *args, **kwargs)

        sc(2, on_true=on_true)
        print('example3 sub 1')
        sc('1', on_true=on_true)  # will break here due to match found.
        print('example3 sub 2')
        sc('10', on_true=on_true)
    print(switcher.result)


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

    class Test(base):
        def __eq__(self, other):
            if isinstance(other, Test):
                return other.id == self.id
            elif isinstance(other, int):
                return other == self.id
            return False


    target1 = Test('Target')
    instance_switcher = SwitchCase(target1, Check_Instance=True)
    with instance_switcher as sc:
        sc(1)
        print('example4.1 sub 1')
        sc('')
        print('example4.1 sub 2')
        sc(None)
        print('example4.1 sub 3')
        sc(TypeError)
        print('example4.1 sub 4')
        sc(Test('Test'))  # will break here due to match found.
        print('example4.1 sub 5')
        sc(int)
        print('example4.1 sub 6')
        sc({})
        print('example4.1 sub 7')
        sc(base('base'))
        print('example4.1 sub 8')

    print()
    target2 = Test('Target')
    SubClass_switcher = SwitchCase(target2, Check_SubClass=True)
    with SubClass_switcher as sc:
        sc(1)
        print('example4.2 sub 1')
        sc('')
        print('example4.2 sub 2')
        sc(None)
        print('example4.2 sub 3')
        sc(TypeError)
        print('example4.2 sub 4')
        sc(Test('Test'))  # will break here due to match found.
        print('example4.2 sub 5')
        sc(int)
        print('example4.2 sub 6')
        sc({})
        print('example4.2 sub 7')
        sc(base('base'))
        print('example4.2 sub 8')

    print()
    target3 = Test('Target')
    value_switcher = SwitchCase(target3)

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

