# CIS419_ViralTweetGenerator
Generates Viral and NonViral Political Tweets, Republican or Democrat. GPT-2 text generator, RoBERTa evaluation model, Twitter API

## Data Preprocessing Folder:
DataFetch.py uses the Twitter API to fetch raw tweets in batches, which is stored in the Tweets folder.
DataMerge.py takes the raw tweets, cleans them up (see Methods), generates virality scores, and puts them into Tweets.csv

## Text Generation Folder:
The notebook gpt2_fine_tune_tweet_gen.ipynb contains the necessary code to
fine-tune a pre-trained GPT-2 model on a collection of text inputs.
The notebook creates datasets for the 4 GPT-2 models for our data, one for each
combination of Republican/Democrat and Viral/Non-viral. The notebook is
designed to run in a Google Colab environment, and the supplement files
in the folder run_clm.py and run_generation.py (taken from the Hugging-Face
Transformers library) need to be uploaded to the runtime in order
to train the models and generate text.

Tweets.csv has all of the final data to train on.
