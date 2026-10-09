# model-swap-ci

## Nuevo: comprobar un alias de modelo en un relé

**« Mi alias de relé perdió el razonamiento o las llamadas a herramientas. »** `python3 capability_alias.py demo --lang es` muestra una discrepancia sintética. Para datos guardados, ejecute `python3 capability_alias.py check --mapping alias.json --catalog catalog.json --lang es`. El mapeo nombra explícitamente `routed_id` y `catalog_id`; `catalog.json` contiene `models` con `reasoning`, `vision`, `context_window` y `tool_calling` por ID. Si falta un campo, el resultado es indeterminado. La herramienta no adivina ni aplica alias.

**Proyectos relacionados:** [Magpie #1383](https://github.com/yetone/magpie/issues/1383) informa de metadatos de capacidad perdidos por un ID de relé renombrado; [Magpie](https://github.com/yetone/magpie) es el enrutador vecino. La integración real es la lectura de un catálogo JSON guardado, sin complemento Magpie directo ni afiliación.

## Nuevo: comparar el razonamiento solicitado y el enrutado

`python3 reasoning_audit.py reasoning-demo --lang es` muestra dos diferencias en diez segundos: `none → low` y `ultra: xhigh → max` (la demo correcta sale con código 0). Para sus capturas, guarde extractos de los logs de ruta Magpie con el formato de `examples/reasoning-cases.json` y apunte al caché real de modelos Codex:

```sh
python3 reasoning_audit.py reasoning-check casos.json --models-cache ~/.codex/models_cache.json --lang es
```

Los casos `none` comparan la petición con `effort` del log; los casos `ultra` requieren una entrada oficial con `multi_agent_reasoning_effort` y una ruta oficial coherente. Si faltan pruebas o `effort` y `tries[].effort` discrepan, el resultado queda inconcluso. Códigos de salida: 0 paridad, 2 diferencia, 3 prueba incompleta, 1 captura no válida. Lee formatos reales de log y caché sin llamar a un modelo ni mostrar prompts. El log indica el nivel elegido por la ruta, **no** el razonamiento interno del proveedor ni los tokens facturados. Las fixtures de la demo se reconstruyeron a partir de informes públicos, no son capturas privadas de sus autores.

**Proyectos relacionados:** [Magpie #1098](https://github.com/yetone/magpie/issues/1098) informa de `off → low` y [#1108](https://github.com/yetone/magpie/issues/1108) de `xhigh → max` con un modelo tercero. [Magpie](https://github.com/yetone/magpie) proporciona las rutas; esta herramienta independiente no cambia su configuración.

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Proyectos relacionados y carencia abordada

- [Magpie](https://github.com/yetone/magpie) facilita elegir y cambiar modelos en distintos agentes. Cada cambio plantea una pregunta práctica: ¿el mismo recorrido de herramientas sigue dando el resultado correcto?
- [ReflexBench](https://github.com/brida-ai/reflexbench) evalúa modelos de decisiones tipadas. Nuestro alcance es **el recorrido completo del agente con herramientas**, que puede complementar un benchmark de modelos.
- **Nuestro enfoque:** repetir las mismas tareas con dos órdenes de adaptador y mostrar regresiones del resultado y de las llamadas. No se incluye un adaptador para Magpie ni ReflexBench.

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


Licencia MIT. Se aceptan más adaptadores y escenarios.
