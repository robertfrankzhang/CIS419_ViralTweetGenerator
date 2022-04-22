# CIS419_ViralTweetGenerator
Generates Viral and NonViral Political Tweets, Republican or Democrat. GPT-2 text generator, RoBERTa evaluation model, Twitter API

## Data Preprocessing Folder:
DataFetch.py uses the Twitter API to fetch raw tweets in batches, which is stored in the Tweets folder.
DataMerge.py takes the raw tweets, cleans them up (see Methods), generates virality scores, and puts them into Tweets.csv

Tweets.csv has all of the final data to train on.
