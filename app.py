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
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= year_ago).all()

    session.close()
    print(results)
    
if __name__ == '__main__':
    app.run(debug=True)
