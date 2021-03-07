import numpy as np
import pandas as pd
import datetime as dt


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

 # Create our session (link) from Python to the DB
session = Session(engine)

# Find the most recent date in the data set.
recent_precip = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date one year from the last date in data set.
year_ago = (dt.datetime.strptime(recent_precip[0], '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

session.close()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Home Page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation Information</a><br/>"
        f"<a href='/api/v1.0/stations'>Weather Data Collection Station Information</a><br/>"
        f"<a href='/api/v1.0/tobs'>Temperature Information</a><br/>"
    )
      
# Precip page      
@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data for 12 month period from Analysis"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= year_ago).order_by(Measurement.date.asc()).all()

    session.close()
    print(results)

# Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitation = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precip"] = prcp
        precipitation.append(precip_dict)

# Return the JSON representation of your dictionary.
    return jsonify(precipitation)

# Station Page

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset """
    # Query all passengers
    results = session.query(Station.station, Station.name).all()

    session.close()
    print(results)

# Convert the query results to a dictionary using date as the key and prcp as the value.
    stations = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        stations.append(station_dict)

# Return the JSON representation of your dictionary.
    return jsonify(stations)

if __name__ == '__main__':
    app.run(debug=True)
