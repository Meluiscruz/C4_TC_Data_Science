import requests
import json
import lxml.html as html
import unidecode
import os
import pymysql.cursors
from datetime import datetime
import math

##Vars, dictionaries and lists.

Cat_dictionary = {
    1 : ['alimentos-y-bebidas', 'alimentos-e-bebidas'],
    2 : ['accesorios-para-vehiculos', 'acessórios-para-veículos'],
    3 : ['bebe', 'bebe'],
    4 : ['deportes-y-fitness', 'esportes-e-fitness'],
    5 : ['celulares-y-telefonia', 'celulares-e-telefones'],
    6 : ['electronica-audio-y-video', 'eletronicos-audio-e-video'],
    7 : ['electrodomesticos', 'eletrodomesticos'],
    8 : ['herramientas-y-construccion', 'ferramentas-e-construcao'],
    9 : ['hogar-muebles-y-jardin', 'casa-moveis-e-decoracao'],
    10 : ['industrias-y-oficinas', 'industria-e-comercio'],
    11 :['instrumentos-musicales','instrumentos-musicais'],
    12 : ['juegos-y-juguetes','brinquedos-e-hobbies'],
    13 : ['libros-revistas-y-comics','livros-revistas-e-comics'],
    14 : ['musica-peliculas-y-series', 'musica-filmes-e-seriados'],
    15 : ['arte-papeleria-y-merceria', 'arte-papelaria-e-armarinho'],
    16: ['animales-y-mascotas', 'animais'],
    17: ['ropa-bolsas-y-calzado', 'calcados-roupas-e-bolsas'],
    18: ['salud-y-equipamiento-medico','saude'],
    19: ['belleza-y-cuidado-personal', 'beleza-e-cuidado-pessoal'],
    20: ['computacion','informatica'],
    21: ['consolas-y-videojuegos', 'games']
}

URL_ML = ["https://listado.mercadolibre.com.mx/", "https://lista.mercadolivre.com.br/"]
Visual_options = ["_DisplayType_G","_DisplayType_LF"]

XPATH_PRODUCT_SENSOR = '//div/div/input[@form="productInfo"]'
XPATH_LIST_AT_MAIN_PAGE = ['//section/ol/li/div/div/div/div/ul/li/a/@href','/html/body/main//ul/li[11]/a/@href']
XPATH_TITLES_AT_PROD_PAGE = ['//div[1]/section[1]/div/header/h1/text()','//div/div/div/div[1]//h1/text()']
URL_API_PREFIX_LIST = ['https://api.mercadolibre.com/sites/MLM/search?q=','https://api.mercadolibre.com/sites/MLB/search?q=']
URL_API_PREFIX_DESC = 'https://api.mercadolibre.com/items/'
URL_API_PREFIX_REVS = 'https://api.mercadolibre.com/reviews/item/'
URL_API_PREFIX_CATS = 'https://api.mercadolibre.com/categories/'

PRODUCT_ATTRIBUTES_LIST = []

##STEP 9.0 Insertion of data to Database.

def Database_Insertion ( list_of_attributes ):
    
    connection = pymysql.connect(host = 'localhost', user = 'admin', password = 'Evil_Corp_24810_!', 
        db = 'ml_top_list', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    region =            list_of_attributes[0]
    product_url =       list_of_attributes[1]
    product_title =     list_of_attributes[2]
    product_img_src =   list_of_attributes[3]
    currency =          list_of_attributes[4]
    main_price =        list_of_attributes[5]
    old_price =         list_of_attributes[6]
    product_condition = list_of_attributes[7]
    qty_sold =          list_of_attributes[8]
    product_desc =      list_of_attributes[9]
    average_rating =    list_of_attributes[10]
    total_of_reviews =  list_of_attributes[11]
    root_category =     list_of_attributes[12]
    catched_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        with connection.cursor() as cursor: 
            sql = "INSERT INTO product_from_ml (region, product_url, product_title, product_img_src, currency,\
                    main_price, old_price, product_condition, qty_sold, product_desc, average_rating, total_of_reviews,\
                    root_category, catched_at) VALUES ('"+ region +"', '" + product_url + "','" + product_title + "',\
                    '"+ product_img_src +"', '"+ currency +"','" + main_price + "', '"+ old_price + "',\
                    '"+ product_condition + "', '"+ qty_sold + "', '"+ product_desc + "', '"+ average_rating + "',\
                    '"+ total_of_reviews + "', '"+ root_category + "', '"+ catched_at + "')"
            cursor.execute(sql)
            connection.commit()                   
    except Exception as E :
        print(E)
    finally:
        connection.close()

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

            P_Rtg_av = str(Query_for_revs['rating_average'])
            #print(P_Rtg_av)
            #P_Rtg_5s = int(Query_for_revs['rating_levels']['one_star'])
            #P_Rtg_4s = int(Query_for_revs['rating_levels']['two_star'])
            #P_Rtg_3s = int(Query_for_revs['rating_levels']['three_star'])
            #P_Rtg_2s = int(Query_for_revs['rating_levels']['four_star'])
            #P_Rtg_1s = int(Query_for_revs['rating_levels']['five_star'])
            
            P_Total_rws = str(Query_for_revs['paging']['total'])

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
   
            ##STEP 8.0: Get Identifications from the first result:
            S_Id = str(Query['results'][0]['site_id'])     #Site_ID
            if S_Id == 'MLM':
                Region = 'MX'
                PRODUCT_ATTRIBUTES_LIST.append(Region)
            elif S_Id == 'MLB':
                Region = 'BR'
                PRODUCT_ATTRIBUTES_LIST.append(Region)
            else:
                Region = 'UN'
                PRODUCT_ATTRIBUTES_LIST.append(Region)
            
            #print(f'Site ID = {S_Id}')
            P_Id = str(Query['results'][0]['id'])          #Product ID
            #print(f'Product ID = {P_Id}')
            C_Id = str(Query['results'][0]['category_id']) #Category ID
            #print(f'Category ID = {C_Id}')

            ##NOTE: To save time, this information may be extracted from STEP 8.1

            Prod_URL = str(Query['results'][0]['permalink']) #Category ID
            #print(f'Product URL = {Prod_URL}')
            PRODUCT_ATTRIBUTES_LIST.append(Prod_URL)

            P_Title = str(Query['results'][0]['title'])     #Product Title
            #print(f'Product Title = {P_Title}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Title)

            P_Image_src = str(Query['results'][0]['thumbnail'])     #Product Image
            #print(f'Product URL Image = {P_Image_src}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Image_src)

            P_Currency = str(Query['results'][0]['currency_id']) #Casting Error
            #print(f'Currency = {P_Currency}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Currency)

            try: #This will happening when the main price is not defined
                P_Main_price = str(Query['results'][0]['price'])  #Current Pricce
                #print(f'Current Price = {P_Main_price}')
                PRODUCT_ATTRIBUTES_LIST.append(P_Main_price)
            except TypeError:
                P_Main_price = None  #Current Pricce
                #print(f'Current Price = {P_Main_price}')
                PRODUCT_ATTRIBUTES_LIST.append(P_Main_price)
            
            try:
                P_Old_price = str(Query['results'][0]['original_price'])
                #print(f'Old Price = {P_Old_price}')
                PRODUCT_ATTRIBUTES_LIST.append(P_Old_price)
            except TypeError:
                P_Old_price = None
                #print(f'Old Price = {P_Old_price}')
                PRODUCT_ATTRIBUTES_LIST.append(P_Old_price)
            
            #P_Discount = float((1-(P_Old_price/P_Main_price))*100) #Real Discount
            #print(P_Discount)
            #PRODUCT_ATTRIBUTES_LIST.append(P_Discount)
            
            P_Conds = str(Query['results'][0]['condition']) #Product Conditions
            #print(f'Product Condition = {P_Conds}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Conds)
            
            Qty_Sold = str(Query['results'][0]['sold_quantity']) #Quantity Sold
            #print(f'Quantity Sold = {Qty_Sold}')
            PRODUCT_ATTRIBUTES_LIST.append(Qty_Sold)

            ##NOTE: To save time, information above may be extracted from STEP 8.1

            ## STEP 8.1: Take the desc information
            url_atributes = URL_API_PREFIX_DESC + P_Id
            P_Desc = ML_API_Desc(url_atributes) #Product
            #print(f'Product Description = {P_Desc}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Desc)

            ##STEP 8.2: Take the reviews information
            url_revs = URL_API_PREFIX_REVS + P_Id
            Rev_Vector = ML_API_Revs(url_revs)
            #print(f'Product Average Rating = {Rev_Vector[0]}')
            #print(f'Total of Reviews = {Rev_Vector[1]}')
            PRODUCT_ATTRIBUTES_LIST.append(Rev_Vector[0])
            PRODUCT_ATTRIBUTES_LIST.append(Rev_Vector[1])

            ##STEP 8.3: Take the category information
            url_cats = URL_API_PREFIX_CATS + C_Id
            Root_Cat = ML_API_Cats(url_cats)
            #print(f'Product Category = {Root_Cat}')
            PRODUCT_ATTRIBUTES_LIST.append(Root_Cat)

            #print('\n')
            #print(f'Insertion of the following data: {PRODUCT_ATTRIBUTES_LIST} . To the database')
            #print('\n')
            #PRODUCT_ATTRIBUTES_LIST.clear()

            ##STEP 9.0: Insertion to Database
            print('\n')
            print(f'Insertion of product: {P_Title} . To the database')
            Database_Insertion ( PRODUCT_ATTRIBUTES_LIST )
            print(f'Insertion complete!')
            print('\n')
            PRODUCT_ATTRIBUTES_LIST.clear()
        else:
            raise ValueError(f'Error: {product_response.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

##STEP 6.0: Build a query for API_Page (Title has ben parsed at Product_page)
def query_builder(region_index, title_string):
    #For MEX https://api.mercadolibre.com/sites/MLM/search?q=tapioca+ball+negra+boba+drink+postre+bebida+perla+enviograti
    #For BRZ https://api.mercadolibre.com/sites/MLB/search?q=teclado+knup+kp+2013+qwerty+portugus+brasil+de+cor+preto
    if region_index == 0:
        url_query = URL_API_PREFIX_LIST[0] + unidecode.unidecode(title_string).replace(" ","+")
    elif region_index == 1:
        url_query = URL_API_PREFIX_LIST[1] + unidecode.unidecode(title_string).replace(" ","+")
    
    #print(url_query)
    
    ML_API_Parsing (url_query) #Go to STEP 7.0.

##STEP 5.1: Take the text of the current product title (Still in Product Page)
def product_parsing_C1(region_index, parsed_doc):
    C1_Title = parsed_doc.xpath(XPATH_TITLES_AT_PROD_PAGE[0])
    if C1_Title == []:
        C1_Flag_Title = 'True'
        C1_T_Tuple = (C1_Flag_Title, C1_Prod_Title)
    else:
        C1_Flag_Title = 'False'
        C1_Prod_Title = C1_Title[0].strip()
        #print(C1_Prod_Title)
        C1_T_Tuple = (C1_Flag_Title, C1_Prod_Title)

    #Go to ask a query (query_builder) at API-page
    if C1_T_Tuple[0] == 'False':
        query_builder(region_index, C1_T_Tuple[1])
    elif C1_T_Tuple[0] == 'True':
        pass
        #no_tilte_fun(region_index, C1_T_Tuple[0])          ##ATENTION: THIS FUNCTION IS NOT DEFINED YET!


##STEP 5.2: Take the text of the current product title (Still in Product Page)
def product_parsing_C2(region_index, parsed_doc):
    C2_Title = parsed_doc.xpath(XPATH_TITLES_AT_PROD_PAGE[1])
    if C2_Title == []:
        C2_Flag_Title = 'True'
        C2_Prod_Title = 'Void'
        C2_T_Tuple = (C2_Flag_Title, C2_Prod_Title)
    else:
        C2_Flag_Title = 'False'
        C2_Prod_Title = C2_Title[0].strip()
        #print(C2_Prod_Title)
        C2_T_Tuple = (C2_Flag_Title, C2_Prod_Title)

    #Go to ask a query (query_builder) at API-page    
    if C2_T_Tuple[0] == 'False':
        query_builder(region_index, C2_T_Tuple[1])
    elif C2_T_Tuple[0] == 'True':
        pass
        #no_tilte_fun(region_index, C2_T_Tuple[0])          ##ATENTION: THIS FUNCTION IS NOT DEFINED YET!

##STEP 4.0:  Connect to the current product link (at Product Page)
def parse_top_list(region_index, link ):
    try:
        product_response = requests.get( link )
        if product_response.status_code == 200:
            Product = product_response.content.decode('utf-8')
            parsed_product = html.fromstring(Product)
            #This sensor exists because there are, at least, two ways to find a title 
            html_sensor = parsed_product.xpath(XPATH_PRODUCT_SENSOR)
            #print(html_sensor)
            try:
                if html_sensor == []:
                    #print(f'This is a case 2')
                    product_parsing_C2(region_index, parsed_product)
                    print(f'\n')
                else:
                    #print(f'This is a case 1')
                    product_parsing_C1(region_index, parsed_product)
                    print(f'\n')
            except IndexError:
                return  
        else:
            raise ValueError(f'Error: {product_response.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        ##STEP 1.0: Go to MAIN PAGE (HOME)
        for j in range(2): # where n = 2 (number or regions)
            #j = 0 for MEX, j = 1 for BRA
            for i in Cat_dictionary:
                ##STEP 2.0: Build the URL Target by Categories
                Target = URL_ML[j]+Cat_dictionary[i][j]+Visual_options[0] #Build the URL Target
                #print(Target)
                print('\n')
                main_response = requests.get(Target)
                if main_response.status_code == 200:
                    Home = main_response.content.decode('utf-8')
                    parsed_home = html.fromstring(Home)
                    #Get all the Links of the products listed in the first page
                    product_links = parsed_home.xpath(XPATH_LIST_AT_MAIN_PAGE[0]) 
                    #print(url_products)
                    ##STEP 3.0: Go to each product link (parse_top_list) at the current Category (Target)
                    for product_url in product_links:
                        parse_top_list(j,product_url)
                        #url_next_page = parsed_home.xpath(XPATH_LIST_AT_MAIN_PAGE[1])
                        #parse_top_list(url_next_page)
                else:
                    raise ValueError(f'Error: {main_response.status_code}') #This is the way to lift (raise) an Error                  
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()