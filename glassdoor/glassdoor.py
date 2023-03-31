from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

class Glassdoor(webdriver.Chrome):
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(fr"--user-data-dir=C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data")
        super(Glassdoor, self).__init__(ChromeDriverManager().install(), options = self.options)
        self.implicitly_wait(20)
        self.maximize_window()
        self.current_window = self.current_window_handle

    def load_page(self, url: str) -> None:
        self.get(url)
        time.sleep(3)

    def navigate_to_salaries(self, location: str, job_title: str = None, company_name: str = None) -> None:
        search_input = self.find_element(By.CSS_SELECTOR, ('input[data-test="search-bar-keyword-input"]'))
        search_input.send_keys(job_title) if job_title is not None else search_input.send_keys(company_name)

        arrow_down = self.find_element(By.CSS_SELECTOR, ('span[class="SVGInline arrowDown"]'))
        arrow_down.click()
        salary_element = self.find_element(By.XPATH, "//Span[text()='Salários']")
        salary_element.click()

        location_input = self.find_element(By.CSS_SELECTOR, ('input[id="sc.location"]'))
        location_input.send_keys(Keys.CONTROL + 'a')
        location_input.send_keys(Keys.DELETE)
        location_input.send_keys(location)

        search_button = self.find_element(By.CSS_SELECTOR, ('button[data-test="search-bar-submit"]'))
        search_button.click()





