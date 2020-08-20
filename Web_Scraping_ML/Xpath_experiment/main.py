#-*- coding: utf-8 -*-

#Step 1: Libraries and frameworks

import requests
import lxml.html as html
import datetime
import os
import sys

#STEP 1. Declaring XPATH, dictionaries and vars.

##At main_page, [0] is Mexico and [1] is Brazil
URL_ML = ["https://listado.mercadolibre.com.mx/", "https://lista.mercadolivre.com.br/"]
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
Visual_options = ["_DisplayType_G","_DisplayType_LF"]
##How to build a main page
#URL_ML_Complete = URL_ML[region]+Cat_dictionary[cat][region]+Visual_options[0]

##At main_page/category/Visual_options[0]
XPATH_LIST_AT_MAIN_PAGE = ['//section/ol/li/div/div/div/div/ul/li/a/@href','/html/body/main//ul/li[11]/a/@href']
XPATH_PRODUCT_SENSOR = '//div/div/input[@form="productInfo"]'

##IF XPATH_PRODUCT_SENSOR == Something...

XPATH_LIST_AT_PROD_PAGE_C1 = ['//div[1]/section[1]/div/header/h1/text()',
'//div[1]/div/div/div/figure[1]/a/img/@src',
'//*[@id="productInfo"]/fieldset/span/span[@class = "price-tag-symbol"]/text()',
'//div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/span/span[@class = "price-tag-fraction"]/text()',
'/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/span[2]/span[@class="price-tag-cents"]/text()',
'/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/span[1]/del/span[@class = "price-tag-fraction"]/text()',
'/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/span[1]/del/span[@class = "price-tag-cents-visible" ]/text()',
'/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/div/p/text()',
'/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/dl/div[@class = "item-conditions"]/text()',
'//div/div[1]/div[1]/section[4]/div/div[1]/span[@class = "review-summary-average"]/text()',
'/html/body/main/div/div[1]/div[1]/section[4]/div/div[1]/span[2]/div/span[2]/text()',
'//div/div/div/section[@class = "main-section item-description "]//p[not (@class) ]/text()',
'//section[2]/div/section[1]/ul/li/strong/text()',
'//section[2]/div/section[1]/ul/li/span/text()',
'/html/body/main/section/nav/div/ul/li/a/text()']

##IF XPATH_PRODUCT_SENSOR == []
#NOTE: There is a sub-case in case 3, please, check products that are sold by Mercado Libre.

XPATH_LIST_AT_PROD_PAGE_C2 = ['//div/div/div/div[1]//h1/text()',
'//div[2]/div[1 or 2]/div[1]/div[1]/div[1]//figure//img[@src or @data-zoom]',
'//div[2]/div[2]/div/div/span/span[@class = "price-tag-symbol"][1]/text()',
'//div[2]/div[1 or 2]/div[1 or 2]/div//span[@class = "price-tag" or @class = "price-tag ui-pdp-price__part"]/span[@class = "price-tag-fraction"][1]/text()',
'//div[2]/div[1 or 2]/div[1 or 2]/div//span[@class = "price-tag" or @class = "price-tag ui-pdp-price__part"]/span[@class = "price-tag-cents"][1]/text()',
'//div[2]/div[1]/div[2]/div[1]//div//del/span[2]/text()',
'//div[2]/div[1]/div[2]/div[1]//div//del/span[3]/text()',
'//div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/span[2]/text()',
'//div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/span/text()',
'//div[2]/div[2]/div[3]/div[1]/div[2]/div/section/header/div/div[1]/h2/text()',
'//div[2]/div[2]/div[3]/div[1]/div[2]/div/section/header/div/div[1]/div/h4/text()',
'//div[2]/div[2]/div[1]/div[1]/div[3]/div/div/p/text()',
'//div[2]/div[2]/div[1]/div[1]/div[4]/div/div/div[1]/table/tbody/tr/th/text()',
'//div[2]/div[2]/div[1]/div[1]/div[4]/div/div/div[1]/table/tbody/tr/td/span/text()',
'//div[2]/div[1]/div/div[1]/div[2]/div/ul/li/a/text()']

#STEP 2. Define functions and decorators.

def product_parsing_C1(parsed_doc):
    C1_Title = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[0])
    print(C1_Title[0].strip())
    C1_Image_link = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[1])
    print(C1_Image_link[0])
    C1_Currency = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[2])
    print(C1_Currency[0])
    C1_Main_price_int = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[3])
    print(C1_Main_price_int[0])
    C1_Main_price_cent = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[4])
    print(C1_Main_price_cent[0])
    C1_Old_price_int = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[5])
    print(C1_Old_price_int[0])
    C1_Old_price_cent = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[6])
    print(C1_Old_price_cent[0])
    C1_Discount = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[7])
    print(C1_Discount[0].replace("OFF",""))
    C1_Condition = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[8])
    print(C1_Condition[0])
    C1_Average_rating = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[9])
    print(C1_Average_rating[0])
    C1_No_of_reviews = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[10])
    print(C1_No_of_reviews[0])
    C1_Description = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[11])
    print(C1_Description)
    C1_Specs = dict(zip(parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[12]),parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[13])))
    print(C1_Specs)
    C1_Cat_path = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C1[14])
    print(C1_Cat_path)

def product_parsing_C2(parsed_doc):
    C2_Title = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[0])
    print(C2_Title)
    C2_Image_link = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[1])
    print(C2_Image_link)
    C2_Currency = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[2])
    print(C2_Currency)
    C2_Main_price_int = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[3])
    print(C2_Main_price_int)
    C2_Main_price_cent = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[4])
    print(C2_Main_price_cent)
    C2_Old_price_int = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[5])
    print(C2_Old_price_int)
    C2_Old_price_cent = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[6])
    print(C2_Old_price_cent)
    C2_Discount = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[7])
    print(C2_Discount)
    C2_Condition = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[8])
    print(C2_Condition)
    C2_Average_rating = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[9])
    print(C2_Average_rating[0])
    C2_No_of_reviews = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[10])
    print(C2_No_of_reviews[0])
    C2_Description = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[11])
    print(C2_Description)
    C2_Specs = dict(zip(parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[12]),parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[13])))
    print(C2_Specs)
    C2_Cat_path = parsed_doc.xpath(XPATH_LIST_AT_PROD_PAGE_C2[14])
    print(C2_Cat_path)

f"//ol/li[{it}]/div/a/div/h2/span/text()"

def parse_top_list( link ):
    try:
        product_response = requests.get( link )
        if product_response.status_code == 200:
            Product = product_response.content.decode('utf-8')
            parsed_product = html.fromstring(Product)
            html_sensor = parsed_product.xpath(XPATH_PRODUCT_SENSOR)
            #print(html_sensor)
            try:
                if html_sensor == []:
                    print(f'This is a case 2')
                    product_parsing_C2(parsed_product)
                    print(f'\n')
                else:
                    print(f'This is a case 1')
                    product_parsing_C1(parsed_product)
                    print(f'\n')
            except IndexError:
                return  
        else:
            raise ValueError(f'Error: {product_response.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        for j in range(2):
            for i in Cat_dictionary:
                Target = URL_ML[j]+Cat_dictionary[i][j]+Visual_options[0]
                print(Target)
                print('\n')
                main_response = requests.get(Target)
                if main_response.status_code == 200:
                    Home = main_response.content.decode('utf-8')
                    parsed_home = html.fromstring(Home)
                    product_links = parsed_home.xpath(XPATH_LIST_AT_MAIN_PAGE[0]) #this is the way to enter XPath exp to parsed html
                    #print(url_products)
                    for product_url in product_links:
                        parse_top_list(product_url)
                        #url_next_page = parsed_home.xpath(XPATH_LIST_AT_MAIN_PAGE[1])
                        #parse_top_list(url_next_page)
                else:
                    raise ValueError(f'Error: {main_response.status_code}') #This is the way to lift (raise) an Error                  
    except ValueError as ve:
        print(ve)

#STEP 3. Define Entry point

def run():
    sys.setrecursionlimit(1000)
    parse_home()

if __name__ == '__main__':
    run()