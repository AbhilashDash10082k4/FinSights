"""
Finance Controller for FinSights.
Coordinates request cycle between Presentation, Services, and Repository.
"""

from typing import Dict, Any, List
from finsights.repository import FinanceRepository
from finsights.services.data_cleaner import DataCleanerService
from finsights.services.analytics import AnalyticsService


class FinanceController:
    """Controller orchestrating data processing & reporting pipeline."""

    def __init__(self) -> None:
        self.repository = FinanceRepository()
        self.cleaner = DataCleanerService()
        self.analytics = AnalyticsService()

    def process_and_analyze(self, csv_file_path: str) -> Dict[str, Any]:
        """
        Main workflow controller method.
        1. Load raw CSV data via Repository
        2. Clean and validate records via DataCleanerService
        3. Perform statistical analysis via AnalyticsService
        """
        # Load raw records
        raw_records = self.repository.load_csv(csv_file_path)

        # Clean records
        valid_txs, rejected_records, unique_merchants = (
            self.cleaner.clean_transactions(raw_records)
        )

        # Compute analytics
        metrics = self.analytics.compute_metrics(valid_txs)

        # Save clean JSON output
        clean_json_data = [tx.to_dict() for tx in valid_txs]
        self.repository.save_json(clean_json_data, "output/clean_transactions.json")

        return {
            "metrics": metrics,
            "valid_count": len(valid_txs),
            "rejected_count": len(rejected_records),
            "unique_merchants": list(unique_merchants),
            "transactions": valid_txs
        }

    def generate_report(self, metrics: Dict[str, Any], output_path: str) -> str:
        """Construct Markdown summary report with ASCII chart."""
        lines: List[str] = [
            "# FinSights - Personal Finance Executive Summary",
            "",
            "## Key Financial Metrics (NumPy Computed)",
            f"- **Total Spend**: ${metrics.get('total_spend', 0.0):,.2f}",
            f"- **Average Transaction (Mean)**: ${metrics.get('mean_spend', 0.0):,.2f}",
            f"- **Median Spend**: ${metrics.get('median_spend', 0.0):,.2f}",
            f"- **Standard Deviation**: ${metrics.get('std_dev', 0.0):,.2f}",
            f"- **75th Percentile**: ${metrics.get('percentile_75', 0.0):,.2f}",
            f"- **Min / Max Spend**: ${metrics.get('min_spend', 0.0):,.2f} / ${metrics.get('max_spend', 0.0):,.2f}",
            f"- **Anomalies Detected**: {metrics.get('anomaly_count', 0)}",
            "",
            "## Spending by Category (ASCII Chart)",
            "```"
        ]

        breakdown = metrics.get("category_breakdown", {})
        max_val = max(breakdown.values()) if breakdown else 1.0

        for category, amount in breakdown.items():
            bar_len = int((amount / max_val) * 30)
            bar = "█" * bar_len
            lines.append(f"{category:<15} | {bar:<30} ${amount:,.2f}")

        lines.extend(["```", ""])
        report_content = "\n".join(lines)

        self.repository.write_markdown_report(report_content, output_path)
        return report_content
