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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["lines.markersize"] = 17

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Models = ["LR", "SVM", "DT", "RF", "GDBT", "MLP"]
markers = ["o", "v", "^", "<", ">", "s", "p", "*", "8"]
my_palette = ["#1178b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a", "#fb9a99"]

INPUT_PATH = "./train_result_text.csv"

df = pd.read_csv(INPUT_PATH)

fig, axes = plt.subplots(1, 2, figsize=(6, 3))
for i in range(len(Models)):
    model = Models[i]
    ef = df[df["Model"] == model].sort_values(by="k")
    axes[0].plot(
        ef["k"].tolist(),
        ef["F1"].tolist(),
        marker=markers[i],
        color=my_palette[i],
        label=model,
        markersize=3,
    )

axes[0].set_title("(a) F1-score")
axes[0].set_xlabel("Top-k features")
axes[0].set_ylabel("F1-score")
# plt.legend()
# plt.tight_layout()
# plt.savefig("feature_engineering.eps")
# plt.savefig("feature_engineering.png")
# plt.clf()

for i in range(len(Models)):
    model = Models[i]
    ef = df[df["Model"] == model].sort_values(by="k")
    axes[1].plot(
        ef["k"].tolist(),
        ef["Time Cost"].tolist(),
        marker=markers[i],
        color=my_palette[i],
        label=model,
        markersize=3,
    )

axes[1].set_title("(b) Time cost")
axes[1].set_xlabel("Top-k features")
axes[1].set_ylabel("Time cost (s)")
lines, labels = axes[1].get_legend_handles_labels()
# plt.legend()
# plt.tight_layout()
# plt.savefig("feature_engineering_time.eps")
# plt.savefig("feature_engineering_time.png")
# plt.clf()
fig.tight_layout()
fig.legend(lines, labels, bbox_to_anchor=(0.5, 1.07), loc="upper center", ncol=6)
fig.savefig("feature_engineering_new_text.eps", bbox_inches="tight")
fig.savefig("feature_engineering_new_text.png", bbox_inches="tight")
# plt.clf()
