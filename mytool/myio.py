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
from ase import Atoms
from ase.calculators.singlepoint import SinglePointCalculator as SPC
from ase.calculators import calculator


def atoms2data(atoms, f_data, bond_list=None):
    '''
    功能
    ----------
    将atoms(单帧)转为LAMMPS data文件

    参数
    ----------
    atoms: ASE中的atoms对象
    f_data: LAMMPS dada文件名
    bond_list: bond list to write, optional

    返回值
    ----------
    无
    '''
    f_output = open(f_data, 'w')
    cell = np.array(atoms.get_cell())
    volume = atoms.get_volume()
    vec_A = cell[0]
    vec_B = cell[1]
    vec_C = cell[2]
    lx = np.linalg.norm(vec_A)
    xy = np.inner(vec_B, vec_A/np.linalg.norm(vec_A))
    ly = np.sqrt(np.linalg.norm(vec_B)**2-xy**2)
    xz = np.inner(vec_C, vec_A/np.linalg.norm(vec_A))
    yz = (np.inner(vec_B, vec_C)-xy*xz)/ly
    lz = np.sqrt(np.linalg.norm(vec_C)**2-xz**2-yz**2)
    positions = atoms.get_positions()
    positions = np.dot(positions, np.array([[lx, xy, xz], [0.0, ly, yz], [0.0, 0.0, lz]]))
    positions /= volume
    positions = np.dot(positions, np.array([np.cross(vec_B, vec_C), np.cross(vec_C, vec_A), np.cross(vec_A, vec_B)]))
    chemical_symbols = atoms.get_chemical_symbols()
    chemical_symbols_list = list()
    atom_types = list()
    for j in range(len(chemical_symbols)):
        if chemical_symbols[j] not in chemical_symbols_list:
            chemical_symbols_list.append(chemical_symbols[j])
        atom_types.append(chemical_symbols_list.index(chemical_symbols[j])+1)
    f_output.write('data.txt (written by Ricky)\n\n')
    f_output.write('%d atoms\n' % len(positions))
    if bond_list is not None:
        f_output.write('%d bonds\n' % len(bond_list))
    f_output.write('%d atom types\n' % len(chemical_symbols_list))
    if bond_list is not None:
        f_output.write('%d bond types\n' % len(np.unique(bond_list[:, 0])))
    f_output.write('\n')
    f_output.write('0.0 %f xlo xhi\n' % lx)
    f_output.write('0.0 %f ylo yhi\n' % ly)
    f_output.write('0.0 %f zlo zhi\n' % lz)
    f_output.write('%f %f %f xy xz yz\n\n' % (xy, xz, yz))
    f_output.write('Atoms\n\n')
    if bond_list is None:
        for i in range(len(positions)):
            f_output.write('%d %d %f %f %f\n' % (i+1, atom_types[i], positions[i][0], positions[i][1], positions[i][2]))
    else:
        for i in range(len(positions)):
            f_output.write('%d %d %d 1.0 %f %f %f\n' % (i+1, np.where(bond_list[:, 1:] == i)[0][0]+1, atom_types[i], positions[i][0], positions[i][1], positions[i][2]))
        f_output.write('\nBonds\n\n')
        for i in range(len(bond_list)):
            f_output.write('%d %d %d %d\n' % (i+1, bond_list[i][0], bond_list[i][1]+1, bond_list[i][2]+1))
    f_output.close()


def extxyz2data(f_extxyz, f_data, frame):
    '''
    功能
    ----------
    将extxyz文件转为LAMMPS data文件

    参数
    ----------
    f_extxyz: extxyz文件名
    f_data: LAMMPS dada文件名
    frame: which frame of extxyz to convert

    返回值
    ----------
    无
    '''
    atoms = io.read(f_extxyz, index='%d' % frame, format='extxyz')
    f_output = open(f_data, 'w')
    cell = np.array(atoms.get_cell())
    volume = atoms.get_volume()
    vec_A = cell[0]
    vec_B = cell[1]
    vec_C = cell[2]
    lx = np.linalg.norm(vec_A)
    xy = np.inner(vec_B, vec_A/np.linalg.norm(vec_A))
    ly = np.sqrt(np.linalg.norm(vec_B)**2-xy**2)
    xz = np.inner(vec_C, vec_A/np.linalg.norm(vec_A))
    yz = (np.inner(vec_B, vec_C)-xy*xz)/ly
    lz = np.sqrt(np.linalg.norm(vec_C)**2-xz**2-yz**2)
    positions = atoms.get_positions()
    positions = np.dot(positions, np.array([[lx, xy, xz], [0.0, ly, yz], [0.0, 0.0, lz]]))
    positions /= volume
    positions = np.dot(positions, np.array([np.cross(vec_B, vec_C), np.cross(vec_C, vec_A), np.cross(vec_A, vec_B)]))
    chemical_symbols = atoms.get_chemical_symbols()
    chemical_symbols_list = list()
    atom_types = list()
    for j in range(len(chemical_symbols)):
        if chemical_symbols[j] not in chemical_symbols_list:
            chemical_symbols_list.append(chemical_symbols[j])
        atom_types.append(chemical_symbols_list.index(chemical_symbols[j])+1)
    f_output.write('data.txt (written by Ricky)\n\n')
    f_output.write('%d atoms\n' % len(positions))
    f_output.write('%d atom types\n' % len(chemical_symbols_list))
    f_output.write('0.0 %f xlo xhi\n' % lx)
    f_output.write('0.0 %f ylo yhi\n' % ly)
    f_output.write('0.0 %f zlo zhi\n' % lz)
    f_output.write('%f %f %f xy xz yz\n\n' % (xy, xz, yz))
    f_output.write('Atoms\n\n')
    for i in range(len(positions)):
        f_output.write('%d %d %f %f %f\n' % (i+1, atom_types[i], positions[i][0], positions[i][1], positions[i][2]))
    f_output.close()


def extxyz2dump(f_extxyz, f_dump):
    '''
    功能
    ----------
    将extxyz文件转为LAMMPS dump文件

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
        volume = atoms[i].get_volume()
        vec_A = cell[0]
        vec_B = cell[1]
        vec_C = cell[2]
        lx = np.linalg.norm(vec_A)
        xy = np.inner(vec_B, vec_A/np.linalg.norm(vec_A))
        ly = np.sqrt(np.linalg.norm(vec_B)**2-xy**2)
        xz = np.inner(vec_C, vec_A/np.linalg.norm(vec_A))
        yz = (np.inner(vec_B, vec_C)-xy*xz)/ly
        lz = np.sqrt(np.linalg.norm(vec_C)**2-xz**2-yz**2)
        positions = atoms[i].get_positions()
        positions = np.dot(positions, np.array([[lx, xy, xz], [0.0, ly, yz], [0.0, 0.0, lz]]))
        positions /= volume
        positions = np.dot(positions, np.array([np.cross(vec_B, vec_C), np.cross(vec_C, vec_A), np.cross(vec_A, vec_B)]))
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
        f_output.write('ITEM: BOX BOUNDS xy xz yz ')
        pbc = atoms[i].get_pbc()
        if pbc[0] == True:
            f_output.write('pp ')
        else:
            f_output.write('xx ')
        if pbc[1] == True:
            f_output.write('pp ')
        else:
            f_output.write('yy ')
        if pbc[2] == True:
            f_output.write('pp\n')
        else:
            f_output.write('zz\n')
        f_output.write('0.0 %f %f\n' % (lx, xy))
        f_output.write('0.0 %f %f\n' % (ly, xz))
        f_output.write('0.0 %f %f\n' % (lz, yz))
        f_output.write('ITEM: ATOMS id type x y z\n')
        for j in range(len(positions)):
            f_output.write('%d %d %f %f %f\n' %(j+1, atom_types[j], positions[j][0], positions[j][1], positions[j][2]))
    f_output.close()


def outcar2extxyz(f_outcar, f_extxyz, ele):
    '''
    功能
    ----------
    将outcar文件转为extxyz文件

    参数
    ----------
    f_outcar: outcar文件名
    f_extxyz: extxyz文件名
    ele: 元素列表(需按顺序排列)

    返回值
    ----------
    无
    '''
    calculator.all_properties.append('energy')
    calculator.all_properties.append('forces')
    type_num = list()
    with open(f_outcar, 'r') as filename:
        while True:
            line = filename.readline()
            if not line:
                break
            search = re.search(r'ions per type =', line)
            if search:
                pattern = re.compile(r'\d+')
                result = pattern.findall(line)
                for i in result:
                    type_num.append(int(i))
                break
    system_size = np.sum(type_num)
    atoms = list()
    with open(f_outcar, 'r') as filename:
        while True:
            line = filename.readline()
            if not line:
                break
            search = re.search(r'VOLUME and BASIS-vectors are now', line)
            if search:
                cell = np.zeros((3, 3))
                postitions = np.zeros((system_size, 3))
                forces = np.zeros((system_size, 3))
                energy = 0.0
                while True:
                    line = filename.readline()
                    search = re.search(r'direct lattice vectors', line)
                    if search:
                        for i in range(3):
                            line = filename.readline()
                            search = re.search(r'(\S+)\s+(\S+)\s+(\S+)\s+', line)
                            for j in range(3):
                                cell[i][j] = float(search.group(j+1))
                        # print(cell)
                        break
                while True:
                    line = filename.readline()
                    search = re.search(r'POSITION\s+TOTAL-FORCE', line)
                    if search:
                        line = filename.readline()
                        for i in range(system_size):
                            line = filename.readline()
                            search = re.search(r'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', line)
                            for j in range(3):
                                postitions[i][j] = float(search.group(j+1))
                                forces[i][j] = float(search.group(j+4))
                        # print(postitions)
                        # print(forces)
                        break
                while True:
                    line = filename.readline()
                    search = re.search(r'sigma->0\S\s+=\s+(\S+)', line)
                    if search:
                        energy = float(search.group(1))
                        # print(energy)
                        break
                sysbols = ''
                for i in range(len(type_num)):
                    sysbols += ele[i]
                    sysbols += '%d' % type_num[i]
                # print(sysbols)
                atoms_append = Atoms(symbols=sysbols, positions=postitions, cell=cell, pbc=True)
                calc = SPC(atoms=atoms_append, energy=energy, forces=forces)
                atoms_append.set_calculator(calc)
                atoms += [atoms_append]
    io.write(f_extxyz, atoms, format='extxyz')


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
