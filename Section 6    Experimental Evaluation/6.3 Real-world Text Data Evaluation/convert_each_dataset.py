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

Features = ['Exponent', 'Types', 'Repeat', 'Pattern Repeat', 'Length']

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RATIO_PATH = "./ratio_each_dataset.csv"
FEATURE_PATH = "./feature_each_dataset.csv"


def get_dataset_name(s: str) -> str:
    return re.findall(r".*/(.*?)/(?:.*?)\.csv", s)[0]


df = pd.read_csv("../../Real_Text_result.csv")

df['Dataset'] = df['Input Direction'].apply(get_dataset_name)
df = df[df['Compress Algorithm'] == 'UNCOMPRESSED']
df = df[['Dataset', 'Encoding Algorithm', 'Compression Ratio']]
df = df.groupby(['Dataset', 'Encoding Algorithm']).mean().reset_index()
df.to_csv(RATIO_PATH, index=False)

df = pd.read_csv("../../Real_Text_feature.csv")

df['Dataset'] = df['DataFile'].apply(get_dataset_name)
df = df[['Dataset']+Features]
df = df.groupby('Dataset').mean().reset_index()
df_new = pd.melt(df, id_vars='Dataset', var_name='feature', value_name='value')
df_new.to_csv(FEATURE_PATH,index=False)