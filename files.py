from openpyxl import workbook
from openpyxl import load_workbook

class Files:
    def __init__(self):
        #Change this path to your file path
        self.doc_path = 'C:\\Users\\Daniel\\source\\repos\\Spell Caster\\Spell_Caster_Strings.xlsx'
        self.save_path = 'C:\\Users\\Daniel\\source\\repos\\Spell Caster\\Spell_Caster_Save_File.xlsx'

    def __delete__(self):
        del self

    def Continue(self):
        wb = load_workbook(self.save_path)
        sheets = wb.sheetnames
        GameState = wb[sheets[5]]
        if GameState.cell(row = 5, column = 2).value == "TRUE":
            return True
        else:
            return False

    def save(self, Player, Game_State, Scene):
        wb = load_workbook(self.save_path)
        sheets = wb.sheetnames
        Speakers = wb[sheets[0]]
        for row in Speakers['B2:B10']:
          for cell in row:
            cell.value = None
        Stats = wb[sheets[1]]
        for row in Stats['B2:D26']:
          for cell in row:
            cell.value = None
        Inventory = wb[sheets[2]]
        for row in Inventory['A2:B300']:
          for cell in row:
            cell.value = None
        Rooms = wb[sheets[3]]
        for row in Rooms['A2:E20']:
          for cell in row:
            cell.value = None
        Interactables = wb[sheets[4]]
        for row in Interactables['A2:G40']:
          for cell in row:
            cell.value = None
        GameState = wb[sheets[5]]
        for row in GameState['B2:B10']:
          for cell in row:
            cell.value = None
        #Save Speaker Names
        Speakers.cell(row = 2, column = 2).value = Player.Name["Value"]
        Speakers.cell(row = 3, column = 2).value = Player.Speakers["Friend"]
        Speakers.cell(row = 4, column = 2).value = Player.Speakers["Grandfather"]
        Speakers.cell(row = 5, column = 2).value = Player.Speakers["Agatha"]
        #Save Stats
        All_Stats = Player.Stats + Player.Hidden_Stats
        for a in range(len(All_Stats)):
            counter = 2
            loop = True
            if All_Stats[a]["Name"] != "Name":
                while loop == True:
                    if Stats.cell(row = counter, column = 1).value == All_Stats[a]["Name"]:
                        Stats.cell(row = counter, column = 2).value = All_Stats[a]["Value"]
                        if "Casts" in All_Stats[a]:
                            Stats.cell(row = counter, column = 3).value = All_Stats[a]["Casts"]
                        if "Max" in All_Stats[a]:
                            Stats.cell(row = counter, column = 4).value = All_Stats[a]["Max"]
                        loop = False
                    else:
                        counter += 1
            else:
                continue
        #Save Inventory
        counter = 2
        for b in Player.Inventory.keys():
            Inventory.cell(row = counter, column = 1).value = b
            Inventory.cell(row = counter, column = 2).value = Player.Inventory[b]
            counter += 1
        if len(Player.Recipes) > 0:
            for b in range(len(Player.Recipes)):
                text = Player.Recipes[b] + " Recipe"
                Inventory.cell(row = counter, column = 1).value = text
                Inventory.cell(row = counter, column = 2).value = 1
        #Save Rooms
        counter = 2
        counter_2 = 2
        for c in range(len(Game_State.tower)):
            #Name
            Rooms.cell(row = counter, column = 1).value = Game_State.tower[c].Name
            #Solved
            Rooms.cell(row = counter, column = 2).value = Game_State.tower[c].Solved
            #Counter
            Rooms.cell(row = counter, column = 3).value = Game_State.tower[c].Counter
            #Description
            Rooms.cell(row = counter, column = 4).value = Game_State.tower[c].Description
            #Steps
            if Game_State.is_dungeon(Game_State.tower[c]) == True:
                Rooms.cell(row = counter, column = 5).value = Game_State.tower[c].Steps_Taken
        #Save Interactables
            if len(Game_State.tower[c].Interactables) > 0:
                for d in range(len(Game_State.tower[c].Interactables)):
                    #Floor
                    Interactables.cell(row = counter_2, column = 1).value = Game_State.tower[c].Floor
                    #Name
                    Interactables.cell(row = counter_2, column = 2).value = str(Game_State.tower[c].Interactables[d].Name)
                    #Solved
                    Interactables.cell(row = counter_2, column = 3).value = Game_State.tower[c].Interactables[d].Solved
                    #Key Name
                    Interactables.cell(row = counter_2, column = 4).value = str(Game_State.tower[c].Interactables[d].Keys[0]["Name"])
                    #Value
                    Interactables.cell(row = counter_2, column = 5).value = Game_State.tower[c].Interactables[d].Keys[0]["Value"]
                    #Commands
                    Interactables.cell(row = counter_2, column = 6).value = str(Game_State.tower[c].Interactables[d].Keys[0]["Terms"])
                    #Type
                    Interactables.cell(row = counter_2, column = 7).value = Game_State.tower[c].Interactables[d].Keys[0]["Type"]
                    counter_2 += 1
            counter += 1
        #Save Game State
        GameState.cell(row = 2, column = 2).value = Game_State.current_floor
        GameState.cell(row = 3, column = 2).value = Game_State.in_dungeon
        GameState.cell(row = 4, column = 2).value = Game_State.tutorial
        GameState.cell(row = 5, column = 2).value = "TRUE"
        wb.save(self.save_path) 
        print(Scene.print_message(85, False, "Menu", {}))

    def load(self, Player, Game_State, Scene):
        pass