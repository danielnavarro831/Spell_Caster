from Item import *
from Room import *
from Scene import Scene
import xlrd
from Files import Files

class Command:
    def __init__(self, Player, Scene, Game_State): #self, Class
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
        self.Scene = Scene
        self.Game_State = Game_State

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
        self.screen = Scene.screen
        self.Scene = Scene
        loop = True
        repeat1 = False
        while loop == True:
            Scene.clear_screen()
            if repeat1 == True:
                self.screen.addstr(Scene.line, 1, Scene.make_line(Scene_num[2], "Story", {})) #Sorry, I don't understand...
                Scene.line += 1
            X = Scene.find_keyword("name", Scene.make_line(Scene_num[0], "Story", {}))
            self.screen.addstr(Scene.line, 1, Scene.print_message(Scene_num[0], False, "Story", {})) #What was their name?
            Scene.pin_line(Scene.line, X, "name", "Cyan")
            Scene.line += 1
            response = self.get_response(Player, False, Scene)
            response = response.title()
            loop2 = True
            repeat2 = False
            while loop2 == True:
                if len(response) > 0:
                    Scene.clear_screen()
                    Scene.help_text(103, {})
                    if repeat2 == True:
                        self.screen.addstr(Scene.line, 1, Scene.make_line(Scene_num[2], "Story", {})) #Sorry, I don't understand...
                        Scene.line += 1
                    self.screen.addstr(Scene.line, 1, Scene.make_line(Scene_num[1], "Story", {"{Name}": response})) #"{Name}". Did I hear that correctly?
                    self.screen.refresh()
                    Scene.line += 1
                    confirmation = self.get_response(Player, False, Scene)
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
                        repeat2 = True
                else:
                    repeat1 = True
                    loop2 = False

    #USED FOR STORY PURPOSES - DOES NOT TRANSLATE COMMANDS - CAN ONLY COMPARE SELF LISTS - DOES NOT .TITLE()
    def get_response(self, Player, Show_Player_Name, Scene): #self, Class, Bool
        if Show_Player_Name == True:
            header = self.Scene.print_header(Player.Name["Value"])
            self.screen.addstr(Scene.line, 1, header)
            Scene.line += 3
        if self.Game_State.story == True or self.Game_State.brewing == True:
            self.screen = Scene.screen
            self.screen.move(43, 16)
            self.screen.clrtoeol() 
            user_input = self.screen.getstr(43, 16).decode('utf-8')
        else:
            self.screen = Scene.screen
            self.screen.move(Scene.line, 1)
            self.screen.clrtoeol() 
            user_input = self.screen.getstr(Scene.line, 1).decode('utf-8')
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
        self.screen = Scene.screen
        self.screen.move(43, 16)
        self.screen.clrtoeol() 
        self.screen.refresh()
        if Game_State.menu == False:
            response = self.screen.getstr(43, 16).decode('utf-8')
        else:
            response = self.screen.getstr(self.line, 1).decode('utf-8')
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
            self.screen.addstr(Scene.print_message(40, False, "Menu", {}))

    def get_help(self, Game_State): #self, Class
        self.screen.addstr(" Available Commands:")
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
                self.screen.addstr(" * " + commands[command])

    def update_line(self):
        self.line = self.Scene.line
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
                if Sheet.cell(row, 2).value == True:
                    Player.Recipes.append(Sheet.cell(row, 0).value)
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
        self.screen = Scene.screen
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
                Scene.log.append(Scene.make_line(6, "Menu", {}))
        #---------------------------------------------------------------------
        #                             Duration Spells
        #---------------------------------------------------------------------
        elif word in self.duration_spells:
            if Player.known_spell(word.title()) == True:
                    for stat in range(len(Player.Stats)):
                        if Player.Stats[stat]["Name"] == word.title():
                            if Player.Stats[stat]["Active"] == True:
                                #That spell is already active!
                                Scene.log.append(Scene.print_message(7, "Menu", {}))
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
        elif word in self.help or self.bools["Help"] == True:
            Game_State.next_turn = False
            self.get_help(Game_State)
        #---------------------------------------------------------------------
        #                               Debug
        #---------------------------------------------------------------------
        elif self.bools["Status"] == True and Game_State.Debug == True:
            self.screen.addstr(Enemy.Scan(Scene))
            Game_State.next_turn = False
        elif word == "Pockets" and Game_State.Debug == True:
            self.fill_inventory(Player)
            Game_State.next_turn = False
            self.screen.addstr(" * Debug: Inventory Filled")
        elif word == "Avada Kedavra" and Game_State.Debug == True:
            self.kill(Enemy, Game_State)
        elif word == "No MP" and Game_State.Debug == True:
            self.depletemp(Player)
            Game_State.next_turn = False
        elif word == "No HP" and Game_State.Debug == True:
            self.depletehp(Player)
            Game_State.next_turn = False
        elif word == self.Cheat:
            if Game_State.Debug == True:
                Game_State.Debug = False
                self.screen.addstr(" * Debug disabled")
            else:
                Game_State.Debug = True
                self.screen.addstr(" * Debug enabled")
        #---------------------------------------------------------------------
        #                               Typo
        #---------------------------------------------------------------------
        else:
            #You stumble and miss!
           Scene.log.append(Scene.make_line(8, "Menu", {}))
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
                Scene.screen.addstr(Scene.line, 1, Scene.make_line(107, "Story", {}))
                Scene.line += 1
        elif self.bools["Up"] == True and type(Room) is Dungeon:
            Game_State.change_floors(Player, Scene, self, 1)
        elif self.bools["Down"] == True and type(Room) is Dungeon:
            if Room.Solved == True:
                Game_State.change_floors(Player, Scene, self, -1)
            else:
                Scene.screen.addstr(Scene.line, 1, Scene.make_line(107, "Story", {}))
                Scene.line += 1
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
            Player.study_magic(Scene, self, Game_State)
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
                Scene.screen.addstr(Scene.line, 1, Scene.make_line(6, "Menu", {}))
                Scene.line += 1
        #---------------------------------------------------------------------
        #                               Status
        #---------------------------------------------------------------------
        elif self.bools["Status"] == True:
            Scene.screen.addstr(Player.Scan(Scene))
        #---------------------------------------------------------------------
        #                   Continue Walking Through Dungeon
        #---------------------------------------------------------------------
        elif self.bools["Attack"] == True or self.bools["Resume"] == True and type(Room) is Dungeon:
            #Take next step in dungeon
            if Room.Steps_Taken < Room.Steps:
                Room.action = False
            else:
                #Continue Fighting
                Room.start_battle(Player, Scene, self, Game_State)
        #---------------------------------------------------------------------
        #                               Save
        #---------------------------------------------------------------------
        elif response in self.save:
            save = Files()
            save.save(Player, Game_State, Scene)
            save.__delete__()
        #---------------------------------------------------------------------
        #                               Debug
        #---------------------------------------------------------------------
        elif response == "Pockets" and Game_State.Debug == True:
            self.fill_inventory(Player)
            Scene.screen.addstr(" * Debug: Inventory Filled")
        elif response == "Solve" and Game_State.Debug == True:
            self.solve(Room)
            Scene.screen.addstr(" * Debug: Room Solved")
        elif response == "No MP" and Game_State.Debug == True:
            self.depletemp(Player)
            Scene.screen.addstr(" * Debug: MP Depleted")
        elif response == "No HP" and Game_State.Debug == True:
            self.depletehp(Player)
            Scene.screen.addstr(" * Debug: HP Depleted")
        elif response == "Level" and Game_State.Debug == True:
            self.levelup(Player, Scene)
        elif response == "Ten" and Game_State.Debug == True:
            counter = 0
            while counter < 10:
                self.levelup(Player, Scene)
                counter += 1
        elif response == "Textbook" and Game_State.Debug == True:
            Player.Upgrades["Value"] += 10
            Scene.screen.addstr(" * Debug: Upgrades available")
        elif response == "Know It All" and Game_State.Debug == True:
            self.learn_all_spells(Player)
            Scene.screen.addstr(" * Debug: Spells Learned")
        elif response == "Interactables" and Game_State.Debug == True:
            for a in range(len(Room.Interactables)):
                Scene.screen.addstr(str(Room.Interactables[a].Name))
                for b in range(len(Room.Interactables[a].Keys)):
                    Scene.screen.addstr(Room.Interactables[a].Keys)
        elif response == self.Cheat:
            if Game_State.Debug == True:
                Game_State.Debug = False
                Scene.screen.addstr(" * Debug disabled")
            else:
                Game_State.Debug = True
                Scene.screen.addstr(" * Debug enabled")
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
        self.screen = Scene.screen
        keywords = []
        for a in range(len(Interactable.Commands)):
            if Interactable.Commands[a] in Response:
                keywords.append(Interactable.Commands[a])
        if len(keywords) == 1:
            for b in range(len(Interactable.Keys)):
                if keywords[0] in Interactable.Keys[b]["Terms"]:
                    Interactable.update_keys(Player, Scene, Interactable.Keys[b]["Name"], Game_State)
        elif len(keywords) > 1:
            Scene.screen.addstr(Scene.line, 1, Scene.make_line(46, "Menu", {}))
            Scene.line +=1
        else:
            if self.bools["Examine"] == True:
                Scene.screen.addstr(Scene.line, 1, Scene.get_interactable_string(Interactable, "Examine", Player))
#---------------------------------------------------------------------------------------------------------------------------------------
#                                                                Main Menu Commands
#---------------------------------------------------------------------------------------------------------------------------------------
    def translate_main_menu_command(self, Response, Player, File, Game_State, Scene):
        self.screen = Scene.screen
        Response = Response.title()
        if Game_State.Options == False:
            #---------------------------------------------------------------------
            #                             About
            #---------------------------------------------------------------------
            if Response == "About":
                Game_State.loop = False
                Game_State.about(Player, self, Scene)
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
                self.screen.addstr(Scene.print_message(90, False, "Menu", {}))
                File.load(Player, Game_State, self, Scene)
            #---------------------------------------------------------------------
            #                             Options
            #---------------------------------------------------------------------
            elif Response == "Options" and File.Continue() == True:
                Game_State.loop = False
                Game_State.options(Player, self, Scene, File)
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
                Game_State.credits(Player, self, Scene)
            #---------------------------------------------------------------------
            #                              Quit
            #---------------------------------------------------------------------
            elif Response == "Quit":
                Game_State.loop = False
                Game_State.quit(Player, self, Scene)
        else: #In Options Menu
        #---------------------------------------------------------------------
        #                              Options
        #---------------------------------------------------------------------
            if Response == "Change Names":
                File.choose_rename(Player, self, Scene)
                Game_State.options(Player, self, Scene, File)
            elif Response == "Delete Save Data":
                File.delete_save_data(Player, self, Scene)
                Game_State.Options = False
                Game_State.loop = False
                Game_State.initialize()
            elif self.bools["Exit"] == True:
                Game_State.Options = False
                Game_State.loop = False
                Game_State.main_menu(Player, self, Scene)
