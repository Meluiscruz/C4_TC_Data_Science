import requests
import lxml.html as html
import datetime
import os

#STEP 1. Declaring XPATH vars

##At main_page
URL_ML_MX = "https://www.mercadolibre.com.mx/"   #Esta variable será utilizada en el script de Python de web scraping más adelante.
XPATH_LINK_TO_OFFERS = '/html/body/main/div/div/section[@class = "recommendations"]/div[@class="row container"]/div[@class="section-header"]/a/@href'

##At main_page/offers_page[current]
XPATH_PRODUCT_TITLES_AT_OFFERS = '/html/body/main/div//div/ol/li/a/div/div/p/text()'

#NOTE: I think the product title shoud be scraped once the agent can access every individual product.
#Currently, this title contruction can be a weak point after IndexErrors

XPATH_URL_EACH_PROD_AT_OFFERS = '/html/body/main/div//div[2]/div/ol/li/a/@href' 

##Gateway to the rest of pages (https://www.mercadolibre.com.mx/ofertas?page=i where i is index >= 2)
XPATH_LINK_TO_PAGES_AT_OFFERS = '/html/body/main/div/div[2]/div[2]/div/ul/li/a/@href'

##If PRODUCT SENSOR == ["Comprar ahora"], PRODUCT = C1. ELSE, PRODUCT = C2 
#XPATH_PRODUCT_SENSOR = '/html/body/main/div[2]/div[1]/div[2]/div[1]/section[1]/div/form/div/div/div/input[@form = "productInfo"]'
XPATH_PRODUCT_SENSOR = '//div/div/input[@form="productInfo"]'

##At main_page/offers_page[i]/product (IF $x('//*[@id="productInfo"]') == [form#productInfo.short-description__form])
XPATH_URL_MAIN_IMG_C1 = '/html/body/main/div[2]/div[1]/div[1]/div[1]/div/div/div/figure[1]/a/img/@src'
XPATH_CURRENCY_C1 = '//*[@id="productInfo"]/fieldset/span/span[@class = "price-tag-symbol"]/text()'
XPATH_MAIN_PRICE_INTEGER_C1 = '/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/span[2]/span[@class = "price-tag-fraction"]/text()'
XPATH_MAIN_PRICE_CENTS_C1 = '/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/span[2]/span[@class="price-tag-cents"]/text()'
XPATH_OLD_PRICE_INTEGER_C1 = '/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/span[1]/del/span[@class = "price-tag-fraction"]/text()'
XPATH_OLD_PRICE_CENTS_C1 = '/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/span[1]/del/span[@class = "price-tag-cents-visible" ]/text()'
XPATH_DISC_C1 = '/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/form/fieldset[1]/div/p/text()'
XPATH_PROD_COND_C1 = '/html/body/main/div/div[1]/div[2]/div[1]/section[1]/div/dl/div[@class = "item-conditions"]/text()'
XPATH_PROD_RATING_C1 = '/html/body/main/div/div[1]/div[1]/section[4]/div/div[1]/span[@class = "review-summary-average"]/text()'
XPATH_NUMB_REVS_C1 = '/html/body/main/div/div[1]/div[1]/section[4]/div/div[1]/span[2]/div/span[2]/text()'
XPATH_PROD_DESC_C1 = '//section[@class = "main-section item-description "]//p[not (@class) ]/text()'
XPATH_PROD_SPECS_FIELDS_C1 = '/html/body/main/div/div[1]/div[1]/section[2]/div/section[1]/ul/li/strong/text()'
XPATH_PRODUCT_SPECS_VALUES_C1 = '/html/body/main/div/div[1]/div[1]/section[2]/div/section[1]/ul/li/span/text()'
XPATH_CATEGORY_PATH_C1 = '/html/body/main/section/nav/div/ul/li/a/text()'

##At main_page/offers_page[i]/product (IF $x('//*[@id="productInfo"]') == [])
#NOTE: Those XPath expresions have to be ammended to achive better results.
XPATH_URL_MAIN_IMG_C2 = '//*[@id="root-app"]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/span[1]/figure/img/@src'
XPATH_CURRENCY_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/span/span[1]/text()'
XPATH_MAIN_PRICE_INTEGER_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/span/span[@class = "price-tag-fraction"]/text()'
XPATH_MAIN_PRICE_CENTS_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/span/span[@class = "price-tag-cents"]/text()'
XPATH_OLD_PRICE_INTEGER_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/del/span[@class="price-tag-fraction"]/text()'
XPATH_OLD_PRICE_CENTS_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/del/span[@class="price-tag-cents-visible"]/text()'
XPATH_DISC_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/span[@class="ui-pdp-price__second-line__label ui-pdp-color--GREEN"]/text()'
XPATH_PROD_COND_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/span[@class = "ui-pdp-subtitle"]/text()' 
XPATH_PROD_RATING_C2 = '/html/body/main/div[2]/div[2]/div[3]/div[1]/div[2]/div/section/header/div/div[1]/h2[@class = "ui-pdp-reviews__rating__summary__average"]/text()'
XPATH_NUMB_REVS_C2 = '/html/body/main/div[2]/div[2]/div[3]/div[1]/div[2]/div/section/header/div/div[1]/div/h4[@class = "ui-pdp-reviews__rating__summary__label"]/text()'
XPATH_PROD_DESC_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[3]/div/div/p[ @class="ui-pdp-description__content"]/text()'
XPATH_PROD_SPECS_FIELDS_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[4]/div/div/div[1]/table/tbody/tr/th/text()'
XPATH_PRODUCT_SPECS_VALUES_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[4]/div/div/div[1]/table/tbody/tr/td/span[@class="andes-table__column--value"]/text()'
XPATH_CATEGORY_PATH_C2 = '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[4]/div/div/div[1]/table/tbody/tr/td/span[@class="andes-table__column--value"]/text()'

#STEP 2. Define functions and decorators.

def product_parsing_C1(parsed_doc):
    URL_Product_img_C1  = parsed_doc.xpath(XPATH_URL_MAIN_IMG_C1) ##List of Image links
    print(URL_Product_img_C1)
    Currency_C1  = parsed_doc.xpath(XPATH_CURRENCY_C1) ##List of currency
    print(Currency_C1)
    M_Price_Int_C1  = parsed_doc.xpath(XPATH_MAIN_PRICE_INTEGER_C1) ##List of 
    print(M_Price_Int_C1)
    M_Price_Cent_C1  = parsed_doc.xpath(XPATH_MAIN_PRICE_CENTS_C1) ##List of 
    print(M_Price_Cent_C1)
    O_Price_Int_C1  = parsed_doc.xpath(XPATH_OLD_PRICE_INTEGER_C1) ##List of 
    print(O_Price_Int_C1)
    O_Price_Cent_C1  = parsed_doc.xpath(XPATH_OLD_PRICE_CENTS_C1) ##List of 
    print(O_Price_Cent_C1)
    D_Price_C1  = parsed_doc.xpath(XPATH_DISC_C1) ##List of 
    print(D_Price_C1)
    Cond_Prod_C1 = parsed_doc.xpath(XPATH_PROD_COND_C1) ##List of 
    print(Cond_Prod_C1)
    Rat_Prod_C1 = parsed_doc.xpath(XPATH_PROD_RATING_C1) ##List of 
    print(Rat_Prod_C1)
    Rev_Prod_C1 = parsed_doc.xpath(XPATH_NUMB_REVS_C1) ##List of 
    print(Rev_Prod_C1)
    Des_Prod_C1 = parsed_doc.xpath(XPATH_PROD_DESC_C1) ##List of 
    print(Des_Prod_C1)
    Specs_Fields_Prod_C1 = parsed_doc.xpath(XPATH_PROD_SPECS_FIELDS_C1) ##List of 
    print(Specs_Fields_Prod_C1)
    Specs_Values_Prod_C1 = parsed_doc.xpath(XPATH_PRODUCT_SPECS_VALUES_C1) ##List of 
    print(Specs_Values_Prod_C1)
    Cat_Path_Prod_C1 = parsed_doc.xpath(XPATH_CATEGORY_PATH_C1) ##List of 
    print(Cat_Path_Prod_C1)

def product_parsing_C2( link ):
    try:
        case_2 = requests.get( link )
        if case_2.status_code == 200:
            Product_C2 = case_2.content.decode('utf-8')
            parsed_doc = html.fromstring(Product_C2)
            try:
                URL_Product_img_C2  = parsed_doc.xpath(XPATH_URL_MAIN_IMG_C2) ##List of Image links
                print(URL_Product_img_C2)
                Currency_C2  = parsed_doc.xpath(XPATH_CURRENCY_C2) ##List of currency
                print(Currency_C2)
                M_Price_Int_C2  = parsed_doc.xpath(XPATH_MAIN_PRICE_INTEGER_C2) ##List of 
                print(M_Price_Int_C2)
                M_Price_Cent_C2  = parsed_doc.xpath(XPATH_MAIN_PRICE_CENTS_C2) ##List of 
                print(M_Price_Cent_C2)
                O_Price_Int_C2  = parsed_doc.xpath(XPATH_OLD_PRICE_INTEGER_C2) ##List of 
                print(O_Price_Int_C2)
                O_Price_Cent_C2  = parsed_doc.xpath(XPATH_OLD_PRICE_CENTS_C2) ##List of 
                print(O_Price_Cent_C2)
                D_Price_C2  = parsed_doc.xpath(XPATH_DISC_C2) ##List of 
                print(D_Price_C2)
                Cond_Prod_C2 = parsed_doc.xpath(XPATH_PROD_COND_C2) ##List of 
                print(Cond_Prod_C2)
                Rat_Prod_C2 = parsed_doc.xpath(XPATH_PROD_RATING_C2) ##List of 
                print(Rat_Prod_C2)
                Rev_Prod_C2 = parsed_doc.xpath(XPATH_NUMB_REVS_C2) ##List of 
                print(Rev_Prod_C2)
                Des_Prod_C2 = parsed_doc.xpath(XPATH_PROD_DESC_C2) ##List of 
                print(Des_Prod_C2)
                Specs_Fields_Prod_C2 = parsed_doc.xpath(XPATH_PROD_SPECS_FIELDS_C2) ##List of 
                print(Specs_Fields_Prod_C2)
                Specs_Values_Prod_C2 = parsed_doc.xpath(XPATH_PRODUCT_SPECS_VALUES_C2) ##List of 
                print(Specs_Values_Prod_C2)
                Cat_Path_Prod_C2 = parsed_doc.xpath(XPATH_CATEGORY_PATH_C2) ##List of 
                print(Cat_Path_Prod_C2)
            except IndexError:
                return  
        else:
            raise ValueError(f'Error: {case_2.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

def parse_ind_prod( link ):
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
                    product_parsing_C2( link )
                else:
                    print(f'This is a case 1')
                    product_parsing_C1(parsed_product)
            except IndexError:
                return  
        else:
            raise ValueError(f'Error: {product_response.status_code}') #This is the way to lift (raise) an Error
    except ValueError as ve:
        print(ve)

def parse_offers( link ):
    try:
        offers_response = requests.get( link )
        if offers_response.status_code == 200:
            Offers = offers_response.content.decode('utf-8')
            parsed_offers = html.fromstring(Offers)
            try:
                product_titles = parsed_offers.xpath(XPATH_PRODUCT_TITLES_AT_OFFERS) ##List of titles
                #product_titles = product_titles.replace('\"', '')
                print(product_titles)
                product_links  = parsed_offers.xpath(XPATH_URL_EACH_PROD_AT_OFFERS) ##List of links
                print(product_links)
                for product_url in product_links:
                    parse_ind_prod(product_url) #change for product_url and add tab
            except IndexError:
                return
        else:
            raise ValueError(f'Error: {offers_response.status_code}') #This is the way to lift (raise) an Error           
    except ValueError as ve:
        print(ve)

#Esto es para tomar datos de todas las páginas, una vez posicionado en offers.
#for Sharingan in range[100]:
    #Tsukuyomi = parsed_offers.xpath('/html/body/main/div/div[2]/div[2]/div/ul/li[Sharingan]/a/@href')
    #parse_offers( Tsukuyomi )

def parse_home():
    try:
        main_response = requests.get(URL_ML_MX)
        if main_response.status_code == 200:
            Home = main_response.content.decode('utf-8')
            parsed_home = html.fromstring(Home)
            url_offers = parsed_home.xpath(XPATH_LINK_TO_OFFERS)[0] #this is the way to enter XPath exp to parsed html
            print(url_offers)
            parse_offers(url_offers)
        else:
            raise ValueError(f'Error: {main_response.status_code}') #This is the way to lift (raise) an Error
                  
    except ValueError as ve:
        print(ve)

#STEP 3. Define Entry point

def run():
    parse_home()

if __name__ == '__main__':
    run()