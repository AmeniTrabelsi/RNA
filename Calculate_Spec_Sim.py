#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from sklearn.neighbors import KNeighborsClassifier as KNC
from sklearn.preprocessing import normalize as normr

def Calculate_Spec_Sim(all_fragmention, target_spec, test_spec, max_true_mz):
    target_spec = np.array(target_spec)
    test_spec = np.array(test_spec)
    test_spec = np.delete(test_spec, np.where(test_spec[:, 0] > max_true_mz), 0)
    test_spec = np.delete(test_spec, np.where(test_spec[:, 1] < max(test_spec[:, 1])/1000), 0)
    all_fragmention = np.array(all_fragmention)
    idx = np.argsort(target_spec[:, 0])
    target_spec_sort = target_spec[idx, :]
    all_fragmention_sort = all_fragmention[idx, :]
    mzAll = np.concatenate((target_spec_sort[:, 0], test_spec[:, 0]), 0)
    mzSort = ClusteringByThreshold(mzAll, 0.015)
    intensityMtx = KNNClassify(mzSort, test_spec, target_spec_sort)
    p_zero = [i for i, j in enumerate(intensityMtx[-1]) if j == 0]
    intensityMtx[0], intensityMtx[-1] = np.delete(intensityMtx[0], p_zero, 0), np.delete(intensityMtx[-1], p_zero, 0)
    mzSort = np.delete(mzSort, p_zero, 0)
    Annotate_ID = []
    fragment_mz = all_fragmention_sort[:, -1].astype(np.float)
    count_nonemptyID = 0
    for mz1 in mzSort:
        diff_mz = abs(fragment_mz - mz1)
        p1 = np.where(diff_mz <= 0.015)[0]
        if len(p1) > 0:
            count_nonemptyID += 1
            if len(p1) > 1:
                p2 = np.where(diff_mz[p1] == min(diff_mz[p1]))[0]
                Annotate_ID.append(str(round(mz1, 2)) + '_' + '_'.join(all_fragmention_sort[p1[p2], 4]) + '_' + '_'.join(all_fragmention_sort[p1[p2], 5])) ##mz+fragmention class+ adduct ion
            else:
                Annotate_ID.append(str(round(mz1, 2)) + '_' + all_fragmention_sort[p1, 4][0] + '_' + all_fragmention_sort[p1, 5][0])
        else:
            Annotate_ID.append('')
    SimScore = GetSimScore(intensityMtx, mzSort)
    return SimScore, Annotate_ID, mzSort, intensityMtx, count_nonemptyID


def ClusteringByThreshold(mzAll, theta):
    # clusters = []
    mzSort = []
    idx = np.argsort(mzAll)
    mz_temp = mzAll[idx]
    i = 0
    while i < len(mz_temp):
        mzz = mz_temp[i]
        px = np.where(abs(mz_temp[i:] - mzz) <= theta)[0]
        mzSort.append(np.array(np.mean(mz_temp[px+i])))
        # clusters.append([mz_temp[id1+i] for id1 in px])
        # print(i)
        i = px[-1] + i + 1

    return mzSort

def KNNClassify(mzSort, test_spec, target_spec):
    intensityMtx = []
    groupID = [i for i in range(len(mzSort))]
    spec = [target_spec, test_spec]
    for temp_spec in spec:
        tempR = np.array([0]*len(mzSort))
        neigh = KNC(n_neighbors=1)
        neigh.fit(np.array(mzSort).reshape((-1, 1)), groupID)
        predict_labels = neigh.predict(temp_spec[:, 0].reshape((-1, 1)))
        tempR[predict_labels] = temp_spec[:, 1]
        intensityMtx.append(tempR)
    return intensityMtx

def GetSimScore(intensityMtx, all_mz, n=0.53, m=1.3):

    expdata = intensityMtx[0]
    libdata = intensityMtx[-1]

    # a = expdata.shape[0]
    newExpdata = expdata ** n * all_mz ** m
    newLibdata = libdata ** n * all_mz ** m
    SimScore = np.dot(normr(newExpdata.reshape((-1, 1))), normr(newLibdata.reshape((-1, 1))).T)[0, 0]

    return SimScore