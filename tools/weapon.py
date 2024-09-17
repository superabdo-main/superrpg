

class Weapon:
    def __init__(self, id=0, name="", type="", attack=0, MATK=0, defence=0, luck=0, speed=0, buy_price=0, sell_price=0, tier="", rate=0, shop_available=True, equipped=False):
        """
        Initialize a weapon object.

        :param id: The id of the weapon (default is 0)
        :param name: The name of the weapon (default is "")
        :param attack: The physical attack of the weapon (default is 0)
        :param MATK: The magic attack of the weapon (default is 0)
        :param defence: The defence of the weapon (default is 0)
        :param luck: The luck of the weapon (default is 0)
        :param speed: The speed of the weapon (default is 0)
        :param buy_price: The price to buy the weapon (default is 0)
        :param sell_price: The price to sell the weapon (default is 0)
        :param tier: The tier of the weapon (default is "")
        :param rate: The rate or quality of the weapon (default is 0)
        :param shop_available: Whether the weapon is available in the shop (default is True)
        :param equipped: Whether the weapon is currently equipped (default is False)
        """

        self.id = id
        self.TID = "weapon"
        self.type = type
        self.name = name
        self.attack = attack
        self.MATK = MATK  # Magic attack
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
        return f"{self.name} (Tier {self.tier}): +{self.attack} Attack, +{self.MATK} MATK, +{self.defence} Defence, Price {self.buy_price} Gold"
