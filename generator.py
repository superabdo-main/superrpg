import random
from inquirer import Confirm, Text, List, prompt
import string
import json
import os

class ItemGenerator:
    def __init__(self, pricing_rate=6):
        """
        Initialize the ItemGenerator with pricing rate.

        :param pricing_rate: The price multiplier for items (default is 3)
        """
        # Define base stat profiles for different item types
        self.base_stats = {
            "attack": {"attack": 10, "defence": 20, "speed": 2, "luck": 2, "MATK": 0},  # Physical weapon
            "magic": {"attack": 5, "defence": 3, "speed": 4, "luck": 3, "MATK": 12},  # Magic weapon
            "helmet": {"defence": 10, "speed": 1, "luck": 3},
            "chestplate": {"defence": 20, "speed": 1, "luck": 2},
            "leggings": {"defence": 18, "speed": 1, "luck": 2},
            "boots": {"defence": 10, "speed": 3, "luck": 3}
        }
        
        self.tier_multiplier = {
            "1": 1.0,  # Multiplier for Tier 1 items
            "2": 1.8   # Higher multiplier for Tier 2 items
        }
        self.pricing_rate = pricing_rate

    def calculate_rate(self, total_stats: int):
        """
        Calculate the drop rate based on total stats.
        Higher stats result in lower rates.
        """
        if total_stats <= 50:
            return random.randint(60, 99)
        elif total_stats <= 100:
            return random.randint(40, 60)
        else:
            return random.randint(10, 40)

    def generate_item_stats(self, name: str, item_type: str, tier: str, heat: int, weapon_type: str = None, armor_type: str = None):
        """
        Generate stats with variability based on heat.
        - `weapon_type`: for weapon items (either 'attack' or 'magic').
        - `heat`: controls the variability range.
        """
        # Select base stats profile
        if item_type == "weapon":
            if weapon_type not in ["attack", "magic"]:
                raise ValueError("Invalid weapon type. Choose 'attack' or 'magic'.")
            base = self.base_stats[weapon_type]
        elif item_type == "armor":
            if armor_type not in ["helmet", "chestplate", "leggings", "boots"]:
                raise ValueError("Invalid armor type. Choose 'helmet', 'chestplate', 'leggings', or 'boots'.")
            base = self.base_stats[armor_type]
        else:
            raise ValueError(f"Invalid item type: {item_type}")

        multiplier = self.tier_multiplier.get(tier, 1.0)

        # Generate item stats by applying tier multiplier and controlled heat-based random variations
        item_stats = {}
        total_value = 0  # For calculating pricing and rate

        for stat, value in base.items():
            # Controlled variation range
            # Increase the range for heat-based variability
            random_variation = random.uniform(1, 1 + heat / 100)
            
            # Apply tier multiplier and scale the stats more aggressively for higher tiers
            stat_value = int((value * multiplier) * random_variation)

            # Ensure no negative stats and apply minimum thresholds
            if stat == 'MATK':
                stat_value = max(5, stat_value)  # Minimum value for MATK
            else:
                stat_value = max(1, stat_value)  # Minimum value for other stats
            
            item_stats[stat] = stat_value
            total_value += stat_value

        # Add item name, type, and tier
        item_stats["name"] = name
        
        # item_stats["type"] = item_type
        if item_type == "armor":
            item_stats["type"] = armor_type
            
        item_stats["tier"] = "I" if tier == "1" else "II"
        item_stats["shop_available"] = True

        # Calculate price based on total stats value with stronger scaling
        item_stats["buy_price"] = int(total_value * self.pricing_rate * (multiplier * 1.2))
        item_stats["sell_price"] = int(item_stats["buy_price"] * 0.7)

        # Calculate drop rate based on total stats
        item_stats["rate"] = self.calculate_rate(total_value)

        return item_stats





class InventoryManager:
    def __init__(self):
        self.confirmed_items = []
        self.ids = []
        self.load_all_kits()

    def load_kit(self, kit_name: str):
        """
        Load a specific kit from a JSON file and return item IDs.

        Args:
            kit_name (str): Name of the kit file (without extension).
        """
        if os.path.exists(f"./kits/{kit_name}.json"):
            with open(f"./kits/{kit_name}.json", "r") as kit_file:
                data = json.load(kit_file)
                for item_id in data.keys():
                    self.ids.append(item_id)

    def load_all_kits(self):
        """Load all kits to populate IDs."""
        self.load_kit("weapons")
        self.load_kit("armor")
        self.load_kit("tools")


    def add_item(self, item):
        """Add an item to the confirmed list."""
        item['id'] = self.id_generator()
        if item['id'] not in self.ids:
            self.confirmed_items.append(item)

    def save_items(self, item_type):
        """Save confirmed items to the appropriate JSON file based on item type."""
        if item_type == 'weapon':
            file_name = 'weapons'
        elif item_type == 'armor':
            file_name = 'armor'
        else:
            raise ValueError(f"Invalid item type: {item_type}")
        
        # Load existing items from the file
        if os.path.exists(f"./kits/{file_name}.json"):
            with open(f"./kits/{file_name}.json", "r") as file:
                existing_items = json.load(file)
        else:
            existing_items = {}
            
        # Add confirmed items to the existing items
        for item in self.confirmed_items:
            existing_items[item['id']] = item
            existing_items[item['id']].pop('id', None)
            
        # Save the updated items back to the file
        with open(f"./kits/{file_name}.json", "w") as file:
            json.dump(existing_items, file, indent=4)

        self.confirmed_items = []

    def show_confirmed_items(self):
        """Display all confirmed items."""
        print("\nYour confirmed items:")
        for item in self.confirmed_items:
            print(item)

    def id_generator(self, size=4):
        """Generate a unique ID for an item."""
        while True:
            new_id = ''.join(random.choices(string.digits, k=size))
            if new_id not in self.ids:
                self.ids.append(new_id)
                return int(new_id)
            
            
class InteractivePrompt:
    def __init__(self):
        self.item_generator = ItemGenerator()
        self.inventory_manager = InventoryManager()

    def prompt_user(self):
        """Main function to run the user interaction loop."""
        while True:
            # Main item type selection
            item_question = [
                List('item_type', message="Choose item type", choices=['weapon', 'armor'])
            ]
            item_answer = prompt(item_question)
            item_type = item_answer['item_type']

            weapon_type = None
            armor_type = None
            
            if item_type == 'weapon':
                # If the item is a weapon, ask for weapon type
                weapon_type_question = [
                    List('weapon_type', message="Choose weapon type", choices=['attack', 'magic'])
                ]
                weapon_type_answer = prompt(weapon_type_question)
                weapon_type = weapon_type_answer['weapon_type']
                
            elif item_type == 'armor':
                # If the item is a weapon, ask for weapon type
                armor_type_question = [
                    List('armor_type', message="Choose armor type", choices=['helmet', 'chestplate', 'leggings', 'boots'])
                ]
                armor_type_answer = prompt(armor_type_question)
                armor_type = armor_type_answer['armor_type']

            # Generate items until confirmed by the user
            while True:
                item_stats = self.generate_item(item_type=item_type, weapon_type=weapon_type, armor_type=armor_type)
                print("\nGenerated Item Stats:")
                print(item_stats)

                # Ask user if they want to confirm this item
                confirm_question = [
                    Confirm('confirm', message="Do you want to keep this item?", default=True)
                ]
                confirm_answer = prompt(confirm_question)

                if confirm_answer['confirm']:
                    name_question = [
                        Text('name', message="Enter item name"),
                    ]
                    name_answer = prompt(name_question)
                    item_stats['name'] = name_answer['name']
                    self.inventory_manager.add_item(item_stats)
                    print("\nItem added to your confirmed list!")
                    break
                else:
                    print("\nGenerating a new item...")

            # Ask if the user wants to save the confirmed items
            save_question = [
                Confirm('save', message="Do you want to save the confirmed items to file?", default=True)
            ]
            save_answer = prompt(save_question)

            if save_answer['save']:
                self.inventory_manager.save_items(item_type)
                print(f"\nItems saved to {item_type}.json")

            # Ask if the user wants to generate a new item type
            reload_question = [
                Confirm('reload', message="Do you want to generate a new item type?", default=True)
            ]
            reload_answer = prompt(reload_question)

            if not reload_answer['reload']:
                break

        # After exiting the loop, display all confirmed items
        self.inventory_manager.show_confirmed_items()

    def generate_item(self, item_type, weapon_type=None, armor_type=None):
        """Generate an item based on user input."""
        # Ask for tier and heat
        tier_question = [
            Text('tier', message="Enter item tier (1 or 2)", default=1),
            Text('heat', message="Enter item heat (intensity of stats)", default=10)
        ]
        tier_answers = prompt(tier_question)

        # Generate item based on user input
        tier = tier_answers['tier']
        heat = int(tier_answers['heat'])

        name = 'RandomItem'  # Temporary name
        item_stats = self.item_generator.generate_item_stats(
            name=name,
            item_type=item_type,
            tier=tier,
            heat=heat,
            weapon_type=weapon_type,
            armor_type=armor_type
        )
        return item_stats


if __name__ == "__main__":
    InteractivePrompt().prompt_user()
