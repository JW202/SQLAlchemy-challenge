from unittest import result
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
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


# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

# precipation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
   
    all_prcp= []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        all_prcp.append(measurement_dict)

    return jsonify(all_prcp)

# station route
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    results = session.query(Station.name, Station.station).all()
    session.close()
  

    # Create a dictionary from the row data and append to a list of stations
    all_stations = []
    for name, station in results:
        station_dict = {}
        station_dict["station id"] = station
        station_dict["station name"] = name
        
        all_stations.append(station_dict)

    return jsonify(all_stations)

# Tobs route
@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    sel = [Measurement.date, Measurement.tobs]
    one_year_ago = dt.date(2017,8,23)- dt.timedelta(days=365)
    results = session.query(*sel).filter(func.strftime(Measurement.date) >= one_year_ago).order_by(Measurement.date).all()
    session.close()

    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temp"] = tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

# start date route
@app.route("/api/v1.0/<start>")
def start(start):
 
    session = Session(engine)
    sel = [Measurement.date,Measurement.tmin,Measurement.tavg, Measurement.tmax]
    
    results = session.query(*sel).filter\
               (func.strftime(Measurement.date) >= start)\
               .order_by(Measurement.date).all()
    
    session.close()
    
    start_tobs = {}
    
    for date, tmin, tavg, tmax in results:
        

        tmin = results.tobs.min()
        tavg = results.tobs.avg()
        tmax = results.tobs.max()
       
        start_tobs["date"] = date
        start_tobs["TMIN"] = tmin
        start_tobs["TAVG"] = tavg
        start_tobs['TMAX'] = tmax
        
        start_tobs.append(start_tobs)
        
        return jsonify(start_tobs)
    """Fetch the temperatures whose date is greater than or equal to
       the path variable supplied by the user, or a 404 if not."""

    return jsonify({"error": f"Dates after {start} not found."}), 404


# Start/end date route
@app.route("/api/v1.0/<start>/<end>")
def startend(start= None, end=None ):
    
    session = Session(engine)
    sel = [Measurement.date, Measurement.tmin,Measurement.tavg,Measurement.tmax]
    
    results = session.query(*sel).filter\
              ( (func.strftime(Measurement.date) >= start ) & ( func.strftime(Measurement.date) <= end )) \
               .order_by(Measurement.date).all()
    
    session.close()
    
    startend_tobs = {}
    
    for date, tmin, tavg, tmax in results:
        
        tmin = results.tobs.min()
        tavg = results.tobs.avg()
        tmax = results.tobs.max()

        startend_tobs["date"] = date
        startend_tobs["TMIN"] = tmin
        startend_tobs["TAVG"] = tavg
        startend_tobs['TMAX'] = tmax
        
        startend_tobs.append(startend_tobs)
        
        return jsonify(startend_tobs)


    """Fetch the temperatures whose dates are between
       the path variables supplied by the user, or a 404 if not."""

    return jsonify({"error": f"Dates between {startend} not found."}), 404



if __name__ == '__main__':
    app.run(debug=True)
