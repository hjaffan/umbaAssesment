# Umba Assessment

Easy to deploy application with support for Postgres or SQL lite for local development.


## Pre-requisites
* Python version 3.8.2
* Flask version 1.1.2
* Environment Variables
    * GITHUB_AUTH_TOKEN (Required)
    * DATABASE_TYPE (Optional default SQLite)
    * NUMBER_OF_USERS (Optional default=150)

## Project Setup & Run SQLite

1. `git clone https://github.com/hjaffan/umbaAssessment.git`
1. `pip install -r requirements.txt`
1. Seed data by running `GITHUB_AUTH_TOKEN=<Your-Auth-Token-Here> python umba_assesment_flask/seed.py`
1. execute ` gunicorn "umba_assesment_flask:create_app()"` from repo directory
1. navigate to `http://<your-host-name/` You should see a view that displays the github users

## Project Setup & Run Posgres

1. `git clone https://github.com/hjaffan/umbaAssessment.git`
1. `pip install -r requirements.txt`
1. Seed data by running `GITHUB_AUTH_TOKEN=<Your-Auth-Token-Here> python umba_assesment_flask/seed.py`
1. execute ` gunicorn "umba_assesment_flask:create_app()"` from repo directory
1. navigate to `http://<your-host-name/` You should see a view that displays the github users

## Deploy on heroku

1. Create a new heroku application
1. Create a heroku postgres instance (Needed to persist the database)
1. Create the following environment variables
1. Add the heroku git remote
1. git push heroku master
1. navigate to `http://<your-host-name/` You should see a view that displays the github users


## Design Approach

The current implementation of this application does the following.
In order to operate this application, a DB population needs to occur. The approach taken here is an API endpoint was
created to accomplish this. The reason for this approach is that we are SQL Lite. This is a file based DB, and needs to be created
with every new deployment of the application. There were two ways to take this, either run the command via CLI,
or doing it via an endpoint as done in this implementation. 

We have tried to make as much of the code configurable as possible to minimize the need to "recompile" code

GITHUB_AUTH_TOKEN is a required variable, and the application will not work without it.
Currently, the application will return a 500 ERROR.