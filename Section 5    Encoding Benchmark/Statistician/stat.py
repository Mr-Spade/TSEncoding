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

DATA_PATH = "../Datasets/Real-world/Numerical/DOUBLE"
RESULT_PATH = "./stat.csv"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger = open(RESULT_PATH, "w")
logger.write("Dataset,points,series\n")

datasets = os.listdir(DATA_PATH)

for dataset in datasets:
    point_count = 0
    datas = os.listdir(DATA_PATH+'/'+dataset)
    for data in datas:
        point_count += len(open(DATA_PATH+'/'+dataset+'/' +
                           data, 'r').read().split('\n'))-1
    logger.write("{},{},{}\n".format(dataset, point_count, len(datas)))
