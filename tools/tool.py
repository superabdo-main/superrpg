

class Tool:
    def __init__(self, id=0, name="", sell_price=0, tier="", rate=0, shop_available=False):
        """
        Initialize a Tool object.

        Args:
            id (int): Unique identifier for the Tool.
            name (str): Name of the Tool.
            sell_price (int): Price the Tool can be sold for.
            tier (str): Tier or level of the Tool.
            rate (int): Quality or rarity of the Tool.
        """
        self.id = id
        self.TID = "tool"
        self.name = name
        self.sell_price = sell_price
        self.tier = tier
        self.rate = rate  # Quality or rarity
        self.shop_available = shop_available

    def __str__(self) -> str:
        return f"{self.name} (Tier {self.tier}): Sell Price: {self.sell_price} Gold"
