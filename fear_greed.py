from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome with webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
FEAR_AND_GREED_URL = 'https://www.cnn.com/markets/fear-and-greed'

# Open the webpage
driver.get(FEAR_AND_GREED_URL)

# Wait for the element with the class 'market-fng-gauge__dial-number-value' to be present
element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'market-fng-gauge__dial-number-value'))
)

# Extract and print the value
fg_value = element.text
print(f"Fear Greed Value: {fg_value}")

# Clean up by closing the browser
driver.quit()

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
