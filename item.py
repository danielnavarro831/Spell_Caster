import xlrd
import random

class Item:
    def __init__(self, name): #self, "name"
        name = name.title()
        self.Info = {"Name": name}
        source = xlrd.open_workbook('C:\\Users\\Daniel\\source\\repos\\Spell Caster\\Spell_Caster_Strings.xlsx')
        Sheet = source.sheet_by_index(6)
        row = 0
        while Sheet.cell(row, 0).value != self.Info["Name"]:
            row += 1
            if str(Sheet.cell(row, 0).value) == self.Info["Name"]:
                #--------------------------------------------------------------
                #                          Set Values
                #--------------------------------------------------------------
                #Set 'Key Item' status
                self.Info["Key"] = Sheet.cell(row, 1).value
                #Set Consumable status
                self.Info["Consumable"] = Sheet.cell(row, 2).value
                #Set Value
                if Sheet.cell(row, 3).value:
                    self.Info["Value"] = Sheet.cell(row, 3).value
                #Set Affected Stats
                if Sheet.cell(row, 4).value:
                    if ', ' in Sheet.cell(row, 4).value:
                        stats = Sheet.cell(row, 4).value
                        self.Info["Restores"] = stats.split(', ')
                    else:
                        self.Info["Restores"] = Sheet.cell(row, 4).value
                #Set Ingredient Status
                self.Info["Ingredient"] = Sheet.cell(row, 5).value

    def use_consumable_item(self, Actor, Scene, Game_State): #self, Class, Class, Class
        if self.Info["Name"] in Actor.Inventory and self.Info["Consumable"] == True:
            if Actor.Inventory[self.Info["Name"]] > 0:
                #--------------------------------------------------------------
                #                       Unstable Potion
                #--------------------------------------------------------------
                if self.Info["Name"] == "Unstable Potion":
                    values = ["Weaknesses", "Resistances", "Heals", -20, 20, 50, -50]
                    elems = [Actor.Fire["Name"], Actor.Ice["Name"], Actor.Water["Name"], Actor.Wind["Name"], Actor.Lightning["Name"]]
                    restore = [Actor.HP["Name"], Actor.MP["Name"]]
                    rando = random.randint(0, len(values) -1)
                    self.Info["Value"] = values[6]
                    if type(self.Info["Value"]) is str:
                        rando = random.randint(0, len(elems)-1)
                        self.Info["Restores"] = elems[rando]
                    else:
                        rando = random.randint(0, len(restore)-1)
                        self.Info["Restores"] = restore[0]
                    print(self.Info)
                    print(type(self.Info["Value"]))
                #--------------------------------------------------------------
                #                       Consume Potion
                #--------------------------------------------------------------
                if isinstance(self.Info["Restores"], list):
                    amounts = []
                    stats = []
                    restored = False
                    for a in range(len(self.Info["Restores"])):
                        for stat in range(len(Actor.Stats)):
                            if Actor.Stats[stat]["Name"] == self.Info["Restores"][a]:
                                if type(self.Info["Value"]) is float or type(self.Info["Value"]) is int:
                                    restored = True
                                    percentage = int(Actor.Stats[stat]["Max"] - (Actor.Stats[stat]["Max"] * (100 - abs(self.Info["Value"]))/100))
                                    stats.append(Actor.Stats[stat]["Name"])
                                    amounts.append(percentage)
                                    if self.Info["Value"] > 0:
                                        Actor.Stats[stat]["Value"] += percentage
                                    else:
                                        Actor.Stats[stat]["Value"] -= percentage
                                        if Actor.HP["Value"] <= 0 and Game_State.battle != True:
                                            Actor.HP["Value"] = 1
                                        if Actor.MP["Value"] < 0:
                                            Actor.MP["Value"] = 0
                                elif self.Info["Value"] == "Resistances":
                                    Actor.Resistances += [self.Info["Restores"][a]]
                                    print(Scene.print_message(57, False, "Menu", {"{Name}":Actor.Name["Value"], "{elem}": self.Info["Restores"][a]}))
                                elif self.Info["Value"] == "Weaknesses":
                                    Actor.Weaknesses += [self.Info["Restores"][a]]
                                    print(Scene.print_message(58, False, "Menu", {"{Name}":Actor.Name["Value"], "{elem}": self.Info["Restores"][a]}))
                                elif self.Info["Value"] == "Heals":
                                    Actor.Heals += [self.Info["Restores"][a]]
                                    print(Scene.print_message(59, False, "Menu", {"{Name}":Actor.Name["Value"], "{elem}": self.Info["Restores"][a]}))
                    if restored == True:
                        #{Name} restored {amount} {stat} and {amount} {stat}
                        if self.Info["Value"] > 0:
                            print(Scene.print_message(23, False, "Menu", {"{Name}": Actor.Name["Value"], "{Amount}": amounts, "{Stat}": stats}))
                        else:
                            print(Scene.print_message(72, False, "Menu", {}))
                            print(Scene.print_message(73, False, "Menu", {"{Name}": Actor.Name["Value"], "{Amount}": amounts, "{Stat}": stats}))
                else:
                    for stat in range(len(Actor.Stats)):
                        if Actor.Stats[stat]["Name"] == self.Info["Restores"]:
                            if type(self.Info["Value"]) is float or type(self.Info["Value"]) is int:
                                percentage = int(Actor.Stats[stat]["Max"] - (Actor.Stats[stat]["Max"] * (100 - abs(self.Info["Value"]))/100))
                                if self.Info["Value"] > 0:
                                    Actor.Stats[stat]["Value"] += percentage
                                    #{Name} restored {amount} {stat}
                                    print(Scene.print_message(4, False, "Menu", {"{Name}": Actor.Name["Value"], "{Amount}": percentage, "{Stat}": self.Info["Restores"]}))
                                else:
                                    Actor.Stats[stat]["Value"] -= percentage
                                    #Unstable potion is poisonous!
                                    print(Scene.print_message(72, False, "Menu", {}))
                                    #{Name} loses {Amount} {Stat}
                                    print(Scene.print_message(74, False, "Menu", {"{Name}": Actor.Name["Value"], "{Amount}": percentage, "{Stat}": self.Info["Restores"]}))
                                if Actor.Stats[stat]["Value"] > Actor.Stats[stat]["Max"]:
                                    Actor.Stats[stat]["Value"] = Actor.Stats[stat]["Max"]
                                if Actor.HP["Value"] <= 0 and Game_State.battle != True:
                                    Actor.HP["Value"] = 1
                                if Actor.MP["Value"] < 0:
                                    Actor.MP["Value"] = 0
                            elif self.Info["Value"] == "Resistances":
                                Actor.Resistances += [self.Info["Restores"]]
                                print(Scene.print_message(57, False, "Menu", {"{Name}":Actor.Name["Value"], "{elem}": self.Info["Restores"]}))
                            elif self.Info["Value"] == "Weaknesses":
                                Actor.Weaknesses += [self.Info["Restores"]]
                                print(Scene.print_message(58, False, "Menu", {"{Name}":Actor.Name["Value"], "{elem}": self.Info["Restores"]}))
                            elif self.Info["Value"] == "Heals":
                                Actor.Heals += [self.Info["Restores"]]
                                print(Scene.print_message(59, False, "Menu", {"{Name}":Actor.Name["Value"], "{elem}": self.Info["Restores"]}))
                Actor.Inventory[self.Info["Name"]] -= 1
            else:
                #None in inventory
                print(Scene.print_message(2, False, "Menu", {}))
        else:
            #You can't use that item right now
            print(Scene.print_message(3, False, "Menu", {}))
            
    def __delete__(self):
        del self