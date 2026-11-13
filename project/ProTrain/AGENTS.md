<!-- portable-protrain-workspace -->
This is the ProTrain-only project payload. After installation, use the containing workspace root instructions and this project's four canonical memories. Historical local paths and verification receipts describe the original host, not proof of setup on this PC. Never execute historical commands without checking the current workspace and destination.

# protrain — lane cliente isolée

Identifiant : `protrain`. Racine : `{{PROTRAIN_PROJECT_ROOT}}`.
Lire le routeur `{{IMRANE_WORKSPACE_ROOT}}/AGENTS.md`, puis CURRENT.md et CONTEXT_INDEX.md
dans `.codex/memory`. Codex et Claude partagent ces règles.

## Mission et choix du contexte

Client protrain : préparer plusieurs business models. Le propriétaire a confirmé quatre lignes ; leurs stacks et commandes de validation restent à qualifier. Choisir explicitement
le business model avant toute lecture de contexte métier ou implémentation.
Les quatre dossiers métier directs sont des composants de protrain,
sans lane autonome tant qu'une qualification et autorisation distinctes manquent.
Lire README.md pour choisir la ligne et son README ; ne pas inventer de modèle.

Cette lane exclut les autres clients et le contexte métier de la lane parent
`clients`. Résoudre le chemin enregistré le plus long. Préserver les changements
des autres agents. Définir des contrôles proportionnés au travail demandé.
Aucune publication, prise de contact, dépense ou installation n'est autorisée
par ce socle. Les secrets, médias, caches et dépendances restent hors corpus.

## Socle et continuité

Moteur commun : `{{IMRANE_WORKSPACE_ROOT}}/tools/systeme-imrane`. Skills communs uniquement
sous `{{IMRANE_WORKSPACE_ROOT}}/.agents/skills` ; les deux wrappers locaux servent à le découvrir.
Le routage suit `.codex/model-routing-policy.json` et
`docs/governance/AUTOMATIC_ROUTING.md` à la gouvernance : contrôleur, un worker
natif selon modèle/effort configurés, attente et vérification ; aucun worker imbriqué.
Ne pas changer modèle principal, permissions, Max/Ultra ou service tier.
Claude reste consultatif ; les hooks ne lancent pas le worker et ne changent pas le modèle.

Les quatre mémoires canoniques sont propres à cette lane ; runtime privé :
`{{IMRANE_WORKSPACE_ROOT}}/tmp/codex-session/projects/protrain/`. Avant arrêt/compactation,
actualiser CURRENT et les décisions, puis snapshot explicite des quatre mémoires.
Graphify n'est pas une mémoire canonique : état PENDING_AUTHORIZATION à la création.
Corpus limité à AGENTS.md et quatre mémoires ; aucun réseau sans revue et accord
explicite pour ce nouveau corpus vers Google Gemini. Utiliser les fichiers directs
tant que graphe/provenance/requête ne sont pas vérifiés. Contrôler la fraîcheur
localement ; ne pas laisser son échec empêcher le snapshot.

Les hooks sont configurés pour cinq événements ; leur appel synthétique ne prouve
pas leur chargement natif. Recharger et vérifier Codex/Claude séparément.
