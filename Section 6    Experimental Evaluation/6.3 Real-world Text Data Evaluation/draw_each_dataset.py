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

def database_name(s: str) -> str:
    if s == "Incident Event Log":
        return "IE-Log"
    elif s == "Web Log":
        return "Web-Log"
    elif s == "Web Server Access Logs":
        return "WSA-Log"
    else:
        return s
    
os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42

# python result_ratio_vis.py
sns.set_theme(style="ticks", palette="pastel")
my_palette = [
    "#1178b4",
    "#33a02c",
    "#e31a1c",
    "#ff7f00",
    "#6a3d9a",
    "#fb9a99",
    "#814a19",
]
my_palette1 = ["#1178b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a"]
hatches = ["//", "..", "xx", "||", "\\\\", "oo", "///", "...", "xxx", "|||", "\\\\\\"]
Datasets = ["CW-AIOps", "IE-Log", "Web-Log", "WSA-Log"]
Encoders = ["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"]
Features = ["Exponent", "Types", "Repeat", "Pattern Repeat", "Length"]

plt.tick_params(labelsize=15)
df = pd.read_csv("ratio_each_dataset.csv")
df["Dataset"] = df["Dataset"].apply(database_name)
fig, ax_arr = plt.subplots(1, 2, figsize=(11, 4))
# fig.subplots_adjust(top=0.82)
# fig.subplots_adjust(hspace=0.2)
# fig.subplots_adjust(wspace=0.2)
# my_palette = sns.color_palette("Set2",n_colors=7)
f = sns.barplot(
    x="Dataset",
    y="Compression Ratio",
    order=Datasets,
    hue="Encoding Algorithm",
    hue_order=Encoders,
    palette=my_palette,
    data=df,
    ax=ax_arr[1],
)
for i, bar in enumerate(f.patches):
    hatch = hatches[i // len(Datasets)]
    bar.set_hatch(hatch)
f.set_xticklabels(labels=Datasets, rotation=0)
f.get_legend().remove()
f.tick_params(labelsize=15)
f.xaxis.label.set_size(15)
f.yaxis.label.set_size(15)
f.set_ylim(0, 2.5)
f.set_title("(b) Compression ratio").set_fontsize(15)
lines, labels = ax_arr[1].get_legend_handles_labels()
f.legend(
    lines, labels, loc="upper center", bbox_to_anchor=(0.5, 1.55), fontsize=15, ncol=2
)

# fig.savefig("vary_dataset.eps", format="eps", dpi=400, bbox_inches="tight")
# fig.savefig("vary_dataset.png", dpi=400, bbox_inches="tight")

plt.close()

df = pd.read_csv("feature_each_dataset.csv")
df["Dataset"] = df["Dataset"].apply(database_name)
# my_palette = sns.color_palette("Set2",n_colors=8)
# fig.subplots_adjust(hspace=0.2)
# fig.subplots_adjust(wspace=0.2)
# fig, ax_arr = plt.subplots(1, 1, figsize=(10, 3))
# fig.subplots_adjust(top=0.82)
f = sns.barplot(
    x="Dataset",
    y="value",
    hue="feature",
    order=Datasets,
    palette=my_palette1,
    hue_order=Features,
    data=df,
    ax=ax_arr[0],
)
for i, bar in enumerate(f.patches):
    hatch = hatches[i // len(Datasets)]
    bar.set_hatch(hatch)
f.get_legend().remove()
f.set(yscale="log")
f.set_xticklabels(labels=Datasets, rotation=0)
# sns.despine(offset=20, trim=True)
f.tick_params(labelsize=15)
# f.xaxis.ticks.set_size(20)
# f.get_legend().remove()
f.xaxis.label.set_size(15)
f.yaxis.label.set_size(15)
f.set_title("(a) Features Values").set_fontsize(15)
lines, labels = ax_arr[0].get_legend_handles_labels()
f.legend(
    lines, labels, loc="upper center", bbox_to_anchor=(0.5, 1.45), fontsize=15, ncol=2
)

# fig.savefig("vary_dataset_features.eps", format="eps", dpi=400, bbox_inches="tight")
# fig.savefig("vary_dataset_features.png", dpi=400, bbox_inches="tight")
fig.savefig("vary_dataset_new.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("vary_dataset_new.png", dpi=400, bbox_inches="tight")