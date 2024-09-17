from enum import Enum
from typing import Dict, List
import inquirer as PR
from dataclasses import dataclass
from player import Player
from bazaar import Bazaar
from console import say, clear_clg, command as CCMD


class State(Enum):
    MAIN_MENU = 'main_menu'
    NEW_GAME = 'new_game'
    INVENTORY = 'inventory'
    BAZAAR = 'bazaar'
    STATS = 'stats'
    ARMOR = 'armor'
    EXIT = 'exit'

@dataclass
class StateConfig:
    commands: List[str]
    handler: callable

class Navigator:
    def __init__(self, player: Player, bazaar: Bazaar):
        self.player = player
        self.bazaar = bazaar
        self.history: List[State] = []
        self.current_state: State = State.MAIN_MENU
        self.state_config: Dict[State, StateConfig] = self._initialize_state_config()

    def _initialize_state_config(self) -> Dict[State, StateConfig]:
        return {
            State.MAIN_MENU: StateConfig(['Continue', 'New Game', 'Load Game', 'Settings', 'Exit'], self._handle_main_menu),
            State.NEW_GAME: StateConfig(['Move', 'Shop', 'Inventory', 'Armor', 'Stats', 'Back', 'Exit'], self._handle_new_game),
            State.BAZAAR: StateConfig(['Buy', 'Sell', 'Back'], self._handle_bazaar),
            State.INVENTORY: StateConfig(['View Items', 'Use Item', 'Back'], self._handle_inventory),
            State.ARMOR: StateConfig(['View Armor', 'Equip Armor', 'Back'], self._handle_armor),
            State.STATS: StateConfig(['Back'], self._handle_stats)
        }

    def navigate_to(self, state: State) -> None:
        """Navigate to a new state and store the current state in history."""
        self.history.append(self.current_state)
        self.current_state = state
        self.show_commands()

    def go_back(self) -> None:
        """Return to the previous state."""
        if self.history:
            self.current_state = self.history.pop()
        else:
            say("No previous state to return to.")
        self.show_commands()

    def show_commands(self) -> None:
        """Display available commands based on the current state."""
        if self.current_state == State.EXIT:
            raise SystemExit

        config = self.state_config.get(self.current_state)
        if not config:
            say(f"No configuration found for state: {self.current_state}")
            return

        command_choice = PR.List('command', 
                                 message=f"You're at {self.current_state.value.capitalize()}. Choose an action:",
                                 choices=config.commands)
        answer = PR.prompt([command_choice])
        self.handle_command(answer['command'])

    def handle_command(self, command: str) -> None:
        """Handle the chosen command."""
        clear_clg()
        config = self.state_config.get(self.current_state)
        if config and config.handler:
            config.handler(command)
        else:
            say(f"No handler found for state: {self.current_state}")

    def _handle_main_menu(self, command: str) -> None:
        if command == 'New Game':
            self.confirm_name()
            self.navigate_to(State.NEW_GAME)
        elif command == 'Exit':
            raise SystemExit
        else:
            say(f"{command} will be available soon.")
            self.show_commands()

    def _handle_new_game(self, command: str) -> None:
        if command == 'Shop':
            self.navigate_to(State.BAZAAR)
        elif command == 'Inventory':
            self.navigate_to(State.INVENTORY)
        elif command == 'Armor':
            self.navigate_to(State.ARMOR)
        elif command == 'Stats':
            self.player.view_stats()
            self.navigate_to(State.STATS)
        elif command == 'Back':
            self.go_back()
        elif command == 'Exit':
            raise SystemExit
        else:
            say(f"{command} will be available soon.")
            self.show_commands()

    def _handle_bazaar(self, command: str) -> None:
        if command == 'Buy':
            self.bazaar.show()
            self.show_commands()
        elif command == 'Back':
            self.go_back()
        else:
            say(f"{command} will be available soon.")
            self.show_commands()

    def _handle_inventory(self, command: str) -> None:
        self._handle_common_commands(command)

    def _handle_armor(self, command: str) -> None:
        self._handle_common_commands(command)

    def _handle_stats(self, command: str) -> None:
        self._handle_common_commands(command)

    def _handle_common_commands(self, command: str) -> None:
        if command == 'Back':
            self.go_back()
        else:
            say(f"{command} is under development.")
            self.show_commands()

    def confirm_name(self) -> None:
        """Prompt player to input their name"""
        while True:
            cmd = CCMD("What's Your Name: ")
            if cmd:
                self.player.name = cmd
                say(f"Hello, {self.player.name}!", bottomBlank=True)
                break
            else:
                say("Please enter a valid name.")