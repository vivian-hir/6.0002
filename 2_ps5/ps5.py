# -*- coding: utf-8 -*-
# Problem Set 5: Modeling Temperature Change
# Name:
# Collaborators:

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAIN_INTERVAL = range(1961, 2000)
TEST_INTERVAL = range(2000, 2017)

##########################
#    Begin helper code   #
##########################

def standard_error_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by a linear
            regression model
        model: a numpy array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]


class Dataset(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Dataset instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_daily_temps(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_temp_on_date(self, city, month, day, year):
        """
        Get the temperature for the given city at the specified date.

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified date and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year {} is not available".format(year)
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

##########################
#    End helper code     #
##########################

    def calculate_annual_temp_averages(self, cities, years):
        # NOTE: TO BE IMPLEMENTED IN PART 4B.2 OF THE PSET
        avg_list=[]
        avg_array=np.zeros((len(cities), len(years)))
        #create array with rows being # cities, cols being # years 
        for i,city in enumerate(cities): #want to use the index 
            temp_list=[]
            for year in years: 
                array=self.get_daily_temps(city, year)
                average=array.mean()
                temp_list.append(average) #average for each year 
            avg_array[i,:]+=np.array(temp_list) #add the list to each row for the city 
        for col in avg_array.T: #transpose array to get sum of the column 
            avg=col.mean() 
            avg_list.append(avg)
        return np.array(avg_list)



def linear_regression(x, y):
    """
    Calculates a linear regression model for the set of data points.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points

    Returns:
        (m, b): A tuple containing the slope and y-intercept of the regression line,
                both of which are floats.
    """
    numerator_sum=((x-x.mean())*(y-y.mean())).sum()
    denominator_sum=((x - x.mean())**2).sum()
    slope=numerator_sum/denominator_sum 
    b=y.mean()-(slope*x.mean())
    return (slope, b)

def squared_error(x, y, m, b):
    """
    Calculates the squared error of the linear regression model given the set
    of data points.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        m: The slope of the regression line
        b: The y-intercept of the regression line


    Returns:
        a float for the total squared error of the regression evaluated on the
        data set
    """
    y_estimate=m*x+b
    standard_error=((y-y_estimate)**2).sum()
    return standard_error 


def generate_polynomial_models(x, y, degrees):
    """
    Generates a list of polynomial regression models with degrees specified by
    degrees for the given set of data points

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        degrees: a list of integers that correspond to the degree of each polynomial
            model that will be fit to the data

    Returns:
        a list of numpy arrays, where each array is a 1-d numpy array of coefficients
        that minimizes the squared error of the fitting polynomial
        
        The models should appear in the list in the same order as their corresponding 
        integers in the `degrees` parameter
    """
    model_list=[]
    for deg in degrees:
        array=np.polyfit(x,y,deg)
        model_list.append(array)
    return model_list


def evaluate_models(x, y, models, display_graphs=False):
    """
    For each regression model, compute the R-squared value for this model and
    if display_graphs is True, plot the data along with the best fit curve. You should make a separate plot for each model.
    
    Your plots should adhere to the following guidelines:

        - Plot the data points as individual green (color='C2') dots.
        - Plot the model with an orange (color='C1') solid line.
        - Include a title. Your title should include the $R^2$ value of the model and the degree. If the model is a linear curve (i.e. its degree is one), the title should also include the ratio of the standard error of this fitted curve's slope to the slope. Round your $R^2$ and SE/slope values to 4 decimal places.
        - Label the axes. You may assume this function will only be used in the case where the x-axis represents years and the y-axis represents temperature in degrees Celsius.

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the R-squared value for each model
    """
    r2_list=[]
    model_dict={}
    pred_dict={}
    for i, model in enumerate(models): 
        y_pred=[]
        for i in (range(len(x))):
            value=np.polyval(model, x[i]) #calculate y value 
            y_pred.append(value) #add y value to list 
        deg_value=len(model)-1
        r2=r2_score(y, y_pred) #calculate r2 
        r2_list.append(r2) 
        if len(model)==2: #if it is linear regression 
                value=standard_error_over_slope(x, y, y_pred, model)
                model_dict[i]=(r2, deg_value, value)
        else:
            model_dict[i]=(r2, deg_value)
        pred_dict[i]=y_pred
    if display_graphs==True: 
        for model in models: 
            tuple=model_dict[i]
            r2_val=round(tuple[0], 4)
            degree=tuple[1]
            predicted_y=pred_dict[i]
            plt.scatter(x,y,s=1, c="C2")
            plt.plot(x, predicted_y, c="C1")
            if degree==1:
                slope_value=round(tuple[2], 4)
                plt.title(f"Temperature Over the Years of degree 1 with r2={r2_val} and SE/slope={slope_value}")
            else: 
                plt.title(f"Temperature Over the Years of degree {degree} with r2={r2_val}") #should I do f string or just string concatenation? 
            plt.xlabel("Years") 
            plt.ylabel("Temperature (deg C)") 
            plt.show() 
    return r2_list
#could you think of another way to access the model? 

def get_max_trend(x, y, length, positive_slope):
    """
    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        length: the length of the interval
        positive_slope: a boolean whose value specifies whether to look for
            an interval with the most extreme positive slope (True) or the most
            extreme negative slope (False)

    Returns:
        a tuple of the form (i, j, m) such that the application of linear (deg=1)
        regression to the data in x[i:j], y[i:j] produces the most extreme
        slope m, with the sign specified by positive_slope and j-i = length.

        In the case of a tie, it returns the first interval. For example,
        if the intervals (2,5) and (8,11) both have slope 3.1, (2,5,3.1) should be returned.

        If no intervals matching the length and sign specified by positive_slope
        exist in the dataset then return None
    """
    max_slope=-float("inf")
    min_slope=float("inf")
    for i in range (len(x)-length+1): #stop iterating when j equals len(x) 
        j=i+length 
        x_snip=x[i:j]
        y_snip=y[i:j]
        tup=linear_regression(x_snip, y_snip)
        slope=tup[0]
        if positive_slope: 
           
            if slope > max_slope+10**(-8):  
                max_slope=slope #reset max_slope to current slope 
                start=i 
                stop=j
        else: 
            if slope < min_slope-10**(-8): #want the lower bound, so minus 
                min_slope = slope #reset min_slope to current slope 
                start=i
                stop=j
    if positive_slope: #check if positive_slope is positive value 
        if max_slope<0: 
            return None 
        return start, stop, max_slope
    else: #negative_slope condition 
        if min_slope>0: #check if min_slope is negative 
            return None 
        return start, stop, min_slope 
    #need to handle the tiebreaker case and the return None case 
    #put the return statement at the end after iterating through a for loop 


def get_all_max_trends(x, y):
    """
    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points

    Returns:
        a list of tuples of the form (i,j,m) such that the application of linear
        regression to the data in x[i:j], y[i:j] produces the most extreme
        positive OR negative slope m, and j-i=length.

        The returned list should have len(x) - 1 tuples, with each tuple representing the
        most extreme slope and associated interval for all interval lengths 2 through len(x).
        If there is no positive or negative slope in a given interval length L (m=0 for all
        intervals of length L), the tuple should be of the form (0,L,None).

        The returned list should be ordered by increasing interval length. For example, the first
        tuple should be for interval length 2, the second should be for interval length 3, and so on.

        If len(x) < 2, return an empty list
    """
    tuple_list=[]
    if len(x)<2:
        return [] 
    for l in range(2, len(x)+1): #iterate through all the interval lengths 2<=x<=len(x) 
        value=get_max_trend(x, y, l, positive_slope=True) #use above function 
        second_value=get_max_trend(x, y, l, positive_slope=False)
        if value is None and second_value is None: 
            tuple_list.append((0, l, None)) 
        elif value is None and second_value is not None:
            tuple_list.append(second_value)
        elif value is not None and second_value is None: 
            tuple_list.append(value) #these cases above handle the None case 
        else: 
            big_slope=value[2]
            small_slope=second_value[2]
            if big_slope>abs(small_slope):
                tuple_list.append(value) #append the most extreme value 
            elif big_slope==0 and small_slope==0: #if both slopes are equal to 0 
                tuple_list.append((0, l, None))
            else:
                tuple_list.append(second_value)
            
    return tuple_list 


def calculate_rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    numerator=((y-estimated)**2).sum()
    rmse=np.sqrt(numerator/len(y))
    return rmse 


def evaluate_rmse(x, y, models, display_graphs=False):
    """
    For each regression model, compute the RMSE for this model and if
    display_graphs is True, plot the test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    RMSE should be rounded to 4 decimal places.

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N test data sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N test data sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.
        display_graphs: A boolean whose value specifies if the graphs should be
            displayed

    Returns:
        A list holding the RMSE value for each model
    """
    rmse_list=[]
    model_dict={}
    pred_dict={}
    for i, model in enumerate(models): #want the index for each model 
        y_pred=[]
        for i in (range(len(x))):
            value=np.polyval(model, x[i])
            y_pred.append(value) #calculate y value, add to list 
        deg_value=len(model)-1
        rmse=calculate_rmse(y, y_pred) 
        rmse_list.append(rmse) 
        model_dict[i]=(rmse, deg_value)
        pred_dict[i]=y_pred
    if display_graphs==True: 
        for model in models: 
            tuple=model_dict[i]
            rmse_val=round(tuple[0], 4)
            degree=tuple[1]
            predicted_y=pred_dict[i]
            plt.scatter(x,y,s=1, c="blue")
            plt.plot(x, predicted_y, c="red")
            plt.title(f"Temperature Over the Years of degree {degree} with RMSE={rmse_val}")
            plt.xlabel("Years") 
            plt.ylabel("Temperature (deg C)") 
            plt.show() 
    return rmse_list
#could you think of another way to access the model? 


if __name__ == '__main__':
    ##################################################################################
    # Problem 4A: DAILY TEMPERATURE
    data=Dataset('data.csv')
    years=range(1961, 2017)
    temp_list=[]
    for i in years: 
        value=data.get_temp_on_date("SAN FRANCISCO", 12, 1, i)
        temp_list.append(value)
    x_array=np.array(years)
    y_array=np.array(temp_list)
    # model=generate_polynomial_models(x_array, y_array, [1])
    # evaluate_models(x_array, y_array,model, True)

    ##################################################################################
    # Problem 4B: ANNUAL TEMPERATURE
    # annual_temp=data.calculate_annual_temp_averages(["SAN FRANCISCO"], years) 
    # temp_array=np.array(annual_temp)
    # avg_model=generate_polynomial_models(x_array, temp_array, [1])
    # evaluate_models(x_array, temp_array, avg_model, True)

    ##################################################################################
    # Problem 5B: INCREASING TRENDS
    # y_array=data.calculate_annual_temp_averages(["SEATTLE"], x_array)
    # tuple_value=get_max_trend(x_array, y_array, 30, True)
    # start=tuple_value[0]
    # stop=tuple_value[1]
    # interval=x_array[start:stop]
    # new_y_array=y_array[start:stop]
    # model=generate_polynomial_models(interval, new_y_array, [1])
    # evaluate_models(interval, new_y_array, model, True)

    ##################################################################################
    # Problem 5C: DECREASING TRENDS
    # y_array=data.calculate_annual_temp_averages(["SEATTLE"], x_array)
    # tuple_value=get_max_trend(x_array, y_array, 12, False)
    # start=tuple_value[0]
    # stop=tuple_value[1]
    # interval=x_array[start:stop]
    # new_y_array=y_array[start:stop]
    # model=generate_polynomial_models(interval, new_y_array, [1])
    # evaluate_models(interval, new_y_array, model, True)

    ##################################################################################
    # Problem 5D: ALL EXTREME TRENDS

    ##################################################################################
    # Problem 6B: PREDICTING
    training_array=data.calculate_annual_temp_averages(CITIES, TRAIN_INTERVAL)
    year_array=np.array(TRAIN_INTERVAL)
    test_array=np.array(TEST_INTERVAL)
    training_model=generate_polynomial_models(year_array, training_array, [2])
    # evaluate_models(year_array, training_array, training_model, True)
    new_array=data.calculate_annual_temp_averages(CITIES, test_array)
    evaluate_rmse(test_array, new_array, training_model, True)
    ####################################################################################
