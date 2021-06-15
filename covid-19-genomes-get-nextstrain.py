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

def processWebPage(webpageURL, datadir, driver, eachRegion):

    print (str(datetime.datetime.now()) + ' Processing:' + eachRegion)
    for p in Path(datadir).glob('nextstrain*' + eachRegion + '*.tsv'):
        p.unlink()
    driver.get(webpageURL + eachRegion)
    time.sleep(30)
    element = FindElem(driver, By.CSS_SELECTOR, "button:nth-child(3) > span")
    element.click()
    element = FindElem(driver, By.CSS_SELECTOR, "button:nth-child(3) > span")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    element = FindElem(driver, By.CSS_SELECTOR, "body")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    element = FindElem(driver, By.NAME, "Metadata (TSV)")
    element.click()
    time.sleep(5)


def main():
    """
    Main - program execute
    """
    print (str(datetime.datetime.now()) + ' Starting ...')
    webpageURL = 'https://nextstrain.org/ncov/'
    webpageRegions = ['africa', 'asia', 'europe' , 'north-america', 'oceania', 'south-america']
    datadir = 'C:/Dev/covid-19-genomes/'

    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : r"C:\Dev\covid-19-genomes", 
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "C:/Dev/ChromeDriver/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

    for eachRegion in webpageRegions:
        processWebPage(webpageURL, datadir, driver, eachRegion)

    driver.quit()

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()
