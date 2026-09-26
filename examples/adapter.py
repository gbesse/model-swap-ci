"""Deterministic adapter demonstrating a model swap regression."""
import json
import sys

request = json.load(sys.stdin)
task = request['task']
observations = request['observations']
if observations:
    print(json.dumps({'answer': observations[-1]['value'], 'tokens': 4}))
else:
    key = task['lookup_key']
    if '--candidate' in sys.argv and task['id'] == 'revenue':
        key = 'profit'
    print(json.dumps({'tool': 'lookup', 'args': {'key': key}, 'tokens': 6}))
