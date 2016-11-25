# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root


omega=0.5
varphi=0.5
rho=0
varrho=1.0
theta=1.0/3
nu=1.0/3
delta=0.1
beta=0.98
A=1
Z=1


k_c=theta/(1/beta-1+delta)

def res(k_s):
    ratio_yterm_num=1-delta*k_c
    inner_term=(nu*(1-omega)/omega)*(k_c/k_s)
    ratio_yterm_den=1+delta*k_s*((inner_term)**(1/(1-rho)))
    ratio_yterm=(ratio_yterm_num/ratio_yterm_den)**(varrho-1)
    
    constants=(omega*(1-theta)*(1-varphi))/((1-omega)*(1-nu)*varphi)
    labor_term_s=(Z*(k_s**nu))**(-1/(1-nu))
    labor_term_c=(A*(k_c**theta))**(-1/(1-theta))
    labor_term=(labor_term_s/labor_term_c)**(varrho)
    capital_term_s=k_s*omega/nu
    capital_term_c=k_c*(1-omega)/theta
    capital_term=(capital_term_s/capital_term_c)**((varrho-rho)/(rho-1))
    res=constants*labor_term*capital_term*ratio_yterm-1
    return res
    
    
    


sol=root(res,k_c)    
if not sol.success:
    raise Exception('Could not find root!')
else:
    k_s=sol.x
    print ('The price, p = {}'.format((theta*k_s)/(nu*k_c)))
