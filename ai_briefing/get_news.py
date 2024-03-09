import requests
from api_keys import NEWS_API_KEY
from newsapi import NewsApiClient
from datetime import datetime, timedelta

# Constants
q = 'finance'
SOURCES = 'the-wall-street-journal, bloomberg, fortune, business-insider, financial-post'
TODAY = datetime.today().strftime("%Y-%m-%d")
YESTERDAY = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")


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


# Init
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# /v2/top-headlines/sources

newsapi.get_sources(category='business', language='en')
# get all list of sources
sources = newsapi.get_sources()['sources']
# List comprehension to filter IDs where language is 'en'
filtered_sources_str = ', '.join([source['id'] for source in sources if source['language'] == 'en'
                                  and (source['category'] == 'general' or source['category'] == 'business')])



# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='finance, economy, stock, stock-market',
                                          sources=filtered_sources_str,
                                          # category='business',
                                          language='en')



# /v2/everything
all_articles = newsapi.get_everything(q='finance, economy',
                                      sources=filtered_sources_str,
                                      from_param='2024-02-23',
                                      to='2024-02-29',
                                      sort_by='popularity ',
                                      page=2)

# /v2/everything
all_articles2 = newsapi.get_everything(
                                      q='finance, economy, economic, stock, stock-market, investing',
                                      # sources='the-wall-street-journal',
                                      from_param=YESTERDAY,  # Adjust the start date as needed
                                      to=TODAY,  # Adjust the end date as needed
                                      language='en',
                                      sort_by='popularity',
                                      # page=1,  # Adjust to explore different pages of results
                                      # page_size=10)  # Fetch 10 articles
)

# /v2/everything
all_articles3 = newsapi.get_everything(
                                      q='AMLX',
                                      # sources='the-wall-street-journal',
                                      from_param=YESTERDAY,  # Adjust the start date as needed
                                      to=TODAY,  # Adjust the end date as needed
                                      language='en',
                                      sort_by='popularity',
                                      # page=1,  # Adjust to explore different pages of results
                                      # page_size=10)  # Fetch 10 articles
)


# /v2/everything
wsj_articles = newsapi.get_everything(
                                      # q='finance, economy, stock, stock-market',
                                      sources=SOURCES,
                                      from_param=YESTERDAY,  # Adjust the start date as needed
                                      to=TODAY,  # Adjust the end date as needed
                                      language='en',
                                      sort_by='popularity',
                                      # page=1,  # Adjust to explore different pages of results
                                      # page_size=10)  # Fetch 10 articles
)

# Concatenate all article contents into one large document
all_titles = "\n".join([article["title"] for article in all_articles2['articles']])
all_descs = "\n".join([article["description"] for article in all_articles2['articles']])
all_content = "\n".join([article["content"] for article in all_articles2['articles']])

# Assuming you want to print the titles, sources, and URLs of the articles
for article in all_articles['articles']:
    print(f"Title: {article['title']}")
    print(f"Source: {article['source']['name']}")
    print(f"URL: {article['url']}\n")

# Replace 'YOUR_API_KEY' with your actual NewsAPI key
api_key = 'YOUR_API_KEY'
base_url = 'https://newsapi.org/v2/everything?'

# Adjusting parameters to include a wider range of credible sources
parameters = {
    'q': 'finance AND (economy OR "stock market" OR cryptocurrency)',
    'sources': 'bloomberg,reuters,cnbc,financial-times,the-wall-street-journal',
    'sortBy': 'popularity',
    'apiKey': api_key
}

response = requests.get(base_url, params=parameters)
articles = response.json()

# Print titles and URLs of top articles
for article in articles['articles'][:5]:
    print(f"Title: {article['title']}\nURL: {article['url']}\n")