import requests
from bs4 import BeautifulSoup
import pandas as pd


def fetch_sp500_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11;Linux x86_64;rv:12.0) Gecko/20100101 Firefox/12.0'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', class_='table table-hover table-borderless table-sm')

        data = []
        for row in table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            if len(cols) > 6:
                company_name = cols[1].text.strip()
                symbol = cols[2].text.strip()
                portfolio_pct = cols[3].text.strip()
                price = cols[4].text.strip()
                change = cols[5].text.strip()
                pct_change = cols[6].text.strip().replace('%', '').replace('(', '').replace(')', '')
                data.append([company_name, symbol, portfolio_pct, price, change, float(pct_change)])

        df = pd.DataFrame(data, columns=['Company', 'Symbol', 'Portfolio%', 'Price', 'Chg', '% Chg'])
        return df
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        return pd.DataFrame()


# Example usage
url = 'https://www.slickcharts.com/sp500'
df = fetch_sp500_data(url)

df.sort_values(by='% Chg', ascending=False).head(10)