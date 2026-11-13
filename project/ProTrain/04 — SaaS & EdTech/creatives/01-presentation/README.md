# ProTrain — Carousel de présentation de l’agence

Production locale du 25 octobre 2026. Proposition de quatre visuels, sans publication, modification des profils, campagne ou dépense.

## Livrables

| Fichier | Usage |
| --- | --- |
| `slide-01.png` à `slide-04.png` | Visuels de production, 1080 × 1350 px, PNG, ratio 4:5 |
| `slide-01.svg` à `slide-04.svg` | Sources éditables et autonomes : textes, formes, polices et images embarqués |
| `contact-sheet.png` | Planche 2 × 2, miniatures de 540 × 675 px, gouttières de 28 px ; total 1164 × 1434 px |
| `preview.html` | Prévisualisation locale responsive avec accès aux sources et à la caption |
| `caption.txt` | Caption Darija/French et URL de contact existante |
| `build.mjs` | Script reproductible de composition SVG et d’export PNG |
| `validation.json` | Dimensions et formats contrôlés automatiquement |

## Contenu et destination

1. Étudier à l’étranger, ça se prépare : orientation, candidatures, visa étudiant ; image de campus contextualisée.
2. Un projet. Des étapes claires : trois composantes de l’accompagnement ; décisions d’admission et de visa attribuées aux établissements et autorités compétentes.
3. À Guéliz. Et en ligne : accueil des étudiants et parents, Rue Ibn Aïcha, Marrakech, et échanges en ligne.
4. Parlons de votre projet : demande → rappel du conseiller → organisation de la consultation. Conditions confirmées avant réservation.

CTA réel : https://protraincompany.com/contactus . Ce formulaire demande un premier échange ; il ne confirme pas instantanément un rendez-vous. Le carousel présente l’agence. Aucun tarif de consultation ou offre Match n’y est ajouté.

## Sources et ressources

- Base éditoriale locale : `../../PACK_TRUST_PAGE.md`, `../../AUDIT_PRESENCE_DIGITALE.md`.
- Site public de référence : https://protraincompany.com/ . Services : https://protraincompany.com/services . Parcours et limites : https://protraincompany.com/comment-ca-marche . Coordonnées et demande : https://protraincompany.com/contactus . Le texte reprend l'audit du 25 octobre 2026 ; le HTML public et les deux ressources ci-dessous ont été récupérés pour cette production.
- `assets/protrain-logo.png` : logo officiel, 128 × 121 px, transparent, téléchargé depuis https://protraincompany.com/web/image/website/1/logo/0x128/ProTrain?unique=0d03712 . Présentation à 102 × 97 px ; original conservé.
- `assets/site-campus.webp` : photo de campus, 1600 × 1067 px, téléchargée depuis https://protraincompany.com/website_protrain/static/src/img/hero-students.webp .

La photo est réutilisée comme contexte de campus, avec libellé explicite sur la slide 1. Les personnes ne sont pas présentées comme équipe, clients ou étudiants confirmés de ProTrain. Aucune authenticité de témoignage, identité ou relation commerciale n’est déduite de cette image. Aucune personne générée, retouchée ou remplacée.

Le WebP original est converti en PNG en mémoire pour son embarquement, car le moteur de rendu de cet environnement n’affichait pas le WebP embarqué. Le cadrage de mise en page coupe des éléments de décor et le bas de l’image ; tous les visages sont conservés. Aucun filtre ou traitement des sujets. Les deux ressources originales sont intactes.

## Direction et spécifications

Direction éditoriale éducation : titres francs, sections numérotées, règles fines, composition variable et motif discret de parcours. Pas de gradient, de cartes décoratives, de témoignage ou de statistique inventés.

- Vert forêt `#0C4935`, crème `#F5F2E9`, ambre `#E8AF43` réservé aux accents et aux petits titres sur fond vert.
- Titres Bahnschrift, corps Arial ; polices locales embarquées dans chaque SVG. Les textes restent éditables. Une application qui ignore les polices embarquées peut produire un rendu différent : les PNG constituent les exports de référence.
- Titres principaux de 84 à 104 px ; corps principalement de 36 à 44 px ; mentions de décision à 32 px ; footer et labels à 25 px.
- Marges de composition de 80 px ; aucune animation, ombre ou arrondi décoratif.
- Contraste calculé des couleurs : forêt/crème ≈ 9,29:1 ; ambre/forêt ≈ 5,27:1. L’ambre ne porte aucun petit texte sur crème.
- Taille 1080 × 1350 px choisie pour cette production, sans revendication de spécification obligatoire d’une plateforme.

## Reconstruction

Dans ce dossier, exécuter en PowerShell :

```powershell
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' '.\build.mjs'
```

Le script utilise le module Sharp local, sans installation ni réseau, et les polices Windows `bahnschrift.ttf` et `arial.ttf`. Il réécrit uniquement ses livrables dans ce dossier, jamais les deux ressources originales.

## Revue de production

- Quatre PNG et quatre SVG réellement exportés ; dimensions PNG vérifiées automatiquement.
- Planche complète et slide 1 finale inspectées visuellement : photo présente, visages visibles, titres et corps lisibles, aucun chevauchement ou texte coupé observé.
- Cohérence factuelle relue : agence préservée, CTA existant, absence de garantie, aucune confusion avec le prix ou la disponibilité de Match.
- Revue de style interne, subjective : AI Slop Score 1/10 ; Distinctiveness Score 8/10. Ces appréciations portent uniquement sur le design, sans mesure d’efficacité publicitaire ni score de confiance.

Limites matérielles : logo de faible définition utilisé à petite taille ; photo de contexte plutôt qu’une photo du vrai bureau ou de l’équipe. Ces dernières pourront compléter un prochain contenu si des ressources réelles sont fournies. Aucun compte ni contenu externe n’a été modifié.
