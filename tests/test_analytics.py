"""
Unit tests for FinSights Analytics & Data Cleaner modules.
"""

import unittest
import numpy as np
from finsights.models import Transaction, TransactionMeta
from finsights.services.data_cleaner import DataCleanerService
from finsights.services.analytics import AnalyticsService


class TestFinSights(unittest.TestCase):
    """Test suite for data cleaner and analytics services."""

    def setUp(self) -> None:
        self.cleaner = DataCleanerService()
        self.analytics = AnalyticsService()

    def test_clean_transactions(self) -> None:
        raw_records = [
            {"id": "T1", "date": "2026-08-01", "merchant": "StoreA", "category": "Groceries", "amount": "100.0"},
            {"id": "T2", "date": "2026-08-02", "merchant": "BadStore", "category": "UnknownCat", "amount": "50.0"},
            {"id": "T3", "date": "2026-08-03", "merchant": "StoreB", "category": "Utilities", "amount": "-20.0"}
        ]
        valid_txs, rejected, unique_merchants = self.cleaner.clean_transactions(raw_records)

        self.assertEqual(len(valid_txs), 1)
        self.assertEqual(len(rejected), 2)
        self.assertIn("StoreA", unique_merchants)
        self.assertEqual(valid_txs[0].amount, 100.0)

    def test_analytics_metrics(self) -> None:
        meta1 = TransactionMeta("T1", "2026-08-01", "StoreA")
        meta2 = TransactionMeta("T2", "2026-08-02", "StoreB")
        tx1 = Transaction(meta=meta1, category="Groceries", amount=100.0)
        tx2 = Transaction(meta=meta2, category="Groceries", amount=200.0)

        metrics = self.analytics.compute_metrics([tx1, tx2])

        self.assertEqual(metrics["total_spend"], 300.0)
        self.assertEqual(metrics["mean_spend"], 150.0)
        self.assertEqual(metrics["median_spend"], 150.0)
        self.assertEqual(metrics["min_spend"], 100.0)
        self.assertEqual(metrics["max_spend"], 200.0)
        self.assertEqual(metrics["category_breakdown"]["Groceries"], 300.0)


if __name__ == "__main__":
    unittest.main()
