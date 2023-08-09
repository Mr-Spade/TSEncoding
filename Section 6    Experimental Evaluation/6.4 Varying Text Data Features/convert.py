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

INPUT_PATH = "../../Synthetic_Text_result.csv"
FEATURE_PATH = "../../Synthetic_Text_feature.csv"

features = [
    ["Exponent", "exponent"],
    ["Length", "length"],
    ["Repeat", "repeat"],
    ["Class", "types"]
]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# "DataFile,Compression,Encoding,Exponent,Types,Length,Repeat,Compression Ratio\n"
# "DataFile,Compression,Encoding,Exponent,Types,Length,Repeat,Select Time,Insert Time\n"

df1 = pd.read_csv(INPUT_PATH)
df1 = df1.rename(columns={"Input Direction": "DataFile",
                 "Encoding Algorithm": "Encoding", "Compress Algorithm": "Compression"})
df1["Insert Time"] = (df1["Encoding Time"]+df1["Compress Time"])/10**9
df1["Select Time"] = (df1["Decoding Time"]+df1["Uncompress Time"])/10**9

df2 = pd.read_csv(FEATURE_PATH)

df = pd.merge(df1, df2, how='inner', on='DataFile')
df = df[df["Compression"].str.contains("UNCOMPRESSED")]

for [feature, PATH] in features:
    ef = df.copy()
    ef = ef[ef["DataFile"].str.contains(feature)]
    ef[["DataFile", "Compression", "Encoding", "Exponent", "Types", "Length", "Repeat", "Pattern Repeat",
        "Compression Ratio"]].to_csv("{}_text_ratio_result.csv".format(PATH), index=False)
    ef[["DataFile", "Compression", "Encoding", "Exponent", "Types", "Length", "Repeat", "Pattern Repeat",
        "Select Time", "Insert Time"]].to_csv("{}_text_time_result.csv".format(PATH), index=False)
