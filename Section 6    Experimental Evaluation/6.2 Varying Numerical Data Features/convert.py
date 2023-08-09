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

# "DataFile,Datatype,Data Mean,Data Std,Data Spread,Delta Mean,Delta Std,Delta Spread,Repeat,Increase,Compression,Encoding,Compression Ratio,Select Time,Insert Time\n"

INPUT_PATH = "../../Synthetic_Numerical_result.csv"
FEATURE_PATH = "../../Synthetic_Numerical_feature.csv"

features = [
    ["Delta_mean", "result_delta_mean_ratio.csv"],
    ["Delta_std", "result_delta_std_ratio.csv"],
    ["Increase", "result_delta_increase_ratio.csv"],
    ["Repeat", "result_repeat_ratio.csv"],
    ["Value_mean", "result_mean_ratio.csv"],
]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

df1 = pd.read_csv(INPUT_PATH)
df1 = df1.rename(
    columns={
        "Input Direction": "DataFile",
        "Compress Algorithm": "Compression",
        "Encoding Algorithm": "Encoding",
    }
)
df1["Insert Time"] = (df1["Encoding Time"] + df1["Compress Time"]) / 10**9
df1["Select Time"] = (df1["Decoding Time"] + df1["Uncompress Time"]) / 10**9

df2 = pd.read_csv(FEATURE_PATH)

df = pd.merge(df1, df2, how="inner", on="DataFile")
df = df[df["Compression"].str.contains("UNCOMPRESSED")]
df = df[df["DataFile"].str.contains("FLOAT")]

for [feature, OUTPUT_PATH] in features:
    ef = df.copy()
    ef = ef[ef["DataFile"].str.contains(feature)]
    ef = ef[
        [
            "DataFile",
            "Datatype",
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
            "Compression",
            "Encoding",
            "Compression Ratio",
            "Select Time",
            "Insert Time",
        ]
    ]
    ef.to_csv(OUTPUT_PATH, index=False)
