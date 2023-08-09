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
import csv
import random
import numpy as np

random.seed(10)


def my_random(mean, std):
    # x = (int)(random.random()*2)
    # if x == 0:
    return np.random.normal(mean, std)
    # elif x == 1:
    #     return np.random.laplace(mean, std/np.sqrt(2))


'''
random_index(rate)
function:
    get '1' or '0' according to certain rate randomly
parameter: 
    rate = [r,100-r]
return: 
    0, possibility r/100
    1, possibility (100-r)/100
'''


def random_index(rate):
    start = 0
    index = 0
    randnum = random.randint(1, sum(rate))
    for index, scope in enumerate(rate):
        start += scope
        if randnum <= start:
            break
    return index


'''
cal_average(data)
function:
    calculate the average value of data
parameter:
    data(list of values)
return:
    the average value of data
'''


def cal_average(data):
    count = 0
    add = 0
    for i in data:
        count += 1
        add += i
    return add/count


'''
generator(mean, delta_mean, delta_variance, repeat, increase, length)
function: 
    generate data with given parameters
parameter:
    mean: value mean of data
    delta_mean: the mean of delta while generating delta
    delta_std: the std of delta while generating delta
    repeat: the possibility of generating '0' as delta value
    increase: the possibility of generating positive delta value once delta value is not '0'
    length: the length of data
return:
    data (list of values)
'''


def generator(mean, delta_mean, delta_std, repeat, increase, length):
    diff = []
    while len(diff) < length:
        isrepeat = random_index([100*repeat, 100*(1-repeat)])
        if isrepeat == 0:
            repeat_len = random.randint(8, 10)
            for j in range(repeat_len):
                diff.append(0)
            continue
        else:
            ispositive = random_index([100*increase, 100*(1-increase)])
            if ispositive == 0:
                delta = 0
                cnt = 0
                while delta <= 0:
                    cnt += 1
                    if cnt == 100:
                        delta = 0
                        break
                    else:
                        delta = float(my_random(delta_mean, delta_std))
            else:
                delta = 0
                cnt = 0
                while delta >= 0:
                    cnt += 1
                    if cnt == 100:
                        delta = 0
                        break
                    else:
                        delta = float(my_random(delta_mean, delta_std))
            diff.append(delta)
    data = [diff[0]]
    for i in range(1, length):
        data.append(diff[i]+data[i-1])
    cur_mean = cal_average(data)
    for i in range(length):
        data[i] += mean - cur_mean
    return data


def my_mkdir(folder_path: str):
    if not os.path.exists(os.path.dirname(folder_path)):
        my_mkdir(os.path.dirname(folder_path))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


os.chdir(os.path.dirname(os.path.abspath(__file__)))
RESULT_PATH = "../Datasets/Synthetic/Numerical"


def my_generate(data, folder_name, file_name):
    for datatype in ["DOUBLE", "FLOAT"]:
        my_mkdir(RESULT_PATH+"/{}/{}/".format(datatype, folder_name))
        writer = csv.writer(open(RESULT_PATH+"/{}/{}/".format(datatype,
                            folder_name)+file_name, 'w', encoding='UTF-8', newline=""))
        writer.writerow(['Sensor', 's_0'])
        for j in range(10000):
            writer.writerow([j, data[j]])
    for datatype in ["INT32", "INT64"]:
        my_mkdir(RESULT_PATH+"/{}/{}/".format(datatype, folder_name))
        writer = csv.writer(open(RESULT_PATH+"/{}/{}/".format(datatype,
                            folder_name)+file_name, 'w', encoding='UTF-8', newline=""))
        writer.writerow(['Sensor', 's_0'])
        for j in range(10000):
            writer.writerow([j, int(data[j])])


for i in range(11):  # vary value mean
    mean = -50000 + i*10000
    data = generator(mean, 0, 50, 0, 0.5, 10000)
    my_generate(data, "Value_mean", "mean_%d.csv" % i)
    print("Value_mean", i)

for i in range(11):  # vary delta mean
    delta_mean = -2000 + i*400
    data = generator(0, delta_mean, 50, 0, 0.5, 10000)
    my_generate(data, "Delta_mean", "diffmean_%d.csv" % i)
    print("Delta_mean", i)

for i in range(11):  # vary value std
    diffstd = 100*i+0.000001
    data = generator(0, 0, diffstd, 0, 0.5, 10000)
    my_generate(data, "Delta_std", "diffstd_%d.csv" % i)
    print("Delta_std", i)

for i in range(11):  # vary repeat
    data = generator(0, 0, 50, i/10, 0.5, 10000)
    my_generate(data, "Repeat", "repeat_%d.csv" % i)
    print("Repeat", i)

for i in range(11):  # vary increase
    data = generator(0, 0, 50, 0, i/10, 10000)
    my_generate(data, "Increase", "increase_%d.csv" % i)
    print("Increase", i)
