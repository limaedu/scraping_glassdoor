import requests
import os
from bs4 import BeautifulSoup
import re
import pandas as pd
from log.log import MyLog
from glassdoor.glassdoor import Glassdoor
from decouple import config

log = MyLog('glassdoor')
 
def get_salaries(url):
    log.logger.info('Start of script.')

    open('content.html', 'a').close()

    html_file_size = os.path.getsize('content.html') 

    if html_file_size == 0: ## Avoid sending multiple requests and being blocked. Delete file for updated information
        log.logger.info('HTML not stored yet. Making request..')

        headers = {'user-agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers = headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            log.logger.error(err)
            raise 

        log.logger.info('Success in request.')
        with open('content.html', 'w', encoding='utf-8') as file:
            log.logger.info('Writing html to file..')
            file.write(response.text)

    with open('content.html', encoding = 'utf-8') as fp:
        log.logger.info('Reading from file..')
        soup = BeautifulSoup(fp, 'html.parser')

    salaries = {}
    rows = soup.find_all('div', {'data-test': re.compile('salaries-list-item-\d{1,2}$')})

    log.logger.info('Storing salaries...')
    for row in rows:
        company = row.find('h3', {'data-test': re.compile('salaries-list-item-.*-employer-name')}).text
        salary_text = row.find('div', {'data-test': re.compile('salaries-list-item-.*-salary-info')}).find('h3').text
        salary = salary_text.replace('\xa0','').replace('\xa0mil', '').replace('mil', '000').replace('.','').replace('R$','')
        salary = round((float(salary.strip().split('-')[0]) + float(salary.strip().split('-')[1]))/2) if '-' in salary else salary
        salaries[company] = str(salary)

    log.logger.info('End of script.')

    df_salaries = pd.DataFrame.from_dict(salaries.items())
    df_salaries.columns  = ['Company', 'Salary']

    return df_salaries

with Glassdoor() as driver:
    try:
        driver.load_page(config('URL_LANDING_PAGE'))
        driver.navigate_to_salaries('Rio de Janeiro', 'Engenheiro de software')
        get_salaries(driver.current_url)
        pass
    except Exception as err:
        log.logger.error(err)

