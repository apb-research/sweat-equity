# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:30:13 2016
Tabel 2 and 3 of QR
@author: Mohammad
"""
scf = pd.read_csv('scf.csv')

################## Table 2
i =0
Q = [0, .01, .05, .1, .2, .4, .5, .6, .8, .9, .95, .99, 1]
qi , qw = np.zeros(len(Q)), np.zeros(len(Q))
for q in Q:
    qi[i]= quant(scf.INCOME, scf.WGT, q)
    qw[i]= quant(scf.NETWORTH, scf.WGT, q)
    i +=1
data_for_plotting=pd.DataFrame(np.vstack((qi,qw)),columns=Q, index=['income', 'wealth'])
print('\n'+'TABLE 2:')
print(data_for_plotting)

################## Table 3
#Income (INCOME2 can also be used!)
si= np.zeros(8)
si[0]=variation(scf.INCOME, scf.WGT)
si[1]=variance(np.log(scf.INCOME[(scf.INCOME>0)]),scf.WGT[(scf.INCOME>0)])
si[2]=gini(scf.INCOME, scf.WGT)

si[3]=loc(scf.INCOME, scf.WGT, mean(scf.INCOME, scf.WGT))
si[4]=quant(scf.INCOME, scf.WGT, .99)/quant(scf.INCOME, scf.WGT, .5)
si[5]=quant(scf.INCOME, scf.WGT, .9)/quant(scf.INCOME, scf.WGT, .5)
si[6]=mean(scf.INCOME, scf.WGT)/quant(scf.INCOME, scf.WGT, .5)
si[7]=quant(scf.INCOME, scf.WGT, .5)/quant(scf.INCOME, scf.WGT, .3)

# Networth
sw= np.zeros(8)
sw[0]=variation(scf.NETWORTH, scf.WGT)
sw[1]=variance(np.log(scf.NETWORTH[(scf.NETWORTH>0)]),scf.WGT[(scf.NETWORTH>0)])
sw[2]=gini(scf.NETWORTH, scf.WGT)

sw[3]=loc(scf.NETWORTH, scf.WGT, mean(scf.NETWORTH, scf.WGT))
sw[4]=quant(scf.NETWORTH, scf.WGT, .99)/quant(scf.NETWORTH, scf.WGT, .5)
sw[5]=quant(scf.NETWORTH, scf.WGT, .9)/quant(scf.NETWORTH, scf.WGT, .5)
sw[6]=mean(scf.NETWORTH, scf.WGT)/quant(scf.NETWORTH, scf.WGT, .5)
sw[7]=quant(scf.NETWORTH, scf.WGT, .5)/quant(scf.NETWORTH, scf.WGT, .3)

data_for_plotting=pd.DataFrame(np.vstack((si,sw)),columns=['Coefficient of variation','Variance of logs',\
     'Gini indexes','Location of mean','99-50 ratio', '90-50 ratio', 'Mean-to-median ratio',\
     '50-30 ratio'], index=['income', 'wealth'])
data_for_plotting=data_for_plotting.T

print('\n'+'TABLE 3')
print(data_for_plotting)