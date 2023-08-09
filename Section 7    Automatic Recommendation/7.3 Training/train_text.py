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
import time

from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import classification_report
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import joblib

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Encoders = ["HUFFMAN", "MTF", "BW", "DICTIONARY", "RLE", "AC", "PLAIN"]
Features = ["Exponent", "Types", "Repeat", "Pattern Repeat", "Length"]

label = Encoders
vnames = Features


def plot_confusion_matrix(
    cm,
    target_names,
    title="Confusion matrix",
    cmap=None,
    normalize=True,
    save="result.eps",
):
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap("Blues")

    plt.figure(figsize=(5, 4))
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(
                j,
                i,
                "{:0.4f}".format(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
            )
        else:
            plt.text(
                j,
                i,
                "{:,}".format(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
            )

    plt.tight_layout()
    plt.ylabel("True label")
    # plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.xlabel("Predicted label")
    plt.savefig(save, format="eps", dpi=40, bbox_inches="tight")
    # plt.show()


def print_metrices(pred, true):
    # print(confusion_matrix(true, pred))
    # print(classification_report(true, pred, target_names=label,digits=4))
    pre = precision_score(true, pred, average="weighted", labels=label)
    recall = recall_score(true, pred, average="weighted", labels=label)
    f1 = f1_score(true, pred, average="weighted", labels=label)
    print("Weighted Precison : ", pre)
    print("Weighted Recall : ", recall)
    print("F1 : ", f1)
    return "{},{},{}".format(pre, recall, f1)


global X_train, X_test, y_train, y_test, logger


def prepare(INPUT_PATH):
    global X_train, X_test, y_train, y_test
    data = pd.read_csv(INPUT_PATH)
    data.dropna(axis=0, how="any", inplace=True)
    data.info()
    encoding = data["Encoding Algorithm"].to_numpy()
    y = encoding
    # print(np.unique(y))
    X = data[vnames].to_numpy()
    # X_train, y_train = X, y
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=81
    )


def LR(position=None):
    start = time.time()
    pipeline = pipeline = Pipeline(
        [("lr", LogisticRegression(class_weight="balanced"))]
    )
    param_dist = {"lr__penalty": ["l2", "elasticnet"], "lr__C": np.logspace(-3, 3, 7)}
    grid = GridSearchCV(
        pipeline,
        param_dist,
        verbose=2,
        refit=True,
        cv=3,
        n_jobs=-1,
        scoring="f1_weighted",
    )
    grid.fit(X_train, y_train)
    end = time.time()
    # print(grid.best_params_, grid.best_score_)
    # print('The accuracy of best model in LogisticRegression set is',
    #       grid.score(X_test, y_test))

    pred = grid.predict(X_test)
    if position != None:
        plot_confusion_matrix(
            confusion_matrix(y_test, pred, labels=label),
            target_names=label,
            normalize=False,
            title="Confusion matrix of Logistic Regression on {} data".format(position),
            save="LR_{}_text.eps".format(position),
        )
    else:
        logger.write(
            "{},{},{}\n".format("LR", print_metrices(pred, y_test), end - start)
        )


def SVM(position=None):
    start = time.time()
    pipeline = pipeline = Pipeline([("lr", SVC())])

    param_dist = {"lr__C": np.logspace(-3, 3, 7)}
    # param_dist = {}
    grid = GridSearchCV(
        pipeline,
        param_dist,
        verbose=2,
        refit=True,
        cv=3,
        n_jobs=-1,
        scoring="f1_weighted",
    )
    grid.fit(X_train, y_train)
    end = time.time()
    # print(grid.best_params_, grid.best_score_)
    # print('The accuracy of best model in Support Vector Machine set is',
    #       grid.score(X_test, y_test))

    pred = grid.predict(X_test)
    if position != None:
        plot_confusion_matrix(
            confusion_matrix(y_test, pred, labels=label),
            target_names=label,
            normalize=False,
            title="Confusion matrix of Support Vector Machine on {} data".format(
                position
            ),
            save="SVM_{}_text.eps".format(position),
        )
    else:
        logger.write(
            "{},{},{}\n".format("SVM", print_metrices(pred, y_test), end - start)
        )


def DT(position=None):
    start = time.time()
    pipeline = Pipeline([("dt", DecisionTreeClassifier())])

    param_dist = {
        "dt__criterion": ["gini", "entropy"],
        "dt__max_depth": [1, 2, 3, 4, 5, 6, 7, 8, 9, None],
    }
    # param_dist ={}
    grid = GridSearchCV(
        pipeline,
        param_dist,
        verbose=2,
        refit=True,
        cv=5,
        n_jobs=-1,
        scoring="f1_weighted",
    )
    grid.fit(X_train, y_train)
    end = time.time()
    # print(grid.best_params_, grid.best_score_)
    # print('The accuracy of best model in SVC set is', grid.score(X_test, y_test))

    pred = grid.predict(X_test)
    print_metrices(pred, y_test)
    if position != None:
        plot_confusion_matrix(
            confusion_matrix(y_test, pred, labels=label),
            target_names=label,
            normalize=False,
            title="Confusion matrix of Decision Tree on {} data".format(position),
            save="DT_{}_text.eps".format(position),
        )
    else:
        logger.write(
            "{},{},{}\n".format("DT", print_metrices(pred, y_test), end - start)
        )


def RF(position=None):
    start = time.time()
    pipeline = Pipeline(
        [("rf", RandomForestClassifier(n_estimators=300, criterion="entropy"))]
    )

    # param_dist = {'rf__n_estimators':range(250,350,10)}
    # param_dist = {  'rf__criterion': ['entropy'], 'rf__n_estimators':[300]}
    param_dist = {}
    grid = GridSearchCV(
        pipeline,
        param_dist,
        verbose=2,
        refit=True,
        cv=2,
        n_jobs=-1,
        scoring="f1_weighted",
    )
    grid.fit(X_train, y_train)
    end = time.time()
    # print(grid.best_params_, grid.best_score_)
    # print('The accuracy of best model in RandomForest set is', grid.score(X_test, y_test))

    pred = grid.predict(X_test)
    if position != None:
        plot_confusion_matrix(
            confusion_matrix(y_test, pred, labels=label),
            target_names=label,
            normalize=False,
            title="Confusion matrix of Random Forest on {} data".format(position),
            save="RF_{}_text.eps".format(position),
        )
    else:
        logger.write(
            "{},{},{}\n".format("RF", print_metrices(pred, y_test), end - start)
        )


def GDBT(position=None):
    start = time.time()
    pipeline = Pipeline(
        [("gbc", GradientBoostingClassifier(n_estimators=100, max_depth=7))]
    )

    # param_dist = {  'gbc__n_estimators': range(10,100,10),'gbc__max_depth': [2,3,4,5,6,7,8,None]}
    param_dist = {}

    grid = GridSearchCV(
        pipeline,
        param_dist,
        verbose=2,
        refit=True,
        cv=2,
        n_jobs=-1,
        scoring="f1_weighted",
    )
    grid.fit(X_train, y_train)
    end = time.time()
    # print(grid.best_params_, grid.best_score_)
    # print('The accuracy of best model in BalancedBagging set is',
    #       grid.score(X_test, y_test))

    pred = grid.predict(X_test)
    if position != None:
        plot_confusion_matrix(
            confusion_matrix(y_test, pred, labels=label),
            target_names=label,
            normalize=False,
            title="Confusion matrix of Gradient Boosting on {} data".format(position),
            save="GDBT_{}_text.eps".format(position),
        )
    else:
        logger.write(
            "{},{},{}\n".format("GDBT", print_metrices(pred, y_test), end - start)
        )


def MLP(position=None):
    start = time.time()
    pipeline = Pipeline(
        [
            (
                "gbc",
                MLPClassifier(hidden_layer_sizes=80, activation="logistic", alpha=0.1),
            )
        ]
    )

    # param_dist = {  'gbc__hidden_layer_sizes': range(10,100,5),
    # 'gbc__activation' : ['identity', 'logistic', 'tanh', 'relu']}
    param_dist = {"gbc__alpha": np.logspace(-4, 4, 9)}
    # param_dist = {}

    grid = GridSearchCV(
        pipeline,
        param_dist,
        verbose=2,
        refit=True,
        cv=3,
        n_jobs=-1,
        scoring="f1_weighted",
    )
    grid.fit(X_train, y_train)
    end = time.time()
    # print(grid.best_params_, grid.best_score_)
    # print('The accuracy of best model in BalancedBagging set is',
    #       grid.score(X_test, y_test))

    pred = grid.predict(X_test)
    if position != None:
        plot_confusion_matrix(
            confusion_matrix(y_test, pred, labels=label),
            target_names=label,
            normalize=False,
            title="Confusion matrix of Multi-layer Perceptron on {} data".format(
                position
            ),
            save="MLP_{}_text.eps".format(position),
        )
    else:
        logger.write(
            "{},{},{}\n".format("MLP", print_metrices(pred, y_test), end - start)
        )


RESULT_PATH = "./train_result_text.csv"

prepare("./train_text.csv")
logger = open(RESULT_PATH, "w")
logger.write("Model,Precison,Recall,F1,Time Cost\n")
LR()
SVM()
DT()
RF()
GDBT()
MLP()

prepare("./train_Real_text.csv")
SVM("real-world")
RF("real-world")

prepare("./train_Synthetic_text.csv")
SVM("synthetic")
RF("synthetic")
