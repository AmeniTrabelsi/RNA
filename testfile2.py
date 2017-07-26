#!/usr/bin/python
# -*- coding: utf-8 -*-

# import pickle
#
# favorite_color = {"lion": "yellow", "kitty": "red"}
#
# pickle.dump(favorite_color, open("save.p", "wb"))
# favorite_color2 = pickle.load( open( "save.p", "rb" ) )
# print favorite_color2


import pymzml
import copy

filename = "input_data/test1.mzML"
result = pymzml.run.Reader(filename, extraAccessions=[('MS:1000827', ['value'])])
data_all = []
msmsSpectra = {'sn': [], 'rt': [], 'parent_mz': [], 'parent_sn': [], 'parent_rt': [], 'Spectra': []}
for idx, spec in enumerate(result):
    if 'scan start time' in spec:
        temp_rt = spec['scan start time']
        temp_mslevel = int(spec['ms level'])
        temp_scan = int(spec.xmlTreeIterFree.attrib['id'].split(' ')[-1].split('=')[-1])
        temp_spec = []
        for mz, i in spec.peaks:
            temp_spec.append([mz, i])
        data_all.append([temp_mslevel, temp_scan, temp_rt, temp_spec])
        if temp_mslevel == 2:
            msmsSpectra['sn'].append(temp_scan)
            msmsSpectra['rt'].append(temp_rt)
            msmsSpectra['parent_mz'].append(spec['isolation window target m/z'])
            msmsSpectra['parent_sn'].append(count1)
            msmsSpectra['parent_rt'].append(data_all[count1-1][2])
            msmsSpectra['Spectra'].append(temp_spec)
        else:
            count1 = copy.copy(temp_scan)

Total_int = []
RT_all = []
for c in data_all:
    RT_all.append(c[2])
    Total_int.append(sum(i[-1] for i in c[3]))

print('finished')
