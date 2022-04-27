# CIS419_ViralTweetGenerator
Generates Viral and NonViral Political Tweets, Republican or Democrat. GPT-2 text generator, RoBERTa evaluation model, Twitter API

## DataPreprocessing
DataFetch.py uses the Twitter API to fetch raw tweets in batches, which is stored in the Tweets folder.
DataMerge.py takes the raw tweets, cleans them up (see Methods), generates virality scores, and puts them into Tweets.csv

Tweets.csv has all of the final data to train on.

## RoBERTa
The code in this notebook is set up to be run on a SageMaker notebook instance. Our instance is of type ml.g4dn.xlarge and 15GB volume. 

tune_roberta.ipynb contains the script to utilize HuggingFace's existing RoBERTa model in order to:
1. Finetune RoBERTa to train a model to predict virality scores of input Tweets
2. Use our [trained model](https://drive.google.com/file/d/1BkpLYFRZUJg7iKMiW6LngT-VuN4-CXNY/view?usp=sharing) to predict virality scores of our generated Tweets
3. Finetune RoBERTa to train a model to classify political party affiliation of input Tweets
4. Use our [trained model](https://drive.google.com/file/d/1BkpLYFRZUJg7iKMiW6LngT-VuN4-CXNY/view?usp=sharing) to predict party affiliations of our generated Tweets

data contains a copies of the preprocessed Tweets contained in DataPreprocessing and the generated Tweets output by our trained GPT-2 models.
