# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:30:13 2016
Tabel 2 and 3 of QR
@author: Mohammad
"""

import pandas as pd
import numpy as np
import stats
pd.options.display.float_format = '${:,.0f}'.format

scf = pd.read_csv('scf.csv')

################## Table 2
i =0
Q = [0, .01, .05, .1, .2, .4, .5, .6, .8, .9, .95, .99, 1]
qi=[stats.quantile_1D(scf.INCOME,scf.WGT,q) for q in Q]
qw=[stats.quantile_1D(scf.NETWORTH,scf.WGT,q) for q in Q]
data_for_plotting=pd.DataFrame(np.vstack((qi,qw)),columns=Q, index=['income', 'wealth'])
print('\n'+'TABLE 2:')
print(data_for_plotting)

pd.options.display.float_format = '{:,.2f}'.format

################## Table 3
#Income (INCOME2 can also be used!)
si=stats.describe(scf.INCOME,scf.WGT)
# Networth
sw=stats.describe(scf.NETWORTH,scf.WGT)

data_for_plotting=pd.DataFrame(np.vstack((si,sw)),columns=['Coefficient of variation','Variance of logs',\
     'Gini indexes','Location of mean','99-50 ratio', '90-50 ratio', 'Mean-to-median ratio',\
     '50-30 ratio'], index=['income', 'wealth'])
data_for_plotting=data_for_plotting.T

print('\n'+'TABLE 3')
print(data_for_plotting)

#
#
moments=['Coefficient of variation','Variance of logs',\
     'Gini indexes','Location of mean','99-50 ratio', '90-50 ratio', 'Mean-to-median ratio',\
     '50-30 ratio']
     
income_by_busorg=pd.DataFrame(np.zeros((len(moments), len(pd.unique(scf.BUSORG)))))
income_by_busorg.index=moments

business_types_codes={1:'P', 2:'SP', 3:'S',\
4:'C', 6:'Foreign',11:'LLP',0:'Inap'}
income_by_busorg.columns=business_types_codes.values()

for bus in pd.unique(scf.BUSORG):
    income_by_busorg[business_types_codes[bus]]=stats.describe(scf[scf.BUSORG==bus].INCOME,scf[scf.BUSORG==bus].WGT)
#
income_by_busorg['overall']=si


networth_by_busorg=pd.DataFrame(np.zeros((len(moments), len(pd.unique(scf.BUSORG)))))
networth_by_busorg.index=moments
networth_by_busorg.columns=business_types_codes.values()
networth_by_busorg['overall']=sw

for bus in pd.unique(scf.BUSORG):
    networth_by_busorg[business_types_codes[bus]]=stats.describe(scf[scf.BUSORG==bus].NETWORTH,scf[scf.BUSORG==bus].WGT)


print('\n'+'TABLE 4: INCOME by BUSORG')
print(income_by_busorg)


print('\n'+'TABLE 5: NETWORTH by BUSORG')
print(networth_by_busorg)

