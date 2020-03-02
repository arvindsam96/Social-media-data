#!/usr/bin/env python
# coding: utf-8

import tweepy
import pandas as pd
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)


def write_to_excel(data_obj):
    tweet_data = []
    for tweet in data_obj:
        tweet_dict = {}
        tweet_dict['tweet-id'] = int(tweet.id)
        tweet_dict['tweet-text'] = str(tweet.text)
        tweet_dict['tweet-created-at'] = tweet.created_at
        tweet_dict['source'] = tweet.source
        
        hash = ''
        if tweet.entities['hashtags'] != None:
            for helem in tweet.entities['hashtags']:
                hash = helem['text'].join(' ,')
            tweet_dict['hashtags'] = hash
        else:
            tweet_dict['hashtags'] = ''
            
        if tweet.coordinates != None:
            for key,value in tweet.coordinates.items():
                tweet_dict['coordinates-type'] = tweet.coordinates['type']
                tweet_dict['coordinates-coordinates'] = tweet.coordinates['coordinates']
        else:
            tweet_dict['coordinates-type'] = ''
            tweet_dict['coordinates-coordinates'] = ''
            
        scr_name = ''
        if tweet.entities['user_mentions'] != None:
            for ument in tweet.entities['user_mentions']:
                scr_name = ument['screen_name'].join(' ,')
            tweet_dict['user_mentions-screen_name'] = scr_name
        else:
            tweet_dict['user_mentions-screen_name'] = ''
            
        name = ''
        if tweet.entities['user_mentions'] != None:
            for ument in tweet.entities['user_mentions']:
                name = ument['name'].join(' ,')
            tweet_dict['user_mentions-name'] = name
        else:
            tweet_dict['user_mentions-name'] = ''
            
        scr_id = ''
        if tweet.entities['user_mentions'] != None:
            for ument in tweet.entities['user_mentions']:
                scr_id = str(ument['id']).join(' ,')
            tweet_dict['user_mentions-id'] = scr_id
        else:
            tweet_dict['user_mentions-id'] = ''
            
        tweet_url = ''
        if tweet.entities['urls'] != None:
            for elem in tweet.entities['urls']:
                tweet_url = elem['url'].join(' ,')
            tweet_dict['tweet_url'] = tweet_url
        else:
            tweet_dict['tweet_url'] = ''
        
        if tweet.place != None:
            tweet_dict['place-id'] = str(tweet.place.id)
            tweet_dict['place-url'] = str(tweet.place.url)
            tweet_dict['place-name'] = str(tweet.place.name)
        else:
            tweet_dict['place-id'] = ''
            tweet_dict['place-url'] = ''
            tweet_dict['place-name'] = ''

        tweet_dict['contributors'] = tweet.contributors
        tweet_dict['is_quote_status'] = tweet.is_quote_status
        tweet_dict['retweet_count'] = tweet.retweet_count
        tweet_dict['favorite_count'] = tweet.favorite_count
        tweet_dict['favorited'] = tweet.favorited
        tweet_dict['retweeted'] = tweet.retweeted
        tweet_dict['lang'] = tweet.lang
        tweet_dict['in_reply_to_status_id'] = tweet.in_reply_to_status_id
        tweet_dict['in_reply_to_user_id'] = tweet.in_reply_to_user_id
        tweet_dict['in_reply_to_screen_name'] = tweet.in_reply_to_screen_name
        tweet_dict['user-id'] = tweet.user.id
        tweet_dict['user-name'] = tweet.user.name
        tweet_dict['user-screen_name'] = tweet.user.screen_name
        tweet_dict['user-location'] = tweet.user.location
        tweet_dict['user-description'] = tweet.user.description
        tweet_dict['user-url'] = tweet.user.url
        tweet_dict['user-protected'] = tweet.user.protected
        tweet_dict['user-followers_count'] = tweet.user.followers_count
        tweet_dict['user-listed_count'] = tweet.user.listed_count
        tweet_dict['user-created_at'] = tweet.user.created_at
        tweet_dict['user-favourites_count'] = tweet.user.favourites_count
        tweet_dict['user-friends_count'] = tweet.user.friends_count
        tweet_dict['user-geo_enabled'] = tweet.user.geo_enabled
        tweet_dict['user-verified'] = tweet.user.verified
        tweet_dict['user-statuses_count'] = tweet.user.statuses_count
        tweet_dict['user-profile_background_image_url'] = tweet.user.profile_background_image_url
        tweet_dict['user-profile_image_url'] = tweet.user.profile_image_url
        tweet_dict['user-profile_image_url_https'] = tweet.user.profile_image_url_https
        tweet_dict['user-profile_use_background_image'] = tweet.user.profile_use_background_image
        # Create list to create dataframe
        tweet_data .append(tweet_dict)
    return tweet_data



def create_excel(data_list, exl_name):
    str(exl_name)
    data_df = pd.DataFrame(data_list)
    data_df.to_excel(exl_name, index=False)


if __name__ == '__main__':
    # Tweets from a respective user
    user_tweets = api.user_timeline()
    user_data = write_to_excel(user_tweets) 
    # Create excel for user data
    create_excel(user_data, 'user_data.xlsx')
    pages_list = ['EpicGames','fortnitegame', 'battlebreakers']
    for elem in pages_list:
        data = []
        excel_name = ''
        for page in tweepy.Cursor(api.user_timeline, id=elem).pages(40):
            page_data = {}
            wte_data = write_to_excel(page)
            data.extend(wte_data)
        excel_name = str(elem)+'_twitter_data.xlsx'
        create_excel(data, excel_name)