from actor import *
import random

class Interactable:
    def __init__(self, name): #self, "name"
        self.Name = name
        self.Commands = []
        self.Keys = []
        self.Solved = False
        self.Counter = 0

    def update_keys(self, Player, Scene, Key, Game_State): #self, Class, Class, "Key", Class
        #Ex Key: Fire = {"Name": ["Fire", "Candle"], "Value": False, "Type": "Spell", "Terms": ["Burn", "Fire", "Melt"]}
        for a in range(len(self.Keys)):
            if self.Keys[a]["Name"] == Key:
                if self.Keys[a]["Value"] == False:
                    #-------------------------------------------------------------------------------------------
                    #                                      Key is an Item
                    #-------------------------------------------------------------------------------------------
                    if self.Keys[a]["Type"] == "Item":
                        if self.Keys[a]["Name"] in Player.Inventory:
                            if Player.Inventory[self.Keys[a]["Name"]] > 0:
                                Player.Inventory[self.Keys[a]["Name"]] -= 1
                                print(Scene.print_message(43, False, "Menu", {"{Item}":self.Keys[a]["Name"]}))
                                self.Keys[a]["Value"] = True
                                if "Chest" not in self.Name:
                                    print(Scene.get_interactable_string(self, Key, Player))
                                else:
                                    print(Scene.get_interactable_string(self, "Open", Player))
                            else:
                                #None in inventory
                                if "Chest" not in self.Name:
                                    print(Scene.print_message(2, False, "Menu", {}))
                                else:
                                    #It's locked
                                    print(Scene.print_message(42, False, "Menu", {}))
                        else:
                            #None in inventory
                            if "Chest" not in self.Name:
                                print(Scene.print_message(2, False, "Menu", {}))
                            else:
                                #It's locked
                                print(Scene.print_message(42, False, "Menu", {}))
                    #-------------------------------------------------------------------------------------------
                    #                                      Key is a Spell
                    #-------------------------------------------------------------------------------------------
                    elif self.Keys[a]["Type"] == "Spell":
                        #Calculate cost
                        for stat in range(len(Player.Stats)):
                            if Player.Stats[stat]["Name"] == self.Keys[a]["Name"]:
                                if Player.known_spell(Player.Stats[stat]["Name"]) == True:
                                    if Player.spend_MP(Player.Stats[stat]["Name"], Game_State, Scene) == True:
                                        print(Scene.get_interactable_string(self, Key, Player))
                                        self.Keys[a]["Value"] = True
                                else:
                                    #You don't know that spell yet
                                    print(Scene.print_message(6, False, "Menu", {}))
                    #-------------------------------------------------------------------------------------------
                    #                                      Key is a switch
                    #-------------------------------------------------------------------------------------------
                    else:
                        #Not an item
                        self.Keys[a]["Value"] = True
                        print(Scene.get_interactable_string(self, Key, Player))#Key = Command
        count = 0
        for key in range(len(self.Keys)):
            if self.Keys[key]["Value"] == True:
                count += 1
        if count == len(self.Keys):
            self.Solved = True

    def __delete__(self):
        del self
#------------------------------------------------------------------------------------------------------------------------------------------
#                                                                  ROOM CLASS
#------------------------------------------------------------------------------------------------------------------------------------------
class Room(Interactable):
    #Story room - nothing to fight
    def __init__(self, name, scene_num, interactables): #self, "name", int, [Class, Class, Class]
        super().__init__(name)
        self.Description = scene_num
        self.Interactables = interactables
        self.Floor = 0
        self.loop = False

    def enter_room(self, Player, Scene, Controller, Game_State): #self, Class, Class, Class
        Game_State.in_dungeon = False
        floors = {0:self.ground_floor, 1:self.tower1, 2:self.tower2, 3:self.tower3, 4:self.tower4, 5:self.tower5}
        print(Scene.print_message(1, False, "Room", {"{Room}": self.Name}))
        floors[self.Floor](Player, Scene, Controller, Game_State)

    def ground_floor(self, Player, Scene, Controller, Game_State): #self, Class, Class, Class
        self.loop = True
        hint_trigger = 0
        while self.loop == True and Game_State.game_over == False:
            if len(self.Interactables) > 0:
                print(Scene.print_message(self.Description, False, "Room", {}))
            print(Scene.print_message(6, False, "Room", {}))
            if len(self.Interactables) > 0:
                if self.Interactables[0].Solved == False:
                    line = Scene.print_message(4, False, "Room", {})
                    line += self.Interactables[0].Name[0]
                    print(line)
                    Controller.get_command(Player, self, Game_State, Scene)
                    if self.Interactables[0].Solved == True:
                        print(Scene.print_message(105, False, "Story", {}))
                        print(Scene.print_message(41, False, "Menu", {"{Name}":Player.Name["Value"], "{Item}": "an Old Key"}))
                        Player.Inventory["Old Key"] = 1
                        self.Description = 45
                        hint_trigger = 0
                        self.Interactables[0].__delete__()
                        self.Interactables = []
                    else:
                        hint_trigger += 1
                    if hint_trigger >= 3:
                        print(Scene.print_message(108, False, "Story", {}))
                        hint_trigger = 0
            else:
                Controller.get_command(Player, self, Game_State, Scene)

    def tower1(self, Player, Scene, Controller, Game_State): #self, Class, Class, Class
        self.loop = True
        treasure = False
        hint_Trigger = 0
        while self.loop == True and Game_State.game_over == False:
            if self.Solved == False:
                for a in range(len(self.Interactables)):
                    if "Chest" in self.Interactables[a].Name:
                        treasure = True
                print(Scene.print_message(self.Description, False, "Room", {}))
                if treasure == True:
                    print(Scene.print_message(14, False, "Room", {}))
                Controller.get_command(Player, self, Game_State, Scene)
                if "Fire" in self.Interactables[0].Name:
                    if self.Interactables[0].Solved == True:
                        self.Counter += 1
                        if self.Counter < 2:
                            self.Interactables[0].Name = ["Ice", "Candle", "Fire"]
                            self.Description = 9
                            self.Interactables[0].Solved = False
                            self.Interactables[0].Keys[0]["Value"] = False
                            self.Interactables[0].Keys[0]["Terms"] = ["Fire", "Melt", "Burn", "Light"]
                            self.Interactables[0].Commands = ["Fire", "Melt", "Burn", "Light"]
                            hint_Trigger = 0
                        else:
                            self.Interactables[0].__delete__()
                            pool = Interactable(["Water", "Pool", "Ice"])
                            pool.Commands = ["Ice", "Freeze"]
                            pool.Keys=[{"Name": "Ice", "Value": False, "Type": "Spell", "Terms": ["Ice", "Freeze"]}]
                            self.Interactables = [pool]
                            self.Description = 10
                            chest = Interactable("Chest")
                            chest.Commands = ["Open", "Unlock"]
                            chest.Keys = [{"Name": "Old Key", "Value":False, "Type":"Item", "Terms":["Open", "Unlock"]}]
                            self.Interactables += [chest]
                            treasure = True
                            hint_Trigger = 0
                    else:
                        hint_Trigger +=1 
                        if hint_Trigger >= 3:
                            print(Scene.print_message(113, False, "Story", {}))
                elif "Water" in self.Interactables[0].Name:
                    if self.Interactables[0].Solved == True:
                        self.Interactables[0].__delete__()
                        self.Description = 11
                        self.Solved = True
                        hint_Trigger = 0
                    else:
                        hint_Trigger += 1
                        if hint_Trigger >= 3:
                            print(Scene.print_message(114, False, "Story", {}))
                for a in range(len(self.Interactables)):
                    if self.Interactables[a].Name == "Chest":
                        treasure = True
                        if self.Interactables[a].Solved == True:
                            self.open_chest(Player, Scene, "Hi-Potion", 1)
                            self.Interactables[a].__delete__()
                            if "Water" in self.Interactables[0].Name:
                                self.Interactables = [self.Interactables[0]]
                            else:
                                self.Interactables = []
                            treasure = False
            else:
                for a in range(len(self.Interactables)):
                    if "Chest" in self.Interactables[a].Name:
                        treasure = True
                print(Scene.print_message(self.Description, False, "Room", {}))
                if treasure == True:
                    print(Scene.print_message(14, False, "Room", {}))
                print(Scene.print_message(13, False, "Room", {}))
                Controller.get_command(Player, self, Game_State, Scene)
                if treasure == True:
                    for a in range(len(self.Interactables)):
                        if self.Interactables[a].Name == "Chest":
                            if self.Interactables[a].Solved == True:
                                self.open_chest(Player, Scene, "Hi-Potion", 1)
                                self.Interactables[a].__delete__()
                                self.Interactables = []
                                treasure = False

    def tower2(self, Player, Scene, Controller, Game_State): #self, Class, Class, Class
        self.loop = True
        hint_trigger = 0
        while self.loop == True and Game_State.game_over == False:
            if self.Solved == False:
                if self.Interactables[0].Solved == False:
                    if self.Description == 15:
                        self.Counter = 1
                        print(Scene.print_message(self.Description, False, "Room", {}))
                        self.Description += 1
                        print(Scene.print_message(self.Description, False, "Room", {}))
                        self.Description += 1
                        print(Scene.print_message(self.Description, False, "Room", {}))
                        self.Description += 1
                    print(Scene.print_message(self.Description, False, "Room", {"{Num}":str(self.Counter), "{Ingredient}":self.Interactables[0].Keys[0]["Name"]}))
                    Controller.get_command(Player, self, Game_State, Scene)
                    if "Water" in self.Interactables[0].Keys[0]["Name"]:
                        if self.Interactables[0].Solved == True:
                            self.Interactables[0].Name = ["Cauldron", "Dragon Scale", "Scale"]
                            self.Interactables[0].Solved = False
                            self.Interactables[0].Keys = [{"Name": "Dragon Scale", "Value": False, "Type": "Item", "Terms":["Add", "Put", "Drop"]}]
                            self.Interactables[0].Commands = self.Interactables[0].Keys[0]["Terms"]
                            self.Description += 1
                            self.Counter += 1
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(116, False, "Story", {}))
                                hint_trigger = 0
                    elif "Dragon Scale" in self.Interactables[0].Keys[0]["Name"]:
                        if self.Interactables[0].Solved == True:
                            self.Interactables[0].Name = ["Cauldron", "Yetti Fur", "Fur"]
                            self.Interactables[0].Solved = False
                            self.Interactables[0].Keys = [{"Name": "Yetti Fur", "Value": False, "Type": "Item", "Terms":["Add", "Put", "Drop"]}]
                            self.Interactables[0].Commands = self.Interactables[0].Keys[0]["Terms"]
                            self.Counter += 1
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(117, False, "Story", {}))
                                hint_trigger = 0
                    elif "Yetti Fur" in self.Interactables[0].Keys[0]["Name"]:
                        if self.Interactables[0].Solved == True:
                            self.Interactables[0].Name = ["Cauldron", "Charred Finger", "Finger"]
                            self.Interactables[0].Solved = False
                            self.Interactables[0].Keys = [{"Name": "Charred Finger", "Value": False, "Type": "Item", "Terms":["Add", "Put", "Drop"]}]
                            self.Interactables[0].Commands = self.Interactables[0].Keys[0]["Terms"]
                            self.Counter += 1
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(117, False, "Story", {}))
                                hint_trigger = 0
                    elif "Charred Finger" in self.Interactables[0].Keys[0]["Name"]:
                        if self.Interactables[0].Solved == True:
                            self.Interactables[0].Name = ["Cauldron", "Fire"]
                            self.Interactables[0].Solved = False
                            self.Interactables[0].Keys = [{"Name": "Fire", "Value": False, "Type": "Spell", "Terms":["Light", "Fire", "Heat"]}]
                            self.Interactables[0].Commands = self.Interactables[0].Keys[0]["Terms"]
                            self.Description += 1
                            self.Counter += 1
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(117, False, "Story", {}))
                                hint_trigger = 0
                    elif "Fire" in self.Interactables[0].Keys[0]["Name"]:
                        if self.Interactables[0].Solved == True:
                            self.Interactables[0].Name = ["Cauldron", "Ice"]
                            self.Interactables[0].Solved = False
                            self.Interactables[0].Keys = [{"Name": "Ice", "Value": False, "Type": "Spell", "Terms":["Cool", "Freeze", "Ice"]}]
                            self.Interactables[0].Commands = self.Interactables[0].Keys[0]["Terms"]
                            self.Description += 1
                            self.Counter += 1
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(118, False, "Story", {}))
                                hint_trigger = 0
                    elif "Ice" in self.Interactables[0].Keys[0]["Name"]:
                        if self.Interactables[0].Solved == True:
                            self.Interactables[0].__delete__()
                            potion = Interactable(["Strength Draught", "Draught", "Drink"])
                            self.Interactables = [potion]
                            Player.Inventory["Strength Draught"] = 1
                            self.Interactables[0].Keys = [{"Name": "Strength Draught", "Value": False, "Type": "Item", "Terms":["Drink", "Chug", "Gulp", "Consume", "Use"]}]
                            self.Interactables[0].Commands = self.Interactables[0].Keys[0]["Terms"]
                            self.Description += 1
                            self.Counter += 1
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(119, False, "Story", {}))
                                hint_trigger = 0
                    elif "Strength Draught" in self.Interactables[0].Keys[0]["Name"]:
                        if self.Interactables[0].Solved == True:
                            Player.Strength["Value"] += 1
                            print(Scene.print_message(25, False, "Menu", {"{Name}": Player.Name["Value"], "{Stat}": Player.Strength["Name"], "{Amount}": 1}))
                            self.Interactables[0].__delete__()
                            door = Interactable(["Door", "Stone Door", "Heavy Door"])
                            self.Interactables = [door]
                            self.Interactables[0].Keys = [{"Name": "Push", "Value": False, "Type": "None", "Terms":["Open", "Unlock", "Push"]}]
                            self.Interactables[0].Commands = self.Interactables[0].Keys[0]["Terms"]
                            self.Description += 1
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(120, False, "Story", {}))
                                hint_trigger = 0
                    elif "Push" in self.Interactables[0].Keys[0]["Name"]:
                        if self.Interactables[0].Solved == True:
                            self.Solved = True
                            self.Interactables[0].__delete__()
                            self.Interactables = []
                            self.Description += 1
                            Scene.print_message([*range(75, 80)], True, "Menu", [{"{Command}": "'Brew'"}, {}, {}, {}, {}, {}])
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(121, False, "Story", {}))
                                hint_trigger = 0
            else:
                self.Commands = {"Brew": Player.brew_potion}
                print(Scene.print_message(self.Description, False, "Room", {}))
                print(Scene.print_message(13, False, "Room", {}))
                Controller.get_command(Player, self, Game_State, Scene)

    def tower3(self, Player, Scene, Controller, Game_State): #self, Class, Class, Class
        self.loop = True
        treasure = False
        poison = False
        hint_trigger = 0
        while self.loop == True and Game_State.game_over == False:
            for a in range(len(self.Interactables)):
                if "Chest" in self.Interactables[a].Name:
                    if self.Interactables[a].Solved == False:
                        treasure = True
                elif "Poison" in self.Interactables[a].Name:
                    if self.Interactables[a].Solved == False:
                        poison = True
            if self.Solved == False:
                if treasure == True:
                    print(Scene.print_message(14, False, "Room", {}))
                if poison == True:
                    print(Scene.print_message(39, False, "Room", {}))
                print(Scene.print_message(self.Description, False, "Room", {}))
                Controller.get_command(Player, self, Game_State, Scene)
                remove = False
                add = False
                pos = 0
                for a in range(len(self.Interactables)):
                    if "Poison" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            remove = True
                            hint_trigger = 0
                            pos = a
                            poison = False
                        else:
                            amount = int(Player.HP["Max"] - (Player.HP["Max"] * (100 - 25)/100))
                            print(Scene.print_message(25, False, "Room", {"{Name}": Player.Name["Value"], "{Amount}":amount, "{HP}":Player.HP["Name"]}))
                            Player.HP["Value"] -= amount
                            if Player.HP["Value"] <= 0:
                                Game_State.game_over = True
                                break
                            else:
                                hint_trigger += 1
                                if hint_trigger >= 3:
                                    print(Scene.print_message(122, False, "Story", {}))
                                    hint_trigger = 0
                    elif "Torch" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            self.Description += 1
                            self.Counter += 1
                            add = True
                            remove = True
                            pos = a
                    elif "Pit" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            self.Description += 1
                            self.Counter += 1
                            add = True
                            remove = True
                            pos = a
                    elif "Pool" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            self.Description += 1
                            self.Counter += 1
                            add = True
                            remove = True
                            pos = a
                    elif "Chest" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            Player.learn_recipe("Hi-Potion", Scene)
                            self.open_chest(Player, Scene, "Hi-Potion", 1)
                            remove = True
                            pos = a
                            treasure = False
                    elif "Door" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            self.Description += 1
                            remove = True
                            pos = a
                            self.Solved = True
                if Game_State.game_over != True:
                    if remove == True:
                        del self.Interactables[pos]
                        remove = False
                    if add == True:
                        if self.Counter == 1:
                            pit = Interactable(["Pit", "Hole", "Water"])
                            pit.Commands = ["Water", "Fill"]
                            pit.Keys = [{"Name": "Water", "Value": False, "Type":"Spell", "Terms":pit.Commands}]
                            self.Interactables.append(pit)
                        elif self.Counter == 2:
                            pool = Interactable(["Water", "Pool", "Ice"])
                            pool.Commands = ["Ice", "Freeze"]
                            pool.Keys = [{"Name": "Ice", "Value": False, "Type": "Spell", "Terms": pool.Commands}]
                            self.Interactables.append(pool)
                        elif self.Counter == 3:
                            chest = Interactable("Chest")
                            chest.Commands = ["Open", "Unlock"]
                            chest.Keys = [{"Name": "Ice Key", "Value": False, "Type": "Item", "Terms": chest.Commands}]
                            self.Interactables.append(chest)
                            door = Interactable(["Door", "Ice", "Fire"])
                            door.Commands = ["Fire", "Melt", "Burn"]
                            door.Keys = [{"Name": "Fire", "Value": False, "Type": "Spell", "Terms": door.Commands}]
                            self.Interactables.append(door)
                        add = False
                else:
                    self.loop = False
                    #Game Over
                    print(Scene.print_message(1, False, "Menu",{}))
                    Game_State.return_to_menu(Controller, Scene)
            else:
                remove = False
                pos = 0
                if treasure == True:
                    print(Scene.print_message(14, False, "Room", {}))
                if poison == True:
                    print(Scene.print_message(39, False, "Room", {}))
                print(Scene.print_message(13, False, "Room", {}))
                Controller.get_command(Player, self, Game_State, Scene)
                for a in range(len(self.Interactables)):
                    if "Chest" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            Player.learn_recipe("Hi-Potion", Scene)
                            self.open_chest(Player, Scene, "Hi-Potion", 1)
                            remove = True
                            pos = a
                            add = True
                            treasure = False
                    elif "Poison" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            remove = True
                            hint_trigger = 0
                            pos = a
                            poison = False
                        else:
                            amount = int(Player.HP["Max"] - (Player.HP["Max"] * (100 - 25)/100))
                            print(Scene.print_message(25, False, "Room", {"{Name}": Player.Name["Value"], "{Amount}":amount, "{HP}":Player.HP["Name"]}))
                            Player.HP["Value"] -= amount
                            if Player.HP["Value"] <= 0:
                                Game_State.game_over = True
                                break
                            else:
                                hint_trigger += 1
                                if hint_trigger >= 3:
                                    print(Scene.print_message(122, False, "Story", {}))
                                    hint_trigger = 0
                if remove == True:
                    del self.Interactables[pos]
                    remove = False
                if Game_State.game_over == True:
                    self.loop = False
                    #Game Over
                    print(Scene.print_message(1, False, "Menu",{}))
                    Game_State.return_to_menu(Controller, Scene)

    def tower4(self, Player, Scene, Controller, Game_State): #self, Class, Class, Class
        self.loop = True
        treasure = False
        poison = False
        hint_trigger = 0
        while self.loop == True and Game_State.game_over == False:
            for a in range(len(self.Interactables)):
                if "Chest" in self.Interactables[a].Name:
                    if self.Interactables[a].Solved == False:
                        treasure = True
                elif "Poison" in self.Interactables[a].Name:
                    if self.Interactables[a].Solved == False:
                        poison = True
            if self.Solved == False:
                remove = False
                add = False
                pos = 0
                if treasure == True:
                    print(Scene.print_message(14, False, "Room", {}))
                if poison == True:
                    print(Scene.print_message(39, False, "Room", {}))
                print(Scene.print_message(self.Description, False, "Room", {}))
                Controller.get_command(Player, self, Game_State, Scene)
                for a in range(len(self.Interactables)):
                    if "Circuit Board" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            self.Description += 1
                            print(Scene.print_message(self.Description, False, "Room", {}))
                            self.Description +=1
                            self.Counter += 1
                            hint_trigger = 0
                            remove = True
                            pos = a
                            add = True
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(123, False, "Story", {}))
                                hint_trigger = 0
                    elif "Torch" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            self.Description += 1
                            print(Scene.print_message(self.Description, False, "Room", {}))
                            self.Description += 1
                            self.Counter += 1
                            remove = True
                            pos = a
                            add = True
                    elif "Console" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            self.Description += 1
                            print(Scene.print_message(self.Description, False, "Room", {}))
                            self.Description += 1
                            self.Counter += 1
                            remove = True
                            pos = a
                            add = True
                            hint_trigger = 0
                        else:
                            hint_trigger += 1
                            if hint_trigger >= 3:
                                print(Scene.print_message(124, False, "Story", {}))
                    elif "Chest" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            Player.learn_recipe("Lightning Resistance", Scene)
                            self.open_chest(Player, Scene, "Mega-Ether", 1)
                            remove = True
                            pos = a
                            treasure = False
                    elif "Poison" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            remove = True
                            hint_trigger = 0
                            pos = a
                            poison = False
                        else:
                            amount = int(Player.HP["Max"] - (Player.HP["Max"] * (100 - 25)/100))
                            print(Scene.print_message(25, False, "Room", {"{Name}": Player.Name["Value"], "{Amount}":amount, "{HP}":Player.HP["Name"]}))
                            Player.HP["Value"] -= amount
                            if Player.HP["Value"] <= 0:
                                Game_State.game_over = True
                                break
                            else:
                                hint_trigger += 1
                                if hint_trigger >= 3:
                                    print(Scene.print_message(122, False, "Story", {}))
                                    hint_trigger = 0
                    elif "Fire" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            self.Description += 1
                            remove = True
                            pos = a
                            self.Solved = True
                if Game_State.game_over != True:
                    if remove == True:
                        del self.Interactables[pos]
                        remove = False
                    if add == True:
                        if self.Counter == 1:
                            torch = Interactable(["Torch", "Fire"])
                            torch.Commands = ["Fire", "Light", "Burn", "Melt"]
                            torch.Keys = [{"Name": "Fire", "Value": False, "Type": "Spell", "Terms": torch.Commands}]
                            self.Interactables.append(torch)
                        elif self.Counter == 2:
                            console = Interactable(["Console", "Energy Core"])
                            console.Commands = ["Add", "Insert", "Power"]
                            console.Keys = [{"Name": "Energy Core", "Value": False, "Type": "Item", "Terms": console.Commands}]
                            self.Interactables.append(console)
                        elif self.Counter == 3:
                            gas = Interactable(["Poison", "Gas", "Wind", "Air", "Miasma"])
                            gas.Commands = ["Wind", "Blow", "Clear"]
                            gas.Keys = [{"Name": "Wind", "Value": False, "Type": "Spell", "Terms": gas.Commands}]
                            self.Interactables.append(gas)
                            chest = Interactable("Chest")
                            chest.Commands = ["Open", "Unlock"]
                            chest.Keys = [{"Name": "Key Card", "Value": False, "Type": "Item", "Terms": chest.Commands}]
                            self.Interactables.append(chest)
                            fire = Interactable(["Fire", "Wall", "Water"])
                            fire.Commands = ["Water", "Extinguish", "Put Out"]
                            fire.Keys = [{"Name": "Water", "Value": False, "Type": "Spell", "Terms": fire.Commands}]
                            self.Interactables.append(fire)
                        add = False
                else:
                    self.loop = False
                    #Game Over
                    print(Scene.print_message(1, False, "Menu",{}))
                    Game_State.return_to_menu(Controller, Scene)
            else:
                remove = False
                pos = 0
                for a in range(len(self.Interactables)):
                    if "Chest" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == False:
                            treasure = True
                if treasure == True:
                    print(Scene.print_message(14, False, "Room", {}))
                print(Scene.print_message(self.Description, False, "Room", {}))
                print(Scene.print_message(13, False, "Room", {}))
                Controller.get_command(Player, self, Game_State, Scene)
                for a in range(len(self.Interactables)):
                    if "Chest" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            Player.learn_recipe("Lightning Resistance", Scene)
                            self.open_chest(Player, Scene, "Mega-Ether", 1)
                            remove = True
                            pos = a
                            add = True
                    elif "Poison" in self.Interactables[a].Name:
                        if self.Interactables[a].Solved == True:
                            remove = True
                            hint_trigger = 0
                            pos = a
                            poison = False
                        else:
                            amount = int(Player.HP["Max"] - (Player.HP["Max"] * (100 - 25)/100))
                            print(Scene.print_message(25, False, "Room", {"{Name}": Player.Name["Value"], "{Amount}":amount, "{HP}":Player.HP["Name"]}))
                            Player.HP["Value"] -= amount
                            if Player.HP["Value"] <= 0:
                                Game_State.game_over = True
                                break
                            else:
                                hint_trigger += 1
                                if hint_trigger >= 3:
                                    print(Scene.print_message(122, False, "Story", {}))
                                    hint_trigger = 0
                if remove == True:
                    del self.Interactables[pos]
                    remove = False
                if Game_State.game_over == True:
                    #Game Over
                    self.loop = False
                    print(Scene.print_message(1, False, "Menu",{}))
                    Game_State.return_to_menu(Controller, Scene)

    def tower5(self, Player, Scene, Controller, Game_State): #self, Class, Class, Class
        self.loop = True
        while self.loop == True and Game_State.game_over == False:
            if self.Solved == False:
                Scene.Top_of_Tower_pre_battle(Player, Controller, Game_State)
                self.Solved = True
                self.loop = False
            else:
                Controller.get_command(Player, self, Game_State, Scene)

    def open_chest(self, Player, Scene, Treasure, Amount): #self, Class, Class, "Treasure", int
        Player.add_item_to_inventory(Treasure, Amount)
        #{Name} acquired {Amount} {Item}
        print(Scene.print_message(26, False, "Menu", {"{Name}":Player.Name["Value"], "{Amount}": Amount, "{Item}":Treasure}))

    def add_interactable(self, Name, Solved, KeyName, Value, Commands, Type):
        thing = Interactable(Name)
        thing.Solved = Solved
        thing.Commands = Commands
        thing.Keys = [{"Name": KeyName, "Value": Value, "Type": Type, "Terms": Commands}]
        self.Interactables.append(thing)
#------------------------------------------------------------------------------------------------------------------------------------------
#                                                                DUNGEON CLASS
#------------------------------------------------------------------------------------------------------------------------------------------
class Dungeon(Room):
    def __init__(self, name, scene_num, interactables, level, type, steps): #self, "name", int, [Class], int, ["type"], int
        super().__init__(name, scene_num, interactables)
        self.Level = level
        self.Type = type
        self.Steps = steps
        self.Steps_Taken = 0
        self.loop = False
        self.action = False
        self.bottom_floor = False

    def enter_dungeon(self, Player, Scene, Controller, Game_State): #self, Class, Class, Class, Class
        Game_State.in_dungeon = True
        print(Scene.print_message(1, False, "Room", {"{Room}": self.Name}))
        Scene.print_message(self.Description, True, "Room", {})
        self.loop = True
        while self.loop == True:
            if self.Solved == False:
                if self.Steps_Taken < self.Steps and Game_State.game_over == False:
                    self.start_battle(Player, Scene, Controller, Game_State)
                    self.Steps_Taken += 1
                    self.action = True
                    if self.Steps_Taken >= self.Steps and Game_State.game_over == False:
                        if self.bottom_floor == False:
                            print(Scene.print_message([2, 3, 12], False, "Room", [{"{Room}": self.Name}, {}, {}]))
                        else:
                            print(Scene.print_message(46, False, "Room", {}))
                            print(Scene.print_message(47, False, "Room", {}))
                        self.Solved = True
                    while self.action == True and Game_State.game_over == False:
                        if self.Steps_Taken < self.Steps and Game_State.game_over == False:
                            print(Scene.print_message(30, False, "Room", {}))
                        response = Controller.get_command(Player, self, Game_State, Scene)
            else:
                while self.loop == True and Game_State.game_over == False:
                    if self.bottom_floor == False:
                        print(Scene.print_message(13, False, "Room", {}))
                        print(Scene.print_message(12, False, "Room", {}))
                    else:
                        print(Scene.print_message(46, False, "Room", {}))
                        print(Scene.print_message(47, False, "Room", {}))
                    response = Controller.get_command(Player, self, Game_State, Scene)
    
    def start_battle(self, Player, Scene, Controller, Game_State): #self, Class, Class, Class, Class
        if self.Steps_Taken == self.Steps -1:
            enemy = self.get_boss()
        else:
            #Randomize enemy traits
            random.shuffle(self.Type)
            #Randomize enemy loot drops
            Loot = ["Potion", "Hi-Potion", "Ether", "Hi-Ether", "Potion Recipe", "Hi-Potion Recipe", "Ether Recipe", "Hi-Ether Recipe"]
            random.shuffle(Loot)
            enemy = Enemy(self.Level, "", self.Type[0], [self.Type[0]], Game_State.get_loot_drops(Loot[0]))
            enemy.add_variance(self.Type[0])
            #A {Name} appeard!
        print(Scene.line_randomizer([37, 38, 39], "Menu", [{"{Name}": enemy.Name["Value"]}, {"{Name}": enemy.Name["Value"]}, {"{Name}": enemy.Name["Value"]}]))
        response = input(" ")
        Game_State.start_battle(Player, enemy, Controller, Scene)

    def get_boss(self):
        if "Fire" in self.Type:
            enemy = Enemy(1, "Grand Dragon", "", ["Fire", "Shell"], [])
            enemy.make_boss()
        elif "Ice" in self.Type:
            enemy = Enemy(1, "Yetti", "", ["Ice", "Protect"], [])
            enemy.make_boss()
        elif "Water" in self.Type:
            enemy = Enemy(1, "Leviathan", "", ["Water"], [])
            enemy.make_boss()
        elif "Wind" in self.Type:
            enemy = Enemy(1, "Ancient Tree", "", ["Wind", "Regen"], [])
            enemy.make_boss()
        elif "Lightning" in self.Type:
            enemy = Enemy(1, "Thunderbird", "", ["Wind", "Lightning"], [])
            enemy.make_boss()
        else:
            enemy = Enemy(1, "not boss", "", [], [])
        return enemy