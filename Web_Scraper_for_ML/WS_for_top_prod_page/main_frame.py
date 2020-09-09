# -*- coding: utf-8 -*-

import requests
import json
import lxml.html as html
import unidecode
import os
import pymysql.cursors
import itertools
from time import sleep
from datetime import datetime
import math
import pandas as pd
import numpy as np
import sys
import re
import data_collector
import df_cleaner
import shutil
import auth_and_pass

INPUT_DIR = 'c:/Users/luisc/Desktop/Web_Scrapers/Web_Scraper_for_ML/WS_for_top_prod_page/input_files/'
MY_SQL_DIR = 'c:/ProgramData/MySQL/MySQL Server 8.0/Uploads/'
NEW_FOLDER = datetime.now( ).strftime("%d/%m/%Y %H:%M").replace("/","_").replace(" ","_").replace(":","")
LAST_WORDS = ["\n\n********** No matter what happens now **********",\
                 "\n********** You shouldn't be afraid **********",\
                 "\n********** Because I know today has been **********",\
                 "\n********** The most perfect day I've ever seen **********",\
                 "\n\n********** END OF VIDEAOTAPE! **********"]
VIDEOTAPE_TITLE = ["     _/    _/  _/_/_/  _/_/_/    _/_/_/_/    _/_/    _/_/_/_/_/    _/_/    _/_/_/    _/_/_/_/   ",\
                   "    _/    _/    _/    _/    _/  _/        _/    _/      _/      _/    _/  _/    _/  _/          ",\
                   "   _/    _/    _/    _/    _/  _/_/_/    _/    _/      _/      _/_/_/_/  _/_/_/    _/_/_/       ",\
                   "   _/  _/     _/    _/    _/  _/        _/    _/      _/      _/    _/  _/        _/            ",\
                   "     _/    _/_/_/  _/_/_/    _/_/_/_/    _/_/        _/      _/    _/  _/        _/_/_/_/       "]

def Countdown ( n = 3600 ):
    
    while n > 0 :
        pass

def Truncate_Main_table( ):
    
    connection = pymysql.connect(host = 'localhost', user = auth_and_pass.MY_SQL_ADMIN_USER, password = auth_and_pass.MY_SQL_ADMIN_PASS,
    db = 'ml_product_table', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor: 
            sql = "TRUNCATE `ml_product_table`.`pre_json`"
            cursor.execute(sql)
            connection.commit()
    except Exception as E :
        print(E)
    finally:
        connection.close()

def Turn_MySQL_Table_into_csv( ):
    
    connection = pymysql.connect(host = 'localhost', user = auth_and_pass.MY_SQL_ADMIN_USER, password = auth_and_pass.MY_SQL_ADMIN_PASS,
    db = 'ml_product_table', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor: 
            sql = "SELECT 'index', 'product_id', 'rank', 'currency', 'region', 'price', 'price_max', 'name', 'image_url', 'link', 'stars', 'reviews', 'category', 'catched_at'\
                 UNION ALL SELECT * FROM pre_json\
                 INTO OUTFILE \"C:\\\\ProgramData\\\\MySQL\\\\MySQL Server 8.0\\\\Uploads\\\\File_from_MySQL.csv\" \
                 FIELDS TERMINATED BY '^' ENCLOSED BY '' LINES TERMINATED BY '\\n'"
            cursor.execute(sql)
            connection.commit()
    except Exception as E :
        print(E)
    finally:
        connection.close()

def videotape():

    print("\n\n********** VIDEAOTAPE IS SPINING AWAY! **********")

    os.chdir( INPUT_DIR )
    if not os.path.exists(NEW_FOLDER):  #https://stackoverflow.com/questions/1274405/how-to-create-new-folder
        os.makedirs(NEW_FOLDER)

    Truncate_Main_table( )

    for index in range(6): #range(12):
        #key_maker.run()
        data_collector.run( )
        print("\n\n********** SLEEPING FOR AN HOUR! **********")
        sleep(3600) #sleep(5)
    
    Turn_MySQL_Table_into_csv( )
    shutil.move(MY_SQL_DIR + "File_from_MySQL.csv", INPUT_DIR + NEW_FOLDER + "/File_from_MySQL.csv") #https://stackoverflow.com/questions/8858008/how-to-move-a-file
    df_cleaner.run( )
    #mr_postman.run( )
    Truncate_Main_table( )

def run():
    print("\n\n")

    for words in VIDEOTAPE_TITLE :
        print( words )
        sleep(0.2)

    print("\n\n")
    print("************************************************************************************************")
    
    while True:
        turn_key = input("\n\n********** WELCOME TO VIDEOTAPE! ********** Please, press 'S' to Turn the key 🔑 .: ")
        if turn_key == 'S' or turn_key == 's':
            videotape()
            break
        else :
            print("\n\n You have pressed an incorrect key! Please, try again")
    
    for words in LAST_WORDS :
        print( words )
        sleep(0.2)

if __name__ == '__main__':
    run()