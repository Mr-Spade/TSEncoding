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

RESULT_PATH = "./result_ingestion.csv"

# header="DataSet,DataType,Compressor,Encoding,Insert Time,Select Time\n"

os.chdir(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv('../../Real_Text_result.csv')


def get_dataset_name(s: str) -> str:
    return re.findall(r".*/(.*?)/(?:.*?)\.csv", s)[0]


def name_convert(s: str) -> str:
    return "NONE" if s == "UNCOMPRESSED" else s


df['DataSet'] = df['Input Direction'].apply(get_dataset_name)
ef = df[['DataSet', 'Input Direction']].drop_duplicates()
ef = ef.groupby('DataSet').head(20).reset_index()
df = ef.merge(df, how="left", on=['DataSet', 'Input Direction'])
df['DataType'] = df['Data Type']
df['Compression'] = df['Compress Algorithm'].apply(name_convert)
df['Encoding'] = df['Encoding Algorithm']
df['Insert Time'] = (df['Encoding Time']+df['Compress Time'])/10**9
df['Select Time'] = (df['Decoding Time']+df['Uncompress Time'])/10**9
df = df[['DataSet', 'DataType', 'Compression',
         'Encoding', 'Insert Time', 'Select Time']]

df.to_csv(RESULT_PATH, index=False)
