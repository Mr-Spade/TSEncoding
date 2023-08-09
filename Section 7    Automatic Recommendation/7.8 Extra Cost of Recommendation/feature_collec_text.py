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

# encoding:utf-8
from math import log
import time
from pathlib import Path
import os
import re

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
import scipy.stats as ss

from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.utils.Tablet import Tablet
from collections import Counter

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def entropy(data):
    prob = []
    length = len(data)
    for i in np.unique(data):
        prob.append(np.sum(data == i)/float(length))
    return ss.entropy(prob)

def repeat_words(data,limit=8):
    lenth = len(data)
    index = 0
    key = data[0]
    count = 0
    for val in data:
        if val == key:
            count+=1
        else:
            if count >= limit:
                index += count
            key=val
            count=0
    return float(index)/lenth

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
        if data[i]<=data[i+1]:
            count += 1
    return count/(length-1)


# def merge(lst1, lst2):
#     """to Merge two list together"""
#     list = []
#     num = 0
#     while len(lst1) > 0 and len(lst2) > 0:
#         data1 = lst1[0]
#         data2 = lst2[0]
#         if data1 <= data2:
#             list.append(lst1.pop(0))
#         else:
#             num += len(lst1)
#             list.append(lst2.pop(0))
#     if len(lst1) > 0:
#         list.extend(lst1)
#     else:
#         list.extend(lst2)
#     return list,num

def count_next_elements(lsts):
    result = {}
    for lst in lsts:
        for i in range(len(lst) - 1):
            current_num = lst[i]
            next_num = lst[i + 1]
            if current_num not in result:
                result[current_num] = Counter([next_num])
            else:
                result[current_num].update([next_num])
    return {key: counts.most_common(1)[0][0] for key, counts in result.items()}

def cal_feature(data):
    N = 0
    repeat = 0
    p_repeat = 0
    length = 0
    tot = 0
    dic = []
    dic_time = []
    dic_time_fst = 0
    dic_time_sec = 0
    lns=[]
    for ln in data:
        ln = "".join(ln)
        lns.append(ln)
    pattern = count_next_elements(lns)
    for ln in data:
        ln = "".join(ln)
        flag = 0
        for j in range(len(dic)):
            if dic[j] == ln:
                flag = 1
                dic_time[j] += 1
        if flag == 0:
            N += 1
            dic.append(ln)
            dic_time.append(1)
            j = len(dic) - 1
        tot += len(ln)
        for i in range(len(ln)):
            if i!=0 and ln[i] == ln[i-1]:
                repeat += 1
            if i!=0 and ln[i] == pattern[ln[i-1]]:
                p_repeat += 1
                #print(repeat)
    dic_time.append(1)
    dic_time.sort(reverse=True)
    theta = log(dic_time[0]/dic_time[1]) / log(2).real
    return "{},{},{},{},{}".format(theta, N, repeat/tot, p_repeat/tot, tot/len(data))

def main():
    print("Start.")

    ip = "127.0.0.1"
    port_ = "6667"
    username_ = 'root'
    password_ = 'root'

    RESULT1_PATH = "time_real_world_insert_extraction_text.csv"  ###
    logger = open(RESULT1_PATH, "w")
    # logger.write("Dataset,Size,Data Extraction Time,Insert Time\n")
    logger.write("Dataset,Size,Time type,Time Cost\n")

    dataset = "Datasets/Real-world/Text" ###
    fileList = os.listdir(dataset)
    count = 0

    for dataFile in fileList:
        count += 1
        print(count)
        path = dataset + '/' + dataFile
        data = pd.read_csv(str(path),encoding='utf-8',dtype = {'Sensor':np.int64,'s_0':str},error_bad_lines=False, engine="python")
        data.dropna(inplace=True)
        device = "root.test.t1"
        time_list = [x for x in data["Sensor"]]
        value_list = [[x] for x in data["s_0"]]
        
        Sata = data["s_0"].to_numpy()
        orginal_data_size = len(time_list)*8
        for values in value_list:
            for value in values:
                orginal_data_size += len(value)
        print(orginal_data_size)

        for s in range(1,11):
            size = s*10000
            time_list_tmp = time_list[:size]
            value_list_tmp = value_list[:size]
            Sata = data["s_0"].to_numpy()[:size]
            print(size)

            time_start = time.time()
            for i in range(10):
                res = cal_feature(Sata)
            time_end = time.time()
            extraction_time = (time_end-time_start)/10
            print("{},{},Data Feature Collection Time,{}\n".format(dataFile,size,extraction_time))
            logger.write("{},{},Data Feature Collection Time,{}\n".format(dataFile,size,extraction_time))        


            tsdt = [TSDataType.TEXT]
            encodings = [TSEncoding.PLAIN,TSEncoding.HUFFMAN,TSEncoding.RLE,TSEncoding.DICTIONARY,TSEncoding.MTF,TSEncoding.BW,TSEncoding.AC]
            compressors = [Compressor.UNCOMPRESSED]#,Compressor.GZIP,Compressor.LZ4,Compressor.SNAPPY]
            insert_time = 100
            for compressor in compressors:
                for encoding in encodings:
                    device = "root.test.t1"
                    measurements = ["s_0"]
                    tablet = Tablet(device, measurements, tsdt,value_list_tmp, time_list_tmp)

                    session = Session(ip, port_, username_, password_)
                    session.open(False)
                    session.execute_non_query_statement(
                        "delete storage group root.*"
                    )
                    session.set_storage_group("root.test")

                    session.execute_non_query_statement(
                        "set system to RUNNING"
                    )
                    session.execute_non_query_statement(
                        "delete timeseries root.test.t1.s_0"
                    )
                    session.execute_non_query_statement(
                        "create timeseries root.test.t1.s_0 with datatype=INT32,encoding={},compressor={}".format(
                            encoding.name, compressor.name)
                    )
                    time_start = time.time()
                    session.insert_tablet(tablet)
                    time_end = time.time()
                    if insert_time > time_end-time_start :
                        insert_time = time_end-time_start
            print("{},{},Insert Time,{}\n".format(dataFile,size,insert_time))
            logger.write("{},{},Insert Time,{}\n".format(dataFile,size,insert_time))  


            # print("{},{},{},{}\n".format(dataFile,size,extraction_time,insert_time))
            # logger.write("{},{},{},{}\n".format(dataFile,size,extraction_time,insert_time))

        # 
        # per_time = 1000000 * 16 * cal_time/orginal_data_size 
        # print("{},INT32,{},{},{}\n".format(path,res,cal_time,per_time))
        # logger.write("{},INT32,{},{},{}\n".format(path,res,cal_time,per_time))

main()