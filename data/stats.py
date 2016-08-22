# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:54:07 2016

Calculates the statistics using the weights.

@author: Mohammad
"""
def mean(series, weights):
    return (series*weights).sum()/weights.sum()

def variance(series, weights):
    var = mean((series-mean(series, weights))**2, weights)
    return var
    
def variation(series, weights): 
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