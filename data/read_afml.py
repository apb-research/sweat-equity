# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 00:17:20 2016

@author: anmol
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

industry_data=pd.read_excel('AFMLdata.xls',sheetname='industry')
state_data=pd.read_excel('AFMLdata.xls',sheetname='state')

important_industries=industry_data[(industry_data['sample']=='full sample') & (industry_data['entity']=='private')][['industry','num']].sort_values(by=['num']).tail(6)


data=industry_data[industry_data.industry.isin(important_industries.industry.values)]
var='roa'


excess_matched=data[(data['sample']=='matched sample') & (data['entity']=='private')][var].values-data[(data['sample']=='matched sample') & (data['entity']=='public')][var].values
excess_full=data[(data['sample']=='full sample') & (data['entity']=='private')][var].values-data[(data['sample']=='full sample') & (data['entity']=='public')][var].values

data_for_plotting=pd.DataFrame(np.vstack((excess_matched,excess_full)),columns=data.iloc[:,0].unique(),index=['matched','full'])
data_for_plotting=data_for_plotting.T


print('private-public: ' +var)

print(data_for_plotting)



