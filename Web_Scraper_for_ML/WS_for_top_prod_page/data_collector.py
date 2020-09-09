import requests
import json
import lxml.html as html
import unidecode
import os
import pymysql.cursors
from time import sleep
from datetime import datetime
import math
import auth_and_pass

##Vars, dictionaries and lists.

#Cat_dictionary FOR TESTING, UNCOMMENT Cat_dictionary when will be in productive enviroment.    #https://stackoverflow.com/questions/5717816/how-to-uncomment-multiple-lines-of-code-in-visual-studio

#Cat_dictionary = {
#    1 : ['alimentos-bebidas/', 'alimentos-bebidas/']
#}

Cat_dictionary = {
    1 : ['alimentos-bebidas/', 'alimentos-bebidas/'],
    2 : ['accesorios-vehiculos', 'acessórios-veículos'],
    3 : ['bebe', 'bebe'],
    4 : ['deportes-fitness', 'esportes-fitness'],
    5 : ['celulares-y-smartphones', 'celulares-e-smartphones'],
    6 : ['audio-y-video', 'audio-e-video'],
    7 : ['electrodomesticos', 'eletrodomesticos'],
    8 : ['herramientas-y-construccion', 'ferramentas-e-construcao'],
    9 : ['hogar-muebles-y-jardin', 'casa-moveis-e-decoracao'],
    10 : ['industrias-y-oficinas/', 'agro-industria-comercio/'],
    11 :['instrumentos-musicales','instrumentos-musicais/'],
    12 : ['juegos-y-juguetes/','brinquedos-e-hobbies'],
    13 : ['libros-revistas-y-comics/','livros-revistas-e-comics'],
    14 : ['musica-peliculas-y-series/', 'musica-filmes-e-seriados'],
    15 : ['arte-papeleria-y-merceria', 'arte-papelaria-e-armarinho'],
    16: ['animales-y-mascotas', 'animais/'],
    17: ['ropa-bolsas-y-calzado', 'calcados-roupas-e-bolsas'],
    18: ['salud-y-equipamiento-medico/','saude/'],
    19: ['belleza-y-cuidado-personal', 'beleza-e-cuidado-pessoal'],
    20: ['computacion','informatica'],
    21: ['consolas-y-videojuegos', 'games/']
}

URL_ML = ["https://listado.mercadolibre.com.mx/", "https://lista.mercadolivre.com.br/"]
Visual_options = ["_DisplayType_G","_DisplayType_LF"]

XPATH_LIST_OF_TITLES_AT_MAIN_PAGE = '/html/body/main/div/div/section/ol/li/div/div/a/div/div/h2/text()'
URL_API_PREFIX_LIST = ['https://api.mercadolibre.com/sites/MLM/search?q=','https://api.mercadolibre.com/sites/MLB/search?q=']
URL_API_PREFIX_REVS = 'https://api.mercadolibre.com/reviews/item/'
PRODUCT_ATTRIBUTES_LIST = []

##STEP 9.0 Insertion of data to Database.

def Database_Insertion ( rank, category, list_of_attributes ):
    
    connection = pymysql.connect(host = 'localhost', user = auth_and_pass.MY_SQL_ADMIN_USER, password = auth_and_pass.MY_SQL_ADMIN_PASS, 
        db = 'ml_product_table', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
    
    product_id =        list_of_attributes[0]
    rank =              rank
    currency =          list_of_attributes[1]
    region =            list_of_attributes[2]
    price =             list_of_attributes[3]
    price_max =         list_of_attributes[4]
    name =              list_of_attributes[5]
    image_url =         list_of_attributes[6]
    link =              list_of_attributes[7]
    stars =             list_of_attributes[8]
    reviews =           list_of_attributes[9]
    category =          category
    catched_at =        datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:

        with connection.cursor() as cursor: 

            sql = "INSERT INTO `pre_json`( `product_id`, `rank`, `currency`, `region`, `price`, `price_max`, `name`, `image_url`, `link`,\
                    `stars`, `reviews`, `category`, `catched_at` ) VALUES ('"+ product_id +"', '" + rank + "','" + currency + "',\
                    '"+ region +"', '"+ price +"', '"+ price_max +"', '"+ name +"', '"+ image_url +"', '"+ link +"', \
                    '"+ stars +"', '"+ reviews +"', '"+ category +"', '"+ catched_at +"')ON DUPLICATE KEY UPDATE `rank` = VALUES( `rank` )"
            cursor.execute(sql)
            connection.commit()

    except Exception as E :

        print(E)

    finally:
        
        connection.close()   

##STEP 8.1 (Cont): Take the first result of the JSON list(At API_subpages)
def ML_API_Revs ( link ):

    try:

        Asking_API_revs = requests.get( link )
        if Asking_API_revs.status_code == 200:
            Query_for_revs = json.loads(Asking_API_revs.content)
   
            ##STEP 8.1.1: Print values:

            P_stars = str(Query_for_revs['rating_average'])
            P_reviews = str(Query_for_revs['paging']['total'])
            Rev_Vector = (P_stars, P_reviews)

            return Rev_Vector
        else:

            raise ValueError(f'Error: {Asking_API_revs.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

##STEP 7.0: Take the first result of the JSON list (At API_page)
def ML_API_Parsing ( link ):

    try:

        Asking_API_req = requests.get( link )
        if Asking_API_req.status_code == 200:
            Query = json.loads(Asking_API_req.content)

            try :
                prod_id = str(Query['results'][0]['id'])                #Product ID
                #print(f'\nProduct ID = {prod_id}')
                PRODUCT_ATTRIBUTES_LIST.append(prod_id)                 #list[0]
            except IndexError :
                return

            P_Currency = str(Query['results'][0]['currency_id'])    #P_Currency
            #print(f'\nCurrency = {P_Currency}')
            PRODUCT_ATTRIBUTES_LIST.append(P_Currency)                 #list[1]
   
            ##STEP 8.0: Get Identifications from the first result:
            site_id = str(Query['results'][0]['site_id'])           #Site_ID
            if site_id == 'MLM':
                region = 'MX'                                       #Region
                PRODUCT_ATTRIBUTES_LIST.append(region)              #list[2]
            elif site_id == 'MLB':
                region = 'BR'
                PRODUCT_ATTRIBUTES_LIST.append(region)              #list[2]
            else:
                region = 'UN'
                PRODUCT_ATTRIBUTES_LIST.append(region)              #list[2]

            ##NOTE: To save time, this information may be extracted from STEP 8.1

            try: #This will happening when the main price is not defined
                P_price = str(Query['results'][0]['price'])         #Current Price
                #print(f'\nCurrent Price = {P_price}')
                PRODUCT_ATTRIBUTES_LIST.append(P_price)                #list[3]
            except TypeError:
                P_price = None  #Current Price
                #print(f'\nCurrent Price = {P_price}')
                PRODUCT_ATTRIBUTES_LIST.append(P_price)                #list[3]
            
            try:
                P_max_price = str(Query['results'][0]['original_price'])        #Max Price (old price)
                #print(f'\nOld Price = {P_max_price}')
                PRODUCT_ATTRIBUTES_LIST.append(P_max_price)            #list[4]
            except TypeError:
                P_max_price = None
                #print(f'\nOld Price = {P_max_price}')
                PRODUCT_ATTRIBUTES_LIST.append(P_max_price)            #list[4]

            P_name = str(Query['results'][0]['title'])              #Name
            #print(f'\nProduct Title = {P_name}')
            PRODUCT_ATTRIBUTES_LIST.append(P_name)                  #list[5]

            P_image_src = str(Query['results'][0]['thumbnail'])     #image_url
            #print(f'\nProduct URL Image = {P_image_src}')
            PRODUCT_ATTRIBUTES_LIST.append(P_image_src)             #list[6]

            P_link = str(Query['results'][0]['permalink'])          #link
            #print(f'\nProduct URL = {P_link}')
            PRODUCT_ATTRIBUTES_LIST.append(P_link)                  #list[7]

            ##NOTE: To save time, information above may be extracted from STEP 8.1

            ##STEP 8.2: Take the reviews information
            url_revs = URL_API_PREFIX_REVS + prod_id
            Rev_Vector = ML_API_Revs(url_revs)
            #print(f'Product Average Rating = {Rev_Vector[0]}')      #stars
            #print(f'Total of Reviews = {Rev_Vector[1]}')            #reviews
            PRODUCT_ATTRIBUTES_LIST.append(Rev_Vector[0])           #list[8]
            PRODUCT_ATTRIBUTES_LIST.append(Rev_Vector[1])           #list[9]

            #print('\n')
            #print(f'Insertion of the following data: {PRODUCT_ATTRIBUTES_LIST} . To the database')
            #print('\n')

            ##STEP 9.0: Insertion to Database
            print('\n')
            print(f'\nInsertion of product: {P_name} . To the database')
            print(f'\nRank = {rank}')
            #print(f'\ncategory = {category}')
            
            Database_Insertion ( rank = rank, category = category, list_of_attributes = PRODUCT_ATTRIBUTES_LIST )
            print(f'\nInsertion complete!')
            print('\n')
            PRODUCT_ATTRIBUTES_LIST.clear()
            sleep(0.20)

        else:

            raise ValueError(f'Error: {Asking_API_req.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

##STEP 6.0: Build a query for API_Page (Title has ben parsed at Product_page)
def query_builder( title_string ):

    #For MEX https://api.mercadolibre.com/sites/MLM/search?q=tapioca+ball+negra+boba+drink+postre+bebida+perla+enviograti
    #For BRZ https://api.mercadolibre.com/sites/MLB/search?q=teclado+knup+kp+2013+qwerty+portugus+brasil+de+cor+preto
    if region_index == 0:
        url_query = URL_API_PREFIX_LIST[0] + unidecode.unidecode(title_string).replace(" ","+")
    elif region_index == 1:
        url_query = URL_API_PREFIX_LIST[1] + unidecode.unidecode(title_string).replace(" ","+")
    
    #print(url_query)
    
    ML_API_Parsing( url_query ) #Go to STEP 7.0.


def run():

    global category
    global rank
    global region_index
    print("\n\n********** DATA_COLLECTOR IS RUNNING! **********")
    try:
        ##STEP 1.0: Go to MAIN PAGE (HOME)
        for j in range(2): # where n = 2 (number or regions)
            #j = 0 for MEX, j = 1 for BRA
            for i in Cat_dictionary: #i is the key
                ##STEP 2.0: Build the URL Target by Categories
                category = Cat_dictionary[i][j].strip().replace("/","").replace("-"," ")
                Target = URL_ML[j] + category + Visual_options[0] #Build the URL Target
                #print(Target)
                print('\n')
                main_response = requests.get(Target)
                if main_response.status_code == 200:
                    Home = main_response.content.decode('utf-8')
                    parsed_home = html.fromstring(Home)
                    #Get all the Links of the products listed in the first page
                    product_titles = parsed_home.xpath(XPATH_LIST_OF_TITLES_AT_MAIN_PAGE)
                    #print(url_products)
                    ##STEP 3.0: Go to each product link (parse_top_list) at the current Category (Target)
                    for index, p_title in enumerate( product_titles ):
                        rank = str( index + 1 )
                        region_index = j
                        query_builder( p_title ) #OVER HERE <---
                        #url_next_page = parsed_home.xpath(XPATH_LIST_AT_MAIN_PAGE[1])
                        #parse_top_list(url_next_page)
                else:
                    raise ValueError(f'Error: {main_response.status_code}') #This is the way to lift (raise) an Error                  
    except ValueError as ve:
        print(ve)
    
    print("\n\n********** END OF DATA_COLLECTOR**********")

if __name__ == '__main__':
    run()