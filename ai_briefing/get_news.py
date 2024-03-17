import requests
from api_keys import NEWS_API_KEY
from newsapi import NewsApiClient
from datetime import datetime, timedelta

def see_available_categories(newsapi):
    try:
        from newsapi.const import categories
        print("Available categories:")
        for category in categories:
            print(f'Available Category is: {category}')
            # sources = newsapi.get_sources(category=category, language='en')
            # print(f'Available sources are {sources}')
    except ImportError:
        print("The 'categories' constant could not be found. Please refer to the News API documentation.")


# Constants
TODAY = datetime.today().strftime("%Y-%m-%d")
YESTERDAY = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
Q = "finance OR economy OR stock market OR cryptocurrency'"
DOMAINS = 'marketwatch.com, cnbc.com, bloomberg.com, wsj.com, reuters.com, foxbusiness.com, bbc.com, nytimes.com, finance.yahoo.com, investing.com'

# Init
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# get all list of sources
sources_list = newsapi.get_sources()['sources']
sources = [source['id'] for source in sources_list]

see_available_categories(newsapi)

# /v2/everything
news_articles = newsapi.get_everything(
                                      q=Q,
                                      # sources='bloomberg',
                                      domains=DOMAINS,
                                      from_param=YESTERDAY,  # Adjust the start date as needed
                                      to=TODAY,  # Adjust the end date as needed
                                      language='en',
                                      sort_by='popularity',
                                      # page=1,  # Adjust to explore different pages of results
                                      # page_size=10)  # Fetch 10 articles
)

len(news_articles['articles'])

# Filter by titles, descriptions, published dates, contents
filtered_data = [{'title': item['title'],
                  'description': item['description'],
                  'publishedAt': item['publishedAt'],
                  'content': item['content']}
                 for item in news_articles['articles']]



