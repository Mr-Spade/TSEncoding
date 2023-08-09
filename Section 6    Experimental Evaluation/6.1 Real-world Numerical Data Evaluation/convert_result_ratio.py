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

DataTypes = ["INT32", "INT64", "FLOAT", "DOUBLE"]

RESULT_PATH = "./result_compression_ratio.csv"

# DataType,Compression,Encoding,Compression Ratio

os.chdir(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv('../../Real_Numerical_result.csv')


def name_convert(s: str) -> str:
    return "NONE" if s == "UNCOMPRESSED" else s


df = df[df["Data Type"].isin(DataTypes)]
df['DataType'] = df['Data Type']
df['Compression'] = df['Compress Algorithm'].apply(name_convert)
df['Encoding'] = df['Encoding Algorithm']
df = df[['DataType', 'Compression', 'Encoding', 'Compression Ratio']]

df.to_csv(RESULT_PATH, index=False)
