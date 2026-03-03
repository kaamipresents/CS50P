"""
test_logic.py — Unit tests for logic.py.
Run:  python -m pytest test_logic.py -v
      — or —
      python test_logic.py
"""

import os
import sys
import json
import unittest

# ── Make sure we import from the project root ──────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import logic


class TestValidateName(unittest.TestCase):

    def test_valid_name(self):
        ok, err = logic.validate_name("Alice")
        self.assertTrue(ok)
        self.assertIsNone(err)

    def test_valid_name_with_space(self):
        ok, err = logic.validate_name("Mary Jane")
        self.assertTrue(ok)

    def test_valid_name_with_hyphen(self):
        ok, err = logic.validate_name("Anne-Marie")
        self.assertTrue(ok)

    def test_valid_name_with_apostrophe(self):
        ok, err = logic.validate_name("O'Brien")
        self.assertTrue(ok)

    def test_empty_name(self):
        ok, err = logic.validate_name("")
        self.assertFalse(ok)
        self.assertIn("empty", err.lower())

    def test_whitespace_only(self):
        ok, err = logic.validate_name("   ")
        self.assertFalse(ok)

    def test_name_too_short(self):
        ok, err = logic.validate_name("A")
        self.assertFalse(ok)
        self.assertIn("2", err)

    def test_name_too_long(self):
        ok, err = logic.validate_name("A" * 51)
        self.assertFalse(ok)
        self.assertIn("50", err)

    def test_name_with_numbers(self):
        ok, err = logic.validate_name("Ali3e")
        self.assertFalse(ok)

    def test_name_with_emoji(self):
        ok, err = logic.validate_name("Ali😀")
        self.assertFalse(ok)


class TestBuildGreeting(unittest.TestCase):

    def test_greeting_contains_name(self):
        greeting = logic.build_greeting("alice")
        self.assertIn("Alice", greeting)

    def test_greeting_is_string(self):
        greeting = logic.build_greeting("Bob")
        self.assertIsInstance(greeting, str)

    def test_greeting_not_empty(self):
        greeting = logic.build_greeting("Carol")
        self.assertTrue(len(greeting) > 0)

    def test_name_is_title_cased(self):
        greeting = logic.build_greeting("david")
        self.assertIn("David", greeting)


class TestRecordGreeting(unittest.TestCase):
    """
    These tests use a temporary JSON file so they don't
    pollute real data and clean up after themselves.
    """

    def setUp(self):
        # Redirect storage to a temp file
        logic.ensure_data_dir()
        self._orig_file = logic.GREETINGS_FILE
        logic.GREETINGS_FILE = os.path.join(logic.DATA_DIR, "_test_greetings.json")
        # Start clean
        if os.path.exists(logic.GREETINGS_FILE):
            os.remove(logic.GREETINGS_FILE)

    def tearDown(self):
        if os.path.exists(logic.GREETINGS_FILE):
            os.remove(logic.GREETINGS_FILE)
        logic.GREETINGS_FILE = self._orig_file

    def test_record_valid_name(self):
        ok, result, name = logic.record_greeting("Eve")
        self.assertTrue(ok)
        self.assertIn("Eve", result)
        self.assertEqual(name, "Eve")

    def test_record_invalid_name(self):
        ok, result, name = logic.record_greeting("")
        self.assertFalse(ok)
        self.assertIsNone(name)
        self.assertIsInstance(result, str)  # error message

    def test_record_persists_to_file(self):
        logic.record_greeting("Frank")
        greetings = logic.load_greetings()
        self.assertEqual(len(greetings), 1)
        self.assertEqual(greetings[0]["name"], "Frank")

    def test_multiple_records(self):
        logic.record_greeting("Grace")
        logic.record_greeting("Hank")
        greetings = logic.load_greetings()
        self.assertEqual(len(greetings), 2)

    def test_get_visitor_count(self):
        logic.record_greeting("Iris")
        logic.record_greeting("Jack")
        self.assertEqual(logic.get_visitor_count(), 2)

    def test_get_all_greetings_newest_first(self):
        logic.record_greeting("First")
        logic.record_greeting("Second")
        all_g = logic.get_all_greetings()
        self.assertEqual(all_g[0]["name"], "Second")
        self.assertEqual(all_g[1]["name"], "First")

    def test_delete_all(self):
        logic.record_greeting("Kim")
        logic.delete_all_greetings()
        self.assertEqual(logic.get_visitor_count(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
