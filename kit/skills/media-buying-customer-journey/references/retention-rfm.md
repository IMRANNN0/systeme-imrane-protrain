# Retention — Satisfaction, personnalisation et développement pertinent

Partir de la cohérence entre promesse, compréhension, valeur délivrée et expérience vécue. L'achat antérieur apporte un historique, mais ne garantit ni confiance actuelle, satisfaction, facilité de revente ni coût inférieur. Une correction de service et la résolution d'une demande ouverte peuvent être prioritaires avant une nouvelle offre. Le cours ne demande pas une perfection imaginaire ; il souligne la qualité de résolution des problèmes, dont il faut connaître les conditions et la capacité réelles.

La relation peut soutenir une valeur à long terme, mais distinguer **revenu historique**, revenue LTV estimée et contribution/profit LTV. Le prix 200 et l'acquisition 50 de l'exemple ne renseignent pas tous les coûts ni achats futurs. Email, SMS ou retargeting ne sont pas gratuits par définition ; leurs coûts, pertinence et autorisations doivent être établis. Le renvoi à Monetization sert seulement à une analyse économique réellement demandée.

## Personalization avec les données réellement disponibles

Le cours cite produits achetés, dates, montant, catégories, price range et zone. Ne retenir que les champs effectivement fournis, fiables et utiles. Un panier ne prouve pas une préférence durable ; un montant ne démontre pas revenu ou capacité à payer. Une géographie manquante n'est pas connue. Éviter une personnalisation plus précise que les données ne l'autorisent.

La possession de first-party data ne vaut pas autorisation d'exporter, enrichir, rapprocher ou transmettre des listes, de créer une audience ou d'envoyer des messages. Dans l'analyse, utiliser seulement le périmètre autorisé et le minimum de données utile ; pseudonymiser les exemples, ne pas copier de vrais fichiers client dans la gouvernance. Séparer recommandation de segment, données nécessaires et action de contact effectivement autorisée.

## RFM : fixer les définitions avant de compter

RFM décrit un historique transactionnel ; il ne mesure directement ni satisfaction, attachement, revenu personnel ou probabilité de rachat. Les paramètres ne sont pas fournis par le cours : les convenir ou décrire le calcul possible sans inventer de barème.

Établir : date de coupure et fuseau, historique accessible pour R, fenêtre de F/M et bornes inclusives/exclusives, devise et base de montant, statut des commandes admissibles, règle de retour/remboursement, identité client et dédoublonnage des commandes. Un événement technique répété ne devient pas une nouvelle commande. Exclure les transactions futures au cutoff et ne pas substituer la date d'aujourd'hui à celle d'un audit historique.

| Dimension | Définition à appliquer au périmètre convenu | Limite |
| --- | --- | --- |
| Recency | Temps, souvent jours calendaires, entre cutoff et dernier achat admissible connu avant ce cutoff | Préciser si la recherche porte sur tout l'historique accessible ou seulement une fenêtre. Sans date fiable, R reste inconnu. |
| Frequency | Nombre de commandes admissibles distinctes du client dans la fenêtre définie | Ce n'est ni quantité d'unités, ni nombre de lignes, ni compteur d'événements `purchase`. |
| Monetary Value | Somme des montants nets admissibles dans cette fenêtre, selon règle explicite sur taxes, port, remises et remboursements | Ce n'est pas l'AOV, le profit ou une lifetime complète. Ne pas additionner des devises sans conversion documentée. |

R peut utiliser un historique plus long que F/M : le déclarer, sans faire passer ces bases pour identiques. Aucun achat admissible **dans la fenêtre** n'est pas aucun achat **jamais**. Zéro F/M peut être valide avec historique complet de la fenêtre et règle explicite ; données tronquées, statut ou montant manquant ne deviennent pas zéro. Un client sans achat admissible connu ne reçoit pas une date de dernier achat inventée. La règle des remboursements partiels/totaux et des achats antérieurs à la fenêtre remboursés pendant celle-ci doit être explicitée avant calcul ; sinon signaler le cas non résolu plutôt que le trancher silencieusement.

Des groupes descriptifs peuvent répondre à une règle métier fournie — par exemple une fenêtre de récence réellement choisie. Ne pas créer par défaut notes 1–5, quintiles, poids, seuil VIP ou « perdu après six mois ». Présenter valeurs, couverture, règles et limites avant labels. Si les règles ou données sont insuffisantes, poser les précisions ciblées ; aucune affectation arbitraire de segment n'est nécessaire pour terminer une carte de parcours.

## Upselling, sens du cours et distinctions utiles

Le cours regroupe sous Upselling la hausse de fréquence et de valeur. Pour choisir la réponse juste, distinguer localement : **upsell** vers une version/panier supérieur, **cross-sell** d'un complément pertinent, **réachat** au rythme d'usage et **win-back** après inactivité contextualisée. Aucun de ces effets n'est acquis par sa recommandation.

Relier l'offre aux besoins et préférences étayés, à son utilité réelle, à la contribution et aux moyens disponibles. Plus de fréquence ou de chiffre d'affaires n'est pas automatiquement plus de profit. Un achat ponctuel n'appelle pas un renouvellement inutile, et une absence de réachat ou de réponse n'est pas automatiquement du churn. Une personne déjà cliente peut retourner en Consideration pour un autre besoin.

Proposer seulement les opportunités et validations pertinentes ; aucun abonnement, option payante, contact, remise, facture ou campagne de réactivation n'est exécuté. Une plainte ouverte ne devient pas une opportunité de pression commerciale. Le plan distingue résolution, service courant, offre proposée et changement réellement accepté.
