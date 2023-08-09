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

import csv
import os
import pandas
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pickle

# Datatypes = ["INT32", "INT64", "FLOAT", "DOUBLE"]
Encoders = ["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"]
Features = ["Exponent", "Types", "Repeat", "Pattern Repeat", "Length"]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.style.use("ggplot")
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="ticks", palette="vlag")

fig, ax_arr = plt.subplots(1, 1, figsize=(5, 3))
my_palette = sns.color_palette("Set1", n_colors=7)
fig.subplots_adjust(hspace=0.22)
fig.subplots_adjust(wspace=0.20)
n = len(Encoders)
m = len(Features)
matrix = [[0] * m for i in range(n)]

data = pd.read_csv("correlation_text.csv")
data = data[ Features + Encoders]

features = [
    data[feature] for feature in Features
]
encodings = [data[encoder] for encoder in Encoders]

matrix_sum = [0] * m

for i in range(n):
    for j in range(m):
        matrix[i][j] = encodings[i].corr(features[j])
        if not np.isnan(matrix[i][j]):
            matrix_sum[j] += matrix[i][j] ** 2

arg = np.argsort(matrix_sum)[::-1]
MyFeatures = np.asarray(Features)[arg]

with open("features_text.pkl", "wb") as f:
    pickle.dump(MyFeatures.tolist(), f)
