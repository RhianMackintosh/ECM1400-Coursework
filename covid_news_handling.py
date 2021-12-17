import requests
from covid_data_handler import *
import logging

logger = logging.getLogger(__name__)


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    """
    This function deals with the news API request

    :param covid_terms: the terms to search the news articles with
    :return: a list of news articles
    """

    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = config_data['apikey']
    country = "gb"
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    response = requests.get(complete_url)
    news_dict = response.json()
    logging.info("news request made")

    search_terms = covid_terms.split(" ")
    news = []
    remove = ['source', 'url', 'author', 'description', 'urlToImage', 'publishedAt']

    articles = news_dict["articles"]
    for article in articles:
        covid_articles = {}
        for i in search_terms:
            if i.lower() in article['title'].lower():
                covid_articles.update(article)

                for j in remove:
                    covid_articles.pop(j)

                news.append(covid_articles)
                break
    return news
