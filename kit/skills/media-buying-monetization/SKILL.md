---
name: media-buying-monetization
description: "Analyser la rentabilité et concevoir le pricing : coûts, marges, objectifs, scénarios financiers, comparaison de prix et prévisions conditionnelles. Utiliser pour Monetization avant ou pendant le media buying ; le diagnostic de demande et la rédaction publicitaire restent distincts."
---

# Monetization

Relier l'objectif du business à une économie documentée et à des scénarios de prix comparables. Le résultat est une décision conditionnelle avec hypothèses visibles, pas une garantie de profit ni un ordre de modifier les prix ou les campagnes. Ce chapitre du propriétaire est distinct de Feature-Benefit Laddering, dont la méthode n'a pas été fournie.

## Délimiter l'analyse

Pour un client réel, résoudre sa lane via `<workspace>/.codex/projects.json`, lire ses consignes et le contexte minimal, puis utiliser uniquement ses sources autorisées. Pour un exercice fictif, rester dans le cas et la destination temporaire autorisée, sans ouvrir de client homonyme. Livrer dans la conversation par défaut ; un fichier demandé reste à la destination autorisée de la lane. Aucun corpus client dans la bibliothèque partagée.

Réutiliser le brief ou les données disponibles, sans imposer un nouvel intake. Préciser offre/segment, devise, période, objectif, unités et statut des sources : mesure, déclaration, hypothèse ou inconnu. Si seules certaines données manquent, livrer l'analyse partielle utile et poser les questions qui affectent réellement la décision ; ne pas convertir l'inconnu en zéro. Les engagements externes, publication, contacts, changement de prix ou de campagne demandent leur propre autorisation.

## Choisir le travail utile

- **Rentabilité/coûts :** lire [couts-indicateurs.md](references/couts-indicateurs.md). Réconcilier revenus reconnus, coûts et pertes sans double compte ; distinguer marge, markup, LTV et les différents événements d'acquisition.
- **Objectif et pricing :** lire [objectifs-pricing.md](references/objectifs-pricing.md). Comparer les stratégies selon objectif, valeur, concurrence, trésorerie et capacité ; aucune stratégie ni trajectoire de prix universelle.
- **Modèle financier, discount ou forecast :** lire [modele-et-calculateur.md](references/modele-et-calculateur.md), puis utiliser le calculateur stdlib [monetization_tools.py](scripts/monetization_tools.py) lorsqu'un schéma compatible est documentable. Les approximations, exclusions et hypothèses de réponse au prix restent visibles. Adapter un calcul hors de ce schéma plutôt que forcer des données incompatibles.
- **Competitive Snapshot :** même référence, mode `competitive` : comparer seulement les offres et unités normalisées pertinentes. Une moyenne d'échantillon n'est ni le marché complet ni automatiquement le prix perçu par le client. Ne pas inventer les seuils Competitive/Outranked/Outlying.
- **Actualisation :** conserver IDs/sources et période du modèle antérieur ; expliquer ce qui a changé, les contradictions et leur effet. Recalculer les cellules dépendantes, sans toucher silencieusement les hypothèses originales.

## Garder les bons dénominateurs

Définir commande créée, expédiée, livrée, retournée après livraison et conservée/payée. Ne pas mélanger les bases des taux de cancellation, échec, retour et dommage. Des retours récupérables restent du stock, pas automatiquement une deuxième charge COGS. Les dépenses d'acquisition sont comptées une seule fois ; rapprocher les frais d'agence, création et salaires de leur vraie période/base.

Le break-even CPS/CPA est un **plafond de dépense d'acquisition**, le break-even ROAS un **minimum de retour** dans le périmètre défini. Sans contribution positive avant publicité, aucune dépense publicitaire positive ne rend le modèle rentable à conditions inchangées. Distinguer commande et nouveau client : pas de CAC ou de LTV profit calculé sans données adaptées.

Prix × UPO n'est l'AOV que dans un panier homogène au prix indiqué, avec conventions explicites sur remises, taxes et frais. Stock est en unités ; le nombre de commandes réalisables dépend d'UPO, dommages, retours et capacité. Le coût marginal de la pièce supplémentaire ne représente pas toutes les charges de l'ordre ou de la période.

Les résultats d'un scénario sont arithmétiques **si** ses entrées se réalisent. Un CVR fourni n'est pas une élasticité mesurée ni un effet causal prouvé du prix. Le meilleur point parmi les scénarios faisables n'établit pas un optimum continu. Un chiffre de revenu ou de ROAS élevé ne démontre pas seul la rentabilité.

## Livrer et passer à la suite

Adapter [trame-sortie.md](references/trame-sortie.md) à la demande : données/limites, coûts réconciliés, scénarios et métrique de décision, besoins de validation. Pour les références et captures reçues, lire [provenance.md](references/provenance.md) ; aucun fichier image temporaire n'est requis pour exécuter la méthode. Les formules du classeur original n'ont pas été inspectées et ne sont pas prétendues reconstituées.

La collecte générale relève de [client-intake](../media-buying-client-intake/SKILL.md) ; la demande globale de [business-diagnosis](../media-buying-business-diagnosis/SKILL.md) ; les besoins et capacités de [customer-profile](../media-buying-customer-profile/SKILL.md) et [value-map](../media-buying-value-map/SKILL.md). Ne pas exécuter ces missions ni créer des annonces, un site ou un forecast de demande supplémentaire sans besoin réel dans la demande.


## Complément local — 5 novembre 2026

Pour des services, leads, rendez-vous ou contrats, lire [économie des services](references/economie-services.md). Définir contribution, capacité, maturation et plafond d'acquisition sur les mêmes bases ; ne pas forcer ces flux dans le calculateur de commandes physiques.

Ce complément est une adaptation locale distincte des sources du cours ; il conserve les limites et autorisations du présent skill.
