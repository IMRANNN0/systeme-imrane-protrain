# Révision du test vidéo — V2

Demande : critiquer le premier résultat et produire une révision concrète. La V1 reste conservée. La V2 porte sur l'explication arabe de 18 secondes, pas sur la mire technique de découpage.

## Critique appliquée

| Défaut de la V1 | Révision réalisée | Contrôle prévu |
| --- | --- | --- |
| Texte et dessins petits dans un cadre très vide | Typographie Tahoma, chiffres et profils agrandis, titres principaux de 88 à 145 px, texte utile de 48 à 65 px | Images réellement exportées à 360×640 |
| Question incomplète sur la première image | Question et deux moyennes visibles dès l'image 0 | Images 0 et 74 |
| Profils qui disparaissent sans montrer le raisonnement | Les deux mêmes cartes persistent, révèlent leurs filières puis se déplacent et se réduisent vers le schéma des prérequis | Images autour de 75, 210, 225 et 240 |
| Deuxième note verte alors que son profil est orange | Couleur propre à chaque étudiant, conservée jusqu'à la comparaison | Scènes 1 à 3 |
| Même animation de montée pour chaque idée | Transformation des cartes, tracé des connexions puis surlignage progressif des catégories de conditions | Images intermédiaires et code temporel |
| Conclusion qui répète sans donner d'action précise | « راجع شروط التكوين وقارنها بملفك. » visible pendant toute la dernière scène | Images 405 à 539 |
| Quatre sons séparés de la nouvelle action | Piste originale locale alignée aux changements de scènes et aux trois étapes de lecture des conditions | Comparaison du signal source et du son exporté ; écoute encore à faire |

## Temps et vérité du contenu

- Question : images `[0,75)`, 2,5 secondes.
- Différence entre les parcours : `[75,225)`, 5 secondes.
- Comparaison avec les exigences publiées : `[225,405)`, 6 secondes.
- Action avant le choix : `[405,540)`, 4,5 secondes.
- Les cartes partagent une seule horloge de l'image 0 à 404. La transformation commence avant le changement de titre et se termine avant le tracé des connexions.
- Exemple fictif explicitement signalé. Aucun diplôme réel, faux rapport, jugement d'éligibilité, résultat d'admission ou témoignage.
- Le diagramme est une illustration pédagogique. Les deux chemins colorés ne sont pas des validations d'admission.

Source éditable : `video-studio/src/PracticeComparisonV2.tsx`.
Son : `video-studio/scripts/prepare-v2.py`.
Export : `npm run practice:render -- v2`.
Contrôle : `python scripts/verify-v2.py`, depuis le studio.

La direction visuelle reste proposée. Le rendu technique et les images peuvent être vérifiés ici ; la rétention, les conversions et l'approbation de marque ne sont pas établies par cette révision. Pas de voix de Hajj ni de synchronisation en darija dans cet exercice.


## Vérification finale

Export réellement produit : 1080×1920, H264, 30 images/s, 540 images décodées, 18 secondes de vidéo. Décodage intégral FFmpeg réussi. Dix-neuf images de sortie ont été contrôlées à 360×640, avec des paires autour des transitions. Arabe lié, cartes compactes non coupées, identités conservées et action finale lisible pendant 4,5 secondes. Contrôle indépendant `/root/editing_v2_review` sans défaut bloquant.

Audio AAC présent. Corrélation avec la piste originale : 0,9994879 ; crête : 0,13984. Écoute encore à faire. La durée de conteneur comporte un petit prolongement AAC d'environ 5 ms ; la vidéo reste exactement à 540 images.

Limites restantes : bandeau d'exemple petit à l'échelle du téléphone, catégories de conditions génériques, perception du mouvement à vitesse réelle et écoute non vérifiées. Ces limites ne constituent pas une preuve d'efficacité publicitaire. La prochaine version client a besoin d'une formation avec exigences réellement sourcées, d'assets de marque et de la voix réelle.

Les premières tentatives de rendu d'images ont rencontré des délais de lancement/chargement du navigateur sous forte pression mémoire (207 Mio libres observés). Après arrêt de la prévisualisation locale et délai de chargement porté à 120 secondes, l'export complet a réussi. Les images finales viennent du MP4 décodé, pas de ces tentatives échouées. Le serveur Studio est arrêté ; `npm run studio` permet de le rouvrir.

Preuve persistante : `verification/editing-revision-v2.json`. La V1 et le test technique de découpage n'ont pas été écrasés.
