from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime

# Set pandas to display all columns in DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import json


# FUNCTIONS
def query_finviz_news(URL):
    """
    Parsing HTML code to extract Finviz News Information

    :param URL: (string) value for Finviz News URL
    :return: (list) Dictionary of data pull saved in empty list
    """

    # Header to avoid response auth error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Send a GET request to the URL
    response = requests.get(URL, headers=headers)

    # check if request was succesful
    if response.status_code == 200:
        # parse html
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve the webpage: Status code {response.status_code}")

    print("Pulling News Table from Finviz...")

    # Empty List
    data_ = []

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

            # Append the extracted information to the news_data list
            data_.append({'date': date, 'title': title, 'url': url, 'source': source})
    return data_


def preprocess_finviz_data(data_):
    """
    Preprocess the Finviz news dataframe.
    1. Drop any NaN rows that are empty. 2. reformat date column 3. filter by today's news only

    :param data_: list of dictionary html parsed data
    :return: pd.DataFrame
    """
    print("Preprocessing the Finviz News Table...")
    # Put the dictionary into a DataFrame
    finviz_news_df = pd.DataFrame(data_)
    # Drop any empty rows
    finviz_news_df = finviz_news_df.dropna()
    # Convert String Date format to datetime
    finviz_news_df['date_'] = pd.to_datetime(finviz_news_df['date'] + f'-{datetime.now().year}', format='%b-%d-%Y')
    # Convert datetime objects to date objects (without time)
    finviz_news_df['date_'] = finviz_news_df['date_'].dt.date
    # Today's date
    today = datetime.now().date()
    # Filter by today's date
    finviz_news_today_df = finviz_news_df[finviz_news_df['date_'] == today]
    # Reset Index
    finviz_news_today_df = finviz_news_today_df.reset_index()
    # Create an empty column for article content
    finviz_news_today_df['article_content'] = None
    return finviz_news_today_df


def fetch_article_content(url, source):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    article_content = ""
    print(url, ': ', source)
    if source == 'CNBC':
        response = requests.get(url, headers=headers)
        if response.status_code == 200:  # Check if the request was successful.
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('div', class_='group')
            article_content = ' '.join([article.text for article in articles])
        else:
            print(f"Failed to fetch article for {source}")
            article_content = None

    elif source == 'BBC':
        # BBC currently pulls for only some, yet since the news seems unrelevent to
        # finance also too many are restricted to UK only
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id='__NEXT_DATA__')
            # If script_tag is truthy, proceed with the rest of the code
            if script_tag:
                data = json.loads(script_tag.string) if script_tag.string else {}
                contents = find_contents(data)
                article_content = ' '.join(
                    block.get('model', {}).get('text', '')
                    for content in contents if content.get('type') == 'text'
                    for block in content.get('model', {}).get('blocks', [])
                )
            else:
                print(f"Failed to fetch article for {source}")
                article_content = None

    elif source == 'Yahoo Finance':
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            body = soup.find_all('div', id='caas-content-body')
            # Initialize an empty string to hold all paragraphs concatenated together
            for item in body:
                # For each div in body, find all <p> tags and concatenate their texts
                for p in item.find_all('p'):
                    article_content += p.text + " "  # Adds a space after each paragraph
        else:
            print(f"Failed to fetch article for {source}")
            article_content = None

    else:
        print(f"Source {source} not supported.")
        article_content = None

    return article_content


# Define the find_contents function outside to avoid redefinitions
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

# Finviz News URL by Source
FINVIZ_NEWS_URL = 'https://finviz.com/news.ashx?v=2'

# check if the request was successful

data = query_finviz_news(FINVIZ_NEWS_URL)
today_fn_df = preprocess_finviz_data(data)
# Apply the fetch_article_content function to rows, passing the URL and source
for index, row in today_fn_df.iterrows():
    today_fn_df.at[index, 'article_content'] = fetch_article_content(row['url'], row['source'])




################

driver.get(CNBC_URL)
# Convert the driver page source to a soup object
soup = BeautifulSoup(driver.page_source, 'html.parser')



# Apply the fetch_article_content function to rows, passing the URL and source
for index, row in yahoo_df.iterrows():
    yahoo_df.at[index, 'article_content'] = fetch_article_content(row['url'], row['source'])

import numpy as np

yahoo_df = today_fn_df[today_fn_df.source == 'Yahoo Finance']
