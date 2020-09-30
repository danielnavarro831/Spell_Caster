import random
from Spell import Spell
from Item import Item
import xlrd
from Files import Files

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
        self.Lightning = {"Name": "Lightning", "Value": 0, "Casts": 0, "Init": 10}
        self.Water = {"Name": "Water", "Value": 0, "Casts": 0, "Init": 5}
        self.Wind = {"Name": "Wind", "Value": 0, "Casts": 0, "Init": 7}
        self.Cure = {"Name": "Cure", "Value": 0, "Casts": 0, "Init": 10} #Heals caster's HP by ({Value} * Magic) /2
        self.Drain = {"Name": "Drain", "Value": 0, "Casts": 0, "Init": 10} #Heals caster's HP by stealing {Value} * Magic amount from enemy
        self.Curse = {"Name": "Curse", "Value": 0, "Duration": 0, "Max": 0, "Active": False, "Offering": False, "Casts": 0, "Init": 5} #Caster steals {Value}% of enemy's MaxHP for {Max} turns
        self.Sand = {"Name": "Sandstorm", "Value": 0, "Duration": 0, "Max": 0, "Active": False, "Casts": 0, "Init": 5} #Lowers enemy accuracy for {Max} number of turns
        self.Regen = {"Name": "Regen", "Value": 0, "Duration": 0, "Max": 0, "Active": False, "Casts": 0, "Init": 10} #Caster regains {Value}% of caster's MaxHP for {Max} turns
        self.Protect = {"Name": "Protect", "Value" : 0, "Duration": 0, "Max": 0, "Active": False, "Casts": 0, "Init": 10} #Reduces incoming physical attacks by {Value}% for {Max} turns
        self.Shell = {"Name": "Shell", "Value": 0, "Duration": 0, "Max": 0, "Active": False, "Casts": 0, "Init": 10} #Reduces incoming magical attacks by {Value}% for {Max} turns
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

        file = Files()
        self.path = file.doc_path
        file.__delete__()

    def __delete__(self):
        del self

    def Scan(self, Scene): #self, Class
        self.screen = Scene.screen
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
        self.screen = Scene.screen
        if self.spend_MP(spell, game_state, Scene) == True:
            if spell not in self.Self_Target and game_state.battle == True:
                if self.accuracy_check() == True:
                    for stat in range(len(self.Stats)):
                        if self.Stats[stat]["Name"] == spell:
                            if "Duration" in self.Stats[stat]:
                                self.Stats[stat]["Duration"] = self.Stats[stat]["Max"]
                                self.Stats[stat]["Active"] = True
                                #{Name} casts {Spell}!
                                Scene.log.append(Scene.make_line(35, "Menu", {"{Name}": self.Name["Value"], "{Spell}": spell}))
                            else:
                                damage = self.Magic["Value"] * self.Stats[stat]["Value"]
                                #{Name} casts {Spell}!
                                Scene.log.append(Scene.make_line(35, "Menu", {"{Name}": self.Name["Value"], "{Spell}": spell}))
                                self.deal_damage(enemy, self.crit_chance(damage), self.Stats[stat]["Name"], game_state, Scene)
                else:
                    #{Name}'s attack missed!
                    Scene.log.append(Scene.make_line(11, "Menu", {"{Name}": self.Name["Value"]}))
            else:
                Scene.log.append(Scene.make_line(35, "Menu", {"{Name}": self.Name["Value"], "{Spell}": spell}))
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
                                Scene.log.append(Scene.make_line(4, "Menu", {"{Name}": self.Name["Value"], "{Amount}": hp_restored, "{Stat}": self.HP["Name"]}))
                                    
    def calculate_MP(self, spell): #self, {"spell": "dict"}
        spell_cost = int((spell["Value"] * self.Magic["Value"]) / 2)
        if "duration" in spell:
            spell_cost = int((spell["Value"] * spell["Max"]) / 5)
        return spell_cost

    def spend_MP(self, spell, game_state, Scene): #self, "Spell", Class, Class
        self.screen = Scene.screen
        spell_dic = self.Spells[spell]
        cost = self.calculate_MP(spell_dic)
        if cost > self.MP["Value"]: #Not Enough MP
            if cost >= self.MP["Value"] + self.HP["Value"]: #Spell will Kill you
                #You don't have enough MP or HP to cast
                Scene.log.append(Scene.make_line(9, "Menu", {}))
                return False
            elif cost <= self.MP["Value"] + self.HP["Value"] and spell != "Cure":
                #You feel yourself losing energy...
                Scene.log.append(Scene.make_line(10, "Menu", {})) #Spell requires you to spend HP
                cost -= self.MP["Value"]
                self.MP["Value"] = 0
                self.Sacrifice["Value"] += cost
                self.HP["Value"] -= cost
                cost = 0
                if spell_dic["Name"] == self.Curse["Name"]:
                    self.Curse["Offering"] == True
                return True
            elif cost <= self.MP["Value"] + self.HP["Value"] and spell == "Cure":
                Scene.log.append(Scene.make_line(60, "Menu", {"{MP}": self.MP["Name"]}))
                return False
        else:
            self.MP["Value"] -= cost #You have enough MP
            cost = 0
            return True

    def attack(self, enemy, game_state, Scene): #self, Class, Class, Class
        self.screen = Scene.screen
        if self.accuracy_check() == True:
            damage = self.Strength["Value"] * self.Level["Value"]
            damage = self.crit_chance(damage)
            self.deal_damage(enemy, damage, "Physical", game_state, Scene)
        else:
            #{Name}'s attack missed!
            Scene.log.append(Scene.make_line(11, "Menu", {"{Name}": self.Name["Value"]}))
    
    def deal_damage(self, enemy, damage, type, game_state, Scene): #self, Class, int, "type", Class, Class
        self.screen = Scene.screen
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
                Scene.log.append(Scene.make_line(13, "Menu", {}))
            if type in enemy.Resistances:
                damage = int(damage / 2)
                #It's not very effective...
                Scene.log.append(Scene.make_line(15, "Menu", {}))
            if type in enemy.Heals:
                damage -= damage * 2
                #{Name} absorbed the attack!
                Scene.log.append(Scene.make_line(16, "Menu", {"{Name}": enemy.Name["Value"]}))
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
            if enemy.HP["Value"] < 0:
                enemy.HP["Value"] = 0
            #{Name} deals {damage} damage to {target}!
            Scene.log.append(Scene.make_line(12, "Menu", {"{Name}": self.Name["Value"], "{Damage}": str(damage), "{Target}": enemy.Name["Value"]}))
            if enemy.HP["Value"] <= 0 and enemy.player == False:
                game_state.battle = False
            if enemy.HP["Value"] <= 0 and enemy.player == True and game_state.can_lose == False:
                game_state.game_over = True
            if enemy.HP["Value"] <= 0 and enemy.player == True and game_state.can_lose == True:
                game_state.battle = False
        else:
            if damage < 0:
                #{Name} restored {amount} {stat}
                Scene.log.append(Scene.make_line(4, "Menu", {"{Name}": enemy.Name["Value"], "{Amount}": str(abs(damage)), "{Stat}": enemy.HP["Name"]}))
                enemy.HP["Value"] -= damage
                if enemy.HP["Value"] > enemy.HP["Max"]: 
                    enemy.HP["Value"] = enemy.HP["Max"]
            else:
                #{Name} resisted {Name}'s attack!
                Scene.log.append(Scene.make_line(14, "Menu", {"{Name}": [enemy.Name["Value"], self.Name["Value"]]}))
    
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
        self.screen = Scene.screen
        for stat in range(len(self.Stats)):
            if "Duration" in self.Stats[stat] and self.Stats[stat]["Duration"] > 0:
                self.Stats[stat]["Duration"] -= 1
                if self.Stats[stat]["Duration"] == 0:
                    self.Stats[stat]["Active"] = False
                    if self.Stats[stat]["Name"] == self.Curse["Name"]:
                        #{Name}'s {Curse} lifted
                        Scene.log.append(Scene.print_message(17, "Menu", {"{Name}": Enemy.Name["Value"], "{Curse}": self.Curse["Name"]}))
                    else:
                        #{Name}'s {Spell} faded
                        Scene.log.append(Scene.make_line(18, "Menu", {"{Name}": self.Name["Value"], "{Spell}": self.Stats[stat]["Name"]}))

    def get_known_spells(self):
        spells = [self.Fire["Name"], self.Ice["Name"], self.Lightning["Name"], self.Water["Name"], self.Wind["Name"], self.Sand["Name"], 
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
        self.screen = Scene.screen
        #Drop XP
        Player.XP["Value"] += self.XP["Value"]
        Scene.render_stat_bar(Player, "XP", 39)
        #{Name} gained {Amount} {Stat}
        self.screen.addstr(Scene.line, 1, "* ", Scene.green)
        self.screen.addstr(Scene.make_line(25, "Menu", {"{Name}": Player.Name["Value"], "{Amount}": self.XP["Value"], "{Stat}": self.XP["Name"]}))
        Scene.line += 1
        #Drop Items
        for item in self.Inventory.keys():
            if self.Inventory[item] > 0:
                if "Recipe" not in item:
                    Player.add_item_to_inventory(item, self.Inventory[item])
                    #{Name} acquired {Amount} {Item}
                    self.screen.addstr(Scene.line, 1, "* ", Scene.green)
                    self.screen.addstr(Scene.make_line(26, "Menu", {"{Name}": Player.Name["Value"], "{Amount}": self.Inventory[item], "{Item}": item}))
                    Scene.line += 1
                else:
                    recipe = item.split(' Recipe')
                    Player.learn_recipe(recipe[0], Scene)

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
        self.Speakers = {"Grandfather": "Merlin", "Friend": "Morty", "Agatha": "???"} #Used to store customized names (Grandfather, Best Friend, etc.)
        self.Upgrades = {"Name": "Chapter", "Value": 0}
        self.Hidden_Stats = [self.Sacrifice, self.Hits, self.MHits, self.Upgrades]
        self.Recipes = []

    def level_up(self, Scene): #self, Class
        self.screen = Scene.screen
        Scene.clear_screen()
        #{Name} leveled up!
        self.Upgrades["Value"] += 1
        self.screen.addstr(Scene.line, 1, Scene.print_header(Scene.make_line(33, "Menu", {"{Name}": self.Name["Value"]})))
        Scene.line += 3
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
                self.screen.addstr(Scene.line, 1, "* ", Scene.green)
                self.screen.addstr(Scene.make_line(25, "Menu", {"{Name}": self.Name["Value"], "{Amount}": str(increase_amount), "{Stat}": self.Stats[stat]["Name"]}))
                Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
        Scene.screen.addstr(Scene.make_line(34, "Menu", {"{Chapter}": self.Upgrades["Name"]}))
        Scene.help_text(106, {})
        response = Scene.Game_State.Controller.get_response(self, False, Scene)

    def check_XP(self, Scene): #self, Class
        if self.XP["Value"] >= self.XP["Max"]:
            self.Level["Value"] += 1
            self.XP["Max"] = self.Level["Value"] * (self.Level["Value"] * 100)
            self.XP["Value"] = 0
            self.level_up(Scene)

    def study_magic(self, Scene, Controller, Game_State): #self, Class, Class, Class
        self.screen = Scene.screen
        #Get list of learnable spells (new and learned)
        Exit = False
        while Exit != True:
            #Get list of learnable spells (new and learned)
            spell_book = Spell(self)
            spells = [self.Fire["Name"], self.Ice["Name"]]
            all_spells = [self.Fire["Name"], self.Ice["Name"], self.Water["Name"], self.Wind["Name"], self.Sand["Name"], self.Lightning["Name"],
                      self.Cure["Name"], self.Regen["Name"], self.Protect["Name"], self.Shell["Name"], self.Drain["Name"], self.Curse["Name"]]
            cond_list = spell_book.has_condition(self)
            for a in range(len(cond_list)):
                if spell_book.Check_Condition(self, cond_list[a]) == True:
                    spells.append(cond_list[a])
            if self.Upgrades["Value"] > 0:
                loop = True
                message = 0
                while loop == True:
                    self.view_spellbook(Scene, True)
                    Scene.line = 19
                    for x in range(19, 32):
                        Scene.screen.addstr(x, 0, "                                                                                      ")
                    if message != 0:
                        if message == 115:
                            Scene.screen.addstr(Scene.line, 1, Scene.make_line(115, "Story", {}))
                        else:
                            Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                            Scene.screen.addstr(Scene.make_line(message, "Menu", {}))
                    #Choose a spell
                    Scene.help_text(31, {})
                    response = Controller.get_response(self, False, Scene)
                    response = response.title()
                    if Game_State.tutorial == False:
                        if response in spells:
                            for z in range(19, 30):
                                Scene.screen.addstr(z, 0, "                                                                                 ")
                            if self.known_spell(response) == False:
                                spell_book.learn_elem_spell(response, self, Scene)
                                Scene.line += 1
                                loop = False
                            else:
                                spell_book.upgrade_spell(response, self, Scene, Controller)
                                Scene.line += 1
                                loop = False
                            self.Upgrades["Value"] -= 1
                            if self.Upgrades["Value"] < 0:
                                self.Upgrades["Value"] = 0
                            self.view_spellbook(Scene, False)
                            Scene.help_text(106, {})
                            response = Controller.get_response(self, False, Scene)
                        elif response in all_spells and spell_book.Check_Condition(self, response) == False:
                            #Prerequisits not met
                            message = 27
                        elif Controller.bools["Exit"] == True:
                            Exit = True
                            break
                        else:
                            #You can't study that!
                            message = 32
                    else: #Tutorial is on
                        for z in range(19, 30):
                                Scene.screen.addstr(z, 0, "                                                                                 ")
                        if response in spells:
                            if self.known_spell(response) == True:
                                message = 115
                            else:
                                spell_book.learn_elem_spell(response, self, Scene)
                                loop = False
                                self.Upgrades["Value"] -= 1
                                Scene.help_text(106, {})
                                response = Controller.get_response(self, False, Scene)
                        else:
                            #You can't study that!
                            message = 32
            else:
                #You don't understand...
                self.view_spellbook(Scene, True)
                Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                Scene.screen.addstr(Scene.make_line(30, "Menu", {}))
                Scene.help_text(65, {})
                response = Controller.get_response(self, False, Scene)
                if Controller.bools["Exit"] == True:
                    Exit = True
                    break
            spell_book.__delete__()
        Scene.clear_screen()
        Game_State.Story_UI(self, Scene, Controller)
   
    def view_spellbook(self, Scene, Clear):
        spell_book = Spell(self)
        spells = [self.Fire["Name"], self.Ice["Name"], self.Water["Name"], self.Wind["Name"], self.Sand["Name"], self.Lightning["Name"],
                  self.Cure["Name"], self.Regen["Name"], self.Protect["Name"], self.Shell["Name"], self.Drain["Name"], self.Curse["Name"]]
        hidden_spells = [self.Cure["Name"], self.Regen["Name"], self.Protect["Name"], self.Shell["Name"], self.Drain["Name"], self.Curse["Name"]]
        cond_list = spell_book.has_condition(self)
        if Clear == True:
            Scene.clear_screen()
        if Scene.line != 0:
            Scene.line = 0
        Scene.screen.addstr(Scene.line, 1, Scene.print_header("Study Magic"))
        Scene.line += 3
        Scene.screen.addstr(Scene.line, 1, Scene.make_line(104, "Menu", {}))
        Scene.line += 1
        color = ""
        if self.Upgrades["Value"] > 0:
            color = Scene.cyan
        else:
            color = Scene.red
        Scene.screen.addstr(Scene.line, 1, Scene.make_line(109, "Menu", {}))
        Scene.screen.addstr(str(self.Upgrades["Value"]), color)
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 2, "____________________________  ___________________________")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "|                            \/                           |")
        Scene.line += 1
        for a in range(0, 9):
            Scene.screen.addstr(Scene.line, 1, "|                            ||                           |")
            Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "|____________________________||___________________________|")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, " \___________________________/\__________________________/")
        Scene.line += 1
        Scene.screen.addstr(6, 11, "Spellbook", Scene.cyan)
        Scene.line = 19
        c_line = 8
        p1 = 4
        p2 = 34
        dots = 19
        for b in range(len(spells)):
            if spells[b] in cond_list:
                color = ""
                name = ""
                if spell_book.Check_Condition(self, spells[b]) == True:
                    color = Scene.cyan
                else:
                    color = Scene.red
                if b < 6:
                    Scene.screen.addstr(c_line, p1, "Ch." + str(b+1))
                    if spells[b] in hidden_spells and color == Scene.red:
                        name = "???"
                    else:
                        name = spells[b]
                    for c in range(dots - len(name)):
                        Scene.screen.addstr(".")
                    Scene.screen.addstr(name, color)
                else:
                    if spells[b] in hidden_spells and color == Scene.red:
                        name = "???"
                    else:
                        name = spells[b]
                    Scene.screen.addstr(c_line, p2, "Ch." + str(b+1))
                    for c in range(dots - len(name)):
                        Scene.screen.addstr(".")
                    Scene.screen.addstr(name, color)
            else:
                if b < 6:
                    Scene.screen.addstr(c_line, p1, "Ch." + str(b+1))
                    for c in range(dots - len(spells[b])):
                        Scene.screen.addstr(".")
                    Scene.screen.addstr(spells[b], Scene.cyan)
                else:
                    Scene.screen.addstr(c_line, p2, "Ch." + str(b+1))
                    for c in range(dots - len(spells[b])):
                        Scene.screen.addstr(".")
                    Scene.screen.addstr(spells[b], Scene.cyan)
            c_line += 1
            if b == 5:
                c_line = 8
            if b == 8:
                dots -=1
    
    def view_spellbook_cutscene(self, Scene):
        spell_book = Spell(self)
        spells = [self.Fire["Name"], self.Ice["Name"], self.Water["Name"], self.Wind["Name"], self.Sand["Name"], self.Lightning["Name"],
                  self.Cure["Name"], self.Regen["Name"], self.Protect["Name"], self.Shell["Name"], self.Drain["Name"], self.Curse["Name"]]
        hidden_spells = [self.Cure["Name"], self.Regen["Name"], self.Protect["Name"], self.Shell["Name"], self.Drain["Name"], self.Curse["Name"]]
        cond_list = spell_book.has_condition(self)
        Scene.screen.addstr(Scene.line, 2, "____________________________  ___________________________")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "|                            \/                           |")
        Scene.line += 1
        for a in range(0, 9):
            Scene.screen.addstr(Scene.line, 1, "|                            ||                           |")
            Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, "|____________________________||___________________________|")
        Scene.line += 1
        Scene.screen.addstr(Scene.line, 1, " \___________________________/\__________________________/")
        Scene.line += 1
        Scene.screen.addstr(Scene.line -12, 11, "Spellbook", Scene.cyan)
        c_line = Scene.line - 10
        p1 = 4
        p2 = 34
        dots = 19
        for b in range(len(spells)):
            if spells[b] in cond_list:
                color = ""
                name = ""
                if spell_book.Check_Condition(self, spells[b]) == True:
                    color = Scene.cyan
                else:
                    color = Scene.red
                if b < 6:
                    Scene.screen.addstr(c_line, p1, "Ch." + str(b+1))
                    if spells[b] in hidden_spells and color == Scene.red:
                        name = "???"
                    else:
                        name = spells[b]
                    for c in range(dots - len(name)):
                        Scene.screen.addstr(".")
                    Scene.screen.addstr(name, color)
                else:
                    if spells[b] in hidden_spells and color == Scene.red:
                        name = "???"
                    else:
                        name = spells[b]
                    Scene.screen.addstr(c_line, p2, "Ch." + str(b+1))
                    for c in range(dots - len(name)):
                        Scene.screen.addstr(".")
                    Scene.screen.addstr(name, color)
            else:
                if b < 6:
                    Scene.screen.addstr(c_line, p1, "Ch." + str(b+1))
                    for c in range(dots - len(spells[b])):
                        Scene.screen.addstr(".")
                    Scene.screen.addstr(spells[b], Scene.cyan)
                else:
                    Scene.screen.addstr(c_line, p2, "Ch." + str(b+1))
                    for c in range(dots - len(spells[b])):
                        Scene.screen.addstr(".")
                    Scene.screen.addstr(spells[b], Scene.cyan)
            c_line += 1
            if b == 5:
                c_line = 8
            if b == 8:
                dots -=1

    def get_inventory(self, Scene): #self, Class
        self.screen = Scene.screen
        consumables = []
        ingredients = []
        key_items = []
        if len(self.Inventory) > 0:
            items = False
            self.screen.addstr(Scene.print_message(102, False, "Menu", {}))
            for a in self.Inventory.keys():
                if self.Inventory[a] > 0:
                    item = Item(a)
                    if item.Info["Consumable"] == True:
                        consumables.append(a)
                    elif item.Info["Ingredient"] == True:
                        ingredients.append(a)
                    elif item.Info["Key"] == True:
                        key_items.append(a)
                    items = True
                    item.__delete__()
            if items == True:
                self.screen.addstr(Scene.print_message(55, False, "Menu", {}))
            if len(consumables) > 0:
                self.screen.addstr(Scene.print_header("Consuambles"))
                for a in range(len(consumables)):
                    self.screen.addstr(" * " + consumables[a] + "  x" + str(self.Inventory[consumables[a]]))
            if len(ingredients) > 0:
                self.screen.addstr(Scene.print_header("Ingredients"))
                for a in range(len(ingredients)):
                    self.screen.addstr(" * " + ingredients[a] + "  x" + str(self.Inventory[ingredients[a]]))
            if len(key_items) > 0:
                self.screen.addstr(Scene.print_header("Key Items"))
                for a in range(len(key_items)):
                    self.screen.addstr(" * " + key_items[a] + "  x" + str(self.Inventory[key_items[a]]))
            if items == False:
                #Nothing in inventory
                self.screen.addstr(Scene.print_message(45, False, "Menu", {}))
        else:
            #Nothing in inventory
            self.screen.addstr(Scene.print_message(45, False, "Menu", {}))

    def brew_potion(self, Scene, Controller, Game_State): #self, Class, Class, Class
        #Player, Scene, self, Game_State)
        #Cast Water in the Cauldron
        if self.spend_MP(self.Water["Name"], Game_State, Scene) == True:
            Game_State.in_tower = False
            Game_State.story = False
            Game_State.brewing = True
            Scene.clear_screen()
            Scene.potion_brew_screen(self, Game_State)
            source = xlrd.open_workbook(self.path)
            Sheet = source.sheet_by_index(7) #Recipes page
            #Casts water
            Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
            Scene.screen.addstr(Scene.make_line(35, "Menu", {"{Name}": self.Name["Value"], "{Spell}": self.Water["Name"]}))
            Scene.line += 1
            #Cauldron fills with water
            Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
            Scene.screen.addstr(Scene.make_line(61, "Menu", {}))
            ingredients = []
            while "Exit" not in ingredients:
                while len(ingredients) < 3:
                    #Items in Cauldron
                    if len(ingredients) > 0:
                        for a in range(len(ingredients)):
                            Scene.screen.addstr(25 + a, 4, "* ", Scene.green)
                            Scene.screen.addstr(ingredients[a])
                    response = Controller.get_response(self, False, Scene)
                    response = response.title()
                    if response in self.Inventory:
                        if self.Inventory[response] > 0:
                            check = Item(response)
                            if check.Info["Ingredient"] == True:
                                ingredients.append(response)
                                self.Inventory[response] -= 1
                                Scene.potion_brew_screen(self, Game_State)
                                #Ingredient removed from inventory
                                Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                                Scene.screen.addstr(Scene.make_line(43, "Menu", {"{Item}": response}))
                                Scene.line += 1
                                #You add {Ingredient} to the cauldron
                                Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                                Scene.screen.addstr(Scene.make_line(67, "Menu", {"{Ingredient}": response}))
                                Scene.line += 1
                            elif response in self.Recipes:
                                #Lists recipes
                                Scene.Recipe = response
                                Scene.potion_brew_screen(self, Game_State)
                            else:
                                #Not an ingredient
                                Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                                Scene.screen.addstr(Scene.make_line(66, "Menu", {}))
                                Scene.line += 1
                        elif response in self.Recipes:
                            #Lists recipes
                            Scene.Recipe = response
                            Scene.potion_brew_screen(self, Game_State)
                        else:
                            #None in inventory
                            Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                            Scene.screen.addstr(Scene.make_line(2, "Menu", {}))
                    elif response in Controller.exit or Controller.bools["Exit"] == True:
                        while len(ingredients) < 3:
                            ingredients.append("Exit")
                            loop = False
                            Game_State.brewing = False
                            Scene.clear_screen()
                            Game_State.story = True
                            Game_State.in_tower = True
                            Game_State.Story_UI(self, Scene, Controller)
                    elif response in self.Recipes:
                        #Lists recipes
                        Scene.Recipe = response
                        Scene.potion_brew_screen(self, Game_State)
                    else:
                        #None in inventory
                        Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                        Scene.screen.addstr(Scene.make_line(2, "Menu", {}))
                        Scene.line += 1
                #Check ingredients in cauldron
                check_recipe = []
                if "Exit" not in ingredients:
                    column = 1
                    row = 1
                    while sorted(check_recipe) != sorted(ingredients):
                        if Sheet.cell(row, column).value:
                            check_recipe.append(Sheet.cell(row, column).value)
                            check_recipe.append(Sheet.cell(row, column +1).value)
                            check_recipe.append(Sheet.cell(row, column +2).value)
                            if sorted(check_recipe) == sorted(ingredients):
                                #You stir the concoction
                                Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                                Scene.screen.addstr(Scene.make_line(69, "Menu", {}))
                                Scene.line += 1
                                self.add_item_to_inventory(Sheet.cell(row, 0).value, 1)
                                #{Name} acquired {Potion}
                                Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                                Scene.screen.addstr(Scene.make_line(26, "Menu", {"{Name}": self.Name["Value"], "{Amount}": 1, "{Item}": Sheet.cell(row, 0).value}))
                                Scene.line += 1
                                #Cauldron magically empties
                                Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                                Scene.screen.addstr(Scene.make_line(68, "Menu", {}))
                                Scene.line += 1
                                ingredients = []
                                Scene.help_text(106, {})
                                response = Controller.get_response(self, False, Scene)
                                Scene.potion_brew_screen(self, Game_State)
                            else:
                                row += 1
                                check_recipe = []
                        else:
                            #You stir the concoction
                            Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                            Scene.screen.addstr(Scene.make_line(69, "Menu", {}))
                            Scene.line += 1
                            #The Cauldron bubbles
                            Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                            Scene.screen.addstr(Scene.make_line(70, "Menu", {}))
                            Scene.screen.addstr(24, 5, "o8", Scene.green)
                            Scene.screen.addstr(23, 6, "O", Scene.green)
                            Scene.screen.addstr(22, 7, "o", Scene.green)
                            self.add_item_to_inventory("Unstable Potion", 1)
                            Scene.line += 1
                            #{Name} acquired {Potion}
                            Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                            Scene.screen.addstr(Scene.make_line(26, "Menu", {"{Name}": self.Name["Value"], "{Amount}": 1, "{Item}": "Unstable Potion"}))
                            Scene.line += 1
                            #Cauldron magically empties
                            Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                            Scene.screen.addstr(Scene.make_line(68, "Menu", {}))
                            Scene.line += 1
                            ingredients = []
                            response = Controller.get_response(self, False, Scene)
                            Scene.potion_brew_screen(self, Game_State)
                            break
                else:
                    #Cauldron magically empties
                    Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
                    self.screen.addstr(Scene.make_line(68, "Menu", {}))
                    loop = False
                    Game_State.brewing = False
                    Game_State.in_tower = True
                    Game_State.story = True
                    Game_State.Story_UI(self, Scene, Controller)
                
    def learn_recipe(self, Recipe, Scene):
        Recipe = Recipe.title()
        if Recipe not in self.Recipes:
            self.Recipes.append(Recipe)
            Scene.screen.addstr(Scene.line, 1, "* ", Scene.green)
            Scene.screen.addstr(Scene.make_line(80, "Menu", {"{Name}": self.Name["Value"], "{Potion}":Recipe}))
            Scene.line += 1

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
        source = xlrd.open_workbook(self.path)
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
        elif type == "Normal":
            if rando == 1:
                self.Name["Value"] = "Golem"
                self.Strength["Value"] += 16
                self.Def["Value"] += 20
                self.Magic["Value"] -=3
                self.MDef["Value"] -= 3
                self.Inventory["Medicinal Herb"] = 1
            elif rando == 2:
                self.Name["Value"] = "Assassin"
                self.Strength["Value"] += 10
                self.MDef["Value"] += 10
                self.Inventory["Mystical Water"] = 1
            else:
                self.Name["Value"] = "Wizard"
                self.Strength["Value"] -= 5
                self.Def["Value"] -= 3
                self.Magic["Value"] += 2
                self.MDef["Value"] += 2
                self.Fire["Value"] += 3
                self.Ice["Value"] += 3
                self.Water["Value"] += 3
                self.Wind["Value"] += 3
                self.Lightning["Value"] += 3
                self.Inventory["Dragon Blood"] = 1

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
            if options[choices] == "Attack":
                loop = False
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


