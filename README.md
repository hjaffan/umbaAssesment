# Umba Assesment

## Pre-requisites
* Python version 3.8.2
* Flask version 1.1.2
* Environment Variables
    * GITHUB_AUTH_TOKEN (Required)
    * NUMBER_OF_USERS (Optional default=150)
    * DB_NAME (Optional default=../instance/test.db)
## Project Setup & Run

1. `git clone https://github.com/hjaffan/umbaAssesment.git`
1. `pip install -r requirements.txt`
1. execute ` gunicorn "umba_assesment_src:create_app()"` from repo directory
1. curl `http://<your-host-name>/initialize` this steps populates the DB
1. navigate to `http://<your-host-name/` You should see a view that displays the github users


## Deploy on heroku

1. Create a new heroku application
1. Add the heroku git remote
1. git push heroku master
1. curl `http://<your-host-name>/initialize` this steps populates the DB
1. navigate to `http://<your-host-name/` You should see a view that displays the github users
