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
        driver.find_element(By.ID, id).click()
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
        df = pd.DataFrame(data=dataset, columns=['valor', 'tipo_do_aluguel', 'descricao', 'condominium', 'iptu', 'andress', 'size', 'bedrooms', 'parking_spaces', 'bathrooms', 'news'])
        df.to_csv(path_or_buf=path, sep=sep)
        logger.info("--> Csv successfully create")
    except Exception as e:
        logger.error(f"--> Unable to extract csv, ERROR:{e}")

# Scraping functions
def zapscraping(driver, soup, logger):
    try:
        cards = soup.find_all('div', class_='card-listing simple-card')
        for apartments in cards:

            value = "".join([c for c in apartments.find('div', 'oz-datazap-stamp').text if c.isdigit()])

            rent_type = apartments.find('small', class_='simple-card__business_type_rental text-small')
            rent_type = rent_type.text.strip() if rent_type else "null"

            description = apartments.find('span', class_='simple-card__text text-regular')
            description = description.text if description else "null"

            condominium = apartments.find('span', 'card-price__value')
            condominium = condominium.text if condominium else "null"
            
            iptu = apartments.find('li', 'card-price__item iptu text-regular')
            iptu = "".join([c for c in iptu.text if c.isdigit()]) if iptu else "null"
            
            andress = apartments.find('h2', 'simple-card__address color-dark text-regular')
            andress = andress.text.strip() if andress else "null"

            size = "".join([c for c in apartments.find('li', 'feature__item text-small js-areas').text if c.isdigit()])
            bedrooms = "".join([c for c in apartments.find('li', 'feature__item text-small js-bedrooms').text if c.isdigit()])

            parking_spaces = apartments.find('li', 'feature__item text-small js-parking-spaces')
            parking_spaces = "".join([c for c in parking_spaces.text if c.isdigit()]) if parking_spaces else "null"
            
            bathrooms = "".join([c for c in apartments.find('li', 'feature__item text-small js-bathrooms').text if c.isdigit()])
            
            news = apartments.find('div', class_='simple-card__highligths')
            news = news.text if news else 'null'

            dataset.append([value, rent_type, description, condominium, iptu, andress, size, bedrooms, parking_spaces, bathrooms, news])
            
    except Exception as e:
        logger.error('ERROR: Unable to get apartment information.', e)
        driver.quit()

def quintoandarscraping():
    pass