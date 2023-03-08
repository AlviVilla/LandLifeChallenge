#!/usr/bin/env

import pymysql
import requests
import csv

class DB_Handler:

    def __init__(self, conf):
        self.create_DB(conf)
        self.create_tables(conf)
        f_data = self.data_retrieval(conf["data"]["field_data"])
        specs_data = self.data_retrieval(conf["data"]["species"])
        self.insert_in_field_data(conf, f_data)
        self.insert_in_species(conf, specs_data)

    def create_DB(self, conf):
        """Create a new DB if doesn't exists.
        Param: 
            conf: configuration file
        """
        con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"])
        cur = con.cursor()
        cur.execute("SHOW DATABASES")
        dbs=cur.fetchall()
        if conf["database"]["db_name"] not in str(dbs):
            cur.execute("CREATE DATABASE "+ conf["database"]["db_name"])
        cur.close()

    def create_tables(self, conf):
        """Define the tables if don't exist.
        Param: 
            conf: configuration file
        """
        con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"], db=conf["database"]["db_name"])
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        tables=cur.fetchall()
        if 'field_data' not in str(tables):
            cur.execute("CREATE TABLE field_data (individual_tree_id int, species_id int, method varchar(32), height int, health int, year_monitored int, PRIMARY KEY (individual_tree_id, year_monitored), UNIQUE (individual_tree_id, year_monitored))")
        if 'species' not in str(tables):
            cur.execute("CREATE TABLE species (tree_species_id int, latin_name varchar(32), PRIMARY KEY (tree_species_id), UNIQUE (tree_species_id))")
        cur.close()



    def data_retrieval(self, url):
        """Retrieves data from CSV and converts in DictReader object
        Params:
            url: web path where the csv is hosted
        """
        data = requests.get(url).content.decode('utf-8')
        if ';' in str(data):
            csv_reader = csv.DictReader(data.splitlines(), delimiter=';')
        elif ',' in str(data):
            csv_reader = csv.DictReader(data.splitlines(), delimiter=',')
        return csv_reader

    def insert_in_field_data(self, conf, data):
        """Insert CSV data into the field_data table
        Params:
            conf: Configuration data
            data: DictReader object with CSV data
        """
        con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"], db=conf["database"]["db_name"])
        for tab in data:
            cur=con.cursor()
            sql = """INSERT IGNORE INTO field_data (individual_tree_id, species_id, method, height, health, year_monitored)
            VALUES (%s, %s, %s, %s, %s, %s) 
            """
            cur.execute(sql,(tab["individual_tree_id"],tab["species_id"],tab["method"],tab["height"],tab["health"],tab["year_monitored"]))
        con.commit()
        con.close()

    def insert_in_species(self, conf, data):
        """Insert CSV data into the species table
        Params:
            conf: Configuration data
            data: DictReader object with CSV data
        """
        con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"], db=conf["database"]["db_name"])
        for tab in data:
            cur=con.cursor()

            sql="""INSERT IGNORE INTO species (tree_species_id, latin_name)
            VALUES (%s, %s)
            """
            cur.execute(sql,(tab["tree_species_id"],tab["latin_name"]))
        con.commit()
        con.close()

    def read_highest(self, result_tuple):
        """Formatting of the resultant SQL query to JSON for the highest trees
        Params:
            result_tuple: tuple returned by cursor
        """
        highest = []
        for a in result_tuple:
            highest.append({"individual_tree_id": a[0], "height": a[3]})
        output= {
            "year": result_tuple[0][-1],
            "highest_trees": highest
        }
        return (output)

    def read_best_method(self, result_tuple1, result_tuple2):
        """Formatting of the resultant SQL query to JSON for the best method
        Params:
            result_tuple1: first match tuple returned by cursor
                expected fields (method, average)
            result_tuple2: second match tuple returned by cursor
        """
        seen_in_list = []
        for a in result_tuple2:
            seen_in_list.append({"individual_tree_id": a[0], "year": a[-3], "health": a[4]})

        output= {
            "tree_species_id": result_tuple2[0][1],
            "tree_species_latin_name":result_tuple2[0][-1],
            "best_method":result_tuple1[0][0],
            "health_average":str(result_tuple1[0][1]),
            "seen_in":seen_in_list
        }
        return (output)


    def cursor_select(self, conf, query):
        """Method to execute query by cursor
        Params:
            conf: Configuration data
            query: String value with SQL query
        """
        con = pymysql.connect(host=conf["database"]["hostname"], user=conf["database"]["user"], password=conf["database"]["password"], db=conf["database"]["db_name"])
        with con.cursor() as cur:
            cur.execute(query)
            queryRes = cur.fetchall()

        con.close()
        return queryRes

