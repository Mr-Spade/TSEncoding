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
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatter
import seaborn as sns


models=["TSEC", "CodecDB", "C-Store", "LEA"]
hatches = ["//", "..", "xx", "||", "\\\\", "oo", "///", "...", "xxx", "|||", "\\\\\\"]

plt.style.use("ggplot")
os.chdir(os.path.dirname(os.path.abspath(__file__)))
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="ticks", palette="pastel")
my_palette = ["#1178b4", "#33a02c", "#e31a1c", "#ff7f00"]

fig = plt.figure(figsize=(18, 5))
ax_arr = fig.add_axes([0.05, 0, 0.22, 0.8])
# fig, ax_arr= plt.subplots(1,3, figsize=(30, 10), sharex=True)
# fig.subplots_adjust(wspace=0.37)
fmri = pd.read_csv("compare.csv")
data1 = pd.concat(
    [
        fmri[fmri["Indicator"] == "Precision"],
        fmri[fmri["Indicator"] == "Recall"],
        fmri[fmri["Indicator"] == "F1-score"],
    ]
)
f = sns.barplot(
    x="Indicator",
    y="Value",
    hue="Recommender",
    hue_order=["TSEC", "CodecDB", "C-Store", "LEA"],
    palette=my_palette,
    data=fmri[fmri["Indicator"] == "F1-score"],
    ax=ax_arr,
)
for i, bar in enumerate(f.patches):
    hatch = hatches[i%len(models)]
    bar.set_hatch(hatch)
f.get_legend().remove()
f.tick_params(axis="x", labelsize=0)
f.tick_params(axis="y", labelsize=30)
f.xaxis.label.set_size(30)
f.yaxis.label.set_size(30)
f_title = f.set_title("(a) F1-score")
f_title.set_fontsize(30)
f.set_ylabel("F1-score")
f.set_xlabel("")
# f.set_ylim(0,1.00)

# lines, labels = ax_arr.get_legend_handles_labels()
# fig.legend(lines, labels, loc = 'upper center', bbox_to_anchor=(0.5,1.05),fontsize=30,ncol=3)
# fig.savefig("compare_ratio_acc.eps",format='eps',dpi = 400,bbox_inches='tight')
# fig.savefig("compare_ratio_acc.png", dpi = 400,bbox_inches='tight')

# fig, ax_arr= plt.subplots(1,2, figsize=(20, 10), sharex=True)

# fmri = pd.read_csv("compare_both.csv")
ax_arr = fig.add_axes([0.42, 0, 0.22, 0.8])
f = sns.barplot(
    x="Indicator",
    y="Value",
    hue="Recommender",
    hue_order=["TSEC", "CodecDB", "C-Store", "LEA"],
    palette=my_palette,
    data=fmri[fmri["Indicator"] == "Average Ratio"],
    ax=ax_arr,
)
for i, bar in enumerate(f.patches):
    hatch = hatches[i%len(models)]
    bar.set_hatch(hatch)
f.get_legend().remove()
f.set(yscale='log')
f.tick_params(axis="x", labelsize=0)
f.yaxis.set_major_formatter(LogFormatter())
f.yaxis.set_tick_params(which='both',labelsize=30)
f.tick_params(axis="y", labelsize=30)
f.xaxis.label.set_size(0)
f.yaxis.label.set_size(30)
# f.set_xticks("")
# f.xaxis.set_label("Compression Ratio")
f_title = f.set_title("(b) Compression Ratio")
f_title.set_fontsize(30)
f.set_ylabel("Compression Ratio")
# f.set_xlabel("")
# f.set_ylim(0.1, 0.125)
# f.set_ylim(0.1,0.13)

ax_arr = fig.add_axes([0.73, 0, 0.22, 0.8])
f = sns.barplot(
    x="Indicator",
    y="Value",
    hue="Recommender",
    hue_order=["TSEC", "CodecDB", "C-Store", "LEA"],
    palette=my_palette,
    data=fmri[fmri["Indicator"] == "Time Cost"],
    ax=ax_arr,
)
for i, bar in enumerate(f.patches):
    hatch = hatches[i%len(models)]
    bar.set_hatch(hatch)
f.get_legend().remove()
f.tick_params(axis="x", labelsize=0)
f.tick_params(axis="y", labelsize=30)
f.xaxis.label.set_size(0)
f.yaxis.label.set_size(30)
f_title = f.set_title("(c) Training Time Cost")
f_title.set_fontsize(30)
f.set_ylabel("Training Time Cost (s)")
# f.set_xlabel("")
# f.set_ylim(0,15)


lines, labels = ax_arr.get_legend_handles_labels()
fig.legend(
    lines, labels, loc="upper center", bbox_to_anchor=(0.5, 1.1), fontsize=30, ncol=4
)
fig.savefig("compare_ratio.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("compare_ratio.png", dpi=400, bbox_inches="tight")
