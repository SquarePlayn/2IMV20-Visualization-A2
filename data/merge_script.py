import pandas as pd
import json
from copy import deepcopy

DATE_COLUMN = 'Date'
COUNTRY_COLUMN = 'Country'
CONFIRMED_COLUMN = 'Confirmed'
DEATHS_COLUMN = 'Deaths'
RECOVERED_COLUMN = 'Recovered'
POWER_COLUMN = 'Emissions'
LAT_COLUMN = 'Lat'
LONG_COLUMN = 'Long'

ROLLING_SUFFIX = "Rolling"

MOVING_WINDOW_SIZE = 14

COUNTRIES = ["Brazil", "China", "France", "Germany", "India", "Italy", "Japan", "Russia", "Spain", "United Kingdom",
             "United States"]


def create_covid_df() -> pd.DataFrame:
    """"Returns a dataframe containing the required COVID data."""

    covid_confirmed_df = pd.read_csv("time_series_covid19_confirmed_global.csv"). \
        rename(columns={"Country/Region": COUNTRY_COLUMN})
    covid_deaths_df = pd.read_csv("time_series_covid19_deaths_global.csv"). \
        rename(columns={"Country/Region": COUNTRY_COLUMN})
    covid_recovered_df = pd.read_csv("time_series_covid19_recovered_global.csv"). \
        rename(columns={"Country/Region": COUNTRY_COLUMN})

    def map_covid_names_and_filter(data):
        data.drop(columns=["Province/State", "Lat", "Long"], inplace=True)
        data.loc[data[COUNTRY_COLUMN] == "US", COUNTRY_COLUMN] = "United States"
        data = data.groupby(COUNTRY_COLUMN).agg(sum)
        return data

    lat_long = covid_confirmed_df.groupby(COUNTRY_COLUMN, as_index=False).agg({LAT_COLUMN: max, LONG_COLUMN: max})
    lat_long.loc[lat_long[COUNTRY_COLUMN] == "US", COUNTRY_COLUMN] = "United States"

    covid_confirmed_df = map_covid_names_and_filter(covid_confirmed_df)
    covid_deaths_df = map_covid_names_and_filter(covid_deaths_df)
    covid_recovered_df = map_covid_names_and_filter(covid_recovered_df)

    dfs = {CONFIRMED_COLUMN: covid_confirmed_df, DEATHS_COLUMN: covid_deaths_df, RECOVERED_COLUMN: covid_recovered_df}
    covid_dfs = preprocess_covid_df(dfs)

    covid_df = pd.merge(covid_dfs[CONFIRMED_COLUMN], covid_dfs[DEATHS_COLUMN], how='inner',
                        on=[DATE_COLUMN, COUNTRY_COLUMN])

    covid_df = pd.merge(covid_df, covid_dfs[RECOVERED_COLUMN], how='inner', on=[DATE_COLUMN, COUNTRY_COLUMN])

    covid_df = pd.merge(covid_df, lat_long, on=[COUNTRY_COLUMN], how='left')

    # TODO: Fix date range

    return covid_df


def preprocess_covid_df(covid_dataframes):
    all_covid_countries = set(covid_dataframes[CONFIRMED_COLUMN].index)
    date_columns = list(covid_dataframes[CONFIRMED_COLUMN].columns)

    covid_dfs = {}
    for col, df in covid_dataframes.items():
        row_formatted_dicts = [{DATE_COLUMN: date, COUNTRY_COLUMN: country, col: df.loc[country, date]}
                               for country in all_covid_countries for date in date_columns]
        formatted_df = pd.DataFrame(row_formatted_dicts)

        formatted_df[DATE_COLUMN] = pd.to_datetime(formatted_df[DATE_COLUMN])

        formatted_df.sort_values(by=[COUNTRY_COLUMN, DATE_COLUMN], inplace=True)
        formatted_df.reset_index(inplace=True, drop=True)

        formatted_df[col+ROLLING_SUFFIX] = \
            formatted_df.groupby(COUNTRY_COLUMN, sort=False)[col].\
                rolling(MOVING_WINDOW_SIZE, min_periods=1).mean().reset_index(drop=True)

        covid_dfs[col] = formatted_df
    return covid_dfs


def create_carbon_df() -> pd.DataFrame:
    """Returns a Dataframe containing the Carbon Monitor data."""

    carbon_df = pd.read_excel("carbon-monitor-maingraphdatas.xls"). \
        rename(columns={"country / group of countries": COUNTRY_COLUMN})

    countries_carbon = deepcopy(COUNTRIES)
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

    carbon_df = carbon_df.groupby([DATE_COLUMN, COUNTRY_COLUMN], as_index=False).agg(
        {POWER_COLUMN: merge_dicts}
    )

    carbon_df[DATE_COLUMN] = pd.to_datetime(carbon_df[DATE_COLUMN])
    return carbon_df


def create_main_dataframe() -> pd.DataFrame:
    """Returns the combined DataFrame containing COVID data and Carbon Monitor data."""
    carbon_df = create_carbon_df()
    covid_df = create_covid_df()


    total_df = pd.merge(covid_df, carbon_df, how='outer', on=[DATE_COLUMN, COUNTRY_COLUMN])

    total_df[DATE_COLUMN] = total_df[DATE_COLUMN].apply(lambda x: x.strftime('%Y-%m-%d'))
    return total_df


def dump_json_to_disk(total_df: pd.DataFrame):
    """Dumps the total result to the disk in json format"""

    def row_to_dict(row):
        return {col: row[col] for col in [CONFIRMED_COLUMN, DEATHS_COLUMN, RECOVERED_COLUMN, POWER_COLUMN]}

    def merge(x):
        return {row[COUNTRY_COLUMN]: row_to_dict(row) for idx, row in x.iterrows()}

    dict_format = total_df.groupby(DATE_COLUMN, as_index=True).apply(merge)
    dict_format = dict_format.to_dict()

    # json_result = json.dumps(dict_format)
    with open("dataset.json", "w") as f:
        json.dump(dict_format, f)


if __name__ == "__main__":
    total_df = create_main_dataframe()

    dump_json_to_disk(total_df)
