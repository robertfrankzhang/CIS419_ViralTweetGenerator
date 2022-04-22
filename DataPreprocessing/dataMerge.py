import pandas as pd
import os
import numpy as np
from unidecode import unidecode

# Merge all tweet data
merged_data = None
counter = 0
for filename in os.listdir('Data/Tweets'):
  f = os.path.join('Data/Tweets',filename)
  data = pd.read_csv(f)
  data['RetweetCountCalc'] = data['RetweetCount'] + data['QuoteCount']
  subdata = data[['ScreenName','TweetID','Text','TweetDate','RetweetCountCalc','LikeCount','1stURL','2ndURL','3rdURL']]
  subdata = subdata.rename(columns={'RetweetCountCalc':'RetweetCount'})
  if counter == 0:
    merged_data = subdata
  else:
    merged_data = pd.concat([merged_data,subdata])
  counter += 1

account_data = pd.read_csv('Data/account_info.csv')
account_data = account_data[['ScreenName','Party']]
party_map = dict(zip(account_data['ScreenName'],account_data['Party']))

# Merge in follower following data
follow_data = pd.read_csv('Data/FolloweringOverTime.csv')
follow_data = follow_data.set_index('Account')
follow_dict = follow_data.to_dict('index')

party_col = []
followers_col = []
following_col = []
for index, row in merged_data.iterrows():
  party_col.append(party_map[row['ScreenName']])

  dates = row['TweetDate'].split(' ')[0].split('-')
  month = int(dates[1])
  year = int(dates[0][-2:])
  if month <= 3:
    block_year = year
    block_month = 1
  elif month >= 10:
    block_year = year + 1
    block_month = 1
  else:
    block_year = year
    block_month = 7
  timeline_range = str(block_month)+'/'+str(block_year)
  follower_count = follow_dict[row['ScreenName']]['Followers '+timeline_range]
  if follower_count == 0:
    print('ERROR Follower')
    print(row['ScreenName'])
    print(row['TweetDate'])
    print()
    followers_col.append(0)
  else:
    followers_col.append(follower_count)
  
  following_count = follow_dict[row['ScreenName']]['Following '+timeline_range]
  if following_count == 0:
    print('ERROR Following')
    print(row['ScreenName'])
    print(row['TweetDate'])
    print()
    following_col.append(0)
  else:
    following_col.append(following_count)

merged_data['Party'] = party_col
merged_data['FollowerCount'] = followers_col
merged_data['FollowingCount'] = following_col

# Checks to make sure length stays the same - it does!
print(len(merged_data))
merged_data = merged_data.drop_duplicates(subset=['TweetID'])
print(len(merged_data)) 

# Tweet Preprocessing Fix unicode-8 symbols, Remove all formatting errors: doubled spaces, new lines, spaces at the end or beginning of tweet
formatted_tweets = []
for index, row in merged_data.iterrows():
  raw_tweet = row['Text']
  
  # Remove new lines
  raw_tweet = raw_tweet.replace('\t','')
  raw_tweet = raw_tweet.replace('\n',' ') #Add space
  raw_tweet = raw_tweet.replace('\r','')

  # Remove URLS
  if row['1stURL'] != 'NA':
    raw_tweet = raw_tweet.replace(str(row['1stURL']),'')
  if row['2ndURL'] != 'NA':
    raw_tweet = raw_tweet.replace(str(row['2ndURL']),'')
  if row['3rdURL'] != 'NA':
    raw_tweet = raw_tweet.replace(str(row['3rdURL']),'')
  
  # Replace non-ascii with ascii
  raw_tweet = raw_tweet.replace('`','\'')
  raw_tweet = raw_tweet.replace('’','\'')
  raw_tweet = raw_tweet.replace('‘','\'')
  raw_tweet = raw_tweet.replace('“','\'')
  raw_tweet = raw_tweet.replace('”','\'')
  raw_tweet = raw_tweet.replace('–',', ')
  raw_tweet = raw_tweet.replace('—',', ')
  raw_tweet = raw_tweet.replace('&amp;',' and ')
  raw_tweet = raw_tweet.replace('&',' and ')
  raw_tweet = unidecode(raw_tweet)

  # Fix other encodings by removing them
  raw_tweet = raw_tweet.encode('ascii', 'ignore').decode('ascii')

  # Remove doubled spaces
  while "  " in raw_tweet:
    raw_tweet = raw_tweet.replace("  "," ")
  
  # Remove spaces and weird punctuation at beginning/end
  raw_tweet = raw_tweet.strip()
  raw_tweet = raw_tweet.lstrip('.')

  formatted_tweets.append(raw_tweet)
merged_data['Text'] = formatted_tweets

# Drop tweets <5 words, tweets <10 words that end in ":"
merged_data = merged_data[merged_data['Text'].str.split().str.len().gt(4)]
print(len(merged_data))
merged_data = merged_data[merged_data['Text'].str.split().str.len().gt(9) | ~merged_data['Text'].str.endswith(':')]
print(len(merged_data))

# Add Ground Truth Virality Scores
virality_scores = []
simple_v_scores = []
user_v_scores = {}
user_simple_v_scores = {}
for index, row in merged_data.iterrows():
  w = row['FollowerCount']
  d = max(row['FollowingCount'],1)
  r = max(row['RetweetCount'],1)
  f = row['LikeCount']
  
  g = r + f
  h = w - d
  A = 10
  inf_t = g + (g * f / r)/A
  inf_a = w + (h * w / d)/A
  inf_twt = inf_t/inf_a
  virality_scores.append(inf_twt)

  simple_v_score = g/max(h,1)
  simple_v_scores.append(simple_v_score)

  if not (row['ScreenName'] in user_v_scores):
    user_v_scores[row['ScreenName']] = [inf_twt]
    user_simple_v_scores[row['ScreenName']] = [simple_v_score]
  else:
    user_v_scores[row['ScreenName']].append(inf_twt)
    user_simple_v_scores[row['ScreenName']].append(simple_v_score)
  
merged_data['ViralityScore'] = virality_scores
merged_data['ViralityScoreSimple'] = simple_v_scores

median_user_v_scores = {}
median_user_simple_v_scores = {}
for name in account_data['ScreenName']:
  median_user_v_scores[name] = np.median(user_v_scores[name])
  median_user_simple_v_scores[name] = np.median(user_simple_v_scores[name])
median_virality_scores_normalized = []
median_simple_v_scores_normalized = []
for index, row in merged_data.iterrows():
  median_virality_scores_normalized.append(row['ViralityScore'] / median_user_v_scores[row['ScreenName']])
  median_simple_v_scores_normalized.append(row['ViralityScoreSimple'] / median_user_simple_v_scores[row['ScreenName']])

# Creation of 4 output variable options, take log of each s.t. median score is 0.
# Not sure if should use Simple or Standard score, total/user median as output variable. Decide based on which does best w/ predictor model
merged_data['ViralityScore_NormalizedByUserMedian'] = np.log(median_virality_scores_normalized)
merged_data['ViralityScoreSimple_NormalizedByUserMedian'] = np.log(median_simple_v_scores_normalized)
merged_data['ViralityScore_NormalizedByTotalMedian'] = np.log(merged_data['ViralityScore']/np.median(merged_data['ViralityScore']))
merged_data['ViralityScoreSimple_NormalizedByTotalMedian'] = np.log(merged_data['ViralityScoreSimple']/np.median(merged_data['ViralityScoreSimple']))

# (optional) Sort Data by best output metric (for visual inspection)
merged_data = merged_data.sort_values(by = ['ViralityScoreSimple_NormalizedByUserMedian'], ascending = False)

# Remove irrelevant columns
merged_data = merged_data[['ScreenName','Party','Text','ViralityScore_NormalizedByUserMedian','ViralityScoreSimple_NormalizedByUserMedian','ViralityScore_NormalizedByTotalMedian','ViralityScoreSimple_NormalizedByTotalMedian']]

# Export Merged, Proprocessed Data
merged_data.to_csv('Data/Tweets.csv',index=False)