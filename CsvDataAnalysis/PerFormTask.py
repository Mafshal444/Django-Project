from tkinter.messagebox import RETRY
from xml.etree.ElementTree import tostring
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os, json, pickle
from .models import DataAnalysis
import redis

r = redis.Redis(
    host='127.0.0.1',
    port="6379", 
    password='')
dataFrame = pd.read_csv(r'C:\Users\lenovo\Downloads\archive\QS World University Rankings 2022.csv')
_dict = dataFrame.to_dict()
r.set('dataframe',pickle.dumps(_dict))
# Get universities which don't have city name
def UniversityWithNoCity():
    univ = pd.DataFrame.from_dict(pickle.loads(r.get('dataframe')))
    return univ[univ['city'].isna()] 

# Get universities within same region and same country
def GetUniversityByRegion(region, country):
    univ = pd.DataFrame.from_dict(pickle.loads(r.get('dataframe')))
    print("insideeee")
    pt = univ.loc[(univ['region'] == region) &  (univ['country'] == country)]
    # print(pt['city'].value_counts())
    df2 = pt.groupby('city')['university'].apply(list).reset_index(name="Universities")
    data = {}
    for ind in df2.index:
        data[df2['city'][ind]] = df2['Universities'][ind]
    # print(data)
    p_mydict = pickle.dumps(data)
    r.set(country,p_mydict)
    value =  pickle.loads(r.get(country))
    return value


def TopTenCountries():
    print('hhhhhh')
    univ = pd.DataFrame.from_dict(pickle.loads(r.get('dataframe')))
    CountryGroupBy = univ.groupby('country').size().reset_index(name='no_of_universities')
    No_Of = CountryGroupBy.sort_values(by='no_of_universities', ascending = False).head(10)
    # print(No_Of)
    TopTen = {}
    for ind in No_Of.index:
        TopTen[No_Of['country'][ind]] = str(No_Of['no_of_universities'][ind])
    p_mydict = pickle.dumps(TopTen)
    r.set("TopTen",p_mydict)
    return TopTen


# Insert Data to MongoDb Database
def InsertData(dataframe):
    value = pickle.loads(r.get(dataframe))
    print(type(value))
    print(value)
    # my_json = json.loads(my_json)
    # pt = univ.loc[(univ['region'] == "Asia") & (univ['country'] == "Pakistan")]
    # print(pt['city'].value_counts())
    # df2 = pt.groupby('city')['university'].apply(list).reset_index(name="Universities")
    page = DataAnalysis(Id=dataframe)
    page.analytized_data = value
    page.save()
    # DataAnalysis.objects.create(data=df2.to_json())
    # data = GetData()
    # print(data)
    return


def GetData(action):
    # data = DataAnalysis.objects.get(Id = 'df1')
    # for i in data.iterator():
    #     print(i)
    data = {}
    if action == 'all':
        for product in DataAnalysis.objects():
            data[product.Id] = product.analytized_data
            # print ('ID:',product.Id, 'Name:',product.analytized_data)
        return data
    else:
        for product in DataAnalysis.objects(Id=action):
            data[product.Id] = product.analytized_data
            # print ('ID:',product.Id, 'Name:',product.analytized_data)
        return data
