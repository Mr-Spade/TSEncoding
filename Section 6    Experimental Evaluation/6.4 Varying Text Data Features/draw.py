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

plt.style.use("ggplot")


os.chdir(os.path.dirname(os.path.abspath(__file__)))

font_size = 38
exp_size = 25

matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
# sns.set_theme(style="ticks", palette="pastel")
sns.set(style="ticks", palette="pastel", rc={"lines.markersize": 17})

markers = ["o", "v", "^", "<", ">", "s", "p"]

# ----------------------------EXPONENT--------------------------------------------------

fig, ax_arr = plt.subplots(1, 2, figsize=(22, 9))

my_palette = [
    "#1178b4",
    "#33a02c",
    "#e31a1c",
    "#ff7f00",
    "#6a3d9a",
    "#fb9a99",
    "#814a19",
]
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.355)

fmri = pd.read_csv("exponent_text_ratio_result.csv")
f = sns.lineplot(
    x="Exponent",
    y="Compression Ratio",
    hue="Encoding",
    hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[0],
    size="Encoding",
    sizes=[5, 5, 5, 5, 5, 5, 5],
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set_ylabel("Compression Ratio")
f_title = f.set_title("(a) Compression Ratio")
f_title.set_fontsize(font_size)

fmri = pd.read_csv("exponent_text_time_result.csv")
f = sns.lineplot(
    x="Exponent",
    y="Insert Time",
    hue="Encoding",
    hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[1],
    size="Encoding",
    sizes=[5, 5, 5, 5, 5, 5, 5],
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set(yscale="log")
f.set_ylabel("Average Time (s)")
f_title = f.set_title("(b) Encoding Time")
f_title.set_fontsize(font_size)
# f.set_ylim(0,1)


# f = sns.lineplot(
#     x="Exponent",
#     y="Select Time",
#     hue="Encoding",
#     hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
#     markers=markers,
#     err_style=None,
#     style="Encoding",
#     dashes=False,
#     palette=my_palette,
#     data=fmri,
#     ax=ax_arr[2],
#     size="Encoding",
#     sizes=[5, 5, 5, 5, 5, 5, 5],
# )
# f.get_legend().remove()
# f.tick_params(labelsize=font_size)
# f.xaxis.label.set_size(font_size)
# f.yaxis.label.set_size(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-1, 1))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f_title = f.set_title("(c) Exponent")
# f.set_ylabel("Select Time (s)")
# f_title.set_fontsize(font_size)
# f.set_ylim(0,4)

lines, labels = ax_arr[0].get_legend_handles_labels()
fig.legend(
    lines,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.2),
    fontsize=font_size,
    ncol=4,
)

fig.savefig("text_features_exponent.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("text_features_exponent.png", dpi=400, bbox_inches="tight")
# plt.show()

# # -------------------------------Types------------------------------------------------

fig, ax_arr = plt.subplots(1, 2, figsize=(22, 9))
my_palette = [
    "#1178b4",
    "#33a02c",
    "#e31a1c",
    "#ff7f00",
    "#6a3d9a",
    "#fb9a99",
    "#814a19",
]
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.355)
fmri = pd.read_csv("types_text_ratio_result.csv")
f = sns.lineplot(
    x="Types",
    y="Compression Ratio",
    hue="Encoding",
    hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[0],
    size="Encoding",
    sizes=[5, 5, 5, 5, 5, 5, 5],
)
# sns.despine(offset=10, trim=True)
f.get_legend().remove()
# f.legend(loc = 'best',fontsize=7)
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set_title("(a) Compression Ratio").set_fontsize(font_size)
f.set_ylabel("Compression Ratio")
f.set_xlabel("Domain")
fmri = pd.read_csv("types_text_time_result.csv")
f = sns.lineplot(
    x="Types",
    y="Insert Time",
    hue="Encoding",
    hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[1],
    size="Encoding",
    sizes=[5, 5, 5, 5, 5, 5, 5],
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set_title("(b) Encoding Time").set_fontsize(font_size)
f.set(yscale="log")
f.set_ylabel("Average Time (s)")
f.set_xlabel("Domain")
# f.set_ylim(0,1)
# f = sns.lineplot(
#     x="Types",
#     y="Select Time",
#     hue="Encoding",
#     hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
#     markers=markers,
#     err_style=None,
#     style="Encoding",
#     dashes=False,
#     palette=my_palette,
#     data=fmri,
#     ax=ax_arr[2],
#     size="Encoding",
#     sizes=[5, 5, 5, 5, 5, 5, 5],
# )
# f.get_legend().remove()
# f.tick_params(labelsize=font_size)
# f.xaxis.label.set_size(font_size)
# f.yaxis.label.set_size(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-1, 1))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylabel("Select Time (s)")
# f.set_title("(c) Domain").set_fontsize(font_size)
# f.set_xlabel("Domain")
# f.set_ylim(0,4)
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
fig.savefig("text_features_domain.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("text_features_domain.png", dpi=400, bbox_inches="tight")

# # -----------------------------Length------------------------------

fig, ax_arr = plt.subplots(1, 2, figsize=(22, 9))
my_palette = [
    "#1178b4",
    "#33a02c",
    "#e31a1c",
    "#ff7f00",
    "#6a3d9a",
    "#fb9a99",
    "#814a19",
]
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.355)
fmri = pd.read_csv("length_text_ratio_result.csv")
f = sns.lineplot(
    x="Length",
    y="Compression Ratio",
    hue="Encoding",
    hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[0],
    size="Encoding",
    sizes=[5, 5, 5, 5, 5, 5, 5],
)
# sns.despine(offset=10, trim=True)
f.get_legend().remove()
# f.legend(loc = 'best',fontsize=7)
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set_ylabel("Compression Ratio")
f_title = f.set_title("(a) Compression Ratio")
f_title.set_fontsize(font_size)
# # f.set_ylim(0,1)
fmri = pd.read_csv("length_text_time_result.csv")
f = sns.lineplot(
    x="Length",
    y="Insert Time",
    hue="Encoding",
    hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[1],
    size="Encoding",
    sizes=[5, 5, 5, 5, 5, 5, 5],
)
f.get_legend().remove()
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set(yscale="log")
f.set_ylabel("Average Time (s)")
f_title = f.set_title("(b) Encoding Time Time")
f_title.set_fontsize(font_size)
# f.set_ylim(0,1)
# f = sns.lineplot(
#     x="Length",
#     y="Select Time",
#     hue="Encoding",
#     hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
#     markers=markers,
#     err_style=None,
#     style="Encoding",
#     dashes=False,
#     palette=my_palette,
#     data=fmri,
#     ax=ax_arr[2],
#     size="Encoding",
#     sizes=[5, 5, 5, 5, 5, 5, 5],
# )
# f.get_legend().remove()
# f.tick_params(labelsize=font_size)
# f.xaxis.label.set_size(font_size)
# f.yaxis.label.set_size(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-1, 1))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# f.set_ylabel("Select Time (s)")
# f_title = f.set_title("(c) Length")
# f_title.set_fontsize(font_size)
# f.set_ylim(0,4)
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
fig.savefig("text_features_length.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("text_features_length.png", dpi=400, bbox_inches="tight")


# # ----------------------------REPEAT----------------------------------

fig, ax_arr = plt.subplots(1, 2, figsize=(22, 9))
my_palette = [
    "#1178b4",
    "#33a02c",
    "#e31a1c",
    "#ff7f00",
    "#6a3d9a",
    "#fb9a99",
    "#814a19",
]
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.355)
fmri = pd.read_csv("repeat_text_ratio_result.csv")
f = sns.lineplot(
    x="Repeat",
    y="Compression Ratio",
    hue="Encoding",
    hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[0],
    size="Encoding",
    sizes=[5, 5, 5, 5, 5, 5, 5],
)
# sns.despine(offset=10, trim=True)
f.get_legend().remove()
# f.legend(loc = 'best',fontsize=7)
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set_ylabel("Compression Ratio")
f.set_title("(a) Compression Ratio").set_fontsize(font_size)
# f.set_ylim(0,0.16)
fmri = pd.read_csv("repeat_text_time_result.csv")
f = sns.lineplot(
    x="Repeat",
    y="Insert Time",
    hue="Encoding",
    hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
    markers=markers,
    err_style=None,
    style="Encoding",
    dashes=False,
    palette=my_palette,
    data=fmri,
    ax=ax_arr[1],
    size="Encoding",
    sizes=[5, 5, 5, 5, 5, 5, 5],
)
# sns.despine(offset=10, trim=True)
f.get_legend().remove()
# f.legend(loc = 'best',fontsize=7)
f.tick_params(labelsize=font_size)
f.xaxis.label.set_size(font_size)
f.yaxis.label.set_size(font_size)
f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
f.set(yscale="log")
f.set_ylabel("Average Time (s)")
f.set_title("(b) Encoding Time").set_fontsize(font_size)
# f.set_ylim(0,1)
# f = sns.lineplot(
#     x="Repeat",
#     y="Select Time",
#     hue="Encoding",
#     hue_order=["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"],
#     markers=markers,
#     err_style=None,
#     style="Encoding",
#     dashes=False,
#     palette=my_palette,
#     data=fmri,
#     ax=ax_arr[2],
#     size="Encoding",
#     sizes=[5, 5, 5, 5, 5, 5, 5],
# )
# # sns.despine(offset=10, trim=True)
# f.get_legend().remove()
# # f.legend(loc = 'best',fontsize=7)
# f.tick_params(labelsize=font_size)
# f.xaxis.label.set_size(font_size)
# f.yaxis.label.set_size(font_size)
# f.axes.ticklabel_format(style="sci", axis="y", scilimits=(-1, 1))
# f.axes.yaxis.get_offset_text().set_fontsize(exp_size)
# # f.set_ylabel("Select Time/s")
# f.set_ylabel("Select Time (s)")
# f.set_title("(c) Repeat").set_fontsize(font_size)
# f.set_ylim(0,4)
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
fig.savefig("text_features_repeat.eps", format="eps", dpi=400, bbox_inches="tight")
fig.savefig("text_features_repeat.png", dpi=400, bbox_inches="tight")
