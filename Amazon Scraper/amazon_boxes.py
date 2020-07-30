from bs4 import BeautifulSoup
import lxml.html as html
from lxml import etree

import re , datetime, os
import time

import requests
from urllib.request import urlopen

def extract_soup(url, preview=True):
    response = requests.get(url)
    print(f'Request status: {response.status_code}\n')

    soup = BeautifulSoup(response.text, 'lxml')

    if preview==True:
        print(soup.prettify())

    return soup

def top_amazon_boxes(soup):
    boxes = soup.find_all('div', attrs={'class':"a-section a-spacing-none aok-relative"})

    return boxes

def scrape_boxes(boxes):
    
    ranks = [None]*50
    product_names = [None]*50
    image_urls = [None]*50
    product_links = [None]*50
    star_ratings = [None]*50
    reviews = [None]*50
    authors_companies = [None]*50
    editions_consoles = [None]*50
    min_prices = [None]*50
    max_prices = [None]*50

    amz_mx_url = 'https://www.amazon.com.mx'
    
    n_box = 0
    for box in boxes:
        rank_box = box.find_all('span', attrs={'class':'zg-badge-text'})
        products_and_image_box = box.find_all('div', attrs={'class' : 'a-section a-spacing-small'})
        product_links_box = box.find_all('a', attrs={'class' : 'a-link-normal'})
        star_ratings_box = box.find_all('span', attrs={'class' : 'a-icon-alt'})
        reviews_box = box.find_all('a', attrs={'class' : 'a-size-small a-link-normal'})
        authors_company_box = box.find_all('span', attrs={'class' : 'a-size-small a-color-base'})
        editions_console_box = box.find_all('span', attrs={'class' : 'a-size-small a-color-secondary'})
        prices_box = box.find_all('span', attrs={'class' : "p13n-sc-price"})
        
        
        ranks[n_box] = rank_box[0].get_text()
        product_names[n_box] = products_and_image_box[0].img.get('alt')
        image_urls[n_box] = products_and_image_box[0].img.get('src')
        product_links[n_box] = amz_mx_url + product_links_box[0].get('href')

        #Depended cases
        try:
            star_ratings[n_box] = float(star_ratings_box[0].get_text()[:3])
            reviews[n_box] = int(reviews_box[0].get_text().replace(',',''))
        except:
            print(f'no revs at : {n_box + 1}')
            star_ratings[n_box] = None
            reviews[n_box] = None

        #Individual cases
        try:
            authors_companies[n_box] = authors_company_box[0].get_text()
        except:
            print(f'no author at : {n_box + 1}')
            authors_companies[n_box] = None
        
        try:
            editions_consoles[n_box] = editions_console_box[0].get_text()
        except:
            print(f'no edition at : {n_box + 1}')
            editions_consoles[n_box] = None

        if domain == 'mx':
            coin_symbol = 1
        elif domain == 'br':
            coin_symbol = 2

        try:
            min_prices[n_box] = float(prices_box[0].get_text()[coin_symbol:].replace(',',''))
        except:
            print(f'no min price at : {n_box + 1}')
            min_prices[n_box] = None

        try:    
            max_prices[n_box] = float(prices_box[1].get_text()[coin_symbol:].replace(',',''))
        except:
            max_prices[n_box] = None

        n_box = n_box + 1 


    # Dictionary
    boxes_dict = {
    "Rank" : ranks,
    "Product Names": product_names,
    "Image urls": image_urls,
    "Product links": product_links,
    "Stars": star_ratings,
    "Reviews": reviews,
    "Authors/Company": authors_companies,
    "Edition/Console": editions_consoles,
    "Price_std_or_min" : min_prices,
    "Max_prices" : max_prices
    }


    return boxes_dict
    
def test_urls(URL_dict, secs):
    n_key = 1
    t_keys = len(URL_dict)
    for key in URL_dict:
        url = f'https://www.amazon.com.mx/gp/bestsellers/{URL_dict[key]}/ref=zg_bs_nav_0'
        print(f'\n{n_key}° Key given : {key}')
        print(f'URL given: {url}')

        response = requests.get(url)
        print(f'Request status: {response.status_code}\n')

        cont = 0.0
        if n_key < t_keys:
            while cont < (secs + 0.25):
                if cont % 1 == 0:
                    print(int(cont), end=' ')
                else:
                    print('.', end=' ')
                cont = cont + 0.25
                time.sleep(.25)

            n_key = n_key + 1


if __name__=='__main__':

    URL_dict = {
        'top_food_and_drinks' : 'grocery',
        'top_automotriz' : 'automotive',
        'top_amazon-devices' : 'amazon-devices',
        'top_bebe': 'baby',
        'top_dep_al' : 'sports',
        'top_electronicos' : 'electronics',
        'top_herramientas' : 'tools',
        'top_hogar_cocina': 'kitchen',
        'top_industrial_emp_ciencia' : 'industrial',
        'top_musical_instruments' : 'musical-instruments',
        'top_juguetes_juegos' : 'toys',
        'top_libros':'books',
        'top_musica' : 'music',
        'top_oficina_papeleria' : 'officeproduct',
        'top_peliculas_series' : 'dvd',
        'top_handmade' : 'handmade',
        'top_prod_animales' : 'pet-supplies',
        'top_ropa_zapatos_acc' : 'shoes',
        'top_salud' : 'hpc',
        'top_software' : 'software',
        'top_kindle' : 'digital-text',
        'top_videojuegos': 'videogames'
        }

    domain = 'mx'
    url = f'https://www.amazon.com.{domain}/gp/bestsellers/{URL_dict["top_musica"]}/ref=zg_bs_nav_0'
    print(f'\nURL given: {url}')

    soup = extract_soup(url, preview=False)
    boxes = top_amazon_boxes(soup)
    print(f'Boxes: {len(boxes)}')

    amaz_boxes = scrape_boxes(boxes)

    for key in amaz_boxes:
        print(f'{key}: {len(amaz_boxes[key])}')
        print(amaz_boxes[key])
        print('loaded \n')