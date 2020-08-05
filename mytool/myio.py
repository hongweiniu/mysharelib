'''
笔记
----------
一些常用的io函数
'''
import re
from io import StringIO
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


def read_lammps_thermo(filename):
    '''
    功能
    ----------
    读LAMMPS的thermo文件。

    参数
    ----------
    filename: 文件名

    返回值
    ----------
    data frame
    '''
    f_lammps_out = open(filename, 'r')
    str_lammps_out = ''
    while True:
        line = f_lammps_out.readline()
        if not line:
            break
        search = re.search('Step', line)
        if search:
            str_lammps_out = line
            while True:
                line = f_lammps_out.readline()
                search1 = re.search(r'\s+\d+\s+[(\-|\+)?\d+(\.\d+)?\s+]+\n$', line)
                search2 = re.search(r'Loop time of', line)
                if search1:
                    str_lammps_out += line
                if search2:
                    break
    data = StringIO(str_lammps_out)
    data_frame = pd.read_csv(data, sep=r'\s+')
    return data_frame
