"""
Repository Layer for FinSights.
Handles File I/O operations (CSV reading, JSON writing, Markdown export).
"""

import csv
import json
import os
from typing import List, Dict, Any


class FinanceRepository:
    """Repository managing dataset loading and saving operations."""

    def load_csv(self, file_path: str) -> List[Dict[str, str]]:
        """
        Load raw transaction records from CSV file.
        Demonstrates File Handling (reading).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at path: {file_path}")

        records: List[Dict[str, str]] = []
        with open(file_path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                records.append(row)
        return records

    def save_json(self, data: List[Dict[str, Any]], output_path: str) -> None:
        """
        Save clean records to JSON format.
        Demonstrates File Handling (writing JSON).
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, mode="w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

    def write_markdown_report(self, report_text: str, output_path: str) -> None:
        """
        Save summary report text to Markdown file.
        Demonstrates File Handling (writing text).
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, mode="w", encoding="utf-8") as md_file:
            md_file.write(report_text)
