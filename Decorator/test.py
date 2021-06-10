# coding=utf-8

# def my_sum(*args):
def my_sum(*args, **kwargs):
    result = 0
    print type(args)

    print type(kwargs)
    # Iterating over the Python args tuple
    for x in kwargs.keys():
        print(x)
    for y in args:
        print(y)
    #     result += x
    # return result
 
print(my_sum(1, 2, [3,4], a=5))