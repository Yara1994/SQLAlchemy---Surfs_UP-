# Import Dependencies

import datetime as dt
import numpy as np  

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine

# engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

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
        f"* /api/v1.0/precipitation"
        f"<br/>"
        f"* /api/v1.0/stations"
        f"<br/>"
        f"* /api/v1.0/tobs"
        f"<br/>"
        f"* /api/v1.0/start_date"
        f"<br/>"
        f"* /api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    max_date = dt.date(2017, 8, 23)

    year_ago = max_date - dt.timedelta(days = 365)

    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    precipitation = dict(query)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(Station.station).all()

    list_of_stations = list(np.ravel(stations))

    return jsonify(list_of_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    maximal_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    maximal_date = dt.date(2017, 8, 23)

    one_year_ago = maximal_date - dt.timedelta(days = 365)

    tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).all()

    tobs_list = list(tobs_query)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start_date(start):

    from_start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    from_start_list = list(from_start)

    return jsonify(from_start_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

   
    from_start_to_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    from_start_to_end_list = list(from_start_to_end)

    return jsonify(from_start_to_end_list)




    
if __name__ == "__main__":
    app.run(debug = True)

