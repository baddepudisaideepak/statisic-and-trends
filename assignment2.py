import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as plt



#import xlrd
import warnings


"""
    settingColumns functions will take data in,
    then rename column names
    input : dataFrame
    output : dataFrame
"""


def settingColumns(data):

    # Renaming year columns

    yearColumns = {data.columns[i]: str(1960 + i - 4) for i in range(4, len(data.columns))}
    data.rename(columns=yearColumns, inplace=True)

    data.rename(columns={
    'Data Source': 'CountryName',
    'World Development Indicators': 'CountryCode',
    'Unnamed: 2': 'IndicatorName',
    'Unnamed: 3': 'IndicatorCode'
        }, inplace=True)

    data.drop(index=data.index[:3], axis=0, inplace=True)
    return data


"""
    settingIndex functions will take data in,
    then resets Index names and drop's column's
    input : dataFrame
    output : dataFrame
"""


def settingIndex(data):

    # Reseting the index
    data.reset_index(drop=True, inplace=True)

    # Changing index
    data.set_index(data['CountryCode']+" "+ data['IndicatorCode'], inplace = True)

    # Dropping columns
    data.drop(['CountryName', 'CountryCode', 'IndicatorName', 'IndicatorCode'], axis=1, inplace = True)

    return data

"""
    readFile functions will take filename in,
    then rename column names
    input : dataFrame
    output : dataFrame
"""


def readFile(fileName):
    data = pd.read_excel(fileName)

    data = settingColumns(data)
    data = settingIndex(data)

    transposedData = data.T
    return data, transposedData

dataset , transposedDataset = readFile('API_19_DS2_en_excel_v2_6002116.xls')

"""
    retrive functions will take
    countryCode, indicatorCode, data in
    then rename column names
    input : list,list, dataFrame
    output : dataFrame
"""

def retrive(countryCode, indicatorCode,data):
    # empty list
    emptylist = []
    if data.all == dataset.all:

        emptyData = pd.DataFrame(columns= dataset.columns)
        for i in countryCode:
            for j in indicatorCode:

                string1 = i +" "+ j
                k = dataset.loc[string1]

                warnings.filterwarnings("ignore")
                emptyData = pd.concat([emptyData, pd.DataFrame([k])], ignore_index=True)
                emptylist.append(string1)

        ind =pd.Series(emptylist)
        emptyData.set_index(ind, inplace=True)

    else:
        emptyData = pd.DataFrame(index=transposedDataset.index)

        for i in countryCode:
            string1 = i+" "+ indicatorCode
            emptyData = pd.concat([emptyData, transposedDataset[string1]], axis = 1, ignore_index=True)
            emptylist.append(string1)

        ind =pd.Series(emptylist)

        emptyData.rename(columns=ind, inplace = True)


    return emptyData


"""
    retrive3 functions will take
    data, gap in
    it divide columns based on gap given
    input : dataFrame, integer
    output : dataFrame
"""
def retrive3(data, gap):
    dataCopy = data.copy()
    emptyData = pd.DataFrame(index=dataCopy.index )
    years = np.arange(1960, 2023, gap)
    years = years.astype('str')
    for i in years:
        warnings.filterwarnings("ignore")
        emptyData = pd.concat([emptyData, dataCopy[i]], axis=1 ,ignore_index=True)
    ind =pd.Series(years)
    emptyData.rename(columns=ind, inplace =True)
    return emptyData

countryName =["Brazil", "Russia", 'India', 'China','south africa']
countryNameSeries =pd.Series(countryName)
countryCode = ["BRA","RUS","IND","CHN", "ZAF"]

def main():

    # urban population growth

    # calling retrive and retrive3 functions, givng gap 2 years
    urbanGrowth= retrive(countryCode, ["SP.URB.GROW"], dataset )
    urbanGrowth = retrive3(urbanGrowth, 2)

    #dropping missing value column's
    urbanGrowth = urbanGrowth.dropna(axis=1)

    print(urbanGrowth)

    # describe functions
    print(urbanGrowth.describe())

    # aggre method on urbanGrowth
    print(urbanGrowth.agg({'1990' : ['mean', 'min', 'max'],
                     '2000' : ['mean', 'min', 'max'],
                     '2010' : ['mean', 'min', 'max'],
                     '2020' : ['mean', 'min', 'max']}))


    # Plotting line graph
    plt.figure(figsize=(8,6))
    plt.plot(urbanGrowth.iloc[0],'-.',label = 'Brazil')
    plt.plot(urbanGrowth.iloc[1],'-.',label = 'Russia')
    plt.plot(urbanGrowth.iloc[2],'-.',label = 'India')
    plt.plot(urbanGrowth.iloc[3],'-.', label = 'China')
    plt.plot(urbanGrowth.iloc[4],'-.', label = 'S.Africa')

    # labeling
    plt.title("Urban population growth (1998 - 2022)")
    plt.xlabel("Year's")
    plt.ylabel("urban population growth %")

    # setting limits
    plt.xlim(18,31)
    plt.ylim(-1,4.5)
    plt.legend(title="years", loc='center left', bbox_to_anchor=(1, 0.5))

    # saving the graph
    plt.savefig("urbanpopulationgrowth.png",dpi = 310,  bbox_inches= 'tight' )
    plt.show()



    #% Foregin Direct Investment
    FDI= retrive(countryCode, ["BX.KLT.DINV.WD.GD.ZS"], dataset )
    FDI = retrive3(FDI, 2)

    #dropping missing value column's
    FDI = FDI.dropna(axis=1)

    print(FDI)

    # describe functions
    print(FDI.describe())

    # aggre method on urbanGrowth
    print(FDI.agg({'2000' : ['mean', 'min', 'max'],
                    '2010' : ['mean', 'min', 'max'],
                    '2020' : ['mean', 'min', 'max']}))


    # Plotting line graph
    plt.figure(figsize=(10,8))

    plt.plot(FDI.iloc[0], '-.', label = 'Brazil')
    plt.plot(FDI.iloc[1], '-.', label = 'Russia')
    plt.plot(FDI.iloc[2], '-.', label = 'India')
    plt.plot(FDI.iloc[3], '-.', label = 'China')
    plt.plot(FDI.iloc[4], '-.', label = 'S. Africa')

    # labeling
    plt.title("Foregin Direct Investment (% of GDP)")
    plt.xlabel("years")
    plt.ylabel("Foregin Drirect Investment")

    # setting limits
    plt.xlim(3,16)
    plt.legend(title="years", loc='center left', bbox_to_anchor=(1, 0.5))

    # saving the graph
    plt.savefig("FDI Growth.png",dpi = 310,  bbox_inches= 'tight' )
    plt.show()

    # CO2 emissions from gaseous fuel consumption (% of total)

    # Using retrive and retrive 3
    gasFuel = retrive(countryCode, ["EN.ATM.CO2E.GF.ZS"], dataset )
    gasFuel = retrive3(gasFuel, 5)

    # droping and slicing
    gasFuel = gasFuel.dropna(axis=1)
    gasFuel = gasFuel.iloc[:,7:]

    # setting index
    gasFuel = gasFuel.set_index(countryNameSeries)

    # describe
    print(gasFuel.describe())

    # Plotting the bar graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # choosing shades of colors
    colors = ['#ff8c00', '#ff9b1e', '#ffa93c', '#ffb85a', '#ffc779', '#ffd597', '#ffe4b5']



    # Plotting each country's data in a grouped bar chart
    gasFuel.plot(kind='bar', ax=ax , color =colors)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # setting labels
    ax.set_title("CO2 emissions from gaseous fuel consumption (% of total)")
    ax.set_xlabel("Country Name's")
    ax.set_ylabel("CO2 emissions")

    #setting limits
    plt.ylim(0,120)
    ax.legend(title="years", loc='center left', bbox_to_anchor=(1, 0.5))")

    # Saving and display the plot
    plt.savefig("gaseousFuel",dpi = 310, bbox_inches= 'tight' )
    plt.show()
    #CO2 emissions from solid fuel consumption (% of total)

    #  Using retrive and retrive 3
    solidFuel = retrive(countryCode, ["EN.ATM.CO2E.SF.ZS"], dataset )
    solidFuel = retrive3(solidFuel, 5)

    # Droping and slicing
    solidFuel = solidFuel.dropna(axis=1)
    solidFuel = solidFuel.iloc[:,7:]

    # Setting index
    solidFuel = solidFuel.set_index(countryNameSeries)

    # Plotting the bar graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # Choosing shades of colors
    colors = ['#add8e6','#7390c8', '#566cb8', '#1d249a', '#00008b' ]


    # Plotting each country's data in a grouped bar chart
    solidFuel.plot(kind='bar', ax=ax, color = colors)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # setting labels
    ax.set_title("CO2 emissions from solid fuel consumption (% of total)")
    ax.set_xlabel("Country Name's")
    ax.set_ylabel("CO2 emissions")


    ax.legend(title="years", loc='center left', bbox_to_anchor=(1, 0.5))
    # Saving and display the plot
    plt.savefig("gaseouddsFuel.png",dpi = 310, bbox_inches= 'tight' )
    plt.show()
