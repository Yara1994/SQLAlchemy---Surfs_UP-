# Import Dependencies

import datetime as dt
import numpy as np  
import pandas as pd  

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a base, using "automap_base()"

Base = automap_base()

# Use the Base class to reflect the database tables

Base.prepare(engine, reflect = True)

# Print all of the classes mapped to the Base

Base.classes.keys()

# Give the names to our classes

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session to make queries

session = Session(engine)

# Create an app

app = Flask (__name__)

# Index route

@app.route("/")
def welcome():
    print("Home page")
    return (
        f"Welcome!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"* /api/v1.0/precipitation - last 12 month of precipitation"
        f"<br/>"
        f"* /api/v1.0/stations"
        f"<br/>"
        f"* /api/v1.0/tobs"
        f"<br/>"
        f"* /api/v1.0/<start>"
        f"<br/>"
        f"* /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Design a query to retrieve the last 12 months of precipitation data and plot the results

    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    max_date = dt.date(2017, 8, 23)

    #year_ago = dt.datetime(year=max_date.year-1, month=max_date.month, day=max_date.day).date()

    year_ago = max_date - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores

    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # Convert list of tuples into normal list
    precipitation = dict(query)

    return jsonify(precipitation)

























if __name__ == "__main__":
    app.run(debug = True)

