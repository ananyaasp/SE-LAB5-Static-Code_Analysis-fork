"""
inventory_system.py

A simple inventory system demonstrating safe coding practices:
- Input validation
- Proper file handling
- Specific exception handling
- Logging configuration
- PEP8-compliant naming and formatting
"""

import json
import logging
import os
from datetime import datetime
from json import JSONDecodeError
from typing import Dict, List, Optional

# Module-level inventory (kept simple for the lab)
stock_data: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0, logs: Optional[List[str]] = None) -> None:
    """
    Add `qty` of `item` to the inventory.

    Args:
        item: item name (must be str)
        qty: quantity to add (must be int)
        logs: optional list to append change messages to
    """
    if logs is None:
        logs = []

    # Input validation
    if not isinstance(item, str) or not item:
        logging.error("add_item: 'item' must be a non-empty string")
        return

    if not isinstance(qty, int):
        logging.error("add_item: 'qty' must be an integer")
        return

    previous = stock_data.get(item, 0)
    stock_data[item] = previous + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s (previous: %d, new: %d)", qty, item, previous, stock_data[item])


def remove_item(item: str, qty: int) -> None:
    """
    Remove `qty` of `item` from the inventory.

    Args:
        item: item name (must be str)
        qty: quantity to remove (must be int)
    """
    if not isinstance(item, str) or not item:
        logging.error("remove_item: 'item' must be a non-empty string")
        return

    if not isinstance(qty, int):
        logging.error("remove_item: 'qty' must be an integer")
        return

    try:
        current = stock_data[item]
    except KeyError:
        logging.warning("remove_item: item '%s' not found in stock", item)
        return

    new_qty = current - qty
    if new_qty <= 0:
        del stock_data[item]
        logging.info("remove_item: removed item '%s' from stock (was %d, removed %d)", item, current, qty)
    else:
        stock_data[item] = new_qty
        logging.info("remove_item: decreased '%s' from %d to %d", item, current, new_qty)


def get_qty(item: str) -> int:
    """
    Return the quantity for `item`. If item does not exist, returns 0.
    """
    if not isinstance(item, str) or not item:
        logging.error("get_qty: 'item' must be a non-empty string")
        return 0

    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """
    Load inventory data from a JSON file into module-level `stock_data`.
    If the file is missing or contains invalid JSON, starts with empty inventory.
    """
    if not isinstance(file, str) or not file:
        logging.error("load_data: 'file' must be a non-empty string")
        return

    if not os.path.exists(file):
        logging.info("load_data: file '%s' not found; using empty inventory", file)
        stock_data.clear()
        return

    try:
        with open(file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, dict):
                # ensure values are integers where possible
                stock_data.clear()
                for k, v in data.items():
                    try:
                        stock_data[str(k)] = int(v)
                    except (TypeError, ValueError):
                        logging.warning("load_data: skipping invalid qty for item '%s': %r", k, v)
                logging.info("load_data: loaded %d items from %s", len(stock_data), file)
            else:
                logging.warning("load_data: file %s does not contain a JSON object; starting empty", file)
                stock_data.clear()
    except (OSError, JSONDecodeError) as exc:
        logging.error("load_data: failed to read %s: %s", file, exc)
        stock_data.clear()


def save_data(file: str = "inventory.json") -> None:
    """
    Save module-level `stock_data` to a JSON file.
    """
    if not isinstance(file, str) or not file:
        logging.error("save_data: 'file' must be a non-empty string")
        return

    try:
        with open(file, "w", encoding="utf-8") as fh:
            json.dump(stock_data, fh, ensure_ascii=False, indent=2)
        logging.info("save_data: saved %d items to %s", len(stock_data), file)
    except OSError as exc:
        logging.error("save_data: failed to write %s: %s", file, exc)


def print_data() -> None:
    """
    Print a human-readable report of current stock.
    """
    logging.info("print_data: printing %d items", len(stock_data))
    print("Items Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold: int = 5) -> List[str]:
    """
    Return a list of items whose quantity is below `threshold`.
    """
    if not isinstance(threshold, int):
        logging.error("check_low_items: 'threshold' must be an integer")
        return []

    return [item for item, qty in stock_data.items() if qty < threshold]


def _demo_actions() -> None:
    """Populate some demo actions to illustrate the API (used by main)."""
    logs: List[str] = []
    add_item("apple", 10, logs)
    add_item("banana", 2, logs)
    # This invalid call will be rejected by validation:
    add_item(123, "ten", logs)  # type: ignore[arg-type]
    remove_item("apple", 3)
    remove_item("orange", 1)
    logging.debug("Demo logs: %s", logs)


def main() -> None:
    """
    Configure logging and exercise some functions for demonstration.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    logging.info("Starting inventory_system demo")

    # Load existing data (if any), perform demo actions, save and print
    load_data()
    _demo_actions()
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    print_data()
    
    # Removed dangerous eval usage from previous version
    logging.info("Removed unsafe eval() usage; program completed")

if __name__ == "__main__":
    main()
