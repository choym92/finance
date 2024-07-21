import sys
import os
from api_keys import NEWS_API_KEY
import pandas as pd

# Append the 'ai_briefing' directory to sys.path
project_directory = 'C:\\Users\\Paul Cho\\Documents\\YM\\Project\\finance'
ai_briefing_directory = os.path.join(project_directory, 'ai_briefing')
sys.path.append(ai_briefing_directory)


from get_news import NewsScraper
from finviz import FinvizNewsScraper

def main():
    # Scrape news data
    finviz_scraper = FinvizNewsScraper()
    finviz_data = finviz_scraper.get_finviz_data()

    news_scraper = NewsScraper(NEWS_API_KEY)
    news_data = news_scraper.scrape_news()

    # Data preprocessing
    # Example: Merge dataframes on a common column (if applicable)
    combined_data = pd.concat([news_data[['date_', 'title', 'url', 'content']], finviz_data[['date_', 'title', 'url', 'content']]], axis=0)

    # Data analysis/processing
    # Example: Filter data, perform analysis, etc.

    # Save or output data
    # combined_data.to_csv('combined_data.csv', index=False)
    # print("Data processing complete. Saved to combined_data.csv")

if __name__ == "__main__":
    main()
