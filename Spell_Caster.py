from command import Command
from actor import *
from spell import Spell
from item import Item
from scene import Scene
from room import *
from files import Files

class Game:
    def __init__(self):
        self.tutorial = False
        self.game_over = False
        self.battle = False
        self.can_lose = False
        self.next_turn = True
        self.in_dungeon = False
        self.turn = 0
        self.win_condition = "Death"
        self.tower = []
        self.current_floor = ""
        self.Debug = False
        self.loop = False
        self.menu = True
        self.Options = False

    def win_conditions(self, Player, Enemy): #self, Class, Class
        status = False
        if self.win_condition == "Death":
            if Player.HP["Value"] <= 0 or Enemy.HP["Value"] <= 0:
                status = True
        return status

    def start_battle(self, Player, Enemy, controller, Scene): #self, Class, Class, Class, Class
        self.battle = True
        self.turn = 1
        while self.win_conditions(Player, Enemy) == False:
            self.take_turn(Player, Enemy, controller, Scene)
        if self.win_conditions(Player, Enemy) == True:
            self.battle = False
            controller.stumbles = 0
            Player.Resistances = []
            Player.Weaknesses = []
            Player.Heals = []
            if self.game_over == True:
                #Game Over!
                Scene.print_message(1, True, "Menu", {})
                self.return_to_menu(controller, Scene)
            elif self.game_over == False and self.can_lose == False:
                #{Name} is defeated!
                print(Scene.print_message(36, False, "Menu", {"{Name}": Enemy.Name["Value"]}))
                end_spells = Spell(Player)
                end_spells.deactivate_duration_spells(Player, Enemy)
                end_spells.__delete__()
                Enemy.drop_loot(Player, Scene)
                Enemy.__delete__()
                Player.check_XP(Scene)
                spell = Spell(Player)
                spell.learn_exp_spells(Player, Scene)
            elif self.game_over == False and self.can_lose == True:
                #{Name} is defeated!
                end_spells = Spell(Player)
                end_spells.deactivate_duration_spells(Player, Enemy)
                end_spells.__delete__()
                print(Scene.print_message(36, False, "Menu", {"{Name}": Player.Name["Value"]}))
                Player.rest()

    def take_turn(self, Player, Enemy, controller, Scene): #self, Class, Class, Class, Class
        print("---------------------------------------------------------------------------------------------------------------------")
        turn_line = "                                                    Turn: " + str(self.turn)
        print(turn_line)
        print("---------------------------------------------------------------------------------------------------------------------")
        print(self.print_HUD(Enemy, Scene))
        print("")
        print("")
        print("")
        print(self.print_HUD(Player, Scene))
        controller.get_command(Player, Enemy, self, Scene)
        if self.next_turn == False:
            while self.next_turn == False:
                self.next_turn = True
                controller.get_command(Player, Enemy, self, Scene)
        if self.battle == True:
            if Enemy.enemy == True:
                Enemy.AI_attack(Enemy.choose_attack(), Player, self, Scene)
            if self.game_over == False:
                duration_spells = Spell(Player)
                duration_spells.activate_duration_spell(Player, Enemy, Scene, self)
                duration_spells.activate_duration_spell(Enemy, Player, Scene, self)
                Player.reduce_duration(Enemy, Scene)
                Enemy.reduce_duration(Player, Scene)
                self.turn += 1
        view_results = input(" ")

    def print_HUD(self, Actor, Scene): #self, Class, Class
        lines = []
        name_line = Scene.print_header(" Lv." + str(Actor.Level["Value"]) + " " + Actor.Name["Value"])
        lines.append(name_line)
        HP_line = " " + Actor.HP["Name"] + ": " + str(Actor.HP["Value"]) + "/" + str(Actor.HP["Max"])
        MP_line = " " + Actor.MP["Name"] + ": " + str(Actor.MP["Value"]) + "/" + str(Actor.MP["Max"])
        lines.append(HP_line)
        lines.append(MP_line)
        HUD = '\n'.join(lines)
        return HUD

    def get_loot_drops(self, list): #self, "list"
        list = list.title()
        Base = 80
        #Potion Inventories
        potion = [{"Name": "Potion", "Value": 1, "Chance": Base}]
        potion_recipe = [{"Name": "Potion Recipe", "Value": 1, "Chance": Base}]
        hi_potion = [{"Name": "Hi-Potion", "Value": 1, "Chance": Base - 20}]
        hi_potion_recipe = [{"Name": "Hi-Potion Recipe", "Value": 1, "Chance": Base - 20}]
        mega_potion = [{"Name": "Mega-Potion", "Value": 1, "Chance": Base - 40}]
        potions = {"Potion": potion, "Hi-Potion": hi_potion, "Mega-Potion": mega_potion, "Potion Recipe": potion_recipe, "Hi-Potion Recipe": hi_potion_recipe}

        #Ether Inventories
        ether = [{"Name": "Ether", "Value": 1, "Chance": Base}]
        ether_recipe = [{"Name": "Ether Recipe", "Value": 1, "Chance": Base}]
        hi_ether = [{"Name": "Hi-Ether", "Value": 1, "Chance": Base - 20}]
        hi_ether_recipe = [{"Name": "Hi-Ether Recipe", "Value": 1, "Chance": Base - 20}]
        mega_ether = [{"Name": "Mega-Ether", "Value": 1, "Chance": Base - 40}]
        ethers = {"Ether": ether, "Hi-Ether": hi_ether, "Mega-Ether": mega_ether, "Ether Recipe": ether_recipe, "Hi-Ether Recipe": hi_ether_recipe}

        #Elixir Inventories
        elixir = [{"Name": "Elixir", "Value": 1, "Chance": int(Base/2)}]
        hi_elixir = [{"Name": "Hi-Elixir", "Value": 1, "Chance": int(Base/4)}]
        mega_elixir = [{"Name": "Mega-Elixir", "Value": 1, "Chance": int(Base/8)}]
        elixirs = {"Elixir": elixir, "Hi-Elixir": hi_elixir, "Mega-Elixir": mega_elixir}
        if "Potion" in list:
            return potions[list]
        elif "Ether" in list:
            return ethers[list]
        elif "Elixir" in list:
            return elixirs[list]
        else:
            return []

    def change_floors(self, Player, Scene, Controller, direction): #self, class, class, class, int(-1 or 1)
        for floor in range(len(self.tower)):
            if self.tower[floor].Name == self.current_floor:
                self.tower[floor].loop = False
                if direction == -1:
                    if floor > 0:
                        self.current_floor = self.tower[floor -1].Name
                        if type(self.tower[floor -1]) is Dungeon:
                            self.tower[floor -1].enter_dungeon(Player, Scene, Controller, self)
                            break
                        else:
                            self.tower[floor -1].enter_room(Player, Scene, Controller, self)
                            break
                    else:
                        #This is the bottom floor
                        print(Scene.print_message(103, False, "Story", {}))
                        break
                else:
                    if floor < len(self.tower):
                        self.current_floor = self.tower[floor+1].Name
                        if type(self.tower[floor+1]) is Dungeon:
                            self.tower[floor+1].enter_dungeon(Player, Scene, Controller, self)
                            break
                        else:
                            self.tower[floor+1].enter_room(Player, Scene, Controller, self)
                            break
                    else:
                        #This is the top floor
                        print(Scene.print_message(104, False, "Story", {}))
                        break

    def get_room_commands(self):
        commands = []
        for a in range(len(self.tower)):
            if self.tower[a].Name == self.current_floor:
                commands = self.tower[a].Commands
        return commands

    def check_room_steps(self):
        for a in range(len(self.tower)):
            if self.tower[a].Name == self.current_floor:
                if self.tower[a].Steps_Taken < self.tower[a].Steps:
                    return False
                else:
                    return True
                break
    
    def is_dungeon(self, Room):
        if type(Room) == Dungeon:
            return True
        else:
            return False

    def check_solved(self):
        for a in range(len(self.tower)):
            if self.tower[a].Name == self.current_floor:
                if self.tower[a].Solved == True:
                    return True
                else:
                    return False
                break

    def main_menu(self, Player, Controller, Scene):
        self.menu = True
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("                                                  Spell Caster                                                Ver.1.10 ")
        print("-----------------------------------------------------------------------------------------------------------------------")
        #Type your selection
        print(Scene.print_header(Scene.print_message(92, False, "Menu", {})))
        print(" * About")
        print(" * New Game")
        file = Files()
        if file.Continue() == True:
            print(" * Continue")
            print(" * Options")
        print(" * Cheats")
        print(" * Credits")
        print(" * Quit")
        self.loop = True
        while self.loop == True:
            Controller.get_command(Player, file, self, Scene)
        file.__delete__()

    def start_game(self, Player, Controller, Scene):
        #Intro
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("                                                    New Game")
        print("-----------------------------------------------------------------------------------------------------------------------")
        if Game_State.Debug == False:
            Scene.get_names(Player, Controller)
            Scene.Intro_Grandfather(Player, Controller, Scene, self)
            Scene.Intro_Friend(Player, Controller)
            Scene.Intro_Agatha(Player, Controller, Scene, self)
            Scene.defeated_by_Agatha(Player)
            Scene.spellbook_tutorial(Player, Controller, self)
        #Enter Tower
        self.current_floor = self.tower[5].Name
        self.tower[5].enter_room(Player, Scene, Controller, self)

    def about(self, Player, Controller, Scene):
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("                                               About Spell Caster")
        print("-----------------------------------------------------------------------------------------------------------------------")
        print(" Welcome to the world of Spell Caster!")
        print(" In this game, you play as a young witch or wizard")
        print(" An evil witch has transformed your best friend into a frog and threatens to take over the world!")
        print(" It is up to you to learn new spells, defeat the evil witch, and help change your friend back!")
        print("")
        print("")
        #Type back to Exit
        print(Scene.print_message(65, False, "Menu", {}))
        loop = True
        while loop == True:
            response = Controller.get_response(Player, False)
            if Controller.bools["Exit"] == True:
                loop = False
                self.main_menu(Player, Controller, Scene)

    def options(self, Player, Controller, Scene, File):
        self.Options = True
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("                                                    Options")
        print("-----------------------------------------------------------------------------------------------------------------------")
        #Type back to Exit
        print(Scene.print_message(65, False, "Menu", {}))
        #Type Your Selection
        print(Scene.print_header(Scene.print_message(92, False, "Menu", {})))
        print(" * Change Names")
        print(" * Delete Save Data")
        self.loop = True
        while self.loop == True:
            Controller.get_command(Player, File, self, Scene)

    def cheats(self, Player, Controller, Scene):
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("                                                     Cheats")
        print("-----------------------------------------------------------------------------------------------------------------------")
        #Type Back to Exit
        print(Scene.print_message(65, False, "Menu", {}))
        #Enter Password
        print(Scene.print_header(Scene.make_line(89, "Menu", {})))
        loop = True
        while loop == True:
            response = Controller.get_response(Player, False)
            if response == Controller.Cheat:
                loop = False
                self.Debug = True
                print(" * Debug Mode Enabled!")
                self.main_menu(Player, Controller, Scene)
            elif Controller.bools["Exit"] == True:
                loop = False
                self.main_menu(Player, Controller, Scene)

    def credits(self, Player, Controller, Scene):
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("                                                     Credits")
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("                                                     Story By")
        print("                                                  Daniel Navarro")
        print("")
        print("                                                    Programming")
        print("                                                  Daniel Navarro")
        print("")
        print("                                            Assistant to the Programmer")
        print("                                                   Iroh the Cat")
        print("")
        print("                                                    QA Testers")
        print("                                                  Daniel Navarro")
        print("                                                  Madhu Kottalam")
        print("")
        print("                                                  Special Thanks")
        print("                                                   Jey Kottalam")
        print("                                                  Madhu Kottalam")
        print("                                                  Estella Garcia")
        print("                                                   Iroh the Cat")
        print("")
        print("")
        #Type back to Exit
        print(Scene.print_message(65, False, "Menu", {}))
        loop = True
        while loop == True:
            response = Controller.get_response(Player, False)
            if Controller.bools["Exit"] == True:
                loop = False
                self.main_menu(Player, Controller, Scene)

    def quit(self, Player, Controller, Scene):
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("                                                   Quit Game")
        print("-----------------------------------------------------------------------------------------------------------------------")
        loop = True
        while loop == True:
            #Are you Sure you want to quit?
            print(Scene.print_message(87, False, "Menu", {}))
            response = Controller.get_response(Player, False)
            if Controller.bools["Yes"] == True:
                loop = False
                if self.menu == False:
                    self.return_to_menu(Controller, Scene)
            elif Controller.bools["No"] == True:
                loop = False
                if self.menu == True:
                    self.initialize()

    def initialize(self):
        self.tutorial = False
        self.game_over = False
        self.battle = False
        self.can_lose = False
        self.next_turn = True
        self.in_dungeon = False
        self.turn = 0
        self.win_condition = "Death"
        self.tower = []
        self.current_floor = ""
        self.loop = False
        player = Player(1, "Magicko")
        Controller = Command(player)
        Narrator = Scene(player)
        #----------------------------------------------------------------------------------------------------------------------------------------
        #                                                          Init Rooms
        #----------------------------------------------------------------------------------------------------------------------------------------
        #Ground Floor
        ground_floor_candle = Interactable(["Candle", "Fire"])
        ground_floor_candle.Commands = ["Fire", "Burn", "Light"]
        ground_floor_candle.Keys = [{"Name": "Fire", "Value": False, "Type": "Spell", "Terms": ground_floor_candle.Commands}]
        ground_floor = Room("Tower Entrance", 5, [ground_floor_candle])
        ground_floor.Solved = True
        ground_floor.Floor = 0

        #Tower 1
        Ice = Interactable(["Ice", "Door", "Fire"])
        Ice.Commands = ["Fire", "Melt", "Burn"]
        Ice.Keys = [{"Name": "Fire", "Value": False, "Type": "Spell", "Terms": Ice.Commands}]
        tower1 = Room("Cold Room", 8, [Ice])
        tower1.Floor = 1

        #Tower 2
        Cauldron = Interactable(["Cauldron", "Water"])
        Cauldron.Commands = ["Pour", "Water", "Fill"]
        Cauldron.Keys = [{"Name": "Water", "Value": False, "Type": "Spell", "Terms": Cauldron.Commands}]
        tower2 = Room("Cauldron Room", 15, [Cauldron])
        tower2.Floor = 2

        #Tower 3
        poison = Interactable(["Poison", "Gas", "Wind", "Air"])
        poison.Commands = ["Wind", "Blow", "Clear"]
        poison.Keys = [{"Name": "Wind", "Value": False, "Type": "Spell", "Terms": poison.Commands}]
        torch = Interactable(["Torch", "Fire"])
        torch.Commands = ["Fire", "Light", "Burn", "Melt"]
        torch.Keys = [{"Name": "Fire", "Value": False, "Type": "Spell", "Terms": torch.Commands}]
        tower3 = Room("Death Room", 26, [poison, torch])
        tower3.Floor = 3

        #Tower 4
        circuit_board = Interactable(["Circuit Board", "Lightning", "Board", "Circuits"])
        circuit_board.Commands = ["Lightning", "Shock", "Electricute", "Jump Start", "Kick Start", "Bolt", "Jolt"]
        circuit_board.Keys = [{"Name": "Lightning", "Value": False, "Type": "Spell", "Terms": circuit_board.Commands}]
        tower4 = Room("Generator Room", 31, [circuit_board])
        tower4.Floor = 4

        #Tower 5
        tower5 = Room("Top of the Tower", 40, [])
        tower5.Floor = 5

        #Dungeon 1
        dungeon1 = Dungeon("Fire Dungeon", 7,  [], 1, ["Fire", "Normal"], 5)

        #Dungeon 2
        dungeon2 = Dungeon("Ice Dungeon", 41, [], 2, ["Ice", "Normal"], 6)

        #Dungeon 3
        dungeon3 = Dungeon("Water Dungeon", 42, [], 3, ["Water", "Normal"], 7)

        #Dungeon 4
        dungeon4 = Dungeon("Wind Dungeon", 43, [], 4, ["Wind", "Normal"], 8)

        #Dungeon 5
        dungeon5 = Dungeon("Lightning Dungeon", 44, [], 5, ["Lightning", "Normal"], 9)
        dungeon5.bottom_floor = True

        self.tower = [dungeon5, dungeon4, dungeon3, dungeon2, dungeon1, 
                    ground_floor, 
                    tower1, tower2, tower3, tower4, tower5]
        self.main_menu(player, Controller, Narrator)

    def return_to_menu(self, Controller, Scene):
        loop = True
        while loop == True:
            #Return to Main Menu?
            print(Scene.print_message(88, False, "Menu", {}))
            response = Controller.get_response(Player, False)
            if Controller.bools["Yes"] == True:
                loop = False
                self.initialize()
            elif Controller.bools["No"] == True:
                loop = False
#---------------------------------------------------------------------------------------------------------------------------------------
#                                                           Game Path
#---------------------------------------------------------------------------------------------------------------------------------------
#file = Files()
#file.fix(Page, Row, Column, Value)
         #Page, Row, Column, Value
Game_State = Game()
Game_State.initialize()