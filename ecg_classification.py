import numpy as py 
import pandas as pd
from sklearn.model_selection import train_test_split
import math 
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, resample
import wfdb 
import ast
import heartpy as hp
import scipy.signal as ss 

Y = pd.read_csv("ptbxl_database.csv")

print("data: ")
print(Y)

path = ""
sampling_rate = 500

Y.scp_codes = Y.scp_codes.apply(lambda x: ast.literal_eval(x))
data = wfdb.rdsamp("00008_hr")

agg_df = pd.read_csv("scp_statements.csv", index_col=0)
# Filter out the empty ones.
agg_df = agg_df[agg_df.diagnostic == True]

def aggregate_diagnostic(y_dic):
    tmp = []
    for key in y_dic.keys():
        if key in agg_df.index:
            tmp.append(agg_df.loc[key].diagnostic_class)
    return list(set(tmp))


Y['diagnostic_superclass'] = Y.scp_codes.apply(aggregate_diagnostic)

print(data[1])
data = py.array(data[0])
print(data.shape)

x = py.linspace(0,2,5000)
y = data[:5000, 6]

plt.plot(x,y, "-")
plt.ylim((-1,1))
plt.show()

filtered = hp.filter_signal(y,sample_rate=500, filtertype="highpass", cutoff=1)
plt.plot(x,filtered)
plt.show()