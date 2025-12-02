# python 中的闭包
# 了解闭包前先明确一点：在python中，既然万物皆对象，那么函数本身自然也是对象
#所谓闭包，就是指在函数内部定义的，可以访问函数外部参数的函数
#实际上，在使用任意带参数的装饰器时就在使用闭包：
#装饰器本身实际上是一个接收函数作为参数的函数，其返回值也是一个参数，装饰器的作用实际上是:对函数进行特定性质的改造
#请看VCR：
def html_tags(tag_name):
    #定义一个装饰器，作用是为页面添加标签，最外层的包装用于传入参数tag
    def wrapper_(func):
        #内层的装饰器定义
        def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)#可以接收参数函数的任意返回值作为content 的内容
            return "<{tag}>{content}</{tag}>".format(tag=tag_name, content=content)#这里使用了wrapper的外层变量tag_name
        return wrapper
    return wrapper_

@html_tags('b')
def hello(name='Toby'):
    return 'Hello {}!'.format(name)

# 不用@的写法如下
# hello = html_tag('b')(hello)
# html_tag('b') 是一个闭包，它接受一个函数，并返回一个函数

print(hello())  # <b>Hello Toby!</b>
print(hello('world'))  # <b>Hello world!</b>

#闭包的内层实现：很简单，闭包函数相对与普通函数会多出一个__closure__的属性，里面定义了一个元组用于存放所有的cell对象，每个cell对象一一保存了这个闭包中所有的外部变量。
def make_printer(msg1, msg2):
    def printer():
        print(msg1, msg2)
    return printer
printer = make_printer('Foo', 'Bar')  # 形成闭包
print(printer.__closure__)# 返回cell元组
#(<cell at 0x0000021BD5921F70: str object at 0x0000021BD3D52D30>, <cell at 0x0000021BD5921E20: str object at 0x0000021BD3D52EB0>)
print(printer.__closure__[0].cell_contents)  # 第一个外部变量
#Foo
print(printer.__closure__[1].cell_contents)  # 第二个外部变量
#Bar