
from email.mime import image
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
import json
import requests
import random


from django.http import HttpResponseRedirect   # For signUp page
from .forms import SignUp                       # For signUp page

###__________________Scrape des tweets__________________###
# 127.0.0.1/form
def signup(request):
    # if request.method == ('POST'):
    #     form = SignUp(request.POST)

    #     if form.is_valid():
    #         return HttpResponseRedirect('/')
    #     else:
    #         return HttpResponseRedirect("non") # render(...) whatever you wanted if form validation fails
         
      
    # else:
    #     form = SignUp()
        return render(request, 'signup.html', {'signupForm' : SignUp})


###__________________about page__________________###
def about(request):
    return render(request, 'about.html')
###__________________Scrape des tweets__________________###

def tweet(request):
    return render(request, 'index.html')


def join_with(mylist, operator):
    return f' {operator} '.join(mylist)


def get_tweets(query, limit):
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            tweets.append([tweet.date, tweet.username, tweet.content, tweet.likeCount, tweet.replyCount, tweet.retweetCount, tweet.url])

    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'Like', 'Replay', 'Retweet', 'Url'])
    return df


###__________________Nettoyage du texte__________________###
#Supression brouillard du texte
def df_only_text(df):
    tweet_text = " ".join(list(df['Tweet']))
    tweet_text = re.sub(r'http\S+', '', tweet_text)
    tweet_text = re.sub(r'@\S+', '', tweet_text)
    tweet_text = re.sub(r'#\S+', '', tweet_text)
    tweet_text = re.sub('\n+', '', tweet_text)
    return tweet_text

#Création d'un texte unique pour l'analyse
def getQuery(searsh_query):
    query = searsh_query[0] + " lang:" + searsh_query[13] + " " 
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

###__________________World cloud__________________###

#Couleur des mots du nuage
def couleur_red(*args, **kwargs):
    return "rgb(255, 0, {})".format(random.randint(0, 170))

def couleur_blue(*args, **kwargs):
    return "rgb({}, 0, 255)".format(random.randint(0, 170))



#Fonction pour générer le nuage de mots
def get_word_cloud(text_only, lang, status):
    stop_words = get_stop_words(lang) #Nettoyage des appax, possible d'en ajouter à la
    if lang == "fr":
        ma_list_fr = ["bcp", "Bcp", "trkl", "c'est", "est","s'en","j'ai","etc", "ça", "n'a","n'as","ca","va", "après", "qu'","c","C","lors","s","S","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","qu'il","qu'elle","vs","bcp","mdr", "d'un", "d'une", "s'il", "s'ils", "ya", "n'est"]
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
    wordcloud = WordCloud(background_color = 'white', stopwords = stop_words, max_words = 75, mask=mask).generate(text_only)
    if status == "Positive" or status == "Neutral":
        fig = plt.figure(figsize=(20,16) , dpi=200) 
        plt.imshow(wordcloud.recolor(color_func = couleur_blue))
        plt.axis("off")
        fig.tight_layout(pad=0, w_pad=0, h_pad=0)
        fig.savefig('./base/static/base/images/mypic.png') 
    else : 
        fig = plt.figure(figsize=(20,16) , dpi=200) 
        plt.imshow(wordcloud.recolor(color_func = couleur_red))
        plt.axis("off")
        fig.tight_layout(pad=0, w_pad=0, h_pad=0)
        fig.savefig('./base/static/base/images/mypic.png')        


###__________________Envoyer les résultats vers le template du site__________________###

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
    df = df.sort_values(['Like', 'Retweet','Replay'],ascending=False)



    text_only = df_only_text(df)
    


###__________________Appel de l'API analyse de sentiments__________________###
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYjI3ODQwYjUtY2IxOC00MGFmLWE5NmEtYWMzNzNjMzAxMDBmIiwidHlwZSI6ImFwaV90b2tlbiJ9.sJnkDP04P0fnK0Bd_ayFkEpFMM0gM9GdM8MR9LwsLG0"}
    lang = "fr"
    url ="https://api.edenai.run/v2/text/sentiment_analysis"
    payload={"providers": "amazon", 'language': lang, 'text': text_only}


    All_text = text_only
    
    # response = requests.post(url, json=payload, headers=headers)
    # result = json.loads(response.text)
    # n = len(text_only)
    # if n >= 4000:
    #     text_only = text_only[:4000]

#     if result['amazon']['status'] == 'fail':
#         for i in range(20):
#             n -= 1000
#             text_only = text_only[:n]
#             payload={"providers": "amazon", 'language': lang, 'text': text_only}
#             response = requests.post(url, json=payload, headers=headers)
#             result = json.loads(response.text)
#             if result['amazon']['status'] != 'fail':
#                 break
#     x = result['amazon']['items']

# #Création dataframe du résultat de l'API
#     api_dico = {}
#     for i in range(len(x)):
#         api_dico[x[i]['sentiment']] = round(x[i]['sentiment_rate'],4)*100

#     api_df = pd.DataFrame(list(api_dico.items()), columns=['sentiment', 'sentiment_rate'])

# ###__________________Mise en forme du graphique de l'analyse sentimentale__________________###
#     labels = api_df['sentiment'].tolist()
#     data = api_df['sentiment_rate'].tolist()


#     #Supression sentiment Mixed
#     labels.remove('Mixed')
#     del data[-1]

    data = [60, 30, 10]
    labels = ["Positive", "Negative", "Neutral"]


    max_data = max(data)
    max_data_index = data.index(max(data))
    max_labels = labels[max_data_index]
#Envoi du résultat sur le site
    if text_only != "":
        get_word_cloud(All_text, lang, max_labels)

            #####################################################################
            #                       Get  3 Tweets most liked                    #
            #####################################################################
        if len(df)>=3:
            tweet_1_date = df.iloc[0]['Date']
            tweet_2_date = df.iloc[1]['Date']
            tweet_3_date = df.iloc[2]['Date']

            tweet_1_User = df.iloc[0]['User']
            tweet_2_User = df.iloc[1]['User']
            tweet_3_User = df.iloc[2]['User']


            tweet_1_Tweet = df.iloc[0]['Tweet']
            tweet_2_Tweet = df.iloc[1]['Tweet']
            tweet_3_Tweet = df.iloc[2]['Tweet']  

            tweet_1_Like = df.iloc[0]['Like']
            tweet_2_Like = df.iloc[1]['Like']
            tweet_3_Like = df.iloc[2]['Like']    

            tweet_1_Replay = df.iloc[0]['Replay']
            tweet_2_Replay = df.iloc[1]['Replay']
            tweet_3_Replay = df.iloc[2]['Replay'] 

            tweet_1_Retweet = df.iloc[0]['Retweet']
            tweet_2_Retweet = df.iloc[1]['Retweet']
            tweet_3_Retweet = df.iloc[2]['Retweet']    

            tweet_1_Url = df.iloc[0]['Url']
            tweet_2_Url = df.iloc[1]['Url']
            tweet_3_Url = df.iloc[2]['Url']    
        else : 
            return render(request, 'result_with_no_text.html', {'query': query})

   
        return render(request, 'result.html', {'query': query,
                                         'df' : df[:3].to_html(),
                                         'text_only' : text_only,
                                        #  'api_df' : api_df.to_html,
                                         'n':len(text_only),
                                         'labels':labels,
                                         'data':data,
                                         'max_data':round(max_data,2),
                                         'max_labels':max_labels,
                                         'tweet_1_date':tweet_1_date,
                                         'tweet_2_date':tweet_2_date,
                                         'tweet_3_date':tweet_3_date,
                                         "tweet_1_User":tweet_1_User,
                                         "tweet_2_User":tweet_2_User,
                                         "tweet_3_User":tweet_3_User,
                                         "tweet_1_Tweet":tweet_1_Tweet,
                                         "tweet_2_Tweet":tweet_2_Tweet,
                                         "tweet_3_Tweet":tweet_3_Tweet,
                                         "tweet_1_Like":tweet_1_Like,
                                         "tweet_2_Like":tweet_2_Like,
                                         "tweet_3_Like":tweet_3_Like,
                                         "tweet_1_Replay":tweet_1_Replay,
                                         "tweet_2_Replay":tweet_2_Replay,
                                         "tweet_3_Replay":tweet_3_Replay,
                                         "tweet_1_Retweet":tweet_1_Retweet,
                                         "tweet_2_Retweet":tweet_2_Retweet,
                                         "tweet_3_Retweet":tweet_3_Retweet,
                                         "tweet_1_Url" : tweet_1_Url,
                                         "tweet_2_Url" : tweet_2_Url,
                                         "tweet_3_Url" : tweet_3_Url,
                                         }
                                        )
    else :
        return render(request, 'result_with_no_text.html', {'query': query}
                                        )


def home(request):
    return render(request, 'home.html')
