---
name: media-buying-customer-profile
description: "Construire ou actualiser un Customer Profile par segment et situation d'achat : Jobs, Pains, Gains, priorités et preuves. Utiliser pour approfondir besoins, envies, peurs et motivations ; la collecte générale relève de l'intake, la demande du diagnostic, la Value Map d'une étape distincte."
---

# Customer Profile

Transformer les informations disponibles en compréhension sourcée de ce que le client cherche à accomplir, de ses difficultés et de ses résultats souhaités. L'âge, le genre et la ville peuvent éclairer des contraintes ; ils ne suffisent pas à décrire un client. Explorer besoins, envies, peurs, motivations, aspirations et comportements dans leur contexte, sans inventer une biographie.

Customer Profile, Value Map et Feature-Benefit Laddering sont trois frameworks distincts de l'étape Value Creation. Ce skill réalise uniquement Customer Profile. Il ne constitue ni un orchestrateur, ni une preuve de demande ou de ventes, ni une production publicitaire.

## Définir le périmètre et partir des sources

Pour un client réel, résoudre sa lane dans `<workspace>/.codex/projects.json` par le chemin enregistré le plus long, puis lire ses consignes et son contexte minimal. Pour un exercice fictif sans client réel, utiliser uniquement le cas et l'espace temporaire autorisés ; ne pas résoudre une lane métier ni ouvrir un client homonyme. Préciser segment, marché/zone, offre ou idée et situation d'achat/d'usage. Utiliser seulement les sources autorisées de cette lane ; ne jamais agréger les clients. Un exercice fictif demandé reste identifié comme tel.

Accepter le brief de [media-buying-client-intake](../media-buying-client-intake/SKILL.md), des sources directes suffisantes ou un diagnostic déjà disponible. Ne pas imposer de nouvel intake. Le [diagnostic de demande](../media-buying-business-diagnosis/SKILL.md) reste une mission distincte.

- **Création à partir de zéro :** commencer par Customer Profile, puis transmettre à Value Map.
- **Produit existant :** partir de l'inventaire Value Map ou des capacités réelles documentées, identifier les segments candidats, puis approfondir leur Customer Profile. Si cet inventaire manque, demander seulement les capacités/valeurs minimales utiles et présenter les segments comme hypothèses provisoires. Ne pas forcer un profil fictif ni inventer un fit.
- **Actualisation :** dater les nouvelles sources, réviser les éléments affectés et conserver les contradictions ouvertes.

Faire un profil par segment ou situation réellement distincte ; ne pas découper uniquement par âge. Préciser acheteur, utilisateur et décideur si ces rôles sont connus et utiles, sans complexité B2B artificielle. Ne pas supposer deux géographies identiques.

## Construire et prioriser Jobs, Pains et Gains

Lire [references/methode.md](references/methode.md) pour les définitions, les axes de priorité et le traitement des preuves. Attribuer des identifiants stables `J1`, `P1`, `G1` pour relier chaque élément à sa source, à sa signification et à ses liens éventuels. Les facettes peuvent coexister ; éviter les doublons et les causalités supposées.

Les Jobs décrivent ce que le client cherche à accomplir ; les Pains distinguent problèmes actuels, obstacles et risques futurs ; les Gains distinguent requis, attendus, désirés et inattendus. Conserver séparément type et priorité. Classer qualitativement l'importance des Jobs d'Insignificant à Important, la sévérité des Pains de Moderate à Extreme et la pertinence des Gains de Nice-to-have à Essential. Donner la base de chaque classement ; une priorité non renseignée reste inconnue. Aucun score, poids, quota de lignes ou confiance chiffrée inventé.

Relier les Jobs/Pains/Gains lorsque les sources ou une hypothèse explicitement étiquetée le permettent. Retenir les quelques priorités utiles quand les éléments disponibles justifient ce choix. Distinguer systématiquement fait vérifié, déclaration client, observation datée, interprétation, hypothèse et inconnu ; une déclaration ne devient pas vérifiée par sa seule présence dans un document. Employer des citations client uniquement si leur texte réel est fourni.

Les recherches et centres d'intérêt sont des indices d'hypothèses, jamais la preuve d'un état de santé, d'anxiété ou d'estime de soi. Ne pas généraliser un trait psychologique à un groupe démographique. La supériorité Broad/Custom est une affirmation du cours à tester dans son contexte, pas une règle établie ni une recommandation de campagne.

Pour illustrer sans données client, lire [references/exemple-mode.md](references/exemple-mode.md). Ne pas transférer cet exemple à un marché réel.

## Livrer et transmettre

Adapter [references/trame-sortie.md](references/trame-sortie.md) au livrable utile : profil sourcé, priorités et leur base, liens, contradictions, inconnues décisives et questions ou tests minimaux. Un plan de validation ne lance aucun contact externe. Éviter de remplir les cases pour donner une impression de complétude.

Terminer par un passage limité : **Job/Pain/Gain prioritaire → valeur existante documentée ou proposée → preuve et écart restant**. Un manque de preuve reste visible ; ne pas compléter automatiquement toute la Value Map. Lire [references/value-map-et-provenance.md](references/value-map-et-provenance.md) seulement pour ce passage, un inventaire existant ou la provenance du cours. Pour poursuivre cette étape distincte lorsqu'elle est demandée, utiliser [media-buying-value-map](../media-buying-value-map/SKILL.md). FBL est seulement nommé comme étape future : sa méthode n'a pas été fournie.

Livrer dans la conversation par défaut. Enregistrer des fichiers uniquement sur demande, à la destination autorisée dans la lane client ; la bibliothèque centrale contient seulement méthode et exemples génériques. Les essais fictifs restent dans le runtime privé de gouvernance. Aucune publication, écriture client, collecte réseau nouvelle, prise de contact ou mutation de campagne n'est autorisée par ce skill. Ne générer ads, hooks, landing pages ou campagnes que sur demande séparée dans le workflow adapté.


## Complément local — 5 novembre 2026

Si le profil utilise motifs CRM, entretiens commerciaux ou performances de contenu, lire [profil et biais de sélection](references/profil-et-biais-crm.md) avant de transformer ces indices en Jobs/Pains/Gains ou en priorités du segment.

Ce complément est une adaptation locale distincte des sources du cours ; il conserve les limites et autorisations du présent skill.
