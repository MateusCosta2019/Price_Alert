from Module.scrapper import ScrapeData
import os 
from Module.logger import etlLogger
from datetime import datetime
from Module.load_data_s3 import UploadDataIntoS3

LabelProcess = 'WebScrapping'

LOGGER_OBJ = etlLogger(project_name='WebScrapping')
LOGGER_OBJ.info(f'--->{LabelProcess}<---')
LOGGER_OBJ.info(f'Start:{datetime.today().strftime("%Y-%m-%d %H:%M")}')

def sendtobucket():
    proj_path = os.path.dirname(__file__)
    direxport = os.path.join(proj_path, 'datasets', 'Raw')
    s3_bucket = 'price-files-all-stores'

    upload = UploadDataIntoS3(s3_bucket=s3_bucket, folder_path=direxport, logger=LOGGER_OBJ)
    upload.upload_to_s3()
    upload.drop_files()

def executorMagazine():
    url = 'https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/'
    proj_path = os.path.dirname(__file__)
    filename = f'DataSmartPhonesMagazineLuiza{datetime.today().strftime("%Y%m%d")}.csv'
    direxport = os.path.join(proj_path, 'datasets', 'Raw', filename)
    variables = dict({
        'Cards': ['li', 'sc-eCihoo BCSuy'],
        'Item': ['h2','sc-kOjCZu enKhKW'],
        'Original_Price': ['p', 'sc-kDvujY gcLiKJ sc-dcntqk cJvvNV'],
        'Price': ['p', 'sc-kDvujY jDmBNY sc-ehkVkK kPMBBS'],
        'Installment': ['p', 'sc-kDvujY szpaO sc-eVspGN QAigN'],
        'Reviews': ['span', 'sc-hgRfpC dOenOK'],
        })

    scrapper = ScrapeData(logger=LOGGER_OBJ, url=url, tag_cookies='.gVxVwR', tag_btn_pag='button[aria-label="Go to next page"]', 
                        path=direxport, separtor='|', variables=variables)
    
    scrapper.accept_cookies()
    rep = 0

    while rep < 16:
        rep += 1
        try:
            scrapper.integratesoup()
            scrapper.get_cards()
            scrapper.scraping()
            LOGGER_OBJ.info("--> Crawler performed successfully.")

            scrapper.next_page()
        except Exception as e:
            print(e)
            break
    
    scrapper.extract_csv()

def executorML():
    url = 'https://lista.mercadolivre.com.br/celulares-smartphones#deal_print_id=c0e995d0-a98d-11ed-b11b-a59bf15bac8d&c_id=carousel&c_element_order=1&c_campaign=BOLOTA_CELULARES-E-SMARTPHONES&c_uid=c0e995d0-a98d-11ed-b11b-a59bf15bac8d'    
    proj_path = os.path.dirname(__file__)
    filename = f'DataSmartPhonesML{datetime.today().strftime("%Y%m%d")}.csv'
    direxport = os.path.join(proj_path, 'datasets', 'Raw', filename)
    variables = dict({ # pagina 5 l8star
        'Cards': ['div', 'ui-search-result__wrapper shops__result-wrapper'],
        'Item': ['h2','ui-search-item__title shops__item-title'],
        'Original_Price': ['s', 'price-tag ui-search-price__part ui-search-price__original-value shops__price-part price-tag__disabled'],
        'Price': ['span', 'price-tag-fraction'],
        'Installment': ['span', 'ui-search-item__group__element shops__items-group-details ui-search-installments ui-search-color--LIGHT_GREEN'],
        'Reviews': ['span', 'ui-search-reviews__amount'],
        })

    scrapper = ScrapeData(logger=LOGGER_OBJ, url=url, tag_cookies='', tag_btn_pag='.andes-pagination__button--next .andes-pagination__link', 
                        path=direxport, separtor='|', variables=variables)
    
    rep = 0

    while rep < 39:
        rep += 1
        try:
            scrapper.integratesoup()
            scrapper.get_cards()
            scrapper.scraping()
            LOGGER_OBJ.info("--> Crawler performed successfully.")

            scrapper.next_page()
        except Exception as e:
            print(e)
            break
    
    scrapper.extract_csv()
    
if __name__=='__main__':
    executorMagazine()
    executorML()
    sendtobucket()