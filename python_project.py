#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:12:23 2020

@author: elizabethboroda
"""


#-----------------------------------------------------------------------------------------------#
# FILE: project4.py									#
# PURPOSE: Analyze eddy flux data from Harvard Forest						#
#												#
#-----------------------------------------------------------------------------------------------#


#----------#
# Notes:   #
#----------#


#----------------------#        

# Required libraries   #
#----------------------#
import numpy as np
import matplotlib.pyplot as plt

#---------------------------#
# FUNCTION: summarizedata   #
#---------------------------#

def summarizedata(filename):
    
    # Purpose:
    #	Create a plot of the CO2 data as a time series
    #	Find the mean, median, and standard deviation of the data
    #	Plot a histogram of the data
    
    # Read in data from the Harvard Forest
    
    #gets all data into one big array called data
    data = np.genfromtxt(filename,delimiter=',', skip_header=1)
    

    # Create a time series plot of the data
    
    
    co2Vals = data[:, 3]
    years = data[:, 0]
    plt.plot(years + data[:,2]/365, co2Vals, '.')
    plt.axis([1992, 2009, -10, 6])
    plt.xlabel("Time")
    plt.ylabel("Co2")
    plt.title("Co2 Flux Data")
    
    3
    # Display the plot
    #plt.show()
    plt.figure()
    
    toReturn = []
    # Find the mean of the data
    mean = np.mean(co2Vals)
    toReturn.append(mean)
    # Find the median of the data
    median = np.median(co2Vals)
    toReturn.append(median)

    # Find the standard deviation of the data
    standardDev = np.std(co2Vals)
    toReturn.append(standardDev)
    # Plot a histogram of the data
    plt.hist(co2Vals, bins=20, density=True)
    plt.xlabel("Co2 Flux Values")
    plt.ylabel("Frequency of Co2 Data (as a decimal)")
    plt.title("Histogram of Co2 Flux Data")

    # Display the plot
    #plt.show()
    plt.figure()
    
    # Return the mean, median, and standard deviation
    return toReturn
    
#---------------------------#
# FUNCTION: missingdata     #
#---------------------------#

def missingdata(filename):
    
    # Purpose: 
    # 	Find the number of missing data points in each year
    
    # Read in the data from the Harvard Forest
    #gets all data into one big array called data
    data = np.genfromtxt(filename,delimiter=',', skip_header=1)

    '''
    
    np.where : find all matching values in rows ie np.where(years == 1992)
    '''
    
    # Find the number of missing data points in each year
    years = data[:,0]
    minyear = int(np.min(years))
    maxyear = int(np.max(years))
    year = range(minyear, maxyear+1)
    
    leapYears = []
    
    for i in range(len(year)):
        if year[i] % 4 == 0: 
            leapYear = year[i]
            leapYears.append(leapYear)
    
    
    daysPerYear = []
    for i in range(len(year)):
        if year[i] in years: 
            days = np.where(data[:,0] == year[i])[0]
            
            daysPerYear.append(len(days))
        else: 
            daysPerYear.append(0)
             
    
    missing = []
    for i in range(len(year)):
        if year[i] in leapYears: 
            missingYearly = 366 - daysPerYear[i]
        else: 
            missingYearly = 365 - daysPerYear[i]
        missing.append(missingYearly)

    # Return the result
    return missing


#---------------------------#
# FUNCTION: seasonalcycle   #
#---------------------------#

def seasonalcycle(filename):

    # Purpose: 
    # 	Find the average flux by month (averaged over all years)
    #	Plot the average monthly flux to visualize the seasonal cycle

    # Read in the data from the Harvard Forest
    data = np.genfromtxt(filename,delimiter=',', skip_header=1)
    
    # Find the average CO2 flux by month
    co2 = data[:,3]
    month = data[:, 1]
    monthlyAvgs = []
    count = 0
    while count != 12:
        count = count + 1
        monthlyAvg = np.mean(co2[month==count])
        monthlyAvgs.append(monthlyAvg)
    
    # Plot the average CO2 flux by month
    
    plt.plot(range(1,13),monthlyAvgs)
    
    plt.xlabel("Month")
    plt.ylabel("Carbon Dioxide Average Values")
    plt.title("Average CO2 Flux Values By Month")
    #plt.show()
    plt.figure()

    # Return the result
    return monthlyAvgs


#---------------------------#
# FUNCTION: HFregression    #
#---------------------------#
def HFregression(filename):
	
    # Purpose: 
        #    Create a regression model for CO2 fluxes
        #    Visualize the outputs of the model

    # Read in the data from the Harvard Forest
    data = np.genfromtxt(filename,delimiter=',', skip_header=1)
    length = len(data)
    # Create the X matrix for the regression
    ones = np.ones((length, 1))
    x_matrix = np.column_stack((ones, data[:, 4:8]))
    
    
    # Estimate the regression coefficients
    
    transposeX = x_matrix.transpose()
    toBeInversed = transposeX@x_matrix
    inverse = np.linalg.inv(toBeInversed)
    step4 = inverse@transposeX
    regCo = step4@data[:,3]
    

    # Create the model estimate
    predictingCo2 = x_matrix@regCo
    
    co2Vals = data[:, 3]
    years = data[:, 0]
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(years + data[:,2]/365, co2Vals, label='given data')
    plt.plot(years+data[:,2]/365, predictingCo2, label='modeled data')
    plt.axis([1992, 2009, -10, 6])
    plt.xlabel("Time")
    plt.ylabel("Co2")
    plt.title("Co2 Flux Data")
    plt.legend()
    
    
    # Calculate the correlation coefficient
    corCo = np.corrcoef(co2Vals, predictingCo2)[0,1]
    stringCorCo = str(corCo)
    plt.text(1994,-9,stringCorCo)
    plt.annotate("Correlation Coefficient:", (1994, -8))
    
    
    
    
    
    # Create a plot of the model components
    interceptData = x_matrix[:,0]*regCo[0]
    netRad = x_matrix[:,1]*regCo[1]
    airTemp = x_matrix[:,2]*regCo[2]
    waterVapor = x_matrix[:,3]*regCo[3]
    windSpd = x_matrix[:,4]*regCo[4]
    
    plt.subplot(2, 1, 2)
    plt.plot(years + data[:,2]/365, interceptData, label='intercept data')
    plt.plot(years + data[:,2]/365, netRad, label='net radiation')
    plt.plot(years + data[:,2]/365, airTemp, label='air temperature')
    plt.plot(years + data[:,2]/365, waterVapor, label='water vapor')
    plt.plot(years + data[:,2]/365, windSpd, label='wind speed')
    plt.xlabel("Time")
    plt.ylabel("Co2 Flux")
    plt.title("Different Model Components")
    plt.legend()
    
    # Display the plot
    #plt.show()
    plt.figure()

    # Return the regression coefficients 
    return regCo


#-----------------------------------------#
# Execute the functions defined above     #
#-----------------------------------------#


if __name__ == "__main__": 
    from IPython import get_ipython
    get_ipython().run_line_magic('matplotlib', 'auto') 
    plt.close('all')
    filename            = 'harvard_forest.csv'
    hfmean, hfmed, hfsd = summarizedata(filename)
    missing_data        = missingdata(filename)
    month_means         = seasonalcycle(filename)
    betas               = HFregression(filename)


#-----------------------------------------------------------------------------------------------#
# END OF SCRIPT
#-----------------------------------------------------------------------------------------------#
