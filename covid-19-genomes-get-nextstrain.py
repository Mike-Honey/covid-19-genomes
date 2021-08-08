import datetime
import gzip
import json
import numpy
import os
import pandas
from pathlib import Path
import pytest
import requests
import shutil
import time
import urllib.request
import zipfile

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

def processWebPage(webpageURL, datadir, driver, eachPath, metadata_name):

    print (str(datetime.datetime.now()) + ' Processing:' + eachPath)
    eachPath_FileName = str.replace(eachPath, '/', '*')
    for p in Path(datadir).glob('nextstrain*' + eachPath_FileName + '*.*'):
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
    element = FindElem(driver, By.NAME, metadata_name)
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

    datadir = 'C:/Dev/covid-19-genomes/'
    ncov_open_filename_out = 'nextstrain_ncov_open_metadata.tsv'
    for p in Path(datadir).glob(ncov_open_filename_out):
        p.unlink()
 
    webpageURL = 'https://nextstrain.org/'
    webpagePaths = ['community/aicbu/ncov/srilanka',
                    'community/alghoribi-lab/ncov/gcc',
                    'community/CHRF-Genomics/ncovBangladesh@main',
                    'community/fai-k/coni/Thailand',
                    # 'community/kkosaki/ncov/japan',
                    'community/quipupe/Nextstrain_Argentina', 
                    # 'community/quipupe/Nextstrain_Chile', 
                    'community/quipupe/Nextstrain_Ecuador', 
                    'community/quipupe/Nextstrain_Peru', 
                    'groups/spheres/ncov/USA'
                    # 'ncov/open/africa', 
                    # 'ncov/open/asia', 
                    # 'ncov/open/europe' , 
                    # 'ncov/open/north-america', 
                    # 'ncov/open/oceania', 
                    # 'ncov/open/south-america'
                    ]
    # webpagePaths = ['groups/spheres/ncov/USA']
    metadata_name = "Metadata (TSV)"

    for eachPath in webpagePaths:
        processWebPage(webpageURL, datadir, driver, eachPath, metadata_name)

    webpageURL = 'http://auspice.finlaymagui.re/'
    webpagePaths = ['ncov/north-america/canada']
    metadata_name = "All Metadata (TSV)"

    for eachPath in webpagePaths:
        processWebPage(webpageURL, datadir, driver, eachPath, metadata_name)

    webpageURL = 'https://auspice.cov2.cl/'
    webpagePaths = ['ncov/chile-global']
    metadata_name = "Metadata (TSV)"

    for eachPath in webpagePaths:
        processWebPage(webpageURL, datadir, driver, eachPath, metadata_name)

    webpageURL = 'https://nextstrain.org/'
    webpagePaths = [
                    'community/kkosaki/ncov/japan',
                    'community/quipupe/Nextstrain_Chile', 
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
                    # 'groups/swiss/ncov/switzerland/?f_country=Switzerland',
                    'ncov/gisaid/africa', 
                    'ncov/gisaid/asia', 
                    'ncov/gisaid/europe' , 
                    'ncov/gisaid/north-america', 
                    'ncov/gisaid/oceania', 
                    'ncov/gisaid/south-america'
                    ]
    # webpagePaths = ['groups/spheres/ncov/USA']
    metadata_name = "TimeTree (Nexus)"

    for eachPath in webpagePaths:
        processWebPage(webpageURL, datadir, driver, eachPath, metadata_name)

    driver.quit()
    print (str(datetime.datetime.now()) + ' individual downloads complete, zipping results ...')

    zipfilename = 'nextstrain_ncov_metadata.zip'
    for p in Path(datadir).glob(zipfilename):
        p.unlink()
    zipf = zipfile.ZipFile(datadir + zipfilename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(datadir):
        for file in files:
            if file.startswith('nextstrain_') and ( file.endswith('.tsv') or file.endswith('.nexus')) :
                zipf.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(datadir, '..')))
    zipf.close()

    print (str(datetime.datetime.now()) + ' Processing ncov/open')
    webpageURL = 'https://data.nextstrain.org/files/ncov/open/metadata.tsv.gz'
    filename = 'metadata.tsv'
    with urllib.request.urlopen(webpageURL) as response, open(datadir + filename + '.gz', 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    with gzip.open(datadir + filename + '.gz', 'rb') as f_in:
        with open(datadir + ncov_open_filename_out, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print (str(datetime.datetime.now()) + ' Finished!')
    exit()

if __name__ == '__main__':
    main()
