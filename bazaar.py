from typing import List
from tools import Weapon, Armor, Tool
import json
from console import say
from time import sleep
from modules import tier_design
from rich.table import Table
from rich.live import Live
from player import Player


class Bazaar:
    """
    Represents a bazaar where players can buy and sell items.
    """

    def __init__(self, player: Player, weapons: List[Weapon] = None, armors: List[Armor] = None, tools: List[Tool] = None) -> None:
        """
        Initialize the Bazaar with optional lists of weapons, armors, and tools.

        Args:
            weapons (List[Weapon], optional): List of weapons. Defaults to None.
            armors (List[Armor], optional): List of armors. Defaults to None.
            tools (List[Tool], optional): List of tools. Defaults to None.
        """
        self.weapons = weapons or []
        self.armors = armors or []
        self.tools = tools or []
        self.player = player
        self.load_kits()

    def load_kits(self) -> None:
        """
        Load item kits from JSON files and populate the bazaar's inventory.
        """
        self._load_kit("weapons", Weapon, self.weapons)
        self._load_kit("armor", Armor, self.armors)
        self._load_kit("tools", Tool, self.tools)

    def _load_kit(self, kit_name: str, item_class, item_list: list) -> None:
        """
        Load a specific kit from a JSON file and add items to the corresponding list.

        Args:
            kit_name (str): Name of the kit file (without extension).
            item_class: Class to instantiate for each item (Weapon, Armor, or Tool).
            item_list (list): List to append the loaded items to.
        """
        with open(f"./kits/{kit_name}.json", "r") as kit_file:
            data = json.load(kit_file)
            for item_id, item_data in data.items():
                if item_data.get("shop_available", True):
                    item_list.append(item_class(id=item_id, **item_data))
    
            
    def show(self) -> None:
        """
        Display the bazaar's inventory in a formatted table.
        """
        say("Welcome To Bazaar")
        say("Here are the items in the bazaar:")
        say("Total Coins:",f"[red]{self.player.coins}[/red]", bottomBlank=True)
        self._display_item_table(
            "Weapons", self.weapons, self._weapon_row_data)
        self._display_item_table("Armor", self.armors, self._armor_row_data)

    def _display_item_table(self, title: str, items: list, row_data_func) -> None:
        """
        Display a table of items with live updates.

        Args:
            title (str): Title of the table.
            items (list): List of items to display.
            row_data_func: Function to generate row data for each item.
        """
        say(f"{title} Total: {len(items)}")
        table = self._create_weapons_table(
            title) if title == "Weapons" else self._create_armor_table(title)
        with Live(table, refresh_per_second=4):
            for item in items:
                sleep(0.05)  # Arbitrary delay for visual effect
                table.add_row(*row_data_func(item))

    def _create_weapons_table(self, title: str) -> Table:
        """
        Create a Rich Weapons Table with predefined columns based on the item type.

        Args:
            title (str): Title of the table.

        Returns:
            Table: A Rich Table object with appropriate columns.
        """
        table = Table(title=title)
        columns = [
            ("ID", "cyan"), ("Name", "white"), ("Tier", "yellow"),
            ("Attack", "red"), ("Defence", "green"), ("MATK", "white"),
            ("Luck", "yellow"), ("Speed", "white"), ("Price", "red")
        ]
        for name, style in columns:
            table.add_column(name, style=style, no_wrap=True)
        return table

    def _create_armor_table(self, title: str) -> Table:
        """
        Create a Rich Armor Table with predefined columns based on the item type.

        Args:
            title (str): Title of the table.

        Returns:
            Table: A Rich Table object with appropriate columns.
        """
        table = Table(title=title)
        columns = [
            ("ID", "cyan"), ("Name", "white"), ("Type", "white"), ("Tier", "yellow"),
            ("Defence", "green"),
            ("Luck", "yellow"), ("Speed", "white"), ("Price", "red")
        ]
        for name, style in columns:
            table.add_column(name, style=style, no_wrap=True)
        return table

    def _weapon_row_data(self, weapon: Weapon) -> tuple:
        """
        Generate row data for a weapon.

        Args:
            weapon (Weapon): The weapon to generate data for.

        Returns:
            tuple: A tuple containing formatted weapon data.
        """
        return (
            str(weapon.id), weapon.name, tier_design(weapon.tier),
            str(weapon.attack), str(weapon.defence), str(weapon.MATK),
            str(weapon.luck), str(weapon.speed), f"{weapon.buy_price} coins"
        )

    def _armor_row_data(self, armor: Armor) -> tuple:
        """
        Generate row data for an armor piece.

        Args:
            armor (Armor): The armor to generate data for.

        Returns:
            tuple: A tuple containing formatted armor data.
        """
        return (
            str(armor.id), armor.name, armor.type, tier_design(armor.tier),
            str(armor.defence), str(armor.luck), str(armor.speed),
            f"{armor.buy_price} coins"
        )
