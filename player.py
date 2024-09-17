from inventory import Inventory
from inventory_armor import ArmorUnits
from console import say, say_light
from time import sleep


class Player:
    def __init__(self):
        """
        Initialize a player object.

        :param name: The name of the player (default is "")
        :param hp: The health of the player (default is 100)
        :param max_hp: The maximum health of the player (default is 100)
        :param level: The level of the player (default is 1)
        :param xp: The experience points of the player (default is 0)
        :param mp: The magic points of the player (default is 100)
        :param max_mp: The maximum magic points of the player (default is 100)
        :param attack: The attack damage of the player (default is 10)
        :param MATK: The magic attack damage of the player (default is 20)
        :param MDEF: The magic defense of the player (default is 20)
        :param defense: The defense of the player (default is 10)
        :param speed: The speed of the player (default is 10)
        :param luck: The luck of the player (default is 10)
        :param coins: The coins of the player (default is 100)
        :param inventory: The inventory of the player (default is {})
        :param armor: The armor of the player (default is a dictionary with "helmet", "chestplate", "leggings", "boots", "weapon" as keys and empty Armor objects as values)
        """
        self.name = ""
        self.hp = 100
        self.max_hp = 100
        self.level = 1
        self.xp = 0  # Level Experience Points
        self.mp = 100  # Health
        self.max_mp = 100
        self.attack = 10  # Attack Damage
        self.MATK = 20  # Magic Attack Damage
        self.MDEF = 20  # Magic Defense
        self.defense = 10
        self.speed = 10
        self.luck = 10
        self.coins = 100
        self.inventory = Inventory()
        self.armor = ArmorUnits()

    def __str__(self):
        return f"{self.name}"

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 10
        self.mp = self.max_mp
        self.attack += 10
        self.MATK += 10
        self.MDEF += 10
        self.defense += 10
        self.speed += 1
        self.luck += 1

    def gain_xp(self, amount):
        self.xp += amount
        xp_required = self.level * 100  # Example: XP needed scales with level
        if self.xp >= xp_required:
            self.xp -= xp_required  # Carry over excess XP
            self.level_up()

    def add_item(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def remove_item(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] -= quantity
            if self.inventory[item] <= 0:
                del self.inventory[item]

    def view_armor(self):
        """
        Prints out the equipped armor.
        """
        say("Equipped Armor")
        say(f"Total Items: {self.armor.total_items}")
        if self.armor.total_items <= 0:
            return say("No armor equipped.", bottomBlank=True)
        for item in self.inventory.items:
            sleep(0.2)
            say(f"{item}")
        say_light("")

    def view_inventory(self):
        """
        Prints out the items in the player's inventory.
        """
        say("Inventory Items")
        say(f"Total Items: {self.inventory.total_items}")
        if self.inventory.total_items <= 0:
            return say("Inventory is empty.", bottomBlank=True)
        for item in self.inventory.items:
            sleep(0.2)
            say(f"{item}")
        say_light("")

    def use_mp(self, amount):
        if self.mp >= amount:
            self.mp -= amount
            return True  # Spell/ability was successful
        return False  # Not enough MP

    def recover_mp(self, amount):
        self.mp = min(self.max_mp, self.mp + amount)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)  # Prevent HP from going below 0
        if self.hp == 0:
            self.die()

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)  # Cap healing at max HP

    def die(self):
        say(f"{self.name} has died.")
        # Handle death logic (respawn, game over, etc.)

    def view_stats(self):
        say(f"👤  Name: {self.name}")
        say(f"⭐  Level: {self.level} (xp: {self.xp})")
        say(f"🪙  Coins: {self.coins}")
        say(f"❤️  HP: {self.hp} (max: {self.max_hp})")
        say(f"💙️  MP: {self.mp} (max: {self.max_mp})")
        say(f"⚔️  ATK: {self.attack}")
        say(f"⚔️  MATK: {self.MATK} (Magic Attack Damage)")
        say(f"🛡️  Defence: {self.defense}")
        say(f"🛡️  MDEF: {self.MDEF} (Magic Defence)")
        say(f"⚡️️speed: {self.speed}")
        say(f"☘️  Luck: {self.luck}")
        say(f"🎒  Inventory Items: {self.inventory.total_items}")
        say(f"🦺  Armor Items: {self.armor.total_items}")
        say_light("")
