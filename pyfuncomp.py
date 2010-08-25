# -*- coding: utf-8 -*-

from functools import partial
import itertools

__all__ = ["_", "c", "composable"]

class ComposableFunction(object):
    func = None
    args = []
    kwargs = {}

    def _isSubst(self, x):
        return isinstance(x, ToBeSubstituted)

    def __init__(self, func, args=[], kwargs={}):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, arg):
        replacer = lambda x: arg if self._isSubst(x) else x
        args = map(replacer, self.args)
        kwargs = dict(zip(self.kwargs.keys(),
                          map(replacer, self.kwargs.values())))
        if len(args) + len(kwargs) > 0:
            return self.func(*args, **kwargs)
        else:
            return self.func(arg)

    def __getitem__(self, arglist):
        args = filter(lambda x: not isinstance(x, slice), arglist)
        kwargs = dict([(x.start, x.end) for x in arglist if isinstance(x, slice)])
        return ComposableFunction(self.func, args, kwargs)

    def __lshift__(self, y):
        f = lambda x: self(y(x))
        return ComposableFunction(f)

    def __rshift__(self, y):
        f = lambda x: y(self(x))
        return ComposableFunction(f)

    def __getattr__(self, name):
        if name == "map":
            f = lambda x: map(self, x)
            return ComposableFunction(f)
        elif name == "filter":
            f = lambda x: filter(self, x)
            return ComposableFunction(f)
        else:
            raise AttributeError("Not implemented modifier %s" % name)

class ToBeSubstituted:
    pass

#decorator
def composable(f):
    return ComposableFunction(f)
#substitution mark
_ = ToBeSubstituted()
#transformer function
c = composable

if __name__ == "__main__":
    @composable
    def f1(x):
        return x * 2

    @composable
    def f2(x):
        return x + 3

    @composable
    def f3(x):
        return (-1) * x

    @composable
    def f4(a):
      return a + [0]

    @composable
    def sqrsum(x, y):
        return x ** 2 + y ** 2

    print f1(2) #4
    print f2(2) #5
    print (f1 << f2 << f1)(2) #14
    print (f3 >> f2)(2) #1
    print (f2 >> f3)(2) #-5
    print (c(float) << f1 << f2)(4) #14.0
    print (sqrsum[_, 1] << f1)(2) #17
    print (sqrsum[_, 1].map)([1, 2, 3, 4, 5])

"""
TODO:
-add support of "eval"
"""
