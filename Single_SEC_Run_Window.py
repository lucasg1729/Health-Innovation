from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
# from selenium.webdriver import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
import time # Import time module for delays

driver = webdriver.Chrome() # Ensure the path is correct

driver.get('https://www.sec.gov/edgar/search-and-access') #opens SEC
### gets to page with all of the files for the firm
searcher = driver.find_element(By.XPATH, '//*[@id="global-search-box"]') #finds searchbox using xpath
searcher.click()
name = 'SV Health'
searcher.send_keys(name)
time.sleep(2) #waits 2 seconds so that the autosuggest has enough time
searcher.send_keys(Keys.DOWN)
searcher.send_keys(Keys.ENTER)
time.sleep(2)
parent_window = driver.current_window_handle #gets the location ID to switch back to initial tab

### Clicks on first filing
box = driver.find_element(By.XPATH, '//*[@id="searchbox"]') #finds the searchbox to filter types of documents
box.click()
box.send_keys('13F')
time.sleep(2)
row=1 #will use later to loop through all links
next = driver.find_element(By.XPATH, f'/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody/tr[{row}]/td[2]/div/a[2]')
next.click()

### Switches control to new tab
all_handles = driver.window_handles
driver.switch_to.window(all_handles[1])
driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/table/tbody/tr[5]/td[3]/a').click()#opens xml file
time.sleep(1)
xml = driver.find_element(By.CSS_SELECTOR, 'body').text #gets the text of the xml data
index = xml.index('<')
xml_data = xml[index:]
time.sleep(2)

###Changes open tab to xml to excel converter
driver.get('https://www.convertcsv.com/xml-to-csv.htm')
conv_box = driver.find_element(By.XPATH, '//*[@id="txt1"]')
conv_box.click()
conv_box.send_keys(xml_data) #inputs xml data
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div[2]/input[2]').click() #downloads as excel
time.sleep(4)
os.remove("/Users/lucasg17/Downloads/convertcsv.xlsx") #deletes file after used

### How to right click
# actions = ActionChains(driver)
# down_link = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/table/tbody/tr[5]/td[3]/a')
# actions.context_click(down_link).perform()
# time.sleep(1)

# going to use this link to try to help me loop through the files https://www.youtube.com/watch?v=rkAa0um6JR0


input("Press Enter to close the browser...")
driver.quit()
