import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FEAR_AND_GREED_URL = 'https://www.cnn.com/markets/fear-and-greed'

# Make a request to the URL
response = requests.get(FEAR_AND_GREED_URL)

# Check if the response was successful (status code 200)
if response.status_code == 200:
    # Setup Chrome with webdriver_manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the webpage
    driver.get(FEAR_AND_GREED_URL)

    # Wait for the element with the class 'market-fng-gauge__dial-number-value' to be present
    fear_greed_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'market-fng-gauge__dial-number-value'))
    )
    fear_greed_element_prev = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH,
                                          '/html/body/div[1]/section[4]/section[1]/section[1]/div/section/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[2]'))
    )
    # Or using XPath (adjust based on actual HTML structure)
    vix_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, '/html/body/div[1]/section[4]/section[1]/section[1]/div/section/div[7]/div[2]/span'))
    )

    # Extract and print the value
    fg_value = int(fear_greed_element.text)
    fg_value_prev = int(fear_greed_element_prev.text)
    vix_value = vix_element.text

    print(f"Fear Greed Value: {fg_value}")


    # Clean up by closing the browser
    driver.quit()
else:
    print(f"Failed to access {FEAR_AND_GREED_URL} - Status Code: {response.status_code}")





fg_value = int(fg_value)





#a
#
#
#
# MARKET VOLATILITY
#
# CPI
#
# PPI
#
# Interest Rate - volatility, acceleration, derivative DELTA% LAGGING -1d vs cd,  -2d vs cd, -3d vs cd
