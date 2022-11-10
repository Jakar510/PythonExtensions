import cython




floating = cython.floating
integral = cython.integral
numeric = cython.numeric
bint = cython.bint
void = cython.void
array = cython.array

# https://docs.cython.org/en/latest/src/userguide/wrapping_CPlusPlus.html
# ctypedef

cpdef class Compares:
    cdef int x

    def __ge__(self, other):
        if not isinstance(other, Compares):
            raise NotImplemented

        return self.x >= (<Compares> other).x

    def __iadd__(self, other):
        pass

    def __eq__(self, other):
        return isinstance(other, Compares) and self.x == (<Compares> other).x

cpdef class Inits:
    def __cinit__(self, *args, **kwargs):
        pass
    def __dealloc__(self):
        pass

    def __init__(self, *args, **kwargs):
        pass
    def __del__(self):
        pass
