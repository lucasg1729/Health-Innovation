from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
# import pandas as pd
import xlwings as xw
# from selenium.webdriver import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
import time # Import time module for delays

driver = webdriver.Chrome() # Ensure the path is correct

### gets to page with all of the files for the firm
search_check = True
while search_check:
    driver.get('https://www.sec.gov/edgar/search-and-access') #opens SEC
    searcher = driver.find_element(By.XPATH, '//*[@id="global-search-box"]') #finds searchbox using xpath
    searcher.click()
    searcher.send_keys('1587143')
    time.sleep(2) #waits 2 seconds so that the autosuggest has enough time
    searcher.send_keys(Keys.DOWN)
    searcher.send_keys(Keys.ENTER)
    time.sleep(2)
    if 'search' not in driver.current_url:
        search_check = False

parent_window = driver.current_window_handle #gets the location ID to switch back to initial tab

### Gets name of firm
search_name = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/h3/span').text

### Opens converter and switches control back to main page
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get('https://www.convertcsv.com/xml-to-csv.htm')
driver.switch_to.window(driver.window_handles[0])

### Clicks on first filing
box = driver.find_element(By.XPATH, '//*[@id="searchbox"]') #finds the searchbox to filter types of documents
box.click()
box.send_keys('13F')
time.sleep(2)
full_number_text = driver.find_element(By.XPATH, '/html/body/main/div[5]/div/div[3]/div[4]').text[18:26]
num_entries = ''
for i in range(len(full_number_text)):
    if full_number_text[i].isnumeric():
        num_entries = num_entries + full_number_text[i]
num_entries = int(num_entries)
row=1 #will use later to loop through all links
while row<=num_entries:
    next = driver.find_element(By.XPATH, f'/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody/tr[{row}]/td[2]/div/a[2]')
    next.click()

    ### Switches control to new tab
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[2])
    year = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/div[1]/div[2]').text[0:4]
    driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/table/tbody/tr[5]/td[3]/a').click()#opens xml file
    time.sleep(1)
    xml = driver.find_element(By.CSS_SELECTOR, 'body').text #gets the text of the xml data
    index = xml.index('<')
    xml_data = xml[index:]
    time.sleep(2)

    ###Switches control to xml to excel converter
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    conv_box = driver.find_element(By.XPATH, '//*[@id="txt1"]')
    driver.execute_script('arguments[0].scrollIntoView(true)', conv_box)
    conv_box.click()
    conv_box.send_keys(xml_data) #inputs xml data
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div[2]/input[2]').click() #downloads as excel
    # make sure to clear data before next submission will do this soon

    ###Moves data from new excel to Master
    master_wb = xw.Book("/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx")
    master_sheets = master_wb.sheets
    if len(master_sheets)==1: ### initializes list with name of sheets for later use
        if master_sheets[0].name != search_name:
            master_sheets[0].name = search_name
        sheet_names = [master_sheets[0].name] 
    if search_name not in sheet_names: ### creates new sheet for vc firm if it doesn't have one
        master_wb.sheets.add(search_name)
        sheet_names.append(search_name)

    newdata_wb = xw.Book("/Users/lucasg17/Downloads/convertcsv.xlsx")
    if master_wb.sheets[search_name]['A1'].value is None:
        new_data_raw = newdata_wb.sheets[0].range('A1').expand().value
        newrow = 0
        temp_data = [i[:] for i in new_data_raw]
        for data_list in temp_data[1:]:
            data_list.insert(0, 2000)
        temp_data[0].insert(0, 'Year')
    else:
        new_data_raw = newdata_wb.sheets[0].range('A2').expand().value
        newrow = master_sheets[0].range('A1').end('down').row
        temp_data = [i[:] for i in new_data_raw]
        for data_list in temp_data:
            data_list.insert(0, year)
    master_wb.sheets[search_name][newrow,0].value = temp_data
    master_wb.save("/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx")
    time.sleep(2)
    newdata_wb.close()
    os.remove("/Users/lucasg17/Downloads/convertcsv.xlsx") #deletes file after used

    ###closing tabs and returning to first page
    time.sleep(2)
    all_handles = driver.window_handles
    driver.switch_to.window(all_handles[0])


    ### Increasing row
    row+=1


# going to use this link to try to help me loop through the files https://www.youtube.com/watch?v=rkAa0um6JR0


input("Press Enter to close the browser...")
driver.quit()
