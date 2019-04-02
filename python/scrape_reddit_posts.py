#!/usr/bin/env python3
import praw
from textblob import TextBlob
import time
import json
import os
import mysql.connector

dirname = os.path.dirname(__file__)
reddit_config_file = os.path.join(dirname, '../reddit_config.json')

with open(reddit_config_file) as json_data_file:
    reddit_config = json.load(json_data_file)

reddit = praw.Reddit(client_id=reddit_config['client_id'],
                     client_secret=reddit_config['client_secret'],
                     user_agent=reddit_config['user_agent'])

#print(reddit.read_only)
interval = 10
current_time = int(time.time())
past_posts_time = current_time - (interval * 60)

# scraped variables
posts = 0
good_posts = 0
bad_posts = 0

for submission in reddit.subreddit('Bitcoin').new():
    # Only take the posts from the past 10 min
    if (submission.created_utc < past_posts_time):
        break

    posts += 1
    blob = TextBlob(submission.title)
    polarity = blob.sentiment.polarity
    #print(submission.title)
    #print('Polarity: ' + str(polarity))
    if polarity >= 0:
        good_posts += 1
    else:
        bad_posts += 1

print('Posts: ' + str(posts))
print('Good Posts: ' + str(good_posts))
print('Bad Posts: ' + str(bad_posts))

configFile = os.path.join(dirname, '../mysql_config.json')
with open(configFile) as json_data_file:
    config = json.load(json_data_file)

mydb = mysql.connector.connect(
    host=config["host"],
    port=config["port"],
    user=config["user"],
    passwd=config["password"],
    database=config["database"]
)

mycursor = mydb.cursor()

createTableSql = 'CREATE TABLE IF NOT EXISTS`currencies`.`' + 'reddit_bitcoin' + '`( `id` INT NOT NULL AUTO_INCREMENT , `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , `posts` INT NOT NULL , `good` INT NOT NULL , `bad` INT NOT NULL, PRIMARY KEY (`id`)) ENGINE = InnoDB;'
mycursor.execute(createTableSql)

mydb.commit()

sql = 'INSERT INTO ' + 'reddit_bitcoin' + ' (posts, good, bad) VALUES (%s, %s, %s)'
val = (posts, good_posts, bad_posts)
mycursor.execute(sql, val)
mydb.commit()