from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
# Set pandas to display all columns in DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def query_finviz_news(soup):
    """
    Parsing HTML code to extract Finviz News Information

    :param soup: Object
    :return: list Dictionary of data pull saved in empty list
    """

    print("Pulling News Table from Finviz")
    # Empty List
    data = []

    # Get all the tables
    news_tables = soup.find_all('table', class_='styled-table-new is-rounded')
    # First 9 tables are related to News, rest are Blogs
    news_tables = news_tables[:9]

    # Loop Through the news_tables
    for news_table in news_tables:
        news_items = news_table.find_all('tr')
        for item in news_items:
            # Extract the date, which is in a <td> tag with a specific class
            date = item.find('td', class_='text-right').text if item.find('td', class_='text-right') else None

            source = [item.find('a', rel="nofollow").text for item in news_items if
                      item.find('a', rel="nofollow") is not None][0]

            # The title and URL are in an <a> tag within a <td> with a specific class
            title_tag = item.find('a', class_='tab-link')
            title = title_tag.text if title_tag else None
            url = title_tag['href'] if title_tag else None

            # The source is a bit trickier; it's in a previous <tr> or another identifiable tag. You might need to adjust this part.
            # For simplicity, let's set it as 'Bloomberg' for now, but you'll need to adjust this based on the actual HTML structure.

            # Append the extracted information to the news_data list
            data.append({'date': date, 'title': title, 'url': url, 'source': source})
    return data

def preprocess_finviz_data(data):
    """

    :param data: list of dictionary html parsed data
    :return: pd.DataFrame
    """
    # Put the dictionary into a DataFrame
    finviz_news_df = pd.DataFrame(data)
    # Drop any empty rows
    finviz_news_df = finviz_news_df.dropna()
    # Convert String Date format to datetime
    finviz_news_df['date_'] = pd.to_datetime(finviz_news_df['date'] + f'-{datetime.now().year}', format='%b-%d-%Y')
    # Convert datetime objects to date objects (without time)
    finviz_news_df['date_'] = finviz_news_df['date_'].dt.date
    # Today's date
    today = datetime.now().date()
    # Filter by today's date
    today_fn_df = finviz_news_df[finviz_news_df['date_'] == today]
    # Reset Index
    today_fn_df = today_fn_df.reset_index()
    # Create an empty column for article content
    today_fn_df['article_content'] = None
    return today_fn_df


# Finviz News URL by Source
FINVIZ_NEWS_URL = 'https://finviz.com/news.ashx?v=2'

# Header to avoid response auth error
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the URL
response = requests.get(FINVIZ_NEWS_URL, headers=headers)

# check if the request was successful
if response.status_code == 200:
    # parse html
    soup = BeautifulSoup(response.text, 'html.parser')
    data = query_finviz_news(soup)
else:
    print(f"Failed to retrieve the webpage: Status code {response.status_code}")

import json
driver.get(CNBC_URL)
# Convert the driver page source to a soup object
soup = BeautifulSoup(driver.page_source, 'html.parser')

BBC_URL = 'https://www.bbc.com/news/technology-68535381'
bbc_response = requests.get(BBC_URL, headers=headers)
bbc_soup = BeautifulSoup(bbc_response.text, 'html.parser')





article = ' '.join([article.text for article in cnbc_articles])


def fetch_article_content(url, source):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:  # Check if the request was successful.
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize an empty string for article content
        article_content = ""

        if source == 'CNBC':
            cnbc_articles = soup.find_all('div', class_='group')
            article_content = ' '.join([article.text for article in cnbc_articles])
        elif source == 'BBC':
            bbc_response = requests.get(BBC_URL, headers=headers)
            bbc_soup = BeautifulSoup(bbc_response.text, 'html.parser')

            # Find the <script> tag with the JSON data
            script_tag = bbc_soup.find('script', id='__NEXT_DATA__')
            data = json.loads(script_tag.string) if script_tag and script_tag.string else {}

            # Function to recursively search for a key in nested dictionaries and lists
            def find_contents(data, key_to_find="contents"):
                if isinstance(data, dict):
                    for key, value in data.items():
                        if key_to_find in key:
                            return value
                        else:
                            found = find_contents(value, key_to_find)
                            if found is not None:
                                return found
                elif isinstance(data, list):
                    for item in data:
                        found = find_contents(item, key_to_find)
                        if found is not None:
                            return found
                return None

            # Use the find_contents function to dynamically locate the article contents
            contents = find_contents(data)

            # Extracting article content in a more concise way
            article_content = ' '.join(
                block.get('model', {}).get('text', '')
                for content in contents if content.get('type') == 'text'
                for block in content.get('model', {}).get('blocks', [])
            )
        return article_content
    else:
        print(f"Failed to fetch article for {source}")
        return None



# Apply the fetch_article_content function to rows, passing the URL and source
for index, row in today_fn_df.iterrows():
    today_fn_df.at[index, 'article_content'] = fetch_article_content(row['url'], row['source'])