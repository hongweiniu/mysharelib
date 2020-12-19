'''
笔记
----------
一些常用的计算
'''
from ovito.io import import_file
from ovito.modifiers import CoordinationAnalysisModifier
import numpy as np


def cal_rdf(filename, end, num_of_confs, every, cutoff, num_of_bins):
    '''
    功能
    ----------
    计算rdf

    参数
    ----------
    filename: 输入结构文件名
    end: 最后一帧
    num_of_confs：合计结构数
    every：每隔#帧取一次结构
    cutoff：截断半径
    num_of_bins：bin个数

    返回值
    ----------
    共3列。第一列是半径r，第二列是rdf，第三列是cutoff内合计原子数。
    '''
    delta = cutoff/num_of_bins
    pipeline = import_file(filename)
    modifier = CoordinationAnalysisModifier(cutoff=cutoff, number_of_bins=num_of_bins)
    pipeline.modifiers.append(modifier)
    r = np.linspace(delta/2, cutoff-delta/2, num=num_of_bins)
    total_rdf = np.zeros(modifier.number_of_bins)
    coord_num = np.zeros(modifier.number_of_bins)
    if end < 0:
        end += pipeline.source.num_frames+1
    for frame in range(end-(num_of_confs-1)*every, end+1, every):
        data = pipeline.compute(frame)
        current_rdf = data.series['coordination-rdf'].xy()
        gr = current_rdf[:, 1]
        total_rdf += gr
        rho = data.particles.count / data.cell.volume
        coord_num_core = gr*4*np.pi*rho*r**2
        coord_num += np.array([np.trapz(coord_num_core[:k+1], dx=delta) for k in range(len(coord_num_core))])
    total_rdf /= num_of_confs
    coord_num /= num_of_confs
    return np.column_stack((r, total_rdf, coord_num))
