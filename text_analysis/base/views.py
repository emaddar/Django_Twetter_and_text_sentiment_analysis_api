#########################################################################
#                          Import packages                              #
#########################################################################

from cProfile import label
from email.mime import image
from http.client import HTTPResponse
import imp
from django.shortcuts import render
import snscrape.modules.twitter as sntwitter                            # For scrapping twitter
import pandas as pd
import re
from stop_words import get_stop_words                                   # For cleaning text
from wordcloud import WordCloud                                         # For get a Wordcloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import json                                                             # For get the sentiment analysis API
import requests                                                         # For get the sentiment analysis API
import random
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect                            # For signUp page
from .forms import SignUp, UploadFileForm                               # For signUp page
from django.contrib.auth.forms import UserCreationForm                  # For signUp page methode 2
from django.urls import reverse_lazy                                    # For signUp page methode 2
from django.views import generic                                        # For signUp page methode 2
from django.views.generic import CreateView                             # For SignUp form Page  
from . import forms                                                     # For SignUp form Page 
from django.contrib.auth.decorators import login_required
import langid                                                           # For language detect
from .forms import YourTextForm                                         # For Your text analysis
from django.views.generic import TemplateView                           # For Your text analysis
from dataclasses import replace                                         # For URL text analysis
from bs4 import BeautifulSoup                                           # For URL text analysis

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
###                                                                                                                           ###
###                                                         About                                                             ###
###                                                                                                                           ###
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

def about(request):
    return render(request, 'about.html')


#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
###                                                                                                                           ###
###                                                   Twitter analysis                                                        ###
###                                                                                                                           ###
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

@login_required                                     # Makes loggin mandatory
def tweet(request):
    return render(request, 'index.html')

###____________________________Scrapping____________________________###

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

###__________________________Text cleaning__________________________###

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

def text_without_stop_words(text,stopwords):
    for i in (text.split()):
        if i in stopwords:
            text = text.replace(i, '')
    return text

def our_get_stop_words(lang):
    stop_words = get_stop_words(lang)               # Possible to add words
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

# Create a single text for analysis
def getQuery(searsh_query):
    query = searsh_query[0] + " lang:" + searsh_query[10] + " " 
    if searsh_query[2] != "":
        query += '"' + searsh_query[2] + '"' + " "
    if searsh_query[3] != "":
        query +=  ' '.join(['-'+i for i in searsh_query[3].split()]) + " "
    if searsh_query[4] != "":
        query += '(' + join_with(searsh_query[4].split(), 'OR') + ')'  + " "
    if searsh_query[5] != "":
        query += '(from:' + join_with(searsh_query[5].split(), 'OR from:') + ')'  + " "
    if searsh_query[6] != "":
        query += '(to:' + join_with(searsh_query[6].split(), 'OR to:') + ')'  + " "
    if searsh_query[7] != "" :
        query += 'min_faves:' + searsh_query[7] + " "
    if searsh_query[8] != "" :
        query += 'since:' + searsh_query[8] + " "
    if searsh_query[9] != "" :
        query += 'until:' + searsh_query[9] + " "
    return query

###___________________________World cloud___________________________###

# Word cloud's color
def couleur_red(*args, **kwargs):
    return "rgb(255, 0, {})".format(random.randint(0, 170))

def couleur_blue(*args, **kwargs):
    return "rgb({}, 0, 255)".format(random.randint(0, 170))

# Create Word cloud
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

###_____________________________Get API_____________________________###

def get_api(text_only_limited, lang, key):
    
    headers = {"Authorization": "Bearer "+key}
    lang = "fr"
    url ="https://api.edenai.run/v2/text/sentiment_analysis"

    n = len(text_only_limited)
    if n >= 4000:
        text_only_limited = text_only_limited[:4000]
        n = len(text_only_limited)

    API_status = 1
    payload={"providers": "google", 'language': lang, 'text': text_only_limited}
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)

    if result['google']['status'] == 'fail':
        for i in range(20):
            n -= 1000
            if  n<=0 :
                API_status = 0
                break
            else:
                text_only_limited = text_only_limited[:n]
                payload={"providers": "google", 'language': lang, 'text': text_only_limited}
                response = requests.post(url, json=payload, headers=headers)
                result = json.loads(response.text)
                if result['google']['status'] != 'fail':
                    API_status = 1
                    break

    if API_status == 1:

    #     x = result['amazon']['items']

    # # Create a dataframe of the API result
    #     api_dico = {}
    #     for i in range(len(x)):
    #         api_dico[x[i]['sentiment']] = round(x[i]['sentiment_rate'],4)*100
    #     api_df = pd.DataFrame(list(api_dico.items()), columns=['sentiment', 'sentiment_rate'])

    # # Formatting of the sentimental analysis graph
    #     labels = api_df['sentiment'].tolist()
    #     data = api_df['sentiment_rate'].tolist()

    # # Remove "Mixed" sentiment
    #     labels.remove('Mixed')
    #     del data[-1]
        result_list = result['google']['items']
        labels = []
        data = []
        for i in range(len(result_list)):
            labels.append(result_list[i]['sentiment'])
            data.append(round(result_list[i]['sentiment_rate']*100,3))

        d = {'labels':labels,'data':data}
        d = pd.DataFrame(d)
        d = d.groupby('labels').mean()
        d = d.reset_index()
        d = dict(zip(d.labels, d.data))


        labels = ["Positive", "Negative", "Neutral"]
        data = [d[labels[0]], d[labels[1]], d[labels[2]]]
        return(data, labels, n, API_status)
    else:
        return API_status

###______________Get from date to date ... k days ago_______________###

def get_from_to_date_k_days_ago(df,k):
    df_date_sorted = df.sort_values(by='Date')
    df_date_sorted_time_type = df_date_sorted 
    
    from_date = df_date_sorted_time_type.iloc[0]['Date']
    to_date = df_date_sorted_time_type.iloc[-1]['Date']

    from_date_1_year_ago = (pd.to_datetime(from_date.strftime('%Y-%m-%d')) - timedelta(days=k)).strftime('%Y-%m-%d')
    to_date_1_year_ago = (pd.to_datetime(to_date.strftime('%Y-%m-%d')) - timedelta(days=k-1)).strftime('%Y-%m-%d')
    return (from_date_1_year_ago, to_date_1_year_ago)

###_____________Sending result to the website template______________###

def result(request):
    api_key = request.user.api_key                              # Get User Api Key



    all_words = request.GET['all_words']                       #0
    limit = request.GET['limit']                               #1
    exact_phrase = request.GET['exact_phrase']                 #2
    None_of_these_words = request.GET['None_of_these_words']   #3
    These_hastags = request.GET['These_hastags']               #4
    From_acounts = request.GET['From_acounts']                 #5
    To_acounts = request.GET['To_acounts']                     #6
    Minimum_likes = request.GET['Minimum_likes']               #7
    from_date = request.GET['from_date']                       #8
    to_date = request.GET['to_date']                           #9
    lang = request.GET['lang']                                 #10
    radio_yes = request.GET['radio_yes']  
    
    query = getQuery(searsh_query = [all_words, limit, exact_phrase, None_of_these_words,
                                            These_hastags, From_acounts, To_acounts, Minimum_likes,
                                            from_date, to_date, lang])
    df = get_tweets(query, int(limit))
    df = df.sort_values(['Like', 'Retweet','Replay'],ascending=False)

    x = " ".join(list(df['Tweet']))
    text_only = clean_text(x)
    
    All_text = text_only
    if text_only == "":
        return render(request, 'result_with_no_text.html', {'query': query})
    else :

    #### API ####
        api_key = request.user.api_key                              # Get User Api Key
        x = get_api(text_only, lang, api_key)
        
        if len(x) == 4 :                              # When get_api return False then len(get_API) = 1 else len(get_API) = 4
            data = x[0]
            labels = x[1]
            n = x[2]
            max_data = max(data)
            max_data_index = data.index(max(data))
            max_labels = labels[max_data_index]
        else :
            data = [0, 0, 0]   # This means wa can not do setiment analysis
            labels = ["Positive", "Negative", "Neutral"]
    #### API ####

        # data = [60, 30, 10]                             # API 365 Fixed Value (to save API credits)
        # labels = ["Positive", "Negative", "Neutral"]    # API 365 Fixed Value (to save API credits)
        # max_data = max(data)                            # API 365 Fixed Value (to save API credits)
        # max_data_index = data.index(max(data))          # API 365 Fixed Value (to save API credits)
        # max_labels = labels[max_data_index]             # API 365 Fixed Value (to save API credits)
        # n = 4000


        

        if radio_yes == "Yes" :

            df_date_sorted = df.sort_values(['Date'],ascending=True)
            from_date = df_date_sorted.iloc[0]['Date'].strftime("%Y-%m-%d") # get date of 1st tweet in result
            to_date = df_date_sorted.iloc[-1]['Date'].strftime("%Y-%m-%d")  # get date of last tweet in result
            phrase = f"from {from_date} to {to_date}"

    ### 365 days ago ###
            from_to_365_days_ago = get_from_to_date_k_days_ago(df,365)
            from_date_1_year_ago = str(from_to_365_days_ago[0])
            to_date_1_year_ago = str(from_to_365_days_ago[1])
            query = re.sub(r'until:\S+', '', query)   # Remove URL
            query = re.sub(r'since:\S+', '', query)   # Remove mentions
            query += ' until:'+to_date_1_year_ago
            query += ' since:'+from_date_1_year_ago

            df_365_days_ago = get_tweets(query, int(limit))
            df_365_days_ago = df_365_days_ago.sort_values(['Like', 'Retweet','Replay'],ascending=False)

            x_365_days_ago = " ".join(list(df_365_days_ago['Tweet']))
            text_only_365_days_ago = clean_text(x_365_days_ago)

    #### API 365_days_ago ####
            
            api_365_days_ago = get_api(text_only_365_days_ago, lang, api_key)
            
            if len(api_365_days_ago) == 4 :   # Whet get_api return False then len(get_API) = 1 else len(get_API) = 4
                data_365_days_ago = api_365_days_ago[0]
                labels_365_days_ago = api_365_days_ago[1]
                n_365_days_ago = api_365_days_ago[2]
            else :
                data_365_days_ago = [0, 0, 0]   # This means wa can not do setiment analysis
                labels_365_days_ago = ["Positive", "Negative", "Neutral"]
    #### API 365_days_ago ####

            # data_365_days_ago = [86.99999999999999, 0.208, 0.9705]            # API 365 Fixed Value (to save API credits)
            # labels_365_days_ago = ["Positive", "Negative", "Neutral"]         # API 365 Fixed Value (to save API credits)
            # n_365_days_ago = 4000                                             # API 365 Fixed Value (to save API credits)

            phrase_365 = f"from {from_date_1_year_ago} to {to_date_1_year_ago}"

            result_df_api = pd.DataFrame({
            "Period" : [phrase, phrase_365]  ,
            "Positive" : [data[0], data_365_days_ago[0]],
            "Negative" :[data[1], data_365_days_ago[1]],
            "Neutral" : [data[2], data_365_days_ago[2]]
            })

            plt.rcParams["figure.figsize"] = (10,3)
            result_df_api.plot(x="Period",
                                    y=["Positive", "Negative", "Neutral"],
                                    kind="bar",
                                    color=[(75/255, 192/255, 192/255, 0.5),
                                        (255/255, 99/255, 132/255, 0.5),
                                        (255/255, 206/255, 86/255, 0.5)])
            plt.xticks(rotation=0)
            plt.savefig('./base/static/base/images/copmared_365_days.png',bbox_inches='tight')  
        else :
            phrase = ""
            phrase_365 = "" 

    ### Envoi du résultat sur le site ###
        if text_only != "":
            stop_words = our_get_stop_words(lang)
            get_word_cloud(stop_words, All_text, max_labels)

    ### Get  3 Tweets most liked ###
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
    
        
            return render(request, 'result.html', {
                                            'api_key':api_key,
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
                                            # "df_365_days_ago":df_365_days_ago.to_html,
                                            # "from_to_365_days_ago":from_to_365_days_ago,
                                            # "data_365_days_ago":data_365_days_ago,
                                            # "labels_365_days_ago":labels_365_days_ago,
                                            # "result_df_api": result_df_api.to_html(),
                                            "phrase" : phrase,
                                            "phrase_365": phrase_365,
                                            "radio_yes":radio_yes
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
###                                         Your text analysis // URL text analysis                                           ###
###                                                                                                                           ###
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

@login_required                                     # Makes loggin mandatory for Your text analysis
def your_text(request):
    return render(request, 'your_text.html', {'YourTextForm' : YourTextForm})

@login_required                                     # Makes loggin mandatory for URL text analysis
def upload_file(request):
    return render(request, 'upload_file.html')

# Language detection
def language_detector(text):
    return langid.classify(text)[0]

# Create Word cloud
def get_word_cloud_your_text_your_url(stop_words, text_only, status):
    mask = np.array(Image.open("../ressources/mask_cloud.png"))
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

###_______________________Your text analysis________________________###

def your_text_result(request):
    form = YourTextForm(request.POST)
    if form.is_valid() and form != "":
        # your_text_field = request.GET['your_text_field']
        text = form.cleaned_data['your_text_field']              # We use this method (instead of GET above) when we use Django's Forms
        text = clean_text(text)                                  # Cleaning the text
        lang = language_detector(text)                           # Detect the language
        supported_language = ["af", "am", "an", "ar", "as", "az", "be", "bg", "bn", "br", "bs", "ca", "cs", "cy", "da", "de",
                         "dz", "el", "en", "eo", "es", "et", "eu", "fa", "fi", "fo", "fr", "ga", "gl", "gu", "he", "hi",
                          "hr", "ht", "hu", "hy", "id", "is", "it", "ja", "jv", "ka", "kk", "km", "kn", "ko", "ku", "ky",
                           "la", "lb", "lo", "lt", "lv", "mg", "mk", "ml", "mn", "mr", "ms", "mt", "nb", "ne", "nl", "nn",
                            "no", "oc", "or", "pa", "pl", "ps", "pt", "qu", "ro", "ru", "rw", "se", "si", "sk", "sl", "sq",
                             "sr", "sv", "sw", "ta", "te", "th", "tl", "tr", "ug", "uk", "ur", "vi", "vo", "wa", "xh", "zh", "zu"]
        if (lang == "la") or (lang not in supported_language) :
            return render(request, 'result_with_no_text.html', {'query': request.GET['file']})
        else:
#### API ####
            api_key = request.user.api_key                              # Get User Api Key
            x = get_api(text, lang, api_key)  # get sentiment analysis
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
    #### API ####

    ### API fixed values (to save API credits) ###
            # data = [60, 30, 10]
            # labels = ["Positive", "Negative", "Neutral"]
            # max_data = max(data)
            # max_data_index = data.index(max(data))
            # max_labels = labels[max_data_index]
            # n = 4000
    ### API fixed values (to save API credits) ###

            stoplist = our_get_stop_words(lang)
            is_without_stop_words = text_without_stop_words(text,stoplist)
            if re.search('[a-zA-Z]', is_without_stop_words) != None:       # check if is_without_stop_words containes any letter from a to Z or from A to Z
                stop_words = our_get_stop_words(lang) #Get stop words with this language
                get_word_cloud_your_text_your_url(stop_words, text, max_labels)
            else : 
                return render(request, 'result_with_no_text.html', {'query': text})

            return render(request, 'your_text_result.html', { 
                                                                'n':n,
                                                                "data":data,
                                                                "labels":labels,
                                                                'max_data':round(max_data,2),
                                                                'max_labels':max_labels
                                                                })

###_______________________URL text analysis_________________________###

def upload_file_result(request):
    text = request.GET['file']
    
    page = requests.get(text) # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup
    scrap_text  = []
    for anchor in soup:
        scrap_text.append(anchor.text) # Display the innerText of each anchor
    text = clean_text(''.join(scrap_text))

    lang = language_detector(text) # detect the language
    supported_language = ["af", "am", "an", "ar", "as", "az", "be", "bg", "bn", "br", "bs", "ca", "cs", "cy", "da", "de",
                         "dz", "el", "en", "eo", "es", "et", "eu", "fa", "fi", "fo", "fr", "ga", "gl", "gu", "he", "hi",
                          "hr", "ht", "hu", "hy", "id", "is", "it", "ja", "jv", "ka", "kk", "km", "kn", "ko", "ku", "ky",
                           "la", "lb", "lo", "lt", "lv", "mg", "mk", "ml", "mn", "mr", "ms", "mt", "nb", "ne", "nl", "nn",
                            "no", "oc", "or", "pa", "pl", "ps", "pt", "qu", "ro", "ru", "rw", "se", "si", "sk", "sl", "sq",
                             "sr", "sv", "sw", "ta", "te", "th", "tl", "tr", "ug", "uk", "ur", "vi", "vo", "wa", "xh", "zh", "zu"]
    if (lang == "la") or (lang not in supported_language) :
        return render(request, 'result_with_no_text.html', {'query': request.GET['file']})
    else:
    #### API ####
        api_key = request.user.api_key                              # Get User Api Key
        x = get_api(text, lang, api_key)  # get sentiment analysis
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
    #### API ####

    ### API fixed values (to save API credits) ###
        # data = [60, 30, 10]
        # labels = ["Positive", "Negative", "Neutral"]
        # max_data = max(data)
        # max_data_index = data.index(max(data))
        # max_labels = labels[max_data_index]
        # n = 4000
    ### API fixed values (to save API credits) ###

        stoplist = our_get_stop_words(lang)
        is_without_stop_words = text_without_stop_words(text,stoplist)
        if re.search('[a-zA-Z]', is_without_stop_words) != None:       # check if is_without_stop_words containes any letter from a to Z or from A to Z
            stop_words = our_get_stop_words(lang) #Get stop words with this language
            get_word_cloud_your_text_your_url(stop_words, text, max_labels)
        else : 
            return render(request, 'result_with_no_text.html', {'query': text})

        return render(request, 'upload_file_result.html', { 
                                                                'n':n,
                                                                "data":data,
                                                                "labels":labels,
                                                                'max_data':round(max_data,2),
                                                                'max_labels':max_labels
                                                                })

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
###                                                                                                                           ###
###                                                     SignUp form Page                                                      ###
###                                                                                                                           ###
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

class SignupPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = './registration/signup.html'
