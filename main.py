from time import sleep
from Module.scrapper import zapscraping, accept_cookies, extract_csv, next_page
from selenium import webdriver
from bs4 import BeautifulSoup
import os 
from Module.logger import etlLogger
from datetime import datetime

LabelProcess = 'WebScrapping-RealState'

LOGGER_OBJ = etlLogger(project_name='WebScrapping-RealState')
LOGGER_OBJ.info(f'--->{LabelProcess}<---')
LOGGER_OBJ.info(f'Start:{datetime.today().strftime("%Y-%m-%d %H:%M")}')

def executorzap():
    LOGGER_OBJ.info('--> Start Porject')
    url = "https://www.zapimoveis.com.br/aluguel/apartamentos/"

    proj_path = os.path.dirname(__file__)
    filename = f'DatafromZap{datetime.today().strftime("%Y%m%d")}.csv'
    direxport = os.path.join(proj_path, 'datasets', filename)
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')

    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    accept_cookies(driver=driver, id="cookie-notifier-cta", logger=LOGGER_OBJ)

    x = 0
    while x < 101:
        x+=1
        try:
            LOGGER_OBJ.info("--> Starting crawler on ZAP Imoveis pages")
            zapscraping(driver=driver, soup=soup, logger=LOGGER_OBJ)
            LOGGER_OBJ.info("--> Crawler performed successfully.")

            next_page(driver=driver, xpath='button[aria-label="Próxima Página"]', logger=LOGGER_OBJ)
        except Exception as e:
            print(e)
            break

    extract_csv(path=direxport, sep='|', logger=LOGGER_OBJ)

if __name__=='__main__':
    executorzap()
