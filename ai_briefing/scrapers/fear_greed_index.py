import requests
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_fear_grid_index(url, chromedriver_dir):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    FG_XPATH = '/html/body/div[1]/section[4]/section[1]/section[1]/div/section/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[2]'
    VIX_XPATH = '/html/body/div[1]/section[4]/section[1]/section[1]/div/section/div[7]/div[2]/span'

    # Make a request to the URL
    response = requests.get(url, headers=headers)

    print(response)

    # Check if the response was successful (status code 200)
    if response.status_code == 200:
        # Setup Chrome with webdriver_manager
        # sudo xattr -r -d com.apple.quarantine /Users/youngmincho/Project/finance/src/chromedriver-mac-arm64/chromedriver
        driver = webdriver.Chrome(service=Service(f'{chromedriver_dir}/chromedriver'))

        # Open the webpage 
        driver.get(url)

        # Wait for the element with the class 'market-fng-gauge__dial-number-value' to be present
        fear_greed_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'market-fng-gauge__dial-number-value'))
        )
        fear_greed_element_prev = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, FG_XPATH))
        )
        # Or using XPath (adjust based on actual HTML structure)
        vix_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, VIX_XPATH))
        )

        # Extract and print the value
        fg_value = int(fear_greed_element.text)
        fg_value_prev = int(fear_greed_element_prev.text)
        vix_value = vix_element.text

        print(f"Fear Greed Value: {fg_value}")


        # Clean up by closing the browser
        driver.quit()
    else:
        print(f"Failed to access {url} - Status Code: {response.status_code}")

    fear_grid_index = int(fg_value)

    return fear_grid_index

def main():
    FEAR_AND_GREED_URL = 'https://www.cnn.com/markets/fear-and-greed'
    CHROME_DRIVER_DIR = 'src/chromedriver-mac-arm64'
    fear_grid_index = get_fear_grid_index(FEAR_AND_GREED_URL, CHROME_DRIVER_DIR)
    print(fear_grid_index)

if __name__ == "__main__":
    main()
