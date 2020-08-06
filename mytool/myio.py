'''
笔记
----------
一些常用的io函数
'''
import re
from io import StringIO
import pandas as pd
import numpy as np
from ase import io


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
    读LAMMPS的thermo文件

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


def extxyz2dump(f_extxyz, f_dump):
    '''
    功能
    ----------
    将extxyz文件转为LAMMPS dump文件，注意仅支持正交盒子

    参数
    ----------
    f_extxyz: extxyz文件名
    f_dump: LAMMPS dump文件名

    返回值
    ----------
    无
    '''
    atoms = io.read(f_extxyz, index=':', format='extxyz')
    f_output = open(f_dump, 'w')
    for i in range(len(atoms)):
        cell = np.array(atoms[i].get_cell())
        positions = atoms[i].get_positions()
        chemical_symbols = atoms[i].get_chemical_symbols()
        chemical_symbols_list = list()
        atom_types = list()
        for j in range(len(chemical_symbols)):
            if chemical_symbols[j] not in chemical_symbols_list:
                chemical_symbols_list.append(chemical_symbols[j])
            atom_types.append(chemical_symbols_list.index(chemical_symbols[j])+1)
        f_output.write('ITEM: TIMESTEP\n')
        f_output.write('%d\n' % i)
        f_output.write('ITEM: NUMBER OF ATOMS\n')
        f_output.write('%d\n' % len(positions))
        f_output.write('ITEM: BOX BOUNDS pp pp pp\n')
        f_output.write('0.0 %f\n' % cell[0][0])
        f_output.write('0.0 %f\n' % cell[1][1])
        f_output.write('0.0 %f\n' % cell[2][2])
        f_output.write('ITEM: ATOMS id type x y z\n')
        for j in range(len(positions)):
            f_output.write('%d %d %f %f %f\n' %(j, atom_types[j], positions[j][0], positions[j][1], positions[j][2]))
