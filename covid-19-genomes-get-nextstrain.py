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

def processWebPage(webpageURL, datadir, driver, eachPath):

    print (str(datetime.datetime.now()) + ' Processing:' + eachPath)
    eachPath_FileName = str.replace(eachPath, '/', '_')
    for p in Path(datadir).glob('nextstrain*' + eachPath_FileName + '*.tsv'):
        p.unlink()
    driver.get(webpageURL + eachPath)
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

    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : r"C:\Dev\covid-19-genomes", 
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "C:/Dev/ChromeDriver/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

    webpageURL = 'https://nextstrain.org/'
    webpagePaths = ['community/aicbu/ncov/srilanka',
                    'community/alghoribi-lab/ncov/gcc',
                    'community/CHRF-Genomics/ncovBangladesh@main',
                    'community/fai-k/coni/Thailand',
                    'community/kkosaki/ncov/japan',
                    'community/quipupe/Nextstrain_Argentina', 
                    'community/quipupe/Nextstrain_Chile', 
                    'community/quipupe/Nextstrain_Ecuador', 
                    'community/quipupe/Nextstrain_Peru', 
                    'groups/neherlab/ncov/austria',
                    'groups/neherlab/ncov/belarus',
                    'groups/neherlab/ncov/belgium',
                    'groups/neherlab/ncov/bosnia-and-herzegovina',
                    'groups/neherlab/ncov/bulgaria',
                    'groups/neherlab/ncov/czech-republic',
                    'groups/neherlab/ncov/denmark',
                    'groups/neherlab/ncov/estonia',
                    'groups/neherlab/ncov/finland',
                    'groups/neherlab/ncov/france',
                    'groups/neherlab/ncov/germany',
                    'groups/neherlab/ncov/greece',
                    'groups/neherlab/ncov/hungary',
                    'groups/neherlab/ncov/iceland',
                    'groups/neherlab/ncov/india',
                    'groups/neherlab/ncov/ireland',
                    'groups/neherlab/ncov/israel',
                    'groups/neherlab/ncov/italy',
                    'groups/neherlab/ncov/latvia',
                    'groups/neherlab/ncov/lithuania',
                    'groups/neherlab/ncov/luxembourg',
                    'groups/neherlab/ncov/netherlands',
                    'groups/neherlab/ncov/norway',
                    'groups/neherlab/ncov/poland',
                    'groups/neherlab/ncov/portugal',
                    'groups/neherlab/ncov/romania',
                    'groups/neherlab/ncov/russia',
                    'groups/neherlab/ncov/serbia',
                    'groups/neherlab/ncov/slovakia',
                    'groups/neherlab/ncov/slovenia',
                    'groups/neherlab/ncov/spain',
                    'groups/neherlab/ncov/sweden',
                    'groups/neherlab/ncov/switzerland',
                    'groups/neherlab/ncov/turkey',
                    'groups/neherlab/ncov/united-kingdom',
                    'groups/spheres/ncov/USA',
                    'ncov/africa', 'ncov/asia', 'ncov/europe' , 'ncov/north-america', 'ncov/oceania', 'ncov/south-america'
                    ]
    # webpagePaths = ['groups/spheres/ncov/USA']
    datadir = 'C:/Dev/covid-19-genomes/'

    for eachPath in webpagePaths:
        processWebPage(webpageURL, datadir, driver, eachPath)

    driver.quit()

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()
