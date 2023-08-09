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
import re
import numpy as np
import pandas as pd

PATHS = [
    ["../../Real_Text_feature.csv", "../../Real_Text_result.csv"],
    ["../../Synthetic_Text_feature.csv", "../../Synthetic_Text_result.csv"],
]
OUTPUT_PATH = "cross_text.csv"

# Datatypes = ["INT32", "INT64", "FLOAT", "DOUBLE"]
Features = ["Exponent", "Types", "Repeat", "Pattern Repeat", "Length"]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

results = []


def get_dataset_name(s: str) -> str:
    return re.findall(r".*/(.*?)/(?:.*?)\.csv", s)[0]


for [FEATURE_PATH, RESULT_PATH] in PATHS:
    df = pd.read_csv(FEATURE_PATH)
    rf = pd.read_csv(RESULT_PATH)
    rf = rf.rename(columns={"Input Direction": "DataFile"})
    rf = rf[rf["Compress Algorithm"] == "UNCOMPRESSED"]
    rf_min = rf.groupby("DataFile")["Compression Ratio"].idxmin()
    rf = rf.loc[rf_min, ["DataFile", "Encoding Algorithm", "Compression Ratio"]]
    df = df.merge(rf, how="left", on="DataFile")
    if "Real" in RESULT_PATH:
        df["Dataset"] = df["DataFile"].apply(get_dataset_name)
    else:
        df["Dataset"] = "Synthetic"
    df = df[["Dataset"] + Features + ["Encoding Algorithm", "Compression Ratio"]]
    results.append(df)

pd.concat(results).to_csv(OUTPUT_PATH, index=False)
