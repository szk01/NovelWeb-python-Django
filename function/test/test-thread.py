#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Su

'''利用装饰器限制函数的执行时间
    把要执行的函数设置成用户线程,超时就抛出异常'''

import time
from threading import Thread

def time_limited_pri(time_limited):
    def wrapper(func):  #接收的参数是函数
        def __wrapper():
            class TimeLimited(Thread):  #class中的两个函数是必须的
                def __init__(self):
                    Thread.__init__(self)

                def run(self):
                    func()

            t = TimeLimited()
            t.setDaemon(True)  #这个用户线程必须设置在start()前面
            t.start()
            t.join(timeout=time_limited)
            if t.is_alive():
                raise Exception('Function execution overtime')

        return __wrapper

    return wrapper


#使用装饰器
@time_limited_pri(10)   #把这个功能装饰到function()函数上
def function():
    time.sleep(11)
    print('我是用户进程')

if __name__ == '__main__':
    try:
        function()
    except Exception as e:
        print(e)