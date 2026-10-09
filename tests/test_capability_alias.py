import unittest

from capability_alias import inspect


class AliasTests(unittest.TestCase):
    def test_complete_and_incomplete(self):
        fields = {"reasoning": True, "vision": False, "context_window": 100, "tool_calling": True}
        mapping = {"routed_id": "alias", "catalog_id": "base"}
        self.assertEqual(inspect(mapping, {"models": {"alias": fields, "base": fields}})["status"], "match")
        self.assertEqual(inspect(mapping, {"models": {"alias": {**fields, "reasoning": False}, "base": fields}})["different_fields"], ["reasoning"])
        self.assertEqual(inspect(mapping, {"models": {"alias": {}, "base": fields}})["status"], "inconclusive")


if __name__ == "__main__":
    unittest.main()
