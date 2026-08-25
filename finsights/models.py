"""
Data models for FinSights application.
Uses NamedTuples, Dataclasses, and core data types.
"""

from dataclasses import dataclass
from typing import NamedTuple, Dict, Any


class TransactionMeta(NamedTuple):
    """
    Immutable metadata Tuple for transaction header.
    Demonstrates Tuple concept.
    """
    tx_id: str
    date: str
    merchant: str


@dataclass
class Transaction:
    """
    Transaction entity representation.
    Demonstrates Data Types: str, float, bool.
    """
    meta: TransactionMeta
    category: str
    amount: float
    is_flagged: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction entity to Dictionary."""
        return {
            "tx_id": self.meta.tx_id,
            "date": self.meta.date,
            "merchant": self.meta.merchant,
            "category": self.category,
            "amount": self.amount,
            "is_flagged": self.is_flagged
        }
