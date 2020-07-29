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
        print(s.prettify())

    return soup

def top_amazon_boxes(soup):
    boxes = soup.find_all('div', attrs={'class':"a-section a-spacing-none aok-relative"})

    return boxes

def boxes_info(boxes):
    
    ranks = []
    product_names = []
    image_urls = []
    product_links = []
    star_ratings = []
    reviews = []
    authors_companies = []
    editions_consoles = []

    amz_mx_url = 'https://www.amazon.com.mx'

    for box in boxes:
        rank_box = box.find_all('span', attrs={'class':'zg-badge-text'})
        products_and_image_box = box.find_all('div', attrs={'class' : 'a-section a-spacing-small'})
        product_links_box = box.find_all('a', attrs={'class' : 'a-link-normal'})
        star_ratings_box = box.find_all('span', attrs={'class' : 'a-icon-alt'})
        reviews_box = box.find_all('a', attrs={'class' : 'a-size-small a-link-normal'})
        authors_company_box = box.find_all('span', attrs={'class' : 'a-size-small a-color-base'})
        editions_console_box = box.find_all('span', attrs={'class' : 'a-size-small a-color-secondary'})
        
        
        rank = rank_box[0].get_text()
        product_name = products_and_image_box[0].img.get('alt')
        image_url = products_and_image_box[0].img.get('src')
        product_link = amz_mx_url + product_links_box[0].get('href')
        try:
            star_rating = star_ratings_box[0].get_text()
            review = reviews_box[0].get_text()
            author_company = authors_company_box[0].get_text()
            edition_console = editions_console_box[0].get_text()
        except:
            star_rating = 'N/A'
            review = 'N/A'
            author_company = 'N/A'
            edition_console = 'N/A'
            print(star_ratings_box)

        ranks.append(rank)
        product_names.append(product_name)
        image_urls.append(image_url)
        product_links.append(product_link)
        star_ratings.append(star_rating)
        reviews.append(review)
        authors_companies.append(author_company)
        editions_consoles.append(edition_console)

    # Dictionary
    boxes_dict = {
    "Rank" : ranks,
    "Product Names": product_names,
    "Image urls": image_urls,
    "Product links": product_links,
    "Stars": star_ratings,
    "Reviews": reviews,
    "Authors/Company": authors_companies,
    "Edition/Console": editions_consoles
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

    url = f'https://www.amazon.com.mx/gp/bestsellers/{URL_dict["top_musica"]}/ref=zg_bs_nav_0'
    print(f'\nURL given: {url}')

    soup = extract_soup(url, preview=False)
    boxes = top_amazon_boxes(soup)
    print(f'Boxes: {len(boxes)}')

    amaz_boxes = boxes_info(boxes)

    for key in amaz_boxes:
        print(f'{key}: {len(amaz_boxes[key])}')
        print(amaz_boxes[key])
        print('\n')