# Guideline: Experimental Reproduction

In our paper Time Series Data Encoding for Efficient Storage A Comparative Analysis in Apache IoTDB, we introduced two data generators, several comparison experiments and TSEC, timeseries encoding classifier. 

To enable reproductivity, we open source all datasets, algorithms and codes introduced in the paper, and this document produces a guideline of reproduction. This readme elaborates the file structure of the whole repository, and folders are organised by the sequence of sections.

Please read the readme file in each folder and follow the instructions to reproduce our experimetal results.

## Section 5: Encoding Benchmark

In this section, we introduced the datasets we use including synthetic numerical data, real-world numerical data, synthetic text data and real-world numerical data. We also introduced the evaluation metrix: several data features and how to calculate them. 

In this repository, we open source both synthetic datasets and real-world datasets, as well as the data generator of both numerical and text synthetic data. We also open source the code we used to calculate data features.

## Section 6: Experimental Evaluation

In this section, we carried out evaluations on real-world numerical data, synthetic numerical data, real-world text data and synthetic text data. 

We uploaded the codes used in the evaluations. Detailed information including how to reproduce the result is written in the readme file in each sub folder.

## Section 7: Automatic Recommendation

Based on the analyze of data features above, we propose Time Series EncodingClassifier (TSEC) to automatically recommend a proper encodingmethod upon the profiled data features.

<!-- This part is not included in the paper published on pVLDB, you can download our Section 8    Automatic Recommendation from this link: https://sxsong.github.io/doc/encoding.pdf -->

---

## File Structure

+ Section 5    Encoding Benchmark: datasets, data generators and feature calculators
  + Data Generator: numerical and text data generator
  + DataSets: all datasets of this paper excluding ingestion datasets
  + Feature Calculator: two feature calculator for numerical and text datasets
  + Statistician: Statistics on the information of the data set for verification
+ Section 6    Experimental Evaluation: codes, data, and intruction file of each subsection
  + 6.1 Real-world Numerical Data Evaluation
  + 6.2 Varying Numerical Data Features 
  + 6.3 Real-world Text Data Evaluation 
  + 6.4 Varying Text Data Features 
+ Section 7    Automatic Recommendation: test code and visualization code of each subsection
  + 7.3 Training: machine learning models used in TSEC and python scripts used to train them
    + Correlation: codes used to calculate the pearson correlation between each feature and predicted result
  + 7.5 Comparison: the comparison code of TSEC, CodecDB, C-store and LEA
  + 7.6 Cross Validation: Cross-validation of TSEC on different datasets
  + 7.7 Extra Cost of Recommendation: the code used to text the time cost of feature extracting

## Environment Requirement

+ OS: Ubuntu 22.04LTS
+ IoTDB: download from branch https://github.com/apache/iotdb/tree/research/encoding-exp
+ python: 3.8+
+ modules needed: seaborn 0.11.1+ (used in visualization), scikit-learn 0.24.1+ (used in TSEC), joblib 1.0.1+ (used in TSEC), numpy, pandas

## Data

- Data can be downloaded as `data.zip` from https://cloud.tsinghua.edu.cn/f/e99a87771f8b43819532/
- Move `data.zip` into `./Section 5    Encoding Benchmark`
- In `./Section 5    Encoding Benchmark`, unzip the data file

## Steps

- Clone this repository
- Set IoTDB
  - Clone from https://github.com/apache/iotdb/tree/research/encoding-exp
  - run `mvn clean package -DskipTests -Drat.skip=true` to build IoTDB
  - Generate result data
    - run `mvn test -pl tsfile -Dtest=org.apache.iotdb.tsfile.encoding.decoder.EncodeTest`, and copy `Real_Numerical_result.csv` and `Synthetic_Numerical_result.csv` into the root folder of this repo
    - run `mvn test -pl tsfile -Dtest=org.apache.iotdb.tsfile.encoding.decoder.EncodeTextTest`, and copy `Real_Text_result.csv` and `Synthetic_Text_result.csv` into the root folder of this repo
  - Start IoTDB Server
    - run `./distribution/target/apache-iotdb-1.0.0-all-bin/apache-iotdb-1.0.0-all-bin/sbin/start-standalone.sh && sleep 3` to start server
  - Copy python client
    - Copy `./client-py/iotdb` as `./Section 7    Automatic Recommendation/7.6 Extra Cost of Recommendation/iotdb`
- Follow the steps in `./Section 5    Experimental Evaluation`
- Follow the steps in `./Section 6    Experimental Evaluation`
- Follow the steps in `./Section 7    Automatic Recommendation`
