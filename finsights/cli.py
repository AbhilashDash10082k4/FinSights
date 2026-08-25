"""
Command-Line Interface for FinSights.
Handles user interactions, menu options, and display output.
"""

import sys
from typing import Dict, Any
from finsights.controllers.finance_controller import FinanceController


class FinSightsCLI:
    """CLI handler for user interaction."""

    def __init__(self, csv_path: str = "data/sample_transactions.csv") -> None:
        self.controller = FinanceController()
        self.csv_path = csv_path
        self.result_cache: Dict[str, Any] = {}

    def run(self) -> None:
        """Run main CLI menu loop."""
        print("=========================================")
        print("   FinSights - Finance Analytics Engine   ")
        print("=========================================")

        # Run initial processing pipeline
        self.result_cache = self.controller.process_and_analyze(self.csv_path)
        print(f"[*] Processed dataset: {self.csv_path}")
        print(f"[*] Clean records: {self.result_cache['valid_count']} | Rejected: {self.result_cache['rejected_count']}")
        print(f"[*] Unique merchants: {len(self.result_cache['unique_merchants'])}")

        while True:
            print("\n-----------------------------------------")
            print("1. View Statistical Metrics (NumPy)")
            print("2. View Category Breakdown (ASCII Chart)")
            print("3. Export Markdown Executive Report")
            print("4. Exit")
            print("-----------------------------------------")

            choice = input("Select an option (1-4): ").strip()

            if choice == "1":
                self._display_metrics()
            elif choice == "2":
                self._display_chart()
            elif choice == "3":
                self._export_report()
            elif choice == "4":
                print("Exiting FinSights. Goodbye!")
                sys.exit(0)
            else:
                print("[!] Invalid option. Please select 1-4.")

    def _display_metrics(self) -> None:
        metrics = self.result_cache.get("metrics", {})
        print("\n--- NumPy Statistical Summary ---")
        print(f"Total Transactions : {metrics.get('transaction_count')}")
        print(f"Total Spending     : ${metrics.get('total_spend'):,.2f}")
        print(f"Mean Spending      : ${metrics.get('mean_spend'):,.2f}")
        print(f"Median Spending    : ${metrics.get('median_spend'):,.2f}")
        print(f"Std Deviation      : ${metrics.get('std_dev'):,.2f}")
        print(f"75th Percentile    : ${metrics.get('percentile_75'):,.2f}")
        print(f"Min / Max Spend    : ${metrics.get('min_spend'):,.2f} / ${metrics.get('max_spend'):,.2f}")

    def _display_chart(self) -> None:
        metrics = self.result_cache.get("metrics", {})
        breakdown = metrics.get("category_breakdown", {})
        print("\n--- Category Spending Breakdown ---")
        max_val = max(breakdown.values()) if breakdown else 1.0
        for cat, amt in breakdown.items():
            bars = "█" * int((amt / max_val) * 25)
            print(f"{cat:<14} | {bars:<25} ${amt:,.2f}")

    def _export_report(self) -> None:
        output_file = "output/summary_report.md"
        self.controller.generate_report(self.result_cache.get("metrics", {}), output_file)
        print(f"[+] Markdown report successfully exported to: {output_file}")
