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

import random
import csv
import os
import re


def random_index(rate):
    start = 0
    index = 0
    randnum = random.randint(1, sum(rate))
    for index, scope in enumerate(rate):
        start += scope
        if randnum <= start:
            break
    return index

# theta: value of exponent
# N: domain size
# l: average length of string
# gamma: repeat rate


def text_generator(theta, N, l, gamma, pointnum):
    dictionary = []
    for i in range(N):
        str = ''
        flag = 0
        for j in range(l):
            if flag == 0:
                flag = 1
                str += chr(random.randint(65, 90))
                continue
            isrepeat = random_index([100 * gamma, 100 * (1 - gamma)])
            if isrepeat == 0:
                str += str[j-1]
            else:
                s = chr(random.randint(65, 90))
                while s == str[j-1]:
                    s = chr(random.randint(65, 90))
                str += s
        dictionary.append(str)

    num = [0 for x in range(N)]
    base = 0
    for i in range(N):
        base += pow(1/(1+i), theta)
    for i in range(N):
        num[i] = round((pow(1/(i+1), theta)/base) * pointnum)

    data = []
    for i in range(N):
        for j in range(num[i]):
            data.append(dictionary[i])
    random.shuffle(data)
    return data


os.chdir(os.path.dirname(os.path.abspath(__file__)))
p_path = "../Datasets/Synthetic/Text"  # to be changed
seed_num = 5


def my_mkdir(folder_path: str):
    if not os.path.exists(os.path.dirname(folder_path)):
        my_mkdir(os.path.dirname(folder_path))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


for i in range(11):
    for j in range(seed_num):
        my_mkdir(p_path+"/Exponent/{}".format(i))
        random.seed(j)
        exp = i+2
        data = text_generator(exp, 750, 100, 0.5, 5000)
        writer = csv.writer(open(p_path+"/Exponent/{}/{}.csv".format(i, j),
                            'w', encoding='utf-8', newline=''), escapechar='\\')
        writer.writerow(['Sensor', 's_0'])
        for k in range(len(data)):
            writer.writerow([k, data[k]])
    print("Exponent: {}".format(i))

for i in range(11):
    for j in range(seed_num):
        my_mkdir(p_path+"/Class/{}".format(i))
        random.seed(j)
        Class = i*150
        if Class == 0:
            Class = 1
        data = text_generator(0, Class, 100, 0.5, 5000)
        print(len(data))
        writer = open(p_path+"/Class/{}/{}.csv".format(i, j),
                      'w', encoding='utf-8', newline='')
        writer.write('Sensor,s_0\n')
        for k in range(len(data)):
            writer.write("{},{}\n".format(k, data[k]))
    print("Class: {}".format(i))

for i in range(11):
    for j in range(seed_num):
        my_mkdir(p_path+"/Length/{}".format(i))
        random.seed(j)
        Len = (i+1)*10
        data = text_generator(0, 2, Len, 0.5, 5000)
        writer = csv.writer(open(p_path+"/Length/{}/{}.csv".format(i, j),
                            'w', encoding='utf-8', newline=''), escapechar='\\')
        writer.writerow(['Sensor', 's_0'])
        for k in range(len(data)):
            writer.writerow([k, data[k]])
    print("Len: {}".format(i))

for i in range(11):
    for j in range(seed_num):
        my_mkdir(p_path+"/Repeat/{}".format(i))
        random.seed(j)
        data = text_generator(0, 2, 100, (i/10)*(0.1)+0.9, 5000)
        writer = csv.writer(open(p_path+"/Repeat/{}/{}.csv".format(i, j),
                            'w', encoding='utf-8', newline=''), escapechar='\\')
        writer.writerow(['Sensor', 's_0'])
        for k in range(len(data)):
            writer.writerow([k, data[k]])
    print("Repeat: {}".format(i))
