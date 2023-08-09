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

INPUT_PATH = "../../Real_Numerical_result.csv"

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
Compressors = ["UNCOMPRESSED", "GZIP", "SNAPPY", "LZ4"]
Types = ["DOUBLE", "TIMESTAMP"]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for type in Types:
    df = pd.read_csv(INPUT_PATH)
    df = df[df["Data Type"] == type]
    del df["Input Direction"]

    for Compressor in Compressors:
        ef = df.copy()
        ef = ef[ef["Compress Algorithm"] == Compressor]
        ef = ef.groupby(["Encoding Algorithm"]).mean()
        ef = 1 - (ef - ef.min()) / (ef.max() - ef.min())
        ef = ef.reset_index()
        ef = ef.rename(columns={"Encoding Algorithm": "Algorithm"})
        ef = ef[
            [
                "Algorithm",
                "Encoding Time",
                "Decoding Time",
                "Compress Time",
                "Uncompress Time",
                "Compression Ratio",
            ]
        ]
        ef["order"] = pd.Categorical(ef["Algorithm"], categories=Encoders, ordered=True)
        ef = ef.sort_values("order").drop("order", axis=1)
        ef.to_csv("{}_avg_{}.csv".format(Compressor.lower(), type), index=False)
