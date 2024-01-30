from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import xlwings as xw
import time # Import time module for delays
from Improved_Functions import add_data, intialize_master, converter, get_data, check_amendment

###Takes in the CIK ID, location of master excel on computer, location of where the first excel would be saved, location of where the second excel would be saved
def execute(ID, master_location, newdata_location, newdata_copy_location):
    driver = webdriver.Chrome() # Ensure the path is correct

    ### gets to page with all of the files for the firm
    search_check = True
    while search_check:
        driver.get('https://www.sec.gov/edgar/search-and-access') #opens SEC
        try: # handles the ad popup by reloading it if an error is thrown since ad is in the way
            searcher = driver.find_element(By.XPATH, '//*[@id="global-search-box"]') #finds searchbox using xpath
            searcher.click()
            searcher.send_keys(ID) #types in CIK ID
            time.sleep(2) #waits 2 seconds so that the autosuggest has enough time
            searcher.send_keys(Keys.DOWN)
            searcher.send_keys(Keys.ENTER)
        except:
            search_check = True #keeps loop going
        time.sleep(.5)
        if 'search' not in driver.current_url:
            search_check = False #ends loop once search is done

    ### Gets name of firm
    time.sleep(.5)
    search_name = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/h3/span').text #name of firm

    ### Opens converter and switches control back to main page
    driver.execute_script("window.open('');") #new tab
    driver.switch_to.window(driver.window_handles[1]) #switches control to it
    # PSA window_handles go in order that the tab was opened
    driver.get('https://www.convertcsv.com/xml-to-csv.htm')
    driver.switch_to.window(driver.window_handles[0]) #switches back to main page

    ### Initializes Master Excel 
    master_wb = intialize_master(master_loc=master_location, name=search_name)

    ### Clicks on first filing
    box = driver.find_element(By.XPATH, '//*[@id="searchbox"]') #finds the searchbox to filter types of documents
    box.click()
    box.send_keys('13F')
    full_number_text = driver.find_element(By.XPATH, '/html/body/main/div[5]/div/div[3]/div[4]').text[18:26]
    num_entries = ''
    for i in range(len(full_number_text)): #gets the total number of entries and stores it in a variable
        if full_number_text[i].isnumeric():
            num_entries = num_entries + full_number_text[i]
    num_entries = int(num_entries)
    row=1 #iterator
    while row<=num_entries:
        doc_type = driver.find_element(By.XPATH, f'/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody/tr[{row}]/td[1]').text
        if 'A' not in doc_type: #if not an amendment
            next = driver.find_element(By.XPATH, f'/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody/tr[{row}]/td[2]/div/a[2]') #filing
            driver.execute_script('arguments[0].scrollIntoView(true)', next)
            next.click()

            ### Switches control to new tab
            time.sleep(.5)
            driver.switch_to.window(driver.window_handles[2]) #switches to filing tab just opened
            year = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/div[1]/div[2]').text[0:4]
            try: #accounts for listings not in xml format
                driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/table/tbody/tr[5]/td[3]/a').click()#opens xml file
            except:
                driver.close()
                row+=1
                driver.switch_to.window(driver.window_handles[0])
                continue
            time.sleep(.5)
            xml = driver.find_element(By.CSS_SELECTOR, 'body').text #gets the entire page's text
            index = xml.index('<')
            xml_data = xml[index:] #isolates just the xml data
            driver.close()

            ###Switches control to xml to excel converter
            converter(web_driver=driver, data=xml_data)

            ###Moves data from new excel to Master
            add_data(master_book=master_wb, newdata_loc=newdata_location, name=search_name, file_year=year)

            ### Increasing row and returns to first page
            driver.switch_to.window(driver.window_handles[0])
            row+=1
        elif 'A' in driver.find_element(By.XPATH, f'/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody/tr[{row+1}]/td[1]').text: #if there are two amendments
            ### gets the data from the two amendments and inputs them into master excel
            year_1, xml_data_1 = get_data(web_driver=driver, ind=row)
            converter(web_driver=driver, data=xml_data_1)
            driver.switch_to.window(driver.window_handles[0])

            year_2, xml_data_2 = get_data(web_driver=driver, ind=row+1)
            converter(web_driver=driver, data=xml_data_2)
            driver.switch_to.window(driver.window_handles[0])
            add_data(master_book=master_wb, newdata_loc=newdata_copy_location, name=search_name, file_year=year_2) #put the full amendment first to handle the correct headers
            add_data(master_book=master_wb, newdata_loc=newdata_location, name=search_name, file_year=year_1)

            row+=3 #increases by 3 so that we skip over the amendments and the file its amending
        else:
            ### gets the data from the amendment based on which kind it is and puts it into 2 files
            year_1, xml_data_1 = get_data(web_driver=driver, ind=row)
            converter(web_driver=driver, data=xml_data_1)
            driver.switch_to.window(driver.window_handles[0])
            
            year_2, xml_data_2 = get_data(web_driver=driver, ind=row+1)
            converter(web_driver=driver, data=xml_data_2)
            driver.switch_to.window(driver.window_handles[0])

            if check_amendment(newdata_loc_1=newdata_location, newdata_loc_2=newdata_copy_location): #checks which kind of amendment - True=overwritten, False=addition
                add_data(master_book=master_wb, newdata_loc=newdata_location, name=search_name, file_year=year_1) #do not append actual file since alrady overwritten
                os.remove(newdata_copy_location) #deletes file after used
            else:
                add_data(master_book=master_wb, newdata_loc=newdata_copy_location, name=search_name, file_year=year_2) #put the full amendment first to handle the correct headers
                add_data(master_book=master_wb, newdata_loc=newdata_location, name=search_name, file_year=year_1)
            
            row+=2 #increase by 2 to skip over amendment and the file its amending


    master_wb.save(master_location) #saves