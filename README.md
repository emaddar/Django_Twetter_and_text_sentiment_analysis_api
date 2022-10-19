<H1 style="color:rgb(44, 44, 90)", align = "center">
Twitter API sentiment analysis
</H1>

<p align="justify">
This application searches for the latest Tweets in a defined period. Then an AI model analyzes and summarizes the tweets to give the general sentiment on the subject or the person in question.

Cette application permet à partir d'une recherche des derniers n tweets (n à définir par l'utilisateur) d'opérer une analyse des sentiments. Pour cela, l'applciation mobilise différents API mobilisant l'intelligence articielle. 

![accueil](./ressources/apercu_accueil.png)


Nous sollicitons notamment :
- [Edenai](https://www.edenai.co/post/top-10-sentiment-analysis-apis) pour analyser la charge émotionnelle des tweets selectionnés
- Le package [snscrape](https://github.com/JustAnotherArchivist/snscrape) pour opérer la requête sur twitter
- Le package [stopwords](https://pypi.org/project/stop-words/) pour chercher les appax permettant de nettoyer le texte récolté. **Note: Nous avons amendé cette liste de nos propres mots** _N'hesitez pas à nous contacter si vous souhaitez ajouter d'autres mots_
- Le package [word cloud](https://pypi.org/project/wordcloud/) pour afficher le nuage de mot afférent

Une fois la requête effectuée, notre application renvoie deux pages possibles de résultat :
- Si la recherche trouve au moins un tweet, le résultat est présenté dans la page `result.html`
![result_page](./ressources/result_page.png)
- Si la recherche ne trouve pas de tweet, le résultat est présenté dans la page `result_with_no_text`
![result_with_no_text_page](./ressources/result_with_no_text_page.png)

Conseil d'utilisation pour l'API
Il n'y a pas de limite (ni en nombre, ni en date) de requêtes par jour en ce qui concerne la recherche de tweets. Cependant, il faut créer un [compte](https://app.edenai.run/user/register?referral=best-sentiment-analysis-apis) pour réaliser l'analyse de sentiments. Le site propose alors un crédit de 10 dollars à consommer selon l'utilisation.

API : 

1. On prend les tweet
2. On les joins+nettoyer pr analyser le texte global -> comment supprimer émojis, " ", appax (il elle, ...)
3. On analyse le sentiment global de ce texte
4. On présente les n tweet les plus likés, les plus retweetés, les plus replayés (commenté)

Todo :
Ajouter un masque : affiché dans un nuage de mots, afficher en rouge si négatif, afficher en vert si positif
Chercher un moyen de reconnaitre le sexe du posteur de tweet
Historique des sentiments pour la même période
Ajouter button pour ddl le nuage de mots
Créer un forum django pour demander key propre de chaque utilisateur

Axe amélioration:
Stop word pour les langues qui n'utilisent pas le même alphabet
</p>