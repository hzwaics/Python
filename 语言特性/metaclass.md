# Python的元类

## Python中类也是对象
&nbsp;&nbsp;&nbsp;&nbsp;在大多数编程语言中，类就是一组用来描述如何生成一个对象的代码段。当然在 Python 中这一点也是成立的。
```python
>>> class ObjectCreator(object):
...     pass
...
>>> my_object = ObjectCreator()
>>> print my_object
<__main__.ObjectCreator object at 0x10623de90>
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Python 中的类还远不止如此，类同样也是一种对象。
只要你使用关键字class，Python 解释器在执行的时候就会创建一个对象。下面的代码段：
```python
>>> class ObjectCreator(object):
...     pass
...
```
&nbsp;&nbsp;&nbsp;&nbsp;将在内存中创建一个对象，名字就是 ObjectCreator，这
个对象（类）自身拥有创建对象（类实例）的能力，而这就是为什么它是一个类的原因。但是
，它的本质仍然是一个对象，所以你就可以对它做如下的操作了：
- 你可以将它赋值给一个变量
- 你可以拷贝它
- 你可以为它增加属性
- 你可以将它作为函数参数进行传递
```python
>>> print ObjectCreator  # 你可以打印一个类，因为它其实也是一个对象
<class '__main__.ObjectCreator'>
>>> def echo(o):
...     print o
...
>>> echo(ObjectCreator)                 # 你可以将类做为参数传给函数
<class '__main__.ObjectCreator'>
>>> print hasattr(ObjectCreator, 'new_attribute')
False
>>> ObjectCreator.new_attribute = 'foo'  #  你可以为类增加属性
>>> print hasattr(ObjectCreator, 'new_attribute')
True
>>> print ObjectCreator.new_attribute
foo
>>> ObjectCreatorMirror = ObjectCreator  # 你可以将类赋值给一个变量
>>> print ObjectCreatorMirror()
<__main__.ObjectCreator object at 0x10624f710>
```

## 动态创建类
&nbsp;&nbsp;&nbsp;&nbsp;因为类也是对象，所以你可以在运行时动态的创建它们，
就像其他任何对象一样。首先，你可以在函数中创建类，使用class关键字即可。
```python
>>> def choose_class(name):
...     if name == 'foo':
...         class Foo(object):
...             pass
...         return Foo    # 返回的是类，不是类的实例
...     else:
...         class Bar(object):
...             pass
...         return Bar
...
>>> MyClass = choose_class('foo')
>>> print MyClass  # 函数返回的是类，不是类的实例
<class '__main__.Foo'>
>>> print MyClass()            # 你可以通过这个类创建类实例，也就是对象
<__main__.Foo object at 0x10624f750>
```
&nbsp;&nbsp;&nbsp;&nbsp;但是这还不够动态，因为你仍然需要自己编写整个类的代
码，由于类也是对象，所以它们必须是通过什么东西来生成的才对，当你使用class关键
字的时候，Python 解释器自动创建这个对象。和 Python 中的大多数事情一样，Python 
仍然提供给你手动处理的方法。还记得内建函数type吗？这个古老但强大的函数能够让你
知道一个对象的类型是什么：
```python
>>> print type(1)
<type 'int'>
>>> print type("1")
<type 'str'>
>>> print type(ObjectCreator)
<type 'type'>
>>> print type(ObjectCreator())
<class '__main__.ObjectCreator'>
```

&nbsp;&nbsp;&nbsp;&nbsp;在这里，type有一种完全不同的能力，它也能动态的创建类，
type 可以接受一个类的描述作为参数，然后返回一个类，type 可以像这样工作：
```python
type(类名, 父类的元组（针对继承的情况，可以为空）, 包含属性的字典（名称和值）)
```

&nbsp;&nbsp;&nbsp;&nbsp;比如下面的这一段代码:
```python
class MyShinyClass(object):
...     pass
```

&nbsp;&nbsp;&nbsp;&nbsp;可以使用 type 手动创建：
```python
>>> MyShinyClass = type('MyShinyClass', (), {})  # 返回一个类对象
>>> print MyShinyClass
<class '__main__.MyShinyClass'>
>>> print MyShinyClass()  # 创建一个该类的实例
<__main__.MyShinyClass object at 0x10624f790>
```

&nbsp;&nbsp;&nbsp;&nbsp;你会发现我们使用"MyShinyClass"作为类名，并且也可以把它
当做一个变量来作为类的引用。如果要定义属性的话，比如下面的类：
```python
>>> class Foo(object):
```


