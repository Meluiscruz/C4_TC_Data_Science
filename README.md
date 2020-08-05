# C4_TC_DS_Repo
### Cohort 4 / Team Cesar / Data Science

This is the official C4-Team-Cesa Project for Data Science team.
This repo will have a branch per Scrapers focused on the following Web Sellers:

- Mercado Libre.
	- Mexico.
	- Brazil.
	- Argentina.

- Amazon.
	- Mexico.
	- Brazil.

- Alibaba.
- Walmart.
- Google Shopping.

**Note 1: ** During the development of this project, some of these Web Sellers could be changed, removed, extended, or decreased to other markets.

**Note 2: ** The Master branch is reserved for field versions of all Web Scrapers, Statistical Analysis, and Data Visualization. Files ready to be delivered to Backend and/or Frontend.

## Scope Source:

https://www.statista.com/topics/2453/e-commerce-in-latin-america/

## Files in ML_testing branch:
- \Web_Scraping_ML\Ofertas_MX\: Directory dedicated for Products-in-Hot-Sale Web Scraper at Mercado Libre\Mexico.
	- /venv: Enviroment.
	- CSV_Design.xlsx : Sketch of the main table before SQL scripting.
	- main.py : Web Scraper coding in Python Script .
	- ML_Mex_ofertas.code-workspace : code-workspace .
	- ML_XPath_exp.txt: First sketch of XPaths directory 

## Files in AZ_testing branch:
- \'Amazon Scraper'\: Directory dedicated for Products in Top Sells at Amazon Mexico.
	-The main file is -> amazon_scraper_boxes_df.py It obtains the top sold products, extratinc:
		- Date
		- Rank
		- Product Name
		- Image URL
		- Product URL
		- Stars
		- Reviews
		- Author (books, music)/Company (industrial products)
		- Edition (books, music)/Console (videogames)
	-Something to consider is that you can program a scrap n-times in steps of n-minutes. For examples:
		- If you want 2 scraps in one hour, it would be programed as:
		scrap_amazon_times(2, 30)
		- If you want 3 scraps in one hour, it would be programed as:
		scrap_amazon_times(3, 20)
