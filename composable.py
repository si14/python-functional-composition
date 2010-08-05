# -*- coding: utf-8 -*-

from functools import partial

class _compfunc(partial):
    def __init__(self, func, args_list=None):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        pass
    
    def __lshift__(self, y):
        f = lambda *args, **kwargs: self.func(y(*args, **kwargs)) 
        return _compfunc(f)

    def __rshift__(self, y):
        f = lambda *args, **kwargs: y(self.func(*args, **kwargs)) 
        return _compfunc(f)

def composable(f):
    return _compfunc(f)
    
def c(f):
    return _compfunc(f)

if __name__ == "__main__":
    @composable    
    def f1(x):
        return x * 2
    
    @composable
    def f2(x):
        return  x + 3
    
    @composable
    def f3(x):
        return (-1) * x
        
    @composable
    def f4(a):
      return a + [0]
    
    print f1(2) #4
    print f2(2) #5
    print (f1 << f2 << f1)(2) #14
    print (f3 >> f2)(2) #1
    print (f2 >> f3)(2) #-5
    print (composable(float) << f1 << f2)(4) #14.0
"""
Проблемы:
1) нельзя использовать expressions - нужна возможность передачи строки для eval'а
2) нельзя подставлять часть переменных, все функции должны иметь одинаковое кол-во аргументов
3) нужен синтаксический сахар для c(map)[func, x]
"""