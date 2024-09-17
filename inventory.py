from typing import List
from console import say
from tools import Weapon


class InventoryItem:
    def __init__(self, id: int = 0, name: str = None, quantity: int = 0, price: float = 0, item_data: dict = {}) -> None:
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.item_data = item_data

    def __str__(self) -> str:
        return f"{self.name} (Qty: {self.quantity}, Price: ${self.price:.2f})"


class Inventory:
    def __init__(self, items: List[InventoryItem] = [], max_items: int = 20) -> None:
        self.items = items
        self.total_items = len(items)
        self.max_items = max_items

    def __str__(self) -> str:
        return (f"Inventory: [{', '.join(str(item) for item in self.items)}], "
                f"Total items: {self.total_items}, Max items: {self.max_items}")

    def add_item(self, item: InventoryItem) -> None:
        if self.total_items < self.max_items:
            self.items.append(item)
            self.total_items += 1
        else:
            say("Inventory is full. Cannot add more items.", newline=True)

    def remove_item(self, item_name: str) -> None:
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                self.total_items = len(self.items)
                return
        say(f"Item '{item_name}' not found in inventory.", newline=True)
