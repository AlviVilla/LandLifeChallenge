#!/usr/bin/env

from flask import Flask
from db_handler import DB_Handler
import json
import os

#   Define the configuration file location and parse to dict
dirname = os.path.dirname(__file__)
with open(dirname + '/../conf/conf.json') as file:
    conf = json.load(file)

#   Create new DB instance and initialize DB class
db= DB_Handler(conf)


app = Flask(__name__)

@app.route("/highest-trees", methods=["GET",  "POST"], defaults={'year': 2021})
@app.route("/highest-trees/<year>", methods=["GET",  "POST"])
def highest_trees(year):
    """Method to define the highest-trees endpoint
    Accepted Operations: GET, POST
    Available endpoints:
        /highest-trees/<year>
    Default functionallity:
        The endpoint will be exposed with a default value of year: 2021
    Returns list of highest trees and year in JSON format
    """
    query= 'SELECT * FROM field_data WHERE year_monitored = '+str(year)+' ORDER BY height DESC LIMIT 5'
    result=db.cursor_select(conf,query)
    print(result[0][-1])
    return db.read_highest(result)

@app.route("/best-method-for-species", methods=["GET", "POST"],  defaults={'species_id': 281})
@app.route("/best-method-for-species/<species_id>", methods=["GET", "POST"])
def best_method(species_id):
    """Method to define the best method endpoint
    Accepted Operations: GET, POST
    Available endpoints:
        /best-method-for-species/<species_id>
    Default functionallity:
        If no species_id is specified, defaults to 281
    Returns list in JSON format
    """
    query= 'SELECT method, AVG (health) from field_data  WHERE species_id = '+str(species_id)+' GROUP BY method, species_id ORDER BY AVG(health) DESC LIMIT 1'
    first_match = db.cursor_select(conf, query)
    query2= 'SELECT * FROM field_data LEFT JOIN species ON field_data.species_id=species.tree_species_id WHERE species_id = '+str(species_id)+' AND method = "'+str(first_match[0][0])+'"'
    second_match = db.cursor_select(conf, query2)
    return db.read_best_method(first_match, second_match)

#   Run the Flask application
app.run(
    debug=False,
    port=conf["service_port"],
    host=conf["service_host"]
)