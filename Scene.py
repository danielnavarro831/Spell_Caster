import xlrd
import random
from Files import Files
from Actor import *
import curses
import os
import time

class Scene():
    def __init__(self, Player, Game_State): #self, Class
        self.Speakers = Player.Speakers
        self.Error = False
        file = Files()
        self.path = file.doc_path
        file.__delete__()
        os.system('mode con: cols=120 lines=45')
        self.screen = curses.initscr()
        self.screen.clear()
        self.line = 0
        self.battle_line = 10
        self.Recipe = ""
        self.inventory_page = 1
        self.log = []
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.HP_bar = curses.color_pair(1)
        self.MP_bar = curses.color_pair(2)
        self.XP_bar = curses.color_pair(3)
        self.HP_low = curses.color_pair(4)
        self.green = curses.color_pair(5)
        self.cyan = curses.color_pair(6)
        self.yellow = curses.color_pair(7)
        self.red = curses.color_pair(8)
        self.white = curses.color_pair(9)
        self.Player = Player
        self.Game_State = Game_State

    def print_header(self, header_text): #self, "header_text"
        lines = []
        bar1 = "--------------------------"
        name_line = "  " + str(header_text)
        if len(bar1) < len(name_line):
            while len(bar1) < len(name_line) + 3:
                bar1 += "-"
        if len(name_line) < len(bar1) -2:
            while len(name_line) < len(bar1) -2:
                name_line += " "
        name_line += " /"
        bar2 = " ------------------------"
        if len(bar2) < len(bar1) -2:
            while len(bar2) < len(bar1) -2:
                bar2 += "-"
        lines.append(bar1)
        lines.append(name_line)
        lines.append(bar2)
        response = '\n'.join(lines)
        return response

    def print_message(self, Scene_Num, Print, Page, Vars): #self, int, Bool, "Page", {"{Vars}": "var"}
        #Get Page
        source = xlrd.open_workbook(self.path)
        if Page.title() == "Menu":
            Sheet = source.sheet_by_index(0)
        elif Page.title() == "Story":
            Sheet = source.sheet_by_index(1)
        elif Page.title() == "Room":
            Sheet = source.sheet_by_index(2)
        else:
            self.screen.addstr(1, 1, "Scene Eror: Page Error - Referenced string page not found or wrong page used")
            self.screen.refresh()
            self.Error = True
        #Check if individual message or scene
        scene = []
        text = ""
        if self.Error == False:
            if isinstance(Scene_Num, list):
                for num in range(len(Scene_Num)):
                    if len(Vars) > 0:
                        line = self.make_line(Scene_Num[num], Sheet, Vars[num])
                    else:
                        line = self.make_line(Scene_Num[num], Sheet, Vars)
                    scene.append(line)
            else:
                line = self.make_line(Scene_Num, Sheet, Vars)
                scene.append(line)
            if Print == True:
                for line in range(len(scene)):
                    self.clear_screen()
                    self.screen.addstr(self.line, 1, scene[line])
                    if "--" in scene[line]:
                        self.line += 4
                    else:
                        self.line += 1
                    if self.Game_State.story == True:
                        self.help_text(106, {})
                        response = self.Game_State.Controller.get_response(self.Player, False, self)
                    else:
                        response = self.screen.getstr(self.line, 1).decode('utf-8')
            else:
                text = '\n'.join(scene)
                return text  

    def make_line(self, Scene_num, Sheet, Vars): #self, int, "Sheet", {"{Vars}": "Var"}
        lines = []
        message = ""
        if type(Sheet) == str:
            source = xlrd.open_workbook(self.path)
            if Sheet == "Menu":
                Sheet = source.sheet_by_index(0)
            elif Sheet == "Story":
                Sheet = source.sheet_by_index(1)
            elif Sheet == "Room":
                Sheet = source.sheet_by_index(2)
            else:
                self.screen.addstr(self.line, 1, "Scene Eror: Page Error - Referenced string page not found or wrong page used")
        if Sheet.cell(Scene_num, 1).value:
            message += " "
            if Sheet.cell(Scene_num, 1).value in self.Speakers:
                name_line = self.Speakers[Sheet.cell(Scene_num, 1).value]
            else:
                name_line = "???"
            lines.append(self.print_header(name_line))
        message += str(Sheet.cell(Scene_num, 0).value)
        if len(Vars) > 0:
            for key in Vars.keys(): 
                if isinstance(Vars[key], list):
                    counter = 1
                    for var in range(len(Vars[key])):
                        message = message.replace(key, str(Vars[key][var]), counter)
                        counter += 1
                else:
                    message = message.replace(key, str(Vars[key]))
        lines.append(message)
        line = '\n'.join(lines)
        return line

    def make_no_header_line(self, Scene_num, Sheet, Vars): #self, int, "Sheet", {"{Vars}": "Var"}
        lines = []
        message = ""
        if type(Sheet) == str:
            source = xlrd.open_workbook(self.path)
            if Sheet == "Menu":
                Sheet = source.sheet_by_index(0)
            elif Sheet == "Story":
                Sheet = source.sheet_by_index(1)
            elif Sheet == "Room":
                Sheet = source.sheet_by_index(2)
            else:
                self.screen.addstr(self.line, 1, "Scene Eror: Page Error - Referenced string page not found or wrong page used")
        message += str(Sheet.cell(Scene_num, 0).value)
        if len(Vars) > 0:
            for key in Vars.keys(): 
                if isinstance(Vars[key], list):
                    counter = 1
                    for var in range(len(Vars[key])):
                        message = message.replace(key, str(Vars[key][var]), counter)
                        counter += 1
                else:
                    message = message.replace(key, str(Vars[key]))
        lines.append(message)
        line = '\n'.join(lines)
        return line

    def find_keyword(self, Keyword, Message):
        word_list = Message.split(Keyword)
        location = len(word_list[0]) + 1
        return location

    def pin_line(self, Y, X, Message, Color):
        color = ""
        if Color == "Green":
            color = self.green
        elif Color == "Cyan":
            color = self.cyan
        elif Color == "Red":
            color = self.red
        elif Color == "Yellow":
            color = self.yellow
        else:
            color = self.white
        self.screen.addstr(Y, X, Message, color)

    def line_randomizer(self, Scene_nums, Page, Vars): #self, [list, of, scenes], "Menu", [{}, {Vars: 1}, {Vars:2}]
        source = xlrd.open_workbook(self.path)
        if Page.title() == "Menu":
            Sheet = source.sheet_by_index(0)
        elif Page.title() == "Story":
            Sheet = source.sheet_by_index(1)
        else:
            self.screen.addstr(self.line, 1, " Scene Eror: Page Error - Referenced string page not found or wrong page referenced")
            self.Error = True
        if self.Error == False:
            lines = []
            randomizer = random.randint(0, len(Scene_nums) -1)
            if Sheet.cell(Scene_nums[randomizer], 1).value:
                if Sheet.cell(Scene_nums[randomizer], 1).value in self.Speakers:
                    name_line = self.Speakers[Sheet.cell(Scene_nums[randomizer], 1).value]
                else:
                    name_line = " ???"
                lines.append(self.print_header(name_line))
            message = str(Sheet.cell(Scene_nums[randomizer], 0).value)
            if len(Vars) > 0:
                for var in range(len(Vars)):
                    for key in Vars[var].keys(): 
                        if isinstance(Vars[var][key], list):
                            counter = 1
                            for thing in range(len(Vars[var][key])):
                                message = message.replace(key, str(Vars[var][key][thing]), counter)
                                counter += 1
                        else:
                            message = message.replace(key, str(Vars[var][key]))
            lines.append(message)
            line_break = ""
            lines.append(line_break)
            text = '\n'.join(lines)
            return text

    def get_interactable_string(self, Interactable, Command, Player): #self, Class, Class, Class
        var_dic = {"Interactable.Name": Interactable.Name, "Player.Name": Player.Name["Value"], 
                   "Player.Fire": Player.Fire["Name"], "Player.Ice": Player.Ice["Name"], "Player.Lightning": Player.Lightning["Name"],
                   "Player.Water": Player.Water["Name"], "Player.Wind": Player.Wind["Name"]}
        source = xlrd.open_workbook(self.path)
        Sheet = source.sheet_by_index(3)
        line = ""
        loop = True
        row = 0
        column = 0
        name = ""
        while loop == True:
            if type(Interactable.Name) is not list:
                name = Interactable.Name
            else:
                name = Interactable.Name[0]
            if Sheet.cell(row, column).value in name:
                column += 1
                loop = False
                loop2 = True
                while loop2 == True:
                    if Sheet.cell(row, column).value == Command:
                        column += 1
                        line = str(Sheet.cell(row, column).value)
                        column += 1
                        if Sheet.cell(row, column).value:
                            vars_string = Sheet.cell(row, column).value
                            vars = vars_string.split(', ')
                            for var in range(len(vars)):
                                vars[var] = vars[var].strip("'")
                                if vars[var] in var_dic:
                                    vars[var] = var_dic[vars[var]]
                                elif "Key." in vars[var]:
                                    a = vars[var].split('.')
                                    b = a[-1]
                                    for c in range(len(Interactable.Keys)):
                                        if Interactable.Keys[c]["Name"] == b:
                                            vars[var] = Interactable.Keys[c]["Name"]
                            Vars = {"{Var}": vars}
                            for a in range(len(Vars["{Var}"])):
                                line = line.replace("{Var}", str(Vars["{Var}"][a]), 1)
                        loop2 = False
                    else:
                        row += 1
            else:
                row += 1
        return line

    def __delete__(self):
        del self

    def clear_screen(self):
        self.line = 0
        if self.Game_State.story == True:
            for x in range(0, 12):
                self.screen.addstr(x, 0, "                                                                                                                      ")
            for y in range(12, 32):
                self.screen.addstr(y, 0, "                                                                                      ")
            self.Game_State.Story_UI(self.Player, self, self.Game_State.Controller)
        else:
            self.screen.clear()

    def help_text(self, Scene_num, Vars):
        clear = ""
        for i in range(0, 89):
            clear += " "
        self.screen.addstr(32, 0, clear)
        message = ""
        if Scene_num != 0:
            source = xlrd.open_workbook(self.path)
            Sheet = source.sheet_by_index(0)
            message += str(Sheet.cell(Scene_num, 0).value)
            if len(Vars) > 0:
                for key in Vars.keys(): 
                    if isinstance(Vars[key], list):
                        counter = 1
                        for var in range(len(Vars[key])):
                            message = message.replace(key, str(Vars[key][var]), counter)
                            counter += 1
                    else:
                        message = message.replace(key, str(Vars[key]))
            self.screen.addstr(32, 1, ">>> " + message, self.yellow)
        else:
            self.screen.addstr(32, 1, message)
#---------------------------------------------------------------------------------------------------------------------------------
#                                                             Curses - Battle Window Display
#---------------------------------------------------------------------------------------------------------------------------------
    def enemy_HUD(self, Enemy):
        self.screen.addstr("____________________________________________________")
        self.screen.addstr(1, 1, Enemy.Name["Value"], self.cyan)
        self.screen.addstr(1, 19, "Lvl. " + str(Enemy.Level["Value"]), self.yellow)
        self.screen.addstr(1, 29, "|")
        self.screen.addstr(2, 0, "-----------------------------|")
        self.screen.addstr(3, 4, "__________")
        self.render_stat_bar(Enemy, "HP", 4)
        self.screen.addstr(2, 29, "|")
        self.render_stat_bar(Enemy, "MP", 5)
        self.screen.addstr(3, 29, "|")
        self.screen.addstr(4, 29, "|")
        self.screen.addstr(5, 29, "|")
        self.screen.addstr(6, 29, "|")
        self.screen.addstr(7, 0, "_____________________________|______________________|")
        self.screen.addstr(0, 52, "|")
        self.screen.addstr(1, 52, "|")
        self.screen.addstr(2, 52, "|")
        self.screen.addstr(3, 52, "|")
        self.screen.addstr(4, 52, "|")
        self.screen.addstr(5, 52, "|")
        self.screen.addstr(6, 52, "|")
        self.screen.addstr(1, 31, "Active Spells:", self.cyan)

    def player_HUD(self, Player, Game):
        self.screen.addstr(33, 0, "_____________________________ ")
        self.screen.addstr(34, 29, "\\")
        if Game.battle == True:
            self.screen.addstr(42, 0, "_____________________________|______________________|___________________________________________________________________")
        elif Game.brewing == True:
            self.screen.addstr(42, 0, "_____________________________|__________________________________________________________________________________________")
        else:
            self.screen.addstr(42, 0, "_____________________________|___________________________________________________________|______________________________")
        self.screen.addstr(35, 0, "-----------------------------|")
        self.screen.addstr(36, 29, "|")
        self.screen.addstr(37, 29, "|")
        self.screen.addstr(38, 29, "|")
        self.screen.addstr(39, 29, "|")
        self.screen.addstr(40, 29, "|")
        self.screen.addstr(41, 29, "|")
        if Game.battle == True:
            self.screen.addstr(35, 52, "|")
            self.screen.addstr(36, 52, "|")
            self.screen.addstr(37, 52, "|")
            self.screen.addstr(38, 52, "|")
            self.screen.addstr(39, 52, "|")
            self.screen.addstr(40, 52, "|")
            self.screen.addstr(41, 52, "|")
        self.screen.addstr(34, 1, Player.Name["Value"], self.cyan)
        self.screen.addstr(34, 19, "Lvl. " + str(Player.Level["Value"]), self.yellow)
        self.screen.addstr(36, 4, "__________")
        self.render_stat_bar(Player, "HP", 37)
        self.render_stat_bar(Player, "MP", 38)
        self.render_stat_bar(Player, "XP", 39)
        if Game.battle == True:
            self.screen.addstr(35, 31, "Active Spells:", self.cyan)

    def inventory_list(self, Player, Game):
        X = 30
        if Game.battle == True:
            X += 21
        else:
            for i in range(35, 43):
                self.screen.addstr(i, 89, "|")
        self.screen.addstr(34, X, "___________________________________________________________")
        if Game.battle == True:
            self.screen.addstr("__________")
            X += 2
        for a in range(6):
            self.screen.addstr(35 + a, X, "                                                           ")
            if Game.battle == True:
                self.screen.addstr("        ")
        self.screen.addstr(35, X+1, "Items: ", self.cyan)
        if self.inventory_page == 1: #HP/MP Restorers
            column1 = X + 1
            column2 = column1 + 20
            column3 = column2 + 19
            #Column 1 - Potions
            if "Potion" in Player.Inventory:
                if Player.Inventory["Potion"] > 0:
                    self.screen.addstr(36, column1, "*", self.yellow)
                    self.screen.addstr(" Potion ")
                    self.screen.addstr("x" + str(Player.Inventory["Potion"]), self.cyan)
            if "Hi-Potion" in Player.Inventory:
                if Player.Inventory["Hi-Potion"] > 0:
                    self.screen.addstr(37, column1, "*", self.yellow)
                    self.screen.addstr(" Hi-Potion ")
                    self.screen.addstr("x" + str(Player.Inventory["Hi-Potion"]), self.cyan)
            if "Mega-Potion" in Player.Inventory:
                if Player.Inventory["Mega-Potion"] > 0:
                    self.screen.addstr(38, column1, "*", self.yellow)
                    self.screen.addstr(" Mega-Potion ")
                    self.screen.addstr("x" + str(Player.Inventory["Mega-Potion"]), self.cyan)
            if "Unstable Potion" in Player.Inventory:
                if Player.Inventory["Unstable Potion"] > 0:
                    self.screen.addstr(39, column1, "*", self.yellow)
                    self.screen.addstr(" Unstable Potion ")
                    self.screen.addstr("x" + str(Player.Inventory["Unstable Potion"]), self.cyan)
            #Column 2 - Ethers
            if "Ether" in Player.Inventory:
                if Player.Inventory["Ether"] > 0:
                    self.screen.addstr(36, column2, "*", self.yellow)
                    self.screen.addstr(" Ether ")
                    self.screen.addstr("x" + str(Player.Inventory["Ether"]), self.cyan)
            if "Hi-Ether" in Player.Inventory:
                if Player.Inventory["Hi-Ether"] > 0:
                    self.screen.addstr(37, column2, "*", self.yellow)
                    self.screen.addstr(" Hi-Ether ")
                    self.screen.addstr("x" + str(Player.Inventory["Hi-Ether"]), self.cyan)
            if "Mega-Ether" in Player.Inventory:
                if Player.Inventory["Mega-Ether"] > 0:
                    self.screen.addstr(38, column2, "*", self.yellow)
                    self.screen.addstr(" Mega-Ether ")
                    self.screen.addstr("x" + str(Player.Inventory["Mega-Ether"]), self.cyan)
            #Column 3 - Elixirs
            if "Elixir" in Player.Inventory:
                if Player.Inventory["Elixir"] > 0:
                    self.screen.addstr(36, column3, "*", self.yellow)
                    self.screen.addstr(" Elixir ")
                    self.screen.addstr("x" + str(Player.Inventory["Elixir"]), self.cyan)
            if "Hi-Elixir" in Player.Inventory:
                if Player.Inventory["Hi-Elixir"] > 0:
                    self.screen.addstr(37, column3, "*", self.yellow)
                    self.screen.addstr(" Hi-Elixir ")
                    self.screen.addstr("x" + str(Player.Inventory["Hi-Elixir"]), self.cyan)
            if "Mega-Elixir" in Player.Inventory:
                if Player.Inventory["Mega-Elixir"] > 0:
                    self.screen.addstr(38, column3, "*", self.yellow)
                    self.screen.addstr(" Mega-Elixir ")
                    self.screen.addstr("x" + str(Player.Inventory["Mega-Elixir"]), self.cyan)
        elif self.inventory_page == 2: #Resisters/Spell Absorbers
            column1 = X+1
            column2 = column1 + 29
            if "Fire Resistance" in Player.Inventory:
                if Player.Inventory["Fire Resistance"] > 0:
                    self.screen.addstr(36, column1, "*", self.yellow)
                    self.screen.addstr(" Fire Resistance ")
                    self.screen.addstr("x" + str(Player.Inventory["Fire Resistance"]), self.cyan)
            if "Ice Resistance" in Player.Inventory:
                if Player.Inventory["Ice Resistance"] > 0:
                    self.screen.addstr(37, column1, "*", self.yellow)
                    self.screen.addstr(" Ice Resistance ")
                    self.screen.addstr("x" + str(Player.Inventory["Ice Resistance"]), self.cyan)
            if "Water Resistance" in Player.Inventory:
                if Player.Inventory["Water Resistance"] > 0:
                    self.screen.addstr(38, column1, "*", self.yellow)
                    self.screen.addstr(" Water Resistance ")
                    self.screen.addstr("x" + str(Player.Inventory["Water Resistance"]), self.cyan)
            if "Wind Resistance" in Player.Inventory:
                if Player.Inventory["Wind Resistance"] > 0:
                    self.screen.addstr(39, column1, "*", self.yellow)
                    self.screen.addstr(" Wind Resistance ")
                    self.screen.addstr("x" + str(Player.Inventory["Wind Resistance"]), self.cyan)
            if "Lightning Resistance" in Player.Inventory:
                if Player.Inventory["Lightning Resistance"] > 0:
                    self.screen.addstr(40, column1, "*", self.yellow)
                    self.screen.addstr(" Lightning Resistance ")
                    self.screen.addstr("x" + str(Player.Inventory["Lightning Resistance"]), self.cyan)
            if "Fire Absorption" in Player.Inventory:
                if Player.Inventory["Fire Absorption"] > 0:
                    self.screen.addstr(36, column2, "*", self.yellow)
                    self.screen.addstr(" Fire Absorption ")
                    self.screen.addstr("x" + str(Player.Inventory["Fire Absorption"]), self.cyan)
            if "Ice Absorption" in Player.Inventory:
                if Player.Inventory["Ice Absorption"] > 0:
                    self.screen.addstr(37, column2, "*", self.yellow)
                    self.screen.addstr(" Ice Absorption ")
                    self.screen.addstr("x" + str(Player.Inventory["Ice Absorption"]), self.cyan)
            if "Water Absorption" in Player.Inventory:
                if Player.Inventory["Water Absorption"] > 0:
                    self.screen.addstr(38, column2, "*", self.yellow)
                    self.screen.addstr(" Water Absorption ")
                    self.screen.addstr("x" + str(Player.Inventory["Water Absorption"]), self.cyan)
            if "Wind Absorption" in Player.Inventory:
                if Player.Inventory["Wind Absorption"] > 0:
                    self.screen.addstr(39, column2, "*", self.yellow)
                    self.screen.addstr(" Wind Absorption ")
                    self.screen.addstr("x" + str(Player.Inventory["Wind Absorption"]), self.cyan)
            if "Lightning Absorption" in Player.Inventory:
                if Player.Inventory["Lightning Absorption"] > 0:
                    self.screen.addstr(40, column2, "*", self.yellow)
                    self.screen.addstr(" Lightning Absorption ")
                    self.screen.addstr("x" + str(Player.Inventory["Lightning Absorption"]), self.cyan)

    def spellbook_display(self, Player, Game):
        Y = 42
        if Game.battle == True:
            Y-=8
            for i in range(13):
                self.screen.addstr(Y - i, 89, "|")
        else:
            for i in range(8, 13):
                self.screen.addstr(Y - i, 89, "|")
        known_spells = Player.get_known_spells()
        for i in range(len(known_spells)):
            Cost = Player.calculate_MP(Player.Spells[known_spells[i]])
            line = known_spells[i] + " ("
            location = Y-12
            self.screen.addstr(location + i, 91, "                          ")
            self.screen.addstr(location + i, 91, "* ", self.yellow)
            self.screen.addstr(line)
            self.screen.addstr(str(Cost), self.cyan)
            self.screen.addstr(" MP)")
        self.screen.addstr(Y-13, 89, "|------------------------------")
        self.screen.addstr(Y-14, 89, "|")
        if Game.story == True and Game.in_tower == True:
            self.screen.addstr(Y-15, 89, "|==============================")
        else:
            self.screen.addstr(Y-15, 90, "______________________________")
        self.screen.addstr(Y-14, 100, "Spellbook", self.cyan)

    def turn_counter(self, Game):
        self.screen.addstr(8, 1, "Turn ")
        self.screen.addstr(str(Game.turn), self.yellow)
        self.screen.addstr(8, 52, "/")
        self.screen.addstr(9, 0, "---------------------------------------------------/")

    def command_line(self):
        self.screen.addstr(43, 1, "Enter ")
        self.screen.addstr("Command", self.yellow)
        self.screen.addstr(": ")

    def get_percentage(self, Actor, Stat):
        if Stat == "HP":
            amount = int((Actor.HP["Value"]/Actor.HP["Max"]) * 100)
        elif Stat == "MP":
            amount = int((Actor.MP["Value"]/Actor.MP["Max"]) * 100)
        else:
            amount = int((Actor.XP["Value"]/Actor.XP["Max"]) * 100)
        return amount

    def render_stat_bar(self, Actor, Stat, line):
        bar = ""
        color = ""
        location = line
        difference = 0
        current_stat = 0
        max_stat = 0
        minus_1 = False
        self.screen.addstr(location, 15, "            ")
        for a in range(int(self.get_percentage(Actor, Stat)/10)):
            if Stat == "XP":
                bar += "_"
            else:
                if Stat == "MP" and Actor.player == False:
                    bar += "_"
                else:
                    bar += " "
            if a > 10:
                break
        if len(bar) < 1 and Stat != "XP":
            if Stat == "HP":
                if Actor.HP["Value"] > 0:
                    bar += " "
                    minus_1 = True
            else:
                if Actor.MP["Value"] > 0:
                    bar += " "
                    minus_1 = True
        self.screen.addstr(location, 1, Stat)
        self.screen.addstr("|")
        if Stat == "HP" and int(self.get_percentage(Actor, Stat)/10) > 5:
            color = self.HP_bar
        elif Stat == "HP" and int(self.get_percentage(Actor, Stat)/10) <=5 and int(self.get_percentage(Actor, Stat)/10) > 2:
            color = self.XP_bar
        elif Stat == "HP" and int(self.get_percentage(Actor, Stat)/10) <= 2:
            color = self.HP_low
        elif Stat == "MP":
            color = self.MP_bar
        else:
            color = self.XP_bar
        self.screen.addstr(bar, color)
        if int(self.get_percentage(Actor, Stat)/10) < 10:
            difference = 10 - int(self.get_percentage(Actor, Stat)/10)
            if minus_1 == True:
                difference -= 1
            for a in range(difference):
                if Stat != "XP":
                    if Stat == "MP" and Actor.player == False:
                        self.screen.addstr("_")
                    else:
                        self.screen.addstr(" ")
                else:
                    self.screen.addstr("_")
        self.screen.addstr("| ")
        if Stat == "HP":
            current_stat = Actor.HP["Value"]
            max_stat = Actor.HP["Max"]
        elif Stat == "MP":
            current_stat = Actor.MP["Value"]
            max_stat = Actor.MP["Max"]
        else:
            current_stat = Actor.XP["Value"]
            max_stat = Actor.XP["Max"]
        self.screen.addstr(str(current_stat) + "/" + str(max_stat))

    def battle_log(self):
        log_line = self.battle_line
        if len(self.log) < 10:
            for i in range(len(self.log)):
                text = self.log[i]
                self.screen.addstr(log_line, 1, "* ", self.green)
                self.screen.addstr(text)
                log_line += 1
        else:
            start = len(self.log) - 10
            for i in range(start, self.log[-1]):
                text = self.log[i]
                self.screen.addstr(log_line, 1, "* ", self.green)
                self.screen.addstr(text)
                log_line += 1

    def active_spells(self, Player):
        d_spells = [Player.Regen["Name"], Player.Curse["Name"], Player.Sand["Name"], Player.Protect["Name"], Player.Shell["Name"]]
        Y = 36
        self.screen.addstr(34, 30, "_____________________")
        if Player.player == False:
            Y = 2
        for a in range(len(d_spells)):
            self.screen.addstr(Y+a, 31, "                     ")
            #self.screen.refresh()
            if Player.Spells[d_spells[a]]["Active"] == True:
                self.screen.addstr(Y + a, 31, "*", self.yellow)
                self.screen.addstr(" " + Player.Spells[d_spells[a]]["Name"] + "(")
                self.screen.addstr(str(Player.Spells[d_spells[a]]["Duration"]), self.cyan)
                self.screen.addstr(" Turns)")

    def tower_map(self, Game):
        Y = 26
        rooms = 0
        for z in range(16):
            self.screen.addstr(Y-z, 90, "                              ")
        seen_flags = [Game.tower_entrance, Game.tower1, Game.tower2, Game.tower3, Game.tower4, Game.tower5,
                      Game.dungeon1, Game.dungeon2, Game.dungeon3, Game.dungeon4, Game.dungeon5]
        for a in range(len(seen_flags)):
            if seen_flags[a] == True:
                rooms += 1
        for b in range(rooms + 1):
            self.screen.addstr(Y-b, 89, "|")
        tower_floors = [Game.tower_entrance, Game.tower1, Game.tower2, Game.tower3, Game.tower4, Game.tower5]
        dungeon_floors = [Game.dungeon1, Game.dungeon2, Game.dungeon3, Game.dungeon4, Game.dungeon5]
        tower_names = ["Tower Entrance", "Cold Room", "Cauldron Room", "Death Room", "Generator Room", "Top of the Tower"]
        dungeon_names = ["Fire Dungeon", "Ice Dungeon", "Water Dungeon", "Wind Dungeon", "Lightning Dungeon"]
        top_floor = 0
        bottom_floor = 0
        for c in range(len(tower_floors)):
            if tower_floors[c] == True:
                top_floor += 1
        for d in range(len(dungeon_floors)):
            if dungeon_floors[d] == True:
                bottom_floor += 1
        for e in range(top_floor):
            self.screen.addstr(Y - (top_floor + bottom_floor) + e, 95, "[ ]")
            self.screen.addstr(Y - (top_floor + bottom_floor) + e, 99, tower_names[(top_floor-1) - e])
            if tower_names[(top_floor-1) - e] == Game.current_floor:
                self.screen.addstr(Y - (top_floor + bottom_floor) + e, 96, "*", self.green)
        if bottom_floor > 0:
            self.screen.addstr(Y - bottom_floor, 94, "-----")
            for f in range(bottom_floor):
                self.screen.addstr((Y+1) - (bottom_floor) + f, 95, "[ ]")
                self.screen.addstr((Y+1) - (bottom_floor) + f, 99, dungeon_names[f])
                if dungeon_names[f] == Game.current_floor:
                    self.screen.addstr((Y+1) - (bottom_floor) + f, 96, "*", self.green)
        header = (Y - rooms) - 1
        self.screen.addstr(header, 89, "|------------------------------")
        self.screen.addstr(header-1, 100, "Tower Map", self.cyan)
        self.screen.addstr(header-1, 89, "|")
        self.screen.addstr(header-2, 90, "______________________________")

    def victory_screen(self, Player, Enemy, Game):
        self.clear_screen()
        self.screen.addstr(self.line, 1, self.print_header("Victory"))
        self.line += 3 
        self.screen.addstr(self.line, 1, "* ", self.green)
        self.screen.addstr(self.make_line(36, "Menu", {"{Name}": Enemy.Name["Value"]}))
        self.line += 1
        self.help_text(106, {})
        Enemy.drop_loot(Player, self)

    def potion_brew_screen(self, Player, Game):
        ingredients = Files()
        ing_list = ingredients.get_ingredient_list()
        self.player_HUD(Player, Game)
        self.screen.addstr(34, 30, "___________________________________________________________|______________________________")
        #Display Ingredient List
        self.screen.addstr(35, 31, "Ingredients: ", self.cyan)
        for z in range(36, 42):
            self.screen.addstr(z, 30, "                                                                                          ")
        col1 = 31
        col2 = col1 + 29
        col3 = col2 + 29
        counter = 1
        X = 0
        top_line = 35
        for a in Player.Inventory.keys():
            if a in ing_list:
                if Player.Inventory[a] > 0:
                    if counter < 7:
                        X = col1
                        Y = top_line + counter
                    elif counter > 6 and counter < 13:
                        X = col2
                        Y = (top_line + counter) - 6
                    else:
                        X = col3
                        Y = (top_line + counter) - 12
                    self.screen.addstr(Y, X, "* ", self.yellow)
                    self.screen.addstr(a)
                    self.screen.addstr(" x" + str(Player.Inventory[a]), self.cyan)
                    counter += 1
        #Display Recipes
        Y = 33
        for b in range(len(Player.Recipes)):
            self.screen.addstr(Y-b, 89, "|")
        self.screen.addstr(Y - len(Player.Recipes), 89, "|------------------------------")
        self.screen.addstr(Y - (len(Player.Recipes)+1), 89, "|")
        self.screen.addstr(Y - (len(Player.Recipes)+1), 100, "Recipes", self.cyan)
        self.screen.addstr(Y - (len(Player.Recipes)+2), 90, "_____________________________")
        Y = 33 - len(Player.Recipes)
        Y += 1
        for c in range(len(Player.Recipes)):
            self.screen.addstr(Y + c, 91, "* ", self.yellow)
            self.screen.addstr(Player.Recipes[c])
        #Make Header
        self.line = 0
        for d in range(30):
            self.screen.addstr(d, 0, "                                                                                         ")
        if self.Recipe not in Player.Recipes:
            self.screen.addstr(self.line, 1, self.print_header("Brew Potions"))
            self.line += 3
            self.screen.addstr(self.line, 1, self.make_line(63, "Menu", {}))
            self.line += 2
        else:
            self.screen.addstr(self.line, 1, self.print_header(self.Recipe + " Recipe"))
            self.line += 3
            recipe = ingredients.get_recipe(self.Recipe)
            for e in range(len(recipe)):
                if recipe[e] in Player.Inventory:
                    if Player.Inventory[recipe[e]] > 0:
                        self.screen.addstr(self.line, 1, "* ", self.yellow)
                    else:
                        self.screen.addstr(self.line, 1, "* ", self.red)
                else:
                    self.screen.addstr(self.line, 1, "* ", self.red)
                self.screen.addstr(recipe[e])
                self.line += 1
            self.line += 1
            self.screen.addstr(self.line, 1, self.make_line(63, "Menu", {}))
            self.line += 2
        ingredients.__delete__()
        #Make Cauldron
        self.screen.addstr(23, 3, "_________________________")
        self.screen.addstr(24, 2, "/_________________________\\")
        self.screen.addstr(25, 1, "|                           |")
        self.screen.addstr(26, 1, "|                           |")
        self.screen.addstr(27, 1, "|                           |")
        self.screen.addstr(28, 2, "\                         /")
        self.screen.addstr(29, 3, "\                       /")
        self.screen.addstr(29, 4, "( ) ( ) ( ) ( ) ( ) ( )", self.red)
        for e in range(11):
            x = 5 + (e*2)
            self.screen.addstr(29, x, "^", self.yellow)
        self.screen.addstr(20, 30, "_", self.yellow)
        self.screen.addstr(21, 29, "//", self.yellow)
        self.screen.addstr(22, 28, "//", self.yellow)
        self.screen.addstr(23, 27, "//", self.yellow)
        self.screen.addstr(24, 26, "//", self.yellow)
        self.help_text(110, {})
        self.command_line()

    def cauldron_only_screen(self, Counter):
        #Make Cauldron
        self.screen.addstr(23, 3, "_________________________")
        self.screen.addstr(24, 2, "/_________________________\\")
        self.screen.addstr(25, 1, "|                           |")
        self.screen.addstr(26, 1, "|                           |")
        self.screen.addstr(27, 1, "|                           |")
        self.screen.addstr(28, 2, "\                         /")
        self.screen.addstr(29, 3, "\                       /")
        if Counter >= 6:
            self.screen.addstr(29, 4, "( ) ( ) ( ) ( ) ( ) ( )", self.red)
            for e in range(11):
                x = 5 + (e*2)
                self.screen.addstr(29, x, "^", self.yellow)
        else:
            self.screen.addstr(29, 4, "_______________________")
        self.screen.addstr(20, 30, "_", self.yellow)
        self.screen.addstr(21, 29, "//", self.yellow)
        self.screen.addstr(22, 28, "//", self.yellow)
        self.screen.addstr(23, 27, "//", self.yellow)
        self.screen.addstr(24, 26, "//", self.yellow)
        ingredients = ["Dragon Scale", "Yetti Fur", "Charred Finger"]
        if Counter > 2 and Counter:
            ing = Counter - 2
            if ing > 3:
                ing = 3
            for a in range(ing):
                self.screen.addstr(25 + a, 3, "* ", self.green)
                self.screen.addstr(ingredients[a])
#---------------------------------------------------------------------------------------------------------------------------------------
#                                                            Cut Scenes
#---------------------------------------------------------------------------------------------------------------------------------------
    def get_names(self, Player, Controller): #self, Class, Class
        #Get Player Name
        Controller.get_speaker_name(Player, "Player", self, [7, 8, 9])
        self.Game_State.story = True
        self.print_message(10, True, "Story", {"{Name}": Player.Name["Value"]})
        self.print_message(11, True, "Story", {})
        #Get Grandfather's Name
        Controller.get_speaker_name(Player, "Grandfather", self, [12, 8, 9])
        self.print_message(13, True, "Story", {})
        #Get Friend's Name
        Controller.get_speaker_name(Player, "Friend", self, [14, 8, 9])

    def Intro_Grandfather(self, Player, Controller, Scene, Game_State): #self, Class, Class
        loop = True
        no = 0
        while loop == True:
            self.clear_screen()
            #You hear a knock at the door
            self.screen.addstr(self.line, 1, self.print_message(15, False, "Story", {}))
            self.line += 1
            #Do you answer it?
            self.screen.addstr(self.line, 1, self.print_message(16, False, "Story", {}))
            self.line += 1
            self.help_text(103, {})
            response = Controller.get_response(Player, False, self)
            if response.title() in Controller.yes:
                self.print_message(23, True, "Story", {})
                loop = False
            else:
                if no == 0:
                    self.print_message(17, False, "Story", {})
                    self.print_message(18, True, "Story", {"{Header}": "Grandfather", "{Name}": Player.Name["Value"]})
                    no += 1
                elif no == 1:
                    self.print_message([*range(19, 23)], True, "Story", {})
                    loop = False
                else:
                    self.screen.addstr(self.line, 1, self.print_message(9, False, "Story", {}))
        self.print_message(24, True, "Story", {"{Name}": Player.Name["Value"]})
        self.print_message(25, True, "Story", {})
        self.print_message(26, True, "Story", {})
        self.print_message(27, True, "Story", {"{Name}": Player.Speakers["Grandfather"]})
        Game_State.spellbook = True
        self.print_message(28, True, "Story", {})
        self.print_message(43, True, "Story", {})
        self.print_message(44, True, "Story", {"{Name}": Player.Speakers["Grandfather"]})
        self.print_message(29, True, "Story", {"{Name}": Player.Speakers["Grandfather"]})
        self.print_message(30, True, "Story", {"{Name}": Player.Name["Value"]})
        self.print_message(31, True, "Story", {"{MP}": Player.MP["Name"]})
        self.print_message(32, True, "Story", {"{MP}": Player.MP["Name"]})
        self.print_message(33, True, "Story", {"{MP}": Player.MP["Name"]})
        self.print_message(34, True, "Story", {"{Stat}": [Player.MP["Name"], Player.HP["Name"]]})
        self.print_message([*range(35, 37)], True, "Story", {})
        #self.clear_screen()
        self.print_message(37, True, "Story", {"{MP}": Player.MP["Name"]})
        #Choose Spell to learn!
        chosen = ""
        self.clear_screen()
        self.print_message(45, True, "Story", {})
        loop = True
        repeat = False
        while loop == True:
            if repeat == True:
                self.screen.addstr(self.line, 1, self.make_line(46, "Story", {}))
                self.line += 4
            self.screen.addstr(self.line, 1, self.make_line(38, "Story", {"{Spell}": [Player.Fire["Name"], Player.Ice["Name"]]}))
            self.line += 1
            Player.view_spellbook_cutscene(self)
            self.help_text(104, {})
            response = Controller.get_response(Player, False, self)
            response = response.title()
            if response == Player.Fire["Name"]:
                chosen = Player.Fire["Name"]
                Player.Fire["Value"] = Player.Fire["Init"]
                loop = False
            elif response == Player.Ice["Name"]:
                chosen = Player.Ice["Name"]
                Player.Ice["Value"] = Player.Ice["Init"]
                loop = False
            else:
                repeat = True
            self.clear_screen()
        effects = {Player.Fire["Name"]: "fireball", Player.Ice["Name"]: "clump of rock-hard ice"}
        self.print_message(39, True, "Story", {"{Name}": Player.Speakers["Grandfather"], "{Spell}": chosen})
        self.print_message(1, True, "Story", {"{Spell}": chosen})
        self.print_message(40, True, "Story", {"{Name}": Player.Speakers["Grandfather"], "{Spell Effect}": effects[chosen]})
        spelled = ""
        for char in range(len(chosen)):
            spelled += chosen[char].upper()
            if char < len(chosen) - 1:
                spelled += "-"
        loop = True
        effects = {Player.Fire["Name"]: "small flame", Player.Ice["Name"]: "snowflake"}
        self.clear_screen()
        message = 2
        while loop == True:
            if message == 2:
                self.screen.addstr(self.line, 1, self.make_line(2, "Story", {"{Spelled}": spelled, "{Spell}": chosen}))
            elif message == 3:
                self.screen.addstr(self.line, 1, self.make_line(3, "Story", {}))
            else:
                self.screen.addstr(self.line, 1, self.make_line(46, "Story", {}))
            self.help_text(105, {})
            response = Controller.get_response(Player, False, self)
            if response == chosen.lower():
                message = 3
            elif response == chosen:
                cost = Player.calculate_MP(Player.Spells[chosen])
                Player.MP["Value"] -= cost
                self.print_message(47, True, "Story", {"{Spell Effect}": effects[chosen]})
                self.print_message(4, True, "Story", {})
                loop = False
            elif response == chosen.upper():
                cost = Player.calculate_MP(Player.Spells[chosen])
                Player.MP["Value"] -= cost
                self.print_message(47, True, "Story", {"{Spell Effect}": effects[chosen]})
                self.print_message(5, True, "Story", {})
                loop = False
            else:
                message = 46
        self.print_message(41, True, "Story", {"{Name}": Player.Speakers["Grandfather"]})
        self.print_message(42, True, "Story", {})
        self.print_message(6, True, "Story", {})
        dummy = Actor(1, "Magical Dummy")
        dummy.XP["Value"] = 100
        Game_State.start_battle(Player, dummy, Controller, Scene)
        Player.rest()

    def Intro_Friend(self, Player, Controller): #self, Class, Class
        #"Excellent! Keep this up and you'll be a master wizard in no time!"
        self.print_message(48, True, "Story", {})
        self.print_message(61, True, "Story", {"{MP}": Player.MP["Name"]})
        self.screen.addstr(self.line, 1, self.make_line(62, "Story", {}))
        self.print_message([54, 55, 56], True, "Story", {})
        loop = True
        #knock at the door
        while loop == True:
            self.clear_screen()
            self.screen.addstr(self.line, 1, self.print_message(15, False, "Story", {}))
            self.line += 1
            self.screen.addstr(self.line, 1, self.print_message(16, False, "Story", {}))
            self.line += 1
            response = Controller.get_response(Player, False, self)
            response = response.title()
            if response in Controller.yes:
                self.print_message(63, True, "Story", {"{Name}": Player.Speakers["Friend"]})
                self.print_message(51, True, "Story", {"{Name}": Player.Name["Value"]})
                self.screen.addstr(self.line, 1, self.print_message(52, False, "Story", {}))
                self.print_message(53, True, "Story", {"{Name}": Player.Speakers["Friend"]})
                Player.Inventory["Potion"] += 1
                loop = False
            else:
                self.print_message(17, True, "Story", {})
                self.print_message(49, True, "Story", {"{Name}": [Player.Name["Value"], Player.Speakers["Friend"]]})
                self.print_message(50, True, "Story", {"{Name}": Player.Name["Value"]})
        #Grandfather leaves
        self.print_message(57, True, "Story", {})
        self.print_message(58, True, "Story", {"{Name}": Player.Name["Value"]})
        self.print_message(59, True, "Story", {})
        self.print_message(60, True, "Story", {})

    def Intro_Agatha(self, Player, Controller, Scene, Game_State): #self, Class, Class
        self.print_message(64, True, "Story", {"{Name}": Player.Speakers["Friend"]})
        self.print_message(65, True, "Story", {})
        self.print_message(66, True, "Story", {})
        self.clear_screen()
        #Think we should take a look at the spellbook?
        self.screen.addstr(self.line, 1, self.make_line(67, "Story", {}))
        self.help_text(107, {})
        response = Controller.get_response(Player, False, self)
        response = response.title()
        if Controller.bools["Yes"] == True:
            self.print_message(69, True, "Story", {})
        else:
            self.print_message(68, True, "Story", {})
        self.print_message(70, True, "Story", {"{Name}": Player.Speakers["Friend"]})
        self.print_message(71, True, "Story", {})
        self.print_message(72, True, "Story", {})
        #Friend reads the incantation
        self.print_message([73, 74, 75], True, "Story", [{"{Name}": Player.Speakers["Friend"]}, {}, {}])
        #Agatha appears
        self.print_message([76, 77, 78, 79], True, "Story", [{}, {}, {"{Name}": Player.Speakers["Grandfather"]}, {}])
        self.print_message(80, True, "Story", {})
        Player.Speakers["Agatha"] = "Agatha"
        self.print_message(81, True, "Story", {"{Name}": Player.Speakers["Agatha"].upper()})
        self.print_message([82, 83, 84], True, "Story", [{}, {"{Name}": Player.Speakers["Agatha"]}, {}])
        self.print_message(109, True, "Story", {"{Name}": Player.Name["Value"]})
        agatha = Enemy(10, "Agatha", "", ["Fire", "Ice", "Water", "Wind", "Lightning"], [])
        agatha.make_boss()
        agatha.Name["Value"] = Player.Speakers["Agatha"]
        Game_State.can_lose = True
        Game_State.start_battle(Player, agatha, Controller, Scene)
        Game_State.can_lose = False
        agatha.__delete__()

    def defeated_by_Agatha(self, Player): #self, Class
        self.print_message(110, True, "Story", {})
        self.print_message([85, 86, 87], True, "Story", [{"{Name}": [Player.Speakers["Agatha"], Player.Speakers["Friend"]]}, {"{Name}": Player.Speakers["Friend"]}, {"{Name}": Player.Speakers["Friend"]}])
        #Agatha leaves
        self.print_message([88, 89, 90, 91], True, "Story", [{"{Name}": Player.Speakers["Agatha"]}, {"{Name}": Player.Speakers["Agatha"]}, {}, {"{Name}": Player.Speakers["Agatha"]}])
        self.print_message(92, True, "Story", {"{Name}": [Player.Speakers["Friend"], Player.Speakers["Agatha"]]})
        self.print_message([93, 94], True, "Story", {})
        self.print_message(95, True, "Story", {"{Name}": Player.Speakers["Friend"]})
        self.print_message([96, 97, 98], True, "Story", [{"{Name}": Player.Name["Value"].upper()}, {}, {}])

    def spellbook_tutorial(self, Player, Controller, Game_State): #self, Class, Class, Class
        self.print_message(111, True, "Story", {})
        self.print_message(112, True, "Story", {})
        loop = True
        Game_State.tutorial = True
        while loop == True:
            self.clear_screen()
            self.screen.addstr(self.line, 1, self.print_message(50, False, "Menu", {}))
            self.line += 1
            response = Controller.get_response(Player, False, self)
            response = response.title()
            if response == "Study":
                Player.study_magic(self, Controller, Game_State)
                loop = False
                Game_State.tutorial = False
        self.print_message([51, 52, 53, 54], True, "Menu", [])
        self.print_message([99, 100, 101, 102], True, "Story", [{}, {"{Name}": Player.Speakers["Agatha"]}, {}, {"{Name}": Player.Speakers["Friend"]}])

    def Top_of_Tower_pre_battle(self, Player, Controller, Game_State):
        self.print_message([*range(125, 140)], True, "Story", 
                           [{"{Agatha}": Player.Speakers["Agatha"], "{Name}": Player.Name["Value"]}, {},{}, {},
                            {"{Name}": Player.Speakers["Agatha"]}, {}, {"{Agatha}": Player.Speakers["Agatha"]},
                            {"{Name}": Player.Name["Value"]}, {}, {"{Name}": Player.Name["Value"]},
                            {"{Merlin}": Player.Speakers["Grandfather"]}, {}, {}, {"{Merlin}": Player.Speakers["Grandfather"]},
                            {"{Name}": Player.Name["Value"]}])
        loop = True
        Path = ""
        while loop == True:
            self.help_text(121, {"{Name}": Player.Speakers["Agatha"]})
            response = Controller.get_response(Player, False, self)
            if Controller.bools["No"] == True:
                Path = "Good"
                self.print_message(140, True, "Story", {})
                #Fight Agatha
                agatha = Enemy(10, "Agatha", "", ["Fire", "Ice", "Water", "Wind", "Lightning"], [])
                agatha.make_boss()
                agatha.Name["Value"] = Player.Speakers["Agatha"]
                Game_State.start_battle(Player, agatha, Controller, self)
                if Game_State.game_over == False:
                    loop = False
                    self.Top_of_Tower_post_battle(Player, Controller, Game_State, Path)
                loop = False
            elif Controller.bools["Yes"] == True:
                Path = "Evil"
                self.print_message([*range(141, 150)], True, "Story", [{}, {"{Merlin}": Player.Speakers["Grandfather"]},
                                                                                             {"{Agatha}": Player.Speakers["Agatha"]}, {"{Merlin}": Player.Speakers["Grandfather"]},
                                                                                             {}, {"{Agatha}": Player.Speakers["Agatha"]}, {}, {}, {}])
                #Fight Merlin
                merlin = Enemy(10, "Merlin", "", ["Fire", "Ice", "Water", "Wind", "Lightning"], [])
                merlin.make_boss()
                merlin.Name["Value"] = Player.Speakers["Grandfather"]
                Game_State.start_battle(Player, merlin, Controller, self)
                if Game_State.game_over == False:
                    loop = False
                    self.Top_of_Tower_post_battle(Player, Controller, Game_State, Path)
                loop = False
            else:
                self.clear_screen()
                self.screen.addstr(self.line, 1, self.print_message(139, False, "Story", {"{Name}": Player.Name["Value"]}))

    def Top_of_Tower_post_battle(self, Player, Controller, Game_State, Path):
        if Path == "Good":
            self.print_message([*range(160, 179)], True, "Story", [{}, {"{Name}": Player.Name["Value"]}, {"{Agatha}": Player.Speakers["Agatha"]}, {"{Name}": Player.Name["Value"]},
                                                                   {}, {}, {"{Merlin}": Player.Speakers["Grandfather"], "{Friend}": Player.Speakers["Friend"]}, {}, {"{Merlin}": Player.Speakers["Grandfather"], "{Friend}": Player.Speakers["Friend"]},
                                                                   {"{Friend}": Player.Speakers["Friend"]}, {"{Friend}": Player.Speakers["Friend"]}, {}, {}, {}, {"{Merlin}": Player.Speakers["Grandfather"]}, {}, 
                                                                   {"{Name}": Player.Name["Value"]}, {"{Name}": Player.Name["Value"]}, {"{Friend}": Player.Speakers["Friend"]}])
        else:
            self.print_message([*range(150, 160)], True, "Story", [{"{Name}": Player.Name["Value"]}, {}, {"{Agatha}": Player.Speakers["Agatha"], "{Merlin}": Player.Speakers["Grandfather"]},
                                                                   {}, {"{Merlin}": Player.Speakers["Grandfather"]}, {}, {"{Name}": Player.Name["Value"]}, {"{Name}": Player.Speakers["Friend"]}, {"{Agatha}": Player.Speakers["Agatha"]}, {}])
        self.print_message(179, True, "Story", {})
        Game_State.story = False
        Game_State.game_over = True
        Game_State.return_to_menu(Controller, self, Player)
