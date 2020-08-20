import requests
import json
import lxml.html as html
import unidecode
import os
import pymysql.cursors
from datetime import datetime

#'https://api.mercadolibre.com/sites/MLM/search?q=se+traspasa+tienda+abarrotes+papeleria+merceria+e+internet'
URL_EXAMPLE = 'https://api.mercadolibre.com/sites/MLM/search?q=se+traspasa+tienda+abarrotes+papeleria+merceria+e+internet'
URL_API_PREFIX_DESC = 'https://api.mercadolibre.com/items/'
URL_API_PREFIX_REVS = 'https://api.mercadolibre.com/reviews/item/'
URL_API_PREFIX_CATS = 'https://api.mercadolibre.com/categories/'

PRODUCT_ATTRIBUTES_LIST = []

##STEP 8.3 (Cont): Take the first result of the JSON list(At API_subpages)
def ML_API_Cats ( link ):
    try:
        Asking_API_cats = requests.get( link )
        if Asking_API_cats.status_code == 200:
            Query_for_cats = json.loads(Asking_API_cats.content)
   
            ##STEP 8.1.1: Print values:

            Root_Cat = str(Query_for_cats['path_from_root'][1]['name'])
            return Root_Cat
        else:
            raise ValueError(f'Error: {product_response.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)    

##STEP 8.2 (Cont): Take the first result of the JSON list(At API_subpages)
def ML_API_Revs ( link ):
    try:
        Asking_API_revs = requests.get( link )
        if Asking_API_revs.status_code == 200:
            Query_for_revs = json.loads(Asking_API_revs.content)
   
            ##STEP 8.1.1: Print values:

            P_Rtg_av = float(Query_for_revs['rating_average'])
            #print(P_Rtg_av)
            #P_Rtg_5s = int(Query_for_revs['rating_levels']['one_star'])
            #P_Rtg_4s = int(Query_for_revs['rating_levels']['two_star'])
            #P_Rtg_3s = int(Query_for_revs['rating_levels']['three_star'])
            #P_Rtg_2s = int(Query_for_revs['rating_levels']['four_star'])
            #P_Rtg_1s = int(Query_for_revs['rating_levels']['five_star'])
            
            P_Total_rws = int(Query_for_revs['paging']['total'])

            Rev_Vector = (P_Rtg_av, P_Total_rws)

            return Rev_Vector
        else:
            raise ValueError(f'Error: {product_response.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

##STEP 8.1 (Cont): Take the first result of the JSON list(At API_subpages)
def ML_API_Desc ( link ):
    try:
        Asking_API_att = requests.get( link )
        if Asking_API_att.status_code == 200:
            Query_for_att = json.loads(Asking_API_att.content)
   
            ##STEP 8.1.1: Print values:
            try:
                first_key= unidecode.unidecode(str(Query_for_att['attributes'][0]['name']))
                second_key= unidecode.unidecode(str(Query_for_att['attributes'][1]['name']))
                third_key= unidecode.unidecode(str(Query_for_att['attributes'][2]['name']))
                fourth_key= unidecode.unidecode(str(Query_for_att['attributes'][3]['name']))
                P_Desc = {f'{first_key}': unidecode.unidecode(str(Query_for_att['attributes'][0]['value_name'])),
                f'{second_key}': unidecode.unidecode(str(Query_for_att['attributes'][1]['value_name'])),
                f'{third_key}': unidecode.unidecode(str(Query_for_att['attributes'][2]['value_name'])),
                f'{fourth_key}': unidecode.unidecode(str(Query_for_att['attributes'][3]['value_name']))}
                
                #Turn P_Desc (Diactionary) into a string
                String_Dic_Desc = json.dumps(P_Desc)
            except IndexError:
                String_Dic_Desc = 'There is not enough information about this product'
            
            #print(String_Dic_Desc)
            return String_Dic_Desc
        else:
            raise ValueError(f'Error: {product_response.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

##STEP 7.0: Take the first result of the JSON list (At API_page)
def ML_API_Parsing ( link ):
    try:
        Asking_API_req = requests.get( link )
        if Asking_API_req.status_code == 200:
            Query = json.loads(Asking_API_req.content)
   
            ##STEP 8.0: Get Identifiations from the first result:
            S_Id = str(Query['results'][0]['site_id'])     #Site_ID
            #print(f'Site ID = {S_Id}')
            P_Id = str(Query['results'][0]['id'])          #Product ID
            #print(f'Product ID = {P_Id}')
            C_Id = str(Query['results'][0]['category_id']) #Category ID
            #print(f'Category ID = {C_Id}')

            ##NOTE: To save time, this information may be extracted from STEP 8.1

            Prod_URL = str(Query['results'][0]['permalink']) #Category ID
            print(f'Product URL = {Prod_URL}')
            PRODUCT_ATTRIBUTES_LIST.append(Prod_URL)

            P_Title = str(Query['results'][0]['title'])     #Product Title
            print(f'Product Title = {P_Title}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Title)

            P_Image_src = str(Query['results'][0]['thumbnail'])     #Product Image
            print(f'Product URL Image = {P_Image_src}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Image_src)

            P_Currency = str(Query['results'][0]['currency_id']) #Casting Error
            print(f'Currency = {P_Currency}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Currency)

            try: #This will happening when the main price is not defined
                P_Main_price = float(Query['results'][0]['price'])  #Current Pricce
                print(f'Current Price = {P_Main_price}')
                #PRODUCT_ATTRIBUTES_LIST.append(P_Main_price)
            except TypeError:
                P_Main_price = None  #Current Pricce
                print(f'Current Price = {P_Main_price}')
                #PRODUCT_ATTRIBUTES_LIST.append(P_Main_price)
            
            try:
                P_Old_price = float(Query['results'][0]['original_price'])
                print(f'Old Price = {P_Old_price}')
                #PRODUCT_ATTRIBUTES_LIST.append(P_Old_price)
            except TypeError:
                P_Old_price = None
                print(f'Old Price = {P_Old_price}')
                #PRODUCT_ATTRIBUTES_LIST.append(P_Old_price)

            #P_Discount = float((1-(P_Old_price/P_Main_price))*100) #Real Discount
            #print(P_Discount)
            #PRODUCT_ATTRIBUTES_LIST.append(P_Discount)
            
            P_Conds = str(Query['results'][0]['condition']) #Product Conditions
            print(f'Product Condition = {P_Conds}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Conds)
            
            Qty_Sold = int(Query['results'][0]['sold_quantity']) #Quantity Sold
            print(f'Quantity Sold = {Qty_Sold}')
            PRODUCT_ATTRIBUTES_LIST.append(Qty_Sold)

            ##NOTE: To save time, information above may be extracted from STEP 8.1

            ## STEP 8.1: Take the desc information
            url_atributes = URL_API_PREFIX_DESC + P_Id
            P_Desc = ML_API_Desc(url_atributes) #Product
            print(f'Product Description = {P_Desc}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Desc)

            ##STEP 8.2: Take the reviews information
            url_revs = URL_API_PREFIX_REVS + P_Id
            Rev_Vector = ML_API_Revs(url_revs)
            print(f'Product Average Rating = {Rev_Vector[0]}')
            print(f'Total of Reviews = {Rev_Vector[1]}')
            PRODUCT_ATTRIBUTES_LIST.append(Rev_Vector[0])
            PRODUCT_ATTRIBUTES_LIST.append(Rev_Vector[1])

            ##STEP 8.3: Take the category information
            url_cats = URL_API_PREFIX_CATS + C_Id
            Root_Cat = ML_API_Cats(url_cats)
            print(f'Product Category = {Root_Cat}')
            PRODUCT_ATTRIBUTES_LIST.append(Root_Cat)

            ##STEP 9.0: Insertion to Database
            #print('\n')
            #print(f'Insertion of product: {} . To the database')
            #Database_Insertion ( PRODUCT_ATTRIBUTES_LIST )
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            #print('\n')
            #PRODUCT_ATTRIBUTES_LIST.clear()
        else:
            raise ValueError(f'Error: {product_response.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

def run():
    ML_API_Parsing ( URL_EXAMPLE )

if __name__ == '__main__':
    run()
