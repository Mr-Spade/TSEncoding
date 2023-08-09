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

from turtle import color
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams['lines.markersize'] = 17


palette = [
    "#1178b4",
    "#33a02c",
    "#e31a1c",
    "#ff7f00",
    "#6a3d9a",
    "#fb9a99",
    "#814a19",
    "#a6cee3",
    "#b2df8a",
]
Types = ["DOUBLE", "TIMESTAMP"]
markers = ["o", "v", "^", "<", ">", "s", "p", "*", "8"]

for type in Types:
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(221, polar=True)
    fmri = pd.read_csv("gzip_avg_{}.csv".format(type))
    feature = ["ET", "DT", "CT", "UT", "CR", "ET"]
    angles = np.linspace(0, 2 * np.pi, 5, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    num_encoding = 9
    for i in range(0, num_encoding):
        values = np.array(fmri.iloc[i, 1 : num_encoding - 1]).tolist()
        values = np.concatenate([values, [values[0]]])

        ax.plot(angles, values, marker=markers[i], linewidth=4, label=fmri.iloc[i, 0], color=palette[i])
        ax.fill(angles, values, alpha=0)

    ax.set_thetagrids(angles * 180 / np.pi, feature)
    ax.set_ylim(-0.2, 1)
    ax.tick_params(labelsize=30)
    ax.xaxis.label.set_size(30)
    ax.yaxis.label.set_size(30)
    ax.set_title("(a) GZIP").set_fontsize(30)
    plt.legend(loc="best")
    ax.get_legend().remove()
    ax.set_facecolor("w")
    # set grid color
    ax.grid(color="silver")
    ax.set_xticklabels(feature, color="black")
    ax.grid(True)


    fmri = pd.read_csv("lz4_avg_{}.csv".format(type))
    ax = fig.add_subplot(222, polar=True)

    angles = np.linspace(0, 2 * np.pi, 5, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    for i in range(0, num_encoding):
        values = np.array(fmri.iloc[i, 1 : num_encoding - 1]).tolist()
        values = np.concatenate([values, [values[0]]])

        ax.plot(angles, values, marker=markers[i], linewidth=4, label=fmri.iloc[i, 0], color=palette[i])
        ax.fill(angles, values, alpha=0)

    ax.set_thetagrids(angles * 180 / np.pi, feature)
    ax.set_ylim(-0.2, 1)
    ax.tick_params(labelsize=30)
    ax.xaxis.label.set_size(30)
    ax.yaxis.label.set_size(30)
    ax.set_title("(b) LZ4").set_fontsize(30)
    plt.legend(loc="best")
    ax.get_legend().remove()
    ax.set_facecolor("w")
    # set grid color
    ax.grid(color="silver")
    ax.set_xticklabels(feature, color="black")
    ax.grid(True)


    fmri = pd.read_csv("snappy_avg_{}.csv".format(type))
    ax = fig.add_subplot(223, polar=True)

    angles = np.linspace(0, 2 * np.pi, 5, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    for i in range(0, num_encoding):
        values = np.array(fmri.iloc[i, 1 : num_encoding - 1]).tolist()
        values = np.concatenate([values, [values[0]]])

        ax.plot(angles, values, marker=markers[i], linewidth=4, label=fmri.iloc[i, 0], color=palette[i])
        ax.fill(angles, values, alpha=0)

    ax.set_thetagrids(angles * 180 / np.pi, feature)
    ax.set_ylim(-0.2, 1)
    ax.tick_params(labelsize=30)
    ax.xaxis.label.set_size(30)
    ax.yaxis.label.set_size(30)
    ax.set_title("(c) SNAPPY").set_fontsize(30)
    plt.legend(loc="best")
    ax.get_legend().remove()

    ax.set_facecolor("w")
    # set grid color
    ax.grid(color="silver")
    ax.set_xticklabels(feature, color="black")
    ax.grid(True)

    fmri = pd.read_csv("uncompressed_avg_{}.csv".format(type))
    fmri["Compress Time"] = float("nan")
    fmri["Uncompress Time"] = float("nan")
    ax = fig.add_subplot(224, polar=True)

    angles = np.linspace(0, 2 * np.pi, 5, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    for i in range(0, num_encoding):
        values = np.array(fmri.iloc[i, 1 : num_encoding - 1]).tolist()
        values = np.concatenate([values, [values[0]]])

        ax.plot(angles, values, marker=markers[i], linewidth=4, label=fmri.iloc[i, 0], color=palette[i])
        ax.fill(angles, values, alpha=0)

    ax.set_thetagrids(angles * 180 / np.pi, feature)
    ax.set_ylim(-0.2, 1)
    ax.tick_params(labelsize=30)
    ax.xaxis.label.set_size(30)
    ax.yaxis.label.set_size(30)
    ax.set_title("(d) NONE").set_fontsize(30)
    plt.legend(loc="best")
    ax.get_legend().remove()

    ax.set_facecolor("w")
    # set grid color
    ax.grid(color="silver")
    ax.set_xticklabels(feature, color="black")
    ax.grid(True)

    lines, labels = ax.get_legend_handles_labels()
    fig.legend(lines, labels, loc="upper center", fontsize=30, ncol=5)

    fig.savefig("radar_{}.eps".format(type), format="eps", dpi=400, bbox_inches="tight")
    fig.savefig("radar_{}.png".format(type), dpi=400, bbox_inches="tight")
    # radar of trade-off between time cost and compression ratio
