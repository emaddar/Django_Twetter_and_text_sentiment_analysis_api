# ### text sentiment analysis

# # https://www.edenai.co/post/top-10-sentiment-analysis-apis
# # https://app.edenai.run/bricks/text/sentiment-analysis#live-testing

# import json
# import requests

# headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYjI3ODQwYjUtY2IxOC00MGFmLWE5NmEtYWMzNzNjMzAxMDBmIiwidHlwZSI6ImFwaV90b2tlbiJ9.sJnkDP04P0fnK0Bd_ayFkEpFMM0gM9GdM8MR9LwsLG0"}

# url ="https://api.edenai.run/v2/text/sentiment_analysis"
# text = "I'm happy to tell you that I have a baby"
# payload={"providers": "google,amazon", 'language': "en", 'text': text}

# response = requests.post(url, json=payload, headers=headers)

# result = json.loads(response.text)
# print(result['google']['items'])

# ###package snscrape.modules.twitter as sntwitter

# #Pour requeter les n tweets sur twitter avec une query définie

from ast import NotIn
from stop_words import get_stop_words

##pour ajouter des appax
stop_words=get_stop_words("fr")
ma_list = ["c'est", "est","j'ai","ça", "ca", "après", "qu'"]
for mot in ma_list:
    if mot not in stop_words:
        stop_words.append(mot)

print(stop_words)