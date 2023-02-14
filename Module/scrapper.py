from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 

class ScrapeData:
    def __init__(self, url:str, tag_cookies:str, tag_btn_pag:str, path:str, separtor:str, logger:str, variables:dict):
        self.logger = logger

        self.driver = webdriver.Chrome('chromedriver')
        self.driver.get(url)
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")

        self.tag_cookies = tag_cookies
        self.tag_btn_pag = tag_btn_pag
        self.variables = variables

        self.path = path
        self.dataset = []
        self.separtor = separtor

    def accept_cookies(self):
        try:
            self.logger.info('Accepting cookies from the page')
            self.driver.find_element(By.CSS_SELECTOR, self.tag_cookies).click()
        except Exception as e:
            self.logger.warn(f'Unable to find cookie acceptance button erro: {e}')

    def next_page(self):
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(5)
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.tag_btn_pag))
            )
            self.logger.info('Going to next page')
            next_button.click() 

        except Exception as e:
            self.logger.warn('End of scraping, next button not found.')
            self.driver.quit()

    def extract_csv(self):
        self.logger.info("--> Starting creation of .csv")
        try:
            df = pd.DataFrame(data=self.dataset)
            df.to_csv(path_or_buf=self.path, sep=self.separtor)
            self.logger.info("--> Csv successfully create")
            return True
        except Exception as e:
            self.logger.error(f"--> Unable to extract csv, ERROR:{e}")
            return False

    def scraping(self):
        try:
            card = self.soup.find_all(self.variables['Cards'][0], class_=self.variables['Cards'][1])
            if len(card) <= 0:
                self.logger.warn('--> No cards were found, check that the class entered is correct')
                return False 
        except Exception as e:
            self.logger.error(f'--> It was not possible to get the cards from the page')
        
        for product in card:
            Item = product.find(self.variables['Item'][0], class_=self.variables['Item'][1]).text

            Original_Price = product.find(self.variables['Original_Price'][0], class_=self.variables['Original_Price'][1])
            Original_Price = Original_Price.text if Original_Price else 'null'

            Price = product.find(self.variables['Price'][0], class_=self.variables['Price'][1])
            Price = Price.text if Price else 'null'

            Installment = product.find(self.variables['Installment'][0], class_=self.variables['Installment'][1])
            Installment = Installment.text if Installment else 'null'
            
            Reviews = product.find(self.variables['Reviews'][0], class_=self.variables['Reviews'][1])
            Reviews = Reviews.text if Reviews else 'null'

            self.dataset.append([Item, Price, Original_Price, Installment, Reviews])