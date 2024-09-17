import os
from rich import print


def clear_clg():
    """cleat console log"""
    clear = lambda: os.system("cls")
    clear()


def command(text: str = None) -> str:
    if text is not None:
        say(text)
    return input("➦ ")


def say(*objects: str, newline: bool = False, topBlank: bool = False, bottomBlank: bool = False):
    """with ● prefix"""
    if newline:
        print(" ")
        print("[#f4a261]●[/#f4a261]", *objects)
        print(" ")
        return
    if topBlank:
        print(" ")
    print("[#f4a261]●[/#f4a261]", *objects)
    if bottomBlank:
        print(" ")


def say_light(text: str):
    """without prefix"""
    print(text)


def continue_cmd():
    """type anything to continue"""
    input("Type anything to continue.")


def start_commands():
    say_light('''
[#f4a261]●[/#f4a261] Welcome To SuperRPG [#f4a261]●[/#f4a261]

[#f4a261]●[/#f4a261] 1: Continue
[#f4a261]●[/#f4a261] 2: New Game
[#f4a261]●[/#f4a261] 3: load Game
[#f4a261]●[/#f4a261] 4: Settings
[#f4a261]●[/#f4a261] 5: Exit (Too Difficult i'm afraid)
''')



