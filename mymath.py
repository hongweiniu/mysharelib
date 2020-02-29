import numpy as np


def cal_mae(a, b):
    return np.mean(np.abs(a - b))


def cal_rmse(a, b):
    return np.sqrt(np.mean(np.square(a - b)))


def cal_r2(a, b):
    return np.corrcoef([a, b])[0][1]


def cal_se(a):
    return np.std(a)/np.sqrt(len(a)-1)
