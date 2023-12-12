import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import warnings


def readFile(file):
    df1 = pd.read_excel(file)

    df1 = settingColumns(df1)
    df1 = settingIndex(df1)

    df2 = df1.T
    return df1, df2


def settingIndex(data):
    data.reset_index(drop=True, inplace=True)
    # setting index
    data.set_index(data['CountryCode']+" "+ data['IndicatorCode'], inplace = True)
    data.drop(['CountryName', 'CountryCode', 'IndicatorName', 'IndicatorCode'], axis=1, inplace = True)
    return data


def settingColumns(data):
    # Renaming year columns
    year_columns = {data.columns[i]: str(1960 + i - 4) for i in range(4, len(data.columns))}
    data.rename(columns=year_columns, inplace=True)

    data.rename(columns={
    'Data Source': 'CountryName',
    'World Development Indicators': 'CountryCode',
    'Unnamed: 2': 'IndicatorName',
    'Unnamed: 3': 'IndicatorCode'
        }, inplace=True)

    data.drop(index=data.index[:3], axis=0, inplace=True)
    return data


def retrive(CountryCode, IndicatorCode,data):
    ls = []
    if data.all == df1.all:

        df = pd.DataFrame(columns= df1.columns)
        for i in CountryCode:
            for j in IndicatorCode:
                string1 = i +" "+ j
                k = df1.loc[string1]

                warnings.filterwarnings("ignore")
                df = pd.concat([df, pd.DataFrame([k])], ignore_index=True)
                ls.append(string1)

        ind =pd.Series(ls)
        df.set_index(ind, inplace=True)

    else:
        df = pd.DataFrame(index=df2.index)
        for i in CountryCode:
            string1 = i+" "+ IndicatorCode
            df = pd.concat([df, df2[string1]], axis = 1, ignore_index=True)
            ls.append(string1)
        ind =pd.Series(ls)

        df.rename(columns=ind, inplace = True)


    return df


def retrive3(data, k):
    df = data.copy()
    dfk = pd.DataFrame(index=df.index )
    ll= np.arange(1960, 2023, k)
    ll = ll.astype('str')
    for i in ll:
        warnings.filterwarnings("ignore")
        dfk = pd.concat([dfk, df[i]], axis=1 ,ignore_index=True)
    ind =pd.Series(ll)
    dfk.rename(columns=ind, inplace =True)
    return dfk
