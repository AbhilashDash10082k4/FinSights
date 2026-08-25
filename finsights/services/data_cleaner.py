"""
Data Cleaner Service for FinSights.
Demonstrates Sets, Lists, Tuples, Conditionals, Loops, Data Validation.
"""

from typing import List, Dict, Any, Tuple, Set
from finsights.models import Transaction, TransactionMeta


class DataCleanerService:
    """Service responsible for data validation and cleaning."""

    # Set of valid spending categories (Demonstrates Sets concept)
    VALID_CATEGORIES: Set[str] = {
        "Groceries", "Utilities", "Electronics",
        "Transport", "Dining", "Health", "Entertainment"
    }

    def clean_transactions(
        self, raw_records: List[Dict[str, str]]
    ) -> Tuple[List[Transaction], List[Dict[str, str]], Set[str]]:
        """
        Clean and validate raw dictionary records.
        Returns:
            - List of valid Transaction objects
            - List of rejected records (Dicts)
            - Set of unique merchants encountered
        """
        valid_transactions: List[Transaction] = []  # List concept
        rejected_records: List[Dict[str, str]] = []  # List concept
        unique_merchants: Set[str] = set()           # Set concept

        # Loop concept
        for record in raw_records:
            tx_id = record.get("id", "").strip()
            date = record.get("date", "").strip()
            merchant = record.get("merchant", "").strip()
            category = record.get("category", "").strip()
            amount_str = record.get("amount", "0").strip()

            # Conditional statements for data validation
            try:
                amount = float(amount_str)
            except ValueError:
                rejected_records.append(record)
                continue

            # Validation rules (amount > 0, valid category, non-empty metadata)
            if amount <= 0 or category not in self.VALID_CATEGORIES or not merchant:
                record["reason"] = "Invalid amount, missing merchant, or unknown category"
                rejected_records.append(record)
            else:
                # Tuple creation (tx_id, date, merchant)
                meta = TransactionMeta(tx_id=tx_id, date=date, merchant=merchant)
                tx = Transaction(meta=meta, category=category, amount=amount)

                valid_transactions.append(tx)
                unique_merchants.add(merchant)  # Add to Set

        return valid_transactions, rejected_records, unique_merchants
