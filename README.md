# model-swap-ci

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

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

Signaux : [Magpie](https://github.com/yetone/magpie) et [ReflexBench](https://github.com/brida-ai/reflexbench). Ici, l'unité de comparaison est le parcours complet d'agent.

Licence MIT. Adaptateurs et scénarios supplémentaires bienvenus.
