from covid_data_handler import *
"""
This module provides tests for the functions in the covid_data_handler module
"""


def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639, "Test failed: for csv length"
    assert type(data) == list, "Test failed: list returned from function"


def test_process_covid_csv_data():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(
        parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240299, "Test failed: number of cases in the last 7 days"
    assert current_hospital_cases == 7019, "Test failed: current number hospital cases"
    assert total_deaths == 141544, "Test failed: total number of deaths"
    assert type(last7days_cases) == int, "Test failed: data returned is int type"
    assert type(current_hospital_cases) == int, "Test failed: data returned is int type"
    assert type(total_deaths) == int, "Test failed: data returned is int type"


def test_covid_API_request():
    assert covid_API_request("Exeter", "ltla") == covid_API_request(), \
        "Test failed: API request with default values"
