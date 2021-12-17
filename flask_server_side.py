# the flask side of the dashboard
from flask import Flask, render_template, request
from covid_data_handler import covid_API_request
from covid_news_handling import news_API_request
import logging

app = Flask(__name__)

logging.basicConfig(filename="logging.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")
logging = logging.getLogger(__name__)


news = news_API_request()
closed_news = []


def removing_news():
    """
    This function removes a news article if it has been 'deleted' from the page

    :return: the new news list without the article
    """
    article = request.args.get('notif')
    logging.info("Request to close news article made")
    closed_news.append(article)

    for article in news:
        if article['title'] in closed_news:
            news.remove(article)
            logging.info("news article removed from news list")

    return news


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def dashboard():
    """
    This function deals with the server side of the flask application

    :return: render the html page
    """
    logging.info("client accessed either route")
    deaths, hospitalCases, natWeekAva = covid_API_request('England', 'Nation')
    locAva = covid_API_request()[2]
    logging.info("covid data API requests made")
    updateSchedules = []

    hospitalCases = "National hospital cases:", str(hospitalCases)
    deaths = "National death total: ", str(deaths)

    # load the page initially
    if request.method == 'GET':

        # if a form has been submitted
        # if request.method == 'POST':
        text_field = request.args.get('two')
        if text_field:
            update_time = request.args.get('update')
            covid_data = request.args.get('covid-data')
            news_update = request.args.get('news')
            repeat = request.args.get('repeat')

            # schedules = {}
            # schedules.update(update_time,covid_data,news_update,repeat)
            # updateSchedules.append(schedules)

            # use workshop 4 to convert to hhmmss, and to find the current time
            logging.debug("schedule to be update at: "+update_time+" ,Name: "+text_field+" To update: " +
                          covid_data+" " + news_update+" "+repeat)
            # schedule_add_news

        return render_template('index.html', title='Smart Covid Dashboard', news_articles=news, deaths_total=deaths,
                               hospital_cases=hospitalCases, national_7day_infections=natWeekAva,
                               local_7day_infections=locAva, updates=updateSchedules, image='covidPic.jpg',
                               notif=removing_news())


app.run()
