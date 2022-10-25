
from cProfile import label
from email.mime import image
import imp
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
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect   # For signUp page
from .forms import SignUp                       # For signUp page


from django.contrib.auth.forms import UserCreationForm  # For signUp page Methode 2
from django.urls import reverse_lazy                    # For signUp page Methode 2
from django.views import generic                        # For signUp page Methode 2

import langid  #for language detect
import datetime 


###__________________Sign Up__________________###
# 127.0.0.1/form
def signup(request):
    return render(request, 'signup.html', {'signupForm' : SignUp})


###__________________about page__________________###
def about(request):
    return render(request, 'about.html')
###__________________Scrape des tweets__________________###

def tweet(request):
    return render(request, 'index.html')



#########################################################################
#                          language detector                            #
#########################################################################
def language_detector(text):
    return langid.classify(text)[0]



######__________________Scrapping__________________###
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
def clean_text(x):
    x = re.sub(r'http\S+', '', x)     # Remove URL
    x = re.sub(r'@\S+', '', x)        # Remove mentions
    x = re.sub(r'#\S+', '', x)        # Remove Hashtags
    x = re.sub('\n+', '', x)
    x = re.sub("\'\w+", '', x)                 # Remove ticks and the next character
    x = re.sub(r'\w*\d+\w*', '', x)     # Remove numbers
    x = re.sub('\s{2,}', " ", x)        # Replace the over spaces
    return x



def text_without_stop_words(text,stopwords):
    for i in (text.split()):
        if i in stopwords:
            text = text.replace(i, '')
    return text



#Création d'un texte unique pour l'analyse
def getQuery(searsh_query):
    query = searsh_query[0] + " lang:" + searsh_query[10] + " " 
    if searsh_query[2] != "":
        query += '"' + searsh_query[2] + '"' + " "
    if searsh_query[3] != "":
        query +=  ' '.join(['-'+i for i in searsh_query[3].split()]) + " "
    # if searsh_query[3] != "":
    #     query += '(' + join_with(searsh_query[3].split(), 'OR') + ')'  + " "
    if searsh_query[4] != "":
        query += '(' + join_with(searsh_query[4].split(), 'OR') + ')'  + " "
    if searsh_query[5] != "":
        query += '(from:' + join_with(searsh_query[5].split(), 'OR from:') + ')'  + " "
    if searsh_query[6] != "":
        query += '(to:' + join_with(searsh_query[6].split(), 'OR to:') + ')'  + " "
    # if searsh_query[7] != "" :
    #     query += 'min_replies:' + searsh_query[7] + " "
    if searsh_query[7] != "" :
        query += 'min_faves:' + searsh_query[7] + " "
    # if searsh_query[8] != "" :
    #     query += 'min_retweets:' + searsh_query[8] + " "
    if searsh_query[8] != "" :
        query += 'since:' + searsh_query[8] + " "
    if searsh_query[9] != "" :
        query += 'until:' + searsh_query[9] + " "

    return query

###__________________World cloud__________________###

#Couleur des mots du nuage
def couleur_red(*args, **kwargs):
    return "rgb(255, 0, {})".format(random.randint(0, 170))

def couleur_blue(*args, **kwargs):
    return "rgb({}, 0, 255)".format(random.randint(0, 170))



def our_get_stop_words(lang):
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
    return stop_words

#Fonction pour générer le nuage de mots
def get_word_cloud(stop_words, text_only, status):
    mask = np.array(Image.open("../ressources/mask_bird.jpg"))
    mask[mask == 1] = 255
    wordcloud = WordCloud(background_color = 'white', stopwords = stop_words, max_words = 75, mask=mask).generate(text_only)
    if status == "Positive" or status == "Neutral":
        fig = plt.figure(figsize=(30,30) , dpi=200) 
        plt.imshow(wordcloud.recolor(color_func = couleur_blue))
        plt.axis("off")
        fig.tight_layout(pad=0, w_pad=0, h_pad=0)
        fig.savefig('./base/static/base/images/mypic.png') 
    else : 
        fig = plt.figure(figsize=(30,30) , dpi=200) 
        plt.imshow(wordcloud.recolor(color_func = couleur_red))
        plt.axis("off")
        fig.tight_layout(pad=0, w_pad=0, h_pad=0)
        fig.savefig('./base/static/base/images/mypic.png')  

#########################################################################
#                          get from date to date ... k days ago         #
#########################################################################

def get_from_to_date_k_days_ago(df,k):
    df_date_sorted = df.sort_values(by='Date')
    df_date_sorted_time_type = df_date_sorted 
    
    from_date = df_date_sorted_time_type.iloc[0]['Date']
    to_date = df_date_sorted_time_type.iloc[-1]['Date']

    from_date_1_year_ago = (pd.to_datetime(from_date.strftime('%Y-%m-%d')) - timedelta(days=k)).strftime('%Y-%m-%d')
    to_date_1_year_ago = (pd.to_datetime(to_date.strftime('%Y-%m-%d')) - timedelta(days=k-1)).strftime('%Y-%m-%d')


    return (from_date_1_year_ago, to_date_1_year_ago)
      

#########################################################################
#                                                                       #
#                          get API function                             #
#                                                                       #
#########################################################################


def get_api(text_only_limited, lang):
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYjI3ODQwYjUtY2IxOC00MGFmLWE5NmEtYWMzNzNjMzAxMDBmIiwidHlwZSI6ImFwaV90b2tlbiJ9.sJnkDP04P0fnK0Bd_ayFkEpFMM0gM9GdM8MR9LwsLG0"}
    lang = "fr"
    url ="https://api.edenai.run/v2/text/sentiment_analysis"

    n = len(text_only_limited)
    if n >= 4000:
        text_only_limited = text_only_limited[:4000]
        n = len(text_only_limited)

    API_status = 1
    payload={"providers": "amazon", 'language': lang, 'text': text_only_limited}
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)

    if result['amazon']['status'] == 'fail':
        for i in range(20):
            n -= 1000
            if  n<=0 :
                API_status = 0
                break
            else:
                text_only_limited = text_only_limited[:n]
                payload={"providers": "amazon", 'language': lang, 'text': text_only_limited}
                response = requests.post(url, json=payload, headers=headers)
                result = json.loads(response.text)
                if result['amazon']['status'] != 'fail':
                    API_status = 1
                    break

    if API_status == 1:
        x = result['amazon']['items']

    #Création dataframe du résultat de l'API
        api_dico = {}
        for i in range(len(x)):
            api_dico[x[i]['sentiment']] = round(x[i]['sentiment_rate'],4)*100

        api_df = pd.DataFrame(list(api_dico.items()), columns=['sentiment', 'sentiment_rate'])

    ###__________________Mise en forme du graphique de l'analyse sentimentale__________________###
        labels = api_df['sentiment'].tolist()
        data = api_df['sentiment_rate'].tolist()


        #Supression sentiment Mixed
        labels.remove('Mixed')
        del data[-1]

        return(data, labels, n, API_status)
    else:
        return API_status





###__________________Envoyer les résultats vers le template du site__________________###

def result(request):
    all_words = request.GET['all_words']                       #0
    limit = request.GET['limit']                               #1
    exact_phrase = request.GET['exact_phrase']                 #2
    # Any_of_these_words = request.GET['Any_of_these_words']   #
    None_of_these_words = request.GET['None_of_these_words']   #3
    These_hastags = request.GET['These_hastags']               #4
    From_acounts = request.GET['From_acounts']                 #5
    To_acounts = request.GET['To_acounts']                     #6
    # Minimun_replies = request.GET['Minimun_replies']         #
    Minimum_likes = request.GET['Minimum_likes']               #7
    # Minimum_retweets = request.GET['Minimum_retweets']       #
    from_date = request.GET['from_date']                       #8
    to_date = request.GET['to_date']                           #9
    lang = request.GET['lang']                                 #10
    
    query = getQuery(searsh_query = [all_words, limit, exact_phrase, None_of_these_words,
                                            These_hastags, From_acounts, To_acounts, Minimum_likes,
                                            from_date, to_date, lang])
    df = get_tweets(query, int(limit))
    df = df.sort_values(['Like', 'Retweet','Replay'],ascending=False)



    x = " ".join(list(df['Tweet']))
    text_only = clean_text(x)
    
    All_text = text_only




##__________________API______________________________###


    x = get_api(text_only, lang)
    
    if len(x) == 4 :   # Whet get_api return False then len(get_API) = 1 else len(get_API) = 4
        data = x[0]
        labels = x[1]
        n = x[2]

        max_data = max(data)
        max_data_index = data.index(max(data))
        max_labels = labels[max_data_index]
    else :
        data = [0, 0, 0]   # This means wa can not do setiment analysis
        labels = ["Positive", "Negative", "Neutral"]




    
    # data = [60, 30, 10]
    # labels = ["Positive", "Negative", "Neutral"]
    # max_data = max(data)
    # max_data_index = data.index(max(data))
    # max_labels = labels[max_data_index]
    # n = 4000

    df_date_sorted = df.sort_values(['Date'],ascending=True)
    from_date = df_date_sorted.iloc[0]['Date'].strftime("%Y-%m-%d")
    to_date = df_date_sorted.iloc[-1]['Date'].strftime("%Y-%m-%d")

    phrase = f"from {from_date} to {to_date}"
    Period = [phrase, phrase, phrase]
    my_api_df = pd.DataFrame({
        "Probability":data,
        "labels":labels,
        "Period":Period
    })



#################################################  365 days ago
    from_to_365_days_ago = get_from_to_date_k_days_ago(df,365)
    from_date_1_year_ago = str(from_to_365_days_ago[0])
    to_date_1_year_ago = str(from_to_365_days_ago[1])
    query = re.sub(r'until:\S+', '', query)     # Remove URL
    query = re.sub(r'since:\S+', '', query)        # Remove mentions
    query += ' until:'+to_date_1_year_ago
    query += ' since:'+from_date_1_year_ago


    df_365_days_ago = get_tweets(query, int(limit))
    df_365_days_ago = df_365_days_ago.sort_values(['Like', 'Retweet','Replay'],ascending=False)

    x_365_days_ago = " ".join(list(df_365_days_ago['Tweet']))
    text_only_365_days_ago = clean_text(x_365_days_ago)


##__________________ API 365_days_ago ______________________________###

    api_365_days_ago = get_api(text_only_365_days_ago, lang)
    
    if len(api_365_days_ago) == 4 :   # Whet get_api return False then len(get_API) = 1 else len(get_API) = 4
        data_365_days_ago = api_365_days_ago[0]
        labels_365_days_ago = api_365_days_ago[1]
        n_365_days_ago = api_365_days_ago[2]
    else :
        data_365_days_ago = [0, 0, 0]   # This means wa can not do setiment analysis
        labels_365_days_ago = ["Positive", "Negative", "Neutral"]

    # data_365_days_ago = [86.99999999999999, 0.208, 0.9705]
    # labels_365_days_ago = ["Positive", "Negative", "Neutral"]
    # n_365_days_ago = 4000


    phrase_365 = f"from {from_date_1_year_ago} to {to_date_1_year_ago}"
    Period = [phrase_365, phrase_365, phrase_365]
    my_api_df_365 = pd.DataFrame({
        "Probability":data_365_days_ago,
        "labels":labels_365_days_ago,
        "Period":Period
    })


    #concatenating dataframes
    frames = [my_api_df, my_api_df_365]
    result_df_api = pd.concat(frames)


    import seaborn as sns


    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.barplot(x = 'Period', y = 'Probability', hue = 'labels', data = result_df_api,
            palette = 'hls',
            # order = ['male', 'female'],  
            capsize = 0.05,             
            saturation = 8,             
            errcolor = 'gray', errwidth = 2,  
            )
    plt.savefig('./base/static/base/images/sns.png')  

#Envoi du résultat sur le site
    if text_only != "":
        stop_words = our_get_stop_words(lang)
        get_word_cloud(stop_words, All_text, max_labels)

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
                                         'n':n,
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
                                        "df_365_days_ago":df_365_days_ago.to_html,
                                        "from_to_365_days_ago":from_to_365_days_ago,
                                        "data_365_days_ago":data_365_days_ago,
                                        "labels_365_days_ago":labels_365_days_ago,
                                         }
                                        )
    else :
        return render(request, 'result_with_no_text.html', {'query': query}
                                        )


def home(request):
    return render(request, 'home.html')











#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
###                                                                                                                           ###
###                                                     Your Own Text Analysis                                                ###
###                                                                                                                           ###
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################





from .forms import YourTextForm                       # For Your Text Analysis
from django.views.generic import TemplateView
from django.shortcuts import render



def your_text(request):
    return render(request, 'your_text.html', {'YourTextForm' : YourTextForm})


def your_text_result(request):
    form = YourTextForm(request.POST)
    if form.is_valid():
        # your_text_field = request.GET['your_text_field']
        text = form.cleaned_data['your_text_field']  # We use this method (instead of GET above) when we use Django's Forms
        text = clean_text(text)  #cleaning the text
        lang = language_detector(text) # detect the language


        # x = get_api(text, lang)  # get sentiment analysis
        # if len(x) == 4 :   # Whet get_api return False then len(get_API) = 1 else len(get_API) = 4
        #     data = x[0]
        #     labels = x[1]
        #     n = x[2]

        #     max_data = max(data)
        #     max_data_index = data.index(max(data))
        #     max_labels = labels[max_data_index]
        # else :
        #     data = [0, 0, 0]   # This means wa can not do setiment analysis
        #     labels = ["Positive", "Negative", "Neutral"]



        data = [60, 30, 10]
        labels = ["Positive", "Negative", "Neutral"]
        max_data = max(data)
        max_data_index = data.index(max(data))
        max_labels = labels[max_data_index]
        n = 4000


        stoplist = our_get_stop_words(lang)
        is_without_stop_words = text_without_stop_words(text,stoplist)
        if re.search('[a-zA-Z]', is_without_stop_words) != None:       # check if is_without_stop_words containes any letter from a to Z or from A to Z
            stop_words = our_get_stop_words(lang) #Get stop words with this language
            get_word_cloud(stop_words, text, max_labels)
        else : 
            return render(request, 'result_with_no_text.html', {'query': text})


        return render(request, 'your_text_result.html', { 
                                                            'n':n,
                                                            "data":data,
                                                            "labels":labels,
                                                            'max_data':round(max_data,2),
                                                            'max_labels':max_labels
                                                            })
