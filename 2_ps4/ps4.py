# -*- coding: utf-8 -*-
# 6.100B Spring 2023
# Problem Set 4: Sea Level Rise
# Name: Vivian Hir 
# Collaborators: None 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import scipy.stats as st
from scipy.interpolate import interp1d

#####################
# Begin helper code #
#####################

def calculate_std(upper, mean):
    """
	Calculate standard deviation based on the upper 97.5th percentile

	Args:
		upper: a 1-d numpy array with length N, representing the 97.5th percentile
            values from N data points
		mean: a 1-d numpy array with length N, representing the mean values from
            the corresponding N data points

	Returns:
		a 1-d numpy array of length N, with the standard deviation corresponding
        to each value in upper and mean
	"""
    return (upper - mean) / st.norm.ppf(.975)

def load_data():
    """
	Loads data from sea_level_change.csv and puts it into numpy arrays

	Returns:
		a length 3 tuple of 1-d numpy arrays:
		    1. an array of years as ints
		    2. an array of 2.5th percentile sea level rises (as floats) for the years from the first array
		    3. an array of 97.5th percentile of sea level rises (as floats) for the years from the first array
        eg.
            (
                [2020, 2030, ..., 2100],
                [3.9, 4.1, ..., 5.4],
                [4.4, 4.8, ..., 10]
            )
            can be interpreted as:
                for the year 2020, the 2.5th percentile SLR is 3.9ft, and the 97.5th percentile would be 4.4ft.
	"""
    df = pd.read_csv('sea_level_change.csv')
    df.columns = ['Year', 'Lower', 'Upper']
    return (df.Year.to_numpy(), df.Lower.to_numpy(), df.Upper.to_numpy())


###################
# End helper code #
###################


##########
# Part 1 #
##########

def predicted_sea_level_rise(show_plot=False):
    """
	Creates a numpy array from the data in sea_level_change.csv where each row
    contains a year, the mean sea level rise for that year, the 2.5th percentile
    sea level rise for that year, the 97.5th percentile sea level rise for that
    year, and the standard deviation of the sea level rise for that year. If
    the year is between 2020 and 2100, inclusive, and not included in the data, 
    the values for that year should be interpolated. If show_plot, displays a 
    plot with mean and the 95% confidence interval, assuming sea level rise 
    follows a linear trend.

	Args:
		show_plot: displays desired plot if true

	Returns:
		a 2-d numpy array with each row containing the year, the mean, the 2.5th 
        percentile, 97.5th percentile, and standard deviation of the sea level rise
        for the years between 2020-2100 inclusive
	"""
    numpy_array=load_data() 
    years=numpy_array[0]
    lower=numpy_array[1]
    higher=numpy_array[2]
    mean=np.zeros(len(higher)) 

    for i in range (len(higher)):
        value=(higher[i]+lower[i])/2
        mean[i]=value
    new_array=[]
    std_dev=calculate_std(higher, mean)

    #iterate years through 2020 and 2100 
    #if the year is already part you don't need to interpolate 
    #else do the function 
    for i in range(2020, 2101):
        if i in years: 
            new_array.append([i, mean[(i-2020)//10], lower[(i-2020)//10], higher[(i-2020)//10], std_dev[(i-2020)//10]])
            
        else: 
            interpolate_slow=interp1d(years, lower)
            lower_interp=interpolate_slow(i)
            interpolate_fast=interp1d(years, higher)
            higher_interp=interpolate_fast(i) #did I return functions and then have to take in the input to get new values? 
            mean_interp=(lower_interp+higher_interp)/2
            std_dev_interp=calculate_std(higher_interp, mean_interp)
            new_array.append([i, mean_interp, lower_interp, higher_interp, std_dev_interp])
    numpy_array=np.array(new_array)
    if show_plot==True: 
        years=range(2020, 2101)
        upper_level=[]
        lower_level=[]
        mean_level=[]
        for year in years: 
            upper_level.append(numpy_array[year-2020][3])
            lower_level.append(numpy_array[year-2020][2])
            mean_level.append(numpy_array[year-2020][1])
        plt.plot(years, upper_level, linestyle='dashed')
        plt.plot(years, lower_level, linestyle='dashed')
        plt.plot(years, mean_level)
        plt.title('Projected Sea Level Rise from 2020 to 2100')
        plt.legend(('Upper', 'Lower', 'Mean'))
        plt.xlabel('Year')
        plt.ylabel('Projected annual mean water level (ft)')
        plt.show() 
    else:
        return numpy_array 

def simulate_year(data, year, num):
    """
	Simulates the sea level rise for a particular year based on that year's
    mean and standard deviation, assuming a normal distribution. 

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2020-2100
            inclusive, mean, the 2.5th percentile, 97.5th percentile, and standard
            deviation of the sea level rise for the given year
		year: the year to simulate sea level rise for
        num: the number of samples you want from this year

	Returns:
		a 1-d numpy array of length num, that contains num simulated values for
        sea level rise during the year specified
	"""
    index=(year-2020)
    #simulate for a particular year, year correspond to the index 
    mean=data[index][1]
    std_dev=data[index][4]
    numpy_array=np.random.normal(mean, std_dev, num)
    return numpy_array
    
    
def plot_simulation(data):
    """
	Runs and plots a Monte Carlo simulation, based on the values in data and
    assuming a normal distribution. Five hundred samples should be generated
    for each year.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2020-2100
            inclusive, mean, the 2.5th percentile, 97.5th percentile, and standard
            deviation of the sea level rise for the given year
	"""
    num=500
    upper_level=[]
    lower_level=[]
    mean_level=[]
    years=range(2020, 2101)
    #do I need to copy the plot commands from the first function or do I just call it? 
    for year in years: 
        simulated_rise=simulate_year(data, year, num)
        year_list=np.array([year]*num)
        plt.scatter(year_list, simulated_rise, s= 0.25, c='gray') #you can input arrays as x and y not points 
        #points will take forever to graph 
    for year in years:
        upper_level.append(data[year-2020][3])
        lower_level.append(data[year-2020][2])
        mean_level.append(data[year-2020][1])
    plt.plot(years, upper_level, linestyle='dashed', label='Upper bound')
    plt.plot(years, lower_level, linestyle='dashed', label='Lower bound')
    plt.plot(years, mean_level, label='Mean') #need to write label so legend knows what to plot 
    plt.title('Monte-Carlo Sea Level Rise Data')
    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Relative water level change (ft)')
    
    plt.show() 
    

##########
# Part 2 #
##########

def simulate_water_levels(data):
    """
	Simulates the water level for all years in the range 2020 to 2100, inclusive.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2020-2100
            inclusive, mean, the 2.5th percentile, 97.5th percentile, and standard
            deviation of the sea level rise for the given year

	Returns:
		a python list of simulated water levels for each year, in the order in which
        they would occur temporally
	"""
    years=range(2020, 2101)
    simulated_list=[]
    for year in years: 
        simulated_data=simulate_year(data, year, 1)
        simulated_list.append(simulated_data)
    return simulated_list


def repair_only(water_level_list, water_level_loss_no_prevention, house_value=400000):
    """
	Simulates the water level for all years in the range 2020 to 2100, inclusive,
    and calculates damage costs in 1000s resulting from a particular water level
    for each year dependent on a repair only strategy, where you would only pay
    to repair damage that already happened.

    The specific damage cost can be calculated using the numpy array
    water_level_loss_no_prevention, where each water level corresponds to the
    percent of property that is damaged.

    The repair only strategy is as follows:
        1) If the water level is less than or equal to 5ft, the cost is 0.
        2) If the water level is between 5ft and 10ft (exclusive), the cost is the
           house_value times the percentage of property damage for that water
           level. If the water level is not an integer value, the percentage
           should be interpolated.
        3) If the water level is at least 10ft, the cost is the entire value of
           the house.

	Args:
		water_level_list: list of simulated water levels for 2020-2100
        water_level_loss_no_prevention: a 2-d numpy array where the first column is
            the SLR levels and the second column is the corresponding property damage expected
            from that water level with no flood prevention (as an integer percentage)
        house_value: the value of the property we are estimating cost for

	Returns:
		a python list of damage costs in 1000s, in the order in which the costs would
        be incurred temporally
	"""
    
    cost_list=[]
    for water_level in water_level_list: 
        if water_level<=5: 
            cost=0
        elif water_level>5 and water_level<10:
            if isinstance(water_level, int):
                for i in range(water_level_loss_no_prevention[:,0]):
                    if water_level_loss_no_prevention[i][0]==water_level:
                        percent=water_level_loss_no_prevention[i][1]*0.01 
                cost=percent*house_value/1000
            else: 
                function=interp1d(water_level_loss_no_prevention[:,0], water_level_loss_no_prevention[:,1]*0.01, fill_value='extrapolate')
                cost=float(function(water_level))*house_value/1000
        else:
            cost=house_value/1000
        cost_list.append(cost)
    return cost_list


def wait_a_bit(water_level_list, water_level_loss_no_prevention, water_level_loss_with_prevention, house_value=400000,
               cost_threshold=100000):
    """
	Simulates the water level for all years in the range 2020 to 2100, inclusive,
    and calculates damage costs in 1000s resulting from a particular water level
    for each year dependent on a wait a bit to repair strategy, where you start
    flood prevention measures after having a year with an excessive amount of
    damage cost.

    The specific damage cost can be calculated using the numpy array
    water_level_loss_no_prevention and water_level_loss_with_prevention, where
    each water level corresponds to the percent of property that is damaged.
    You should be using water_level_loss_no_prevention when no flood prevention
    measures are in place, and water_level_loss_with_prevention when there are
    flood prevention measures in place.

    Flood prevention measures are put into place if you have any year with a
    damage cost above the cost_threshold.

    The wait a bit to repair only strategy is as follows:
        1) If the water level is less than or equal to 5ft, the cost is 0.
        2) If the water level is between 5ft and 10ft (exclusive), the cost is the
           house_value times the percentage of property damage for that water
           level, which is affected by the implementation of flood prevention
           measures. If the water level is not an integer value, the percentage
           should be interpolated.
        3) If the water level is at least 10ft, the cost is the entire value of
           the house.

	Args:
		water_level_list: list of simulated water levels for 2020-2100
        water_level_loss_no_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with no flood prevention
        water_level_loss_with_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with flood prevention
        house_value: the value of the property we are estimating cost for
        cost_threshold: the amount of cost incurred before flood prevention
            measures are put into place

	Returns:
		an list of damage costs in 1000s, in the order in which the costs would
        be incurred temporally
	"""
    #for the investment don't you need to add the extra money to the total cost??? 
    #start off no prevention then at some point will exceed cost threshold 
    #year where too much damage to the house 
    #every single year afterwards you will be prepared then ultimately will have a lowered cost 
    cost_list=[]
    prevention=False 
    for water_level in water_level_list: 
        if water_level<=5: 
            cost=0
        elif water_level>5 and water_level<10:
            if not prevention: 
                if isinstance(water_level, int):
                    for i in range(water_level_loss_no_prevention[:,0]):
                        if water_level_loss_no_prevention[i][0]==water_level:
                            percent=water_level_loss_no_prevention[i][1]*0.01 
                    cost=percent*house_value/1000
                else: 
                    function=interp1d(water_level_loss_no_prevention[:,0], water_level_loss_no_prevention[:,1]*0.01, fill_value='extrapolate')
                    cost=float(function(water_level))*house_value/1000
            if prevention:
                if isinstance(water_level, int):
                    for i in range(water_level_loss_with_prevention[:,0]):
                        if water_level_loss_with_prevention[i][0]==water_level:
                            percent=water_level_loss_with_prevention[i][1]*0.01 
                    cost=percent*house_value/1000
                else: 
                    function=interp1d(water_level_loss_with_prevention[:,0], water_level_loss_with_prevention[:,1]*0.01, fill_value='extrapolate')
                    cost=float(function(water_level))*house_value/1000
        else:
            cost=house_value/1000
        if cost>cost_threshold/1000:
            prevention=True #check before appending so that next iteration will not go through the wrong if statement 
        cost_list.append(cost)
    return cost_list



def prepare_immediately(water_level_list, water_level_loss_with_prevention, house_value=400000):
    """
	Simulates the water level for all years in the range 2020 to 2100, inclusive,
    and calculates damage costs in 1000s resulting from a particular water level
    for each year dependent on a prepare immediately strategy, where you start
    flood prevention measures immediately.

    The specific damage cost can be calculated using the numpy array
    water_level_loss_with_prevention, where each water level corresponds to the
    percent of property that is damaged.

    The prepare immediately strategy is as follows:
        1) If the water level is less than or equal to 5ft, the cost is 0.
        2) If the water level is between 5ft and 10ft (exclusive), the cost is the
           house_value times the percentage of property damage for that water
           level, which is affected by the implementation of flood prevention
           measures. If the water level is not an integer value, the percentage
           should be interpolated.
        3) If the water level is at least 10ft, the cost is the entire value of
           the house.

	Args:
		water_level_list: list of simulated water levels for 2020-2100
        water_level_loss_with_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with flood prevention
        house_value: the value of the property we are estimating cost for

	Returns:
		an list of damage costs in 1000s, in the order in which the costs would
        be incurred temporally
	"""
    cost_list=[]
    for water_level in water_level_list: 
        if water_level<=5: 
            cost=0
        elif water_level>5 and water_level<10:
            if isinstance(water_level, int):
                for i in range(water_level_loss_with_prevention[:,0]):
                    if water_level_loss_with_prevention[i][0]==water_level:
                        percent=water_level_loss_with_prevention[i][1]*0.01 
                cost=percent*house_value/1000
            else: 
                function=interp1d(water_level_loss_with_prevention[:,0], water_level_loss_with_prevention[:,1]*0.01, fill_value='extrapolate')
                cost=float(function(water_level))*house_value/1000
        else:
            cost=house_value/1000
        cost_list.append(cost)
    return cost_list


def plot_strategies(data, water_level_loss_no_prevention, water_level_loss_with_prevention, house_value=400000,
                    cost_threshold=100000):
    """
	Runs and plots a Monte Carlo simulation of all of the different preparation
    strategies, based on the values in data and assuming a normal distribution.
    Five hundred samples should be generated for each year.

	Args:
		data: a 2-d numpy array with each row containing a year in order from 2020-2100
            inclusive, the 2.5th percentile, 97.5th percentile, mean, and standard
            deviation of the sea level rise for the given year
        water_level_loss_no_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with no flood prevention
        water_level_loss_with_prevention: a 2-d numpy array where the columns are
            water levels and the corresponding percent of property damage expected
            from that water level with flood prevention
        house_value: the value of the property we are estimating cost for
        cost_threshold: the amount of cost incurred before flood prevention
            measures are put into place
	"""
    num=500
    new_array=np.zeros((3, 81))
    years=range(2020, 2101)
    #do I need to copy the plot commands from the first function or do I just call it? 
    #each trial should redo the water level list that is the random part 
    #two nested for loops starting with for trial in range(num ) and then for loop for each year 
    #simulating water levels. Each trial has 81 samples, one for each year. 
    #t[0:,]=np.array(range(81))
    #np array version of simulated_cost_repair and totals stored across numpy 
    #convert to np.array for each list 
    for trial in range(num):
        water_level_list=simulate_water_levels(data)
        simulated_cost_repair=repair_only(water_level_list, water_level_loss_no_prevention, house_value)
        simulated_cost_wait=wait_a_bit(water_level_list, water_level_loss_no_prevention, water_level_loss_with_prevention,house_value, cost_threshold)
        simulated_cost_immediate=prepare_immediately(water_level_list,water_level_loss_with_prevention, house_value)
        #[:,1]
        #np array construct and initalize above the for loop. store the data from 500 trials across 81 years 
        #years are rows, column is trials 
        new_array[0,:]+=np.array(simulated_cost_repair)
        new_array[1,:]+=np.array(simulated_cost_wait)
        new_array[2,:]+=np.array(simulated_cost_immediate)
         #do I need to generate this each time in the for loop or remove it to outside? 
        plt.scatter(years, simulated_cost_repair, s= 0.25, c='green') 
        plt.scatter(years, simulated_cost_wait, s= 0.25, c='blue')
        plt.scatter(years, simulated_cost_immediate, s= 0.25, c='red')
    average_repair=new_array[0,:]/num
    average_wait=new_array[1,:]/num
    average_immediate=new_array[2,:]/num
    plt.plot(years, average_repair, color='green', label='Repair-only scenario')
    plt.plot(years, average_wait, color='blue', label='Wait-a-bit scenario')
    plt.plot(years, average_immediate, color='red', label='Prepare immediately scenario') #need to write label so legend knows what to plot 
    plt.title('Property Damage Cost Comparison')
    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Estimated Damage Cost ($K))')
    
    plt.show() 



if __name__ == '__main__':
    # Comment out the 'pass' statement below to run the lines below it
    # Uncomment the following lines to plot generate plots
    data = predicted_sea_level_rise(show_plot=False)
    water_level_list=simulate_water_levels(data)
    #print(water_level_list)
    water_level_loss_no_prevention = np.array([[5, 6, 7, 8, 9, 10], [0, 10, 25, 45, 75, 100]]).T
    #print(water_level_loss_no_prevention[:,0])
    #print(repair_only(water_level_list, water_level_loss_no_prevention, house_value= 400000) )
    water_level_loss_with_prevention = np.array([[5, 6, 7, 8, 9, 10], [0, 5, 15, 30, 70, 100]]).T
    #plot_simulation(data)
    plot_strategies(data, water_level_loss_no_prevention, water_level_loss_with_prevention)
    