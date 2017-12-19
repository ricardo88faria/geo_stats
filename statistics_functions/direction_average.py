#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Fri Nov  3 14:24:41 2017

@author: ricardofaria

Wind direction average calc:
    x = y = 0
    foreach angle {
        x += cos(angle)
        y += sin(angle)
    }
    average_angle = atan2(y, x)

input must be numpy array

"""


def dir_avg(tab):

    import numpy as np
    import math

    x, y = [], []
    for i in range(0, len(tab)) :
        x.append(math.cos(tab[i] * math.pi / 180.0))
        y.append(math.sin(tab[i] * math.pi / 180.0))

    average_angle = math.atan2(np.average(np.array(y)), np.average(np.array(x))) * 180 / math.pi

    if average_angle < 0 :
        average_angle = average_angle + 360

    return average_angle
