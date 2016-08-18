# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:39:25 2016

This is a script for reading SCF 2013.
@author: khani004
"""
#    Table of contents:
#        Weights
#        Demographics
#        Net worth
#        Income
#        Earnings
#        Private Business
from pylab import *
import numpy as np
import pandas as pd

# conv converts payments to YEARLY basis
# NOTE: this macro does not convert LUMP SUM (code 8), BY THE PIECE/JOB (code 14), and VARIES (code 22)
def conv(f):
    cf=(f==1)*365+(f==2)*52+(f==3)*26+(f==4)*12+(f==5)*4+(f==6)+(f==11)*2\
        +(f==12)*6+(f==18)*24*30*12+(f==31)*24+(f==23)*13+(f==24)*52/6
    return cf

scf = pd.read_stata('p13i6.dta')

# Series of zeros used for max(0,x)
zero=pd.Series(np.zeros(scf.X102.size)) # X102 is arbitrary!

# Keep list:
keep = ['WGT', 'WGT0', 'HHSEX', 'EDUC', 'CHECKING', 'SAVING', 'MMA', 'CALL', 'LIQ', 'CDS',\
     'STMUTF', 'TFBMUTF', 'GBMUTF', 'OBMUTF', 'COMUTF', 'OMUTF', 'NMMF', 'STOCKS', 'NOTXBND',\
     'MORTBND', 'GOVTBND', 'OBND', 'BOND', 'IRAKH', 'THRIFT', 'PENEQ', 'FUTPEN', 'CURRPEN',\
     'RETQLIQ', 'SAVBND', 'CASHLI', 'ANNUIT', 'TRUSTS', 'OTHMA', 'OTHFIN', 'FIN',\
     'VEHIC', 'FARMBUS', 'HOUSES', 'ORESRE', 'NNRESRE', 'BUS', 'ACTBUS', 'NONACTBUS', 'OTHNFIN', 'NFIN',\
     'ASSET', 'MRTHEL', 'RESDBT', 'OTHLOC', 'CCBAL', 'INSTALL', 'ODEBT', 'DEBT', 'NETWORTH',\
     'INCOME', 'WAGEINC', 'SOLPFARMINC', 'RENTINC', 'BUSSEFARMINC', 'INTDIVINC', 'KGINC',\
     'SSRETINC', 'TRANSFOTHINC', 'PENACCTWD', 'OWNPBUS', 'ACTMGT', 'BUSORG']



###############################################################################
#                                     Weights
###############################################################################
#   divide weight by 5 so totals estimated on the 5 implicates jointly
#   are correct
scf['WGT']=scf.X42001/5

#   retain original weight: WGT0
scf['WGT0']=scf.X42001

###############################################################################
#                                   Demographics
###############################################################################
#   sex of household head
scf['HHSEX']=scf.X8021
#   education of the HH head
scf['EDUC']=scf.X5901
# There are more! I am not including much for now!

###############################################################################
#                                   NET WORTH
###############################################################################

############################### FINANCIAL ASSETS ##############################
## Checking Accounts
scf['CHECKING'] = scf.X3506.combine(zero,max)*(scf.X3507==5)+scf.X3510.combine(zero,max)*(scf.X3511==5)+\
    scf.X3514.combine(zero,max)*(scf.X3515==5)+scf.X3518.combine(zero,max)*(scf.X3519==5)+\
    scf.X3522.combine(zero,max)*(scf.X3523==5)+scf.X3526.combine(zero,max)*(scf.X3527==5)+\
    scf.X3529.combine(zero,max)*(scf.X3527==5)

## Saving Accounts
scf['SAVING']=scf.X3730.combine(zero,max)*(~scf.X3732.isin([4, 30]))+scf.X3736.combine(zero,max)*(~scf.X3738.isin([4, 30]))+\
    scf.X3742.combine(zero,max)*(~scf.X3744.isin([4, 30]))+scf.X3748.combine(zero,max)*(~scf.X3750.isin([4, 30]))+\
    scf.X3754.combine(zero,max)*(~scf.X3756.isin([4, 30]))+scf.X3760.combine(zero,max)*(~scf.X3762.isin([4, 30]))+\
    scf.X3765.combine(zero,max)
        

##  money market accounts;
#scf.MMA=scf.MMDA+scf.MMMF
scf['MMA']=scf.X3506.combine(zero,max)*(scf.X3507==1)\
          +scf.X3510.combine(zero,max)*(scf.X3511==1)\
          +scf.X3514.combine(zero,max)*(scf.X3515==1)\
          +scf.X3518.combine(zero,max)*(scf.X3519==1)\
          +scf.X3522.combine(zero,max)*(scf.X3523==1)\
          +scf.X3526.combine(zero,max)*(scf.X3527==1)\
          +scf.X3529.combine(zero,max)*(scf.X3527==1)\
          +scf.X3730.combine(zero,max)*(scf.X3732.isin([4,30]))\
          +scf.X3736.combine(zero,max)*(scf.X3738.isin([4,30]))\
          +scf.X3742.combine(zero,max)*(scf.X3744.isin([4,30]))\
          +scf.X3748.combine(zero,max)*(scf.X3750.isin([4,30]))\
          +scf.X3754.combine(zero,max)*(scf.X3756.isin([4,30]))\
          +scf.X3760.combine(zero,max)*(scf.X3762.isin([4,30]))\
          +scf.X3765.combine(zero,max)*(scf.X3762.isin([4,30]))
    
##  call accounts at brokerages;
scf['CALL']=scf.X3930.combine(zero,max)

#   all types of transactions accounts (liquid assets);
scf['LIQ']=scf.CHECKING+scf.SAVING+scf.MMA+scf.CALL

##   certificates of deposit;
scf['CDS']=scf.X3721.combine(zero,max)

###   mutual funds;
##   stock mutual funds;
scf['STMUTF']=(scf.X3821==1)*scf.X3822.combine(zero,max)
##   tax-free bond mutual funds;
scf['TFBMUTF']=(scf.X3823==1)*scf.X3824.combine(zero,max)
##   government bond mutual funds;
scf['GBMUTF']=(scf.X3825==1)*scf.X3826.combine(zero,max)
##   other bond mutual funds;
scf['OBMUTF']=(scf.X3827==1)*scf.X3828.combine(zero,max)
##   combination and other mutual funds;
scf['COMUTF']=(scf.X3829==1)*scf.X3830.combine(zero,max)
##     other mutual funds;
scf['OMUTF']=(scf.X7785==1)*scf.X7787.combine(zero,max)
##  total directly-held mutual funds, excluding MMMFs;
scf['NMMF']=scf.STMUTF+scf.TFBMUTF+scf.GBMUTF+scf.OBMUTF+scf.COMUTF  

###   stocks;
scf['STOCKS']=scf.X3915.combine(zero,max)

###   bonds, not including bond funds or savings bonds;
##   tax-exempt bonds (state and local bonds);
scf['NOTXBND']=scf.X3910
##   mortgage-backed bonds;
scf['MORTBND']=scf.X3906
##   US government and government agency bonds and bills;
scf['GOVTBND']=scf.X3908
##   corporate and foreign bonds;
scf['OBND']=scf.X7634+scf.X7633
##   total bonds, not including bond funds or savings bonds;
scf['BOND']=scf.NOTXBND+scf.MORTBND+scf.GOVTBND+scf.OBND

#*   quasi-liquid retirement accounts (IRAs and thrift-type accounts);
#*   individual retirement accounts/Keoghs;
scf['IRAKH']=scf.X6551+scf.X6559+scf.X6567+scf.X6552+scf.X6560+scf.X6568+scf.X6553+scf.X6561+scf.X6569+scf.X6554+scf.X6562+scf.X6570

#     account-type pension plans (included if type is 401k, 403b,
#      thrift, savings, SRA, or if participant has option to borrow or
#      withdraw);

#     PENEQ counts thrift amounts invested in stock;
PTYPE1=['X11000', 'X11100', 'X11300','X11400']
PTYPE2=['X11001', 'X11101', 'X11301','X11401']
PAMT=['X11032', 'X11132', 'X11332','X11432']
PBOR=['X11025', 'X11125', 'X11325','X11425']
PWIT=['X11031', 'X11131', 'X11331','X11431']
PALL=['X11036', 'X11136', 'X11336','X11436']
PPCT=['X11037', 'X11137', 'X11337','X11437']
scf['THRIFT'] =zero
scf['PENEQ'] =zero
RTHRIFT=zero
STHRIFT=zero
REQ=zero
SEQ=zero

for i in range(len(PTYPE1)):
    HOLD = scf[PAMT[i]].combine(zero,max)*((scf[PTYPE1[i]]==1) |\
      scf[PTYPE2[i]].isin([2,3,4,6,20,21,22,26]) | (scf[PBOR[i]]==1) | (scf[PWIT[i]]==1))
    if (i<=2): RTHRIFT=RTHRIFT+HOLD
    else: STHRIFT=STHRIFT+HOLD
    scf.THRIFT=scf.THRIFT+HOLD
    scf.PENEQ=scf.PENEQ+HOLD*(scf[PALL[i]]==1)+HOLD*(scf[PALL[i]].isin([3,30]))*((scf[PPCT[i]].combine(zero,max))/10000)
    if (i<=2): REQ=scf.PENEQ
    else: SEQ=scf.PENEQ-REQ
      
#     allocate the pension mopups;
#     where possible, use information for first three pensions to infer
#      characteristics of this amount;
#     where not possible to infer whether R can borrow/make withdrawals,
#      assume this is possible;
#     where not possible to determine investment direction, assume half
#      in stocks;

PMOP=scf.X11259*(scf.X11259>0)*(((scf[PTYPE1[0]]==1) | (scf[PTYPE1[1]]==1) | scf[PTYPE2[0]].isin([2,3,4,6,20,21,22,26]) |\
    scf[PTYPE2[1]].isin([2,3,4,6,20,21,22,26]) | (scf[PWIT[0]]==1) | (scf[PWIT[1]]==1) | (scf[PBOR[0]]==1) | (scf[PBOR[1]]==1))|\
    ((scf[PTYPE1[0]]==0) | (scf[PTYPE1[1]]==0) | (scf[PWIT[0]]==0) | (scf[PWIT[1]]==0)))   
scf.THRIFT=scf.THRIFT+PMOP
scf.PENEQ=scf.PENEQ+(REQ>0)*PMOP*(REQ/RTHRIFT)+(REQ<=0)*PMOP/2

PMOP=scf.X11559*(scf.X11559>0)*(((scf[PTYPE1[2]]==1) | (scf[PTYPE1[3]]==1) | \
      scf[PTYPE2[2]].isin([2,3,4,6,20,21,22,26]) | \
      scf[PTYPE2[3]].isin([2,3,4,6,20,21,22,26]) |  \
      (scf[PWIT[2]]==1)|(scf[PWIT[3]]==1)|(scf[PBOR[2]]==1)|(scf[PBOR[3]]==1))|\
    ((scf[PTYPE1[2]]==0) | (scf[PTYPE1[3]]==0) | (scf[PWIT[2]]==0) | (scf[PWIT[3]]==0)))
scf.THRIFT=scf.THRIFT+PMOP
scf.PENEQ=scf.PENEQ+(SEQ>0)*PMOP*(SEQ/STHRIFT)+(REQ<=0)*PMOP/2

#  DROP HOLD PMOP RTHRIFT STHRIFT REQ SEQ;

##   future pensions (accumulated in an account for the R/S); 
scf['FUTPEN']=scf.X5604.combine(zero,max)+scf.X5612.combine(zero,max)+scf.X5620.combine(zero,max)+scf.X5628.combine(zero,max)
    
##   NOTE: there is very little evidence that pensions with currently
#    received benefits recorded in the SCFs before 2001 were any type
#    of 401k or related account from which the R was making
#    withdrawals:  the questions added in 2001 allow one to distinguish
#    such account, and there are 55 of them in that year:
#    create a second version of RETQLIQ to include this information;
scf['CURRPEN']=scf.X6462+scf.X6467+scf.X6472+scf.X6477+scf.X6957
##     total quasi-liquid: sum of IRAs, thrift accounts, and future pensions; 
##     this version includes currently received benefits;
scf['RETQLIQ']=scf.IRAKH+scf.THRIFT+scf.FUTPEN+scf.CURRPEN

##   savings bonds;
scf['SAVBND']=scf.X3902
    
##   cash value of whole life insurance;
scf['CASHLI']=scf.X4006.combine(zero,max)
    
##   other managed assets (trusts, annuities and managed investment
##    accounts in which HH has equity interest);
scf['ANNUIT']=scf.X6577.combine(zero,max)
scf['TRUSTS']=scf.X6587.combine(zero,max)
scf['OTHMA']=scf.ANNUIT+scf.TRUSTS

##   other financial assets
scf['OTHFIN']=scf.X4018+scf.X4022*(scf.X4020.isin([61,62,63,64,65,66,71,72,73,74,77,80,81,-7]))+\
        scf.X4026*(scf.X4024.isin([61,62,63,64,65,66,71,72,73,74,77,80,81,-7]))+\
        scf.X4030*(scf.X4028.isin([61,62,63,64,65,66,71,72,73,74,77,80,81,-7]))

    
scf['FIN']=scf.LIQ+scf.CDS+scf.NMMF+scf.STOCKS+scf.BOND+scf.RETQLIQ+scf.SAVBND+scf.CASHLI+scf.OTHMA+scf.OTHFIN

############################# NONFINANCIAL ASSETS #############################


##   value of all vehicles (includes autos, motor homes, RVs, airplanes,boats)

scf['VEHIC']=scf.X8166.combine(zero,max)+scf.X8167.combine(zero,max)+scf.X8168.combine(zero,max)+scf.X8188.combine(zero,max)+\
        scf.X2422.combine(zero,max)+scf.X2506.combine(zero,max)+scf.X2606.combine(zero,max)+scf.X2623.combine(zero,max)

#   primary residence;
#   for farmers, assume X507 (percent of farm used for
#    farming/ranching) is maxed at 90%;
scf.X507[scf.X507>9000]=9000
#   compute value of business part of farm net of outstanding mortgages;

scf.X805=scf.X805*((10000-scf.X507)/10000)
scf.X808=scf.X808*((10000-scf.X507)/10000)
scf.X813=scf.X813*((10000-scf.X507)/10000)
scf.X905=scf.X905*((10000-scf.X507)/10000)
scf.X908=scf.X908*((10000-scf.X507)/10000)
scf.X913=scf.X913*((10000-scf.X507)/10000)
scf.X1005=scf.X1005*((10000-scf.X507)/10000)
scf.X1008=scf.X1008*((10000-scf.X507)/10000)
scf.X1013=scf.X1013*((10000-scf.X507)/10000)

scf['FARMBUS']=(scf.X507/10000)*(scf.X513+scf.X526-scf.X805-scf.X905-scf.X1005)\
    -(scf.X1103==1)*scf.X1108*(scf.X507/10000)\
    -(scf.X1114==1)*scf.X1119*(scf.X507/10000)\
    -(scf.X1125==1)*scf.X1130*(scf.X507/10000)
ADD = (scf.X1136*(scf.X507/10000)*\
    (scf.X1108*(scf.X1103==1)+scf.X1119*(scf.X1114==1)+scf.X1130*(scf.X1125==1))/(scf.X1108+scf.X1119+scf.X1130)).replace({np.NaN:0})
scf.FARMBUS=scf.FARMBUS-((scf.X1136>0) & ((scf.X1108+scf.X1119+scf.X1130)>0))*ADD
          
scf.X1108=scf.X1108-(scf.X1103==1)*scf.X1108*(scf.X507/10000)
scf.X1109=scf.X1109-(scf.X1103==1)*scf.X1109*(scf.X507/10000)
scf.X1119=scf.X1108-(scf.X1114==1)*scf.X1119*(scf.X507/10000)
scf.X1120=scf.X1109-(scf.X1114==1)*scf.X1120*(scf.X507/10000)
scf.X1130=scf.X1130-(scf.X1125==1)*scf.X1130*(scf.X507/10000)
scf.X1131=scf.X1131-(scf.X1125==1)*scf.X1131*(scf.X507/10000)

ADD = (scf.X1136*(scf.X507/10000)*((scf.X1108*(scf.X1103==1)\
    +scf.X1119*(scf.X1114==1)+scf.X1130*(scf.X1125==1))/(scf.X1108+scf.X1119+scf.X1130))).replace({np.NaN:0})
scf.X1136=scf.X1136-((scf.X1136>0) & ((scf.X1108+scf.X1119+scf.X1130)>0))*ADD

##   value of primary residence;
scf['HOUSES']=(scf.X604+scf.X614+scf.X623+scf.X716)+((10000-scf.X507.combine(zero,max))/10000)*(scf.X513+scf.X526)
    
##   other residential real estate
scf['ORESRE']=scf.X1306.combine(scf.X1310, max)+scf.X1325.combine(scf.X1329, max)+scf.X1339.combine(zero,max)\
      +(scf.X1703.isin([12,14,21,22,25,40,41,42,43,44,49,50,52,999]))*\
      scf.X1706.combine(zero,max)*(scf.X1705/10000)\
      +(scf.X1803.isin([12,14,21,22,25,40,41,42,43,44,49,50,52,999]))*\
      scf.X1806.combine(zero,max)*(scf.X1805/10000)\
      +scf.X2002.combine(zero,max)
 
##   net equity in nonresidential real estate:
scf['NNRESRE']=(scf.X1703.isin([1,2,3,4,5,6,7,10,11,13,15,24,45,46,47,48,51,53,-7]))*\
      scf.X1706.combine(zero,max)*(scf.X1705/10000)\
      +(scf.X1803.isin([1,2,3,4,5,6,7,10,11,13,15,24,45,46,47,48,51,53,-7]))*\
      scf.X1806.combine(zero,max)*(scf.X1805/10000)\
      +scf.X2012.combine(zero,max)\
      -(scf.X1703.isin([1,2,3,4,5,6,7,10,11,13,15,24,45,46,47,48,51,53,-7]))*\
      scf.X1715*(scf.X1705/10000)\
      -(scf.X1803.isin([1,2,3,4,5,6,7,10,11,13,15,24,45,46,47,48,51,53,-7]))*\
      scf.X1815*(scf.X1805/10000)\
      -scf.X2016

#   remove installment loans for PURPOSE=78 from NNRESRE only
#    where such property exists--otherwise, if ORESRE exists, include
#    loan as RESDBT---otherwise, treat as installment loan;
    
scf['FLAG781']=(scf.NNRESRE!=0).astype(int)
scf.NNRESRE=scf.NNRESRE+scf.FLAG781*(-scf.X2723*(scf.X2710==78)-scf.X2740*(scf.X2727==78)-scf.X2823*(scf.X2810==78)\
        -scf.X2840*(scf.X2827==78)-scf.X2923*(scf.X2910==78)-scf.X2940*(scf.X2927==78))

    
    
##   business interests;
#*   for businesses where the HH has an active interest, value is net
#    equity if business were sold today, plus loans from HH to
#    business, minus loans from business to HH not previously
#    reported, plus value of personal assets used as collateral for
#    business loans that were reported earlier;
#*   for businesses where the HH does not have an active interest,
#    market value of the interest;
scf['BUS']=scf.X3129.combine(zero,max)+scf.X3124.combine(zero,max)-scf.X3126.combine(zero,max)*(scf.X3127==5)+\
        scf.X3121.combine(zero,max)*scf.X3122.isin([1,6])+\
        scf.X3229.combine(zero,max)+scf.X3224.combine(zero,max)-scf.X3226.combine(zero,max)*(scf.X3227==5)+\
        scf.X3221.combine(zero,max)*scf.X3222.isin([1,6])+\
        scf.X3335.combine(zero,max)+scf.FARMBUS+\
        scf.X3408.combine(zero,max)+scf.X3412.combine(zero,max)+scf.X3416.combine(zero,max)+\
        scf.X3420.combine(zero,max)+scf.X3452.combine(zero,max)+scf.X3428.combine(zero,max)
        
scf['ACTBUS']=scf.X3129.combine(zero,max)+scf.X3124.combine(zero,max)-scf.X3126.combine(zero,max)*(scf.X3127==5)+\
        scf.X3121.combine(zero,max)*scf.X3122.isin([1,6])+\
        scf.X3129.combine(zero,max)+scf.X3124.combine(zero,max)-scf.X3126.combine(zero,max)*(scf.X3127==5)+\
        scf.X3121.combine(zero,max)*scf.X3222.isin([1,6])+\
        scf.X3335.combine(zero,max)+scf.FARMBUS
        
scf['NONACTBUS']=scf.X3408.combine(zero,max)+scf.X3412.combine(zero,max)+scf.X3416.combine(zero,max)+\
    scf.X3420.combine(zero,max)+scf.X3452.combine(zero,max)+scf.X3428.combine(zero,max)
    
##   other nonfinancial assets
scf['OTHNFIN']=scf.X4022+scf.X4026+scf.X4030-scf.OTHFIN+scf.X4018
    
##   total nonfinancial assets;
scf['NFIN']=scf.VEHIC+scf.HOUSES+scf.ORESRE+scf.NNRESRE+scf.BUS+scf.OTHNFIN

################################ TOTAL ASSETS #################################
scf['ASSET']=scf.FIN+scf.NFIN
    
    
#################################### DEBTS ####################################
    
##   housing debt (mortgage, home equity loans and HELOCs --    mopup LOCs divided between HE and other)

#scf.HELOC=((scf.X1108+scf.X1119+scf.X1130)>=1)*(scf.X1108*(scf.X1103==1)+scf.X1119*(scf.X1114==1)+scf.X1130*(scf.X1125==1)\
#        +scf.X1136.combine(zero,max)*(scf.X1108*(scf.X1103==1)\
#        +scf.X1119*(scf.X1114==1)+scf.X1130*(scf.X1125==1))/(scf.X1108+scf.X1119+scf.X1130))
ADD = (scf.X1108*(scf.X1103==1)+scf.X1119*(scf.X1114==1)+scf.X1130*(scf.X1125==1)\
        +scf.X1136*(scf.X1136>=0)*(scf.X1108*(scf.X1103==1)\
        +scf.X1119*(scf.X1114==1)+scf.X1130*(scf.X1125==1))/(scf.X1108+scf.X1119+scf.X1130)).replace({np.NaN:0})
scf['MRTHEL']=scf.X805+scf.X905+scf.X1005+\
        ((scf.X1108+scf.X1119+scf.X1130)>=1)*ADD\
        +(~((scf.X1108+scf.X1119+scf.X1130)>=1))*(0.5*scf.X1136.combine(zero,max)*(scf.HOUSES>0))
    
#scf.NH_MORT=scf.MRTHEL-scf.HELOC
###   Home equity equals home value less all home secured debt (Maybe useful)
#scf.HOMEEQ=scf.HOUSES-scf.MRTHEL

##   debt for other residential property: includes land contracts,
##    residential property other than the principal residence, misc
##    vacation, and installment debt reported for cottage/vacation home
##    code 67); 
##   NOTE: debt for nonresidential real estate is netted out of the
#    corresponding assets; 
scf['MORT1']=(scf.X1703.isin([12,14,21,22,25,40,41,42,43,44,49,50,52,53,999]))*\
     scf.X1715*(scf.X1705/10000)
scf['MORT2']=(scf.X1803.isin([12,14,21,22,25,40,41,42,43,44,49,50,52,53,999]))*\
     scf.X1815*(scf.X1805/10000)
#*   JXB - in 2013 RESDBT, use 1318 for 1417, 1337 for 1517, 1342 for 1621;
scf['RESDBT']=scf.X1318+scf.X1337+scf.X1342+scf.MORT1+scf.MORT2+scf.X2006
#*   see note above at definition of NNRESRE;
scf['FLAG782']=((scf.FLAG781!=1) & (scf.ORESRE>0)).astype(int)
scf.RESDBT=scf.RESDBT+((scf.FLAG781!=1) & (scf.ORESRE>0))*(scf.X2723*(scf.X2710==78)+scf.X2740*(scf.X2727==78)\
       +scf.X2823*(scf.X2810==78)+scf.X2840*(scf.X2827==78)\
       +scf.X2923*(scf.X2910==78)+scf.X2940*(scf.X2927==78))

#    *   for parallel treatment, only inlcude PURPOSE=67 where
#    ORESRE>0--otherwise, treat as installment loan;
    
scf['FLAG67']=(scf.ORESRE>0).astype(int)
scf.RESDBT=scf.RESDBT+(scf.ORESRE>0)*(scf.X2723*(scf.X2710==67)+scf.X2740*(scf.X2727==67)\
       +scf.X2823*(scf.X2810==67)+scf.X2840*(scf.X2827==67)\
       +scf.X2923*(scf.X2910==67)+scf.X2940*(scf.X2927==67))


##   other lines of credit;
ADD = (scf.X1108*(scf.X1103!=1)+scf.X1119*(scf.X1114!=1)+scf.X1130*(scf.X1125!=1)+\
        scf.X1136*(scf.X1136>=0)*(scf.X1108*(scf.X1103!=1)+scf.X1119*(scf.X1114!=1)+\
        scf.X1130*(scf.X1125!=1))/(scf.X1108+scf.X1119+scf.X1130)).replace({np.NaN:0})
scf['OTHLOC']=((scf.X1108+scf.X1119+scf.X1130)>=1)*ADD+\
        ((scf.X1108+scf.X1119+scf.X1130)<1)*(((scf.HOUSES<=0)+.5*(scf.HOUSES>0))*scf.X1136*(scf.X1136>=0))
   

###   credit card debt;
#   NOTE: from 1992 forward, specific question addresses revolving
#    debt at stores, and this amount is treated as credit card debt here;
#   convenience use of credit cards - NOCCBAL, excludes charge
#   accounts at stores; 
scf['CCBAL']=scf.X427.combine(zero,max)+scf.X413.combine(zero,max)+scf.X421.combine(zero,max)\
    +scf.X430.combine(zero,max)+scf.X7575.combine(zero,max)

 
###   installment loans not classified elsewhere;
#   subdivide into vehicle loans, education loans, and other
#    installment loans;


scf['INSTALL']=scf.X2218+scf.X2318+scf.X2418+scf.X7169+scf.X2424+scf.X2519+scf.X2619+scf.X2625+scf.X7183\
        +scf.X7824+scf.X7847+scf.X7870+scf.X7924\
        +scf.X7947+scf.X7970+scf.X7179\
        +scf.X1044+scf.X1215+scf.X1219

#*   see notes above at definitions of NNRESRE and RESDBT;

scf.INSTALL=scf.INSTALL+((scf.FLAG781==0) & (scf.FLAG782==0))\
    *(scf.X2723*(scf.X2710==78)+scf.X2740*(scf.X2727==78)+scf.X2823*(scf.X2810==78)+scf.X2840*(scf.X2827==78)+scf.X2923*(scf.X2910==78)+scf.X2940*(scf.X2927==78))\
    +(scf.FLAG67==0)*(scf.X2723*(scf.X2710==67)+scf.X2740*(scf.X2727==67)+scf.X2823*(scf.X2810==67)+scf.X2840*(scf.X2827==67)+scf.X2923*(scf.X2910==67)+scf.X2940*(scf.X2927==67))

scf.INSTALL=scf.INSTALL+scf.X2723*(~scf.X2710.isin([67,78]))+scf.X2740*(~scf.X2727.isin([67,78]))+\
    scf.X2823*(~scf.X2810.isin([67,78]))+scf.X2840*(~scf.X2827.isin([67,78]))+\
    scf.X2923*(~scf.X2910.isin([67,78]))+scf.X2940*(~scf.X2927.isin([67,78]))


##   margin loans; 
#*   except in 1995, the SCF does not ask whether the margin loan
#    was reported earlier: the instruction explicitly excludes loans
#    reported earlier;

scf['OUTMARG']=scf.X3932.combine(zero,max)

scf['OUTPEN1']=scf.X11027.combine(zero,max)*(scf.X11070==5)
scf['OUTPEN2']=scf.X11127.combine(zero,max)*(scf.X11170==5)
scf['OUTPEN4']=scf.X11327.combine(zero,max)*(scf.X11370==5)
scf['OUTPEN5']=scf.X11427.combine(zero,max)*(scf.X11470==5)


###   other debts (loans against pensions, loans against life insurance,
#    margin loans, miscellaneous);
scf['ODEBT']=scf.OUTPEN1+scf.OUTPEN2+scf.OUTPEN4+scf.OUTPEN5\
      +scf.X4010.combine(zero,max)+scf.X4032.combine(zero,max)+scf.OUTMARG
    
################################# TOTAL DEBTS #################################
scf['DEBT']=scf.MRTHEL+scf.RESDBT+scf.OTHLOC+scf.CCBAL+scf.INSTALL+scf.ODEBT

############################### TOTAL NET WORTH ###############################
scf['NETWORTH']=scf.ASSET-scf.DEBT
    
###############################################################################
#                                   INCOME
###############################################################################
#   All income variables are before tax incomes
    
#   HH income in previous calendar year
#    NOTE: For 2004 forward, IRA and withdrawals from tax-deferred
#    pension accounts added to INCOME below
scf['INCOME']=scf.X5729.combine(zero,max)

######   HH income components in previous calendar year  ######

#   NOTE: Components of income may not sum to INCOME and in the public
#   data X5704/X5714/X5724 may have a value of -9 if X5729 was
#   negative and X5704/X5714/X5724 was also negative

#   income from wages and salaries
scf['WAGEINC']=scf.X5702   # IRS from 1040 line 7

#   income from a sole proprietorship or a farm
scf['SOLPFARMINC']=scf.X5704   # IRS from 1040 line 12,18

#   income from other businesses or investments, net rent, trusts, or royalties
scf['RENTINC']=scf.X5714    # IRS from 1040 line 17

scf['BUSSEFARMINC']=scf.X5704+scf.X5714

#   X5706: income from non-taxable investments such as municipal bonds: IRS from 1040 line 8b
#   X5708: income from other interest: IRS from 1040 line 8a
#   X5710: income from dividends: IRS from 1040 line 9a, 9b
scf['INTDIVINC']=scf.X5706+scf.X5708+scf.X5710

#   income from gains or losses from mutual funds or from the sale of stocks,
#                bonds, or real estate
scf['KGINC']=scf.X5712     # IRS from 1040 line 13, 14

#   income from Social Security or other pensions, annuities, or other
#               disability or retirement programs
scf['SSRETINC']=scf.X5722  # IRS from 1040 line 16a, 20a

#   X5716: income from unemployment or worker's compensation: IRS from 1040 line 19
#   X5718: income from child support or alimony: IRS from 1040 line 11
#   X5720: income from TANF, SNAP (food stamps), or other forms of welfare or
#                assistance such as SSI: Source?
#   X5724: income from any other sources (other than withdrawals from
#       account-type pensions or IRAs): IRS from 1040 line 10, 21
scf['TRANSFOTHINC']=scf.X5716+scf.X5718+scf.X5720+scf.X5724

#   for 2004 and beyond, add in the amount of withdrawals from IRAs
#    and tax-deferred pension accounts (already included in earlier
#    years). need to convert pension withdrawals to annual frequency
scf['PENACCTWD']=scf.X6558+scf.X6566+scf.X6574\
        +(scf.X6464*conv(scf.X6465)).combine(zero,max)\
        +(scf.X6469*conv(scf.X6470)).combine(zero,max)+(scf.X6474*conv(scf.X6475)).combine(zero,max)\
        +(scf.X6479*conv(scf.X6480)).combine(zero,max)+(scf.X6965*conv(scf.X6966)).combine(zero,max)\
        +(scf.X6971*conv(scf.X6972)).combine(zero,max)+(scf.X6977*conv(scf.X6978)).combine(zero,max)\
        +(scf.X6983*conv(scf.X6984)).combine(zero,max)
scf.INCOME=scf.INCOME+scf.PENACCTWD
scf.SSRETINC=scf.SSRETINC+scf.PENACCTWD

# NOTE: There are questions about whether this has been a normal year\
#  and if not what is the income in a normal year! I haven't included those!
###############################################################################
#                                   Earnings
###############################################################################


###############################################################################
#                              PRIVATE BUSINESSES
###############################################################################
scf['OWNPBUS']=(scf.X3103==1).astype(int)
scf['ACTMGT']=(scf.X3104==1).astype(int)
scf['BUSORG']=scf.X3119
#                     1.    *PARTNERSHIP
#                     2.    *SOLE-PROPRIETORSHIP
#                     3.    *SUBCHAPTER S
#                     4.    *OTHER CORPORATION (including C chapter corps)
#                     6.     Foreign business type
#                    11.    *LIMITED PARTNERSHIP/LLP
#                    12.    *LLC (LIMITED LIABILITY COMPANY) (include
#                            professional limited liability companies)
#                    15.     Cooperative
#                    40.     Not a formal business type
#                    -7.    *OTHER
#                     0.     Inap. (no businesses: X3103^=1; no actively managed
#                            businesses: X3104^=1/fewer than 2 actively managed
#                            businesses: X3105<2)

###############################################################################
df=scf[keep]
df.to_csv('scf.csv')