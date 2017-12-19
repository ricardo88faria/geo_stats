#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Jul 17 14:34:45 2017

@author: ricardofaria

Calculating confidence intervals for a linear regression

This script calculates and plots confidence intervals around a linear regression based on new observations. 
After I couldn’t find anything similar on the internet I developed my own implementation based on 
Statistics in Geography by David Ebdon (ISBN: 978-0631136880).
Based on with my own fixes: 
    1 - https://tomholderness.wordpress.com/2013/01/10/confidence_intervals 
    2 - https://github.com/KirstieJane/STATISTICS/blob/master/CIs_LinearRegression.py

"""



def lr_cl(x, y, units, output_file_name):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import t
    import scipy
    
    # R value
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)

    # fit a curve to the data using a least squares 1st order polynomial fit
    z = np.polyfit(x,y,1)
    p = np.poly1d(z)
    fit = p(x)
     
    # get the coordinates for the fit curve
#    c_x = [np.min(x),np.max(x)]
#    c_y = p(c_x)
     
    # predict y values of origional data using the fit
    p_y = z[0] * x + z[1]
     
    # calculate the y-error (residuals)
    y_err = y - fit
     
    # create series of new test x-values to predict for
    p_x = np.arange(np.min(x),np.max(x)+1,1)
     
    # now calculate confidence intervals for new test x-series
    c_limit = 0.975
    mean_x = np.mean(x)                 # mean of x
    n = len(x)                          # number of samples in origional fit
    tstat = t.ppf(c_limit, n-1)         # appropriate t value
    s_err = np.sum(np.power(y_err,2))   # sum of the squares of the residuals
     
    confs = tstat * np.sqrt((s_err/(n-2))*(1.0/n + (np.power((p_x-mean_x),2)/
                                    ((np.sum(np.power(x,2)))-n*(np.power(mean_x,2))))))
     
    # now predict y based on test x-values
    p_y = p(p_x) #z[0] * p_x + z[1]
     
    # get lower and upper confidence limits based on predicted y and confidence intervals
    lower = p_y - abs(confs)
    upper = p_y + abs(confs)
     
    # set-up the plot
    plt.figure(figsize=(10,10))
    #plt.axes().set_aspect('equal')
    plt.xlabel('Measurements [' + units + ']')
    plt.ylabel('Model [' + units + ']') # Bias (%)    IGH ($w/m^2$)
    plt.title('Linear regression and confidence limits')
     
    # plot sample data
    #for i in range(0,len(colors)) :
    #    plt.plot(x[i], y[i], 'ro', label = labels[i], color = colors[i])
    plt.plot(x,y,'bo',label='Sample observations')
     
    # plot line of best fit
    plt.plot(p_x,p_y,"r-",label='Regression line y=' + str(round(z[0], 3)) + 'x+' + str(round(z[1], 3)) + '    $R^2$=' + str(round(r_value**2, 3)))
    
    # plot y = x line
    yx = np.linspace(-1000,1000, 10)
    plt.plot(yx, yx, color = 'k',label='y=x')
    
    # plot confidence limits
    plt.plot(p_x,lower,'b--',label='Lower confidence limit (95%)')
    plt.plot(p_x,upper,'b--',label='Upper confidence limit (95%)')
     
    # set coordinate limits may be problematic!!!! if so comment
    plt.xlim(min(x) - (max(x)-min(x))/10, max(x) + (max(x)-min(x))/10)  # min(x) - (max(x)-min(x))/10, max(x) + (max(x)-min(x))/10
    plt.ylim(min(y) - (max(y)-min(y))/10, max(y) + (max(y)-min(y))/10)
     
    # configure legend
    plt.legend(loc=0, ncol=2)
    leg = plt.gca().get_legend()
    leg.get_frame().set_alpha(0)
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=6)
     
    # show the plot
    #plt.show()
    plt.savefig(output_file_name, format = 'png', dpi = 150, bbox_inches = 'tight')