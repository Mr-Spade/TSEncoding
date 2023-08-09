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
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

Datatypes = ["INT32", "INT64", "FLOAT", "DOUBLE"]
Encoders = ["TS_2DIFF", "GORILLA", "CHIMP", "RAKE", "RLE", "RLBE", "SPRINTZ", "BUFF"]
Features = [
    "Data Mean",
    "Data Std",
    "Data Spread",
    "SB_BinaryStats",
    "Delta Mean",
    "Delta Std",
    "Delta Spread",
    "MD_hrv",
    "Repeat",
    "Non-C Repeat",
    "Increase",
]


def trans_feature_name(s: str):
    if s == "Data Mean":
        return "Value Mean"
    elif s == "Data Std":
        return "Value Std"
    elif s == "Data Spread":
        return "Value Spread"
    else:
        return s


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
m = len(Datatypes) + len(Features)
matrix = [[0] * m for i in range(n)]

data = pd.read_csv("correlation.csv")
data = data[Datatypes + Features + Encoders]

features = [data[datatype] for datatype in Datatypes] + [
    data[feature] for feature in Features
]
encodings = [data[encoder] for encoder in Encoders]

for i in range(n):
    for j in range(m):
        matrix[i][j] = encodings[i].corr(features[j])
sns.set()
label_x = Datatypes + [trans_feature_name(s) for s in Features]
label_y = Encoders
heatmap = sns.heatmap(
    matrix,
    xticklabels=label_x,
    yticklabels=label_y,
    cmap="vlag_r",
    vmin=-0.5,
    vmax=0.5,
    ax=ax_arr,
)

heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=90)
heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0)
plt.setp(label_x)
# print(matrix)
lines, labels = ax_arr.get_legend_handles_labels()
# fig.legend(lines)
# plt.show()
fig.savefig("features-encoding.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("features-encoding.png", dpi=400, bbox_inches="tight")

sns.lineplot
