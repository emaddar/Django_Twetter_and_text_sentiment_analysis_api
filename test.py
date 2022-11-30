# import snscrape.modules.twitter as sntwitter                            # For scrapping twitter
# import pandas as pd
# import streamlit as st
# #########################################################################################################
# ###                                                                                                                           ###
# ###                                                   Twitter analysis                                                        ###
# ###                                                                                                                           ###
# #################################################################################################################################
# #################################################################################################################################
# #################################################################################################################################

import pandas as pd
import streamlit as st
import snscrape.modules.twitter as sntwitter                            # For scrapping twitter
import re
import requests
import json

###____________________________Scrapping____________________________###
query = st.text_input(label = "query")
# query = "Emad"
limit = st.number_input(label = "limit",  min_value=1, max_value=100, value=5, step=1)

tweets = []
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.username, tweet.content, tweet.likeCount, tweet.replyCount, tweet.retweetCount, tweet.url])
df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'Like', 'Replay', 'Retweet', 'Url'])

st.dataframe(df)
df = df.sort_values(['Like', 'Retweet','Replay'],ascending=False)



# Removal the text fog
def clean_text(x):
    x = re.sub(r'http\S+', '', x)                   # Remove URL
    x = re.sub(r'@\S+', '', x)                      # Remove mentions
    x = re.sub(r'#\S+', '', x)                      # Remove Hashtags
    x = re.sub('\n+', '', x)
    x = re.sub("\'\w+", '', x)                      # Remove ticks and the next character
    x = re.sub(r'\w*\d+\w*', '', x)                 # Remove numbers
    x = re.sub('\s{2,}', " ", x)                    # Replace the over spaces
    x = x.replace('()', '')                         # Remove ()
    x = x.replace('>>>','')
    x = x.replace('#', '')
    return x

# Removal the text fog
def clean_text(x):
    x = re.sub(r'http\S+', '', x)                   # Remove URL
    x = re.sub(r'@\S+', '', x)                      # Remove mentions
    x = re.sub(r'#\S+', '', x)                      # Remove Hashtags
    x = re.sub('\n+', '', x)
    x = re.sub("\'\w+", '', x)                      # Remove ticks and the next character
    x = re.sub(r'\w*\d+\w*', '', x)                 # Remove numbers
    x = re.sub('\s{2,}', " ", x)                    # Replace the over spaces
    x = x.replace('()', '')                         # Remove ()
    x = x.replace('>>>','')
    x = x.replace('#', '')
    return x

x = " ".join(list(df['Tweet']))
text_only = clean_text(x)

headers = {"Authorization": "Bearer "+'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYjI3ODQwYjUtY2IxOC00MGFmLWE5NmEtYWMzNzNjMzAxMDBmIiwidHlwZSI6ImFwaV90b2tlbiJ9.sJnkDP04P0fnK0Bd_ayFkEpFMM0gM9GdM8MR9LwsLG0'}
lang = "fr"
url ="https://api.edenai.run/v2/text/sentiment_analysis"

n = len(text_only)
if n >= 4000:
    text_only = text_only[:4000]
    n = len(text_only)

API_status = 1
payload={"providers": "google", 'language': lang, 'text': text_only}
response = requests.post(url, json=payload, headers=headers)
result = json.loads(response.text)
result_list = result['google']['items']
labels = []
data = []
for i in range(len(result_list)):
    labels.append(result_list[i]['sentiment'])
    data.append(result_list[i]['sentiment_rate'])

d = {'labels':labels,'data':data}
d = pd.DataFrame(d)
d = d.groupby('labels').mean()
d = d.reset_index()
d = dict(zip(d.labels, d.data))


labels = ["Positive", "Negative", "Neutral"]
data = [d[labels[0]], d[labels[1]], d[labels[2]]]
