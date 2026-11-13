# Calculs locaux et sorties — contrat d'utilisation

Outil standard Python, sans réseau ni dépendance supplémentaire :
`<workspace>/.agents/skills/media-buying-business-diagnosis/scripts/demand_tools.py`.
Choisir une destination autorisée dans la lane du client lorsque le livrable fichier est demandé ; utiliser un dossier de simulation pour les exemples. Les fichiers existants ne sont pas écrasés.

## Demand Assessment : formule reconstruite, barème proposé

Pour un axe :

`pourcentage = 100 × Σ(poids × note) / (note_max × Σ(poids des facteurs notés))`.

Cette formule **reproduit** les quatre pourcentages visibles dans la capture transmise par le propriétaire ; nous n'avons pas le classeur original pour prouver sa formule interne ni son barème de jugement.

La transcription et les quatre calculs de vérification sont conservés dans [methodes-quantitatives.md](methodes-quantitatives.md), section « Assessment pondéré et vue radar ».

Urgency et Supply sont vides dans la capture : ils restent inconnus et hors du sous-total, pas notés zéro ni déclarés sans objet. Le résultat affiche donc la couverture partielle. Le pourcentage représente les points de la grille rapportés à leur maximum, **pas une probabilité de vente**. Avec des notes minimales de 1 sur 5, le minimum noté est 20 %, pas 0 % : aucune transformation implicite vers une autre échelle.

Les quatre axes n'ont pas d'agrégation globale confirmée. L'outil ne produit ni moyenne globale arbitraire, ni seuil GO/STOP. Voir [bareme-local.md](bareme-local.md) pour la proposition de notation à revoir avec le propriétaire.

### Entrées et états

Partir de `assets/assessment-template.json`. Renseigner scope (client/offre/marché/période), puis chaque facteur :

- `rated` : poids entier de 1 à 5, note entière dans l'échelle explicite, `reason` et `evidence` obligatoires ;
- `unknown` : information absente ; aucune note ;
- `not_applicable` : sans objet avec justification, aucune note.

Les facteurs absents de l'entrée restent inconnus. Les axes attendus sont `product_nature`, `market`, `consumer`, `economic_conditions`, avec les 17 identifiants du modèle. Les axes et facteurs en double sont refusés. Dates, sources et qualité des preuves doivent être examinées dans le diagnostic : le calcul ne les authentifie pas.

`factor_coverage` est la fraction de critères applicables renseignés. `weighted_coverage` est une fraction de poids, calculable seulement si tous les poids applicables sont connus ; sinon elle vaut `null`, avec explication. Le ratio de critères ne remplace pas ce ratio pondéré.

`rubric.status` peut être `draft_local`, `screenshot_demo` ou `owner_confirmed`. Les deux premiers exigent `--demo` et marquent les sorties DEMONSTRATION. Pour un usage client, obtenir l'accord réel du propriétaire sur le barème et les notes, puis inscrire `owner_confirmed`, `approved_by` et `approved_at` dans le JSON. Ces champs consignent l'accord ; les renseigner ne crée pas l'autorisation. Ne jamais les préremplir pour contourner une revue.

Exemple de reproduction de la capture, à lancer dans un nouveau dossier de simulation :

```powershell
python <workspace>/.agents/skills/media-buying-business-diagnosis/scripts/demand_tools.py assessment --input <workspace>/.agents/skills/media-buying-business-diagnosis/assets/screenshot-assessment.json --out <workspace>/tmp/codex-session/demand-demo-NOUVEAU --demo
```

Sorties : `assessment.json`, `assessment.csv`, `assessment.svg` et `assessment.html`. HTML autonome, sans service distant ; tableau des résultats et données/limites. Les axes partiels sont des points non reliés ; les inconnus ne créent pas artificiellement une surface nulle. Le radar n'est relié que si les quatre axes ont chacun une valeur et aucun facteur applicable inconnu. Un axe entièrement sans objet n'est pas dessiné comme zéro.

## Élasticité au point milieu

```powershell
python <workspace>/.agents/skills/media-buying-business-diagnosis/scripts/demand_tools.py elasticity --p1 100 --p2 110 --q1 110 --q2 100
```

Retour JSON : élasticité signée et absolue, variations relatives et catégorie. Prix strictement positifs, quantités non négatives, prix différents et quantité moyenne positive. Comparer des périmètres réellement comparables ; le calcul descriptif n'isole pas un effet causal du prix. Voir [methodes-quantitatives.md](methodes-quantitatives.md).

## Séries temporelles : baselines exécutables

Partir de `assets/timeseries-template.json`, dont les observations sont volontairement vides. Renseigner `metric`, `unit`, `source`, `frequency` (`day`, `week`, `month`), `horizon`, `holdout` et les observations `date/value`.

Les valeurs d'entrée sont non négatives. Dates ISO, ordonnées, uniques et régulières ; une observation mensuelle utilise le premier jour du mois. Les trous ne deviennent pas zéro. Vérifier auparavant changements de définition, retours, périodes incomplètes, ruptures et comparabilité.

```powershell
python <workspace>/.agents/skills/media-buying-business-diagnosis/scripts/demand_tools.py timeseries --input CHEMIN_JSON_CLIENT --out NOUVEAU_DOSSIER_CLIENT
```

L'outil compare naïf et dérive, plus naïf saisonnier si `seasonal_period` est fourni et si l'entraînement initial comprend deux saisons complètes. Minimum technique : quatre observations, au moins trois points avant le holdout ; ce minimum ne constitue pas une validation statistique. Validation en fenêtres croissantes à un pas, sans utiliser l'observation test pour ajuster sa prévision. Choix par MAE minimum ; égalité : naïf puis dérive. RMSE et nombre de points test conservés.

Un horizon jusqu'à 60 périodes est accepté par l'outil ; il doit être pertinent métier. La précision à un pas ne valide pas tous les horizons futurs. Pas d'intervalle probabiliste inventé, ni d'effet causal des dépenses publicitaires. Une prévision négative est conservée avec `requires_review`, pas tronquée silencieusement. Sorties JSON, SVG et HTML ; la partie prévue est distincte de l'observé.

Les modèles de régression multivariée du cours ne sont **pas ajustés par ce script**. Leur protocole de données, estimation, diagnostics et validation est décrit dans `methodes-quantitatives.md` ; utiliser un outil statistique disponible et validé lorsque les données justifient un ajustement. Les coefficients de l'exemple pédagogique ne remplacent jamais cette estimation.
