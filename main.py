from Module.scrapper import accept_cookies, extract_csv, next_page, MLscraping, Magazinescraping
from selenium import webdriver
from bs4 import BeautifulSoup
import os 
from Module.logger import etlLogger
from datetime import datetime

LabelProcess = 'WebScrapping-RealState'

LOGGER_OBJ = etlLogger(project_name='WebScrapping-RealState')
LOGGER_OBJ.info(f'--->{LabelProcess}<---')
LOGGER_OBJ.info(f'Start:{datetime.today().strftime("%Y-%m-%d %H:%M")}')

def executorML():
    LOGGER_OBJ.info('--> Start Project')
    url = "https://lista.mercadolivre.com.br/celulares-smartphones#deal_print_id=c0e995d0-a98d-11ed-b11b-a59bf15bac8d&c_id=carousel&c_element_order=1&c_campaign=BOLOTA_CELULARES-E-SMARTPHONES&c_uid=c0e995d0-a98d-11ed-b11b-a59bf15bac8d"

    proj_path = os.path.dirname(__file__)
    filename = f'DataSmartPhonesML{datetime.today().strftime("%Y%m%d")}.csv'
    direxport = os.path.join(proj_path, 'datasets', filename)

    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # accept_cookies(driver=driver, id="cookie-notifier-cta", logger=LOGGER_OBJ)

    x = 0
    LOGGER_OBJ.info("--> Starting crawler on ZAP Imoveis pages")
    while x < 40:
        x+=1
        try:
            MLscraping(driver=driver, soup=soup, logger=LOGGER_OBJ)
            LOGGER_OBJ.info("--> Crawler performed successfully.")

            next_page(driver=driver, xpath='.andes-pagination__button--next .andes-pagination__link', logger=LOGGER_OBJ)
        except Exception as e:
            print(e)
            break
 
    extract_csv(path=direxport, sep='|', logger=LOGGER_OBJ)

def executorMagazine():
    LOGGER_OBJ.info('--> Start Project')
    url = "https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/"
    proj_path = os.path.dirname(__file__)
    filename = f'DataSmartPhonesMagazineLuiza{datetime.today().strftime("%Y%m%d")}.csv'
    direxport = os.path.join(proj_path, 'datasets', filename)

    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    accept_cookies(driver=driver, id=".gVxVwR", logger=LOGGER_OBJ)

    x = 0
    LOGGER_OBJ.info("--> Starting crawler on Magazine Luiza pages")
    while x < 16:
        x+=1
        try:
            Magazinescraping(driver=driver, soup=soup, logger=LOGGER_OBJ)
            LOGGER_OBJ.info("--> Crawler performed successfully.")

            next_page(driver=driver, xpath='button[aria-label="Go to next page"]', logger=LOGGER_OBJ)
        except Exception as e:
            print(e)
            break
 
    extract_csv(path=direxport, sep='|', logger=LOGGER_OBJ)

if __name__=='__main__':
    executorMagazine()
