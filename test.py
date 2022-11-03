from bs4 import BeautifulSoup  
import re
import requests

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

URL = "https://mail.google.com/mail/u/0/#inbox/FMfcgzGqRQBpmrRggsxwQbcbtgQwcVbb"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup

scrap_text  = []
for anchor in soup:
    scrap_text.append(anchor.text) # Display the innerText of each anchor

text = clean_text(''.join(scrap_text))



def get_api(text_only_limited, lang, key):
    headers = {"Authorization": "Bearer "+key}
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

    # Create a dataframe of the API result
        api_dico = {}
        for i in range(len(x)):
            api_dico[x[i]['sentiment']] = round(x[i]['sentiment_rate'],4)*100
        api_df = pd.DataFrame(list(api_dico.items()), columns=['sentiment', 'sentiment_rate'])

    # Formatting of the sentimental analysis graph
        labels = api_df['sentiment'].tolist()
        data = api_df['sentiment_rate'].tolist()

    # Remove "Mixed" sentiment
        labels.remove('Mixed')
        del data[-1]
        return(data, labels, n, API_status)
    else:
        return API_status