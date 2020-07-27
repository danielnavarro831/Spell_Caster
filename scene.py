import xlrd
import random

class Scene():
    def __init__(self, Player): #self, Class
        self.Speakers = Player.Speakers
        self.Error = False

    def print_header(self, header_text): #self, "header_text"
        lines = []
        bar1 = "--------------------------"
        name_line = " " + str(header_text)
        if len(bar1) < len(name_line):
            while len(bar1) < len(name_line) + 3:
                bar1 += "-"
        if len(name_line) < len(bar1) -2:
            while len(name_line) < len(bar1) -2:
                name_line += " "
        name_line += "/"
        bar2 = "------------------------"
        if len(bar2) < len(bar1) -2:
            while len(bar2) < len(bar1) -2:
                bar2 += "-"
        lines.append(bar1)
        lines.append(name_line)
        lines.append(bar2)
        response = '\n'.join(lines)
        return response

    def print_message(self, Scene_Num, Print, Page, Vars): #self, int, Bool, "Page", {"{Vars}": "var"}
        #Get Page
        source = xlrd.open_workbook('C:\\Users\\Daniel\\source\\repos\\Spell Caster\\Spell_Caster_Strings.xlsx')
        if Page.title() == "Menu":
            Sheet = source.sheet_by_index(0)
        elif Page.title() == "Story":
            Sheet = source.sheet_by_index(1)
        elif Page.title() == "Room":
            Sheet = source.sheet_by_index(2)
        else:
            print(" Scene Eror: Page Error - Referenced string page not found or wrong page used")
            self.Error = True
        #Check if individual message or scene
        scene = []
        text = ""
        if self.Error == False:
            if isinstance(Scene_Num, list):
                for num in range(len(Scene_Num)):
                    if len(Vars) > 0:
                        line = self.make_line(Scene_Num[num], Sheet, Vars[num])
                    else:
                        line = self.make_line(Scene_Num[num], Sheet, Vars)
                    scene.append(line)
            else:
                line = self.make_line(Scene_Num, Sheet, Vars)
                scene.append(line)
            if Print == True:
                for line in range(len(scene)):
                    print(scene[line])
                    response = input(" ")
            else:
                text = '\n'.join(scene)
                return text  

    def make_line(self, Scene_num, Sheet, Vars): #self, int, "Sheet", {"{Vars}": "Var"}
        lines = []
        if type(Sheet) == str:
            source = xlrd.open_workbook('C:\\Users\\Daniel\\source\\repos\\Spell Caster\\Spell_Caster_Strings.xlsx')
            if Sheet == "Menu":
                Sheet = source.sheet_by_index(0)
            elif Sheet == "Story":
                Sheet = source.sheet_by_index(1)
            elif Sheet == "Room":
                Sheet = source.sheet_by_index(2)
            else:
                print(" Scene Eror: Page Error - Referenced string page not found or wrong page used")
        if Sheet.cell(Scene_num, 1).value:
            if Sheet.cell(Scene_num, 1).value in self.Speakers:
                name_line = self.Speakers[Sheet.cell(Scene_num, 1).value]
            else:
                name_line = "???"
            lines.append(self.print_header(name_line))
        message = " " + str(Sheet.cell(Scene_num, 0).value)
        if len(Vars) > 0:
            for key in Vars.keys(): 
                if isinstance(Vars[key], list):
                    counter = 1
                    for var in range(len(Vars[key])):
                        message = message.replace(key, str(Vars[key][var]), counter)
                        counter += 1
                else:
                    message = message.replace(key, str(Vars[key]))
        lines.append(message)
        line = '\n'.join(lines)
        return line

    def line_randomizer(self, Scene_nums, Page, Vars): #self, [list, of, scenes], "Menu", [{}, {Vars: 1}, {Vars:2}]
        source = xlrd.open_workbook('C:\\Users\\Daniel\\source\\repos\\Spell Caster\\Spell_Caster_Strings.xlsx')
        if Page.title() == "Menu":
            Sheet = source.sheet_by_index(0)
        elif Page.title() == "Story":
            Sheet = source.sheet_by_index(1)
        else:
            print(" Scene Eror: Page Error - Referenced string page not found or wrong page referenced")
            self.Error = True
        if self.Error == False:
            lines = []
            randomizer = random.randint(0, len(Scene_nums) -1)
            if Sheet.cell(Scene_nums[randomizer], 1).value:
                if Sheet.cell(Scene_nums[randomizer], 1).value in self.Speakers:
                    name_line = self.Speakers[Sheet.cell(Scene_nums[randomizer], 1).value]
                else:
                    name_line = " ???"
                lines.append(self.print_header(name_line))
            message = " " + str(Sheet.cell(Scene_nums[randomizer], 0).value)
            if len(Vars) > 0:
                for var in range(len(Vars)):
                    for key in Vars[var].keys(): 
                        if isinstance(Vars[var][key], list):
                            counter = 1
                            for thing in range(len(Vars[var][key])):
                                message = message.replace(key, str(Vars[var][key][thing]), counter)
                                counter += 1
                        else:
                            message = message.replace(key, str(Vars[var][key]))
            lines.append(message)
            line_break = ""
            lines.append(line_break)
            text = '\n'.join(lines)
            return text

    def get_interactable_string(self, Interactable, Command, Player): #self, Class, Class, Class
        var_dic = {"Interactable.Name": Interactable.Name, "Player.Name": Player.Name["Value"], 
                   "Player.Fire": Player.Fire["Name"], "Player.Ice": Player.Ice["Name"], "Player.Lightning": Player.Lightning["Name"],
                   "Player.Water": Player.Water["Name"], "Player.Wind": Player.Wind["Name"]}
        source = xlrd.open_workbook('C:\\Users\\Daniel\\source\\repos\\Spell Caster\\Spell_Caster_Strings.xlsx')
        Sheet = source.sheet_by_index(3)
        line = ""
        loop = True
        row = 0
        column = 0
        name = ""
        while loop == True:
            if type(Interactable.Name) is not list:
                name = Interactable.Name
            else:
                name = Interactable.Name[0]
            if Sheet.cell(row, column).value in name:
                column += 1
                loop = False
                loop2 = True
                while loop2 == True:
                    if Sheet.cell(row, column).value == Command:
                        column += 1
                        line = " " + str(Sheet.cell(row, column).value)
                        column += 1
                        if Sheet.cell(row, column).value:
                            vars_string = Sheet.cell(row, column).value
                            vars = vars_string.split(', ')
                            for var in range(len(vars)):
                                vars[var] = vars[var].strip("'")
                                if vars[var] in var_dic:
                                    vars[var] = var_dic[vars[var]]
                                elif "Key." in vars[var]:
                                    a = vars[var].split('.')
                                    b = a[-1]
                                    for c in range(len(Interactable.Keys)):
                                        if Interactable.Keys[c]["Name"] == b:
                                            vars[var] = Interactable.Keys[c]["Name"]
                            Vars = {"{Var}": vars}
                            for a in range(len(Vars["{Var}"])):
                                line = line.replace("{Var}", str(Vars["{Var}"][a]), 1)
                        loop2 = False
                    else:
                        row += 1
            else:
                row += 1
        return line

    def __delete__(self):
        del self
#---------------------------------------------------------------------------------------------------------------------------------------
#                                                            Cut Scenes
#---------------------------------------------------------------------------------------------------------------------------------------
    def get_names(self, Player, Controller): #self, Class, Class
        #Get Player Name
        Controller.get_speaker_name(Player, "Player", self, [7, 8, 9])
        self.print_message(10, True, "Story", {"{Name}": Player.Name["Value"]})
        self.print_message(11, True, "Story", {})
        #Get Grandfather's Name
        Controller.get_speaker_name(Player, "Grandfather", self, [12, 8, 9])
        self.print_message(13, True, "Story", {})
        #Get Friend's Name
        Controller.get_speaker_name(Player, "Friend", self, [14, 8, 9])

    def Intro_Grandfather(self, Player, Controller): #self, Class, Class
        loop = True
        no = 0
        while loop == True:
            self.print_message(15, True, "Story", {})
            print(self.print_message(16, False, "Story", {}))
            response = Controller.get_response(Player, False)
            if response.title() in Controller.yes:
                self.print_message(23, True, "Story", {})
                loop = False
            else:
                if no == 0:
                    print(self.print_message(17, False, "Story", {}))
                    self.print_message(18, True, "Story", {"{Header}": "Grandfather", "{Name}": Player.Name["Value"]})
                    no += 1
                elif no == 1:
                    self.print_message([*range(19, 23)], True, "Story", {})
                    loop = False
                else:
                    print(self.print_message(9, False, "Story", {}))
        self.print_message(24, True, "Story", {"{Header}": "Grandfather", "{Name}": Player.Name["Value"]})
        self.print_message([*range(25, 27)], True, "Story", {})
        self.print_message(27, True, "Story", {"{Name}": Player.Speakers["Grandfather"]})
        self.print_message(28, True, "Story", {})
        print(self.print_message(43, False, "Story", {}))
        self.print_message(44, True, "Story", {"{Name}": Player.Speakers["Grandfather"]})
        self.print_message(29, True, "Story", {"{Name}": Player.Speakers["Grandfather"]})
        self.print_message(30, True, "Story", {"{Header}": "Grandfather", "{Name}": Player.Name["Value"]})
        print(self.print_message(31, False, "Story", {"{MP}": Player.MP["Name"]}))
        self.print_message(32, True, "Story", {"{MP}": Player.MP["Name"]})
        print(self.print_message(33, False, "Story", {"{MP}": Player.MP["Name"]}))
        self.print_message(34, True, "Story", {"{Stat}": [Player.MP["Name"], Player.HP["Name"]]})
        self.print_message([*range(35, 37)], True, "Story", {})
        self.print_message(37, True, "Story", {"{MP}": Player.MP["Name"]})
        #Choose Spell to learn!
        chosen = ""
        self.print_message(45, True, "Story", {})
        loop = True
        while loop == True:
            print(self.print_message(38, False, "Story", {"{Spell}": [Player.Fire["Name"], Player.Ice["Name"]]}))
            response = Controller.get_response(Player, True)
            response = response.title()
            if response == Player.Fire["Name"]:
                chosen = Player.Fire["Name"]
                Player.Fire["Value"] = Player.Fire["Init"]
                loop = False
            elif response == Player.Ice["Name"]:
                chosen = Player.Ice["Name"]
                Player.Ice["Value"] = Player.Ice["Init"]
                loop = False
            else:
                print(self.print_message(46, False, "Story", {}))
        effects = {Player.Fire["Name"]: "fireball", Player.Ice["Name"]: "clump of rock-hard ice"}
        self.print_message(39, True, "Story", {"{Name}": Player.Speakers["Grandfather"], "{Spell}": chosen})
        self.print_message(1, True, "Story", {"{Spell}": chosen})
        self.print_message(40, True, "Story", {"{Name}": Player.Speakers["Grandfather"], "{Spell Effect}": effects[chosen]})
        spelled = ""
        for char in range(len(chosen)):
            spelled += chosen[char].upper()
            if char < len(chosen) - 1:
                spelled += "-"
        loop = True
        effects = {Player.Fire["Name"]: "small flame", Player.Ice["Name"]: "snowflake"}
        while loop == True:
            print(self.print_message(2, False, "Story", {"{Spelled}": spelled, "{Spell}": chosen}))
            response = Controller.get_response(Player, True)
            if response == chosen.lower():
                print(self.print_message(3, False, "Story", {}))
            elif response == chosen:
                self.print_message(47, True, "Story", {"{Spell Effect}": effects[chosen]})
                self.print_message(4, True, "Story", {})
                loop = False
            elif response == chosen.upper():
                self.print_message(47, True, "Story", {"{Spell Effect}": effects[chosen]})
                self.print_message(5, True, "Story", {})
                loop = False
            else:
                print(self.print_message(46, False, "Story", {}))
        print(self.print_message(41, False, "Story", {"{Name}": Player.Speakers["Grandfather"]}))
        self.print_message(42, True, "Story", {})
        self.print_message(6, True, "Story", {})

    def Intro_Friend(self, Player, Controller): #self, Class, Class
        #"Excellent! Keep this up and you'll be a master wizard in no time!"
        self.print_message(48, True, "Story", {})
        print(self.print_message(61, False, "Story", {"{MP}": Player.MP["Name"]}))
        self.print_message(62, True, "Story", {})
        self.print_message([54, 55, 56], True, "Story", {})
        loop = True
        #knock at the door
        while loop == True:
            self.print_message(15, True, "Story", {})
            print(self.print_message(16, False, "Story", {}))
            response = Controller.get_response(Player, False)
            response = response.title()
            if response in Controller.yes:
                self.print_message(63, True, "Story", {"{Name}": Player.Speakers["Friend"]})
                self.print_message(51, True, "Story", {"{Name}": Player.Name["Value"]})
                print(self.print_message(52, False, "Story", {}))
                self.print_message(53, True, "Story", {"{Name}": Player.Speakers["Friend"]})
                Player.Inventory["Potion"] += 1
                loop = False
            else:
                print(self.print_message(17, False, "Story", {}))
                self.print_message(49, True, "Story", {"{Name}": [Player.Name["Value"], Player.Speakers["Friend"]]})
                print(self.print_message(50, False, "Story", {"{Name}": Player.Name["Value"]}))
        #Grandfather leaves
        print(self.print_message(57, False, "Story", {}))
        self.print_message(58, True, "Story", {"{Name}": Player.Name["Value"]})
        print(self.print_message(59, False, "Story", {}))
        self.print_message(60, True, "Story", {})

    def Intro_Agatha(self, Player, Controller): #self, Class, Class
        print(self.print_message(64, False, "Story", {"{Name}": Player.Speakers["Friend"]}))
        print(self.print_message(65, False, "Story", {}))
        self.print_message(66, True, "Story", {})
        print(self.print_message(67, False, "Story", {}))
        response = Controller.get_response(Player, True)
        response = response.title()
        #Think we should take a look at the spellbook?
        if Controller.bools["Yes"] == True:
            print(self.print_message(69, False, "Story", {}))
        else:
            print(self.print_message(68, False, "Story", {}))
        self.print_message(70, True, "Story", {"{Name}": Player.Speakers["Friend"]})
        print(self.print_message(71, False, "Story", {}))
        self.print_message(72, True, "Story", {})
        #Friend reads the incantation
        self.print_message([73, 74, 75], True, "Story", [{"{Name}": Player.Speakers["Friend"]}, {}, {}])
        #Agatha appears
        self.print_message([76, 77, 78, 79], True, "Story", [{}, {}, {"{Name}": Player.Speakers["Grandfather"]}, {}])
        self.print_message(80, True, "Story", {})
        Player.Speakers["Agatha"] = "Agatha"
        self.print_message(81, True, "Story", {"{Name}": Player.Speakers["Agatha"].upper()})
        self.print_message([82, 83, 84], True, "Story", [{}, {"{Name}": Player.Speakers["Agatha"]}, {}])
        self.print_message(109, True, "Story", {"{Name}": Player.Name["Value"]})

    def defeated_by_Agatha(self, Player): #self, Class
        self.print_message(110, True, "Story", {})
        self.print_message([85, 86, 87], True, "Story", [{"{Name}": [Player.Speakers["Agatha"], Player.Speakers["Friend"]]}, {"{Name}": Player.Speakers["Friend"]}, {"{Name}": Player.Speakers["Friend"]}])
        #Agatha leaves
        self.print_message([88, 89, 90, 91], True, "Story", [{"{Name}": Player.Speakers["Agatha"]}, {"{Name}": Player.Speakers["Agatha"]}, {}, {"{Name}": Player.Speakers["Agatha"]}])
        self.print_message(92, True, "Story", {"{Name}": Player.Speakers["Friend"]})
        self.print_message([93, 94], True, "Story", {})
        self.print_message(95, True, "Story", {"{Name}": Player.Speakers["Friend"]})
        self.print_message([96, 97, 98], True, "Story", [{"{Name}": Player.Name["Value"].upper()}, {}, {}])

    def spellbook_tutorial(self, Player, Controller, Game_State): #self, Class, Class, Class
        print(self.print_message(111, False, "Story", {}))
        print(self.print_message(112, False, "Story", {}))
        loop = True
        Game_State.tutorial = True
        while loop == True:
            print(self.print_message(50, False, "Menu", {}))
            response = Controller.get_response(Player, False)
            response = response.title()
            if response == "Study":
                Player.study_magic(self, Controller, Game_State)
                loop = False
                Game_State.tutorial = False
        self.print_message([51, 52, 53, 54], True, "Menu", [])
        self.print_message([99, 100, 101, 102], True, "Story", [{}, {"{Name}": Player.Speakers["Agatha"]}, {}, {"{Name}": Player.Speakers["Friend"]}])