# Barème local proposé — à revoir avec le propriétaire

Version de travail du 2026-10-25, rédigée à la demande du propriétaire pour revue commune. **Non approuvé pour noter de vrais clients.** Ce n'est ni le barème original de la formation, ni un modèle prédictif validé. Démonstration possible sous `draft_local` avec `--demo`, clairement étiquetée. La confirmation de production ne se déduit pas de l'autorisation de rédiger ce document.

## Sens des notes, preuves et poids

La note décrit à quel point un facteur favorise l'offre étudiée et son objectif, sur un marché et un horizon explicites. Les ancres 1/3/5 ci-dessous signifient défavorable vérifié / bilan observé mixte / favorable vérifié. Les notes 2 et 4 sont intermédiaires, avec justification. **Inconnu ≠ 1, 0 ou 3** : laisser la note vide. « Non applicable » exige une raison et une exclusion explicite.

Avant de noter, préciser objectif, sens du facteur dans ce contexte, source et date, période et limites. Conserver statut de preuve et confiance séparément de la note : une preuve solide peut montrer un facteur défavorable ; un discours rassurant ne mérite pas 5. Si les éléments sont insuffisants ou contradictoires, conserver l'inconnu ou l'écart à résoudre.

Proposition générale pour l'importance des poids, **sans valeurs par défaut** : 1 marginale, 2 secondaire, 3 matérielle, 4 majeure, 5 décisive pour la décision étudiée. Le propriétaire doit confirmer les poids propres au client avant usage numérique réel. Ne pas compter plusieurs fois un même effet par des facteurs fortement corrélés ; expliquer leurs contributions distinctes ou réduire la redondance avant confirmation.

## Nature du produit — 7 critères

Identifiant d'axe `product_nature` ; identifiants des lignes, dans l'ordre : `expiration`, `essentiality`, `dependency`, `seasonality`, `price_elasticity`, `versatility`, `urgency`.

| Critère | 1 — défavorable vérifié | 3 — bilan mixte observé | 5 — favorable vérifié |
| --- | --- | --- | --- |
| Périssabilité | Durée d'usage ou conservation incompatible avec les délais, avec pertes constatées | Pertes ou contraintes réelles partiellement maîtrisées | Durée et organisation adaptées au cycle réel, qualité et pertes maîtrisées |
| Besoin / essentialité | Problème peu prioritaire pour l'achat étudié d'après les comportements observés | Priorité réelle pour certains usages, arbitrages fréquents | Problème prioritaire et valeur de sa résolution soutenant les achats observés |
| Autonomie / dépendance | Prérequis indisponibles ou obstacles d'adoption bloquant l'usage | Dépendances accessibles mais friction constatée | Prérequis ou complémentarités accessibles et cohérents avec l'adoption observée |
| Saisonnalité | Décalage documenté entre saison de demande et capacité, trésorerie ou objectif | Calendrier connu avec fragilités observées sur certaines périodes | Cycle saisonnier ou régulier exploitable avec capacité et trésorerie adaptées |
| Sensibilité au prix | Réactions au prix incompatibles avec l'économie nécessaire | Arbitrages observés permettant certains prix, avec limites | Réactions documentées compatibles avec prix, valeur et économie visés |
| Polyvalence | Usages annoncés non tenus ou dispersion dégradant la valeur | Plusieurs usages réels, utilité ou coûts variables | Usages pertinents effectivement servis sans dégradation de la promesse |
| Urgence | Moment d'achat mal aligné avec délai et proposition | Situations d'achat connues mais alignement inégal | Moment du besoin et délai de réponse adaptés aux décisions observées |

Un produit périssable, de luxe, spécialisé ou saisonnier n'est pas défavorable par nature. L'essentialité et l'urgence s'apprécient dans le contexte d'achat ; une urgence forte mal servie peut être défavorable. Une spécialisation utile peut rendre la polyvalence sans objet plutôt que mériter une mauvaise note.

## Marché — 3 critères

Identifiant d'axe `market` ; lignes : `competition`, `size`, `supply`.

| Critère | 1 — défavorable vérifié | 3 — bilan mixte observé | 5 — favorable vérifié |
| --- | --- | --- | --- |
| Concurrence | Alternatives et conditions concurrentielles rendent la position actuelle difficilement soutenable | Demande et espace de différenciation observés, avec contraintes réelles | Position défendable étayée face aux alternatives et économie compatible |
| Taille du marché | Marché accessible documenté insuffisant pour l'objectif déclaré | Espace accessible réel mais marge de développement limitée | Marché accessible documenté compatible avec l'objectif et les capacités |
| Offre disponible / Supply | Disponibilité ou approvisionnement bloque régulièrement la promesse | Disponibilité variable avec solutions partielles observées | Approvisionnement ou capacité de prestation fiable pour le volume considéré |

Une concurrence forte peut aussi signaler une demande existante ; une absence de concurrent ne prouve pas une opportunité. « Supply » doit être défini pour ce cas (offre sur le marché, disponibilité ou approvisionnement), puis conservé avec ce sens ; ne pas confondre ces dimensions ni leur affecter une note unique ambiguë.

## Consommateur — 3 critères

Identifiant d'axe `consumer` ; lignes : `preferences`, `expectations`, `loyalty`.

| Critère | 1 — défavorable vérifié | 3 — bilan mixte observé | 5 — favorable vérifié |
| --- | --- | --- | --- |
| Préférences | Choix observés défavorables à l'offre pour les usages ciblés | Préférences partagées selon les situations documentées | Préférences et comportements d'achat favorables étayés |
| Attentes | Écart récurrent entre attentes et prestation réellement délivrée | Attentes satisfaites sur certains points, écarts persistants sur d'autres | Attentes ciblées satisfaites avec preuves d'usage et limites claires |
| Fidélité | Départs ou absence de renouvellement incompatibles avec le modèle qui en dépend | Rétention mesurée avec forces et fragilités économiques | Rétention observée compatible avec la valeur délivrée et l'économie du modèle |

La fidélité peut être sans objet pour un achat ponctuel. Ne pas la remplacer par des réachats espérés ni assimiler satisfaction déclarée et rétention mesurée.

## Économie — 4 critères

Identifiant d'axe `economic_conditions` ; lignes : `purchase_power`, `economic_cycle`, `income_distribution`, `inflation`.

| Critère | 1 — défavorable vérifié | 3 — bilan mixte observé | 5 — favorable vérifié |
| --- | --- | --- | --- |
| Pouvoir d'achat | Capacité à payer incompatible avec le prix dans les situations documentées | Paiement possible pour certains cas, arbitrages ou contraintes observés | Capacité et volonté de payer étayées dans le marché accessible ciblé |
| Cycle économique | Cycle documenté défavorable à la demande et à l'économie de cette offre | Effets contrastés ou vulnérabilités compensées partiellement | Offre et économie adaptées au cycle documenté sur l'horizon étudié |
| Répartition des revenus | Distribution pertinente et accès au segment rendent l'objectif peu soutenable | Segment solvable identifié mais accès ou profondeur contraints | Segment accessible et solvable documenté, compatible avec l'objectif |
| Inflation | Coûts ou prix réels évoluent de façon incompatible avec la marge et le paiement | Ajustements possibles mais tensions de coûts ou demande observées | Adaptations de coûts, prix et trésorerie soutenables et documentées |

Ces directions dépendent de l'offre, de la zone et de l'horizon ; inflation, concentration de revenus ou cycle ne sont pas automatiquement bons ou mauvais. Ne pas attribuer de pouvoir d'achat à une personne d'après son seul groupe démographique.

## Revue avant adoption

Revoir avec le propriétaire la pertinence des 17 critères, le sens de Supply, les ancres et l'objectif, l'échelle, les poids, les exclusions et le traitement des manquants. La formule et le radar sont expliqués dans [methodes-quantitatives.md](methodes-quantitatives.md), leur interface dans [calculs.md](calculs.md). Ne pas fixer de coupure GO/STOP ni de probabilité de réussite. Aucun grade global sans règle d'agrégation explicitement fournie et approuvée.
