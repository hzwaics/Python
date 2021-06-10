# Python 闭包
&nbsp;&nbsp;&nbsp;&nbsp;首先[闭包](https://zh.wikipedia.org/wiki/%E9%97%AD%E5%8C%85_(%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6))是计算机科学中的一种应用技术，其概念出现于60年代，最早实现闭包的程序语言是Scheme。闭包可以用来在一个函数与一组“私有”变量之间创建关联关系。

## 1.闭包例子
&nbsp;&nbsp;&nbsp;&nbsp;python中使用闭包主要是在进行函数式开发时使用。以具体例子，讲解闭包在python中的应用：在一个内部函数中，对外部作用域的变量进行引用，(并且一般外部函数的返回值为内部函数)，那么内部函数就被认为是闭包。
```python
def startAx(x):
    def incrementBy(y):
        return  x+y
    return incrementBy
```

&nbsp;&nbsp;&nbsp;&nbsp;在函数startAt中定义了一个incrementBy函数，incrementBy访问了外部函数startAt的变量，并且函数返回值为incrementBy函数
```python
a = startAx(1)
print("function:", a)
print("function.name:", a.func_name)
print("result:", a(1))
print("result:", a(3))
```
&nbsp;&nbsp;&nbsp;&nbsp;执行结果：
```python
('function:', <function incrementBy at 0x1039910c8>)
('function.name:', 'incrementBy')
('result:', 2)
('result:', 4)
```
&nbsp;&nbsp;&nbsp;&nbsp;a是函数incrementBy而不是startAt，如果调用函数a的话，得到的结果是传入参数的整数值加1。


## 2.常见问题
### 2.1 闭包无法改变外部函数局部变量指向的内存地址
- 当外部函数的局部变量为[不可变类型](https://zhuanlan.zhihu.com/p/130773890)时，修改时会改变其内存地址。
- 当局部变量为可变类型是，不改变其内存地址，添加内容的话，是能够改变成功的。

```python
def outerFunc():
    x = 0
    def innerFunc():
        x = 1
        print("inner x:", x)

    print("outer x before call inner:", x)
    innerFunc()
    print("outer x after call inner:", x)
```
&nbsp;&nbsp;&nbsp;&nbsp;执行结果：
```python
('outer x before call inner:', 0)
('inner x:', 1)
('outer x after call inner:', 0)
```

### 2.2 python循环中不包含域的概念
&nbsp;&nbsp;&nbsp;&nbsp;返回闭包时牢记的一点就是：返回函数不要引用任何循环变量，或者后续会发生变化的变量。

&nbsp;&nbsp;&nbsp;&nbsp;如果一定要引用循环变量怎么办？方法是再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变

```python
first = []

for i in xrange(3):
    def func(x):
        return x*i
    first.append(func)

for f in first:
    print f(2)
```
&nbsp;&nbsp;&nbsp;&nbsp;按照大家正常的理解，应该输出的是0, 2, 4对吧？但实际输出的结果是:4, 4, 4. 原因是什么呢？loop在python中是没有域的概念的，flist在像列表中添加func的时候，并没有保存i的值，而是当执行f(2)的时候才去取，这时候循环已经结束，i的值是2，所以结果都是4。

&nbsp;&nbsp;&nbsp;&nbsp;在程序里面经常会出现这类的循环语句，Python的问题就在于，当循环结束以后，循环体中的临时变量i不会销毁，而是继续存在于执行环境中。还有一个python的现象是，python的函数只有在执行时，才会去找函数体里的变量的值。

&nbsp;&nbsp;&nbsp;&nbsp;通过闭包就可以修改上面的实现
```python
first = []

for i in xrange(3):
    def makefunc(i):
        def func(x):
            return x*i
        return func
    first.append(makefunc(i))

for f in first:
    print f(2)
```

### 2.3 python闭包的作用
用途1：当闭包执行完后，仍然能够保持住当前的运行环境。

&nbsp;&nbsp;&nbsp;&nbsp;举例：如果你希望函数的每次执行结果，都是基于这个函数上次的运行结果。以一个类似棋盘游戏的例子来说明。假设棋盘大小为50*50，左上角为坐标系原点(0,0)，我需要一个函数，接收2个参数，分别为方向(direction)，步长(step)，该函数控制棋子的运动。 这里需要说明的是，每次运动的起点都是上次运动结束的终点。
```python
origin = [0, 0] # 坐标系统原点
legal_x = [0, 50] # x轴方向的合法坐标
legal_y = [0, 50] # y轴方向的合法坐标
def create(pos=origin):
    def player(direction, step):
    # 这里应该首先判断参数direction,step的合法性，比如direction不能斜着走，step不能为负等
    # 然后还要对新生成的x，y坐标的合法性进行判断处理，这里主要是想介绍闭包，就不详细写了。
        new_x = pos[0] + direction[0] * step
        new_y = pos[1] + direction[1] * step
        pos[0] = new_x
        pos[1] = new_y
        # 注意！此处不能写成 pos = [new_x, new_y]，原因在上文有说过
        return pos

    return player

go = create()
print go([1,0], 10)  # 向x轴正向走10步
print go([0,1], 20)  # 向y轴正向走20步
print go([-1,0], 10) # 向x轴反向走10步
```
&nbsp;&nbsp;&nbsp;&nbsp;执行结果：
```python
[10, 0]
[10, 20]
[0, 20]
```
&nbsp;&nbsp;&nbsp;&nbsp;也就是我们先沿X轴前进了10，然后沿Y轴前进了20，然后反方向沿X轴退了10，坐标分别问[10,0], [10, 20], [0, 20]。


用途2：闭包可以根据外部作用域的局部变量来得到不同的结果

&nbsp;&nbsp;&nbsp;&nbsp;举例：比如有时我们需要对某些文件的特殊行进行分析，先要提取出这些特殊行。
```python
def make_filter(keep):
    def the_filter(file_name):
        file = open(file_name)
        lines = file.readlines()
        file.close()
        filter_doc = [i for i in lines if keep in i]
        return filter_doc

    return the_filter
```
&nbsp;&nbsp;&nbsp;&nbsp;如果我们需要取得文件"result.txt"中含有"pass"关键字的行，则可以这样使用例子程序。
```python
filter = make_filter("pass")
filter_result = filter("result.txt")
```

用途3：闭包在爬虫以及web应用中都有很广泛的应用，并且闭包也是装饰器的基础。


## 3.底层实现
- 参考：https://wklken.me/posts/2015/09/04/python-source-closure.html