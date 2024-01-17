from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
import time # Import time module for delays

driver = webdriver.Chrome() # Ensure the path is correct

driver.get('https://www.sec.gov/edgar/search-and-access') #opens SEC
### gets to page with all of the files for the firm
searcher = driver.find_element(By.XPATH, '//*[@id="global-search-box"]') #finds searchbox using xpath
searcher.click()
searcher.send_keys('SV Health')
time.sleep(2) #waits 2 seconds so that the autosuggest has enough time
searcher.send_keys(Keys.DOWN)
searcher.send_keys(Keys.ENTER)
time.sleep(2)
### Clicks on first filing
box = driver.find_element(By.XPATH, '//*[@id="searchbox"]') #finds the searchbox to filter types of documents
box.click()
box.send_keys('13F')
time.sleep(2)
row=1 #will use later to loop through all links
next = driver.find_element(By.XPATH, f'/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody/tr[{row}]/td[2]/div/a[2]')
next.click()
base_url = next.get_attribute('href')[:70]
new_url = base_url + 'primary_doc.xml'
time.sleep(2)
driver.switch_to.new_window()
driver.get(new_url)
time.sleep(2)

# going to use this link to try to help me loop through the files https://www.youtube.com/watch?v=rkAa0um6JR0


input("Press Enter to close the browser...")
driver.quit()