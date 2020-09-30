from Command import Command
from Actor import *
from Spell import Spell
from Item import Item
from Scene import Scene
from Room import *
from Files import Files

class Game:
    def __init__(self):
        self.tutorial = False
        self.game_over = False
        self.battle = False
        self.story = False
        self.can_lose = False
        self.next_turn = True
        self.in_dungeon = False
        self.in_tower = False
        self.spellbook = False
        self.brewing = False
        self.turn = 0
        self.win_condition = "Death"
        self.tower = []
        self.current_floor = ""
        self.Debug = False
        self.loop = False
        self.menu = True
        self.Options = False
        self.tower_entrance = False
        self.tower1 = False
        self.tower2 = False
        self.tower3 = False
        self.tower4 = False
        self.tower5 = False
        self.dungeon1 = False
        self.dungeon2 = False
        self.dungeon3 = False
        self.dungeon4 = False
        self.dungeon5 = False

    def win_conditions(self, Player, Enemy): #self, Class, Class
        status = False
        if self.win_condition == "Death":
            if Player.HP["Value"] <= 0 or Enemy.HP["Value"] <= 0:
                status = True
        return status

    def start_battle(self, Player, Enemy, controller, Scene): #self, Class, Class, Class, Class
        self.screen = Scene.screen
        Scene.log = []
        self.battle = True
        self.story = False
        self.turn = 1
        while self.win_conditions(Player, Enemy) == False:
            self.take_turn(Player, Enemy, controller, Scene)
        if self.win_conditions(Player, Enemy) == True:
            self.battle = False
            self.story = True
            controller.stumbles = 0
            Player.Resistances = []
            Player.Weaknesses = []
            Player.Heals = []
            if self.game_over == True:
                #Game Over!
                self.story = False
                Scene.clear_screen()
                Scene.screen.addstr(Scene.line, 1, Scene.print_header(Scene.make_line(1, "Menu", {})))
                Scene.line += 3
                self.return_to_menu(controller, Scene, Player)
            elif self.game_over == False and self.can_lose == False:
                Scene.log = []
                Scene.clear_screen()
                self.Story_UI(Player, Scene, controller)
                Scene.victory_screen(Player, Enemy, self)
                response = controller.get_response(Player, False, Scene)
                end_spells = Spell(Player)
                end_spells.deactivate_duration_spells(Player, Enemy)
                end_spells.__delete__()
                Enemy.__delete__()
                Scene.clear_screen()
                Player.check_XP(Scene)
                spell = Spell(Player)
                spell.learn_exp_spells(Player, Scene)
            elif self.game_over == False and self.can_lose == True:
                Scene.log = []
                response = controller.get_response(Player, False, Scene)
                Scene.clear_screen()
                #{Name} is defeated!
                end_spells = Spell(Player)
                end_spells.deactivate_duration_spells(Player, Enemy)
                end_spells.__delete__()
                Scene.screen.addstr(Scene.line, 1, Scene.print_header("Defeated"))
                Scene.line += 3
                Scene.screen.addstr(Scene.line, 1, Scene.make_line(36, "Menu", {"{Name}": Player.Name["Value"]}))
                Scene.help_text(106, {})
                Scene.screen.refresh()
                response = controller.get_response(Player, False, Scene)
                Player.rest()

    def take_turn(self, Player, Enemy, controller, Scene): #self, Class, Class, Class, Class
        self.screen = Scene.screen
        self.battle_UI(Player, Enemy, Scene, controller)
        Scene.log = []
        controller.get_command(Player, Enemy, self, Scene)
        self.battle_UI(Player, Enemy, Scene, controller)
        if self.next_turn == False:
            while self.next_turn == False:
                self.next_turn = True
                controller.get_command(Player, Enemy, self, Scene)
                self.battle_UI(Player, Enemy, Scene, controller)
        if self.battle == True:
            if Enemy.enemy == True:
                self.battle_UI(Player, Enemy, Scene, controller)
                Enemy.AI_attack(Enemy.choose_attack(), Player, self, Scene)
                self.battle_UI(Player, Enemy, Scene, controller)
            if self.game_over == False:
                duration_spells = Spell(Player)
                duration_spells.activate_duration_spell(Player, Enemy, Scene, self)
                duration_spells.activate_duration_spell(Enemy, Player, Scene, self)
                Player.reduce_duration(Enemy, Scene)
                Enemy.reduce_duration(Player, Scene)
                self.turn += 1

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
                        Scene.log.append(Scene.make_line(103, "Story", {}))
                        Scene.line += 1
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
                        Scene.log.append(Scene.make_line(104, "Story", {}))
                        Scene.line += 1
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
        Scene.clear_screen()
        self.menu = True
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "                                                  Spell Caster", Scene.cyan)
        Scene.screen.addstr(Scene.line, 110, "Ver: ")
        Scene.screen.addstr("2.00", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        #Type your selection
        Scene.screen.addstr(Scene.line, 1, Scene.print_header(Scene.make_line(92, "Menu", {})))
        Scene.line += 3
        selection = ["About", "New Game", "Continue", "Options", "Cheats", "Credits", "Quit"]
        file = Files()
        for x in range(len(selection)):
            if selection[x] != "Continue" and selection[x] != "Options":
                Scene.screen.addstr(Scene.line, 1, "* ", Scene.yellow)
                Scene.screen.addstr(selection[x])
                Scene.line += 1
            else:
                if file.Continue() == True:
                    Scene.screen.addstr(Scene.line, 1, "* ", Scene.yellow)
                    Scene.screen.addstr(selection[x])
                    Scene.line += 1
                else:
                    continue
        self.loop = True
        while self.loop == True:
            Controller.line = Scene.line
            Controller.get_command(Player, file, self, Scene)
        file.__delete__()

    def start_game(self, Player, Controller, Scene):
        if self.Debug == False:
            Scene.get_names(Player, Controller)
            Scene.Intro_Grandfather(Player, Controller, Scene, self)
            Scene.Intro_Friend(Player, Controller)
            Scene.Intro_Agatha(Player, Controller, Scene, self)
            Scene.defeated_by_Agatha(Player)
            Scene.spellbook_tutorial(Player, Controller, self)
        else:
            Scene.clear_screen()
            self.story = True
            self.spellbook = True
            #self.in_tower = True
        #Enter Tower
        self.current_floor = self.tower[5].Name
        self.tower[5].enter_room(Player, Scene, Controller, self)

    def about(self, Player, Controller, Scene):
        Scene.clear_screen()
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "                                               About Spell Caster", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "Welcome to the world of Spell Caster!")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "In this game, you play as a young witch or wizard")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "An evil witch has transformed your best friend into a frog and threatens to take over the world!")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "It is up to you to learn new spells, defeat the evil witch, and help change your friend back!")
        Scene.line += 3
        #Type back to Exit
        Scene.screen.addstr(Scene.line, 1, Scene.make_line(65, "Menu", {}))
        Scene.line += 1
        loop = True
        while loop == True:
            response = Controller.get_response(Player, False, Scene)
            if Controller.bools["Exit"] == True:
                loop = False
                self.main_menu(Player, Controller, Scene)

    def options(self, Player, Controller, Scene, File):
        self.Options = True
        Scene.clear_screen()
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "                                                    Options", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        #Type back to Exit
        Scene.screen.addstr(Scene.line, 1, Scene.make_line(65, "Menu", {}))
        Scene.line += 1
        #Type Your Selection
        Scene.screen.addstr(Scene.line, 1, Scene.print_header(Scene.make_line(92, "Menu", {})))
        Scene.line += 3
        selections = ["Change Names", "Delete Save Data"]
        for x in range(len(selections)):
            Scene.screen.addstr(Scene.line, 1, "* ", Scene.yellow)
            Scene.screen.addstr(selections[x])
            Scene.line += 1
        self.loop = True
        while self.loop == True:
            Controller.line = Scene.line
            Controller.get_command(Player, File, self, Scene)

    def cheats(self, Player, Controller, Scene):
        Scene.clear_screen()
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "                                                     Cheats", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        #Type Back to Exit
        Scene.screen.addstr(Scene.line, 1, Scene.make_line(65, "Menu", {}))
        Scene.line += 1
        #Enter Password
        Scene.screen.addstr(Scene.line, 1, Scene.print_header(Scene.make_line(89, "Menu", {})))
        Scene.line += 3
        loop = True
        while loop == True:
            response = Controller.get_response(Player, False, Scene)
            if response == Controller.Cheat:
                loop = False
                self.Debug = True
                Scene.screen.addstr(Scene.line + 1, 1, " * Debug Mode Enabled!", Scene.green)
                response = Controller.get_response(Player, False, Scene)
                self.main_menu(Player, Controller, Scene)
            elif Controller.bools["Exit"] == True:
                loop = False
                self.main_menu(Player, Controller, Scene)

    def credits(self, Player, Controller, Scene):
        Scene.clear_screen()
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "                                                     Credits", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 53, "Story By")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 50, "Daniel Navarro", Scene.cyan)
        Scene.line += 2
        Scene.screen.addstr(Scene.line, 51, "Programming")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 50, "Daniel Navarro", Scene.cyan)
        Scene.line += 2
        Scene.screen.addstr(Scene.line, 44, "Assistant to the Programmer")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 51, "Iroh the Cat", Scene.cyan)
        Scene.line += 2
        Scene.screen.addstr(Scene.line, 52, "QA Testers")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 50, "Daniel Navarro", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 50, "Madhu Kottalam", Scene.cyan)
        Scene.line += 2
        Scene.screen.addstr(Scene.line, 50, "Special Thanks")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 51, "Jey Kottalam", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 50, "Madhu Kottalam", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 50, "Estella Garcia", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 51, "Iroh the Cat", Scene.cyan)
        Scene.line += 2
        #Type back to Exit
        Scene.screen.addstr(Scene.line, 1, Scene.make_line(65, "Menu", {}))
        Scene.line += 1
        loop = True
        while loop == True:
            response = Controller.get_response(Player, False, Scene)
            if Controller.bools["Exit"] == True:
                loop = False
                self.main_menu(Player, Controller, Scene)

    def quit(self, Player, Controller, Scene):
        Scene.clear_screen()
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "                                                   Quit Game", Scene.cyan)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "-----------------------------------------------------------------------------------------------------------------------")
        Scene.line += 1
        loop = True
        while loop == True:
            Scene.line = 3
            #Are you Sure you want to quit?
            Scene.screen.addstr(Scene.line, 1, Scene.make_line(87, "Menu", {}))
            Scene.line += 1
            response = Controller.get_response(Player, False, Scene)
            if Controller.bools["Yes"] == True:
                loop = False
                if self.menu == False:
                    self.return_to_menu(Controller, Scene, Player)
            elif Controller.bools["No"] == True:
                loop = False
                if self.menu == True:
                    self.initialize()

    def initialize(self):
        self.tutorial = False
        self.game_over = False
        self.battle = False
        self.story = False
        self.can_lose = False
        self.next_turn = True
        self.in_dungeon = False
        self.in_tower = False
        self.turn = 0
        self.win_condition = "Death"
        self.tower = []
        self.current_floor = ""
        self.loop = False
        player = Player(1, "Magicko")
        player.Inventory["Potion"] += 2
        Narrator = Scene(player, self)
        Controller = Command(player, Narrator, self)
        self.Controller = Controller
        Narrator.Game_State = self
        Controller.screen = Narrator.screen
        Controller.line = Narrator.line
        player.screen = Narrator.screen
        player.line = Narrator.line
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
        #self.testing_stuff(player, Controller, Narrator)
#--------------------------------------------------
# Debug
#--------------------------------------------------
    def testing_stuff(self, player, Controller, Narrator):
        #------------------------------------------------------------
        # Debug Testing -- Please Delete
        #------------------------------------------------------------
        self.menu = False
        Controller.fill_inventory(player)
        player.Regen["Active"] = True
        player.Curse["Active"] = True
        player.Protect["Active"] = True
        player.Shell["Active"] = True
        player.Sand["Active"] = True
        player.Fire["Value"] = 2
        player.Cure["Casts"] = 100
        player.Regen["Value"] = 5
        bad_guy = Enemy(1, "Rude", "", [], [])
        bad_guy.Regen["Active"] = True
        bad_guy.Curse["Active"] = True
        bad_guy.Protect["Active"] = True
        bad_guy.Shell["Active"] = True
        bad_guy.Sand["Active"] = True
        self.tower_entrance = True
        #self.tower1 = True
        #self.tower2 = True
        #self.tower3 = True
        #self.tower4 = True
        #self.tower5 = True
        #self.dungeon1 = True
        #self.dungeon2 = True
        #self.dungeon3 = True
        #self.dungeon4 = True
        #self.dungeon5 = True
        #self.current_floor = "Cold Room"
        #self.battle = True
        self.story = True
        self.in_tower = True
        self.spellbook = True
        self.brewing = False
        Narrator.inventory_page = 1
        #self.battle_UI(player, bad_guy, Narrator, Controller)
        self.Story_UI(player, Narrator, Controller)
        Narrator.Top_of_Tower_pre_battle(player, Controller, self)
        #player.Upgrades["Value"] += 3
        #player.study_magic(Narrator, Controller, self)
        #player.brew_potion(Narrator, Controller, self)
        Controller.get_command(player, player, self, Narrator)

    def return_to_menu(self, Controller, Scene, Player):
        loop = True
        while loop == True:
            #Return to Main Menu?
            Scene.screen.addstr(Scene.line, 1, Scene.print_message(88, False, "Menu", {}))
            Scene.line += 1
            response = Controller.get_response(Player, False, Scene)
            if Controller.bools["Yes"] == True:
                loop = False
                self.initialize()
            elif Controller.bools["No"] == True:
                loop = False
                self.Story = False
                Scene.clear_screen()
                Scene.screen.addstr(Scene.line, 1, "Thanks for Playing!")
                response = Controller.get_response(Player, False, Scene)

    def Story_UI(self, Player, Scene, Command):
        Scene.player_HUD(Player, self)
        Scene.inventory_list(Player, self)
        if self.spellbook == True:
            Scene.spellbook_display(Player, self)
        if self.in_tower == True:
            Scene.tower_map(self)
        Scene.command_line()

    def battle_UI(self, Player, Enemy, Scene, Command):
        Scene.clear_screen()
        Scene.enemy_HUD(Enemy)
        Scene.active_spells(Enemy)
        Scene.player_HUD(Player, self)
        Scene.active_spells(Player)
        Scene.inventory_list(Player, self)
        Scene.spellbook_display(Player, self)
        Scene.turn_counter(self)
        Scene.battle_log()
        Scene.command_line()
#---------------------------------------------------------------------------------------------------------------------------------------
#                                                           Game Path
#---------------------------------------------------------------------------------------------------------------------------------------
#file = Files()
#file.fix(Page, Row, Column, Value)
         #Page, Row, Column, Value
Game_State = Game()
Game_State.initialize()
