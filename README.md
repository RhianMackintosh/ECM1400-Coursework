## README

## Introduction

This program is a simple COVID dashboard that can be personalised. It displays current COVID data, taken from the Public Heath England API as well as news articles containing certain COVID terms.
It also allows you to schedule updates. 

## Prerequisites

This program was developed using Python 3.7 with Pycharm on a windows machine.
The program uses the following modules that will have to be installed seperatley (see next section):

* Flask (v.2.0.2)
* uk-covid19 (v.1.2.2)

Other modules used in the program:

* requests
* datetime
* sched
* time

## Intstallation

Using the command line and pip, install the following packages:

* flask -> pip install flask
* uk_covid19 -> pip install uk-covid19

## Getting started
1. Download the project files
2. Install all of the rerequisites mentioned above
3. Access the newsapi website and retrieve you're free API key
4. Open the config file and replace any relavent infomation with your own
5. Run the program using the flask_server_side.py file
6. The dashboard will run locally on: http://127.0.0.1:5000/ 

## Testing

## Details

Author: Rhian Mackintosh
Date: 10/12/21

Special thanks: Dr Matt Collision - University of Exeter 2021

## Licence
