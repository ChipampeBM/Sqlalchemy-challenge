import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database Setup

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

#Precipitation 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query Precipitation 
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > dt.date(2016,8,23)).order_by(Measurement.date.asc()).all()
    precipitation_data = []
    for date, precipitation in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['precipitation'] = precipitation
        precipitation_data.append(precipitation_dict)
    
    return jsonify(precipitation_data)

#STATATIONS
@app.route("/api/v1.0/stations")
def stations():

    all_stations = session.query(Station.station).all()

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temps():
    year = dt.date(2016,8,18)
    data_results = session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.date > year).all()
    
    temps_data = []
    for date, temperature, station in data_results:
        temps_dict = {}
        temps_dict['date'] = date
        temps_dict['temperature'] = temperature
        temps_dict['station'] = station
        temps_data.append(temps_dict)
 
    return jsonify(temps_data)

if __name__ == '__main__':
    app.run(debug=True)
