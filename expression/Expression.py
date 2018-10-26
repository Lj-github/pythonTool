# -*- coding: utf-8 -*-
# @Time    : 2018/10/26 上午11:54

"""
    1 false
"""
# 布尔类型的值，表示假，与true对应


"""
    2 class
"""


# 定义类的关键字

class Person:
    "Person类"

    def __init__(self, name, age, gender):
        print('进入Person的初始化')
        self.name = name
        self.age = age
        self.gender = gender
        print('离开Person的初始化')

    def getName(self):
        print(self.name)


p = Person('ice', 18, '男')

print(p.name)  # ice
print(p.age)  # 18
print(p.gender)  # 男
print(hasattr(p, 'weight'))  # False
# 为p添加weight属性
p.weight = '70kg'
print(hasattr(p, 'weight'))  # True
print(getattr(p, 'name'))  # ice

print(p.__dict__)  # {'age': 18, 'gender': '男', 'name': 'ice'}
print(Person.__name__)  # Person
print(Person.__doc__)  # Person类
print(
    Person.__dict__)  # {'__doc__': 'Person类', '__weakref__': <attribute '__weakref__' of 'Person' objects>, '__init__': <function Person.__init__ at 0x000000000284E950>, 'getName': <function Person.getName at 0x000000000284EA60>, '__dict__': <attribute '__dict__' of 'Person' objects>, '__module__': '__main__'}
print(Person.__mro__)  # (<class '__main__.Person'>, <class 'object'>)
print(Person.__bases__)  # (<class 'object'>,)
print(Person.__module__)  # __main__


# python通过变量名命名来区分属性和方法的访问权限，默认权限相当于c + +和java中的public
#
# 类的私有属性： __private_attrs：两个下划线开头，声明该属性为私有，不能在类地外部被使用或直接访问。在类内部的方法中使用时self.__private_attrs。
#
# 类的私有方法：__private_method：两个下划线开头，声明该方法为私有方法，不能在类地外部调用。在类的内部调用
# self.__private_methods

class Demo:
    __id = 123456

    def getId(self):
        return self.__id


temp = Demo()
# print(temp.__id)  # 报错 AttributeError: 'Demo' object has no attribute '__id'
print(temp.getId())  # 123456
print(temp._Demo__id)  # 123456


## 继承

class ParentClass1:  # 定义父类
    pass


class ParentClass2:  # 定义父类
    pass


class SubClass1(ParentClass1):  # 单继承，基类是ParentClass1，派生类是SubClass
    pass


class SubClass2(ParentClass1, ParentClass2):  # python支持多继承，用逗号分隔开多个继承的类
    pass


# supper
class A:
    def print(self):
        print('A')


class B(A):
    def print(self):
        super().print()
        # super(B,self).hahaha()
        # A.hahaha(self)
        print('B')


a = A()
b = B()
b.print()
super(B, b).print()

"""
    3 finally
"""


class MyException(Exception): pass


try:
    # some code here
    raise MyException
except MyException:
    print("MyException encoutered")
finally:
    print("Arrive finally")

"""
    4 is
"""
# Python中的对象包含三个要素：id,type,value

# id:用来唯一标示一个对象
# type：标识对象的类型
# value：是对象的值
# is：就是用来判断a对象是否就是b对象，是通过id来判断的
# ==：判断的是a对象的值是否和b对象的值相等，是通过value来判断的
a = 1
b = 1.0
a is b
# False
a == b
# True
print(id(a))
print(id(b))

"""
    5 return
"""
# 返回值


"""
    6  none
"""
# 空
"""
    7  continue
"""
"""
    8 for
"""
"""
    9  lambda
"""
# 匿名函数

g = lambda x: x + 1

print(g(1))
print(g(2))
print(g(7))

foo = [2, 18, 9, 22, 17, 24, 8, 12, 27]
print(filter(lambda x: x % 3 == 0, foo))
print(map(lambda x: x * 2 + 10, foo))

"""
    10  try
"""

"""
    11  true
"""

"""
    12  def
"""
"""
    13  from
"""
"""
    14  nonlocal
"""


# nonlocal关键字用来在函数或其他作用域中使用外层（非全局）变量。
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


def make_counter_test():
    mc = make_counter()
    print(mc())
    print(mc())
    print(mc())


make_counter_test()
"""
    15  while
""""""
    16  and
"""
"""
    17  del
"""
# del用于list列表操作，删除一个或者连续几个元素。

a = [-1, 3, 'aa', 85]  # 定义一个list
del a[0]  # 删除第0个元素
del a[2:4]  # 删除从第2个到第3个元素。

"""
    18  global
"""
# 定义全局标量。
"""
    19  not
"""

"""
    20  with
"""


# with是python2.5以后有的，它实质是一个控制流语句，with可以用来简化try…finally语句，它的主要用法是实现一个类_enter_()和_exit_()方法。
class controlled_execution:
    def __enter__(self):
        print("__enter__")
        return "Foo"

    def __exit__(self, type, value, traceback):
        print("__exit__")


def get_sample():
    return controlled_execution()


with controlled_execution() as sample:
    print(sample)

"""
    21  as
"""
"""　　　　　　
    22  elif　　　　　　
"""
"""
    23  if
"""
"""
    24  or
"""

"""
    25  yield
"""


# yield用起来像return,yield在告诉程序，要求函数返回一个生成器
def createGenerator():
    mylist = range(3)
    for i in mylist:
        yield i * i


def fibonacci(n):  # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1


f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成

while True:
    try:
        print(next(f), end=" ")
    except StopIteration:
        break

"""
    26  assret
"""

# 断言，用来在运行中检查程序的正确性，和其他语言一样的作用。
# mylist = []
# assert len(mylist) >= 1

"""
    27  else
"""

"""
    28  import
"""

"""
    29  pass
"""


# pass的意思是什么都不要做，作用是为了弥补语法和空定义上的冲突，
# 它的好处体现在代码的编写过程之中，比如你可以先写好软件的整个框架，
# 然后再填好框架内具体函数和class的内容，如果没有pass编译器会报一堆的错误，让整个开发很不流畅。
def f(arg): pass  # a function that does nothing (yet)


class C: pass  # a class with no methods(yet)


"""
    30  break
"""

"""
    31  except
"""

"""
    32  in
"""

"""
    33  raise
"""


# railse抛出异常。

print("\n")

class MyException(Exception): pass

try:
    # some code here
    raise MyException
except MyException:
    print('MyException encoutered')
finally:
    print('Arrive finally')
