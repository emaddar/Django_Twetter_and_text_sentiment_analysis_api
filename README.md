<H1 style="color:rgb(44, 44, 90)", align = "center">
Twitter API sentiment analysis
</H1>

Cette application permet à partir d'une recherche des derniers n tweets (n à définir par l'utilisateur) d'opérer une analyse des sentiments. Pour cela, l'application mobilise différents API mobilisant l'intelligence articielle. 

![accueil](./ressources/apercu_accueil.png)


Nous sollicitons notamment :
- [Edenai](https://www.edenai.co/post/which-sentiment-analysis-api-to-choose-for-your-project) pour analyser la charge émotionnelle des tweets selectionnés
- Le package [snscrape](https://github.com/JustAnotherArchivist/snscrape) pour opérer la requête sur twitter
- Le package [stopwords](https://pypi.org/project/stop-words/) pour chercher les appax permettant de nettoyer le texte récolté. **Note: Nous avons amendé cette liste de nos propres mots** _N'hesitez pas à nous contacter si vous souhaitez ajouter d'autres mots_
- Le package [word cloud](https://pypi.org/project/wordcloud/) pour afficher le nuage de mot afférent

Une fois la requête effectuée, notre application trie les tweets en priorisant les tweets les plus likés (puis les plus retweetés, puis les plus commentés) et renvoie deux pages possibles de résultat :
- Si la recherche trouve au moins un tweet, le résultat est présenté dans la page `result.html`
![result_page](./ressources/result_page.png)
- Si la recherche ne trouve pas de tweet, le résultat est présenté dans la page `result_with_no_text`
![result_with_no_text_page](./ressources/result_with_no_text_page.png)

Conseil d'utilisation pour l'API
Il n'y a pas de limite (ni en nombre, ni en date) de requêtes par jour en ce qui concerne la recherche de tweets. Cependant, il faut créer un [compte](https://app.edenai.run/user/login?referral=sentiment-analysis-how-to) pour réaliser l'analyse de sentiments et renseigner la key obtenue. De plus, l'analyse ne peut se réaliser que sur un corpus de 10 000 characters maximum. Le site propose alors un crédit de 10 dollars à consommer selon l'utilisation.

API : 

1. On prend les tweet
2. On les joins+nettoyer pr analyser le texte global -> comment supprimer émojis, " ", appax (il elle, ...)
3. On analyse le sentiment global de ce texte
4. On présente les n tweet les plus likés, les plus retweetés, les plus replayés (commenté)

Todo :
1. DONE : Ajouter un masque : affiché dans un nuage de mots
2. DONE: Ajouter un button pour télécharger le nuage
3. Done: classer les tweets les plus likés 
4. DONE: mettre une limite à 10000 characters + ajouter message d'information
5. DONE: implémenter l'api
6. présenter graphique 
7. liste des 3 tweets les plus importants 
8. historique en graphique à 1 semaine/1 mois/1 an
9. créer un forum pour demander la key
10. afficher en rouge si négatif, afficher en vert si positif
11. créer une fonction pour faire tourner même sans l'api
12. explorer la possibilité d'analyser facebook, instagram
Chercher un moyen de reconnaitre le sexe du posteur de tweet
Historique des sentiments pour la même période
Créer un forum django pour demander key propre de chaque utilisateur

Axe amélioration:
Stop word pour les langues qui n'utilisent pas le même alphabet