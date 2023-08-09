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

import os
import re
import numpy as np
import pandas as pd
from numpy import log
from collections import Counter

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATHs = [
    ["../Datasets/Real-world/Text", "../../Real_Text_feature.csv"],
    ["../Datasets/Synthetic/Text", "../../Synthetic_Text_feature.csv"],
]


# def count_next_elements(lsts):
#     result = {}
#     for lst in lsts:
#         for i in range(len(lst) - 1):
#             current_num = lst[i]
#             next_num = lst[i + 1]
#             if current_num not in result:
#                 result[current_num] = Counter([next_num])
#             else:
#                 result[current_num].update([next_num])
#     return {key: counts.most_common(1)[0][0] for key, counts in result.items()}

k = 3
P = 0.01
p_result = {}
p_tot = 1


def p_clear():
    global p_result, p_tot
    p_result = {}
    p_tot = 1


def p_update(s: str):
    global p_result, p_tot
    for i in range(len(s) - k + 1):
        h = hash(s[i : i + k])
        p_tot += 1
        if h in p_result.keys():
            p_result[h] += 1
        else:
            p_result[h] = 1


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
    p_clear()
    # lns = []
    for ln in data:
        ln = "".join(ln)
        p_update(ln)
    # pattern = count_next_elements(lns)
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
            if i != 0 and ln[i] == ln[i - 1]:
                repeat += 1
        for i in range(len(ln) - k + 1):
            h = hash(ln[i : i + k])
            if h in p_result.keys() and p_result[h] / p_tot > P:
                p_repeat += 1
            # if i != 0 and ln[i] == pattern[ln[i-1]]:
            #     p_repeat += 1
            # print(repeat)
    dic_time.append(1)
    dic_time.sort(reverse=True)
    theta = log(dic_time[0] / dic_time[1]) / log(2).real
    return "{},{},{},{},{}".format(
        theta, N, repeat / tot, p_repeat / p_tot, tot / len(data)
    )


def dfs(path: str, log_path: str, logger):
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            dfs(path + "/" + file, log_path + "/" + file, logger)
    else:
        try:
            data = pd.read_csv(
                path,
                encoding="utf-8",
                dtype={"Sensor": np.int64, "s_0": str},
                error_bad_lines=False,
                engine="python",
            ).dropna()
        except Exception as e:
            print("Error")
            return
        data = data["s_0"]
        logger.write("{},{}\n".format(log_path, cal_feature(data)))


for [DATA_PATH, RESULT_PATH] in PATHs:
    logger = open(RESULT_PATH, "w")
    logger.write("DataFile,Exponent,Types,Repeat,Pattern Repeat,Length\n")
    dfs(DATA_PATH, re.findall(r".*/(.*?/.*?/.*?)$", DATA_PATH)[0], logger)
