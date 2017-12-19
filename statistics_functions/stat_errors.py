#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Mon May  8 10:54:18 2017

@author: ricardofaria

version 1.0

Calc the statistical errors betewen 2 dataframe tables measured & modelated with the same len, calculated:
    Pearson correlation coefficients (R);
    Root Mean Squared Error (RMSE);
    Mean Squared Error (MSE);
    Mean Absolute Error (MAE);
    Mean Forecast Error (Bias);
    Residual error measured-model.


rmse(measured, modelated)

Note:   For wind direction values must be betwen 0 and 360.
        The used method is Cyclic kernel (DOI: 10.1175/WAF-D-14-00006.1):

            min(b - a, a + 360 - b)

"""


def rmse(modelated, measured, wind_direction):

    import pandas as pd
    import numpy as np
    from collections import OrderedDict
    from scipy import stats
    import direction_average as dir_avg


    # create table for calc
    calc_tab = pd.DataFrame(OrderedDict({'modelated':modelated, 'measured':measured}))
    #calc_tab = pd.DataFrame(OrderedDict({'modelated':np.array([-.5,0,.5]), 'measured':np.array([-.1,0,.1])}))
    #calc_tab = pd.DataFrame(OrderedDict({'measured':err_tab.dd_med, 'modelated':err_tab.wrf_wind_dir}))
    # Residual error measured-model
    if wind_direction == True :
        calc_tab.iloc[:,0][calc_tab.iloc[:,0] == 0] = 360
        calc_tab.iloc[:,1][calc_tab.iloc[:,1] == 0] = 360

    # N
    N = len(calc_tab.iloc[:,0])

    if wind_direction == True :

        dir_err1 = calc_tab.iloc[:,0] - calc_tab.iloc[:,1]
        dir_err2 = calc_tab.iloc[:,1] + 360 - calc_tab.iloc[:,0]

        dir_err1[(dir_err1 >= 180)] = dir_err2[(dir_err1 >= 180)]
        dir_err1[(dir_err1 <= -180)] = dir_err1[(dir_err1 <= -180)] + 360

        calc_tab['mod-med'] = dir_err1
        #calc_tab['mod-med'] = 100*calc_tab['mod-med']/calc_tab.iloc[:,1]

    else :
        calc_tab['mod-med'] = calc_tab.iloc[:,0] - calc_tab.iloc[:,1]
        #calc_tab['mod-med'] = 100*calc_tab['mod-med']/calc_tab.iloc[:,1]

    # Mean Forecast Error (Bias)
    if wind_direction == True :
        bias = dir_avg.dir_avg(np.array(calc_tab['mod-med']))
    else :
        bias = np.mean(calc_tab['mod-med'])
    #mean_forecast_error = 100*sum(calc_tab['mod-med'])/sum(calc_tab.iloc[:,1])
    #mean_forecast_error_perc = np.mean(calc_tab['mod-med_perc'])

    # Mean Absolute Error (MAE)
    if wind_direction == True :
        mae = dir_avg.dir_avg(np.array(np.abs(calc_tab['mod-med'])))  #mean_absolute_error = np.absolute(mean_forecast_error) #np.mean(np.absolute(calc_tab['mod-med']))
    else :
        mae = np.mean(np.abs(calc_tab['mod-med']))
    #mean_absolute_error_perc = np.absolute(mean_forecast_error_perc) #np.mean(np.absolute(calc_tab['mod-med_perc']))

    # Mean Squared Error (MSE)
    if wind_direction == True :
        mse = dir_avg.dir_avg(np.array((calc_tab['mod-med'])**2)) #/len(calc_tab['mod-med']) #np.mean((calc_tab['mod-med'])**2)
    else :
        mse = np.mean((calc_tab['mod-med'])**2)
    #mean_squared_error_perc = mean_forecast_error_perc**2 #np.mean((calc_tab['mod-med_perc'])**2)

    # Root Mean Squared Error (RMSE)
    if wind_direction == True :
        rmse =  np.sqrt(dir_avg.dir_avg(np.array((calc_tab['mod-med'])**2))) #mean_squared_error**(1/2) #np.sqrt(mean_squared_error)
    else :
        rmse =  np.sqrt(np.mean((calc_tab['mod-med'])**2))
    #rmse_perc = mean_squared_error_perc**(1/2) #np.sqrt(mean_squared_error)

    # Pearson product-moment correlation coefficients
#    r = np.corrcoef(calc_tab.iloc[:,0],calc_tab.iloc[:,1])
#    r = r[0,1]
    r = stats.pearsonr(calc_tab.iloc[:,0],calc_tab.iloc[:,1])
    r = r[0]

    stat_table = pd.DataFrame(OrderedDict({'N':N, 'Bias':bias, 'MAE':mae, 'MSE':mse, 'RMSE':rmse, 'R':r}), index=[0]) #[mean_forecast_error, mean_absolute_error, mean_absolute_error, rmse] #pd.DataFrame({'Bias':mean_forecast_error, 'MAE':mean_absolute_error, 'MSE':mean_squared_error, 'RMSE':rmse}, index=[0])

    return stat_table
