#!/usr/bin/env python

import json
import numpy as np
from scipy import stats
import os
import sys
from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans



# Choosing config file
configFilename = "config-sample.json"
argCount = len(sys.argv)
if(argCount > 1):
    configFilename = sys.argv[1]

# Defining paths
outputDirectory = "output/csv"

if(not os.path.exists(outputDirectory)):
    os.makedirs(outputDirectory)

outputDirectory1="output"

# Reading config file
with open(configFilename, "r") as fd:
    config = json.load(fd)




print("Loading time series...")

timeseriesFilename = config["tsv"]
nclus = config["nclus"]

ts = pd.read_csv(timeseriesFilename,sep="\t")

K = np.sum(ts, axis=1)
R = (K != 0)
xR, = np.where(R == 0)
ts = np.delete(ts, xR, axis=1)

columns=ts.columns
# z-scored time series
z = stats.zscore(ts,1)


print("Building edge time series...")
T, N= ts.shape
u,v = np.where(np.triu(np.ones(N),1))           # get edges
# element-wise prroduct of time series
ets = (z[:,u]*z[:,v])
edgeids = {"edgeid":edge for edge in zip(columns[u],columns[v])}

nclus=int(config['num_clus'])
#Clustering edge time series
etsclus=KMeans(n_clusters=nclus, random_state=0).fit(ets).labels_

np.savetxt('outputDirectory/clustered_edge_timeseries.csv',etsclus,delimiter=',') 
with open('edgeids.json', 'w') as outfile:
    json.dump(outputDirectory1/edgeids, outfile)