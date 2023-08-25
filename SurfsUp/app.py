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


os.chdir(os.path.dirname(os.path.realpath(__file__)))


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Create our session (link) from Python to the DB


# don't use global variable ^


# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# create Flask app
app = Flask(__name__)


@app.route("/")
def home():
    routes = [rule.rule for rule in app.url_map.iter_rules() if "static" not in rule.rule]
    routes_html = "\n".join([f"<p style='font-size: 30px;'>{url}</p>" for url in routes])
    return render_template("home.html", routes_html=routes_html)


@app.route("/api/v1.0/station")
def display_station():
    session = Session(engine)




    session.close()
    return jsonify()


@app.route("/api/v1.0/measurement")
def display_measurement():
    session = Session(engine)

    # Find the most recent date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

    # Calculate the date one year previous
    last_date = dt.date.fromisoformat(most_recent_date)
    one_year_previous = last_date - dt.timedelta(days=365)

    # Query data from Measurement table 
    row_data = session.query(Measurement.date, func.avg(Measurement.prcp))\
        .filter(Measurement.date > one_year_previous)\
        .group_by(Measurement.date)\
        .order_by(Measurement.date)\
        .all()

    measurements = {}
    for r in row_data:
        measurements[r[0]] = r[1]

    session.close()
    return jsonify(measurements)

app.run()