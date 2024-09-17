from enum import Enum


class ArmorType(Enum):
    CHESTPLATE = "chestplate"
    LEGGINGS = "leggings"
    HELMET = "helmet"
    BOOTS = "boots"
    WEAPON = "weapon"


class Armor:
    def __init__(self, id=0, name="", type: ArmorType = "", defence=0, luck=0, speed=0, buy_price=0, sell_price=0, tier=None, rate=0, shop_available=True, equipped=False):
        """
        Initialize an armor object.

        :param id: The id of the armor (default is 0)
        :param name: The name of the armor (default is None)
        :param type: The type of the armor (default is None)
        :param defence: The physical defence of the armor (default is 0)
        :param luck: The luck of the armor (default is 0)
        :param speed: The speed of the armor (default is 0)
        :param buy_price: The price to buy the armor (default is 0)
        :param sell_price: The price to sell the armor (default is 0)
        :param tier: The tier of the armor (default is None)
        :param rate: The rate or quality of the armor (default is 0)
        :param shop_available: Whether the armor is available in the shop (default is True)
        :param equipped: Whether the armor is currently equipped (default is False)
        """

        self.id = id
        self.TID = "armor"
        self.name = name
        self.type = type
        self.defence = defence
        self.luck = luck
        self.speed = speed
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.tier = tier
        self.rate = rate  # Quality or rarity
        self.shop_available = shop_available
        self.equipped = equipped

    def __str__(self) -> str:
        return f"{self.name} (Tier {self.tier}): Defence: {self.defence}, Price: {self.buy_price} Gold"
