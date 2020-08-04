'''
笔记
----------
一些常用的工具
'''
import pandas as pd


def read_csv_number_sign(filename):
    '''
    功能
    ----------
    用pandas的read_csv读带#的文件

    参数
    ----------
    filename: 文件名

    返回值
    ----------
    data frame

    '''
    data_frame = pd.read_csv(filename, sep=r'\s+', names=open(filename, 'r').readline().split()[1:], skiprows=1)
    return data_frame
