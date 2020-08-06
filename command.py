from item import *
from room import *
from scene import Scene
import xlrd
from files import Files

class Command:
    def __init__(self, Player): #self, Class
        self.stumbles = 0
        self.attack_spells = [Player.Fire["Name"], Player.Ice["Name"], Player.Lightning["Name"], Player.Water["Name"], Player.Wind["Name"], Player.Drain["Name"]]
        self.duration_spells = [Player.Curse["Name"], Player.Sand["Name"], Player.Regen["Name"], Player.Protect["Name"], Player.Shell["Name"]]
        self.items = Player.Inventory
        self.yes = ["Yes", "Yup", "Yeah", "Ye", "Correct", "Y", "Sure", "Always", "Ok", "Fine"]
        self.no = ["No", "Nope", "Nah", "Negative", "Incorrect", "N", "Never", "Pass"]
        self.attack = ["Attack", "Hit", "Damage", "Kill", "Hurt", "Smack", "Slap", "Strike", "Whack", "Bludgeon", "Fight"]
        self.exit = ["Back", "Exit", "Return", "Cancel", "Leave"]
        self.up = ["Up", "Ascend"]
        self.down = ["Down", "Descend"]
        self.resume = ["Continue", "Resume"]
        self.recipes = ["Recipe", "Recipes", "Instructions"]
        self.inventory = ["Items", "Inventory", "Potions", "Ethers", "Elixirs"]
        self.examine = ["Examine", "Inspect", "Observe", "Look", "Check"]
        self.spellbook = ["Magic", "Spells", "Spell", "Spellbook"]
        self.help = ["Help", "Commands", "Terms", "Glossary", "Words"]
        self.status = ["Status", "Stats", "Self", "Scan"]
        self.save = ["Save"]
        self.Cheat = "Pumpkin Eater"
        self.bools = {"Yes": False, "No": False, "Attack": False, "Exit": False, "Up": False, "Down": False,  
                      "Resume": False, "Inventory": False, "Examine": False, "Spellbook": False, "Help": False, 
                      "Status": False, "Recipes": False}

        file = Files()
        self.path = file.doc_path
        file.__delete__()

    def check_terms(self, response): #self, "response"
        response = response.title()
        yes = False
        no = False
        attack = False
        exit = False
        up = False
        down = False
        resume = False
        inventory = False
        examine = False
        spellbook = False
        help = False
        status = False
        recipes = False
        for a in range(len(self.yes)):
            if self.yes[a] in response:
                yes = True
        for b in range(len(self.no)):
            if self.no[b] in response:
                no = True
        for c in range(len(self.attack)):
            if self.attack[c] in response:
                attack = True
        for d in range(len(self.exit)):
            if self.exit[d] in response:
                exit = True
        for e in range(len(self.up)):
            if self.up[e] in response:
                up = True
        for i in range(len(self.down)):
            if self.down[i] in response:
                down = True
        for f in range(len(self.resume)):
            if self.resume[f] in response:
                resume = True
        for g in range(len(self.inventory)):
            if self.inventory[g] in response:
                inventory = True
        for h in range(len(self.examine)):
            if self.examine[h] in response:
                examine = True
        for j in range(len(self.spellbook)):
            if self.spellbook[j] in response:
                spellbook = True
        for k in range(len(self.help)):
            if self.help[k] in response:
                help = True
        for l in range(len(self.status)):
            if self.status[l] in response:
                status = True
        for m in range(len(self.recipes)):
            if self.recipes[m] in response:
                recipes = True
        self.bools = {"Yes": yes, "No": no, "Attack": attack, "Exit": exit, "Up": up, "Down": down, 
                      "Resume": resume, "Inventory": inventory, "Examine": examine, "Spellbook": spellbook, 
                      "Help": help, "Status": status, "Recipes": recipes}

    def get_speaker_name(self, Player, Key, Scene, Scene_num): #self, Class, "Key", Class, [Scene_num0, Scene_num1, Scene_num2]
        loop = True
        while loop == True:
            print(Scene.print_message(Scene_num[0], False, "Story", {})) #What was their name?
            response = self.get_response(Player, False)
            response = response.title()
            loop2 = True
            while loop2 == True:
                if len(response) > 0:
                    print(Scene.print_message(Scene_num[1], False, "Story", {"{Name}": response})) #"{Name}". Did I hear that correctly?
                    confirmation = self.get_response(Player, False)
                    confirmation = confirmation.title()
                    if confirmation in self.yes:
                        loop = False
                        loop2 = False
                        if Key != "Player":
                            Player.Speakers[Key] = response
                        else:
                            Player.Name["Value"] = response
                    elif confirmation in self.no:
                        loop2 = False
                    else:
                        print(Scene.print_message(Scene_num[2], False, "Story", {})) #Sorry, I don't understand...
                else:
                    print(Scene.print_message(Scene_num[2], False, "Story", {})) #Sorry, I don't understand...
                    loop2 = False

    #USED FOR STORY PURPOSES - DOES NOT TRANSLATE COMMANDS - CAN ONLY COMPARE SELF LISTS - DOES NOT .TITLE()
    def get_response(self, Player, Show_Player_Name): #self, Class, Bool
        if Show_Player_Name == True:
            line_maker = Scene(Player)
            header = line_maker.print_header(Player.Name["Value"])
            user_input = input(header + '\n ')
            line_maker.__delete__()
        else:
            user_input = input(" ")
        response = user_input.strip()
        char = ""
        if len(response) > 0:
            char = response[-1]
        if char.isalpha() == False and len(response) > 0:
            response = self.strip_punc(response)
        self.check_terms(response)
        return response

    def strip_punc(self, text): #self, "text"
        punc = ["!", ".", ",", ";", "?", "'"]
        while text[-1] in punc:
            for char in range(len(punc)):
                if text[-1] == punc[char]:
                    text = text.strip(punc[char])
        return text

    def get_command(self, Player, Obj, Game_State, Scene): #self, Class, Class, Class, Class
        if Game_State.menu == False:
            print(Scene.print_message(5, False, "Menu", {})) #What will you do?
        response = input(" >")
        char = ""
        #strip
        if len(response) > 0:
            char = response[-1]
        if char.isalpha() == False and len(response) > 0:
            response = self.strip_punc(response)
        #set bools
        response = response.title()
        self.check_terms(response)
        #Choose translator
        if isinstance(Obj, Actor):
            self.translate_battle_command(response, Player, Obj, Game_State, Scene)
        elif isinstance(Obj, Room):
            if len(Obj.Interactables) > 0:
                interactable_command = False
                for a in range(len(Obj.Interactables)):
                    if type(Obj.Interactables[a].Name) is list:
                        for b in range(len(Obj.Interactables[a].Name)):
                            if Obj.Interactables[a].Name[b] in response:
                                self.translate_interactable_command(response, Player, Obj.Interactables[a], Game_State, Scene)
                                interactable_command = True
                                break
                    else:
                        if Obj.Interactables[a].Name in response:
                            self.translate_interactable_command(response, Player, Obj.Interactables[a], Game_State, Scene)
                            interactable_command = True
                            break
                if interactable_command == False:
                    self.translate_room_command(response, Player, Obj, Game_State, Scene)
            else:
                self.translate_room_command(response, Player, Obj, Game_State, Scene)
        elif type(Obj) is Interactable:
            self.translate_interactable_command(response, Player, Obj, Game_State, Scene)
        elif type(Obj) is Files:
            self.translate_main_menu_command(response, Player, Obj, Game_State, Scene)
        else:
            print(Scene.print_message(40, False, "Menu", {}))

    def get_help(self, Game_State): #self, Class
        print(" Available Commands:")
        if Game_State.battle == True:
            commands = ["Attack", "Inventory", "Spellbook"]
        else:
            if Game_State.in_dungeon == False:
                commands = ["Examine", "Spellbook", "Inventory", "Stats", "Recipes", "Save", "Quit"]
                if len(Game_State.get_room_commands()) > 0:
                    commands += Game_State.get_room_commands()
                if Game_State.check_solved == True:
                    comands += ["Go Up"]
                commands += ["Go Down"]
            else:
                commands = ["Fight", "Spellbook", "Inventory", "Stats", "Recipes", "Save", "Quit"]
                if Game_State.check_room_steps() == False:
                    commands += ["Continue"]
                else:
                    commands += ["Go Down"]
                commands += ["Go Up"]
                if len(Game_State.get_room_commands()) > 0:
                    commands += Game_State.get_room_commands()
        for command in range(len(commands)):
                print(" * " + commands[command])
#-----------------------------------------------------------------------------------------------------------------------------------------
#                                                                  Debug Commands
#-----------------------------------------------------------------------------------------------------------------------------------------
    def fill_inventory(self, Player): #self, Class
        source = xlrd.open_workbook(self.path)
        Sheet = source.sheet_by_index(6)
        row = 1
        loop = True
        while row < Sheet.nrows:
            if Sheet.cell(row, 0).value:
                Player.Inventory[Sheet.cell(row, 0).value] = 999
            else:
                break
            row += 1

    def levelup(self, Player, Scene): #self, Class, Class
        Player.XP["Value"] = Player.XP["Max"]
        Player.check_XP(Scene)

    def kill(self, Enemy, Game_State): #self, Class
        Enemy.HP["Value"] = 0
        Game_State.battle = False

    def solve(self, Room): #self, Class
        if len(Room.Interactables) > 0:
            for a in range(len(Room.Interactables)):
                Room.Interactables[a].Solved = True
                Room.Solved = True
        if type(Room) is Dungeon:
            Room.Steps_Taken = Room.Steps

    def depletemp(self, Player): #self, Class
        Player.MP["Value"] = 0

    def depletehp(self, Player): #self, Class
        Player.HP["Value"] = 1

    def learn_all_spells(self, Player): #self, Class
        Player.Sacrifice["Value"] = 999
        Player.MHits["Value"] = 999
        Player.Hits["Value"] = 999
        for a in Player.Spells.keys():
            Player.Spells[a]["Casts"] = 999
            if Player.known_spell(Player.Spells[a]["Name"]) == False:
                Player.Spells[a]["Value"] = Player.Spells[a]["Init"]
                if "Duration" in Player.Spells[a]:
                    Player.Spells[a]["Max"] = 3
#-----------------------------------------------------------------------------------------------------------------------------------------
#                                                                  Battle Commands
#-----------------------------------------------------------------------------------------------------------------------------------------
    def translate_battle_command(self, word, Player, Enemy, Game_State, Scene): #self, "word", Class, Class, Class, Class
        word = word.title()
        #---------------------------------------------------------------------
        #                             Physical Attack
        #---------------------------------------------------------------------
        if word in self.attack:
            Player.attack(Enemy, Game_State, Scene)
        #---------------------------------------------------------------------
        #                             Attack Spells
        #---------------------------------------------------------------------
        elif word in self.attack_spells:
            if Player.known_spell(word.title()) == True:
                    for stat in range(len(Player.Stats)):
                        if Player.Stats[stat]["Name"] == word.title():
                            Player.cast_Spell(word, Enemy, Game_State, Scene)
            else:
                #You don't know that spell yet!
                print(Scene.print_message(6, False, "Menu", {}))
        #---------------------------------------------------------------------
        #                             Duration Spells
        #---------------------------------------------------------------------
        elif word in self.duration_spells:
            if Player.known_spell(word.title()) == True:
                    for stat in range(len(Player.Stats)):
                        if Player.Stats[stat]["Name"] == word.title():
                            if Player.Stats[stat]["Active"] == True:
                                #That spell is already active!
                                print(Scene.print_message(7, False, "Menu", {}))
                            else:
                                Player.cast_Spell(Player.Stats[stat]["Name"], Enemy, Game_State, Scene)
        #---------------------------------------------------------------------
        #                             Cure Spell
        #---------------------------------------------------------------------
        elif word == Player.Cure["Name"]: #Cure Spell
            if Player.known_spell(word) == True:
                Player.cast_Spell(Player.Cure["Name"], Enemy, Game_State, Scene)
        #---------------------------------------------------------------------
        #                               Items
        #---------------------------------------------------------------------
        elif word in self.items:
            item = Item(word)
            item.use_consumable_item(Player, Scene, Game_State)
            item.__delete__()
        elif word in self.inventory:
            Game_State.next_turn = False
            Player.get_inventory(Scene)
        #---------------------------------------------------------------------
        #                               Misc.
        #---------------------------------------------------------------------
        elif word in self.spellbook:
            Game_State.next_turn = False
            print(Player.get_spellbook(Game_State, Scene))
        elif word in self.help or self.bools["Help"] == True:
            Game_State.next_turn = False
            self.get_help(Game_State)
        #---------------------------------------------------------------------
        #                               Debug
        #---------------------------------------------------------------------
        elif self.bools["Status"] == True and Game_State.Debug == True:
            print(Enemy.Scan(Scene))
            Game_State.next_turn = False
        elif word == "Pockets" and Game_State.Debug == True:
            self.fill_inventory(Player)
            Game_State.next_turn = False
            print(" * Debug: Inventory Filled")
        elif word == "Avada Kedavra" and Game_State.Debug == True:
            self.kill(Enemy, Game_State)
        elif word == "Deplete MP" and Game_State.Debug == True:
            self.depletemp(Player)
            Game_State.next_turn = False
        elif word == "Deplete HP" and Game_State.Debug == True:
            self.depletehp(Player)
            Game_State.next_turn = False
        elif word == self.Cheat:
            if Game_State.Debug == True:
                Game_State.Debug = False
                print(" * Debug disabled")
            else:
                Game_State.Debug = True
                print(" * Debug enabled")
        #---------------------------------------------------------------------
        #                               Typo
        #---------------------------------------------------------------------
        else:
            #You stumble and miss!
           print(Scene.print_message(8, False, "Menu", {}))
           self.stumbles += 1
           if self.stumbles >= 3:
               self.get_help(Game_State)
               self.stumbles = 0
#----------------------------------------------------------------------------------------------------------------------------------------
#                                                                   Room Commands
#----------------------------------------------------------------------------------------------------------------------------------------
    def translate_room_command(self, response, Player, Room, Game_State, Scene): #self, "response", Class, Class, Class, Class
        response = response.title()
        #---------------------------------------------------------------------
        #                            Room Command
        #---------------------------------------------------------------------
        if response in Room.Commands:
            #Room Commands must only have these vars passed
            Room.Commands[response](Scene, self, Game_State)
        #---------------------------------------------------------------------
        #                            Change Floors
        #---------------------------------------------------------------------
        elif self.bools["Up"] == True and type(Room) is not Dungeon:
            if Room.Solved == True:
                Game_State.change_floors(Player, Scene, self, 1)
            else:
                print(Scene.print_message(107, False, "Story", {}))
        elif self.bools["Up"] == True and type(Room) is Dungeon:
            Game_State.change_floors(Player, Scene, self, 1)
        elif self.bools["Down"] == True and type(Room) is Dungeon:
            if Room.Solved == True:
                Game_State.change_floors(Player, Scene, self, -1)
            else:
                print(Scene.print_message(107, False, "Story", {}))
        elif self.bools["Down"] == True and type(Room) is not Dungeon:
            Game_State.change_floors(Player, Scene, self, -1)
        #---------------------------------------------------------------------
        #                               Study
        #---------------------------------------------------------------------
        elif response == "Study":
            Player.study_magic(Scene, self, Game_State)
        #---------------------------------------------------------------------
        #                             Spellbook
        #---------------------------------------------------------------------
        elif self.bools["Spellbook"] == True:
            print(Player.get_spellbook(Game_State, Scene))
        #---------------------------------------------------------------------
        #                               Items
        #---------------------------------------------------------------------
        elif response in self.items:
            item = Item(response)
            item.use_consumable_item(Player, Scene, Game_State)
            item.__delete__()
        elif response in self.inventory:
            Player.get_inventory(Scene)
        elif self.bools["Recipes"] == True:
            Player.view_recipes(self, Scene)
        #---------------------------------------------------------------------
        #                               Cure
        #---------------------------------------------------------------------
        elif response == Player.Cure["Name"]: #Cure Spell
            if Player.known_spell(response) == True:
                placeholder = Actor(1, "")
                Player.cast_Spell(Player.Cure["Name"], placeholder, Game_State, Scene)
                placeholder.__delete__()
            else:
                #You don't know that spell yet!
                print(Scene.print_message(6, False, "Menu", {}))
        #---------------------------------------------------------------------
        #                               Status
        #---------------------------------------------------------------------
        elif self.bools["Status"] == True:
            print(Player.Scan(Scene))
        #---------------------------------------------------------------------
        #                         Continue Fighting
        #---------------------------------------------------------------------
        elif self.bools["Attack"] == True and type(Room) is Dungeon:
            if Room.Steps_Taken >= Room.Steps: 
                #Continue Fighting
                Room.start_battle(Player, Scene, self, Game_State)
            else:
                Room.Loop = False
        #---------------------------------------------------------------------
        #                   Continue Walking Through Dungeon
        #---------------------------------------------------------------------
        elif self.bools["Attack"] == True or self.bools["Resume"] == True and type(Room) is Dungeon:
            #Take next step in dungeon
            if Room.Steps_Taken < Room.Steps:
                Room.Loop = False
        #---------------------------------------------------------------------
        #                               Save
        #---------------------------------------------------------------------
        elif response in self.save:
            print(Scene.print_message(86, False, "Menu", {}))
            save = Files()
            save.save(Player, Game_State, Scene)
            save.__delete__()
        #---------------------------------------------------------------------
        #                               Debug
        #---------------------------------------------------------------------
        elif response == "Pockets" and Game_State.Debug == True:
            self.fill_inventory(Player)
            print(" * Debug: Inventory Filled")
        elif response == "Solve" and Game_State.Debug == True:
            self.solve(Room)
            print(" * Debug: Room Solved")
        elif response == "Deplete MP" and Game_State.Debug == True:
            self.depletemp(Player)
            print(" * Debug: MP Depleted")
        elif response == "Deplete HP" and Game_State.Debug == True:
            self.depletehp(Player)
            print(" * Debug: HP Depleted")
        elif response == "Level" and Game_State.Debug == True:
            self.levelup(Player, Scene)
        elif response == "Ten" and Game_State.Debug == True:
            counter = 0
            while counter < 10:
                self.levelup(Player, Scene)
                counter += 1
        elif response == "Textbook" and Game_State.Debug == True:
            Player.Upgrades["Value"] += 10
            print(" * Debug: Upgrades available")
        elif response == "Know It All" and Game_State.Debug == True:
            self.learn_all_spells(Player)
            print(" * Debug: Spells Learned")
        elif response == "Interactables" and Game_State.Debug == True:
            for a in range(len(Room.Interactables)):
                print(str(Room.Interactables[a].Name))
                for b in range(len(Room.Interactables[a].Keys)):
                    print(Room.Interactables[a].Keys)
        elif response == self.Cheat:
            if Game_State.Debug == True:
                Game_State.Debug = False
                print(" * Debug disabled")
            else:
                Game_State.Debug = True
                print(" * Debug enabled")
        #---------------------------------------------------------------------
        #                                Misc
        #---------------------------------------------------------------------
        elif self.bools["Help"] == True:
            self.get_help(Game_State)
        elif response == "Quit":
            Game_State.quit(Player, self, Scene)
#---------------------------------------------------------------------------------------------------------------------------------------
#                                                                Interactable Commands
#---------------------------------------------------------------------------------------------------------------------------------------
    def translate_interactable_command(self, Response, Player, Interactable, Game_State, Scene): 
        #self, "Response", Class, Class, Class, Class
        keywords = []
        for a in range(len(Interactable.Commands)):
            if Interactable.Commands[a] in Response:
                keywords.append(Interactable.Commands[a])
        if len(keywords) == 1:
            for b in range(len(Interactable.Keys)):
                if keywords[0] in Interactable.Keys[b]["Terms"]:
                    Interactable.update_keys(Player, Scene, Interactable.Keys[b]["Name"], Game_State)
        elif len(keywords) > 1:
            print(Scene.print_message(46, False, "Menu", {}))
        else:
            if self.bools["Examine"] == True:
                print(Scene.get_interactable_string(Interactable, "Examine", Player))
#---------------------------------------------------------------------------------------------------------------------------------------
#                                                                Main Menu Commands
#---------------------------------------------------------------------------------------------------------------------------------------
    def translate_main_menu_command(self, Response, Player, File, Game_State, Scene):
        Response = Response.title()
        #---------------------------------------------------------------------
        #                             About
        #---------------------------------------------------------------------
        if Response == "About":
            Game_State.loop = False
        #---------------------------------------------------------------------
        #                            New Game
        #---------------------------------------------------------------------
        elif Response == "New Game":
            Game_State.loop = False
            Game_State.menu = False
            Game_State.start_game(Player, self, Scene)
        #---------------------------------------------------------------------
        #                             Continue
        #---------------------------------------------------------------------
        elif Response == "Continue" and File.Continue() == True:
            Game_State.loop = False
            Game_State.menu = False
            print(Scene.print_message(90, False, "Menu", {}))
            File.load(Player, Game_State, self, Scene)
        #---------------------------------------------------------------------
        #                             Options
        #---------------------------------------------------------------------
        elif Response == "Options":
            Game_State.loop = False
        #---------------------------------------------------------------------
        #                             Cheats
        #---------------------------------------------------------------------
        elif Response == "Cheats":
            Game_State.loop = False
            Game_State.cheats(Player, self, Scene)
        #---------------------------------------------------------------------
        #                             Credits
        #---------------------------------------------------------------------
        elif Response == "Credits":
            Game_State.loop = False
        #---------------------------------------------------------------------
        #                              Quit
        #---------------------------------------------------------------------
        elif Response == "Quit":
            Game_State.loop = False
            Game_State.quit(Player, self, Scene)