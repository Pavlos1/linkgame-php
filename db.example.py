#!/usr/bin/env python2

import mysql.connector

def dbConnect(database):
    host = "localhost"
    username = ""
    password = ""
    
    return mysql.connector.connect(user=username, password=password,
        host=host, database=database)
