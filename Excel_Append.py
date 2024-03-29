# from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import os
import xlwings as xw
import time # Import time module for delays

def add_data(master_book, newdata_loc, name, file_year): #adds data to master excel from other file
    master_sheets = master_book.sheets
    newdata_wb = xw.Book(newdata_loc) #opens the new data in an excel
    if master_book.sheets[name]['A1'].value is None: #if it is a new sheet gets the headers too
        new_data_raw = newdata_wb.sheets[0].range('A1').expand().value 
        newrow = 0
        temp_data = [i[:] for i in new_data_raw] #gets the data in a form of a nested list
        for data_list in temp_data[1:]: #adds years 
            data_list.insert(0, file_year)
        temp_data[0].insert(0, 'Year') #adds year header
    else:
        new_data_raw = newdata_wb.sheets[0].range('A2').expand().value
        newrow = master_sheets[name].range('A1').end('down').row
        temp_data = [i[:] for i in new_data_raw] #gets the data in a form of a nested list
        if type(temp_data[0]) == type([]):
            for data_list in temp_data: #adds years 
                data_list.insert(0, file_year)
        else:
            temp_data.insert(0, file_year)
            temp_data.pop(len(temp_data)-1) #goes 4 times to get rid of links at the end
            temp_data.pop(len(temp_data)-1)
            temp_data.pop(len(temp_data)-1)
            temp_data.pop(len(temp_data)-1)
    print(temp_data)
    print(newrow)
    print(master_book.sheets[name][newrow,0].value)
    master_book.sheets[name][newrow,0].value = temp_data #appends data to master excel
    time.sleep(.5)
    newdata_wb.close() #closes new data excel
    os.remove(newdata_loc) #deletes file after used
    master_book.save("/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx") #saves

def intialize_master(master_loc, name): #opens the master excel and adds a new sheet accordingly
    master_wb = xw.Book(master_loc)
    master_sheets = master_wb.sheets
    sheet_names = []
    for j in master_wb.sheets:
        sheet_names.append(j.name)
    if len(master_sheets)==1 and master_wb.sheets[0]['A1'].value is None: ### initializes list with name of sheets for later use
        if master_sheets[0].name != name:
            master_sheets[0].name = name
        sheet_names = [master_sheets[0].name] 
    if name not in sheet_names: ### creates new sheet for vc firm if it doesn't have one
        master_wb.sheets.add(name)
        sheet_names.append(name)
    return master_wb

def converter(web_driver, data): #uses the converter to change the xml to excel
    web_driver.switch_to.window(web_driver.window_handles[1]) #switches to converter
    if 'google' in web_driver.current_url: #handles google ad popups
        web_driver.get('https://www.convertcsv.com/xml-to-csv.htm') 
    conv_box = web_driver.find_element(By.XPATH, '//*[@id="txt1"]')
    web_driver.execute_script('arguments[0].scrollIntoView(true)', conv_box)
    conv_box.click()
    conv_box.clear()
    conv_box.send_keys(data) #inputs xml data
    time.sleep(.5)
    web_driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div[2]/input[2]').click() #downloads as excel

def get_data(web_driver, ind): #retrieves the data from the SEC filings page for each firm
    next = web_driver.find_element(By.XPATH, f'/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody/tr[{ind}]/td[2]/div/a[2]') #filing
    web_driver.execute_script('arguments[0].scrollIntoView(true)', next)
    next.click()

    ### Switches control to new tab
    time.sleep(.5)
    web_driver.switch_to.window(web_driver.window_handles[2]) #switches to filing tab just opened
    file_year = web_driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/div[1]/div[2]').text[0:4]
    web_driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/table/tbody/tr[5]/td[3]/a').click()#opens xml file
    time.sleep(.5)
    xml = web_driver.find_element(By.CSS_SELECTOR, 'body').text #gets the entire page's text
    index = xml.index('<')
    data_text = xml[index:] #isolates just the xml data
    web_driver.close()
    return (file_year, data_text)

def check_amendment(newdata_loc_1, newdata_loc_2): #returns True if the amendment is overwriting and False if it is adding
    newdata_wb = xw.Book(newdata_loc_1) #opens the new data in an excel
    newdata_wb2 = xw.Book(newdata_loc_2)
    val1 = newdata_wb.sheets[0]['A2'].value
    val2 = newdata_wb2.sheets[0]['A2'].value
    time.sleep(.5)
    newdata_wb.close() #closes new data excel
    newdata_wb2.close()
    if val1 is val2: #compares the first cell to see if its overwriting or not
        return True
    else:
        return False
