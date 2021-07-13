import datetime
import numpy
import os
import pandas
from pathlib import Path
import requests
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def FindElem(driver: webdriver, driver_by, selector: str, Timeout: int = 300):
    while Timeout > 0:
        try:
            return driver.find_element(driver_by, selector)
        except: # if element isn't already loaded or doesn't exist
            time.sleep(1)
            Timeout -= 1
    raise RuntimeError(f"Page loading timeout") 

def processWebPage(eachURL, datadir, driver, eachCountry):

    print (str(datetime.datetime.now()) + ' Processing:' + eachCountry)
    driver.get(eachURL)
    time.sleep(30)
    for p in Path(datadir).glob('outbreakinfo_mutation_report_data_' + eachCountry + '.tsv'):
        p.unlink()
    element = FindElem(driver, By.CSS_SELECTOR, "#location-report-prevalence #download-btn small")
    element.click()
    element = FindElem(driver, By.CSS_SELECTOR, ".text-uppercase:nth-child(8) > .focustext")
    element.click()
    time.sleep(5)
    for p in Path(datadir).glob('outbreakinfo_mutation_report_data_20*.tsv'):
        p.rename(datadir + 'outbreakinfo_mutation_report_data_' + eachCountry + '.tsv')
    for p in Path(datadir).glob('outbreakinfo_mutation_report_data_20*.txt'):
        p.unlink()


def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')

    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : r"C:\Dev\covid-19-genomes", 
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "C:/Dev/ChromeDriver/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

    datadir = 'C:/Dev/covid-19-genomes/'
    webpageURL = 'https://outbreak.info/location-reports?loc=ZZZ&selected=S%3AE484K&selected=AV.1&selected=AY.1&selected=AY.2&selected=B.1.1.7&selected=B.1.1.7%20%2B%20S%3AE484K&selected=B.1.351&selected=B.1.617.1&selected=B.1.617.2&selected=B.1.1.318&selected=B.1.427&selected=B.1.429&selected=B.1.525&selected=B.1.526&selected=B.1.526.1&selected=B.1.526.2&selected=B.1.617&selected=B.1.617.1&selected=B.1.617.2&selected=B.1.617.3&pango=B.1.619&selected=B.1.619&pango=B.1.620&selected=B.1.620&pango=B.1.621&selected=B.1.621&selected=C.36.3&selected=C.37&selected=P.1&selected=P.1.1&selected=P.1.2&selected=P.2&selected=P.3'
    webpageCountries = ['AGO', 'ARG', 'AUS', 'BGD', 'BWA', 'CAN', 'CHE', 'CHL', 'COL', 'DEU', 'GBR', 'IDN', 'IND', 'IRL', 'ISR', 'JPN', 'KOR', 'NPL', 'NZL', 'PER', 'POL', 'PRT', 'RUS', 'SGP', 'THA', 'UGA', 'USA', 'ZAF']
    webpageCountries = ['KOR']

    for eachCountry in webpageCountries:
        eachURL = str.replace(webpageURL, 'loc=ZZZ' , 'loc=' + eachCountry )
        processWebPage(eachURL, datadir, driver, eachCountry)

    driver.quit()

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()
