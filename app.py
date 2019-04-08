import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///hawaii.sqlite")
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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/><br/>"
        f"Available routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        #f"/api/v1.0/precipitation_2<br>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/temp_observations"
    )


@app.route("/api/v1.0/precipitation")
def precip_1():
    """Return a list of dates and precipitation values"""
    
    sel_nogb = [Measurement.date,
        Measurement.prcp]

    precip_totals_ngb = session.query(*sel_nogb).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
    precip_dict = {date:prcp for date, prcp in precip_totals_ngb}

    return jsonify(precip_dict)


# @app.route("/api/v1.0/precipitation_2")
# def precip_2():
#     """Return a list of dates and precipitation values"""
#     # Query all passengers
#     precip_results = session.query(Measurement.date, Measurement.prcp).all()

#     # Create a dictionary from the row data and append to a list of dates & precip values
#     all_precip_values = []
#     for date, prcp, in precip_results:
#         precip_dict = {}
#         precip_dict["date"] = date
#         precip_dict["prcp"] = prcp
#         all_precip_values.append(precip_dict)

#     return jsonify(precip_dict)


@app.route("/api/v1.0/station")
def station():
    """Return a list of stations from that data set"""
    # Query all stations
    station_names = session.query(Station.station, Station.name).all()
    # Convert list of tuples into normal list
    all_station_names = list(np.ravel(station_names)) 

    return jsonify(all_station_names)


@app.route("/api/v1.0/temp_observations")
def tobs():
# filter Measurement based on lat year of data
    sel_tobs = [Measurement.date,
        Measurement.tobs]

    tobs_freq = session.query(*sel_tobs).\
    filter(Measurement.date > '2016-08-23').\
    filter(Measurement.station == 'USC00519397').\
    order_by(Measurement.date).all()
    tobs_dict = {date:tobs for date, tobs in tobs_freq}

    return jsonify(tobs_dict)

if __name__ == '__main__':
    app.run(debug=True)
