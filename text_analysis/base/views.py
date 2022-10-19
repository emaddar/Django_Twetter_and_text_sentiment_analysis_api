# https://www.youtube.com/watch?v=a1j8g01ics4
from django.shortcuts import render
import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
from stop_words import get_stop_words
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image


def home(request):
    return render(request, 'index.html')


def join_with(mylist, operator):
    return f' {operator} '.join(mylist)


def get_tweets(query, limit):
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            tweets.append([tweet.date, tweet.username, tweet.content, tweet.likeCount, tweet.replyCount, tweet.retweetCount])

    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'Like', 'Replay', 'Retweet'])
    return df

def df_only_text(df):
    tweet_text = " ".join(list(df['Tweet']))
    tweet_text = re.sub(r'http\S+', '', tweet_text)
    tweet_text = re.sub(r'@\S+', '', tweet_text)
    tweet_text = re.sub(r'#\S+', '', tweet_text)
    return tweet_text


def couleur_blue(*args, **kwargs):
    import random
    return "rgb({}, 0, 255)".format(random.randint(0, 170))
    
def get_word_cloud(text_only, lang):
    stop_words = get_stop_words(lang) #pour nettoyer des appax, on peut en ajouter à la liste
    if lang == "fr":
        ma_list_fr = ["c'est", "est","j'ai","ça", "ca","va", "après", "qu'","c","C","lors","s","S","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        for mot in ma_list_fr:
             if mot not in stop_words:
                 stop_words.append(mot)
    elif lang == "en":
        ma_list_en = ["day","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        for mot in ma_list_en:
             if mot not in stop_words:
                 stop_words.append(mot)
    mask = np.array(Image.open("../ressources/mask_bird.jpg"))
    mask[mask == 1] = 255
    wordcloud = WordCloud(background_color = 'white', stopwords = stop_words, max_words = 100, mask=mask).generate(text_only)


    fig = plt.figure(figsize=(8, 18), dpi=200) 
    plt.imshow(wordcloud.recolor(color_func = couleur_blue))
    plt.axis("off")
    fig.savefig('./base/static/base/images/mypic.png') 

def getQuery(searsh_query):
    query = searsh_query[0] + " lang:" + searsh_query[13] + " " #  + searsh_query[1] + " "
    if searsh_query[2] != "":
        query += '"' + searsh_query[2] + '"' + " "
    if searsh_query[4] != "":
        query +=  ' '.join(['-'+i for i in searsh_query[4].split()]) + " "
    if searsh_query[3] != "":
        query += '(' + join_with(searsh_query[3].split(), 'OR') + ')'  + " "
    if searsh_query[5] != "":
        query += '(' + join_with(searsh_query[5].split(), 'OR') + ')'  + " "
    if searsh_query[6] != "":
        query += '(from:' + join_with(searsh_query[6].split(), 'OR from:') + ')'  + " "
    if searsh_query[7] != "":
        query += '(to:' + join_with(searsh_query[7].split(), 'OR to:') + ')'  + " "
    if searsh_query[8] != "" :
        query += 'min_replies:' + searsh_query[8] + " "
    if searsh_query[9] != "" :
        query += 'min_faves:' + searsh_query[9] + " "
    if searsh_query[10] != "" :
        query += 'min_retweets:' + searsh_query[10] + " "
    if searsh_query[11] != "" :
        query += 'since:' + searsh_query[11] + " "
    if searsh_query[12] != "" :
        query += 'until:' + searsh_query[12] + " "

    return query

def result(request):
    all_words = request.GET['all_words']                       #0
    limit = request.GET['limit']                               #1
    exact_phrase = request.GET['exact_phrase']                 #2
    Any_of_these_words = request.GET['Any_of_these_words']     #3
    None_of_these_words = request.GET['None_of_these_words']   #4
    These_hastags = request.GET['These_hastags']               #5
    From_acounts = request.GET['From_acounts']                 #6
    To_acounts = request.GET['To_acounts']                     #7
    Minimun_replies = request.GET['Minimun_replies']           #8
    Minimum_likes = request.GET['Minimum_likes']               #9
    Minimum_retweets = request.GET['Minimum_retweets']         #10
    from_date = request.GET['from_date']                       #11
    to_date = request.GET['to_date']                           #12
    lang = request.GET['lang']                                 #13
    
    query = getQuery(searsh_query = [all_words, limit, exact_phrase, Any_of_these_words, None_of_these_words,
                                            These_hastags, From_acounts, To_acounts, Minimun_replies, Minimum_likes,
                                            Minimum_retweets, from_date, to_date, lang])
    df = get_tweets(query, int(limit))

    text_only = df_only_text(df) #avoir seulement le texte

    if text_only != "":
        get_word_cloud(text_only, lang)
   
        return render(request, 'result.html', {'query': query,
                                         'df' : df.to_html(),
                                         'text_only' : text_only}
                                        )
    else :
        return render(request, 'result_with_no_text.html', {'query': query}
                                        )