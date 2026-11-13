# Modèle financier, snapshot et prévisions conditionnelles

## Reprendre les trois parties du cours

**Cost Analysis :** stock en unités, coût unitaire COGS, transport, taux d'échec/retour/cancellation et leur base, overhead et période, prix et UPO. Calculer coûts, contribution avant acquisition et seuils sur le même événement. Les cellules jaunes sont les entrées et les blanches les formules dans les captures du cours ; cette convention ne prouve ni une protection du fichier ni une autorisation d'éditer un autre classeur. Les formules originales n'ont pas été inspectées.

**Profitability Analysis :** AOV net et acquisition cible, résultat par commande et résultat total sur un volume/horizon réalisable. `AOV = prix × UPO` suppose panier homogène ; `target CPS = AOV / target ROAS` suppose même revenu, événement, attribution et période. Quand un ROAS de plateforme porte sur commandes créées mais les coûts sur ventes conservées, reconstruire un pont de statuts avant comparaison.

**Discount Modeling :** varier remise, prix, UPO et hypothèses d'acquisition/réponse explicitement. Tenir le CVR et le volume constants donne une comparaison mécanique, pas une prévision d'augmentation de demande. Une remise peut augmenter le volume et néanmoins diminuer le résultat. Présenter le coût marginal de la pièce ajoutée sans lui attribuer tous les frais de l'ordre ni oublier le coût complet de l'horizon.

Pour un nombre `N` de commandes, revenu net `R`, coûts hors publicité `C`, budget média `A` : résultat du périmètre `R−C−A`. Le plafond média de break-even est `R−C`, positif seulement ; CPS plafond = ce montant / nombre d'événements défini ; ROAS reconnu minimum = `R/(R−C)`. Un ROAS supérieur ou un CPS inférieur est favorable **si toutes les autres hypothèses et bases restent identiques**. Pour contribution nulle/négative, ne pas afficher un seuil publicitaire positif. Un objectif de profit réduit le budget admissible : ne pas confondre break-even et cible.

Allouer overhead / nombre d'ordres demande un volume et un horizon ; si ce volume dépend du budget/prix, rendre l'hypothèse explicite ou réconcilier au niveau période. Ne pas faire disparaître les charges fixes quand le volume est nul. Pour le stock, les unités conservées/vendues et irrécupérables consomment le stock ; les retours récupérables peuvent être revendus selon délai et capacité. Achat du stock, résultat comptable et besoin de trésorerie sont distincts. `profit/order × stock` n'est valide que si une pièce = un ordre réalisé, et si les coûts/période sont cohérents.

## Calculateur fourni

Outil local déterministe, Python standard, sans réseau. Commande (chemins de sortie déjà autorisés, dossier parent existant) :

```powershell
python -B <workspace>/.agents/skills/media-buying-monetization/scripts/monetization_tools.py --input scenario.json --output resultat.json
```

Sans `--input`, lire JSON sur stdin ; sans `--output`, écrire stdout. `--html graphique.html` ajoute un graphique autonome **pour forecast seulement**. Une entrée manquante, booléenne à la place d'un nombre, non finie, hors bornes ou incompatible produit un message d'erreur et code 2, sans conversion implicite. Rates en fractions `[0,1]`, jamais 15 pour 15 %. Calculs en précision flottante sans arrondi intermédiaire ; arrondir pour l'affichage seulement. Les comptages fractionnaires sont des espérances de scénario, pas des commandes physiques.

`context` obligatoire pour `order_model` et `forecast` : textes `currency`, `period`, `source`, `cost_scope` et liste explicite `excluded_costs` (vide si vraiment aucune exclusion). Date, version, source et statut des hypothèses peuvent être détaillés dans le livrable ; le calculateur ne vérifie pas leur vérité. Il ne convertit ni monnaie ni fiscalité. Une donnée absente ne doit pas devenir zéro pour satisfaire le schéma : demander/estimer de façon explicite, ou calculer partiellement hors de cet outil.

### Mode order_model — flux d'une période

Champs numériques **tous requis**, zéros seulement s'ils correspondent à une hypothèse/documentation explicite :

| Champs | Base et sens |
| --- | --- |
| `placed_orders`, `price_unit`, `upo` | Ordres créés attendus, prix net unitaire homogène, unités/ordre. UPO > 0. |
| `cancel_rate_of_placed` | Annulations avant départ / créées. |
| `fail_rate_of_shipped` | Refus/échec final de livraison retournés / expédiées après annulations. |
| `post_return_rate_of_delivered` | Retours remboursés après livraison / livrées. |
| `damaged_fraction_of_return_units` | Fraction irrécupérable des unités de tous les retours (échecs + après livraison). |
| `other_damaged_units` | Unités irrécupérables hors flux de retour, non déjà inclues dans les COGS/pertes. |
| `cogs_unit` | Coût de l'unité vendue ou perdue ; ne pas incorporer les frais séparés ci-dessous. |
| `forward_shipping_per_shipped`, `packaging_per_shipped` | Coûts par ordre expédié, y compris ceux qui échouent ensuite. |
| `reverse_shipping_per_return`, `handling_per_return` | Coûts moyens par retour, refus inclus. Si contrats différents, fournir une moyenne pondérée documentée ou un calcul distinct. |
| `payment_fee_per_retained` | Partie fixe des frais par ordre conservé. |
| `payment_fee_rate_of_product_revenue` | Taux de commission sur le revenu produit net conservé (hors port), fraction `[0,1]`, explicite même si zéro. Cette partie est recalculée avec le prix remisé. Les frais non remboursables sur commandes livrées puis retournées, ou commissions prélevées sur un autre revenu/événement, doivent être calculés dans un poste adapté (`other_period_costs` décomposé par scénario), pas supprimés par le statut conservé. |
| `cancellation_fee_per_cancelled` | Frais par annulation pré-départ effectivement applicable. |
| `shipping_revenue_per_retained` | Frais de port facturés et conservés par ordre retenu. |
| `ad_spend`, `other_marketing_period`, `overhead_period`, `other_period_costs` | Montants de la même période, sans média dans les trois autres champs. Détailler la décomposition hors outil. |

Optionnels : `discount_rates` liste fractions, `target_roas` > 0, `stock_units` et `capacity_orders` ≥ 0. La capacité est en **expéditions par période**, le stock borne les unités consommées à terme. Ce contrôle ne prouve pas la possibilité d'expédier simultanément, le recyclage à temps des retours, la trésorerie ou le financement initial. Une ligne infaisable reste de l'arithmétique non applicable, pas une recommandation.

Flux : créées → annulées ou expédiées → échecs ou livrées → retours après livraison ou conservées. Tous les échecs et retours post-livraison annulent intégralement leur revenu produit et de port dans ce modèle ; les unités retournées sont récupérables sauf fraction de dommage explicite. Il ne représente pas remboursements partiels, échanges, retenues de frais ou différentes compositions de panier : pour ces cas, décomposer les flux ou utiliser un modèle adapté. Le coût COGS = unités conservées + unités irrécupérables, pas tout le stock acheté.

Sorties : comptages, succès livraison et conservation (deux bases explicites), revenu reconnu, ledger hors média, coût total, résultat du périmètre total/par conservée, AOV produits et avec port, CPS média créé/conservé, ROAS reconnu et plafonds break-even sur les mêmes bases. Le `target_roas` donne le budget et CPS compatibles **à flux maintenu**, sans prédire la réponse des ventes à ce budget. Discounts gardent flux, UPO et paramètres de coût inchangés, mais recalculent les commissions proportionnelles au revenu produit conservé. D'autres coûts liés au prix (commission sur port, remboursement partiel, taxes) demandent des scénarios séparés ou un modèle adapté : cette simulation n'est pas automatiquement complète pour eux.

### Mode forecast — les prix/CVR sont fournis, non estimés

Sous-modèle partiel autorisé : si les charges fixes sont inconnues, nommer explicitement le résultat « avant charges fixes inconnues » et les déclarer omises dans `context.cost_scope` et `context.excluded_costs`. Dans ce seul périmètre volontairement partiel, `period_fixed_costs=0` signifie aucune charge fixe imputée au sous-modèle ; ce n’est pas une estimation des charges fixes réelles à zéro, ni un net profit complet. Sinon, conserver le rejet du champ manquant ou calculer partiellement hors outil.

Champs requis : `context`, `ad_budget` ≥ 0, `cpc` > 0, `non_ad_cost_per_order` ≥ 0, `period_fixed_costs` ≥ 0, `upo` > 0 ; `conversion_event` = `retained_order` ou `sale_in_simplified_model` ; `scenarios` = liste non vide d'objets avec `id` unique, `price_unit` ≥ 0 et `cvr` en `[0,1]`. Si CVR mesure les ordres créés avec échecs/retours, utiliser `order_model` ou adapter le flux ; ne pas le traiter comme CVR de ventes conservées.

Formules : clics = budget/CPC ; ordres = clics×CVR ; unités = ordres×UPO ; revenu = prix×unités ; CPS = CPC/CVR ; résultat du périmètre = revenu − coût hors média par ordre×ordres − charges fixes période − budget. CVR zéro : zéro revenu/ordre, CPS et résultat par ordre indéfinis (`null`), perte du budget et des charges fixes maintenue. CPC zéro est refusé : budget positif / clics gratuits n'est pas une prévision définie par ce schéma.

`non_ad_cost_per_order` doit exclure budget média et `period_fixed_costs` ; indiquer ce qu'il inclut, notamment retours/frais si pertinents. Coût marginal d'une pièce additionnelle seul ne suffit généralement pas. L'exemple de cours à 120 est une hypothèse de coût simplifié, pas une preuve que toutes les charges sont incluses. `break_even_cps_before_period_fixed_costs` exclut explicitement ces dernières ; le résultat total, lui, les déduit.

Optionnels : `stock_units`, `capacity_orders` bornent unités et ordres. Les dépassements sont signalés, non écrêtés silencieusement ; seuls les points faisables sont classés. Pour simuler un budget plafonné ou un arrêt pour rupture, établir séparément le budget réellement dépensable et les effets temporels. Le classement donne tous les ex æquo par revenu, ordres et résultat. Tous les résultats négatifs = au mieux moindre perte, pas un prix profitable. Le meilleur parmi les points fournis n'établit pas un optimum continu/causal. Le chart garde deux libellés distincts Revenu / résultat du périmètre et un tableau de nombres.

Exécuter [exemple-forecast.json](exemple-forecast.json) reproduit l'arithmétique de la dernière capture : budget 200 000, CPC 1, coût 120, UPO 1 ; maximum du résultat modélisé 1 200 000 au prix 400 ; revenu 2 100 000 ex æquo aux prix 300 et 350. Il ne reproduit pas les formules inconnues des autres captures et ne démontre pas ces CVR sur un marché.

### Mode competitive — moyenne d'offres comparables

Requis : `own_price` numérique ≥ 0 ; `comparison_basis` avec textes `currency`, `tax_basis`, `unit_basis`, `shipping_basis`, `observation_date` ; `competitors` liste d'objets avec `id`, booléen `comparable`, `price` (nombre ou null) et mêmes champs de base.

La déclaration comparable reflète l'analyse de segment, qualité, positionnement/catégorie et promotion : elle ne se déduit pas de l'égalité des bases. L'outil exclut aussi prix manquants et bases différentes/non renseignées, sans convertir une monnaie ni un prix par unité. Normaliser les sources d'abord. Moyenne simple des prix inclus, écart monétaire et relatif ; moyenne/écart indéfinis si échantillon vide (ou dénominateur zéro pour le relatif). `classification` reste null : aucune règle originale Competitive/Outranked/Outlying n'a été fournie, aucun seuil local n'est inventé. Une segmentation ou pondération justifiée se fait explicitement hors outil.

## Passage du scénario à la décision

Comparer revenu, résultat total, ordres, cash/stock/capacité selon l'objectif réel. Relier toute recommandation à la période, au coût inclus, aux points faisables et à l'incertitude sur CPC/CVR. Le « turning point » du cours est ici le meilleur point testé, susceptible de changer si hypothèses changent. Les assertions de hausse de prix sans baisse importante de CVR demandent des observations/test appropriés ; le calcul seul ne les démontre pas. Aucune campagne, expérience ou modification de prix n'est lancée par ce skill.
