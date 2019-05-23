import tweepy
import json
import math
import pymongo
import twitter_key
from tqdm import tqdm

def authenticate_twitter_app():

    auth = tweepy.OAuthHandler(twitter_key.consumer_key, twitter_key.consumer_secret)
    auth.set_access_token(twitter_key.access_token, twitter_key.access_token_secret)
    api = tweepy.API(auth)
    return api

def get_user_timeline_tweets(num_tweets, screen_name, myclient):

    mydb = myclient["reply"]
    db_reply = mydb["reply"]

    mydb = myclient["tweeted"]
    db_tweeted = mydb["tweeted"]

    mydb = myclient["retweeted"]
    db_retweeted = mydb["retweeted"]

    count = 0
    for tweet in tweepy.Cursor(authenticate_twitter_app().user_timeline, id=screen_name).items(num_tweets):
        tweets = tweet._json
        if(tweet.in_reply_to_status_id != None):
            db_reply.insert_one(tweets)
           
        elif(tweet.text.startswith("RT @") == True):
            db_retweeted.insert_one(tweets)
            
        else:
            db_tweeted.insert_one(tweets)
           
        print(count)
        count += 1

    print("timeline complete")

    return tweets    

def get_friend_list(number_friends, screen_name, myclient):

    count = 0
    mydb = myclient["friend_list"]
    db_friend_list = mydb["friend_list"]
    friend_list = []

    for friend in tweepy.Cursor(authenticate_twitter_app().friends, id=screen_name).items(number_friends):
        friend_list.append(friend)
        print(count)
        count += 1
        
    db_friend_list.insert_one(friend_list)

    print("friend_list complete")

    return friend_list

def get_profile_user(screen_name, myclient):

    mydb = myclient["profile_user"]
    db_profile_user = mydb["profile_user"]
    profile_user = authenticate_twitter_app().get_user(screen_name)
    db_profile_user.insert_one(profile_user._json)
    
    print("profile:" + screen_name + " complete")

    return profile_user
    
if __name__=="__main__":

    screen_name = ['@EmmaWatson', '@ArianaGrande', '@realDonaldTrump', '@gamthestar', '@johnwinyu', '@justinbieber',
                   '@chocoopal', '@thePompam', '@StampApiwat', '@AjarnAdam']
    
    for name in tqdm(screen_name):

        myclient = pymongo.MongoClient("mongodb://<user>:<password>@<mongodb>:<port>/")

        profile_user = get_profile_user(name, myclient)

        print("screen_name: " + name)
        print(profile_user.statuses_count)

        data_tweet = get_user_timeline_tweets(profile_user.statuses_count, name, myclient)
