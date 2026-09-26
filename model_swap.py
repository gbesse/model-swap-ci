"""Replay tool-using tasks against two JSON-line command adapters."""
import argparse
import json
from pathlib import Path
import shlex
import subprocess
import sys


def replay(task, command, max_steps=8):
    observations = []
    calls = []
    tokens = 0
    for _ in range(max_steps):
        request = {'task': task, 'observations': observations}
        try:
            process = subprocess.run(shlex.split(command), input=json.dumps(request), text=True,
                                     capture_output=True, check=False, timeout=30)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {'pass': False, 'error': str(exc), 'calls': calls, 'tokens': tokens}
        if process.returncode:
            return {'pass': False, 'error': f'adapter exit {process.returncode}', 'calls': calls, 'tokens': tokens}
        try:
            decision = json.loads(process.stdout)
            tokens += int(decision.get('tokens', 0))
            if 'answer' in decision:
                answer = decision['answer']
                return {'pass': answer == task['expected_answer'], 'answer': answer,
                        'calls': calls, 'tokens': tokens}
            if decision.get('tool') != 'lookup':
                raise ValueError('only lookup tool is available')
            key = decision['args']['key']
            calls.append({'tool': 'lookup', 'key': key})
            observations.append({'key': key, 'value': task['tool_data'].get(key)})
        except (ValueError, KeyError, TypeError) as exc:
            return {'pass': False, 'error': str(exc), 'calls': calls, 'tokens': tokens}
    return {'pass': False, 'error': 'step limit exceeded', 'calls': calls, 'tokens': tokens}


def compare(tasks, baseline_command, candidate_command):
    cases = []
    for task in tasks:
        baseline = replay(task, baseline_command)
        candidate = replay(task, candidate_command)
        cases.append({'id': task['id'], 'baseline': baseline, 'candidate': candidate,
                      'outcome_regression': baseline['pass'] and not candidate['pass'],
                      'tool_calls_changed': baseline['calls'] != candidate['calls'],
                      'token_delta': candidate['tokens'] - baseline['tokens']})
    return {'pass': not any(c['outcome_regression'] for c in cases), 'cases': cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tasks', type=Path)
    parser.add_argument('--baseline-cmd', required=True)
    parser.add_argument('--candidate-cmd', required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = compare(json.loads(args.tasks.read_text())['tasks'], args.baseline_cmd, args.candidate_cmd)
    encoded = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(encoded + '\n')
    print(encoded)
    return 0 if report['pass'] else 2


if __name__ == '__main__':
    sys.exit(main())
