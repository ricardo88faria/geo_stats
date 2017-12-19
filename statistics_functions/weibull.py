#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 12:11:05 2017

@author: ricardofaria

weibul function from example:
    https://docs.scipy.org/doc/numpy-1.6.0/reference/generated/numpy-random-weibull-1.py
    https://github.com/cqcn1991/Wind-Speed-Analysis
    https://github.com/cqcn1991/Wind-Speed-Analysis/blob/master/helpers/app_helper.py
    https://cdn.rawgit.com/cqcn1991/Wind-Speed-Analysis/master/output_HTML/hongqiao_intl.html

NREL (Reference Manual for the System Advisor Model’s Wind Power Performance Model):
    Rayleigh wind speed distribution (Rayleigh): Another commonly-used probability distribution function for wind resource analysis. The Weibull and Rayleigh distributions are the same when k = 2.


example of use:
    df_speed = np.random.weibull(1,1000)
    count, bins, ignored = plt.hist(df_speed, bins=30, normed=True)
    x, y_weibull, density_expected_weibull, y_cdf_weibull, weibull_params, y_ecdf = fit_weibull_and_ecdf(df_speed)
    plt.plot(x, y_weibull, '-', color='black',label='Weibull')

"""


import numpy as np


def fit_weibull(df_speed, x, weibull_params = None):

    from scipy.stats import weibull_min

    if not weibull_params:

        k_shape, _, lamb_scale = weibull_params = weibull_min.fit(df_speed, loc=0)

    y_weibull = weibull_min.pdf(x, *weibull_params)
    density_expected_weibull = weibull_min.cdf(x[1:], *weibull_params) - weibull_min.cdf(x[:-1], *weibull_params)
    y_cdf_weibull = 1 - np.exp(-(x / lamb_scale) ** k_shape)

    return weibull_params, y_weibull, density_expected_weibull, y_cdf_weibull



def fit_weibull_and_ecdf(df_speed, x = None):

    from statsmodels.distributions.empirical_distribution import ECDF

    max_speed = df_speed.max()
    if x is None:

        x = np.linspace(0, max_speed, 100)

    # Fit Weibull, notice loc value 0 or not
    weibull_params, y_weibull, density_expected_weibull, y_cdf_weibull = fit_weibull(df_speed, x)
    # Fit Ecdf
    y_ecdf = ECDF(df_speed)(x)

    return x, y_weibull, density_expected_weibull, y_cdf_weibull, weibull_params, y_ecdf
