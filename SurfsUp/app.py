# Dependencies
import sqlalchemy
from flask import Flask, jsonify, render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt
import flask_sqlalchemy
import os 


# change directory to the same directory as this file. 
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# -----------------------------------------------

# create Flask app
app = Flask(__name__)

# HOME screen displays all routes
@app.route("/")
def home():
    routes = [rule.rule for rule in app.url_map.iter_rules() if "static" not in rule.rule]
    return jsonify(routes)

# show precipitation for past year
@app.route("/api/v1.0/precipitation")
def display_precipitation():
    session = Session(engine)

    # Find the most recent date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

    # Calculate the date one year previous
    last_date = dt.date.fromisoformat(most_recent_date)
    one_year_previous = last_date - dt.timedelta(days=365)

    # Query data from Measurement (1yr precipitation) table 
    precipitation = session.query(Measurement.date, func.avg(Measurement.prcp))\
        .filter(Measurement.date > one_year_previous)\
        .group_by(Measurement.date)\
        .order_by(Measurement.date)\
        .all()

    # convert results into a dictionary
    measurements = {}
    for r in precipitation:
        measurements[r[0]] = r[1]

    session.close()
    return jsonify(measurements)

# list all stations
@app.route("/api/v1.0/stations")
def display_stations():
    session = Session(engine)

    s_data = session.query(Station.station, Station.name).all()
    
    # convert results into a dictionary
    stations = {}
    for r in s_data:
        stations[r[0]] = r[1]

    session.close()
    return jsonify(stations)

# past year temperature observations from most active station
@app.route("/api/v1.0/tobs")
def display_tobs():
    session = Session(engine)

    # determine most recent date and previous 1-year window
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    last_date = dt.date.fromisoformat(most_recent_date)
    one_year_previous = last_date - dt.timedelta(days=365)

    # query tobs from only most active station, previous 1-year window
    most_active_data = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == 'USC00519281')\
        .filter(Measurement.date > one_year_previous)\
        .all() 
       
    # convert results into a dictionary
    temp_obs = {}
    for r in most_active_data:
        temp_obs[r[0]] = r[1]

    session.close()
    return jsonify(temp_obs)

# display temperature stats, aggregated from a beginning date
@app.route("/api/v1.0/<start>")
def display_from(start):
    session = Session(engine)

    # query stats from all dates after <start>
    most_active_stats = session.query(
        func.min(Measurement.tobs).label('mas_lo'),
        func.max(Measurement.tobs).label('mas_hi'),
        func.avg(Measurement.tobs).label('mas_avg'))\
        .filter(Measurement.date >= start)\
        .all()
    
    mas_lo, mas_hi, mas_avg = most_active_stats[0]

    session.close()
    return jsonify({
        'min_temperature': mas_lo,
        'avg_temperature': mas_avg,
        'max_temperature': mas_hi
    })
  
# display temperature stats, aggregated between a start and an end date
@app.route("/api/v1.0/<start>/<end>")
def display_between(start, end):
    session = Session(engine)

    # query stats for all dates between <start> and <end> dates.
    most_active_stats = session.query(
        func.min(Measurement.tobs).label('mas_lo'),
        func.max(Measurement.tobs).label('mas_hi'),
        func.avg(Measurement.tobs).label('mas_avg'))\
        .filter(Measurement.date >= start, Measurement.date <= end)\
        .all()
    
    mas_lo, mas_hi, mas_avg = most_active_stats[0]

    session.close()
    
    return jsonify({
        'min_temperature': mas_lo,
        'avg_temperature': mas_avg,
        'max_temperature': mas_hi
    })


if __name__ == "__main__":
    app.run()