import functools


def outer(func):
    functools.wraps(func)  # inner.__name__ = func.__name__  inner.__doc__ = func.__doc__  伪装的更像主函数而已

    def inner(*args, **kwargs):  # 如果func()有参数，那装饰器之后func就等价于inner函数，所以也需要参数接收
        print("原函数执行前的任务")  # 当然也可以直接形象接受参数，前提是你知道原函数的参数，如inner(a,b=1,*args, **kwargs)
        if False:
            res = func(*args, **kwargs)  # 这里是真正调用原函数，原函数如果有参数，这里肯定也得有参数啊，这里的参数从inner参数获取
            return res
        else:
            print("原函数执行后的任务")
            print("反向解析跳转登陆界面")

    return inner


@outer
def func(a, b=1):
    print("进入个人详情页")


# func("a", 2)


# 装饰器说明:
# 对于装饰器有一点必须要说明，不然很难理解，就是函数名是否加括号的问题
# 函数加括号表示对函数的调用
# 函数不加括号表示引用，可以理解成一个变量，指向函数代码所在的地址
# 如果上面两行不明白的，会直接在下面两句中迷茫，这也是我原来学装饰器迷茫的地方，（迷茫：一个func被赋值,然后func()就装饰器或闭包生效了)
# func添加装饰器之后 相当于是func = outer(func)    此时函数func相当于一个变量，指向outer(func)函数
# 然而 outer(func) return返回的是inner函数        return 后面的函数是不加括号的，表示引用inner函数
# 所以在执行 func函数的时候，实际上执行的是inner函数  inner函数返回原函数的值，所以在拿该值的时候会执行原来的func函数
# 在inner函数中对原函数func做了功能扩展 比如做是否登陆的判断 如果登陆了执行inner里面的return res实际上是调用原函数，比如打开个人详情页
# 运行程序，修改if判断的结果，查看装饰器运行的结果

# 当理解了上面的单个装饰器的时候再理解多个装饰器，面试题很嚣张的

def outer1(func):
    functools.wraps(func)  # inner.__name__ = func.__name__  inner.__doc__ = func.__doc__  伪装的更像主函数而已

    def inner1(*args, **kwargs):  # 如果func()有参数，那装饰器之后func就等价于inner函数，所以也需要参数接收
        print("原函数执行前的任务1")  # 当然也可以直接形象接受参数，前提是你知道原函数的参数，如inner(a,b=1,*args, **kwargs)
        if True:
            res = func(*args, **kwargs)  # 这里是真正调用原函数，原函数如果有参数，这里肯定也得有参数啊，这里的参数从inner参数获取
            return res
        else:
            print("原函数执行后的任务1")
            print("反向解析跳转登陆界面1")

    return inner1


def outer2(func):
    functools.wraps(func)  # inner.__name__ = func.__name__  inner.__doc__ = func.__doc__  伪装的更像主函数而已

    def inner2(*args, **kwargs):  # 如果func()有参数，那装饰器之后func就等价于inner函数，所以也需要参数接收
        print("原函数执行前的任务2")  # 当然也可以直接形象接受参数，前提是你知道原函数的参数，如inner(a,b=1,*args, **kwargs)
        if True:
            res = func(*args, **kwargs)  # 这里是真正调用原函数，原函数如果有参数，这里肯定也得有参数啊，这里的参数从inner参数获取
            return res
        else:
            print("原函数执行后的任务2")
            print("反向解析跳转登陆界面2")

    return inner2


@outer1
@outer2
def func_s(a, b=1):
    print("进入个人详情页")


func_s("a", 2)
# 下面按照if的判断来做多个装饰的分析
# 首先要明白两个装饰器的闭包形式

# func_s = outer1(outer2(func_s))   # 一句话：括号里面的函数是括号外面的参数也是其内部的func(*args, **kwargs)原函数
# func_s("a", 2)

# 首先看出装饰器是从上向下执行的，先进入到outer1里面，经过判断之后执行里面的inner1函数，判断是否进入res = func(*args, **kwargs)
# 在执行outer1时，实际上执行的是inner1闭包函数，最上面说到 func = outer(func)等价于把outer的inner赋值给了func,并且在inner中扩展了功能和判断是否调用原函数func
# 所以outer1里面这个res = func(*args, **kwargs)是谁呢？他就是outer2(func_s)，因为他就是outer1的参数，也是他的原函数,是对outer2的功能扩展
# 在调用outer2(func_s)的时候，就是func_s = inner2了，在inner2中对func_s做了功能扩展和判断是否调用原函数func_s

# True  True
# 调用outer1装饰器,判断为真，调用res = func(*args, **kwargs)。进入outer2，outer2为真，调用func_s
"""
原函数执行前的任务1
原函数执行前的任务2
进入个人详情页
"""
# True  False
# 调用outer1装饰器,判断为真，调用res = func(*args, **kwargs)。进入outer2，outer2为假，不调用func_s
"""
原函数执行前的任务1
原函数执行前的任务2
原函数执行后的任务2
反向解析跳转登陆界面2
"""
# False  True
# 调用outer1装饰器,判断为假，不调用res = func(*args, **kwargs)。不进入outer2，不调用func_s
"""
原函数执行前的任务1
原函数执行后的任务1
反向解析跳转登陆界面1
"""
# False  False
# 调用outer1装饰器,判断为假，不调用res = func(*args, **kwargs)。不进入outer2，不调用func_s
"""
原函数执行前的任务1
原函数执行后的任务1
反向解析跳转登陆界面1
"""
