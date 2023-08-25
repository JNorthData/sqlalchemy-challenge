# Dependencies
import sqlalchemy
from flask import Flask, jsonify, render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Create our session (link) from Python to the DB
session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Get the table names from the database
table_names = Base.classes.keys()

# Save references to each table
M_base = Base.classes.measurement
S_base = Base.classes.station

# Import Measurement data
measure_col_names = [column.key for column in M_base.__table__.columns]
measure_rows = session.query(M_base).all()
measure_data = [m.__dict__ for m in measure_rows]
Measurement = pd.DataFrame(measure_data, columns=measure_col_names)

# Import Station data
station_col_names = [column.key for column in S_base.__table__.columns]
station_rows = session.query(S_base).all()
station_data = [s.__dict__ for s in station_rows]
Stations = pd.DataFrame(station_data, columns=station_col_names)

# create Flask app
app = Flask(__name__)


@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page, homey!"

@app.route("/second")

def second():
    print("Server received request for SECOND page...")
    return "Welcome to the SECOND page!"

@app.route("/measurement")
def display_measurement():
    mcol = Measurement.columns.tolist()  # Get column names
    mrows = Measurement.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
    return render_template("measurement.html", columns=mcol, rows=mrows)

@app.route("/station")
def display_station():
    scol = Station.columns.tolist()  # Get column names
    srows = Station.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
    return render_template("station.html", columns=scol, rows=srows)


app.run()