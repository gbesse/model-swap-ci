# model-swap-ci

## Nouveau : vérifier un alias de modèle relayé

**« Mon alias de relais a perdu la capacité de raisonner ou d’appeler des outils. »** `python3 capability_alias.py demo --lang fr` affiche une divergence synthétique. Pour vos données, lancez `python3 capability_alias.py check --mapping alias.json --catalog catalog.json --lang fr`. Le mapping nomme explicitement `routed_id` et `catalog_id` ; `catalog.json` contient `models` avec `reasoning`, `vision`, `context_window` et `tool_calling` pour chaque ID. Un champ absent donne « preuve incomplète ». Aucun alias n’est deviné ni appliqué automatiquement.

**Projets voisins :** [Magpie #1383](https://github.com/yetone/magpie/issues/1383) décrit les métadonnées perdues par un ID de relais renommé ; [Magpie](https://github.com/yetone/magpie) est le routeur voisin. L’intégration réelle est l’analyse d’un catalogue JSON sauvegardé ; pas de branchement Magpie direct ni d’affiliation.

## Nouveau : comparer le raisonnement demandé et routé

`python3 reasoning_audit.py reasoning-demo --lang fr` montre deux divergences en dix secondes : `none → low` et `ultra : xhigh → max` (démo réussie : code 0). Pour vos captures, enregistrez les extraits de journaux de route Magpie dans un fichier au format `examples/reasoning-cases.json`, puis utilisez le vrai cache de modèles Codex :

```sh
python3 reasoning_audit.py reasoning-check cas.json --models-cache ~/.codex/models_cache.json --lang fr
```

Les cas `none` comparent la demande au champ `effort` du journal ; les cas `ultra` exigent une entrée de modèle officiel avec `multi_agent_reasoning_effort` et une route officielle cohérente. Si une preuve manque ou si `effort` et `tries[].effort` se contredisent, le résultat reste indéterminé. Codes de sortie : 0 parité, 2 divergence, 3 preuve incomplète, 1 capture invalide. L’outil lit de vrais formats de journal et de cache, sans appeler de modèle ni exposer les prompts. Le journal montre le niveau choisi par la route, **pas** le raisonnement interne du fournisseur ni les tokens facturés. Les fixtures de démo sont reconstruites à partir des rapports publics, pas des captures privées de leurs auteurs.

**Projets voisins :** [Magpie #1098](https://github.com/yetone/magpie/issues/1098) rapporte `off → low` et [#1108](https://github.com/yetone/magpie/issues/1108) rapporte `xhigh → max` via un modèle tiers. [Magpie](https://github.com/yetone/magpie) fournit les routes ; ce contrôleur indépendant ne change pas sa configuration.

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Projets voisins et lacune visée

- [Magpie](https://github.com/yetone/magpie) facilite le choix et le changement de modèle dans les agents. Chaque changement crée une question pratique : le même parcours d'outils produit-il toujours le bon résultat ?
- [ReflexBench](https://github.com/brida-ai/reflexbench) évalue des modèles de décision typés. Notre périmètre est le **parcours complet d'un agent avec outils**, ce qui peut compléter un benchmark de modèle.
- **Notre angle :** rejouer les mêmes tâches sur deux commandes d'adaptateur et montrer les régressions de résultat et les changements d'appels. Aucun adaptateur Magpie ou ReflexBench n'est inclus.

Rejoue les mêmes tâches d'agent sur deux adaptateurs de modèle et compare réponse vérifiée, appels d'outils et nombre de tokens déclaré. Chaque adaptateur est une commande : elle reçoit en entrée standard un JSON avec `task` et `observations`, puis renvoie soit `{"tool":"lookup","args":{"key":"..."},"tokens":6}`, soit `{"answer":"...","tokens":4}`.

## Démarrage

Python 3.11+, sans dépendance externe.

```bash
python3 model_swap.py examples/tasks.json --baseline-cmd "python3 examples/adapter.py" --candidate-cmd "python3 examples/adapter.py --candidate"
python3 -m unittest discover -s tests -v
```

La démo sort avec le code `2` : le candidat consulte `profit` au lieu de `revenue`. Le rapport indique `outcome_regression`, `tool_calls_changed` et `token_delta` par tâche. `--output report.json` l'enregistre. Remplacez les deux commandes par vos adaptateurs réels pour tester un changement de modèle.

## Périmètre

Le MVP propose un outil synthétique `lookup` et vérifie les réponses par égalité exacte. L'adaptateur de démo est déterministe : ses résultats ne mesurent aucun modèle réel. Les commandes d'adaptateur sont du code exécuté localement ; n'utilisez que des commandes de confiance.


Licence MIT. Adaptateurs et scénarios supplémentaires bienvenus.
