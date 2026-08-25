"""
Analytics Engine Service for FinSights.
Demonstrates NumPy computations, Dictionaries, Lists, Statistical Analysis.
"""

from typing import List, Dict, Any
import numpy as np
from finsights.models import Transaction


class AnalyticsService:
    """Service performing financial analytics using NumPy."""

    def compute_metrics(self, transactions: List[Transaction]) -> Dict[str, Any]:
        """
        Compute statistical analytics using NumPy array operations.
        Returns a dictionary containing calculated summary metrics.
        """
        if not transactions:
            return {
                "total_spend": 0.0,
                "mean_spend": 0.0,
                "median_spend": 0.0,
                "std_dev": 0.0,
                "min_spend": 0.0,
                "max_spend": 0.0,
                "percentile_75": 0.0,
                "category_breakdown": {},
                "anomaly_count": 0
            }

        # Extract amounts into a NumPy ndarray
        amounts_list = [tx.amount for tx in transactions]
        amounts_array = np.array(amounts_list, dtype=np.float64)

        # NumPy statistical calculations
        total_spend = float(np.sum(amounts_array))
        mean_spend = float(np.mean(amounts_array))
        median_spend = float(np.median(amounts_array))
        std_dev = float(np.std(amounts_array))
        min_spend = float(np.min(amounts_array))
        max_spend = float(np.max(amounts_array))
        percentile_75 = float(np.percentile(amounts_array, 75))

        # Category spending aggregation using Dictionary
        category_breakdown: Dict[str, float] = {}
        for tx in transactions:
            category_breakdown[tx.category] = (
                category_breakdown.get(tx.category, 0.0) + tx.amount
            )

        # Anomaly detection threshold (mean + 2 * std_dev)
        anomaly_threshold = mean_spend + (2 * std_dev)
        anomalies = [tx for tx in transactions if tx.amount > anomaly_threshold]

        return {
            "transaction_count": len(transactions),
            "total_spend": round(total_spend, 2),
            "mean_spend": round(mean_spend, 2),
            "median_spend": round(median_spend, 2),
            "std_dev": round(std_dev, 2),
            "min_spend": round(min_spend, 2),
            "max_spend": round(max_spend, 2),
            "percentile_75": round(percentile_75, 2),
            "category_breakdown": {
                k: round(v, 2) for k, v in category_breakdown.items()
            },
            "anomaly_count": len(anomalies)
        }
