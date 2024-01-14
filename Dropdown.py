from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time # Import time module for delays

driver = webdriver.Chrome() # Ensure the path is correct

driver.get('https://www.sec.gov/edgar/search-and-access')

searcher = driver.find_element(By.XPATH, '//*[@id="global-search-box"]')
searcher.click()
searcher.send_keys('SV Health')
time.sleep(2)
searcher.send_keys(Keys.DOWN)
searcher.send_keys(Keys.ENTER)
time.sleep(2)

box = driver.find_element(By.XPATH, '//*[@id="searchbox"]')
box.click()
box.send_keys('13F')

input("Press Enter to close the browser...")
driver.quit()