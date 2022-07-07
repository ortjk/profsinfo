from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

import useful_functions
import rateprof

names_url = 'https://www.mun.ca/engineering/about/our-people/faculty-and-instructor-profiles/'

options = Options()
# chrome v103.0.5060.114 (latest official version) cannot be used due to a semi-unavoidable bug
options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'
driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
driver.get(names_url)

# get and format the names from a table from the link
elem = driver.find_element(By.CLASS_NAME, "table-striped")
names = elem.find_elements(By.CSS_SELECTOR, 'td')
names = names[:-1]
names = list(map(useful_functions.clean_name, names))

# create a new csv file with information from ratemyprof on names, school, and subject using pandas
new_csv = pd.DataFrame(rateprof.prof_searcher(names, school_name='memorial university of newfoundland', subject='Engineering', driver=driver))
new_csv.to_csv('proffs.csv')

driver.close()
