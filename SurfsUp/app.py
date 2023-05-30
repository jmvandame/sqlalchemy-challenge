# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
base = automap_base()
base.prepare(autoload_with=engine, reflect=True)
# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station
# Create our session (link) from Python to the DB
session = Session(bind=engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

#create app route for the welcome page
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br/>   
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/yyyy-mm-dd<br/>
    /api/v1.0/yyyy-mm-dd/yyyy-mm-dd</p><br/>
    ''') 
#create app route for precipitation data
@app.route("/api/v1.0/precipitation")

def precipitation():
   first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= first_date).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station, Station.name).all()
    station_dict = {results[i][0]: results[i][1] for i in range(len(results))}
    return jsonify(station_dict)


@app.route("/api/v1.0/tobs")
    
def temp_monthly():
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= first_date).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/<start>")
def start(start):
    # create session (link) from Python to the DB
    session = Session(bind=engine)
    # Query for the minimum temperature, the average temperature, and the maximum temperature for a specified start date
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    # Create a dictionary from the row data and add key/value pairs
    temp_dict = {"Minimum Temperature": temp_data[0][0], "Average Temperature": round(temp_data[0][1], 2), "Maximum Temperature": temp_data[0][2]}
    # close session
    session.close()
    return jsonify(temp_dict)
# design start/end route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # create session (link) from Python to the DB
    session = Session(bind=engine)
    # Query for the minimum temperature, the average temperature, and the maximum temperature for a specified start and end date
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Create a dictionary from the row data and add key/value pairs
    temp_dict = {"Minimum Temperature": temp_data[0][0], "Average Temperature": round(temp_data[0][1], 2), "Maximum Temperature": temp_data[0][2]}
    return jsonify(temp_dict)
    # close session
    session.close()
if __name__ == "__main__":
    app.run(debug=True)