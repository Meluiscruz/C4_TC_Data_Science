# C4_TC_DS_Repo
### Cohort 4 / Team Cesar / Data Science & Backend

This is the official C4-Team-Cesa Project for Data Science  and Backend team.
This repo will have a branch per Scrapers focused on the following Web Sellers:

- Mercado Libre:

	- Mexico.
	- Brazil.

- Amazon:

	- Mexico.
	- Brazil.

**Note 1: ** During the development of this project, some of these Web Sellers could be changed, removed, extended, or decreased to other markets. The only websellers that are fixed are Amazon (for MX and BZ) and Mercado Libre (for MX and BZ).

**Note 2: ** The Master branch is reserved for field versions of all Web Scrapers, Statistical Analysis, and Data Visualization. Files ready to be delivered to Backend and/or Frontend.

## Scope Source:

https://www.statista.com/topics/2453/e-commerce-in-latin-america/

## Files in ML_testing branch:
- \Web_Scraping_ML\Ofertas_MX\: Directory dedicated for Products-in-Hot-Sale Web Scraper at Mercado Libre\Mexico.
	- \Ofertas_MX: This directory has the first version of the web scrapper, (innactictive).
	- \Top_ML_Products_per_Cat : This directory contains the last version of the webscraper for MX and BZ markets. (current active):
		-The following dictionary contains the categories that the webscraper crawls:
		```
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
		```
	- \Xpath_experiment: Just for experiments in XLM/XPATH (innactictive).

## Files in AZ_testing branch:
- \'Amazon Scraper'\: Directory dedicated for Products in Top Sells at Amazon Mexico.
	-amazon_boxes.py : Obtains the top sold products, extratinc:
		1) Rank
		2) Product Name
		3) Image URL
		4) Product URL
		5) Stars
		6) Reviews
		7) Author (books, music)/Company (industrial products)
		8) Edition (books, music)/Console (videogames)
