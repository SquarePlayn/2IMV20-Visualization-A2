import pandas as pd
import json
from copy import deepcopy

DATE_COLUMN = 'Date'
COUNTRY_COLUMN = 'Country'
CONFIRMED_COLUMN = 'Confirmed'
DEATHS_COLUMN = 'Deaths'
RECOVERED_COLUMN = 'Recovered'
POWER_COLUMN = 'Emissions'

carbon_df = pd.read_excel("carbon-monitor-maingraphdatas.xls"). \
    rename(columns={"country / group of countries": COUNTRY_COLUMN})
covid_confirmed_df = pd.read_csv("time_series_covid19_confirmed_global.csv"). \
    rename(columns={"Country/Region": COUNTRY_COLUMN})
covid_deaths_df = pd.read_csv("time_series_covid19_deaths_global.csv"). \
    rename(columns={"Country/Region": COUNTRY_COLUMN})
covid_recovered_df = pd.read_csv("time_series_covid19_recovered_global.csv"). \
    rename(columns={"Country/Region": COUNTRY_COLUMN})

countries = ["Brazil", "China", "France", "Germany", "India", "Italy", "Japan", "Russia", "Spain", "United Kingdom",
             "United States"]
countries_carbon = deepcopy(countries)
countries_carbon.append('World')

carbon_df.loc[carbon_df[COUNTRY_COLUMN] == "UK", COUNTRY_COLUMN] = "United Kingdom"
carbon_df.loc[carbon_df[COUNTRY_COLUMN] == "US", COUNTRY_COLUMN] = "United States"
carbon_df.loc[carbon_df[COUNTRY_COLUMN] == "WORLD", COUNTRY_COLUMN] = "World"
carbon_df = carbon_df[carbon_df[COUNTRY_COLUMN].isin(countries_carbon)]
carbon_df.rename(columns={"MtCO2 per day": "MtCO2", "date": DATE_COLUMN}, inplace=True)


def merge_dicts(x):
    return {k: v for d in x.dropna() for k, v in d.items()}


carbon_df[POWER_COLUMN] = carbon_df.apply(lambda x: {x['sector']: x['MtCO2']}, axis=1)
carbon_df.drop(columns=['sector', 'MtCO2'], inplace=True)

carbon_df = carbon_df.groupby([DATE_COLUMN, COUNTRY_COLUMN], as_index=False).agg({POWER_COLUMN: merge_dicts})


def map_covid_names_and_filter(data):
    data.drop(columns=["Lat", "Long", "Province/State"], inplace=True)
    data.loc[data[COUNTRY_COLUMN] == "US", COUNTRY_COLUMN] = "United States"
    # data = data[data[COUNTRY_COLUMN].isin(countries)]
    data = data.groupby(COUNTRY_COLUMN).agg(sum)
    return data


covid_confirmed_df = map_covid_names_and_filter(covid_confirmed_df)
covid_deaths_df = map_covid_names_and_filter(covid_deaths_df)
covid_recovered_df = map_covid_names_and_filter(covid_recovered_df)

date_columns = list(covid_confirmed_df.columns)
covid_dfs = {}

for col, df in {CONFIRMED_COLUMN: covid_confirmed_df, DEATHS_COLUMN: covid_deaths_df,
                RECOVERED_COLUMN: covid_recovered_df}.items():
    result = [{DATE_COLUMN: date, COUNTRY_COLUMN: country, col: df.loc[country, date]} for country in countries for date
              in date_columns]

    covid_dfs[col] = pd.DataFrame(result)

covid_df = pd.merge(covid_dfs[CONFIRMED_COLUMN], covid_dfs[DEATHS_COLUMN], how='inner',
                    on=[DATE_COLUMN, COUNTRY_COLUMN])

covid_df = pd.merge(covid_df, covid_dfs[RECOVERED_COLUMN], how='inner', on=[DATE_COLUMN, COUNTRY_COLUMN])

covid_df[DATE_COLUMN] = pd.to_datetime(covid_df[DATE_COLUMN])
carbon_df[DATE_COLUMN] = pd.to_datetime(carbon_df[DATE_COLUMN])

total_df = pd.merge(covid_df, carbon_df, how='outer', on=[DATE_COLUMN, COUNTRY_COLUMN])

total_df[DATE_COLUMN] = total_df[DATE_COLUMN].apply(lambda x: x.strftime('%Y-%m-%d'))


def row_to_dict(row):
    return {col: row[col] for col in [CONFIRMED_COLUMN, DEATHS_COLUMN, RECOVERED_COLUMN, POWER_COLUMN]}


def merge(x):
    return {row[COUNTRY_COLUMN]: row_to_dict(row) for idx, row in x.iterrows()}


dict_format = total_df.groupby(DATE_COLUMN, as_index=True).apply(merge)
dict_format = dict_format.to_dict()

json_result = json.dumps(dict_format)

with open("dataset.json", "w") as f:
    json.dump(dict_format, f)
