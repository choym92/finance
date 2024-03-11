from google_trend import fetch_top_trends
from get_news import fetch_news_articles


def main():
    # Fetch top 5 trending company queries from Google Trends
    top_companies = fetch_top_trends()

    # Iterate through the list of top companies and fetch related news articles for each
    for company in top_companies:
        print(f"Fetching news for {company}...")
        news_articles = fetch_news_articles(company)

        # Process or display the fetched news articles as needed
        for article in news_articles:
            print(article)  # This is a placeholder; customize it according to your data structure


if __name__ == "__main__":
    main()