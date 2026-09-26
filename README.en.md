# model-swap-ci

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
