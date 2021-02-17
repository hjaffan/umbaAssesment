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
Displays a list of Github users with their avatar and profile name and URL.
Exposes and API that displays 100 profiles at a time
Allows the developer to use two database types Postgres & SQLite
Covers testing of DB / Home and Profile

Why we chose to be multi-DB. In order to support deployment in Heroku, we felt we need to address the persistence question.
Heroku works in an ephemeral system, so we had to move the data outside the container. 
In order to support local development we maintained support for SQLite

## API Docs

### Base Request
* request http://<your-host-here/profiles
* response :
```
{
    "page": 0,
    "total_pages": 1, 
    "profiles": [
        {
            "avatar": "https://avatars.githubusercontent.com/u/2?v=4",
            "id": 2,
            "profile": "https://github.com/defunkt",
            "type": "User",
            "username": "defunkt"
        },
        {
            "avatar": "https://avatars.githubusercontent.com/u/3?v=4",
            "id": 3,
            "profile": "https://github.com/pjhyett",
            "type": "User",
            "username": "pjhyett"
        },....
  ]
  }
  ```
### Request with User
* request http://<your-host-here/profiles?user=defunkt
* response :
```
{
    "page": 0,
    "total_pages": 0.01,
    "profiles": [
        {
            "avatar": "https://avatars.githubusercontent.com/u/2?v=4",
            "id": 2,
            "profile": "https://github.com/defunkt",
            "type": "User",
            "username": "defunkt"
        }
    ]
   
    }
  }
  ```

### Request with Page

* request http://<your-host-here/profiles?page=1
* response :
```
{
    "page": 1,
    "total_pages": 2,
    "profiles": [
        {
            "avatar": "https://avatars.githubusercontent.com/u/2?v=4",
            "id": 2,
            "profile": "https://github.com/defunkt",
            "type": "User",
            "username": "defunkt"
        }, ......
    ]
 
    }
  }
  ```