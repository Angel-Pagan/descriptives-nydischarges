import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
from tableone import TableOne, load_dataset
import urllib.request
import os
import seaborn
import researchpy as rp
import patsy
from scipy import stats
from pandas.plotting import scatter_matrix

""" Loading and Cleaning SPARCS Data """
sparcs = pd.read_csv('https://health.data.ny.gov/resource/gnzp-ekau.csv')

# get a count of the number of rows and columns and column data types
sparcs.columns
sparcs.shape
sparcs.dtypes

#Cleaning

sparcs.columns = sparcs.columns.str.replace('[^A-Za-z0-9]+', '_')
sparcs.columns = sparcs.columns.str.lower()
sparcs.columns #Print Updated column names


""" Descriptive Statistics (By Age Group) """

# Length of stay 
los_mean = sparcs['length_of_stay'].mean()
los_median = sparcs['length_of_stay'].median()
los_describe = sparcs['length_of_stay'].describe()
boxplot = seaborn.boxplot(data=sparcs, x="length_of_stay", y="age_group")
plt.show()

#Total costs 
costs_mean = sparcs['total_costs'].mean()
costs_median = sparcs['total_costs'].median()
costs_describe = sparcs['total_costs'].describe()
boxplot = seaborn.boxplot(data=sparcs, x="total_costs", y="age_group") 
plt.show()

#Total charges 
charges_mean = sparcs['total_charges'].mean()
charges_median = sparcs['total_charges'].mean()
charges_describe = sparcs['total_charges'].mean()
boxplot = seaborn.boxplot(data=sparcs, x="total_charges", y="age_group") 
plt.show() 


#Risk of mortality by age group
sparcs['apr_risk_of_mortality'].value_counts()
risk = ['Minor', 'Moderate', 'Major', 'Exreme']
count = [623, 190, 154, 33]
plt.bar(risk, count)
plt.title('Risk of Mortality Among Hospital Discharges')
plt.xlabel('Risk of Mortality')
plt.ylabel('Number of Patients')
plt.show()

""" Correlation analysis  """

# 2-sample t-test
stats.ttest_1samp(sparcs.dropna()['Weight'], 0)
female_costs = sparcs.dropna()[sparcs['gender'] == 'F']['total_costs']
male_costs = sparcs.dropna()[sparcs['gender'] == 'M']['total_costs']
stats.ttest_ind(female_costs, male_costs) 

# TableOne
sparcs_columns = ['age_group', 'gender', 'race', 'type_of_admission', 'length_of_stay']
categorical = ['gender', 'race', 'type_of_admission', 'age_group']
groupby = ['age_group']
table1 = TableOne(sparcs, columns=sparcs_columns, categorical=categorical, groupby=groupby, pval=False)
print(table1.tabulate(tablefmt = "fancy_grid"))
table1.to_csv('data/tableone_sparcs.csv')

# Researchpy
rp.summary_cont(sparcs[['length_of_stay', 'total_costs']])