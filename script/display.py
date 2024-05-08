import os
import platform
import sys
import time
from colorama import Style
from rich.console import Console
from rich import print


class Display:
    def __init__(self):
        self.console = Console()

    def colored_input(self, prompt, color="green"):
        self.console.print(prompt, style=color, end="")
        user_input = input()
        return user_input

    def clear_screen(self):
        if platform.system() == 'Windows':
            os.system("cls")
        else:
            os.system("clear")

    def draw(self):
        print("[aquamarine3]++------------------------++[/]")

    def print_monster_info(self, name, health, attack, loot, items_required):
        # Table outline structure
        column_width = 30
        line = '-' * (column_width * 2 + 7)
        # Printing table header
        print(line)
        print(f"| [violet]{'Attribute':<{column_width}}[/] | [violet]{'Information':{column_width}}[/] |")
        print(line)
        print(f"| [yellow1]{'Name':<{column_width}}[/] | {name:<{column_width}} |")
        print(f"| [yellow1]{'Health':<{column_width}}[/] | {health:<{column_width}} |")
        print(f"| [yellow1]{'Attack':<{column_width}}[/] | {attack:<{column_width}} |")
        print(f"| [yellow1]{'Loot':<{column_width}}[/] | {loot:<{column_width}} |")
        items_str = ', '.join(items_required)
        print(f"| [yellow1]{'Items Needed':<{column_width}}[/] | {items_str:<{column_width}} |")
        print(line)
    #Changing the color of specific characters in the ascii art
    def print_ascii_art(self, file_path, mode='basic', hair_color=None, eye_color=None):
        with open(file_path, 'r') as file:
            ascii_art = file.read()

        if mode == 'character':
            placeholders = {'@': '<@>', '0': '<0>'}
            colored_strings = {'<@>': f'[{hair_color}]@[/]', '<0>': f'[{eye_color}]0[/]'}
        elif mode == 'items':
            placeholders = {
                '0': '<0>',
                'A': '<A>',
                'H': '<H>',
                '|': '<|>',
                '/': '</>',
                '-': '<->',
                '▆': '<▆>',
                'U': '<U>',
                '█': '<█>',
                '#': '<#>',
                '▄': '<▄>',
                'W': '<W>',
                'V': '<V>',
                'o': '<o>'
            }
            colored_strings = {
                '<0>': '[bright_white]0[/]',
                '<A>': '[cyan1]A[/]',
                '<H>': '[gold3]H[/gold3]',
                '<|>': '[red]|[/red]',
                '</>': '[red]/[/red]',
                '<->': '[red]-[/red]',
                '<▆>': '[bright_white]▆[/bright_white]',
                '<U>': '[yellow]U[/yellow]',
                '<█>': '[black]█[/black]',
                '<#>': '[grey50]#[/grey50]',
                '<▄>': '[green]▄[/green]',
                '<W>': '[light_pink4]W[/light_pink4]',
                '<V>': '[orange3]V[/orange3]',
                '<o>': '[hot_pink3]o[/]'
            }
        elif mode == 'monsters':
            placeholders = {
                '0': '<0>',
                '(': '<(>',
                ')': '<)>',
                '^': '<^>',
                'U': '<U>',
                '~': '<~>',
                'i': '<i>',
                'p': '<p>',
                'd': '<d>',
                'b': '<b>',
                'D': '<D>',
                '%': '<%>'
            }
            colored_strings = {
                '<0>': '[bright_white]0[/]',
                '<(>': '[khaki1]([/]',
                '<)>': '[khaki1])[/]',
                '<^>': '[khaki1]^|[/]',
                '<U>': '[sandy_brown]U[/]',
                '<~>': '[khaki1]~[/]',
                '<i>': '[plum2]i[/]',
                '<p>': '[dark_sea_green2]p[/]',
                '<b>': '[dark_sea_green2]b[/]',
                '<d>': '[dark_sea_green2]d[/]',
                '<D>': '[dark_sea_green2]D[/]',
                '<%>': '[green_yellow]%[/]'
            }
        else:
            return ascii_art
        #Replacing characters with placeholder
        for char, placeholder in placeholders.items():
            ascii_art = ascii_art.replace(char, placeholder)
        #Coloring the replaced characters
        for placeholder, colored in colored_strings.items():
            ascii_art = ascii_art.replace(placeholder, colored)

        return ascii_art
    def typing_effect(self, text, delay=0.03, color_words=None):
        def get_color(word, color_words):
            for key, color in color_words.items():
                if word.startswith(key):
                    return color, len(key)
            return None, 0

        i = 0
        while i < len(text):
            if color_words:
                color, length = get_color(text[i:], color_words)
                if color:
                    sys.stdout.write(color + text[i:i + length] + Style.RESET_ALL)
                    i += length
                    continue

            sys.stdout.write(text[i])
            sys.stdout.flush()
            time.sleep(delay)
            i += 1
    #Clearing the lines when users type the wrong information when creating a new account
    def clear_last_two_lines(self, num_lines):
        for _ in range(num_lines):
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')

