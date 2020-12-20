'''
笔记
----------
一些常用的函数
'''
import numpy as np


def seq(first, increment, last):
    '''
    功能
    ----------
    模仿Shell里的seq

    参数
    ----------
    first: 第一个数
    increment: 间隔
    last：最后一个数
    type: 数据类型

    返回值
    ----------
    numpy array
    '''
    return np.arange(first, last+increment, increment)
