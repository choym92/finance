import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import json

class FinvizNewsScraper:
    def __init__(self):
        logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def query_finviz_news(self, URL):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(URL, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
            else:
                logging.error(f"Failed to retrieve the webpage: Status code {response.status_code}")
                return []

            print("Pulling News Table from Finviz...")

            data_ = []
            news_tables = soup.find_all('table', class_='styled-table-new is-rounded')
            news_tables = news_tables[:9]

            for news_table in news_tables:
                news_items = news_table.find_all('tr')
                for item in news_items:
                    date = item.find('td', class_='text-right').text if item.find('td', class_='text-right') else None
                    source = [item.find('a', rel="nofollow").text for item in news_items if item.find('a', rel="nofollow") is not None][0]
                    title_tag = item.find('a', class_='tab-link')
                    title = title_tag.text if title_tag else None
                    url = title_tag['href'] if title_tag else None
                    data_.append({'date': date, 'title': title, 'url': url, 'source': source})
            return data_
        except Exception as e:
            logging.error(f"An error occurred while querying Finviz news: {e}")
            return []

    def preprocess_finviz_data(self, data_):
        try:
            print("Preprocessing the Finviz News Table...")
            finviz_news_df = pd.DataFrame(data_)
            finviz_news_df = finviz_news_df.dropna()
            finviz_news_df['date_'] = pd.to_datetime(finviz_news_df['date'] + f'-{datetime.now().year}', format='%b-%d-%Y')
            finviz_news_df['date_'] = finviz_news_df['date_'].dt.date
            today = datetime.now().date()
            finviz_news_today_df = finviz_news_df[finviz_news_df['date_'] == today]
            finviz_news_today_df = finviz_news_today_df.reset_index(drop=True)
            finviz_news_today_df['article_content'] = None
            return finviz_news_today_df
        except Exception as e:
            logging.error(f"An error occurred while preprocessing Finviz data: {e}")
            return pd.DataFrame()

    def fetch_article_content(self, url, source):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            article_content = ""

            if source == 'CNBC':
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    articles = soup.find_all('div', class_='group')
                    article_content = ' '.join([article.text for article in articles])
                else:
                    logging.error(f"Failed to fetch article for {source}")
                    article_content = None

            elif source == 'BBC':
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    script_tag = soup.find('script', id='__NEXT_DATA__')
                    if script_tag:
                        data = json.loads(script_tag.string) if script_tag.string else {}
                        contents = self.find_contents(data)
                        article_content = ' '.join(
                            block.get('model', {}).get('text', '')
                            for content in contents if content.get('type') == 'text'
                            for block in content.get('model', {}).get('blocks', [])
                        )
                    else:
                        logging.error(f"May need to work on this later on java script not been parsed: {source}")
                        article_content = None
                else:
                    logging.error(f"Failed to fetch article for {source}")
                    article_content = None

            elif source == 'Yahoo Finance':
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    body = soup.find_all('div', id='caas-content-body')
                    for item in body:
                        for p in item.find_all('p'):
                            article_content += p.text + " "
                else:
                    logging.error(f"Failed to fetch article for {source}")
                    article_content = None

            else:
                logging.error(f"Source {source} not supported.")
                article_content = None

            return article_content
        except Exception as e:
            logging.error(f"An error occurred while fetching article content for {source}: {e}")
            return None

    def find_contents(self, data, key_to_find="contents"):
        if isinstance(data, dict):
            for key, value in data.items():
                if key_to_find in key:
                    return value
                else:
                    found = self.find_contents(value, key_to_find)
                    if found is not None:
                        return found
        elif isinstance(data, list):
            for item in data:
                found = self.find_contents(item, key_to_find)
                if found is not None:
                    return found
        return None

    def get_finviz_data(self):
        FINVIZ_NEWS_URL = 'https://finviz.com/news.ashx?v=2'
        data = self.query_finviz_news(FINVIZ_NEWS_URL)
        today_fn_df = self.preprocess_finviz_data(data)
        for index, row in today_fn_df.iterrows():
            today_fn_df.at[index, 'content'] = self.fetch_article_content(row['url'], row['source'])
        return today_fn_df

# # Example usage:
# # finviz_scraper = FinvizNewsScraper()
# # finviz_df = finviz_scraper.get_finviz_data()
# # print(finviz_df)