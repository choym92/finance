from pytrends.request import TrendReq
import pandas as pd

# Set pandas to display all columns in DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

pytrends = TrendReq(hl='en-US')

keyword_data = pytrends.realtime_trending_searches(pn='US')

cats = pytrends.categories()

cats.keys()

for a in cats['children']:
    print(a)

KW = 'stock'
pytrends.build_payload(kw_list=[KW], cat=107, timeframe='now 7-d', geo='', gprop='')

pytrends.build_payload(kw_list=[KW], cat=16, timeframe='now 1-d', geo='', gprop='news')


# Get related topics
related_topics = pytrends.related_topics()
print(related_topics[KW]['top'][['value', 'formattedValue','topic_title']])
print(related_topics[KW]['rising'][['value', 'formattedValue','topic_title']])

related_Queries = pytrends.related_queries()
print(related_Queries[KW]['rising'])


trending_searches = pytrends.trending_searches(pn='united_states')
print(trending_searches)





pytrends.suggestions('stock market')