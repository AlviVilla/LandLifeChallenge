#!/usr/bin/env 

from flask import Flask
import pymysql
import requests
import csv
import json
import os

dirname = os.path.dirname(__file__)
with open(dirname + '/../conf/conf.json') as file:
    conf = json.load(file)

def create_DB(name):
    con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"])
    cur = con.cursor()
    cur.execute("SHOW DATABASES")
    dbs=cur.fetchall()
    if name not in str(dbs):
        cur.execute("CREATE DATABASE "+ conf["database"]["db_name"])

    cur.close()

def create_tables():

    con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"], db=conf["database"]["db_name"])
    cur = con.cursor()
    cur.execute("SHOW TABLES")
    tables=cur.fetchall()
    print(tables)
    if 'field_data' not in str(tables):
        cur.execute("CREATE TABLE field_data (individual_tree_id int, species_id int, method varchar(32), height int, health int, year_monitored int)")
    if 'species' not in str(tables):
        cur.execute("CREATE TABLE species (tree_species_id int, latin_name varchar(32))")

    cur.close()


#Retrieves data from CSV and converts in DictReader object
def data_retrieval(url):
    data = requests.get(url).content.decode('utf-8')
    if ';' in str(data):
        csv_reader = csv.DictReader(data.splitlines(), delimiter=';')
    elif ',' in str(data):
        csv_reader = csv.DictReader(data.splitlines(), delimiter=',')
    return csv_reader

def insert_in_field_data(data):
    con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"], db=conf["database"]["db_name"])
    for tab in data:
        cur=con.cursor()
        sql = """insert into field_data (individual_tree_id, species_id, method, height, health, year_monitored)
        values (%s, %s, %s, %s, %s, %s) 
        """
        cur.execute(sql,(tab["individual_tree_id"],tab["species_id"],tab["method"],tab["height"],tab["health"],tab["year_monitored"]))
    con.commit()
    con.close()

def insert_in_species(data):
    con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"], db=conf["database"]["db_name"])
    for tab in data:
        cur=con.cursor()
        sql = """insert into species (tree_species_id, latin_name)
        values (%s, %s) 
        """
        print((tab["tree_species_id"],tab["latin_name"]))
        cur.execute(sql,(tab["tree_species_id"],tab["latin_name"]))
    con.commit()
    con.close()

def read_from():
    con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"], db=conf["database"]["db_name"])
    cur = con.cursor()
    cur.execute('SELECT * FROM species')

    queryRes = cur.fetchall()
    print(queryRes)
    con.close()


create_DB(conf["database"]["db_name"])
create_tables()
f_data = data_retrieval(field_data)
specs_data = data_retrieval(species)
insert_in_field_data(f_data)
insert_in_species(specs_data)
read_from()



def cursorSelect(query):
    
    con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"])
    with con.cursor() as cur:
        cur.execute(query)
        queryRes = cur.fetchone()

    con.close()
    return str(queryRes[0])










app = Flask(__name__)

versionQ= 'SELECT VERSION()'
@app.route("/highest-trees", methods=["GET",  "POST"])
def highest_trees():
    
    return cursorSelect(versionQ)

@app.route("/best-method-for-species", methods=["GET", "POST"])
def best_method():
    return "<p>Hello, Species!</p>"

app.run(
    debug=False,
    port=conf["service_port"],
    host=conf["service_host"]
)