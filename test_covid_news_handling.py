from covid_news_handling import *
"""
This module provides tests for the functions in the covid_news_handling module
"""


def test_news_API_request():
    assert news_API_request() == news_API_request("Covid COVID-19 coronavirus"), "Test failed: default covid terms"
    assert isinstance(list, news_API_request()), "Test failed: list returned from news request"
