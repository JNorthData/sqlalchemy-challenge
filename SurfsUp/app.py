# Import the dependencies.
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

#################################################
# Database Setup
#################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users/jnorth/Documents/GitHub/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite'
db = SQLAlchemy(app)

# reflect an existing database into a new model
db.reflect()

# Access the reflected models for each table
measurement = db.classes.measurement  # Replace 'Item' with the actual name of your table

# Now you can use the 'Item' class to query and manipulate data
items = db.session.query(Item).all()
# reflect the tables



# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################


if __name__ == '__main__':
    app.run()