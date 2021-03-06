# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:54:07 2016

Calculates the statistics using the weights.

@author: Mohammad
"""

import numpy as np
import pandas as pd
def mean(series, weights):
    return (series*weights).sum()/weights.sum()

def variance(series, weights):
    var = mean((series-mean(series, weights))**2, weights)
    return var
    
def coeff_variation(series, weights): 
    return variance(series, weights)**.5 / mean(series, weights)
    
def quant(series, weights, quantile):
    if series.size!=weights.size:
        print("Weights are not the same size as the series")
        return
    sorted_series = series.sort_values()
    if quantile==1:
        return sorted_series.iloc[-1]
    threshold = quantile* weights.sum()
    s, i = 0, 0
    while ((s<threshold) & (i<series.size)):
        s += weights[sorted_series.index[i]]
        i+=1
    return series[sorted_series.index[i]]
    
def gini(series, weights):
    if series.size!=weights.size:
        print("Weights are not the same size as the series")
        return
    sorted_series = series.sort_values()
    height, area = 0, 0
    for i in range(series.size):
        value = series[sorted_series.index[i]]
        wgt = weights[sorted_series.index[i]]
        height += wgt*value
        area += wgt*(height - value / 2)
    fair_area = height * weights.sum() / 2.
    return (fair_area - area) / fair_area


def loc(series, weights, a):
    sorted_series = series.sort_values()
    i, s = 0, 0
    while series[sorted_series.index[i]]<a:
        s += weights[sorted_series.index[i]]
        i +=1
    while series[sorted_series.index[i]]<=a:
        s += weights[sorted_series.index[i]]/2
        i +=1
    return s/weights.sum()
    
        
def quantile_1D(data, weights, quantile):
    """
    Compute the weighted quantile of a 1D numpy array.
    Parameters
    ----------
    data : ndarray
        Input array (one dimension).
    weights : ndarray
        Array with the weights of the same size of `data`.
    quantile : float
        Quantile to compute. It must have a value between 0 and 1.
    Returns
    -------
    quantile_1D : float
        The output value.
    """
    # Check the data
    if not isinstance(data, np.matrix):
        data = np.asarray(data)
    if not isinstance(weights, np.matrix):
        weights = np.asarray(weights)
    nd = data.ndim
    if nd != 1:
        raise TypeError("data must be a one dimensional array")
    ndw = weights.ndim
    if ndw != 1:
        raise TypeError("weights must be a one dimensional array")
    if data.shape != weights.shape:
        raise TypeError("the length of data and weights must be the same")
    if ((quantile > 1.) or (quantile < 0.)):
        raise ValueError("quantile must have a value between 0. and 1.")
    # Sort the data
    ind_sorted = np.argsort(data)
    sorted_data = data[ind_sorted]
    sorted_weights = weights[ind_sorted]
    # Compute the auxiliary arrays
    Sn = np.cumsum(sorted_weights)
    # TODO: Check that the weights do not sum zero
    #assert Sn != 0, "The sum of the weights must not be zero"
    Pn = (Sn-0.5*sorted_weights)/np.sum(sorted_weights)
    # Get the value of the weighted median
    return np.interp(quantile, Pn, sorted_data)



def describe(data,weights):
    s= np.zeros(8)
    s[0]=coeff_variation(data, weights)
    s[1]=variance(np.log(data[(data>0)]),weights[(data>0)])
    s[2]=gini(data, weights)

    s[3]=loc(data, weights, mean(data, weights))
    s[4]=quantile_1D(data, weights, .99)/quantile_1D(data, weights, .5)
    s[5]=quantile_1D(data, weights, .9)/quantile_1D(data, weights, .5)
    s[6]=mean(data, weights)/quantile_1D(data, weights, .5)
    s[7]=quantile_1D(data, weights, .5)/quantile_1D(data, weights, .3)
    moments=['Coefficient of variation','Variance of logs',\
     'Gini indexes','Location of mean','99-50 ratio', '90-50 ratio', 'Mean-to-median ratio',\
     '50-30 ratio']
     
    return_data=pd.DataFrame(s,index=moments)
    return return_data
    