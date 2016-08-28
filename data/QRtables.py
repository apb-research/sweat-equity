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
pd.set_option('expand_frame_repr', False)


scf = pd.read_csv('scf.csv')


################## Table 2
i =0
Q = [0, .01, .05, .1, .2, .4, .5, .6, .8, .9, .95, .99, 1]
qi=[stats.quantile_1D(scf.INCOME,scf.WGT,q) for q in Q]
qw=[stats.quantile_1D(scf.NETWORTH,scf.WGT,q) for q in Q]
data_for_plotting=pd.DataFrame(np.vstack((qi,qw)),columns=[str(q) for q in Q], index=['income', 'wealth'])
print('\n'+'TABLE 2:')
print(data_for_plotting)

pd.options.display.float_format = '{:,.2f}'.format

################## Table 3
#Income (INCOME2 can also be used!)

data_for_plotting=pd.concat([stats.describe(scf.NETWORTH,scf.WGT),stats.describe(scf.INCOME,scf.WGT)],axis=1)

data_for_plotting.columns=['NETWORTH','INCOME']
print('\n'+'TABLE 3')
print(data_for_plotting)

#
     
income_by_busorg=[]
colnames=[]
business_types_codes={1:'P', 2:'SP', 3:'S',\
4:'C', 6:'Foreign',11:'LLP',0:'No-Business'}

for bus in pd.unique(scf.BUSORG):
    income_by_busorg.append(stats.describe(scf[scf.BUSORG==bus].INCOME,scf[scf.BUSORG==bus].WGT))
    colnames.append(business_types_codes[bus])


income_by_busorg= pd.concat(income_by_busorg,axis=1)
income_by_busorg.columns=colnames
income_by_busorg['overall']=data_for_plotting['INCOME']
print('\n'+'TABLE 4: INCOME by BUSORG')
print(income_by_busorg)



networth_by_busorg=[]
colnames=[]
business_types_codes={1:'P', 2:'SP', 3:'S',\
4:'C', 6:'Foreign',11:'LLP',0:'No-Business'}

for bus in pd.unique(scf.BUSORG):
    networth_by_busorg.append(stats.describe(scf[scf.BUSORG==bus].NETWORTH,scf[scf.BUSORG==bus].WGT))
    colnames.append(business_types_codes[bus])


networth_by_busorg= pd.concat(networth_by_busorg,axis=1)
networth_by_busorg.columns=colnames
networth_by_busorg['overall']=data_for_plotting['NETWORTH']
print('\n'+'TABLE 5: NETWORTH by BUSORG')
print(networth_by_busorg)

scorpwages=scf[(scf.BUSORG==3)&(scf.WAGEINC>0)].WAGEINC
scorpwages_wgts=scf[(scf.BUSORG==3)&(scf.WAGEINC>0)].WGT

scorpincome=scf[(scf.BUSORG==3)&(scf.WAGEINC>0)].INCOME
scorpincome_wgts=scf[(scf.BUSORG==3)&(scf.WAGEINC>0)].WGT

scorps=pd.concat([stats.describe(scorpwages,scorpwages_wgts),stats.describe(scorpincome,scorpincome_wgts)],axis=1)
scorps.columns=['S-WAGE','S-INCOME']



partnershipwages=scf[(scf.BUSORG==1)&(scf.WAGEINC>0)].WAGEINC
partnershipwages_wgts=scf[(scf.BUSORG==1)&(scf.WAGEINC>0)].WGT

partnershipincome=scf[(scf.BUSORG==1)&(scf.WAGEINC>0)].INCOME
partnershipincome_wgts=scf[(scf.BUSORG==1)&(scf.WAGEINC>0)].WGT

partnerships=pd.concat([stats.describe(partnershipwages,partnershipwages_wgts),stats.describe(partnershipincome,partnershipincome_wgts)],axis=1)
partnerships.columns=['P-WAGE','P-INCOME']




solepropwages=scf[(scf.BUSORG==2)&(scf.WAGEINC>0)].WAGEINC
solepropwages_wgts=scf[(scf.BUSORG==2)&(scf.WAGEINC>0)].WGT

solepropincome=scf[(scf.BUSORG==2)&(scf.WAGEINC>0)].INCOME
solepropincome_wgts=scf[(scf.BUSORG==2)&(scf.WAGEINC>0)].WGT

soleprops=pd.concat([stats.describe(solepropwages,solepropwages_wgts),stats.describe(solepropincome,solepropincome_wgts)],axis=1)
soleprops.columns=['SP-WAGE','SP-INCOME']



wage_income=pd.concat([soleprops,partnerships,scorps],axis=1)
print('\n'+'TABLE 5: INCOME,WAGES by BUSORG')
print(wage_income)
