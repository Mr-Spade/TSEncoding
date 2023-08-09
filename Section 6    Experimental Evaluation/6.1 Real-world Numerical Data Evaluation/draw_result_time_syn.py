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
import os
import csv
from itertools import islice
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

fin = open("result_ingestion_syn.csv", "r", encoding="UTF-8")
fout1 = open("result_int_syn.csv", "w", encoding="UTF-8", newline="")
fout2 = open("result_long_syn.csv", "w", encoding="UTF-8", newline="")
fout3 = open("result_float_syn.csv", "w", encoding="UTF-8", newline="")
fout4 = open("result_double_syn.csv", "w", encoding="UTF-8", newline="")

reader = csv.reader(fin)


fout1.write("DataSet,Compression,Encoding,Insert Time,Select Time\n")
fout2.write("DataSet,Compression,Encoding,Insert Time,Select Time\n")
fout3.write("DataSet,Compression,Encoding,Insert Time,Select Time\n")
fout4.write("DataSet,Compression,Encoding,Insert Time,Select Time\n")

for ln in islice(reader, 1, None):
    if ln[1] == "INT32":
        fout1.write("{},{},{},{},{}\n".format(ln[0], ln[2], ln[3], ln[4], ln[5]))
    if ln[1] == "INT64":
        fout2.write("{},{},{},{},{}\n".format(ln[0], ln[2], ln[3], ln[4], ln[5]))
    if ln[1] == "FLOAT":
        fout3.write("{},{},{},{},{}\n".format(ln[0], ln[2], ln[3], ln[4], ln[5]))
    if ln[1] == "DOUBLE":
        fout4.write("{},{},{},{},{}\n".format(ln[0], ln[2], ln[3], ln[4], ln[5]))
fout1.close()
fout2.close()
fout3.close()
fout4.close()


plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

# python result_time_vis.py
# sns.set_theme(style="ticks", palette="pastel")
sns.set(style="ticks", palette="pastel", rc={"lines.markersize": 25})
plt.tick_params(labelsize=30)
# 画插入时间的图
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
# palette=["#1178b4", "#33a02c","#e31a1c", "#ff7f00","#6a3d9a","#fb9a99", "#814a19"]
fig, ax_arr = plt.subplots(2, 2, figsize=(20, 20))

fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.25)

df = pd.read_csv("result_int_syn.csv")
f = sns.lineplot(
    x="Compression",
    y="Insert Time",
    hue="Encoding",
    palette=palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[0][0],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
f.set_ylabel("Average Time (s)")
f.set(yscale="log")
# f.set(ylim=(-0.005,0.05))

f.get_legend().remove()
f.set_title("(a) INT32").set_fontsize(30)
f.tick_params(labelsize=30)
f.set_xticklabels(compressions)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

df = pd.read_csv("result_long_syn.csv")
f = sns.lineplot(
    x="Compression",
    y="Insert Time",
    hue="Encoding",
    palette=palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[0][1],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
f.set_ylabel("Average Time (s)")
f.set(yscale="log")
# f.set(ylim=(-0.01,0.1))

f.get_legend().remove()
f.set_title("(b) INT64").set_fontsize(30)
f.tick_params(labelsize=30)
f.set_xticklabels(compressions)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

df = pd.read_csv("result_float_syn.csv")
f = sns.lineplot(
    x="Compression",
    y="Insert Time",
    hue="Encoding",
    palette=palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[1][0],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
f.set_ylabel("Average Time (s)")
f.set(yscale="log")
# f.set(ylim=(-0.005,0.05))

f.get_legend().remove()
f.set_title("(c) FLOAT").set_fontsize(30)
f.tick_params(labelsize=30)
f.set_xticklabels(compressions)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

df = pd.read_csv("result_double_syn.csv")
f = sns.lineplot(
    x="Compression",
    y="Insert Time",
    hue="Encoding",
    palette=palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[1][1],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
f.set_ylabel("Average Time (s)")
f.set(yscale="log")
# f.set(ylim=(-0.01,0.1))

f.get_legend().remove()
f.set_title("(d) DOUBLE").set_fontsize(30)
f.tick_params(labelsize=30)
f.set_xticklabels(compressions)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)
lines, labels = ax_arr[0][1].get_legend_handles_labels()
fig.legend(lines, labels, loc="upper center", fontsize=30, ncol=5)

# plt.show()
fig.savefig("insert_time_syn.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("insert_time_syn.png", dpi=400, bbox_inches="tight")


# 画查询时间的图


fig, ax_arr = plt.subplots(2, 2, figsize=(20, 20))
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.25)

df = pd.read_csv("result_int_syn.csv")
f = sns.lineplot(
    x="Compression",
    y="Select Time",
    hue="Encoding",
    palette=palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[0][0],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
f.set_ylabel("Decoding Time + Uncompression Time (s)")

f.get_legend().remove()
f.set_title("(a) INT32").set_fontsize(30)
f.tick_params(labelsize=30)
f.set_xticklabels(compressions)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

df = pd.read_csv("result_long_syn.csv")
f = sns.lineplot(
    x="Compression",
    y="Select Time",
    hue="Encoding",
    palette=palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[0][1],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
f.set_ylabel("Decoding Time + Uncompression Time (s)")

f.get_legend().remove()
f.set_title("(b) INT64").set_fontsize(30)
f.tick_params(labelsize=30)
f.set_xticklabels(compressions)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

df = pd.read_csv("result_float_syn.csv")
f = sns.lineplot(
    x="Compression",
    y="Select Time",
    hue="Encoding",
    palette=palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[1][0],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
f.set_ylabel("Decoding Time + Uncompression Time (s)")

f.get_legend().remove()
f.set_title("(c) FLOAT").set_fontsize(30)
f.tick_params(labelsize=30)
f.set_xticklabels(compressions)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

df = pd.read_csv("result_double_syn.csv")
f = sns.lineplot(
    x="Compression",
    y="Select Time",
    hue="Encoding",
    palette=palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[1][1],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
f.set_ylabel("Decoding Time + Uncompression Time (s)")

f.get_legend().remove()
f.set_title("(d) DOUBLE").set_fontsize(30)
f.tick_params(labelsize=30)
f.set_xticklabels(compressions)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)

lines, labels = ax_arr[0][1].get_legend_handles_labels()
fig.legend(lines, labels, loc="upper center", fontsize=30, ncol=5)

# plt.show()
fig.savefig("select_time_syn.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("select_time_syn.png", dpi=400, bbox_inches="tight")
