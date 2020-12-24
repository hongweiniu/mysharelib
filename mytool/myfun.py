'''
笔记
----------
一些常用的函数
'''
import os
import numpy as np


def mkdir(path):
    '''
    功能
    ----------
    模仿Shell里的mkdir

    参数
    ----------
    path: 文件夹路径

    返回值
    ----------
    无
    '''
    os.makedirs(path, exist_ok=True)


def seq(*args):
    '''
    功能
    ----------
    模仿Shell里的seq

    参数
    ----------
    一个两个或者三个数

    返回值
    ----------
    numpy array
    '''
    if len(args) == 1:
        return np.arange(1, args[0]+1)
    elif len(args) == 2:
        return np.arange(args[0], args[1]+1)
    elif len(args) == 3:
        return np.arange(args[0], args[2]+args[1], args[1])
    else:
        print('error using mytool.myfun.seq!!!')
        exit('1')
