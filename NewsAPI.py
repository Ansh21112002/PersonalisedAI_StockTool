import requests
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from newsapi import NewsApiClient


api_key = '5fc65c42b6ba4139b7b8e6d57cbcbff9'
endpoint = 'https://newsapi.org/v2/everything'


nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def getNews(ticker):
    params = {
        'q': ticker,
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 100,
    }
    response = requests.get(endpoint, params=params)
    data = json.loads(response.text)
    
    news_data = []
    for article in data['articles']:
        title = article['title']
        description = article['description']
        url = article['url']
        url2i = article['urlToImage']
        text = title + ' ' + description
        sentiment_score = sia.polarity_scores(text)['compound']
        news_data.append({
            'title': title,
            'description': description,
            'url': url,
            'urlToImage': url2i,
            'sentiment_score': sentiment_score
        })

    return news_data



