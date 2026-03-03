"""
tests/test_logic.py — Unit tests for the Smart Expense Tracker business logic.
Run with: python -m pytest tests/ -v
"""

import sys
import os
import json
import unittest

# Allow importing from parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Point storage to a temp test file BEFORE importing logic
import storage
storage.DATA_FILE = os.path.join(os.path.dirname(__file__), "test_expenses.json")

from logic import (
    validate_amount,
    validate_category,
    validate_description,
    add_expense,
    get_all_expenses,
    update_expense,
    delete_expense,
    get_summary,
)


class TestValidation(unittest.TestCase):

    def test_valid_amount(self):
        self.assertEqual(validate_amount("25.50"), 25.50)
        self.assertEqual(validate_amount(100), 100.0)

    def test_invalid_amount_zero(self):
        with self.assertRaises(ValueError):
            validate_amount("0")

    def test_invalid_amount_negative(self):
        with self.assertRaises(ValueError):
            validate_amount("-10")

    def test_invalid_amount_string(self):
        with self.assertRaises(ValueError):
            validate_amount("abc")

    def test_valid_category(self):
        self.assertEqual(validate_category("food"), "Food")
        self.assertEqual(validate_category("TRANSPORT"), "Transport")

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_category("Luxury")

    def test_empty_category(self):
        with self.assertRaises(ValueError):
            validate_category("")

    def test_valid_description(self):
        self.assertEqual(validate_description("  Lunch at work  "), "Lunch at work")

    def test_empty_description(self):
        with self.assertRaises(ValueError):
            validate_description("")

    def test_long_description(self):
        with self.assertRaises(ValueError):
            validate_description("x" * 201)


class TestCRUD(unittest.TestCase):

    def setUp(self):
        """Reset test data file before each test."""
        with open(storage.DATA_FILE, "w") as f:
            json.dump([], f)

    def tearDown(self):
        """Clean up test data file."""
        if os.path.exists(storage.DATA_FILE):
            os.remove(storage.DATA_FILE)

    def test_add_expense(self):
        expense = add_expense("50.00", "Food", "Grocery shopping")
        self.assertEqual(expense["amount"], 50.00)
        self.assertEqual(expense["category"], "Food")
        self.assertEqual(expense["description"], "Grocery shopping")
        self.assertIn("id", expense)
        self.assertIn("date", expense)

    def test_add_multiple_expenses_unique_ids(self):
        e1 = add_expense("10.00", "Food", "Coffee")
        e2 = add_expense("20.00", "Transport", "Bus fare")
        self.assertNotEqual(e1["id"], e2["id"])

    def test_get_all_expenses(self):
        add_expense("10.00", "Food", "Coffee")
        add_expense("20.00", "Transport", "Bus")
        all_expenses = get_all_expenses()
        self.assertEqual(len(all_expenses), 2)

    def test_update_expense_amount(self):
        expense = add_expense("10.00", "Food", "Coffee")
        updated = update_expense(expense["id"], amount_str="15.00")
        self.assertEqual(updated["amount"], 15.00)
        self.assertEqual(updated["category"], "Food")  # unchanged

    def test_update_expense_not_found(self):
        with self.assertRaises(ValueError):
            update_expense(9999, amount_str="10.00")

    def test_delete_expense(self):
        expense = add_expense("10.00", "Food", "Test")
        result = delete_expense(expense["id"])
        self.assertTrue(result)
        remaining = get_all_expenses()
        self.assertEqual(len(remaining), 0)

    def test_delete_nonexistent_expense(self):
        with self.assertRaises(ValueError):
            delete_expense(9999)


class TestSummary(unittest.TestCase):

    def setUp(self):
        with open(storage.DATA_FILE, "w") as f:
            json.dump([], f)

    def tearDown(self):
        if os.path.exists(storage.DATA_FILE):
            os.remove(storage.DATA_FILE)

    def test_summary_empty(self):
        summary = get_summary()
        self.assertEqual(summary["total"], 0.0)
        self.assertEqual(summary["count"], 0)

    def test_summary_totals(self):
        add_expense("30.00", "Food", "Dinner")
        add_expense("20.00", "Food", "Lunch")
        add_expense("50.00", "Transport", "Taxi")

        summary = get_summary()
        self.assertEqual(summary["total"], 100.00)
        self.assertEqual(summary["count"], 3)
        self.assertEqual(summary["by_category"]["Food"], 50.00)
        self.assertEqual(summary["by_category"]["Transport"], 50.00)
        self.assertAlmostEqual(summary["average"], 33.33, places=1)


if __name__ == "__main__":
    unittest.main()
