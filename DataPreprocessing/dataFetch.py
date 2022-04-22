import tweepy
import time
import pandas as pd

'''
User Fields:
- Screen Name
- User ID
- Account Creation Date (created_at)
- isVerified (verified)
- Follower Count (public_metrics.followers_count)
- Following Count (public_metrics.following_count)
- Tweet Count (includes retweets) (public_metrics.tweet_count)

Tweet Fields: Should have max 800 tweets per user, excluding replies and retweets

- Author Screen Name
- Author ID (author_id)
- Tweet ID
- text
- Creation Date (created_at)
- in_reply_to_user_id (will be null if not a reply)
- Retweet Count - DOES NOT INCLUDE QUOTES (public_metrics_retweet_count)
- Reply Count (public_metrics_reply_count)
- Like Count (public_metrics_like_count)
- Quote Count - # times retweeted w comment (public_metrics_quote_count)
- Language (lang)
- Possibly Sensitive - is tweet for mature audiences (possibly_sensitive)
- Source - which platform the user tweeted from (source)
- 1st url start index (inclusive) (entities.urls[0].start
- 1st url end index (exclusive) (entities.urls[0].end
- 1st url url (entities.urls[0].url)
- 2nd url start index (inclusive) (entities.urls[1].start
- 2nd url end index (exclusive) (entities.urls[1].end
- 2nd url url (entities.urls[1].url)
'''
consumer_key = "B1K6ZA3LD789sVp68wEsCut5P" #API Key
consumer_secret = "qBC1xJEYEpfqQY4zocfn6WlLImcJ1lwrwED54PaQT9z5ao7RzC" #API Key Secret
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKoyagEAAAAANfy9s%2BN5NN%2B45sP4NP8oNQnySu0%3DU5GxXYB0E1C1QGaWMh1DzaUPBJeXZdhIDmcJrIPXKZwyAqgJEY"

client = tweepy.Client(bearer_token = bearer_token)

democrats = ['HillaryClinton','BarackObama','BernieSanders','AOC','KamalaHarris','JoeBiden','SenSchumer','SpeakerPelosi','EWarren',
'PeteButtigieg','RepAdamSchiff','CoryBooker','GavinNewsom','AmyKlobuchar','SenSherrodBrown','ChrisMurphyCT','RBReich','SenGillibrand',
'SenDuckworth','RepMaxineWaters']

republicans = ['MarcoRubio','SenTedCruz','Jim_Jordan','GOPLeader','LindseyGrahamSC','GovRonDeSantis','HawleyMO','MarshaBlackburn','SenTomCotton',
'SenJohnKennedy','ChuckGrassley','RandPaul','SenRickScott','SenMikeLee','SenJoniErnst','LeaderMcConnell','RepMattGaetz','JohnCornyn',
'DonaldJTrumpJr','SenatorRomney']

politicians = democrats + republicans

run_accounts = False
run_tweets = True

if run_accounts: 
  account_info = []
  for i in range(len(politicians)):
    print(i)
    screen_name = politicians[i]
    if i < 20:
      party = 'democrat'
    else:
      party = 'republican'
    my_profile = client.get_user(username=screen_name, user_fields=['created_at','id','verified','public_metrics'])
    authorID = str(my_profile.data.id)
    createdAt = str(my_profile.data.created_at)
    isVerified = str(my_profile.data.verified)
    followerCount = str(my_profile.data.public_metrics['followers_count'])
    followingCount = str(my_profile.data.public_metrics['following_count'])
    tweetCount = str(my_profile.data.public_metrics['tweet_count'])
    info = [screen_name, authorID, createdAt, isVerified, followerCount, followingCount, tweetCount, party]
    account_info.append(info)
  account_info = pd.DataFrame(account_info, columns = ['ScreenName','AuthorID','AccountCreationDate','isVerified','FollowerCount','FollowingCount','TweetCount','Party'])
  account_info.to_csv('Data/account_info.csv',index=False)

if run_tweets:
  for i in range(0,40):
    print('Started '+str(politicians[i]))
    screen_name = politicians[i]
    user = client.get_user(username=screen_name)
    author_id = str(user.data.id)

    prev_tweet_id = None
    for batch_i in range(8):
      print('Started batch '+str(batch_i))
      if prev_tweet_id == None:
        tweets = client.get_users_tweets(id=author_id,max_results = 100, exclude=['retweets','replies'],tweet_fields=['created_at','author_id','in_reply_to_user_id','public_metrics','lang','possibly_sensitive','source','text','entities']).data
      else:
        tweets = client.get_users_tweets(id=author_id,max_results = 100, until_id = prev_tweet_id, exclude=['retweets','replies'],tweet_fields=['created_at','author_id','in_reply_to_user_id','public_metrics','lang','possibly_sensitive','source','text','entities']).data
      tweet_info = []
      if tweets != None:
        for tweet in tweets:
          author_name = str(screen_name)
          author_id = str(tweet.author_id)
          tweet_id = str(tweet.id)
          text = str(tweet.text)
          tweetDate = str(tweet.created_at)
          isReply = str(tweet.in_reply_to_user_id != None)
          retweetCount = str(tweet.public_metrics['retweet_count'])
          replyCount = str(tweet.public_metrics['reply_count'])
          likeCount = str(tweet.public_metrics['like_count'])
          quoteCount = str(tweet.public_metrics['quote_count'])
          language = str(tweet.lang)
          possSens = str(tweet.possibly_sensitive)
          source = str(tweet.source)
          if tweet.entities != None and 'urls' in tweet.entities:
            if len(tweet.entities['urls']) >= 1:
              firstURLStart = str(tweet.entities['urls'][0]['start'])
              firstURLEnd = str(tweet.entities['urls'][0]['end'])
              firstURL = str(tweet.entities['urls'][0]['url'])
              firstURLExp = str(tweet.entities['urls'][0]['expanded_url'])
            else:
              firstURLStart = 'NA'
              firstURLEnd = 'NA'
              firstURL = 'NA'
              firstURLExp = 'NA'
            if len(tweet.entities['urls']) >= 2:
              secondURLStart = str(tweet.entities['urls'][1]['start'])
              secondURLEnd = str(tweet.entities['urls'][1]['end'])
              secondURL = str(tweet.entities['urls'][1]['url'])
              secondURLExp = str(tweet.entities['urls'][1]['expanded_url'])
            else:
              secondURLStart = 'NA'
              secondURLEnd = 'NA'
              secondURL = 'NA'
              secondURLExp = 'NA'
            if len(tweet.entities['urls']) >= 3:
              thirdURLStart = str(tweet.entities['urls'][1]['start'])
              thirdURLEnd = str(tweet.entities['urls'][1]['end'])
              thirdURL = str(tweet.entities['urls'][1]['url'])
              thirdURLExp = str(tweet.entities['urls'][1]['expanded_url'])
            else:
              thirdURLStart = 'NA'
              thirdURLEnd = 'NA'
              thirdURL = 'NA'
              thirdURLExp = 'NA'
          else:
            firstURLStart = 'NA'
            firstURLEnd = 'NA'
            firstURL = 'NA'
            firstURLExp = 'NA'
            secondURLStart = 'NA'
            secondURLEnd = 'NA'
            secondURL = 'NA'
            secondURLExp = 'NA'
            thirdURLStart = 'NA'
            thirdURLEnd = 'NA'
            thirdURL = 'NA'
            thirdURLExp = 'NA'
          row = [author_name,author_id,tweet_id,text,tweetDate,isReply,retweetCount,replyCount,likeCount,quoteCount,language,possSens,source,
                firstURLStart,firstURLEnd,firstURL,firstURLExp,secondURLStart,secondURLEnd,secondURL,secondURLExp,
                thirdURLStart,thirdURLEnd,thirdURL,thirdURLExp]
          tweet_info.append(row)
        tweet_info = pd.DataFrame(tweet_info, columns=['ScreenName','AuthorID','TweetID','Text','TweetDate','isReply','RetweetCount','ReplyCount','LikeCount','QuoteCount',
                                                    'Language','PossibleSensitive','Source','1stURLStart','1stURLEnd','1stURL','1stURLExp',
                                                    '2ndURLStart','2ndURLEnd','2ndURL','2ndURLExp','3rdURLStart','3rdURLEnd','3rdURL','3rdURLExp'])
        tweet_info.to_csv('Data/Tweets/'+str(i)+'_batch'+str(batch_i)+'_'+str(screen_name)+'.csv',index=False)
        prev_tweet_id = tweet_id
    print()


