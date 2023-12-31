"""
    this is Assignment 2 of Applied Data science 1 ,
    Statistic and trends

"""

# Import the pandas library for data manipulation and analysis
import pandas as pd

# Import the Matplotlib library for creating plots and visualizations
import matplotlib.pyplot as plt

# Import the NumPy library for numerical computations
import numpy as np
"""
    Please Install xlrd package in your environment
    "pip install xlrd"
    or
    "conda install -c anaconda xlrd"
"""
# Import the xlrd library for excel sheet
import xlrd

# Import warning to skip some # WARNING:
import warnings


"""
    settingColumns functions will take data in,
    then rename column names
    input : dataFrame
    output : dataFrame
"""


def settingColumns(data):

    # Renaming year columns

    yearColumns = {data.columns[i]: str(1960 + i - 4)
                   for i in range(4, len(data.columns))}
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
    data.set_index(
        data['CountryCode'] +
        " " +
        data['IndicatorCode'],
        inplace=True)

    # Dropping columns
    data.drop(['CountryName', 'CountryCode', 'IndicatorName',
              'IndicatorCode'], axis=1, inplace=True)

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


"""
    retrive functions will take
    countryCode, indicatorCode, data in
    then rename column names
    input : list,list, dataFrame
    output : dataFrame
"""


def retrive(countryCode, indicatorCode, data):
    # empty list
    emptylist = []
    if data.all == dataset.all:

        emptyData = pd.DataFrame(columns=dataset.columns)
        for i in countryCode:
            for j in indicatorCode:

                string1 = i + " " + j
                k = dataset.loc[string1]

                warnings.filterwarnings("ignore")
                emptyData = pd.concat(
                    [emptyData, pd.DataFrame([k])], ignore_index=True)
                emptylist.append(string1)

        ind = pd.Series(emptylist)
        emptyData.set_index(ind, inplace=True)

    else:
        emptyData = pd.DataFrame(index=transposedDataset.index)

        for i in countryCode:
            string1 = i + " " + indicatorCode
            emptyData = pd.concat(
                [emptyData, transposedDataset[string1]], axis=1,
                ignore_index=True)
            emptylist.append(string1)

        ind = pd.Series(emptylist)

        emptyData.rename(columns=ind, inplace=True)

    return emptyData


"""
    slicing functions will take
    data, gap in
    it divide columns based on gap given
    input : dataFrame, integer
    output : dataFrame
"""


def slicing(data, gap):
    dataCopy = data.copy()
    emptyData = pd.DataFrame(index=dataCopy.index)
    years = np.arange(1960, 2023, gap)
    years = years.astype('str')
    for i in years:
        warnings.filterwarnings("ignore")
        emptyData = pd.concat([emptyData, dataCopy[i]],
                              axis=1, ignore_index=True)
    ind = pd.Series(years)
    emptyData.rename(columns=ind, inplace=True)
    return emptyData


countryName = ["Brazil", "Russia", 'India', 'China', 'south africa']
countryNameSeries = pd.Series(countryName)
countryCode = ["BRA", "RUS", "IND", "CHN", "ZAF"]


"""
    Reading data from excel and
    storing in dataset, transposedDataset DataFrame
    by calling readFile function
"""

dataset, transposedDataset = readFile('API_19_DS2_en_excel_v2_6002116.xls')
print('Cleaned dataset :-')
print(dataset.head(5))
print("cleaned transposedDataset :-")
print(transposedDataset.head(5))


def main():
    # urban population growth

    # calling retrive and slicing functions, givng gap 2 years
    urbanGrowth = retrive(countryCode, ["SP.URB.GROW"], dataset)
    urbanGrowth = slicing(urbanGrowth, 2)

    # dropping missing value column's
    urbanGrowth = urbanGrowth.dropna(axis=1)

    print(urbanGrowth)

    # describe functions
    print('Urban population growth')
    print(urbanGrowth.describe())

    # aggre method on urbanGrowth
    print(urbanGrowth.agg({'1990': ['mean', 'min', 'max'],
                           '2000': ['mean', 'min', 'max'],
                           '2010': ['mean', 'min', 'max'],
                           '2020': ['mean', 'min', 'max']}))

    # Plotting line graph
    plt.figure(figsize=(8, 6))
    plt.plot(urbanGrowth.iloc[0], '-.', label='Brazil')
    plt.plot(urbanGrowth.iloc[1], '-.', label='Russia')
    plt.plot(urbanGrowth.iloc[2], '-.', label='India')
    plt.plot(urbanGrowth.iloc[3], '-.', label='China')
    plt.plot(urbanGrowth.iloc[4], '-.', label='S.Africa')

    # labeling
    plt.title("Urban population growth (1998 - 2022)")
    plt.xlabel("Year's")
    plt.ylabel("urban population growth %")

    # setting limits
    plt.xlim(18, 31)
    plt.ylim(-1, 4.5)
    plt.legend(title="years", loc='center left', bbox_to_anchor=(1, 0.5))

    # saving the graph
    plt.savefig(
        "graphs/urbanPopulationGrowth.png",
        dpi=310,
        bbox_inches='tight')
    plt.show()

    # % Foreign Direct Investment
    FDI = retrive(countryCode, ["BX.KLT.DINV.WD.GD.ZS"], dataset)
    FDI = slicing(FDI, 2)

    # dropping missing value column's
    FDI = FDI.dropna(axis=1)
    print("Foreign Direct Investment's")
    print(FDI)

    # describe functions
    print(FDI.describe())

    # aggre method on urbanGrowth
    print(FDI.agg({'2000': ['mean', 'min', 'max'],
                   '2010': ['mean', 'min', 'max'],
                   '2020': ['mean', 'min', 'max']}))

    # Plotting line graph
    plt.figure(figsize=(10, 8))

    plt.plot(FDI.iloc[0], '-.', label='Brazil')
    plt.plot(FDI.iloc[1], '-.', label='Russia')
    plt.plot(FDI.iloc[2], '-.', label='India')
    plt.plot(FDI.iloc[3], '-.', label='China')
    plt.plot(FDI.iloc[4], '-.', label='S. Africa')

    # labeling
    plt.title("Foreign Direct Investment (% of GDP)")
    plt.xlabel("years")
    plt.ylabel("Foreign Drirect Investment")

    # setting limits
    plt.xlim(3, 16)
    plt.legend(title="years", loc='center left', bbox_to_anchor=(1, 0.5))

    # saving the graph
    plt.savefig("graphs/FDI_Growth.png", dpi=310, bbox_inches='tight')
    plt.show()

    # CO2 emissions from gaseous fuel consumption (% of total)

    # Using retrive and retrive 3
    gasFuel = retrive(countryCode, ["EN.ATM.CO2E.GF.ZS"], dataset)
    gasFuel = slicing(gasFuel, 5)

    # droping and slicing
    gasFuel = gasFuel.dropna(axis=1)
    gasFuel = gasFuel.iloc[:, 7:]

    # setting index
    gasFuel = gasFuel.set_index(countryNameSeries)

    # describe
    print("CO2 emissions from gaseous fuel consumption")
    print(gasFuel.describe())

    # Plotting the bar graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # choosing shades of colors
    colors = [
        '#ff8c00',
        '#ff9b1e',
        '#ffa93c',
        '#ffb85a',
        '#ffc779',
        '#ffd597',
        '#ffe4b5']

    # Plotting each country's data in a grouped bar chart
    gasFuel.plot(kind='bar', ax=ax, color=colors)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # setting labels
    ax.set_title("CO2 emissions from gaseous fuel consumption (% of total)")
    ax.set_xlabel("Country Name's")
    ax.set_ylabel("CO2 emissions")

    # setting limits
    plt.ylim(0, 120)
    ax.legend(title="years", loc='center left', bbox_to_anchor=(1, 0.5))

    # Saving and display the plot
    plt.savefig("graphs/gaseousFuel", dpi=310, bbox_inches='tight')
    plt.show()

    # CO2 emissions from solid fuel consumption (% of total)

    #  Using retrive and retrive 3
    solidFuel = retrive(countryCode, ["EN.ATM.CO2E.SF.ZS"], dataset)
    solidFuel = slicing(solidFuel, 5)

    # Droping and slicing
    solidFuel = solidFuel.dropna(axis=1)
    solidFuel = solidFuel.iloc[:, 7:]

    # Setting index
    solidFuel = solidFuel.set_index(countryNameSeries)

    # describe
    print('CO2 emissions from solid fuel ')
    print(solidFuel.describe())

    # Plotting the bar graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # Choosing shades of colors
    colors = ['#add8e6', '#7390c8', '#566cb8', '#1d249a', '#00008b']

    # Plotting each country's data in a grouped bar chart
    solidFuel.plot(kind='bar', ax=ax, color=colors)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # setting labels
    ax.set_title("CO2 emissions from solid fuel consumption (% of total)")
    ax.set_xlabel("Country Name's")
    ax.set_ylabel("CO2 emissions")

    ax.legend(title="years", loc='center left', bbox_to_anchor=(1, 0.5))
    # Saving and display the plot
    plt.savefig("graphs/solidFuel.png", dpi=310, bbox_inches='tight')
    plt.show()

    """
    EN.URB.MCTY.TL.ZS : Population in urban agglomerations of more
    than 1 million (% of total population)

    SI.POV.DDAY : Poverty headcount ratio at $2.15 a day (2017 PPP)
    (% of population)

    SH.DYN.MORT : Mortality rate, under-5 (per 1,000 live births)
    SP.URB.TOTL.IN.ZS : Urban population (% of total population)
    EN.ATM.CO2E.GF.ZS :CO2 emissions from gaseous fuel consumption
    EN.ATM.CO2E.SF.ZS :CO2 emissions from solid fuel consumption
    """

    indicators = [
        'EN.URB.MCTY.TL.ZS',
        "SI.POV.DDAY",
        'SH.DYN.MORT',
        'SP.URB.TOTL.IN.ZS',
        'EN.ATM.CO2E.GF.ZS',
        'EN.ATM.CO2E.SF.ZS']

    countryCode2 = ['USA']
    indicatorNames = [
        'Urban agglom',
        'Poverty',
        'Mortality',
        'Urban population',
        'CO2 gas fuels',
        'CO2 solid fuels']
    # Using retrive function and drop method
    USA = retrive(countryCode2, indicators, dataset)
    USA = USA.dropna(axis=1)

    # setting index
    indicatorNamesSeries = pd.Series(indicatorNames)
    USA = USA.set_index(indicatorNamesSeries)

    # transposing and Correcaltio
    USA = USA.T
    print("USA data")
    print(USA)
    corrUSA = USA.corr()
    print('correlation of USA')
    print(corrUSA)

    # Create the heatmap
    plt.imshow(corrUSA, cmap='viridis', interpolation='nearest')
    plt.colorbar()

    # Creating X and Y ticks and title
    plt.xticks(ticks=np.arange(len(USA.columns)),
               rotation=90, labels=USA.columns)
    plt.yticks(ticks=np.arange(len(USA.columns)), labels=USA.columns)
    plt.title("USA - Heatmap")

    # Saving and display the plot
    plt.savefig("graphs/USA_heatmap.png", dpi=310, bbox_inches='tight')
    plt.show()

    countryCode2 = ['IND']
    # Using retrive function and drop method
    India = retrive(countryCode2, indicators, dataset)
    India = India.dropna(axis=1)

    # setting index
    indicatorNamesSeries = pd.Series(indicatorNames)
    India = India.set_index(indicatorNamesSeries)

    # transposing and Correcaltio
    India = India.T

    print("USA data")
    print(USA)

    corrIndia = India.corr()

    print('correlation of India')
    print(corrIndia)
    # Create the heatmap
    plt.imshow(corrIndia, cmap='viridis', interpolation='nearest')
    plt.colorbar()

    # Creating X and Y ticks and title

    plt.xticks(ticks=np.arange(len(India.columns)),
               rotation=90, labels=India.columns)
    plt.yticks(ticks=np.arange(len(India.columns)), labels=India.columns)
    plt.title("India - Heatmap")

    # Saving and display the plot
    plt.savefig("graphs/India_heatmap.png", dpi=310, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
