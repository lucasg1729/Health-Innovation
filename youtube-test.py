from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time # Import time module for delays

driver = webdriver.Chrome() # Ensure the path is correct

driver.get('https://youtube.com')

try:
    # Using CSS Selectors instead of XPath
    searchbox = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#search'))
    )
    searchbox.click() # Click the search box before sending keys
    searchbox.clear()  # Clear the search box if needed
    searchbox.send_keys('Music')

    searchButton = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#search-icon-legacy'))
    )
    searchButton.click()

    # Add further code here

    # Adding a delay to observe the browser behavior
    time.sleep(10)

except TimeoutException:
    print("Element not found within the given time.")
    # Handle the exception as needed

# finally:
#     # Ensure the browser always closes
#     driver.quit()
input("Press Enter to close the browser...")
driver.quit()

### Trying to use urllib to open sec
# import urllib.request

# base_url = urllib.request.urlopen('https://www.sec.gov/edgar/browse/?CIK=1587143')
# output = base_url.read()
# print(output)
# base_url.close()