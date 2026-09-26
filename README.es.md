# model-swap-ci

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

Repite las mismas tareas de agente con dos adaptadores de modelo y compara respuesta verificada, llamadas a herramientas y tokens declarados. Cada adaptador es una orden: recibe JSON con `task` y `observations` por stdin y devuelve `{"tool":"lookup","args":{"key":"..."},"tokens":6}` o `{"answer":"...","tokens":4}`.

## Inicio rápido

Python 3.11+, sin dependencias externas.

```bash
python3 model_swap.py examples/tasks.json --baseline-cmd "python3 examples/adapter.py" --candidate-cmd "python3 examples/adapter.py --candidate"
python3 -m unittest discover -s tests -v
```

La demostración sale con código `2`: el candidato consulta `profit` en vez de `revenue`. El informe muestra `outcome_regression`, `tool_calls_changed` y `token_delta` por tarea. `--output report.json` lo guarda. Sustituye ambas órdenes por tus adaptadores reales para probar un cambio de modelo.

## Alcance

El MVP ofrece una herramienta sintética `lookup` y comprueba respuestas por igualdad exacta. El adaptador de demostración es determinista; sus resultados no miden ningún modelo real. Las órdenes de adaptador ejecutan código local: usa solo órdenes de confianza.

Señales: [Magpie](https://github.com/yetone/magpie) y [ReflexBench](https://github.com/brida-ai/reflexbench). Aquí se compara el recorrido completo del agente.

Licencia MIT. Se aceptan más adaptadores y escenarios.
