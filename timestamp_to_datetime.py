#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:18:34 2017

@author: ricardofaria

Transform pandas Timestamp to datetime.datetime

"""

def timestamp_to_datetime(x):
    y_stat_data = []
    for dt in range(len(x)):
        y_stat_data.append(x[dt].to_pydatetime())
        #print(dt + ':' + len(x))
    
    return y_stat_data