## GROUP 1 Flask App

import numpy as np
import pandas as pd
import os
import csv
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import json

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from config import dbuser, dbpassword, dbhost, dbport, dbname

Base = declarative_base()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Used below for pulling data from .CSVs
#################################################

# file_path = os.path.join("Resources", "Temp_Average_Auto_Insurance_Data.csv")
# DATA = pd.read_csv(file_path)
#print(DATA['Zip_Code'].dtype) <-- this was int64

#################################################
# Database Setup
#################################################

# Create engine
engine = create_engine(f'postgresql://{dbuser}:{dbpassword}@database-1.cvmfiiilpm7y.us-east-1.rds.amazonaws.com:{dbport}/{dbname}')
Base.metadata.create_all(engine)

# Create session
from sqlalchemy.orm import Session
session = Session(bind=engine)
connection = engine.connect()

# Join the necessary table/query opt1
DATA = pd.read_sql("SELECT a.State, a.Zip_Code, a.city, a.average_auto_insurance_rate, w.Weather_Forecast, w.Weather_Description, w.Max_Temperature, w.Min_Temperature, w.Humidity FROM Auto_Insurance_Data AS a INNER JOIN Weather_Data AS w ON a.Zip_Code = w.Zip_Code", connection)

# Close session 
connection.close()

# Close session
session.close()



#################################################
# Flask Routes
#################################################
# List all available api routes for the user
@app.route("/")
def welcome():
    """Return all routes/display options available"""
    return (
        f"Welcome! Utilize this API to find Car Insurance Data by Area<br/>"
        f"Available searches are as follows:<br/>"
        f"Enter a Zip@          /api/v1.0/by_zip<br/>"
        f"Enter a City@         /api/v1.0/by_city<br/>"
        f"Enter a State@        /api/v1.0/by_state<br/>"
        f"Or, return all data@  /api/v1.0/all_data<br/>"
    )

# return the data according to zip entry
@app.route("/api/v1.0/zipcode/<by_Zip>")
def zip(by_Zip = None):
    """Return the car insurance and weather data by zip code"""
    try:
        working_zip = DATA.loc[DATA["zip_code"] == int(by_Zip)]
        zip_dict = working_zip.to_dict(orient="records")
        return jsonify(zip_dict)
    except Exception as e:
        print(e)
        return jsonify([{'error':"Something went horribly wrong, no one ever learned to drive a car in your area."}])


## flask exception resource: https://opensource.com/article/17/3/python-flask-exceptions


# return the data according to city entry
@app.route("/api/v1.0/city/<by_City>")
def city(by_City = None):
    """Return the car insurance and weather data by Zip Code"""
    
    ## Need some method in here for .lower example in justice league 
    ## looking for something similar to this: https://docs.python.org/2/library/difflib.html

    ## actually, looking for sequense matcher... 

            # for city in test:
    #     city_result = test['by_City'].replace(" ","").lower()

    #     if city_result == search_city:
    #         return jsonify(test)

    try:
        working_zip2 = DATA.loc[DATA["city"] == by_City]
        city_dict = working_zip2.to_dict(orient="records")
        return jsonify(city_dict)
    except Exception as error:
        print(error)
        return jsonify([{'error':"Something went horribly wrong; Tesla overtook your city - autopilot only = no insurance necessary."}])


# return the data according to state entry
@app.route("/api/v1.0/state/<by_State>")
def state(by_State = None):
    """Return the car insurance and weather data by State"""
    
    try:
        working_zip3 = DATA.loc[DATA["state"] == by_State]
        state_dict = working_zip3.to_dict(orient="records")
        return jsonify(state_dict)
    except Exception as error:
        print(error)
    return jsonify([{'error':"Something went horribly wrong; your state has been taken over by murder hornets - no driving for you!"}])

   
# return the data according to city entry
@app.route("/api/v1.0/all_data")
def all():
    """Return all the car insurance and weather data"""

## This displays a mess but is infact all the data! 

    all_data = DATA.to_json(orient="records")

    return jsonify(all_data)


if __name__ == "__main__":
    app.run(debug=True)
