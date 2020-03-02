# -*- coding: utf-8 -*-

import praw
import pandas as pd
import datetime as dt
from datetime import datetime

CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = ''
USER_NAME = ''


reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

def get_srch_posts(srch_term, limit=100):
    srch_data_list = []
    ml_subreddit = reddit.subreddit(srch_term)
    for post in ml_subreddit.hot(limit=limit):
        srch_data_list.append([post.title, post.selftext, post.author, post.id, post.score, post.url, post.created, post.subreddit, post.num_comments, post.name, post.permalink])
    srch_df = pd.DataFrame(srch_data_list, columns=['post_title', 'post_body', 'post_author', 'post_id', 'post_score', 'post_url', 'post_created', 'subreddit', 'num_comments', 'name', 'post_permalink'])
    return srch_df

def get_user_data():
    post_data_list = []
    ml_reddit_user = reddit.redditor(USER_NAME).submissions.new()
    for post in ml_reddit_user:
        post_data_list.append([post.title, post.selftext, post.author, post.id, post.score, post.url, post.created, post.subreddit, post.num_comments, post.name, post.permalink])
    post_df = pd.DataFrame(post_data_list, columns=['post_title', 'post_body', 'post_author', 'post_id', 'post_score', 'post_url', 'post_created', 'subreddit', 'num_comments', 'name', 'post_permalink'])
    return post_df

def create_excel(data_list, exl_name):
    data_df = pd.DataFrame(data_list)
    sht_name = str(datetime.now()).replace(':', '%').split('.')[0]
    data_df.to_excel(str(exl_name), index=False, sheet_name=sht_name)

def get_date(created):
    return dt.datetime.fromtimestamp(created)



if __name__ == '__main__':
    # Get user posts data
    gud_data = get_user_data()
    _timestamp = gud_data["post_created"].apply(get_date)
    # write data to excel file
    create_excel(gud_data, 'red_user_data_reddit_data.xlsx')
    
    #Get Search posts data for EpicGamesPC
    srch = get_srch_posts('EpicGamesPC', 100)
    #Write data to excel file
    create_excel(srch, 'EpicGamesPC_reddit_data.xlsx')
    
    #Get Search posts data for FORTnITE
    srch = get_srch_posts('FORTnITE', 100)
    #Write data to excel file
    create_excel(srch, 'FORTnITE_reddit_data.xlsx')
    
    
    #Get Search posts data for FortniteCompetitive
    srch = get_srch_posts('FortniteCompetitive', 100)
    #Write data to excel file
    create_excel(srch, 'FortniteCompetitive_redd_data.xlsx')
    
    
    #Get Search posts data for BattleBreakers
    srch = get_srch_posts('BattleBreakers', 100)
    #Write data to excel file
    create_excel(srch, 'BattleBreakers_redd_data.xlsx')

