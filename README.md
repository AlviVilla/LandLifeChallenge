# LandLifeChallenge


## Getting Started

The purpose of this document is to explain what technologies has been used and how to prepare the environment to get the service running.

### Pre-Requisites

In this case the operator of the code should have an instance of a mySQL server instance running locally or deployed to be pointed at. Note that the service will perform operations against it to create a DB aswell as to tables to ingest the data provided.

The API is developed in python which will require to have the latest version installed in the machine. It will also make use of some PyPI libraries that are referenced in the 'requirements.txt' file.

### Python3 Installation

Check if Python3 is installed in your machine
`python3 --version`
If not, proceed to install it in your environment
`sudo apt-get update`
Recommended to use the version 3.6 for avoiding version conflicts, noting also that the installation for this version include the third-party package `pip3`
`sudo apt-get install python3.6`

### Local MySQL in Linux Ubuntu

Installing MariaDB Server into Linux Ubuntu
`sudo apt update`
`sudo apt install mariadb-server`
`sudo apt install mariadb-client-core-10.1`

Check your installation by running 
`sudo mysql`

If you can access the server, you should be able to create a user and pwd as follows:
`CREATE USER '<your-username>'@'localhost' IDENTIFIED BY '<your-password>';`
and grant access to create databases by typing:
`GRANT ALL PRIVILEGES ON *.* TO '<your-username>'@'localhost';`


### Cloning the repository

`git@github.com:AlviVilla/LandLifeChallenge.git`
`cd LandLifeChallenge`

### Installing Python dependencies

`pip3 install -r src/requirements.txt`

## Configuration and Deployment

Once the requisites are fullfilled, the only steps left would be to update the configuration file in `conf/conf.json` with the database info and run the main script to deploy the service.

`python3 src/main.py`


## Test and Validation

The service will be running in `localhost` by default, under the port `5555` altough this value can be changed in the configuration file.
In order to test the endopints, both GET and POST methods are allowed so just by accessing the http://localhost:5555/highest-trees and followed by the corresponding parameter, in this case the year. i.e:  http://localhost:5555/highest-trees/2018 should list the top 5 ocurrences of the dataset with the higher altitude in 2018. 
Note that if no value is selected there is a default seted to show up the ones from 2021.
The second endpoint accessible is located in http://localhost:5555/best-method-for-species which by default will prompt the list of the ocurrences with the best methods for a given species, in this case the tree with the id 281. In order to specify the desired tree specie just need to add the id at the end of the enpoint, same as the example above. i.e: http://localhost:5555/best-method-for-species/280
