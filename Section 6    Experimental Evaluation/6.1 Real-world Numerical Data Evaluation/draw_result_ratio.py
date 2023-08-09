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

from cProfile import label
import csv
from itertools import islice
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

# python result_ratio_vis.py
# sns.set_theme(style="ticks", palette="pastel")
sns.set(style="ticks", palette="pastel", rc={"lines.markersize": 25})

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
# hatches = ["//", "..", "xx", "||", "\\\\", "oo", "///", "...", "xxx", "|||", "\\\\\\"]
encodings = [
    "TS_2DIFF",
    "GORILLA",
    "CHIMP",
    "RAKE",
    "RLE",
    "RLBE",
    "SPRINTZ",
    "BUFF",
    "PLAIN",
]
compressions = ["NONE", "SNAPPY", "LZ4", "GZIP"]
markers = ["o", "v", "^", "<", ">", "s", "p", "*", "8"]
# palette=["#a6cee3", "#b2df8a","#fb9a99", "#fdbf6f","#cab2d6", "#1f78b4","#33a02c"],
# drow the fig of compression ratio
# plt.tick_params(labelsize=30)
df = pd.read_csv("result_compression_ratio.csv")
fig, ax_arr = plt.subplots(2, 2, figsize=(20, 20))


fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.2)

f = sns.lineplot(
    x="Compression",
    y="Compression Ratio",
    hue="Encoding",
    palette=palette,
    data=df[df["DataType"] == "INT32"],
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    # order=compressions,
    ax=ax_arr[0][0],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
# f.set(ylim=(-0.1,1.5))
# sns.despine(offset=30, trim=True)
f.set_xticklabels(compressions)
f.tick_params(labelsize=30)
f_title = f.set_title("(a) INT32")
f_title.set_fontsize(30)
# f.xaxis.ticks.set_size(30)

f.get_legend().remove()
# f.legend(fontsize=30)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

f = sns.lineplot(
    x="Compression",
    y="Compression Ratio",
    hue="Encoding",
    palette=palette,
    data=df[df["DataType"] == "INT64"],
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    # order=compressions,
    ax=ax_arr[0][1],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
# f.set(ylim=(-0.1,1.5))
# sns.despine(offset=30, trim=True)

f.set_title("(b) INT64").set_fontsize(30)
f.get_legend().remove()
# f.legend(fontsize=7)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)
f.set_xticklabels(compressions)
f.tick_params(labelsize=30)
# labels = ax_arr[0][1].get_xticklabels() + ax_arr[0][1].get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]


f = sns.lineplot(
    x="Compression",
    y="Compression Ratio",
    hue="Encoding",
    palette=palette,
    data=df[df["DataType"] == "FLOAT"],
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    # order=compressions,
    ax=ax_arr[1][0],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
# f.set(ylim=(-0.1,1.5))
# sns.despine(offset=30, trim=True)


f_title = f.set_title("(c) FLOAT")
f_title.set_fontsize(30)
f.get_legend().remove()
f.set_xticklabels(compressions)
f.tick_params(labelsize=30)
# f.legend(fontsize=7)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

f = sns.lineplot(
    x="Compression",
    y="Compression Ratio",
    hue="Encoding",
    palette=palette,
    data=df[df["DataType"] == "DOUBLE"],
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    # order=compressions,
    ax=ax_arr[1][1],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
# f.set(ylim=(-0.1,1.5))
# sns.despine(offset=30, trim=True)

f.set_title("(d) DOUBLE").set_fontsize(30)

f.get_legend().remove()
f.set_xticklabels(compressions)
f.tick_params(labelsize=30)
# f.legend(fontsize=7)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

lines, labels = ax_arr[0][1].get_legend_handles_labels()
fig.legend(lines, labels, loc="upper center", fontsize=30, ncol=5)


# plt.tick_params(labelsize=30)
# labels = ax_arr[1][1].get_xticklabels() + ax_arr[1][1].get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]

# plt.subplots_adjust(bottom=0.30)
# plt.subplots_adjust(left=0.30)
# plt.show()
fig.savefig("compression_ratio.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("compression_ratio.png", dpi=400, bbox_inches="tight")
