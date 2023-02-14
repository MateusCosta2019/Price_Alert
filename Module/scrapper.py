from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 

dataset = []

# helper functions
def accept_cookies(driver, id, logger):
    try:
        logger.info('Accepting cookies from the page')
        driver.find_element(By.CSS_SELECTOR, id).click()
    except Exception as e:
        logger.warn('Unable to find cookie acceptance button')

def next_page(driver, xpath, logger):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, xpath))
        )
        logger.info('Going to next page')
        next_button.click() 

    except Exception as e:
        logger.warn('End of scraping, next button not found.')
        driver.quit()

def extract_csv(path, sep, logger):
    try:
        logger.info("--> Starting creation of .csv")
        df = pd.DataFrame(data=dataset)
        df.to_csv(path_or_buf=path, sep=sep)
        logger.info("--> Csv successfully create")
    except Exception as e:
        logger.error(f"--> Unable to extract csv, ERROR:{e}")

# Scraping functions

def MLscraping(driver, soup, logger):
    try:
        card = soup.find_all('div', class_='ui-search-result__wrapper shops__result-wrapper')
        for ap in card:
            item = ap.find('h2', class_='ui-search-item__title shops__item-title').text

            preco_original = ap.find('s', 'price-tag ui-search-price__part ui-search-price__original-value shops__price-part price-tag__disabled')
            preco_original = preco_original.text if preco_original else 'null'

            tag_price = ap.find('span', 'price-tag ui-search-price__part shops__price-part')
            value = tag_price.find('span', 'price-tag-fraction').text

            parcelas = ap.find('span', class_='ui-search-item__group__element shops__items-group-details ui-search-installments ui-search-color--LIGHT_GREEN')
            parcelas = parcelas.text if parcelas else 'null'
            
            review = ap.find('span', 'ui-search-reviews__amount')
            review = review.text if review else 'null'
        
            dataset.append([item, value, preco_original, parcelas, review])
            
    except Exception as e:
        logger.error('ERROR: Unable to get apartment information.', e)
        driver.quit()

def Magazinescraping(driver, soup, logger):
    try:
        card = soup.find_all('li', class_='sc-eCihoo BCSuy')
        for ap in card:
            item = ap.find('h2', class_='sc-kOjCZu enKhKW').text

            preco_original = ap.find('p', 'sc-kDvujY gcLiKJ sc-dcntqk cJvvNV')
            preco_original = preco_original.text if preco_original else 'null'

            value = ap.find('p', 'sc-kDvujY jDmBNY sc-ehkVkK kPMBBS')
            value = value.text if value else 'null'

            parcelas = ap.find('p', class_='sc-kDvujY szpaO sc-eVspGN QAigN')
            parcelas = parcelas.text if parcelas else 'null'
            
            review = ap.find('span', 'sc-hgRfpC dOenOK')
            review = review.text if review else 'null'

            dataset.append([item, value, preco_original, parcelas, review])
            
    except Exception as e:
        logger.error('ERROR: Unable to get apartment information.', e)
        driver.quit()