import json
import sys
import unittest
from pathlib import Path
from model_swap import compare

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'
TASKS = json.loads((EXAMPLES / 'tasks.json').read_text())['tasks']
BASELINE = f'{sys.executable} {EXAMPLES / "adapter.py"}'
CANDIDATE = f'{sys.executable} {EXAMPLES / "adapter.py"} --candidate'


class SwapTests(unittest.TestCase):
    def test_identical_adapter_passes(self):
        self.assertTrue(compare(TASKS, BASELINE, BASELINE)['pass'])

    def test_regression_and_tool_drift(self):
        report = compare(TASKS, BASELINE, CANDIDATE)
        self.assertFalse(report['pass'])
        self.assertTrue(report['cases'][0]['outcome_regression'])
        self.assertTrue(report['cases'][0]['tool_calls_changed'])
        self.assertFalse(report['cases'][1]['tool_calls_changed'])
