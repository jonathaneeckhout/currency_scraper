#!/usr/bin/env python3
import praw
from textblob import TextBlob
import math


reddit = praw.Reddit(client_id='blabla',
                     client_secret='blabla',
                     user_agent='subSentiment')

print(reddit.read_only)

for submission in reddit.subreddit('Bitcoin').hot(limit=100):
    print(submission.title)
    blob = TextBlob(submission.title)
    print(blob.sentiment.polarity)
