from enum import Enum
from tools import Armor, Weapon


class UnitType(Enum):
    ARMOR = Armor
    WEAPON = Weapon


class ArmorUnits:
    def __init__(self, items: UnitType = []) -> None:
        self.items = items
        self.total_items = len(items)

    def __str__(self) -> str:
        return (f"Inventory: [{', '.join(str(item) for item in self.items)}], "
                f"Total items: {self.total_items}")
