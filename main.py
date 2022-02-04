# Import modules
import mysql.connector
from mysql.connector import Error
import os
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob


class TweetObject():

    def __init__(self, host, database, user):
        self.password = os.environ['PASSWORD']
        self.host = host
        self.database = database
        self.user = user


    def MySQLConnect(self, query):
        """
        Connects to an sql database ti extract data and return a pd dataframe
        Parameters:
        _______________
        param: string: SQL query
        Returns: pandas dataframe
        """

        try:
            #connect to the database
            conn = mysql.connector.connect(host=self.host, database=self.database, user=self.user, password=self.password, charset = 'utf8')

            if conn.is_connected():
                print("Successfully connected to twitter SQL database")

                cursor = conn.cursor()
                cursor.execute(query)

                ##get data and store in a pandas df
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns = ['date', 'tweet'])
                print(df.head())

        except Error as e:
            print(e)

        cursor.close()
        conn.close()

        return df

    def clean_tweets(self, df):
        """
        intakes raw tweets and cleans them by removing stopwords, punctuation, html, emoticons
        and converts them all words to lowercase
        Parameters:
        __________________
        arg :pandas dataframe
        Returns: pandas dataframe
        """
        stopword_list = stopwords.words('english')
        wordnet_lemmatizer = WordNetLemmatizer()
        df["clean_tweets"] = None
        df['len'] = None
        for i in range(0, len(df['tweet]'])):
            #remove everything thats not a letter
            exclusion_list = ['[^a-zA-z]', 'rt', 'http', 'co', 'RT']
            exclusions = '|'.join(exclusion_list)
            text = re.sub(exclusions, ' ', df['tweet'][i])
            text = text.lower()
            words = text.splot()
            words = [wordnet_lemmatizer.lemmatize(word) for word in words if not word in stopword_list]
            df['clean_tweets'][i] = ' '.join(words)
            df['len'] = np.array([len(tweet) for tweet in df["clean_tweets"]])

        return df


    def sentiment(self, tweet):
        """
        This function analyses tweets based on sentiment analyses using TextBlob
        :param tweet:
        :return: Sentiment(on a scale of -1 to 1)
        """
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity> 0:
            return 1
        elif analysis.sentiment.polarity ==0:
            return 0
        else:
            return -1

    def save_to_csv(selfself, df):
        """
        saves cleaned data for further analysis
        :param pandas dataframe:
        :return:
        """
        try:
            df.to_csv("clean_tweets.csv")
            print("\n")
            print("csv successfully saved. \n")

        except Error as e:
            print(e)

    def word_cloud(self, df):
        """
        plots a dataframe using matplotlib
        :param pandas dataframe:
        """
        plt.subplots(figsize = (12, 10))
        wordcloud = WordCloud(background_color='white', width=1000, height=800).generate(" ".join(df['clean_tweets']))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()

if __name__ =='__main__':
    t = TweetObject( host = 'localhost', database = 'twitterdb', user = 'root')
    data = t.MySQLConnect("SELECT created_at, tweet FROM `TwitterDB`.`Golf`;")
    data = t.cleantweets(data)
    data['Sentiment'] = np.array([t.sentiment(x) for x in data['clean_tweets']])
    t.word_cloud(data)
    t.save_to_csv(data)

    pos_tweets = [tweet for index, tweet in enumerate(data['clean_tweets']) if data["Sentiment"][index] > 0]
    neg_tweets = [tweet for index, tweet in enumerate(data['clean_tweets']) if data["Sentiment"][index] < 0]
    pos_tweets = [tweet for index, tweet in enumerate(data['clean_tweets']) if data["Sentiment"][index] > 0]

    print("percentage of positive tweets: {}%".format(100*(len(pos_tweets)/len(data['clean_tweets']))))
	print("percentage of negative tweets: {}%".format(100*(len(neg_tweets)/len(data['clean_tweets']))))
	print("percentage of neutral tweets: {}%".format(100*(len(neu_tweets)/len(data['clean_tweets']))))