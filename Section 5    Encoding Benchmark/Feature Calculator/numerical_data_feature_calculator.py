# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import time
from pathlib import Path
import os
import re
import math

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss
import pycatch22


os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATHs = [
    ["../Datasets/Real-world/Numerical", "../../Real_Numerical_feature.csv"],
    ["../Datasets/Synthetic/Numerical", "../../Synthetic_Numerical_feature.csv"]
]


def drop_nan(x):
    return 0 if math.isnan(x) else x


def entropy(data):
    prob = []
    length = len(data)
    for i in np.unique(data):
        prob.append(np.sum(data == i)/float(length))
    return ss.entropy(prob)


def repeat_words(data, limit=8):
    lenth = len(data)
    index = 0
    key = data[0]
    count = 0
    for val in data:
        if val == key:
            count += 1
        else:
            if count >= limit:
                index += count
            key = val
            count = 0
    return float(index)/lenth


def nc_repeat(data, limit=128):
    length = len(data)
    index = 0
    dic = {}
    for i in range(length):
        if data[i] in dic.keys():
            index += 1
            dic[data[i]] += 1
        else:
            dic[data[i]] = 1
        if i >= limit:
            dic[data[i-limit]] -= 1
    return float(index)/length


'''
def sortedness(data):
    if len(data) <= 1:
        return data,0
    index = len(data) // 2
    lst1 = data[:index]
    lst2 = data[index:]
    left,n1 = sortedness(lst1)
    right,n2 = sortedness(lst2)
    sorted,num = merge(left,right)
    return sorted,n1+n2+num
'''


def sortedness(data):
    length = len(data)
    count = 0
    for i in range(length-1):
        if data[i] <= data[i+1]:
            count += 1
    return count/(length-1)


def merge(lst1, lst2):
    """to Merge two list together"""
    list = []
    num = 0
    while len(lst1) > 0 and len(lst2) > 0:
        data1 = lst1[0]
        data2 = lst2[0]
        if data1 <= data2:
            list.append(lst1.pop(0))
        else:
            num += len(lst1)
            list.append(lst2.pop(0))
    if len(lst1) > 0:
        list.extend(lst1)
    else:
        list.extend(lst2)
    return list, num


def statistic(data):
    ave = np.nanmean(data, axis=0)

    std = np.nanstd(data, axis=0)
    Min = np.nanmin(data, axis=0)
    Max = np.nanmax(data, axis=0)
    std_spread = Max-Min
    diff_data = np.diff(data, axis=0)
    diff_ave = np.nanmean(diff_data, axis=0)
    diff_min = np.nanmin(diff_data, axis=0)
    diff_max = np.nanmax(diff_data, axis=0)
    diff_spread = diff_max-diff_min
    diff_std = np.nanstd(diff_data, axis=0)
    repeat = repeat_words(data)
    nrepeat = nc_repeat(data)
    sort = sortedness(data.tolist())
    return "{},{},{},{},{},{},{},{},{},{},{}".format(
        ave, std, std_spread, drop_nan(
            pycatch22.SB_BinaryStats_mean_longstretch1(data.tolist())),
        diff_ave, diff_std, diff_spread, drop_nan(
            pycatch22.MD_hrv_classic_pnn40(data.tolist())),
        repeat, nrepeat,
        sort
    )


for [DATA_PATH, RESULT_PATH] in PATHs:
    logger = open(RESULT_PATH, "w")
    logger.write("DataFile,Datatype,Data Mean,Data Std,Data Spread,SB_BinaryStats,Delta Mean,Delta Std,Delta Spread,MD_hrv,Repeat,Non-C Repeat,Increase\n")

    datatypes = os.listdir(DATA_PATH)
    for datatype in datatypes:
        datasets = os.listdir(DATA_PATH+'/'+datatype)
        for dataset in datasets:
            files = os.listdir(DATA_PATH+'/'+datatype+'/'+dataset)
            for file in files:
                df = pd.read_csv(DATA_PATH+'/'+datatype+'/'+dataset+'/'+file)
                data = df['s_0']
                logger.write('{},{},{}\n'.format(re.findall(r".*/(.*?/.*?/.*?)$", DATA_PATH)[0]+'/'+datatype +
                                                 '/'+dataset+'/'+file, datatype, statistic(data)))
