![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Coverage Status](https://coveralls.io/repos/github/kelvinndmo/send/badge.svg?branch=develop)](https://coveralls.io/github/kelvinndmo/send?branch=develop)
[![Build Status](https://travis-ci.org/kelvinndmo/send.svg?branch=challenge-3-develop)](https://travis-ci.org/kelvinndmo/send)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d5b456c6aa5a4648a45f2c72346dba4a)](https://www.codacy.com/app/kelvinndmo/send?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kelvinndmo/send&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/a236552c6eda78af4c69/maintainability)](https://codeclimate.com/github/kelvinndmo/send/maintainability)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

## SendIT
- SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides      courier quotes based on weight categories.

### Required Features
- Users can create an account and log in.
- Users can create a parcel delivery order.
- Users can change the destination of a parcel delivery order.
- Users can cancel a parcel delivery order.
- Users can see the details of a delivery order.
- Admin can change the status and present location of a parcel delivery order.

### Additional Features
- The application should display a Google Map with Markers showing the pickup location and the destination.
- The application should display a Google Map with a line connecting both Markers (pickup location and the     destination).
- The application should display a Google Map with computed travel distance and journey duration between the   pickup location and the destination.
- The user gets real-time email notification when Admin changes the status of their parcel.
- The user gets real-time email notification when Admin changes the present location their parcel.

### NB:

- The user can only cancel or change the destination of a parcel delivery when the parcel’s status is yet to   be marked as delivered.
- Only the user who created the parcel delivery order can cancel the order.
## Prerequisite

- [Python3.6](https://www.python.org/downloads/release/python-365/)
- [Virtual Environment](https://virtualenv.pypa.io/en/stable/installation/)
- [Flask](http://flask.pocoo.org/)
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)

## Technologies & Languages

**Project management (Agile)** [https://www.pivotaltracker.com](url)

**Version control (Git)** [https://git-scm.com/](url)

# Installation and Setup

Clone the repository below

```
git clone https://github.com/kelvinndmo/send.git
```

### Create and activate a virtual environment

    virtualenv env --python=python3.6

    source env/bin/activate

### Install required Dependencies

    pip install -r requirements.txt

## Running the application

```bash
$ export FLASK_APP="run.py"
$ export FLASK_DEBUG=1
$ export APP_SETTINGS="development"
```
### Open Terminal and type
$ flask run

### Open postman and use the below endpoints.


## Endpoints Available

| Method | Endpoint                        | Description                           | Roles         |
| ------ | ------------------------------- | ------------------------------------- | ------------  |
| POST   | /api/v1/auth/signup             | sign up a user                        | users         |
| POST   | /api/v1/parcels                 | post a parcel order                   | users         |
| GET    |/api/v1/orders/users/<id>/parcels| Get as specific users orders          | users/admin   |
| GET    | /api/v1/parcels/acceptedorders  | get accepted parcel orders            | User          |
| GET    | /api/v1/parcels/declined        | return a list of declined orders      |user           |
| PUT    |/api/v1/parcels/1/declined       | Decline a specific order              | Admin         |
| PUT    | /api/v1/parcels/<id>/cancel     | cancel a spefic order                 | Users         |
| POST   | /api/v1/auth/login              | Login to the application              | Users/Admin   |
| GET    | /api/v1/parcels/<id>            | Get a specific order by id            | user/Admin    |
| GET    | api/v1/parcels/intransit        | get orders in transit                 | Admin/users   |
| DELETE | /api/v1/parcels/<id>            | delete a specific order               | Admin/users   |
| PUT    | /api/v1/parcels/<id>/ompleted   | complete an order                     | Admin         |
| PUT    | /api/v1/parcels/<id>/intransit  | approve an order to be in transit     | Admin         |
| PUT    | /api/v1/parcels/<id>/approved   | approve a pending order               | Admin         |
| GET    | /api/v1/parcels                 | Get a list of all orders              | Admin/users            |

### Testing

### Testing

    nosetests

    - Testing with coverage

    nosetests --with-coverage --cover-package=app

### Author

Kelvin Onkundi Ndemo

## License

MIT


