# model-swap-ci

## New: check a renamed relay model

**“My relay alias lost reasoning or tool calling.”** `python3 capability_alias.py demo --lang en` shows a synthetic mismatch. For saved evidence, run `python3 capability_alias.py check --mapping alias.json --catalog catalog.json --lang en`. The mapping explicitly names `routed_id` and `catalog_id`; `catalog.json` has a `models` object with `reasoning`, `vision`, `context_window`, and `tool_calling` per ID. Missing fields are inconclusive. The tool never guesses or applies an alias.

**Related projects:** [Magpie #1383](https://github.com/yetone/magpie/issues/1383) reports lost capability metadata on a renamed relay ID; [Magpie](https://github.com/yetone/magpie) is the neighboring router. The actual integration is reading a saved JSON catalog, with no direct Magpie plugin or affiliation.

## New: compare requested and routed reasoning

`python3 reasoning_audit.py reasoning-demo --lang en` shows two mismatches in ten seconds: `none → low` and `ultra: xhigh → max` (successful demo exits 0). For your captures, save Magpie route-log excerpts in the shape of `examples/reasoning-cases.json`, then point to the real Codex model cache:

```sh
python3 reasoning_audit.py reasoning-check cases.json --models-cache ~/.codex/models_cache.json --lang en
```

`none` cases compare the request with route-log `effort`; `ultra` cases require an official model entry with `multi_agent_reasoning_effort` and a consistent official route. Missing evidence or disagreement between `effort` and `tries[].effort` stays inconclusive. Exit codes: 0 parity, 2 mismatch, 3 incomplete evidence, 1 invalid capture. This reads real route-log and cache formats without calling a model or showing prompts. The log shows the effort selected by the route, **not** provider-internal reasoning or billed tokens. Demo fixtures are reconstructed from public reports, not the reporters' private captures.

**Related projects:** [Magpie #1098](https://github.com/yetone/magpie/issues/1098) reports `off → low`; [#1108](https://github.com/yetone/magpie/issues/1108) reports `xhigh → max` through a third-party model. [Magpie](https://github.com/yetone/magpie) supplies the routes; this independent checker does not change its configuration.

[Français](README.md) · [English](README.en.md) · [Español](README.es.md)

## Related projects and target gap

- [Magpie](https://github.com/yetone/magpie) makes model selection and switching easier across agents. Every switch raises a practical question: does the same tool workflow still reach the right outcome?
- [ReflexBench](https://github.com/brida-ai/reflexbench) evaluates typed decision models. Our scope is the **complete tool-using agent workflow**, which can complement a model benchmark.
- **Our angle:** replay the same tasks through two adapter commands and show outcome and tool-call regressions. No Magpie or ReflexBench adapter is included.

Replay the same agent tasks against two model adapters and compare verified answer, tool calls, and reported token count. Each adapter is a command: it receives JSON with `task` and `observations` on stdin, then returns either `{"tool":"lookup","args":{"key":"..."},"tokens":6}` or `{"answer":"...","tokens":4}`.

## Quick start

Python 3.11+, no external dependencies.

```bash
python3 model_swap.py examples/tasks.json --baseline-cmd "python3 examples/adapter.py" --candidate-cmd "python3 examples/adapter.py --candidate"
python3 -m unittest discover -s tests -v
```

The demo exits `2`: the candidate looks up `profit` instead of `revenue`. The report shows `outcome_regression`, `tool_calls_changed`, and `token_delta` per task. `--output report.json` saves it. Replace both commands with your real adapters to test a model change.

## Scope

The MVP provides one synthetic `lookup` tool and checks answers by exact equality. The demo adapter is deterministic; its results say nothing about any real model. Adapter commands execute local code, so use trusted commands only.


MIT licensed. Additional adapters and scenarios are welcome.
