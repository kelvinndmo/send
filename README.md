![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.org/kelvinndmo/send.svg?branch=challenge-two-develop)](https://travis-ci.org/kelvinndmo/send)
[![Coverage Status](https://coveralls.io/repos/github/kelvinndmo/send/badge.svg?branch=challenge-two-develop)](https://coveralls.io/github/kelvinndmo/send?branch=challenge-two-develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d5b456c6aa5a4648a45f2c72346dba4a)](https://www.codacy.com/app/kelvinndmo/send?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kelvinndmo/send&amp;utm_campaign=Badge_Grade)
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

### .env file
source venv/bin/activate


export FLASK_APP="run.py"
export FLASK_DEBUG=1
export APP_SETTINGS="development"




## Author

### Kelvin Onkundi Ndemo
