from datetime import datetime, timedelta
from newsapi import NewsApiClient
import pandas as pd

import requests
from dotenv import load_dotenv
import os
# Load environment variables from the .env file
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

class NewsScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.newsapi = NewsApiClient(api_key=api_key)

    def see_available_categories(self):
        try:
            from newsapi.const import categories
            print("Available categories:")
            for category in categories:
                print(f'Available Category is: {category}')
                # sources = self.newsapi.get_sources(category=category, language='en')
                # print(f'Available sources are {sources}')
        except ImportError:
            print("The 'categories' constant could not be found. Please refer to the News API documentation.")

    def scrape_news(self):
        TODAY = datetime.today().strftime("%Y-%m-%d")
        YESTERDAY = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        Q = "finance OR economy OR stock market OR cryptocurrency'"
        DOMAINS = 'marketwatch.com, cnbc.com, bloomberg.com, wsj.com, reuters.com, foxbusiness.com, bbc.com, nytimes.com, finance.yahoo.com, investing.com'

        sources_list = self.newsapi.get_sources()['sources']
        sources = [source['id'] for source in sources_list]

        self.see_available_categories()

        news_articles = self.newsapi.get_everything(
                                            q=Q,
                                            # sources='bloomberg',
                                            domains=DOMAINS,
                                            from_param=YESTERDAY,
                                            to=TODAY,
                                            language='en',
                                            sort_by='popularity',
                                        )

        filtered_data = [{'date_': item['publishedAt'],
                          'title': item['title'],
                          'url': item['url'],
                          'description': item['description'],
                          'content': item['content']}
                         for item in news_articles['articles']]

        news_df = pd.DataFrame(filtered_data)
        news_df['date_'] = pd.to_datetime(news_df['date_']).dt.strftime('%m-%d-%Y')
        return news_df

# # Example usage:
# news_scraper = NewsScraper(NEWS_API_KEY)
# news_data = news_scraper.scrape_news()
# print(news_data)