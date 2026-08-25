"""
FinSights Application Entry Point.
"""

from finsights.cli import FinSightsCLI


def main() -> None:
    """Initialize and run FinSights CLI application."""
    cli = FinSightsCLI(csv_path="data/sample_transactions.csv")
    cli.run()


if __name__ == "__main__":
    main()
