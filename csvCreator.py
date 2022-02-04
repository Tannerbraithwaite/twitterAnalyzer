import csv

csvFile = open("data.csv", "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)

csvWriter.writerow(['author_id', 'created_at', 'geo', 'id', 'lang', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet', 'user_created_at', 'user_description', 'user_id', 'user_name', 'user_follower_count', 'user_following_count', 'user_listed_count', 'user_tweet_count', 'username', 'user_verification_status', 'date'])
csvFile.close()