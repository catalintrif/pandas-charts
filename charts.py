import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

# Loads data from CSV and produces graph based on data aggregations 
data = pd.read_csv('ps1-2017.csv', index_col=0)
df = data.groupby('Ofertant').sum().sort_values(by='Pret inchidere', ascending=False)
df = df[0:10]
print df
#df.plot.bar()
#nr = data.groupby('Ofertant').size()
#print nr
#plot.figure()
#df.iloc[1].plot(kind='bar')
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
print ts
plt.figure()
ts.plot()
pylab.show()
