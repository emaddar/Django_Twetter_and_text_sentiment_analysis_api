import snscrape.modules.twitter as sntwitter                            # For scrapping twitter
import pandas as pd
import streamlit as st
#########################################################################################################
###                                                                                                                           ###
###                                                   Twitter analysis                                                        ###
###                                                                                                                           ###
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################


###____________________________Scrapping____________________________###
query = st.text_input()
# query = "Emad"
limit = st.number_input()

tweets = []
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.username, tweet.content, tweet.likeCount, tweet.replyCount, tweet.retweetCount, tweet.url])
df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'Like', 'Replay', 'Retweet', 'Url'])

st.dataframe(df)