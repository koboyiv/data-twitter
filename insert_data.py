import pymongo
import json
import pprint
from tqdm import tqdm


#list twitter name
screen_name = ['EmmaWatson', 'ArianaGrande', 'realDonaldTrump', 'gamthestar', 'johnwinyu', 'justinbieber',
                   'chocoopal', 'thePompam', 'StampApiwat', 'AjarnAdam']


#connect to mongodb cloud
myclient = pymongo.MongoClient("mongodb://<username>:<password>@mongodb:<port>/")

mydb = myclient['profile_user']
profile = mydb['profile_user']

dict = []

for name in tqdm(screen_name):

    data = profile.find_one(({'screen_name':name}))
    dict.append([{
    'screen_name': data['screen_name'],
    'favourites_count': data['favourites_count'],
    'followers_count': data['followers_count'],
    'friends_count': data['friends_count'],
    'statuses_count': data['statuses_count'],
    'retweet_count': data['status']['retweet_count']
    }])

#insert to mongodb
mydb = myclient['twitter']
profile = mydb['twitter']
profile.insert_one(dict._json)






