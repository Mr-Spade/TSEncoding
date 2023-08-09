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

import matplotlib
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir(os.path.dirname(os.path.abspath(__file__)))
plt.style.use("ggplot")
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
# sns.set_theme(style="ticks", palette="pastel")
sns.set(style="ticks", palette="pastel", rc={"lines.markersize": 17})

font_size = 44
exp_size = 25

fig, ax_arr = plt.subplots(1, 2, figsize=(22, 9))

markers = ["o", "v", "^", "<", ">", "s", "p", "*", "8"]

my_palette = [
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

fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.37)

fmri = pd.read_csv("result_mean_ratio.csv")
f = sns.lineplot(
    x="Data Mean",
    y="Compression Ratio",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[0],
    size="Encoding",
    sizes=[5] * len(encodings),
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f_title = f.set_title("(a) Compression Ratio Mean")
f.set_xlabel("Value Mean")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)

fmri = pd.read_csv("result_mean_ratio.csv")
f = sns.lineplot(
    x="Data Mean",
    y="Insert Time",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[1],
    size="Encoding",
    sizes=[5] * len(encodings),
)

f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f_title = f.set_title("(b) Encoding Time")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set(yscale="log")
f.set_ylabel("Average Time (s)")
f.set_xlabel("Value Mean")
# f.set_ylim(0,0.16)


# fmri = pd.read_csv("result_mean_ratio.csv")
# f = sns.lineplot(
#     x="Data Mean",
#     y="Select Time",
#     hue="Encoding",
#     hue_order=encodings,
#     markers=markers,
#     err_style=None,
#     style="Encoding",
#     dashes=False,
#     palette=my_palette,
#     data=fmri,
#     ax=ax_arr[2],
#     size="Encoding",
#     sizes=[5] * len(encodings),
# )
# f.get_legend().remove()
# f.tick_params(labelsize=font_size)
# f.xaxis.label.set_size(font_size)
# f.yaxis.label.set_size(font_size)
# f.set_ylabel("Select Time (s)")
# f.set_xlabel("Value Mean")
# f_title = f.set_title("(c) Value Mean")
# f_title.set_fontsize(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-3, 3))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.012)

lines, labels = ax_arr[0].get_legend_handles_labels()
fig.legend(
    lines,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.3),
    fontsize=font_size,
    ncol=4,
)

fig.savefig("features_mean.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("features_mean.png", dpi=400, bbox_inches="tight")

# #-----------------------------------diffmean-------------------------------------------

fig, ax_arr = plt.subplots(1, 2, figsize=(22, 9))
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.37)
fmri = pd.read_csv("result_delta_mean_ratio.csv")
f = sns.lineplot(
    x="Delta Mean",
    y="Compression Ratio",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[0],
    size="Encoding",
    sizes=[5] * len(encodings),
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.set_xlabel("Delta Mean")
f_title = f.set_title("(a) Compression Ratio Mean")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.16)
fmri = pd.read_csv("result_delta_mean_ratio.csv")
f = sns.lineplot(
    x="Delta Mean",
    y="Insert Time",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[1],
    size="Encoding",
    sizes=[5] * len(encodings),
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
# f.set(yscale="log")
f.set_ylabel("Average Time (s)")
f.set_xlabel("Delta Mean")
f_title = f.set_title("(b) Encoding Time")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.16)
# fmri = pd.read_csv("result_delta_mean_ratio.csv")
# f = sns.lineplot(
#     x="Delta Mean",
#     y="Select Time",
#     hue="Encoding",
#     hue_order=encodings,
#     markers=markers,
#     err_style=None,
#     style="Encoding",
#     dashes=False,
#     palette=my_palette,
#     data=fmri,
#     ax=ax_arr[2],
#     size="Encoding",
#     sizes=[5] * len(encodings),
# )
# f.get_legend().remove()
# f.tick_params(labelsize=font_size)
# f.xaxis.label.set_size(font_size)
# f.yaxis.label.set_size(font_size)
# f.set_ylabel("Select Time (s)")
# f.set_xlabel("Delta Mean")
# f_title = f.set_title("(c) Delta Mean")
# f_title.set_fontsize(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-3, 3))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.012)
lines, labels = ax_arr[0].get_legend_handles_labels()
fig.legend(
    lines,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.3),
    fontsize=font_size,
    ncol=4,
)
fig.savefig("features_diffmean.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("features_diffmean.png", dpi=400, bbox_inches="tight")

# # -----------------------------------------diffstd------------------------------------

fig, ax_arr = plt.subplots(1, 2, figsize=(22, 9))
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.37)
fmri = pd.read_csv("result_delta_std_ratio.csv")
f = sns.lineplot(
    x="Delta Std",
    y="Compression Ratio",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[0],
    size="Encoding",
    sizes=[5] * len(encodings),
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.set_xlabel("Delta Std")
f_title = f.set_title("(a) Compression Ratio Std")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.16)
fmri = pd.read_csv("result_delta_std_ratio.csv")
f = sns.lineplot(
    x="Delta Std",
    y="Insert Time",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[1],
    size="Encoding",
    sizes=[5] * len(encodings),
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
# f.set(yscale="log")
f.set_ylabel("Average Time (s)")
f_title = f.set_title("(b) Encoding Time")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.16)
# fmri = pd.read_csv("result_delta_std_ratio.csv")
# f = sns.lineplot(
#     x="Delta Std",
#     y="Select Time",
#     hue="Encoding",
#     hue_order=encodings,
#     markers=markers,
#     err_style=None,
#     style="Encoding",
#     dashes=False,
#     palette=my_palette,
#     data=fmri,
#     ax=ax_arr[2],
#     size="Encoding",
#     sizes=[5] * len(encodings),
# )
# f.get_legend().remove()
# f.tick_params(labelsize=font_size)
# f.xaxis.label.set_size(font_size)
# f.yaxis.label.set_size(font_size)
# f.set_ylabel("Select Time (s)")
# f_title = f.set_title("(c) Delta Std")
# f_title.set_fontsize(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-3, 3))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.012)
lines, labels = ax_arr[0].get_legend_handles_labels()
fig.legend(
    lines,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.3),
    fontsize=font_size,
    ncol=4,
)
fig.savefig("features_diffstd.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("features_diffstd.png", dpi=400, bbox_inches="tight")

# # ------------------------------repeat------------------------------------------------


fig, ax_arr = plt.subplots(1, 2, figsize=(22, 9))
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.37)
fmri = pd.read_csv("result_repeat_ratio.csv")
f = sns.lineplot(
    x="Repeat",
    y="Compression Ratio",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[0],
    size="Encoding",
    sizes=[5] * len(encodings),
)
f.get_legend().remove()
f.xaxis.label.set_size(font_size)
f.tick_params(labelsize=font_size)
f.yaxis.label.set_size(font_size)
f_title = f.set_title("(a) Compression Ratio")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.16)
fmri = pd.read_csv("result_repeat_ratio.csv")
f = sns.lineplot(
    x="Repeat",
    y="Insert Time",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[1],
    size="Encoding",
    sizes=[5] * len(encodings),
)
f.get_legend().remove()
f.xaxis.label.set_size(font_size)
f.tick_params(labelsize=font_size)
f.yaxis.label.set_size(font_size)
# f.set(yscale="log")
f.set_ylabel("Average Time (s)")
f_title = f.set_title("(b) Encoding Time")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.16)
# fmri = pd.read_csv("result_repeat_ratio.csv")
# f = sns.lineplot(
#     x="Repeat",
#     y="Select Time",
#     hue="Encoding",
#     hue_order=encodings,
#     markers=markers,
#     err_style=None,
#     style="Encoding",
#     dashes=False,
#     palette=my_palette,
#     data=fmri,
#     ax=ax_arr[2],
#     size="Encoding",
#     sizes=[5] * len(encodings),
# )
# f.get_legend().remove()
# f.xaxis.label.set_size(font_size)
# f.tick_params(labelsize=font_size)
# f.yaxis.label.set_size(font_size)
# f.set_ylabel("Select Time (s)")
# f_title = f.set_title("(c) Repeat")
# f_title.set_fontsize(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-3, 3))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.012)
lines, labels = ax_arr[0].get_legend_handles_labels()
fig.legend(
    lines,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.3),
    fontsize=font_size,
    ncol=4,
)
fig.savefig("features_repeat.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("features_repeat.png", dpi=400, bbox_inches="tight")
#  -----------------------------------------increase-------------------------------------------
fig, ax_arr = plt.subplots(1, 2, figsize=(22, 9))
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.37)
fmri = pd.read_csv("result_delta_increase_ratio.csv")
f = sns.lineplot(
    x="Increase",
    y="Compression Ratio",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[0],
    size="Encoding",
    sizes=[5] * len(encodings),
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f_title = f.set_title("(a) Compression Ratio")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.16)
fmri = pd.read_csv("result_delta_increase_ratio.csv")
f = sns.lineplot(
    x="Increase",
    y="Insert Time",
    hue="Encoding",
    hue_order=encodings,
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[1],
    size="Encoding",
    sizes=[5] * len(encodings),
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
# f.set(yscale="log")
f.set_ylabel("Average Time (s)")
f_title = f.set_title("(b) Encoding Time")
f_title.set_fontsize(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.16)
# fmri = pd.read_csv("result_delta_increase_ratio.csv")
# f = sns.lineplot(
#     x="Increase",
#     y="Select Time",
#     hue="Encoding",
#     hue_order=encodings,
#     markers=markers,
#     err_style=None,
#     style="Encoding",
#     dashes=False,
#     palette=my_palette,
#     data=fmri,
#     ax=ax_arr[2],
#     size="Encoding",
#     sizes=[5] * len(encodings),
# )
# f.get_legend().remove()
# f.tick_params(labelsize=font_size)
# f.xaxis.label.set_size(font_size)
# f.yaxis.label.set_size(font_size)
# f.set_ylabel("Select Time (s)")
# f_title = f.set_title("(c) Increase")
# f_title.set_fontsize(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-3, 3))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylim(0,0.012)
lines, labels = ax_arr[0].get_legend_handles_labels()
fig.legend(
    lines,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.3),
    fontsize=font_size,
    ncol=4,
)
fig.savefig("features_increase.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("features_increase.png", dpi=400, bbox_inches="tight")
