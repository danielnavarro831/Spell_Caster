

class Spell:
    def __init__(self, Player): #self, Class
        self.exp_spells = [Player.Cure["Name"], Player.Regen["Name"], 
                      Player.Drain["Name"], Player.Curse["Name"], 
                      Player.Protect["Name"], Player.Shell["Name"]]

        self.duration_spells = [Player.Regen["Name"], Player.Sand["Name"], Player.Curse["Name"], 
                                Player.Protect["Name"], Player.Shell["Name"]]

    def __delete__(self):
        del self

    def activate_duration_spell(self, Player, Enemy, Scene, Game_State): #self, Class, Class, Class, Class
        for spell in range(len(self.duration_spells)):
            for stat in range(len(Player.Stats)):
                if Player.Stats[stat]["Name"] == self.duration_spells[spell] and Player.Stats[stat]["Active"] == True:
                    if Player.Stats[stat]["Name"] == Player.Regen["Name"]:
                        amount = int(Player.HP["Max"] - (Player.HP["Max"] * (100 - Player.Regen["Value"])/100))
                        Player.HP["Value"] += amount
                        if Player.HP["Value"] > Player.HP["Max"]:
                            Player.HP["Value"] = Player.HP["Max"]
                        #{Name} restored {Amount} {Stat}
                        print(Scene.print_message(4, False, "Menu", {"{Name}": Player.Name["Name"], "{Amount}": amount, "{Stat}": Player.HP["Name"]}))
                    if Player.Stats[stat]["Name"] == Player.Sand["Name"]:
                        Enemy.Accuracy["Value"] = Enemy.Accuracy["Max"] - Player.Sand["Value"]
                        #{Name}'s {Spell} rages on!
                        print(Scene.print_message(21, False, "Menu", {"{Name}": Player.Name["Value"], "{Spell}": Player.Sand["Name"]}))
                    if Player.Stats[stat]["Name"] == Player.Curse["Name"]:
                        MP_amount = 0
                        HP_amount = 0
                        if Enemy.MP["Value"] > 0:
                            MP_amount = int(Enemy.MP["Max"] - (Enemy.MP["Max"] * (100 - Player.Curse["Value"])/100))
                            HP_amount = 0
                            if MP_amount > Enemy.MP["Value"]: #Stealing more MP than available
                                HP_amount = MP_amount - Enemy.MP["Value"]
                                Enemy.MP["Value"] = 0
                                Enemy.HP["Value"] -= HP_amount
                            else: #Enemy has enough MP
                                Enemy.MP["Value"] -= MP_amount
                        else:
                            MP_amount = 0
                            HP_amount = int(Enemy.HP["Max"] - (Enemy.HP["Max"] * (100 - Player.Curse["Value"])/100))
                            Enemy.HP["Value"] -= HP_amount
                            if Enemy.HP["Value"] < 0:
                                Enemy.HP["Value"] = 0
                                if Enemy.player == False:
                                    Game_State.battle = False
                                elif Enemy.player == True and Game_State.can_lose == False:
                                    Game_State.game_over = True
                                elif Enemy.player == True and Game_State.can_lose == True:
                                    Game_State.battle = False
                        #{Name} is afflicted by a {Curse}
                        print(Scene.print_message(22, False, "Menu", {"{Name}": Enemy.Name["Value"], "{Curse}": Player.Curse["Name"]}))
                        if Player.Curse["Offering"] == True:
                            HP_and_MP = False
                            total_drained = HP_amount + MP_amount
                            if Player.MP["Value"] + total_drained > Player.MP["Max"]:
                                total_drained -= Player.MP["Max"] - Player.MP["Value"]
                                MP_amount = Player.MP["Max"] - Player.MP["Value"]
                                HP_amount = total_drained
                                Player.MP["Value"] = Player.MP["Max"]
                                Player.HP["Value"] += total_drained
                                HP_and_MP = True
                            else:
                                Player.MP["Value"] += total_drained
                            if HP_and_MP == True:
                                #{Name} restored {Amount} {Stat} and {Amount} {Stat}
                                print(Scene.print_message(23, False, "Menu", 
                                                     {"{Name}": Player.Name["Value"], "{Amount}": [HP_amount, MP_amount], "{Stat}": [Player.HP["Name"], Player.MP["Name"]]}))
                            else:
                                #{Name} restored {Amount} {Stat}
                                print(Scene.print_message(4, False, "Menu", {"{Name}": Player.Name["Value"], "{Amount}": total_drained, "{Stat}": Player.MP["Name"]}))
                            if Player.HP["Value"] > Player.HP["Max"]:
                                Player.HP["Value"] = Player.HP["Max"]

    def deactivate_duration_spells(self, Player, Enemy): #self, Class, Class
        Player.Regen["Duration"] = 0
        Player.Regen["Active"] = False
        Player.Sand["Duration"] = 0
        Player.Sand["Active"] = False
        Player.Curse["Duration"] = 0
        Player.Curse["Active"] = False
        Player.Curse["Offering"] = False
        Player.Protect["Duration"] = 0
        Player.Protect["Active"] = False
        Player.Shell["Duration"] = 0
        Player.Shell["Active"] = False

        Enemy.Regen["Duration"] = 0
        Enemy.Regen["Active"] = False
        Enemy.Sand["Duration"] = 0
        Enemy.Sand["Active"] = False
        Enemy.Curse["Duration"] = 0
        Enemy.Curse["Active"] = False
        Enemy.Curse["Offering"] = False
        Enemy.Protect["Duration"] = 0
        Enemy.Protect["Active"] = False
        Enemy.Shell["Duration"] = 0
        Enemy.Shell["Active"] = False
#-----------------------------------------------------------------------------------------------------------------------------------
#                                                             Conditions
#-----------------------------------------------------------------------------------------------------------------------------------
    def has_condition(self, Player): #self, Class
        condition_spells = [Player.Cure["Name"], Player.Regen["Name"], Player.Drain["Name"], Player.Curse["Name"], 
                            Player.Protect["Name"], Player.Shell["Name"], Player.Water["Name"], Player.Wind["Name"],
                            Player.Lightning["Name"], Player.Sand["Name"]]
        return condition_spells

    def Check_Condition(self, Player, Spell): #self, Player, "Spell"
        Spell = Spell.title()
        condition = False
        if Spell == Player.Cure["Name"]:
            condition = self.Cure_Condition(Player)
        if Spell == Player.Regen["Name"]:
            condition = self.Regen_Condition(Player)
        if Spell == Player.Drain["Name"]:
            condition = self.Drain_Condition(Player)
        if Spell == Player.Curse["Name"]:
            condition = self.Curse_Condition(Player)
        if Spell == Player.Protect["Name"]:
            condition = self.Protect_Condition(Player)
        if Spell == Player.Shell["Name"]:
            condition = self.Shell_Condition(Player)
        if Spell == Player.Water["Name"]:
            condition = self.Water_Condition(Player)
        if Spell == Player.Wind["Name"]:
            condition = self.Wind_Condition(Player)
        if Spell == Player.Lightning["Name"]:
            condition = self.Lightning_Condition(Player)
        if Spell == Player.Sand["Name"]:
            condition = self.Sand_Condition(Player)
        return condition

    def Cure_Condition(self, Player): #self, Class
        meets_condition = False
        if Player.Sacrifice["Value"] >= 100:
            meets_condition = True
        return meets_condition

    def Regen_Condition(self, Player): #self, Class
        meets_condition = False
        if Player.Cure["Casts"] >= 10:
            meets_condition = True
        return meets_condition

    def Drain_Condition(self, Player): #self, Class
        meets_condition = False
        if Player.Regen["Casts"] >= 5 and Player.Cure["Casts"] >= 20 and Player.Sacrifice["Value"] >= 200:
            meets_condition = True
        return meets_condition

    def Curse_Condition(self, Player): #self, Class
        meets_condition = False
        if Player.Drain["Casts"] >= 10 and Player.Regen["Casts"] >= 10 and Player.Sacrifice["Value"] >= 300:
            meets_condition = True
        return meets_condition

    def Protect_Condition(self, Player): #self, Class
        meets_condition = False
        if Player.Hits["Value"] >= 500:
            meets_condition = True
        return meets_condition

    def Shell_Condition(self, Player): #self, Class
        meets_condition = False 
        if Player.MHits["Value"] >= 500:
            meets_condition = True
        return meets_condition

    def Water_Condition(self, Player): #self, Class
        meets_condition = False
        if Player.known_spell(Player.Fire["Name"]) == True and Player.known_spell(Player.Ice["Name"]) == True:
            meets_condition = True
        return meets_condition

    def Wind_Condition(self, Player): #self, Class
        meets_condition = False
        if Player.known_spell(Player.Water["Name"]) == True:
            meets_condition = True
        return meets_condition

    def Lightning_Condition(self, Player): #self, Class
        meets_condition = False
        if Player.known_spell(Player.Wind["Name"]) == True:
            meets_condition = True
        return meets_condition

    def Sand_Condition(self, Player): #self, Class
        meets_condition = False
        if Player.known_spell(Player.Wind["Name"]) == True:
            meets_condition = True
        return meets_condition
#----------------------------------------------------------------------------------------------------------------------------------------
#                                                             Learn/Upgrade
#----------------------------------------------------------------------------------------------------------------------------------------
    def learn_elem_spell(self, Spell, Player, Scene): #self, "Spell", Class, Class
        Spell = Spell.title()
        conditions = {Player.Water["Name"]: self.Water_Condition(Player), Player.Wind["Name"]: self.Wind_Condition(Player),
        Player.Lightning["Name"]: self.Lightning_Condition(Player), Player.Sand["Name"]: self.Sand_Condition(Player)}
        for stat in range(len(Player.Stats)):
            if Player.Stats[stat]["Name"] == Spell:
                if Spell in conditions:
                    if conditions[Spell] == True:
                        Player.Stats[stat]["Value"] = Player.Stats[stat]["Init"]
                        #{Name} learned {Spell}
                        Scene.print_message(19, True, "Menu", {"{Name}": Player.Name["Value"], "{Spell}": Player.Stats[stat]["Name"]})
                    else:
                        #Prereqs not met
                        Scene.print_message(27, True, "Menu", {})
                else:
                    Player.Stats[stat]["Value"] = Player.Stats[stat]["Init"]
                    #{Name} learned {Spell}
                    print(Scene.print_message(19, False, "Menu", {"{Name}": Player.Name["Value"], "{Spell}": Player.Stats[stat]["Name"]}))

    def upgrade_spell(self, Spell, Player, Scene, Controller): #self, "Spell", Class, Class, Class
        Spell = Spell.title()
        stats = ["Strength", "Duration"]
        for stat in range(len(Player.Stats)):
            if Player.Stats[stat]["Name"] == Spell:
                if "Duration" in Player.Stats[stat]:
                    loop = True
                    while loop == True:
                        #Learn {Stat} {Chapter} or the {Stat} {Chapter}?
                        print(Scene.print_message(28, False, "Menu", {"{Stat}": [stats[0], stats[1]], "{Chapter}": Player.Upgrades["Name"]}))
                        response = Controller.get_response(Player, False)
                        response = response.title()
                        if response == stats[0]: #Strength
                            Player.Stats[stat]["Value"] += 1
                            Scene.print_message(29, True, "Menu", {"{Spell}": Player.Stats[stat]["Name"]})
                            loop = False
                        if response == stats[1]: #Duration
                            Player.Stats[stat]["Max"] += 1
                            Scene.print_message(29, True, "Menu", {"{Spell}": Player.Stats[stat]["Name"]})
                            loop = False
                else:
                    Player.Stats[stat]["Value"] += 1
                    print(Scene.print_message(29, False, "Menu", {"{Spell}": Player.Stats[stat]["Name"]}))

    def learn_exp_spells(self, Player, Scene): #self, Class, Class
        for spell in self.exp_spells:
            if Player.known_spell(spell) == False:
                if spell == Player.Cure["Name"]:
                    if self.Cure_Condition(Player) == True:
                        #{Name} learned {Spell}!
                        Scene.print_message(19, True, "Menu", {"{Name}": Player.Name["Value"], "{Spell}": Player.Cure["Name"]})
                        Player.Cure["Value"] = Player.Cure["Init"]
                elif spell == Player.Regen["Name"]:
                    if self.Regen_Condition(Player) == True:
                        Scene.print_message(19, True, "Menu", {"{Name}": Player.Name["Value"], "{Spell}": Player.Regen["Name"]})
                        Player.Regen["Value"] = Player.Regen["Init"]
                        Player.Regen["Max"] = 3
                elif spell == Player.Drain["Name"]:
                    if self.Drain_Condition(Player) == True:
                        Scene.print_message(19, True, "Menu", {"{Name}": Player.Name["Value"], "{Spell}": Player.Drain["Name"]})
                        Player.Drain["Value"] = Player.Drain["Init"]
                elif spell == Player.Curse["Name"]:
                    if self.Curse_Condition(Player) == True:
                        Scene.print_message(19, True, "Menu", {"{Name}": Player.Name["Value"], "{Spell}": Player.Curse["Name"]})
                        Player.Curse["Value"] = Player.Curse["Init"]
                        Player.Curse["Max"] = 3
                elif spell == Player.Protect["Name"]:
                    if self.Protect_Condition(Player) == True:
                        Scene.print_message(19, True, "Menu", {"{Name}": Player.Name["Value"], "{Spell}": Player.Protect["Name"]})
                        Player.Protect["Value"] = Player.Protect["Init"]
                        Player.Protect["Max"] = 3
                elif spell == Player.Shell["Name"]:
                    if self.Shell_Condition(Player) == True:
                        Scene.print_message(19, True, "Menu", {"{Name}": Player.Name["Value"], "{Spell}": Player.Shell["Name"]})
                        Player.Shell["Value"] = Player.Shell["Init"]
                        Player.Shell["Max"] = 3
                else:
                    #Error: condition not found
                    print(Scene.print_message(20, False, "Menu", {}))
