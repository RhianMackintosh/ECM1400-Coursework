from datetime import date, timedelta
from uk_covid19 import Cov19API
import sched
import time
import json
import logging


logger = logging.getLogger(__name__)

with open('config.json') as config_file:
    config_data = json.load(config_file)
    logging.info("config file data accessible")

s = sched.scheduler(time.time, time.sleep)


def parse_csv_data(csv_filename):
    """
    This function takes a csv file and returns the data in a list

    :param csv_filename: the name of the csv file to be read
    :return: the data in a list format
    """

    csv_data = []
    f = open(csv_filename, 'r')
    for line in f.readlines():
        splits = []
        for x in line.split(','):
            splits.append(x)
        csv_data.append(splits)

    return csv_data


def process_covid_csv_data(covid_csv_data):
    """
    This function process the covid data and extracts the data needed

    :param covid_csv_data: a list of data, returned from the parse_csv_data function
    :return: currentDeaths: the current number of deaths
            currentHospital: the current number of hospital admissions
            casesWeek: the total number of cases in a week
    """
    # returns three variables: no. cases in last 7 days, current no. of hospital cases, cumulative no. deaths
    week = []
    week_data = []
    cases_week = 0

    today = date(2021, 10, 26)

    for i in range(0, 7):
        week.append(str(today - timedelta(days=i)))

    for i in covid_csv_data:
        for j in week:
            if i[3] == j:
                week_data.append(i)
                cases = i[6]
                cases = cases.strip('\n')
                cases_week += int(cases)

    current_deaths = int(covid_csv_data[14][4])
    current_hospital = int(covid_csv_data[1][5])

    return cases_week, current_hospital, current_deaths


def covid_API_request(location=config_data['default_location'], location_type=config_data['default_location_type']):
    """
    This function creates an API request for the covid data

    :param location: this is the location to search for the data, e.g. uk, exeter
    :param location_type: this is the type of location, e.g. country, city
    :return: deaths: the most recent deaths
            hospitalCases: the most recent hospital cases
            natWeekAva: the national weekly avarage cases
    """
    # returns up to data covid data as a dictionary
    national_week = []
    deaths = None
    hospital_cases = None

    area_filter = ['areaType=%s' % location_type, 'areaName=%s' % location]
    cases_and_deaths = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "date": "date",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate",
        "hospitalCases": "hospitalCases",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate"
    }
    logging.info("filter and structure set up")

    api = Cov19API(filters=area_filter, structure=cases_and_deaths)
    data = api.get_json()
    logging.info("covid api data request made")

    if location_type == 'Nation':
        for i in data["data"]:
            if not i["cumDailyNsoDeathsByDeathDate"]:
                logging.debug("data entry is empty, moving onto the next entry")
                pass
            else:
                deaths = i["cumDailyNsoDeathsByDeathDate"]
                logging.debug("data entry not empty for the no. deaths, using the data")
                break

        for i in data["data"]:
            if not i["hospitalCases"]:
                logging.debug("data entry is empty, moving onto the next entry")
                pass
            else:
                hospital_cases = i["hospitalCases"]
                logging.debug("data entry not empty for the no. hospital cases, using the data")

                break

    j = 0
    for i in data["data"]:
        if not i["newCasesBySpecimenDate"]:
            logging.debug("data entry is empty, moving onto the next entry")
            pass
        elif j == 0:
            logging.debug("first data entry being skipped as data is incomplete")
            pass
        elif j > 7:
            logging.debug("week has been exceeded, breaking loop")
            break
        else:
            national_week.append(i["newCasesBySpecimenDate"])
        j += 1

    national_week_average = 0
    for i in national_week:
        national_week_average += i

    return deaths, hospital_cases, national_week_average


def schedule_covid_updates(update_interval, update_name):

    def job():
        print("update news/covid numbers")

    e1 = s.enter(update_interval, 1, job, (update_name,))
    s.run(blocking=False)
    # use the sched module to update the covid data at given time intervals
    return
