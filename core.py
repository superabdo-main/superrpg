# Core game class
from player import Player
from bazaar import Bazaar
from console import clear_clg
from navigator import Navigator

class Core:
    def __init__(self) -> None:
        self.player = Player()
        self.bazaar = Bazaar(self.player)
        self.navigator = Navigator(self.player, self.bazaar)  # Initialize the Navigator class
        self.day = 1
        self.start()

    def start(self):
        """Main menu"""
        clear_clg()
        self.navigator.show_commands()  # Start navigation from MAIN_MENU

