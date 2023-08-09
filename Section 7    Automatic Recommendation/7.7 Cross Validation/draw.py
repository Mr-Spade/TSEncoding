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
import pandas as pd
import matplotlib
import os


def dataset_convert(s: str) -> str:
    if s == "Chemistry":
        return "WH-Chemistry"
    elif s == "Climate":
        return "THU-Climate"
    elif s == "Cloud":
        return "CW-AIOps"
    elif s == "Engine":
        return "CBMI-Engine"
    elif s == "MSRC-12":
        return "MSRC-12"
    elif s == "Ship":
        return "CSSC-Ship"
    elif s == "Train":
        return "CRRC-Train"
    elif s == "UCI-Gas":
        return "UCI-Gas"
    elif s == "Vehicle1":
        return "TY-Carriage"
    elif s == "Vehicle2":
        return "WC-Vehicle"
    elif s == "dianwang":
        return "DW-Electricity"
    elif s == "liantong":
        return "LT-Mobile"
    elif s == "yinlian":
        return "YL-Economy"
    elif s == "zhongxin":
        return "ZX-Call"
    else:
        raise


os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

# python result_ratio_vis.py
sns.set_theme(style="ticks", palette="pastel")
my_palette = ["#1178b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a", "#fb9a99"]
hatches = ["//", "..", "xx", "||", "\\\\", "oo", "///", "...", "xxx", "|||", "\\\\\\"]
Datasets = [
    "MSRC-12",
    "UCI-Gas",
    "WC-Vehicle",
    "THU-Climate",
    "CW-AIOps",
    "CSSC-Ship",
    "TY-Carriage",
    "WH-Chemistry",
    "CRRC-Train",
    "CBMI-Engine",
    "DW-Electricity",
    "LT-Mobile",
    "YL-Economy",
    "ZX-Call",
]
Encoders = [
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
Models = ["LR", "SVM", "DT", "RF", "GDBT", "MLP"]

plt.tick_params(labelsize=15)
df = pd.read_csv("cross_result.csv")
df["Dataset"] = df["Dataset"].apply(dataset_convert)
fig, ax_arr = plt.subplots(1, 1, figsize=(10, 3.6))
# fig.subplots_adjust(top=0.82)
# fig.subplots_adjust(hspace=0.2)
# fig.subplots_adjust(wspace=0.2)
# my_palette = sns.color_palette("Set2",n_colors=7)
f = sns.barplot(
    x="Dataset",
    y="F1",
    order=Datasets,
    hue="Model",
    hue_order=Models,
    palette=my_palette,
    data=df,
    ax=ax_arr,
)
for i, bar in enumerate(f.patches):
    hatch = hatches[i // len(Datasets)]
    bar.set_hatch(hatch)
f.set_xticklabels(labels=Datasets, rotation=45)
f.get_legend().remove()
f.tick_params(labelsize=15)
f.xaxis.label.set_size(15)
f.yaxis.label.set_size(15)
f.set_ylabel("F1-score")
# f.set_title("(a) Compression ratio").set_fontsize(20)
lines, labels = ax_arr.get_legend_handles_labels()
fig.legend(
    lines, labels, loc="upper center", bbox_to_anchor=(0.5, 1.1), fontsize=15, ncol=6
)

fig.savefig("vary_precison.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("vary_precison.png", dpi=400, bbox_inches="tight")

plt.close()

# my_palette = sns.color_palette("Set2",n_colors=8)
# fig.subplots_adjust(hspace=0.2)
# fig.subplots_adjust(wspace=0.2)
fig, ax_arr = plt.subplots(1, 1, figsize=(10, 3.6))
# fig.subplots_adjust(top=0.82)
f = sns.barplot(
    x="Dataset",
    y="Time Cost",
    hue="Model",
    order=Datasets,
    palette=my_palette,
    hue_order=Models,
    data=df,
    ax=ax_arr,
)
for i, bar in enumerate(f.patches):
    hatch = hatches[i // len(Datasets)]
    bar.set_hatch(hatch)
f.get_legend().remove()
f.set_xticklabels(labels=Datasets, rotation=45)
# sns.despine(offset=20, trim=True)
f.tick_params(labelsize=15)
# f.xaxis.ticks.set_size(20)
# f.get_legend().remove()
f.xaxis.label.set_size(15)
f.yaxis.label.set_size(15)
f.set_ylabel("Time Cost (s)")
# f.set_title("(b) Features Values").set_fontsize(20)
lines, labels = ax_arr.get_legend_handles_labels()
fig.legend(
    lines, labels, loc="upper center", bbox_to_anchor=(0.5, 1.1), fontsize=15, ncol=6
)

fig.savefig("vary_time.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("vary_time.png", dpi=400, bbox_inches="tight")
