---
name: media-buying-client-intake
description: "Préparer et adapter un questionnaire client avant le media buying, puis structurer les réponses, observations de site et notes d'entretien en brief factuel sourcé. Utiliser pour la collecte et les clarifications ; le diagnostic stratégique de demande relève de media-buying-business-diagnosis."
---

# Questionnaire et brief client

Préparer la collecte utile à ce client, puis un brief exploitable. Garder l'ordre **Produit → Offre → Demande** sans rendre le questionnaire identique pour tous. Ce skill ne produit ni verdict stratégique, score, prévision, Buyer Persona détaillé ou décision de campagne.

## Périmètre et ressources

Résoudre le client dans `<workspace>/.codex/projects.json` au chemin enregistré le plus long et lire ses consignes et son contexte minimal. Préciser une offre, une zone, le stade et l'objectif du rendez-vous. Demander uniquement le périmètre manquant avant de lire des données métier. Un exercice fictif reste identifié comme tel, sans charger de client réel.

Lire le modèle utile au livrable :

- [QUESTIONNAIRE_CLIENT.md](resources/QUESTIONNAIRE_CLIENT.md) pour choisir et reformuler les questions ;
- [GUIDE_ENTRETIEN.md](resources/GUIDE_ENTRETIEN.md) pour l'adaptation et le traitement des sources ;
- [references/brief.md](references/brief.md) pour structurer le brief et son passage à l'analyse.

Ces ressources restent canoniques à ces chemins ; ce skill est local au workspace et ne les duplique pas. Les passages analytiques du guide servent au skill d'analyse, sans élargir ici la mission de collecte.

Utiliser seulement les sources autorisées de cette lane, sans document, donnée personnelle, réponse ou graphe d'un autre client. Aucun accès privé ni collecte d'identifiants. Le skill ne donne aucune permission de contact externe, publication, nouveau corpus réseau ou action de campagne. Consulter un site public seulement dans le périmètre demandé avec les outils autorisés.

## Adapter la collecte

Partir des informations déjà disponibles. Sélectionner les questions utiles ; aucun quota fixe ni obligation d'envoyer les 18 questions du modèle. Ne pas redemander un fait clairement établi ; confirmer seulement les éléments anciens, contradictoires ou ambigus. Une donnée absente reste inconnue.

Adapter vocabulaire et champs au produit ou service, à l'offre, au marché et à la devise réels. Pour un service, explorer temps, équipe et capacité d'exécution plutôt que stock et expédition. Pour un lancement, demander tests et signaux disponibles sans exiger ventes ou rétention historiques. Distinguer achat ponctuel et récurrent. En B2B, préciser les fonctions intervenant dans l'achat, étapes et délais connus, sans construire le Buyer Persona. Ne pas inventer de détail métier pour compléter un modèle.

Recueillir problème, alternatives, bénéfices et preuves ; capacité et coûts connus ; inclusions/exclusions, prix et conditions actuelles ; puis faits de demande, réactions au prix, saisonnalité et suites d'achat si suivies. Les données sensibles peuvent rester facultatives, en fourchettes ou à l'oral. Ne demander ni auto-évaluation du client ni note 1–5 : ce skill ne score pas.

Pendant l'entretien, clarifier périodes, unités et définitions. Séparer déclaration client, observation avec URL/date, pièce vérifiée et contrôles effectués, hypothèse et inconnu. Un document reçu n'est pas automatiquement vérifié ; une page affichée ne prouve ni ventes ni résultats. Présenter les divergences à résoudre, sans inventer de politique d'achat ni choisir arbitrairement une version.

## Livrables et passage à l'analyse

Pour un questionnaire, livrer les questions adaptées dans la langue utile au client, avec champs de réponse et possibilité d'indiquer « inconnu » ou « non applicable ». Garder les notes privées séparées. Si des réponses existent, produire ou actualiser le brief sans imposer un nouvel intake complet.

Le brief conserve périmètre, faits Produit/Offre/Demande sourcés et datés, définitions chiffrées, divergences, inconnues et clarifications restantes. Il décrit, sans verdict sur viabilité, taille de marché ou ROI.

Pour un diagnostic demandé, passer ce brief à [media-buying-business-diagnosis](../media-buying-business-diagnosis/SKILL.md) ; ne pas exécuter l'analyse dans l'intake ni envoyer de message à un autre agent. Aucun orchestrateur maître. Enregistrer un fichier seulement si demandé, dans la destination autorisée de la lane client ; sinon livrer dans la conversation, jamais dans les documents métier de gouvernance.


## Complément local — 5 novembre 2026

Quand la collecte porte sur un service ou un parcours à leads, utiliser les [questions ciblées service/CRM et preuves](references/collecte-service-crm.md) seulement pour les inconnues utiles au brief ; les statuts commerciaux ne sont ni des ventes ni des diagnostics.

Ce complément est une adaptation locale distincte des sources du cours ; il conserve les limites et autorisations du présent skill.
