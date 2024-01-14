from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time # Import time module for delays

driver = webdriver.Chrome() # Ensure the path is correct

driver.get('https://www.sec.gov/edgar/search-and-access')

### Tried to use xpaths but closed too early
# searchbox = driver.find_element_by_xpath('//*[@id="global-search-box"]')
# searchbox.send_keys('SV Health')

# searchbutton = driver.find_element_by_xpath('//*[@id="global-search-form"]/fieldset/div/input[4]')
# searchbutton.click()

try:
    # Using CSS Selectors instead of XPath
    searchbox = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#global-search-box')) #delays until searchbar is found
    )
    searchbox.click() # Click the search box before sending keys
    searchbox.clear()  # Clear the search box if needed
    searchbox.send_keys('SV Health')

    searchButton = WebDriverWait(driver, 20).until( #currently not working
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#global-search-form > fieldset > div > input.global-search-button'))
    )
    searchButton.click()

except TimeoutException:
    print("Element not found within the given time.")
    # Handle the exception as needed

input("Press Enter to close the browser...")
driver.quit()

### Trying to use urllib to open sec
# import urllib.request

# base_url = urllib.request.urlopen('https://www.sec.gov/edgar/browse/?CIK=1587143')
# output = base_url.read()
# print(output)
# base_url.close()