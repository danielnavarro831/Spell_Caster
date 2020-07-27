from command import Command
from actor import *
from spell import Spell
from item import Item
from scene import Scene
from room import *

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
        hi_potion = [{"Name": "Hi-Potion", "Value": 1, "Chance": Base - 20}]
        mega_potion = [{"Name": "Mega-Potion", "Value": 1, "Chance": Base - 40}]
        potions = {"Potion": potion, "Hi-Potion": hi_potion, "Mega-Potion": mega_potion}

        #Ether Inventories
        ether = [{"Name": "Ether", "Value": 1, "Chance": Base}]
        hi_ether = [{"Name": "Hi-Ether", "Value": 1, "Chance": Base - 20}]
        mega_ether = [{"Name": "Mega-Ether", "Value": 1, "Chance": Base - 40}]
        ethers = {"Ether": ether, "Hi-Ether": hi_ether, "Mega-Ether": mega_ether}

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
#----------------------------------------------------------------------------------------------------------------------------------------
#                                                          Init Classes
#----------------------------------------------------------------------------------------------------------------------------------------
Game_State = Game()
player = Player(1, "Daniel")
Controller = Command(player)
Narrator = Scene(player)

#----------------------------------------------------------------------------------------------------------------------------------------
#                                                          Init Rooms
#----------------------------------------------------------------------------------------------------------------------------------------
#Ground Floor
ground_floor_candle = Interactable(["Candle", "Fire"])
ground_floor_candle.Commands = ["Fire", "Burn", "Light"]
ground_floor_candle.Keys = [{"Name": "Fire", "Value": False, "Type": "Spell", "Terms": ["Fire", "Burn", "Light"]}]
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
Cauldron.Keys = [{"Name": "Water", "Value": False, "Type": "Spell", "Terms":Cauldron.Commands}]
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
tower4 = Room("Wind Puzzle Room", 0, [])
tower4.Floor = 4

#Tower 5
tower5 = Room("Lightning Puzzle Room", 0, [])
tower5.Floor = 5

#Dungeon 1
dungeon1 = Dungeon("Fire Dungeon", 7,  [], 1, ["Fire"], 5)

#Dungeon 2
dungeon2 = Dungeon("Ice Dungeon", 0, [], 2, ["Ice"], 6)

#Dungeon 3
dungeon3 = Dungeon("Water Dungeon", 0, [], 3, ["Water"], 7)

#Dungeon 4
dungeon4 = Dungeon("Wind Dungeon", 0, [], 4, ["Wind"], 8)

#Dungeon 5
dungeon5 = Dungeon("Lightning Dungeon", 0, [], 5, ["Lightning"], 9)

Game_State.tower = [dungeon5, dungeon4, dungeon3, dungeon2, dungeon1, 
             ground_floor, 
             tower1, tower2, tower3, tower4, tower5]

#---------------------------------------------------------------------------------------------------------------------------------------
#                                                           Game Path
#---------------------------------------------------------------------------------------------------------------------------------------

#Intro
if Game_State.Debug == False:
    Narrator.get_names(player, Controller)
    Narrator.Intro_Grandfather(player, Controller)
    dummy = Actor(1, "Magical Dummy")
    dummy.XP["Value"] = 100
    Game_State.start_battle(player, dummy, Controller, Narrator)
    player.rest()
    Narrator.Intro_Friend(player, Controller)
    Narrator.Intro_Agatha(player, Controller)
    #Fight Agatha
    agatha = Enemy(10, "Agatha", "", ["Fire", "Ice", "Water", "Wind", "Lightning"], [])
    agatha.make_boss()
    Game_State.can_lose = True
    Game_State.start_battle(player, agatha, Controller, Narrator)
    Game_State.can_lose = False
    agatha.__delete__()
    Narrator.defeated_by_Agatha(player)
    Narrator.spellbook_tutorial(player, Controller, Game_State)
#Enter Tower
Game_State.current_floor = ground_floor.Name
ground_floor.enter_room(player, Narrator, Controller, Game_State)