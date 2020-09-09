import pandas as pd
import numpy as np
import os
import sys
import re
from datetime import datetime
import main_frame

BASE_FILE_DIR = 'c:/Users/luisc/Desktop/Web_Scrapers/Web_Scraper_for_ML/WS_for_top_prod_page/input_files/{}/'

def DF_From_Region( df, reg ):
    df_from_r = df[df.region.eq(reg)]
    df_from_r = df_from_r.sort_values( by = ['rank', 'region', 'category', 'catched_at'], ascending = True )
    df_from_r = df_from_r[['product_id','rank','region','currency','price', 'price_max','name', 'image_url', 'link', 'stars', 'reviews', 'category', 'catched_at']]
    dir_csv = BASE_FILE_DIR.format(name_for_dirs)+'{}_{}.csv'.format(reg, name_for_files)
    dir_json = BASE_FILE_DIR.format(name_for_dirs)+'{}_{}.json'.format(reg, name_for_files)
    df_from_r.to_csv(dir_csv, index = False, encoding='utf-8')
    df_from_r.to_json(dir_json, indent = 4)

def emergency_parcing( base_file_name ): #https://www.w3schools.com/python/trypython.asp?filename=demo_regex_sub
    pass

def Read_raw_df( base_file_name ):
    try:
        os.chdir( BASE_FILE_DIR.format( name_for_dirs ) )
        df_raw = pd.read_csv(base_file_name, sep = '^',  encoding='utf-8', index_col = False )
        #Change types
        df_raw['catched_at'] = pd.to_datetime( df_raw['catched_at'] )
        df_raw['price'] = df_raw['price'].replace( 'None',np.nan )
        df_raw['price'] = pd.to_numeric(df_raw['price'])
        df_raw['price_max'] = df_raw['price_max'].replace( 'None',np.nan )
        df_raw['reviews'] = pd.to_numeric(df_raw['reviews'])
        df_raw['stars'] = pd.to_numeric(df_raw['reviews'])
        df_raw['out_of_50'] = df_raw['rank'].apply( lambda x: True if x < 51 else False )
        df_raw = df_raw.loc[ df_raw.out_of_50 ].reset_index( drop = True )
        DF_From_Region( df_raw, 'MX' )
        DF_From_Region( df_raw, 'BR' )
        os.remove( bfile_name )

    except ParcingError as Pe:
        print(Pe)
        try:
            emergency_parcing(base_file_name)
        except Exception as Extraord:
            print(Extraord)

def run():

    global name_for_files 
    global name_for_dirs
    global bfile_name

    print("ATTENTION: THE PROCESS OF CLEANING DATAFRAME IS BEGINNING")
    pd.set_option( 'display.float_format', '{:,.2f}'.format )
    name_for_files = datetime.now().strftime("%d/%m/%Y %H:%M").replace("/","_").replace(" ","_").replace(":","") #El momento final de cada proceso, lo crea este proceso
    #name_for_files = '04_09_2020_0353'
    #name_for_dirs = datetime.now().strftime("%d/%m/%Y %H:%M").replace("/","_").replace(" ","_").replace(":","") EL primer momento, lo crea main.py
    name_for_dirs = main_frame.NEW_FOLDER
    bfile_name = 'File_from_MySQL.csv'
    Read_raw_df( bfile_name )
    print("ATTENTION: THE PROCESS OF CLEANING DATAFRAME IS COMPLETE")

if __name__ == '__main__':
    run()