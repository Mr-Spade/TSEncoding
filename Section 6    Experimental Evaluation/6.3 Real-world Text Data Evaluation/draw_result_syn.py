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
from matplotlib.ticker import FormatStrFormatter
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib

font_size = 48
exp_size = 30

os.chdir(os.path.dirname(os.path.abspath(__file__)))
plt.rc("font", family="sans-serif")
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
# python result_ratio_vis.py
# sns.set_theme(style="ticks", palette="pastel")
sns.set(style="ticks", palette="pastel", rc={"lines.markersize": 30})
# drow the fig of compression ratio
# plt.tick_params(labelsize=30)
df = pd.read_csv("result_compression_ratio_syn.csv")
fig, ax_arr = plt.subplots(1, 2, figsize=(30, 13))
my_palette = [
    "#1178b4",
    "#33a02c",
    "#e31a1c",
    "#ff7f00",
    "#6a3d9a",
    "#fb9a99",
    "#814a19",
]
# hatches = ["//", "..", "xx", "||", "\\\\", "oo", "///", "...", "xxx", "|||", "\\\\\\"]
encodings = ["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"]
compressions = ["NONE", "SNAPPY", "LZ4", "GZIP"]
markers = ["o", "v", "^", "<", ">", "s", "p", "*", "8"]

# fig.subplots_adjust(bottom=0.1)
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.25)

f = sns.lineplot(
    x="Compression",
    y="Compression Ratio",
    hue="Encoding",
    palette=my_palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[0],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
# f.set(ylim=(-0.1, 4.2))
f.tick_params(labelsize=font_size)
f.set_xticklabels(compressions)
f_title = f.set_title("(a) Compression Ratio")
f_title.set_fontsize(font_size)

f.get_legend().remove()
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-1, 1))
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set_xticklabels(f.get_xticklabels())

df = pd.read_csv("result_ingestion_syn.csv")
f = sns.lineplot(
    x="Compression",
    y="Insert Time",
    hue="Encoding",
    palette=my_palette,
    data=df,
    hue_order=encodings,
    estimator=np.mean,
    style="Encoding",
    dashes=False,
    markers=markers,
    size="Encoding",
    sizes=[5] * len(encodings),
    errorbar=None,
    ax=ax_arr[1],
)
# for i, bar in enumerate(f.patches):
#     if i < 2 * len(encodings):
#         hatch = hatches[(i // 2) % len(encodings)]
#         bar.set_hatch(hatch)
#     else:
#         hatch = hatches[i % len(encodings)]
#         bar.set_hatch(hatch)
f.set_ylabel("Average Time (s)")
# f.set(ylim=(0, 0.12))

f.get_legend().remove()
f.set_title("(b) Encoding Time + Compression Time").set_fontsize(font_size)
f.tick_params(labelsize=font_size)
f.set_xticklabels(compressions)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-1, 1))
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set_xticklabels(f.get_xticklabels())

# df = pd.read_csv("result_long_syn.csv")
# f = sns.lineplot(
#     x="Compression",
#     y="Select Time",
#     hue="Encoding",
#     palette=my_palette,
#     data=df,
#     hue_order=encodings,
#     order=["NONE", "SNAPPY", "LZ4", "GZIP"],
#     ax=ax_arr[2],
# )
# # for i, bar in enumerate(f.patches):
# #     if i < 2 * len(encodings):
# #         hatch = hatches[(i // 2) % len(encodings)]
# #         bar.set_hatch(hatch)
# #     else:
# #         hatch = hatches[i % len(encodings)]
# #         bar.set_hatch(hatch)
# f.set_ylabel("Select Time (s)")

# f.get_legend().remove()
# f.set_title("(c) Select Time").set_fontsize(font_size)
# f.tick_params(labelsize=font_size)
# f.xaxis.label.set_size(font_size)
# f.yaxis.label.set_size(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-1, 1))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_xticklabels(f.get_xticklabels())

lines, labels = ax_arr[0].get_legend_handles_labels()
fig.legend(
    lines,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.2),
    fontsize=font_size,
    ncol=4,
)


# plt.show()
fig.savefig("text_compression_syn.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("text_compression_syn.png", dpi=400, bbox_inches="tight")
