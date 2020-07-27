import random
from spell import Spell
from item import Item
import xlrd

class Actor:
    def __init__(self, level, name): #self, int, "Name"
        self.player = False
        self.enemy = False
        self.Level = {"Name": "Level", "Value": level}
        self.XP = {"Name": "XP", "Value": 0, "Max": 0} #When Value matches Max, the player levels up
        self.Name = {"Name": "Name", "Value": name}
        self.HP = {"Name": "HP", "Value": 100 * level, "Max": 100 * level} #Health Points
        self.MP = {"Name": "MP", "Value": 100 * level, "Max": 100 * level} #Magic Points used for casting spells
        self.Accuracy = {"Name": "Accuracy", "Value": 85, "Max": 85} #Chance of landing a hit
        self.Magic = {"Name": "Magic", "Value": 9 + level} #Strength of Magic Spells
        self.MDef = {"Name": "Magic Defense", "Value": 4 + level} #Defense against enemy spells
        self.Strength = {"Name": "Strength", "Value": 9 + level} #Physical strength used for non-magic attacks
        self.Def = {"Name": "Defense", "Value": 4 + level} #Defense against enemy physical (non-magic) attacks
        self.Fire = {"Name": "Fire", "Value": 0, "Casts": 0, "Init": 2}
        self.Ice = {"Name": "Ice", "Value": 0, "Casts": 0, "Init": 2}
        self.Lightning = {"Name": "Lightning", "Value": 0, "Casts": 0, "Init": 2}
        self.Water = {"Name": "Water", "Value": 0, "Casts": 0, "Init": 2}
        self.Wind = {"Name": "Wind", "Value": 0, "Casts": 0, "Init": 2}
        self.Cure = {"Name": "Cure", "Value": 0, "Casts": 0, "Init": 2} #Heals caster's HP by ({Value} * Magic) /2
        self.Drain = {"Name": "Drain", "Value": 0, "Casts": 0, "Init": 2} #Heals caster's HP by stealing {Value} * Magic amount from enemy
        self.Curse = {"Name": "Curse", "Value": 0, "Duration": 0, "Max": 0, "Active": False, "Offering": False, "Casts": 0, "Init": 2} #Caster steals {Value}% of enemy's MaxHP for {Max} turns
        self.Sand = {"Name": "Sandstorm", "Value": 0, "Duration": 0, "Max": 0, "Active": False, "Casts": 0, "Init": 2} #Lowers enemy accuracy for {Max} number of turns
        self.Regen = {"Name": "Regen", "Value": 0, "Duration": 0, "Max": 0, "Active": False, "Casts": 0, "Init": 2} #Caster regains {Value}% of caster's MaxHP for {Max} turns
        self.Protect = {"Name": "Protect", "Value" : 0, "Duration": 0, "Max": 0, "Active": False, "Casts": 0, "Init": 2} #Reduces incoming physical attacks by {Value}% for {Max} turns
        self.Shell = {"Name": "Shell", "Value": 0, "Duration": 0, "Max": 0, "Active": False, "Casts": 0, "Init": 2} #Reduces incoming magical attacks by {Value}% for {Max} turns
        self.Sacrifice = {"Name": "Sacrifice", "Value": 0}
        self.Hits = {"Name": "Hits", "Value": 0}
        self.MHits = {"Name": "MHits", "Value": 0}
        self.Stats = [self.Name, self.Level, self.XP, self.HP, self.MP, 
                      self.Accuracy, self.Magic, self.MDef, self.Strength, self.Def, 
                      self.Fire, self.Ice, self.Lightning, self.Water, self.Wind, self.Sand,
                      self.Cure, self.Regen, self.Drain, self.Curse, self.Protect, self.Shell]

        self.Weaknesses = []
        self.Resistances = []
        self.Heals = []
        self.Inventory = {"Potion": 0, "Hi-Potion": 0, "Mega-Potion": 0,
                         "Ether": 0, "Hi-Ether": 0, "Mega-Potion": 0,
                         "Elixir": 0, "Hi-Elixir": 0, "Mega-Elixir": 0}

        self.Spells = {"Fire": self.Fire, "Ice": self.Ice, "Water": self.Water, "Wind": self.Wind, "Lightning": self.Lightning, "Sandstorm": self.Sand,
                       "Cure": self.Cure, "Regen": self.Regen, "Drain": self.Drain, "Curse": self.Curse,
                       "Protect": self.Protect, "Shell": self.Shell}

        self.Self_Target = [self.Cure["Name"], self.Regen["Name"], self.Protect["Name"], self.Shell["Name"]]

    def __delete__(self):
        del self

    def Scan(self, Scene): #self, Class
        Scan = ""
        lines = []
        for stat in range(len(self.Stats)):
            line = " "
            max = False
            duration = False
            if self.Stats[stat]["Name"] == "Name":
                line = Scene.print_header(self.Stats[stat]["Value"])
            if "Duration" in self.Stats[stat]: #Used to display spell duration if spell has duration
                duration = True
            if "Max" in self.Stats[stat]:  #Used for HP/MaxHP and MP/MaxMP. Displays as NextStat/CurrentStat
                max = True
            if max == False and self.Stats[stat]["Value"] != 0 and self.Stats[stat]["Name"] != "Name":
                line += self.Stats[stat]["Name"] + ": " + str(self.Stats[stat]["Value"])
            if max == True and duration == False:
                line += self.Stats[stat]["Name"] + ": " + str(self.Stats[stat]["Value"]) + "/" + str(self.Stats[stat]["Max"])
            if duration == True and max == True and self.Stats[stat]["Value"] != 0:
                line += self.Stats[stat]["Name"] + ": " + str(self.Stats[stat]["Value"]) + "  Duration: " + str(self.Stats[stat]["Duration"]) + "/" + str(self.Stats[stat]["Max"])
            if len(line) > 1:
                lines.append(line)
        if len(self.Weaknesses) > 0:
            line += "Weaknesses: "
            for weakness in range(len(self.Weaknesses)):
                line += self.Weaknesses[weakness]
                if weakness < len(self.Weaknesses) -1:
                    line += ", "
            lines.append(line)
        if len(self.Resistances) > 0:
            line += "Resistances: "
            for resist in range(len(self.Resistances)):
                line += self.Resistances[resist]
                if resist < len(self.Resistances) -1:
                    line += ", "
            lines.append(line)
        if len(self.Heals) > 0:
            line += "Absorbs: "
            for heal in range(len(self.Heals)):
                line += self.Heals[heal]
                if heal < len(self.Heals) -1:
                    line += ", "
            lines.append(line)
        line = ""
        lines.append(line)
        for line in range(len(lines)):
            Scan = "\n".join(lines)
        return Scan

    def accuracy_check(self):
        hits = False
        chance = random.randint(1, 100)
        if chance <= self.Accuracy["Value"]:
            hits = True
        return hits

    def crit_chance(self, damage): #self, int
        variant = random.uniform(1.0, 1.5)
        damage *= variant
        return int(damage)

    def cast_Spell(self, spell, enemy, game_state, Scene): #self, "Spell", Class, Class, Class
        if self.spend_MP(spell, game_state, Scene) == True:
            if spell not in self.Self_Target and game_state.battle == True:
                if self.accuracy_check() == True:
                    for stat in range(len(self.Stats)):
                        if self.Stats[stat]["Name"] == spell:
                            if "Duration" in self.Stats[stat]:
                                self.Stats[stat]["Duration"] = self.Stats[stat]["Max"]
                                self.Stats[stat]["Active"] = True
                                #{Name} casts {Spell}!
                                print(Scene.print_message(35, False, "Menu", {"{Name}": self.Name["Value"], "{Spell}": spell}))
                            else:
                                damage = self.Magic["Value"] * self.Stats[stat]["Value"]
                                #{Name} casts {Spell}!
                                print(Scene.print_message(35, False, "Menu", {"{Name}": self.Name["Value"], "{Spell}": spell}))
                                self.deal_damage(enemy, self.crit_chance(damage), self.Stats[stat]["Name"], game_state, Scene)
                else:
                    #{Name}'s attack missed!
                    print(Scene.print_message(11, False, "Menu", {"{Name}": self.Name["Value"]}))
            else:
                print(Scene.print_message(35, False, "Menu", {"{Name}": self.Name["Value"], "{Spell}": spell}))
                if spell in self.Self_Target:
                    for stat in range(len(self.Stats)):
                        if self.Stats[stat]["Name"] == spell:
                            if "Duration" in self.Stats[stat]:
                                self.Stats[stat]["Duration"] = self.Stats[stat]["Max"]
                                self.Stats[stat]["Active"] = True
                            else:
                                hp_restored = self.Magic["Value"] * self.Stats[stat]["Value"]
                                self.HP["Value"] += hp_restored
                                if self.HP["Value"] > self.HP["Max"]:
                                    self.HP["Value"] = self.HP["Max"]
                                print(Scene.print_message(4, False, "Menu", {"{Name}": self.Name["Value"], "{Amount}": hp_restored, "{Stat}": self.HP["Name"]}))
                                    
    def calculate_MP(self, spell): #self, {"spell": "dict"}
        spell_cost = int((spell["Value"] * self.Magic["Value"]) / 5)
        if "duration" in spell:
            spell_cost = int((spell["Value"] * spell["Max"]) / 2)
        return spell_cost

    def spend_MP(self, spell, game_state, Scene): #self, "Spell", Class, Class
        spell_dic = self.Spells[spell]
        cost = self.calculate_MP(spell_dic)
        if cost > self.MP["Value"]: #Not Enough MP
            if cost >= self.MP["Value"] + self.HP["Value"]: #Spell will Kill you
                #You don't have enough MP or HP to cast
                print(Scene.print_message(9, False, "Menu", {}))
                return False
            elif cost <= self.MP["Value"] + self.HP["Value"] and spell != "Cure":
                #You feel yourself losing energy...
                print(Scene.print_message(10, False, "Menu", {})) #Spell requires you to spend HP
                cost -= self.MP["Value"]
                self.MP["Value"] = 0
                self.Sacrifice["Value"] += cost
                self.HP["Value"] -= cost
                cost = 0
                if spell_dic["Name"] == self.Curse["Name"]:
                    self.Curse["Offering"] == True
                return True
            elif cost <= self.MP["Value"] + self.HP["Value"] and spell == "Cure":
                print(Scene.print_message(60, False, "Menu", {"{MP}": self.MP["Name"]}))
                return False
        else:
            self.MP["Value"] -= cost #You have enough MP
            cost = 0
            return True

    def attack(self, enemy, game_state, Scene): #self, Class, Class, Class
        if self.accuracy_check() == True:
            damage = self.Strength["Value"] * self.Level["Value"]
            damage = self.crit_chance(damage)
            self.deal_damage(enemy, damage, "Physical", game_state, Scene)
        else:
            #{Name}'s attack missed!
            print(Scene.print_message(11, False, "Menu", {"{Name}": self.Name["Value"]}))
    
    def deal_damage(self, enemy, damage, type, game_state, Scene): #self, Class, int, "type", Class, Class
        Magic = [self.Fire["Name"], self.Ice["Name"], self.Lightning["Name"], self.Water["Name"], self.Wind["Name"], "Magic"]
        #Apply weakness/resistance/heal/shield mods
        if type in Magic:
            mdef = enemy.MDef["Value"]
            damage -= mdef
            if enemy.Shell["Active"] == True:
                damage = int(damage *((100 - enemy.Shell["Value"])/100))
            if type in enemy.Weaknesses:
                damage *= 2
                #It's super effective!
                print(Scene.print_message(13, False, "Menu", {}))
            if type in enemy.Resistances:
                damage = int(damage / 2)
                #It's not very effective...
                print(Scene.print_message(15, False, "Menu", {}))
            if type in enemy.Heals:
                damage -= damage * 2
                #{Name} absorbed the attack!
                print(Scene.print_message(16, False, "Menu", {"{Name}": enemy.Name["Value"]}))
            enemy.MHits["Value"] += abs(damage)
        else:
            defense = enemy.Def["Value"]
            damage -= defense
            if enemy.Protect["Active"] == True:
                defense = int(damage *((100 - enemy.Protect["Value"])/100))
            enemy.Hits["Value"] += damage
        #Calculate Damage
        if damage < 0 and type not in enemy.Heals:
            damage = 0
        if damage > 0:
            enemy.HP["Value"] -= damage
            #{Name} deals {damage} damage to {target}!
            print(Scene.print_message(12, False, "Menu", {"{Name}": self.Name["Value"], "{Damage}": str(damage), "{Target}": enemy.Name["Value"]}))
            if enemy.HP["Value"] <= 0 and enemy.player == False:
                game_state.battle = False
            if enemy.HP["Value"] <= 0 and enemy.player == True and game_state.can_lose == False:
                game_state.game_over = True
            if enemy.HP["Value"] <= 0 and enemy.player == True and game_state.can_lose == True:
                game_state.battle = False
        else:
            if damage < 0:
                #{Name} restored {amount} {stat}
                print(Scene.print_message(4, False, "Menu", {"{Name}": enemy.Name["Value"], "{Amount}": str(abs(damage)), "{Stat}": enemy.HP["Name"]}))
                enemy.HP["Value"] -= damage
                if enemy.HP["Value"] > enemy.HP["Max"]: 
                    enemy.HP["Value"] = enemy.HP["Max"]
            else:
                #{Name} resisted {Name}'s attack!
                print(Scene.print_message(14, False, "Menu", {"{Name}": [enemy.Name["Value"], self.Name["Value"]]}))
    
    def known_spell(self, spell): #self, "spell"
        known = False
        spell = spell.title()
        for stat in range(len(self.Stats)):
            if self.Stats[stat]["Name"] == spell:
                if self.Stats[stat]["Value"] > 0:
                    known = True
                else:
                    known = False
        return known

    def reduce_duration(self, Enemy, Scene): #self, Class, Class
        for stat in range(len(self.Stats)):
            if "Duration" in self.Stats[stat] and self.Stats[stat]["Duration"] > 0:
                self.Stats[stat]["Duration"] -= 1
                if self.Stats[stat]["Duration"] == 0:
                    self.Stats[stat]["Active"] = False
                    if self.Stats[stat]["Name"] == self.Curse["Name"]:
                        #{Name}'s {Curse} lifted
                        print(Scene.print_message(17, False, "Menu", {"{Name}": Enemy.Name["Value"], "{Curse}": self.Curse["Name"]}))
                    else:
                        #{Name}'s {Spell} faded
                        print(Scene.print_message(18, False, "Menu", {"{Name}": self.Name["Value"], "{Spell}": self.Stats[stat]["Name"]}))

    def get_known_spells(self):
        spells = [self.Fire["Name"], self.Ice["Name"], self.Lightning["Name"], self.Water["Name"], self.Wind["Name"],
                  self.Cure["Name"], self.Regen["Name"], self.Drain["Name"], self.Curse["Name"], 
                  self.Protect["Name"], self.Shell["Name"]]
        known = []
        for stat in range(len(self.Stats)):
            for spell in range(len(spells)):
                if self.Stats[stat]["Name"] == spells[spell]:
                    if self.Stats[stat]["Value"] > 0:
                        known.append(spells[spell])
        return known

    def add_item_to_inventory(self, Item, quantity): #self, "Item", int
        if Item in self.Inventory:
            self.Inventory[Item] += quantity
        else:
            self.Inventory[Item] = quantity

    def drop_loot(self, Player, Scene): #self, Class, Class
        #Drop XP
        Player.XP["Value"] += self.XP["Value"]
        #{Name} gained {Amount} {Stat}
        print(Scene.print_message(25, False, "Menu", {"{Name}": Player.Name["Value"], "{Amount}": self.XP["Value"], "{Stat}": self.XP["Name"]}))
        #Drop Items
        for item in self.Inventory.keys():
            if self.Inventory[item] > 0:
                Player.add_item_to_inventory(item, self.Inventory[item])
                #{Name} acquired {Amount} {Item}
                print(Scene.print_message(26, False, "Menu", {"{Name}": Player.Name["Value"], "{Amount}": self.Inventory[item], "{Item}": item}))

    def rest(self):
        self.HP["Value"] = self.HP["Max"]
        self.MP["Value"] = self.MP["Max"]
        self.Accuracy["Value"] = self.Accuracy["Max"]
#------------------------------------------------------------------------------------------------------------------------------------------
#                                                                  PLAYER CLASS
#------------------------------------------------------------------------------------------------------------------------------------------
class Player(Actor):
    def __init__(self, level, name): #self, int, "name"
        super().__init__(level, name)
        self.player = True
        self.enemy = False
        self.XP["Max"] = self.Level["Value"] * (self.Level["Value"] * 100)
        self.Speakers = {"Grandfather": "Merlin", "Friend": "Morty", "Agatha": "Agatha"} #Used to store customized names (Grandfather, Best Friend, etc.)
        self.Upgrades = {"Name": "Chapter", "Value": 0}
        self.Recipes = []

    def level_up(self, Scene): #self, Class
        #{Name} leveled up!
        self.Level["Value"] += 1
        self.Upgrades["Value"] += 1
        print(Scene.print_header(Scene.print_message(33, False, "Menu", {"{Name}": self.Name["Value"]})))
        buff_stats = []
        buff_stats = [self.HP["Name"], self.Strength["Name"], self.Def["Name"], self.Accuracy["Name"], self.MP["Name"], self.Magic["Name"], self.MDef["Name"]]
        for stat in range(len(self.Stats)):
            if self.Stats[stat]["Name"] in buff_stats:
                increase_amount = 2
                if self.HP["Name"] in self.Stats[stat]["Name"] or self.MP["Name"] in self.Stats[stat]["Name"]:
                    increase_amount = 100
                    self.Stats[stat]["Max"] += increase_amount
                    self.Stats[stat]["Value"] = self.Stats[stat]["Max"]
                elif self.Accuracy["Name"] in self.Stats[stat]["Name"]:
                    increase_amount = 1
                    self.Stats[stat]["Max"] += increase_amount
                    self.Stats[stat]["Value"] = self.Stats[stat]["Max"]
                else:
                    self.Stats[stat]["Value"] += increase_amount
                #{Name} gained {Amount} {Stat}!
                print(Scene.print_message(25, False, "Menu", {"{Name}": self.Name["Value"], "{Amount}": str(increase_amount), "{Stat}": self.Stats[stat]["Name"]}))
        Scene.print_message(34, True, "Menu", {"{Chapter}": self.Upgrades["Name"]})

    def check_XP(self, Scene): #self, Class
        if self.XP["Value"] >= self.XP["Max"]:
            self.level_up(Scene)
            self.XP["Max"] = self.Level["Value"] * (self.Level["Value"] * 100)
            self.XP["Value"] = 0

    def study_magic(self, Scene, Controller, Game_State): #self, Class, Class, Class
        #Get list of learnable spells (new and learned)
        spell_book = Spell(self)
        spells = [self.Fire["Name"], self.Ice["Name"]]
        cond_list = spell_book.has_condition(self)
        for a in range(len(cond_list)):
            if spell_book.Check_Condition(self, cond_list[a]) == True:
                spells.append(cond_list[a])
        if self.Upgrades["Value"] > 0:
            print(Scene.print_message(48, False, "Menu", {}))
            for spell in range(len(spells)):
                message = ""
                if self.known_spell(spells[spell]) == True:
                    message = " * " + spells[spell]
                    print(message)
            print("")
            print(Scene.print_message(49, False, "Menu", {}))
            for spell in range(len(spells)):
                message = ""
                if self.known_spell(spells[spell]) == False:
                    message = " * " + spells[spell]
                    print(message)
            loop = True
            while loop == True:
                #Choose a spell to study
                print(Scene.print_message(31, False, "Menu", {}))
                response = Controller.get_response(self, False)
                response = response.title()
                if Game_State.tutorial == False:
                    if response in spells:
                        if self.known_spell(response) == False:
                            spell_book.learn_elem_spell(response, self, Scene)
                            loop = False
                        else:
                            spell_book.upgrade_spell(response, self, Scene, Controller)
                            loop = False
                        self.Upgrades["Value"] -= 1
                        if self.Upgrades["Value"] < 0:
                            self.Upgrades["Value"] = 0
                    else:
                        #You can't study that!
                        print(Scene.print_message(32, False, "Menu", {}))
                else: #Tutorial is on
                    if response in spells:
                        if self.known_spell(response) == True:
                            print(Scene.print_message(115, False, "Story", {}))
                        else:
                            spell_book.learn_elem_spell(response, self, Scene)
                            loop = False
                    else:
                        #You can't study that!
                        print(Scene.print_message(32, False, "Menu", {}))
        else:
            #You don't understand...
            Scene.print_message(30, True, "Menu", {})
        spell_book.__delete__()

    def get_spellbook(self, Game_State, Scene): #self, Class, Class
        spells = self.get_known_spells()
        line = Scene.make_line(47, "Menu", {})
        costs = [line]
        for spell in range(len(spells)):
            for stat in range(len(self.Stats)):
                if self.Stats[stat]["Name"] == spells[spell]:
                    cost = " * "+ self.Stats[stat]["Name"] + "...(" + str(self.calculate_MP(self.Stats[stat])) + ")MP"
                    costs.append(cost)
        if Game_State.battle == False:
            if self.Upgrades["Value"] > 0:
                line = Scene.make_line(44, "Menu", {"{Amount}":self.Upgrades["Value"]})
                costs.append(line)
        spellbook = '\n'.join(costs)
        return spellbook

    def get_inventory(self, Scene): #self, Class
        if len(self.Inventory) > 0:
            items = False
            print(Scene.print_message(55, False, "Menu", {}))
            for a in self.Inventory.keys():
                if self.Inventory[a] > 0:
                    print(" * " + a + ": " + str(self.Inventory[a]))
                    items = True
            if items == False:
                #Nothing in inventory
                print(Scene.print_message(45, False, "Menu", {}))
        else:
            #Nothing in inventory
            print(Scene.print_message(45, False, "Menu", {}))

    def brew_potion(self, Scene, Controller, Game_State): #self, Class, Class, Class
        #Player, Scene, self, Game_State)
        if self.spend_MP(self.Water["Name"], Game_State, Scene) == True:
            source = xlrd.open_workbook('C:\\Users\\Daniel\\source\\repos\\Spell Caster\\Spell_Caster_Strings.xlsx')
            Sheet = source.sheet_by_index(7) #Recipes page
            #Casts water
            print(Scene.print_message(35, False, "Menu", {"{Name}": self.Name["Value"], "{Spell}": self.Water["Name"]}))
            #Cauldron fills with water
            print(Scene.print_message(61, False, "Menu", {}))
            ingredients = []
            while len(ingredients) < 3:
                header = Scene.print_header(" Ingredients")
                print(header)
                listed = False
                for item in self.Inventory.keys():
                    if self.Inventory[item] > 0:
                        ingr = Item(item)
                        if ingr.Info["Ingredient"] == True:
                            print(" * " + item + "...(x" + str(self.Inventory[item]) + ")")
                            listed = True
                        ingr.__delete__()
                if listed == False:
                    #No ingredients in inventory
                    print(Scene.print_message(62, False, "Menu", {}))
                loop = True
                while loop == True:
                    #Type Ingredient name to add
                    print(Scene.print_message(63, False, "Menu", {}))
                    #Type Recipes to view recipes
                    print(Scene.print_message(64, False, "Menu", {}))
                    #Type Back to exit
                    print(Scene.print_message(65, False, "Menu", {}))
                    #Items in Cauldron
                    concoction = "None"
                    if len(ingredients) > 0:
                        concoction = ""
                        counter = 0
                        while counter < len(ingredients):
                            concoction += ingredients[counter]
                            if counter < len(ingredients) -1:
                                concoction += ", "
                            counter += 1
                    in_cauldron = Scene.make_line(71, "Menu", {}) + concoction
                    print(in_cauldron)
                    response = Controller.get_response(self, False)
                    response = response.title()
                    if response in self.Inventory:
                        if self.Inventory[response] > 0:
                            check = Item(response)
                            if check.Info["Ingredient"] == True:
                                ingredients.append(response)
                                #Ingredient removed from inventory
                                print(Scene.print_message(43, False, "Menu", {"{Item}": response}))
                                #You add {Ingredient} to the cauldron
                                print(Scene.print_message(67, False, "Menu", {"{Ingredient}": response}))
                                self.Inventory[response] -= 1
                                loop = False
                            else:
                                #Not an ingredient
                                print(Scene.print_message(66, False, "Menu", {}))
                        else:
                            #None in inventory
                            print(Scene.print_message(2, False, "Menu", {}))
                    elif response in Controller.exit or Controller.bools["Exit"] == True:
                        while len(ingredients) < 3:
                            ingredients.append("Exit")
                            loop = False
                    elif response in Controller.Recipes:
                        pass
                        #Lists recipes
                    else:
                        #None in inventory
                        print(Scene.print_message(2, False, "Menu", {}))
            #Check ingredients in cauldron
            check_recipe = []
            if "Exit" not in ingredients:
                column = 1
                row = 1
                while sorted(check_recipe) != sorted(ingredients):
                    if Sheet.cell(column, row).value:
                        check_recipe.append(Sheet.cell(row, column).value)
                        check_recipe.append(Sheet.cell(row, column +1).value)
                        check_recipe.append(Sheet.cell(row, column +2).value)
                        if sorted(check_recipe) == sorted(ingredients):
                            #You stir the concoction
                            print(Scene.print_message(69, False, "Menu", {}))
                            self.add_item_to_inventory(Sheet.cell(row, 0).value, 1)
                            #{Name} acquired {Potion}
                            print(Scene.print_message(26, False, "Menu", {"{Name}": self.Name["Value"], "{Amount}": 1, "{Item}": Sheet.cell(column, 0).value}))
                            #Cauldron magically empties
                            print(Scene.print_message(68, False, "Menu", {}))
                        else:
                            row += 1
                            check_recipe = []
                    else:
                        #You stir the concoction
                        print(Scene.print_message(69, False, "Menu", {}))
                        #The Cauldron bubbles
                        print(Scene.print_message(70, False, "Menu", {}))
                        self.add_item_to_inventory("Unstable Potion", 1)
                        #{Name} acquired {Potion}
                        print(Scene.print_message(26, False, "Menu", {"{Name}": self.Name["Value"], "{Amount}": 1, "{Item}": "Unstable Potion"}))
                        #Cauldron magically empties
                        print(Scene.print_message(68, False, "Menu", {}))
                        break
            else:
                #Cauldron magically empties
                print(Scene.print_message(68, False, "Menu", {}))
#------------------------------------------------------------------------------------------------------------------------------------------
#                                                                  ENEMY CLASS
#------------------------------------------------------------------------------------------------------------------------------------------
class Enemy(Actor):
    def __init__(self, level, name, type, known_spells, Inventory): 
        #self, int, "Name", "Type", ["Fire", "Ice", etc.], [Inventory]
        super().__init__(level, name)
        self.player = False
        self.enemy = True
        self.HP_Caster = False
        self.XP["Value"] = 100 * self.Level["Value"]
        for spell in range(len(known_spells)):
            for stat in range(len(self.Stats)):
                if self.Stats[stat]["Name"] == known_spells[spell]:
                    self.Stats[stat]["Value"] = (self.Level["Value"] - 1) + self.Stats[stat]["Init"]
                    if "Duration" in self.Stats[stat]:
                        self.Stats[stat]["Max"] = 5
        self.set_type(type)
        if len(Inventory) > 0:
            self.fill_inventory(Inventory)

    def make_boss(self):
        source = xlrd.open_workbook('C:\\Users\\Daniel\\source\\repos\\Spell Caster\\Spell_Caster_Strings.xlsx')
        Sheet = source.sheet_by_index(4) #Bosses Page
        column = 0
        while Sheet.cell(column, 0).value != self.Name["Value"]:
            column += 1
            if Sheet.cell(column, 0).value == self.Name["Value"]:
                #Set Level
                self.Level["Value"] = int(Sheet.cell(column, 1).value)
                self.XP["Value"] = 100 * self.Level["Value"]
                self.HP["Max"] = 100 * self.Level["Value"]
                self.HP["Value"] = self.HP["Max"]
                self.MP["Max"] = 100 * self.Level["Value"]
                self.MP["Value"] = self.MP["Max"]
                self.Strength["Value"] = 9 + self.Level["Value"]
                self.Def["Value"] = 4 + self.Level["Value"]
                self.Magic["Value"] = 9 + self.Level["Value"]
                self.MDef["Value"] = 4 + self.Level["Value"]
                #Set Type
                if Sheet.cell(column, 2).value:
                    self.set_type(Sheet.cell(column, 2).value)
                #Adjust Stats
                if Sheet.cell(column, 3).value:
                    stats = Sheet.cell(column, 3).value
                    if ',' in stats:
                        stats_to_adjust = Sheet.cell(column, 3).value.split(', ')
                        new_stat_values = Sheet.cell(column, 4).value.split(', ')
                        for adjustment in range(len(stats_to_adjust)):
                            for stat in range(len(self.Stats)):
                                if stats_to_adjust[adjustment] == self.Stats[stat]["Name"]:
                                    self.Stats[stat]["Value"] = int(new_stat_values[adjustment])
                    else:
                        for stat in range(len(self.Stats)):
                            if self.Stats[stat]["Name"] == stats:
                                self.Stats[stat]["Value"] = int(Sheet.cell(column, 4).value)
                #Set Inventory
                if Sheet.cell(column, 5).value:
                    item = Sheet.cell(column, 5).value
                    if ',' in item:
                       items = item.split(', ')
                       amounts = Sheet.cell(column, 6).value.split(', ')
                       for thing in range(len(items)):
                           self.Inventory[items[thing]] = int(amounts[thing])
                    else:
                        self.Inventory[item] = int(Sheet.cell(column, 6).value)
                #Set HP Caster
                if Sheet.cell(column, 7).value == 1:
                    self.HP_Caster = True

    def add_variance(self, type): #self, "type"
        rando = random.randint(1, 3)
        if type == "Fire":
            if rando == 1:
                self.Name["Value"] = "Goblin"
                self.Strength["Value"] += 1
                self.MDef["Value"] -= 2
                self.Inventory["Goblin Toe"] = 1
            elif rando == 2:
                self.Name["Value"] = "Will-O'-Wisp"
                self.Strength["Value"] -= 5
                self.Magic["Value"] += 2
                self.Def["Value"] -= 2
                self.Inventory["Ashes"] = 1
            else:
                self.Name["Value"] = "Pyromancer"
                self.Strength["Value"] -= 5
                self.Def["Value"] -= 3
                self.Magic["Value"] += 2
                self.MDef["Value"] += 2
                self.Inventory["Charred Finger"] = 1
        elif type == "Ice":
            if rando == 1:
                self.Name["Value"] = "Arctic Wolf"
                self.Strength["Value"] += 2
                self.Magic["Value"] -= 3
                self.MDef["Value"] -= 3
                self.Def["Value"] -= 2
                self.Inventory["Wolf Tooth"] = 1
            elif rando == 2:
                self.Name["Value"] = "Ice Monster"
                self.Strength["Value"] += 2
                self.Def["Value"] += 2
                self.Magic["Value"] -= 2
                self.MDef["Value"] -= 2
                self.Inventory["Never-Melt Ice"] = 1
            else:
                self.Name["Value"] = "Cryomancer"
                self.Strength["Value"] -= 5
                self.Def["Value"] -= 3
                self.Magic["Value"] += 2
                self.MDef["Value"] += 2
                self.Inventory["Frost-Bitten Finger"] = 1
        elif type == "Lightning":
            if rando == 1:
                self.Name["Value"] = "Electric Eel"
                self.Strength["Value"] -= 3
                self.Def["Value"] -= 2
                self.Inventory["Electric Scale"] = 1
            elif rando == 2:
                self.Name["Value"] = "Killer Robot"
                self.Strength["Value"] += 2
                self.Def["Value"] += 2
                self.MDef["Value"] -= 4
                self.Inventory["Energy Core"] = 1
            else:
                self.Name["Value"] = "Electromancer"
                self.Strength["Value"] -= 5
                self.Def["Value"] -= 3
                self.Magic["Value"] += 2
                self.MDef["Value"] += 2
                self.Inventory["Static Finger"] = 1
        elif type == "Water":
            if rando == 1:
                self.Name["Value"] = "Shark"
                self.Strength["Value"] += 3
                self.Def["Value"] += 2
                self.Magic["Value"] -= 2
                self.MDef["Value"] -= 2
                self.Inventory["Shark Tooth"] = 1
            elif rando == 2:
                self.Name["Value"] = "Killer Whale"
                self.Def["Value"] += 3
                self.MDef["Value"] += 3
                self.Inventory["Whale Eye"] = 1
            else:
                self.Name["Value"] = "Hydromancer"
                self.Strength["Value"] -= 5
                self.Def["Value"] -= 3
                self.Magic["Value"] += 2
                self.MDef["Value"] += 2
                self.Inventory["Pruney Finger"] = 1
        elif type == "Wind":
            if rando == 1:
                self.Name["Value"] = "Giant Bird"
                self.Strength["Value"] -= 3
                self.Def["Value"] -= 3
                self.Magic["Value"] += 3
                self.Inventory["Giant Feather"] = 1
            elif rando == 2:
                self.Name["Value"] = "Tree Monster"
                self.Def["Value"] += 2
                self.Magic["Value"] += 2
                self.Inventory["Magic Leaf"] = 1
            else:
                self.Name["Value"] = "Aeromancer"
                self.Strength["Value"] -= 5
                self.Def["Value"] -= 3
                self.Magic["Value"] += 2
                self.MDef["Value"] += 2
                self.Inventory["Hollow Finger"] = 1
        elif type == "Sand":
            if rando == 1:
                self.Name["Value"] = "Giant Scorpion"
                self.Strength["Value"] += 3
                self.Def["Value"] += 3
                self.Inventory["Scorpion Stinger"] = 1
            elif rando == 2:
                self.Name["Value"] = "Rock Monster"
                self.Strength["Value"] += 5
                self.Def["Value"] += 5
                self.Magic["Value"] -= 3
                self.MDef["Value"] -= 3
                self.Inventory["Unbreakable Rock"]
            else:
                self.Name["Value"] = "Terramancer"
                self.Strength["Value"] -= 5
                self.Def["Value"] -= 3
                self.Magic["Value"] += 2
                self.MDef["Value"] += 2
                self.Inventory["Dirty Finger"] = 1

    def set_type(self, Type): #self, "Type"
        #Enemy Types
        FireType = {"Name": self.Fire["Name"], "Weaknesses": [self.Ice["Name"], self.Water["Name"], self.Wind["Name"]], "Resistances": [self.Lightning["Name"]], "Heals": [self.Fire["Name"]]}
        IceType = {"Name": self.Ice["Name"], "Weaknesses": [self.Fire["Name"], self.Lightning["Name"]], "Resistances": [self.Water["Name"]], "Heals": [self.Ice["Name"]]}
        LightningType = {"Name": self.Lightning["Name"], "Weaknesses": [self.Water["Name"]], "Resistances": [self.Wind["Name"], self.Fire["Name"]], "Heals": [self.Lightning["Name"]]}
        WaterType = {"Name": self.Water["Name"], "Weaknesses": [self.Lightning["Name"]], "Resistances": [self.Ice["Name"], self.Fire["Name"]], "Heals": [self.Water["Name"]]}
        WindType = {"Name": self.Wind["Name"], "Weaknesses": [self.Lightning["Name"]], "Resistances": [self.Fire["Name"]], "Heals": [self.Wind["Name"]]}
        SandType = {"Name": self.Sand["Name"], "Weaknesses": [self.Water["Name"], self.Ice["Name"], self.Wind["Name"]], "Resistances": [self.Fire["Name"], self.Lightning["Name"]], "Heals": []}

        #Magic Resistant
        MResistant = {"Name": "MResistant", "Weaknesses": [], "Resistances": [self.Fire["Name"], self.Ice["Name"], self.Lightning["Name"], self.Water["Name"], self.Wind["Name"]], "Heals": []}

        #Magic Eater
        MSponge = {"Name": "Sponge", "Weaknesses": [], "Resistances": [], "Heals": [self.Fire["Name"], self.Ice["Name"], self.Lightning["Name"], self.Water["Name"], self.Wind["Name"]]}

        #Weak to Magic
        Weakling = {"Name": "Weakling", "Weaknesses": [self.Fire["Name"], self.Ice["Name"], self.Lightning["Name"], self.Water["Name"], self.Wind["Name"]], "Resistances": [], "Heals": []}
        
        types = [FireType, IceType, LightningType, WaterType, WindType, SandType, MResistant, MSponge, Weakling]
        for type in range(len(types)):
            if types[type]["Name"] == Type:
                self.Weaknesses = types[type]["Weaknesses"]
                self.Resistances = types[type]["Resistances"]
                self.Heals = types[type]["Heals"]

    def fill_inventory(self, Inventory): #self, [{Inventory}]
        #Inventory_Example = [{"Name": "Potion", "Value":2, "Chance": 80}]
        for a in range(len(Inventory)):
            chance = random.randint(1, 100)
            if chance <= Inventory[a]["Chance"]:
                self.add_item_to_inventory(Inventory[a]["Name"], Inventory[a]["Value"])

    def choose_attack(self):
        options = ["Attack"]
        loop = True
        while loop == True:
            if len(self.get_known_spells()) > 0:
                options += self.get_known_spells()
            if len(options) > 1:
                choices = random.randint(0, len(options) -1)
            else:
                choices = 0
            for a in range(len(self.Stats)):
                if self.Stats[a]["Name"] == options[choices]:
                    if "Duration" in self.Stats[a]:
                        if self.Stats[a]["Active"] == False:
                            loop = False
                    else:
                        loop = False
        return options[choices]

    def AI_attack(self, type, Enemy, Game_State, Scene): #self, "type", Class, Class, Class
        spells = self.get_known_spells()
        Type = {}
        for stat in range(len(self.Stats)):
            if self.Stats[stat]["Name"] == type:
                Type = self.Stats[stat]
        if type in spells:
            cost = self.calculate_MP(Type) #Calculate cost
            if self.MP["Value"] >= cost: #Has enough MP
                self.MP["Value"] -= cost
                self.cast_Spell(type, Enemy, Game_State, Scene)
            elif self.MP["Value"] + self.HP["Value"] > cost and self.HP_Caster == True: #Must use MP and/or HP
                cost -= self.MP["Value"]
                self.MP["Value"] = 0
                self.HP["Value"] -= cost
                cost = 0
                self.cast_Spell(type, Enemy, Game_State, Scene)
            else: #Cannot cast magic
                type = "Attack"
        if type not in spells:
            self.attack(Enemy, Game_State, Scene)

