---
name: media-buying-business-diagnosis
description: "Analyser la demande et la viabilité business avant le media buying, ou actualiser ce diagnostic : Produit, Offre, preuves de demande, économie, élasticité, assessment et prévisions lorsque les données le permettent. Pour préparer un questionnaire client, utiliser media-buying-client-intake."
---

# Analyse de la demande

Conserver le slug historique pour compatibilité. Ce skill analyse ; [media-buying-client-intake](../media-buying-client-intake/SKILL.md) prépare les questions et le brief factuel. Accepter son brief ou directement des sources autorisées suffisantes, sans imposer l’intake. Le Buyer Persona détaillé, les campagnes et l’orchestrateur maître restent hors périmètre.

## Périmètre et sources

Résoudre le client dans `<workspace>/.codex/projects.json` au chemin enregistré le plus long ; lire ses consignes et son contexte minimal. Préciser offre, marché, stade et décision à éclairer. Demander seulement le périmètre manquant avant de lire des données métier. Pour un exercice fictif demandé, le signaler sans charger de client réel.

Utiliser uniquement les sources autorisées de cette lane, sans mélange entre clients ou graphes. Le skill n’autorise ni nouveau corpus réseau, contact externe, publication ou mutation de campagne. Une analyse de site public suit le périmètre demandé et les outils autorisés, sans accès privé ni collecte d’identifiants.

Qualifier déclaration, observation publique avec URL/date, pièce vérifiée et contrôles, hypothèse ou inconnu. Un document reçu ou une promesse affichée ne prouve pas des ventes ou résultats. Conserver date, période, offre, zone, unité, définition et dénominateur ; distinguer mesures, estimations, commandes et ventes réalisées. Expliquer solidité et limites sans confiance chiffrée inventée. Réconcilier les divergences avec le client, sans choisir silencieusement une version.

## Choisir l’analyse utile

Lire [references/methode.md](references/methode.md) pour suivre **Produit → Offre → Demande** et examiner valeur, fonctionnement, conditions réelles, économie, capacité et continuité. Mobiliser les critères pertinents ; une absence de données n’est pas un résultat négatif. Comparer hypothèses de produit et de contexte sans attribuer automatiquement une difficulté aux publicités.

- **Diagnostic qualitatif :** relier constats et signes de besoin, envie, volonté et capacité à payer ; isoler difficultés observées, causes supposées et vérifications prioritaires.
- **Analyse quantitative demandée et possible :** lire [references/methodes-quantitatives.md](references/methodes-quantitatives.md) pour choisir assessment, élasticité, série temporelle ou régression, puis [references/calculs.md](references/calculs.md) pour les schémas et commandes de `scripts/demand_tools.py`. Le script fournit assessment, élasticité et baselines temporelles, sans ajustement OLS. Un calcul descriptif n’établit ni causalité ni prévision validée.
- **Actualisation :** reprendre le diagnostic de la même lane, dater les nouveaux faits et corriger les conclusions affectées. Indiquer les hypothèses confirmées, infirmées ou ouvertes ; conserver les limites valides sans refaire toute la collecte.

Le barème original 1–5 reste manquant. Le [barème local proposé](references/bareme-local.md), demandé par le propriétaire pour revue commune, est **non approuvé pour un usage chiffré client**. Ne pas choisir de notes à partir du récit pour remplir les cases. La formule compatible avec la capture est une reconstruction documentée, sans preuve du barème original.

Les statuts `draft_local` et `screenshot_demo` sont réservés aux démonstrations signalées avec `--demo`. `owner_confirmed` requiert une confirmation réelle du propriétaire sur le barème, les notes/poids explicites, leur sens et les règles de manquants ; ne pas attribuer ce statut soi-même. Les manquants produisent une vue partielle, et aucun poids d’axe ni grade global de viabilité n’est disponible. Aucun coefficient illustratif ne doit produire une prévision client.

## Conclusion traçable

Répondre dans la langue utile, avec un livrable proportionné :

- périmètre et synthèse Produit → Offre → Demande ;
- constats, difficultés, hypothèses et contradictions sourcés ;
- économie, capacité, rétention et continuité documentées ;
- calculs réellement exécutés : données, formules/modèle, statut d’approbation, résultats, couverture, validation et limites ;
- inconnues décisives et vérifications prioritaires avec responsable ;
- éléments pour le futur Buyer Persona : premiers groupes, situations, mots et objections connus, sans profil détaillé inventé.

Ne pas rejeter un produit par défaut faute d’historique ni décider d’une campagne sur ses seuls indicateurs publicitaires. Aucune promesse de croissance ou ROI. Prix, garanties, remboursements et bénéfices doivent être réels ou identifiés comme propositions à tester. Si une collecte manque, préciser les seuls points bloquants et orienter la préparation du questionnaire vers l’intake, sans le recréer ici.

Ce skill utilise la bibliothèque portable de ce workspace. Le [guide canonique](../media-buying-client-intake/resources/GUIDE_ENTRETIEN.md) fournit les conventions de sources ; le [questionnaire canonique](../media-buying-client-intake/resources/QUESTIONNAIRE_CLIENT.md) appartient à l’intake. Ne pas les dupliquer. Enregistrer un fichier seulement si demandé à la destination autorisée dans la lane client ; sinon répondre dans la conversation. Aucune donnée métier à la gouvernance.


## Complément local — 5 novembre 2026

Pour une offre à leads, rendez-vous ou contrats, lire le [complément sur la viabilité des services et les preuves](references/viabilite-service-et-preuves.md) : distinguer maturation CRM, contribution, capacité et événements attribués avant de conclure.

Ce complément est une adaptation locale distincte des sources du cours ; il conserve les limites et autorisations du présent skill.
