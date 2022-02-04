import os
from dotenv import load_dotenv
import requests
from datetime import date
import csv
from dateutil import parser
import time
#load API keys
load_dotenv()
#API_KEY = os.getenv('TWITTER_API_KEY')
#API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
#ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
#ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN')
#ClIENT_ID = os.getenv('TWITTER_CLIENT_ID')
#CLIENT_ID_SECRET = os.getenv("TWITTER_CLIENT_ID_SECRET")

keywordlist = ['Cryptocurrency lang:en', 'Bitcoin lang:en', 'Ethereum lang:en', "BlockChain lang:en", "Altcoin lang:en", "Coinbase lang:en", "HODL lang:en", ]


def auth():
    return os.getenv('TWITTER_BEARER_TOKEN')


def create_headers(bearer_token):
    return {"Authorization": "Bearer {}".format(bearer_token)}


def create_url(keyword, max_results=10):
    #end point
    search_url = "https://api.twitter.com/2/tweets/search/recent?"

    query_params = {'query': keyword,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token=None):
    params['next_token'] = next_token
    response = requests.request("GET", url, headers=headers, params=params)
    print(f"Endpoint Response Code: {response.status_code}")
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def append_to_csv(json_response, fileName):
    ##create a dump file
    counter = 0
    csvFile = open(fileName, 'a', newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #loop through the data in the twitter response
    for tweet, user in zip(json_response['data'], json_response['includes']['users']):
        author_id = tweet['author_id']
        created_at = parser.parse(tweet['created_at'])
        if ('geo' in tweet):
            geo = tweet['geo']['place_id']
        else:
            geo = ""
        tweet_id = tweet['id']
        lang = tweet['lang']
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']
        source = tweet['source']
        text = tweet['text']
        user_created_at = parser.parse(user['created_at'])
        user_description = user['description']
        user_id = user['id']
        user_name = user['name']
        user_followers_count = user['public_metrics']['followers_count']
        user_following_count = user['public_metrics']['following_count']
        user_listed_count = user['public_metrics']['listed_count']
        user_tweet_count = user['public_metrics']['tweet_count']
        user_username = user['username']
        user_verified = user['verified']
        today = date.today()

        res = [author_id, created_at, geo, tweet_id, lang, like_count, quote_count, reply_count, retweet_count, source, text, \
               user_created_at, user_description, user_id, user_name, user_followers_count, user_following_count, user_listed_count, user_tweet_count, user_username, user_verified, today]

        csvWriter.writerow(res)
        counter += 1

    csvFile.close()
    print(f"we've recieved {counter} tweets from this response")


if __name__=="__main__":
    bearer_token = auth()
    headers = create_headers(bearer_token)
    max_results = 100
    for keyword in keywordlist:
        url = create_url(keyword, max_results)
        json_response = connect_to_endpoint(url[0], headers, url[1])
        append_to_csv(json_response, 'data.csv')
        time.sleep(5)