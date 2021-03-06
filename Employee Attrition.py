# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 13:39:29 2020

@author: Sundharesan
"""

#Importing necessary libraries:
import numpy as np
import pandas as pd
import seaborn as sb

#Loading the data:
from google.colab import files
uploaded = files.upload()

#Storing data as a dataframe:
df=pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

#Display first 7 rows of data:
df.head(7)

#Number of rows and columns:
df.shape

#Column datatypes:
df.dtypes

#Find empty values in each column:
df.isna().sum()

#Missing values in the data:
df.isnull().values.any()

#View some statistics:

df.describe()

#Count of the no. of employees that stayed and left the company:
df['Attrition'].value_counts()

#Visualize the no. of employees that stayed and left the company:
sb.countplot(df['Attrition'])

#Percentage if we guessed "No" for attrition:
((1233-237)/1233)*100

#No. of employees that left stayed by age:
import matplotlib.pyplot as plt
plt.subplots(figsize=(12,4))
sb.countplot(x='Age', hue='Attrition', data=df, palette='colorblind')

for column in df.columns:
  if df[column].dtype == object:
    print(str(column) + ' : '+ str(df[column].unique())) 
    print(df[column].value_counts())
    print('__________________________________________________________')

#Removing unwanted columns:
df=df.drop('Over18', axis=1)
df=df.drop('EmployeeNumber', axis=1)
df=df.drop('StandardHours', axis=1)
df=df.drop('EmployeeCount', axis=1)

#Correlation:
df.corr()

#Visualizing the correlation:
plt.figure(figsize=(14,14))
sb.heatmap(df.corr(), annot=True, fmt= '.0%')

#Transform the data(non-numeric to numeric):
from sklearn.preprocessing import LabelEncoder

for column in df.columns:
  if df[column].dtype == np.number:
    continue
  df[column] = LabelEncoder().fit_transform(df[column])

#Creating new column:
df['Age_Years'] = df['Age']

#Dropping the age column:
df = df.drop('Age', axis=1)

#Display the dataframe:
df

#Splitting the data:
X=df.iloc[:,1:df.shape[1]].values
Y=df.iloc[:,0].values

#Split the data into 75% training and 25% testing:
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=0)

#Random Forest Classifier:
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
forest.fit(X_train,Y_train)

#Get the accuracy on training dataset:
(forest.score(X_train,Y_train))*100

#Confusion matrix and accuracy score for the model on the test data:
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(Y_test, forest.predict(X_test))

TN=cm[0][0]
TP=cm[1][1]
FN=cm[1][0]
FP=cm[0][1]

print(cm)
print('Model Testing Accuracy ={}'.format(((TP+TN)/(TP+TN+FP+FN))*100))
