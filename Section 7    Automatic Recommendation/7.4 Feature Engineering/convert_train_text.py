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

PATHS = [
    [
        "../../Real_Text_feature.csv",
        "../../Real_Text_result.csv",
        "train_Real_text.csv",
    ],
    [
        "../../Synthetic_Text_feature.csv",
        "../../Synthetic_Text_result.csv",
        "train_Synthetic_text.csv",
    ],
]
OUTPUT_PATH = "train_text.csv"

# Datatypes = ["INT32", "INT64", "FLOAT", "DOUBLE"]
Features = ["Exponent", "Types", "Repeat", "Pattern Repeat", "Length"]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

results = []


# def to_index(datatype):
#     return Datatypes.index(datatype) + 1


for [FEATURE_PATH, RESULT_PATH, OUT_PATH] in PATHS:
    df = pd.read_csv(FEATURE_PATH)
    # df = df[df["Datatype"].isin(Datatypes)]
    rf = pd.read_csv(RESULT_PATH)
    # rf = rf[rf["Data Type"].isin(Datatypes)]
    rf = rf.rename(columns={"Input Direction": "DataFile"})
    rf = rf[rf["Compress Algorithm"] == "UNCOMPRESSED"]
    rf_min = rf.groupby("DataFile")["Compression Ratio"].idxmin()
    rf = rf.loc[rf_min, ["DataFile", "Encoding Algorithm", "Compression Ratio"]]
    df = df.merge(rf, how="left", on="DataFile")
    # df["Datatype"] = df["Datatype"].apply(to_index)
    df = df[Features + ["Encoding Algorithm", "Compression Ratio"]]
    df.to_csv(OUT_PATH, index=False)
    results.append(df)

pd.concat(results).to_csv(OUTPUT_PATH, index=False)
