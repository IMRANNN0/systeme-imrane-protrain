# Méthodes quantitatives — choix et limites

Lire [calculs.md](calculs.md) pour le schéma et les commandes exactes du script, puis la section utile ci-dessous. Les outils exécutent des règles explicites ; ils ne valident ni les données, ni un barème, ni une causalité. Les critères business restent dans [methode.md](methode.md).

## Assessment pondéré et vue radar

La capture transmise donne quatre cas. Une formule reconstruite compatible est, pour un axe et ses facteurs renseignés `S` :

`Axe (%) = 100 × Σ(i∈S) [poids_i × note_i] / [5 × Σ(i∈S) poids_i]`.

| Axe de la capture | Poids visibles | Notes visibles | Résultat de reconstruction |
| --- | --- | --- | --- |
| Produit | 5, 5, 1, 5, 5, 5 | 4, 1, 5, 4, 1, 2 | 65 / 130 × 100 = 50 % |
| Marché | 5, 5 | 1, 2 | 15 / 50 × 100 = 30 % |
| Consommateur | 5, 4, 5 | 3, 1, 2 | 29 / 70 × 100 ≈ 41,43 % |
| Économie | 5, 5, 5, 5 | 2, 2, 2, 1 | 35 / 100 × 100 = 35 % |

Urgence et offre disponible (« Supply ») sont vides dans la capture et exclues de ces sommes. Les données correspondent à la démonstration fournie, pas à des défauts de poids pour un client. La correspondance des quatre résultats étaye la reconstruction arithmétique ; elle ne révèle ni le sens original de chaque note ni les seuils.

Avec l'échelle proposée 1–5, ce pourcentage normalise une appréciation, pas une probabilité de vente ; son minimum avec toutes les notes à 1 est 20 %, pas 0 %. Les poids indiquent l'importance pour le client, pas la solidité de la preuve. Lire [bareme-local.md](bareme-local.md) avant de proposer des notes : version locale à revoir, jamais présentée comme approuvée ou comme barème original retrouvé.

Un inconnu n'est pas 0 ou 1. Un non-applicable est justifié et exclu explicitement. Afficher facteurs renseignés, exclus et manquants, et la couverture des poids si tous les poids nécessaires sont connus. Sinon, dire que cette couverture pondérée est indéterminée. Si aucun facteur utilisable ne reste, ne pas calculer l'axe. Ne pas supposer les poids absents.

Le radar présente les axes sur une même échelle avec libellés et limites. Un axe manquant reste visiblement manquant, sans interpolation en zéro ; des axes partiels sont signalés. Aire du polygone, ordre des axes et moyenne non autorisée ne constituent pas un grade global. Aucune pondération entre axes ni coupure GO/STOP n'a été fournie.

Statuts de calcul : `draft_local` et `screenshot_demo` nécessitent `--demo` et une étiquette de démonstration non validée. `owner_confirmed` exige confirmation explicite préalable des règles et entrées par le propriétaire. Le script ne doit pas convertir un récit en notes. Voir les conditions exactes dans [calculs.md](calculs.md).

## Élasticité-prix : midpoint

Sur deux observations comparables :

`E = [(Q2−Q1)/((Q1+Q2)/2)] / [(P2−P1)/((P1+P2)/2)]`.

Conserver le signe et interpréter habituellement `|E|` : supérieur à 1, élastique ; inférieur à 1, inélastique ; égal à 1, unitaire, sous réserve de précision. Prix inchangé ou moyenne nulle rend le ratio concerné indéfini ; refuser les entrées incohérentes. Comparer même produit, zone, unités et durée de mesure. L'élasticité est sans unité ; une pente linéaire `dQ/dP` a des unités. Au point, `E = (dQ/dP) × P/Q` : une pente constante ne signifie pas élasticité constante. [Appui : OpenStax, section 5.1](https://openstax.org/books/principles-economics-2e/pages/5-1-price-elasticity-of-demand-and-price-elasticity-of-supply).

Le calcul entre deux points reste descriptif si publicité, saison, stock, concurrence ou clientèle ont changé. Ne pas qualifier un effet de causal sans identification adaptée. Effets de prix croisés : examiner substitutions ou complémentarités avec des données pertinentes, sans en faire une catégorie discrète ni transférer automatiquement l'élasticité d'un autre produit.

## Demande statistique et régression

La méthode transmise propose `Qd = f(P, Prg, Y)` : quantité demandée, prix propre, prix d'un bien relié et revenu, dont les unités et populations doivent être précisées. **Exemple de cours seulement :** `Qd = 1000 − 2P + 3Prg + 0,5Y`. Ces nombres ne sont pas des coefficients client ; `−2` est une pente, pas une élasticité. Le signe du prix relié n'est pas universel : substitut, complément et contexte doivent être étudiés.

Pour ajuster un modèle avec des outils statistiques déjà autorisés, définir la cible, aligner les observations et prédicteurs disponibles au moment prévu, puis estimer sur un jeu d'apprentissage. Examiner résidus, autocorrélation, observations influentes et colinéarité. Évaluer hors échantillon, comparer une baseline et documenter scénarios des prédicteurs futurs et incertitude. Ne pas présenter corrélation, coefficient significatif ou bon ajustement interne comme preuve causale. [Appui : FPP3, modèles de régression](https://otexts.com/fpp3/regression.html).

Le script fourni n'ajuste pas d'OLS. En l'absence de données, d'outil ou de validation adaptés, décrire ce qui manque et rester qualitatif. Des dépenses publicitaires peuvent répondre à la demande attendue : leur corrélation avec les ventes ne prouve pas leur effet incrémental.

## Séries temporelles, baselines et erreurs

Définir la cible : quantité, revenu ou profit ne sont pas interchangeables. Fixer fréquence, calendrier, fuseau, périmètre, retours et taxes ; repérer doublons, trous, valeurs nulles, ruptures de stock et changements de définition. Décrire tendance, saisonnalité, anomalies et événements sans les supprimer automatiquement. Une saisonnalité annuelle ne se démontre pas avec quelques semaines.

Réserver chronologiquement les dernières observations pour un horizon pertinent ; aucun mélange aléatoire ni information du futur dans l'apprentissage. Si les données suffisent, employer plusieurs origines temporelles de backtest. Comparer les méthodes disponibles, notamment naïve et naïve saisonnière si la saison est définie et observée. Sur les mêmes dates et le même horizon :

`e_t = réel_t − prévision_t`

`MAE = moyenne(|e_t|)` ; `RMSE = racine(moyenne(e_t²))`.

Ces erreurs ont l'unité de la cible et doivent être calculées hors apprentissage. Un modèle complexe n'est retenu que si son utilité et ses performances comparées le justifient ; sinon garder la baseline ou déclarer les données insuffisantes. [Appuis : FPP3, validation temporelle](https://otexts.com/fpp3/toolbox.html#time-series-cross-validation) et [précision des prévisions](https://otexts.com/fpp3/toolbox.html#evaluating-point-forecast-accuracy).

Une prévision de ventes n'est ni une prévision de marge nette ni un effet de publicité. Documenter coûts, prix, capacité et scénarios séparément avant d'en tirer une décision business. Les fonctionnalités et limites réelles des baselines du script sont précisées dans [calculs.md](calculs.md), sans inventer un modèle causal ou des intervalles non calculés.
