import sqlite3
import os
from random import randint

intro = '''GAMEDB
    GameDB is an Action Terminal
    Created By Willie McClinton

    The Commands are:
        END - closes GameDB terminal
        save - save changes to database
        intro - displays this intro
        add - adds characters to GameDB
        remove - removes characters from GameDB
        move - moves characters between locations
        find/search - searches for characters based on attributes

        ***WARNING***
        MAY BE UNFINISHED
        change - changes characters attributes
        addl - adds locations to GameDB
        removel - removes locations from GameDB
        battle - starts battle mode in a location

'''

BMintro = '''BATTLE MODE
    GameDB is in Battle Mode

    The Commands are:
        END - ends battle mode
        save - save changes to database
        intro - displays this intro
        add - adds characters to GameDB
        remove - removes characters from GameDB
        find/search - searches for characters based on attributes

        * Special Commands *
        ***WARNING***
        MAY BE UNFINISHED
        change - changes characters attributes
        attack - starts attack sequence
        burry - removes all killed characters
        ********************

'''

BattleText = '''BATTLE MODE
    BATTLE HAS STARTED!!!

'''

NEW_TABLE = 0

MAXLOCATION = 14

gameDB = sqlite3.connect('gameDB.db')
gdb = gameDB.cursor()

def main():
    if(NEW_TABLE):
        create_new_table()

    clear_screen()
    print(intro)
    status = input("GameDB Action? >> ")
    
    while(True):
        if(status == ''):
            pass
        elif(status == 'end' or status == 'END'):
            clear_screen()
            gameDB.commit()
            gameDB.close()
            return
        elif(status == 'intro'):
            clear_screen()
            print(intro)
            input("Done?")
        elif(status == 'save'):
            gameDB.commit()
            input("\nSaved\n")
        elif(status == 'add'):
            add_new_character()
        elif(status == 'remove'):
            remove_character()
        elif(status == 'move'):
            move_character()
        elif(status == 'find' or status == 'search'):
            find_character()
        elif(status == 'change'):
            change_attribute()
        elif(status == 'addl'):
            add_new_location()
        elif(status == 'removel'):
            remove_location()
        elif(status == 'battle'):
            battle_mode()
        else:
            print(status," is not a valid Command")
            input("Returning To Menu..")
        display_table()
        status = input("GameDB Action? >> ")

def change_attribute():
    character = input("\nCharacter to Change Attribute?\n" + ">"*29 + " ")
    query = input("\nAttribute to Change?(i.e. Health=15)\n" + ">"*35 + " ")
    t = "Name" in query
    t1 = "Attack" in query
    t2 = "Defense" in query
    t3 = "Level" in query
    t4 = "MaxHealth" in query

    if(t1 or t2 or t3 or t4):
        print(query, " is not a valid command")
        input("Returning To Menu..")
        return

    if(query != "" and character != ""):
        comamnds = query.split(',')
    else:
        return

    if(t):
        for q in query:  
            if("Name" in q):
                name = (q.split('=')[1],)
                # Checks if name already exists
                if(gdb.execute("SELECT COUNT(*) FROM Characters WHERE Name=?", name).fetchone()[0] != 0):
                    print(name[0]," already exists")
                    return False
    
    print("\nDo you really want to change this Charcater?")
    print("(Name, Kingdom, Clan, Rank, Lvl, A, D, MaxH, H, Location)\n")
    i = 0
    for row in gdb.execute("SELECT * FROM Characters WHERE Name=?",(character,)):
        MaxH=row[7]
        print(row)

    for q in query:  
        if("Health" in q):
            if(int(q.split('=')[1]) > int(MaxH)):
                print(q," is not a valid command")
                input("Returning To Menu..")
                return
    i = i + 1
    if(i == 0):
        print(character, " was not Found")
        input("Returning To Menu..")
    if(input("\ny/n?\n>>>>>>> ") == 'y'):
        for q in query:
            gdb.execute("UPDATE Characters SET " + q + " WHERE Name=?", (character,))
            print(character," has ",q)
        gameDB.commit()
        input("Returning To Menu..")
        return new_health
    else:
        print("No Change To Character")
        input("Returning To Menu..")
        return -1

# Needs Revising Too Long
def randomized_battle(kingdoms,battlers,location):
    while(True):
        clear_screen()
        print(BattleText)
        try:
            print("Whose Attack?\n#OPTIONS#")
            values = {}
            for kingdom in kingdoms:
                values[kingdom] = [0,0]
                print(kingdom)

            attacker = input("\n> ")
            values[attacker]

            print("\nWhose Defense?\n#OPTIONS#")
            for kingdom in kingdoms:
                if kingdom != attacker:
                    print(kingdom)

            defender = input("\n> ")
            values[defender]

            clear_screen()
            for kingdom in kingdoms:
                print("#"*20)
                print()
                print(kingdom)
                num_char = 0
                for character in battlers[kingdom]:
                    if(character[8] != 0):
                        values[kingdom][0] = values[kingdom][0] + character[5]
                        values[kingdom][1] = values[kingdom][1] + character[6]
                        print("\t",character[0]," A: ",character[5]," D: ",character[6]," H: ",character[8])
                        num_char = num_char + 1
                    else:
                        print("\t(Killed) ",character[0]," A: ",character[5]," D: ",character[6]," H: ",character[8])
                if(num_char == 0):
                    clear_screen()
                    print(kingdom," has no more Living Charcters")
                    input("Returning To Menu..")
                    return kingdom
                print()
                print(kingdom," has ",values[kingdom][0]," Total Attack and ",values[kingdom][1]," Total Defense\n")

            print("#"*20)

            finished = 0
            if(attacker != defender):
                print("ATTACKER: ",attacker)
                print('#'*20)
                damage = calc_damage(values[attacker][0],values[defender][1])
                while(finished == 0):
                    input("Next->")

                    if(damage == 0):
                        finished = 1

                    clear_screen()
                    print("(Name, Kingdom, Clan, Rank, Lvl, A, D, MaxH, H, Location)")
                    for character in battlers[defender]:
                        if character[8] != 0:
                            print(character)
                        else:
                            print("(Killed) ",character)
                    buffer = input("\nCharacter To Damage " + str(damage) + "?\n" + ">"*27 + " ")
                    for row in gdb.execute("SELECT * FROM Characters WHERE Name=?",(buffer,)):
                        print("Damage this Character?")
                        print("(Name, Kingdom, Clan, Rank, Lvl, A, D, MaxH, H, Location)\n")
                        print(row)
                        if(input("\ny/n?\n>>>>>>> ") == 'y'):
                            new_health = damage_charcter(row[8],damage,row[0])
                            if(new_health != -1):
                                finished = 1
                                # Update Values
                                i = 0
                                for character in battlers[defender]:
                                    if character[0] == row[0]:
                                        buffer = list(battlers[defender][i])
                                        buffer[8] = new_health
                                        battlers[defender][i] = tuple(buffer)
                                    i = i + 1
                                damage = 0


        except KeyError:
            print("Invalid Attcker or Defender")
            print("Cancel Battle?")
            if(input("\ny/n?\n>>>>>>> ") == 'y'):
                print('Battle Canceled')
                return input("Returning To Menu..")

def calc_damage(A,D):
    d1 = randint(1, 6)
    d2 = randint(1, 6)
    d3 = randint(1, 6)
    damage = (A * max([d1,d2])) - (D * d3)
    print("\nDICE ROLL\n\n","\tAttacker: ",d1," and ",d2,"\n\n\tDefender: ",d3)
    print()
    print("Damage => Attack * HighAttackDie - Defense * DefenseDie")
    print("Damage = ",A," * ",max([d1,d2])," - ",D," * ",d3," = ",damage)
    if(damage < 0):
        damage = 0
    return damage

def damage_charcter(health,damage,character):
    new_health = int(health) - int(damage)
    if(new_health < 0):
        new_health = 0

    print("Do you really want to Damage this Charcater?")
    print("(Name, Kingdom, Clan, Rank, Lvl, A, D, MaxH, H, Location)\n")
    for row in gdb.execute("SELECT * FROM Characters WHERE Name=?",(character,)):
        print(row)
    if(input("\ny/n?\n>>>>>>> ") == 'y'):
        gdb.execute("UPDATE Characters SET Health =? WHERE Name=?", (new_health,) + (character,))
        print(character," was Damaged by ",damage)
        gameDB.commit()
        input("Returning To Menu..")
        return new_health
    else:
        print("No Character Damaged")
        input("Returning To Menu..")
        return -1

def battle_mode():
    num = input("Battle Location? >> ")
    if(num != ""):
        try:
            location = get_location(int(num))
        except ValueError:
            print("Recieved ValueError with Battle Location")
            input("Returning To Menu..")
            return
    else:
        return

    if(location):
        clear_screen()
        print(BMintro)
        print("Battling in ",location)
        status = input("(Battle Mode)GameDB Action? >> ")
        
        while(True):
            if(status == ''):
                pass
            elif(status == 'end' or status == 'END'):
                clear_screen()
                gameDB.commit()
                return
            elif(status == 'intro'):
                clear_screen()
                print(BMintro)
                input("Done?")
            elif(status == 'save'):
                gameDB.commit()
                input("\nSaved\n")
            elif(status == 'add'):
                add_new_character()
            elif(status == 'remove'):
                remove_character()
            elif(status == 'find' or status == 'search'):
                find_character()
            elif(status == 'change'):
                change_attribute()
            elif(status == 'attack'):
                attack_seq(num)
            elif(status == 'burry'):
                remove_killed(num)
            else:
                print(status," is not a valid Command")
                input("Returning To Menu..")
            display_table(num)
            print("Battling in ",location)
            status = input("(Battle Mode)GameDB Action? >> ")

def attack_seq(location):
    kingdoms = []
    for row in gdb.execute("SELECT Kingdom FROM Characters WHERE Location=?",location):
        if row[0] not in kingdoms:
            kingdoms.append(row[0])

    print("What Characters are Battling?")
    print("#Names#")
    counter = 0
    for row in gdb.execute("SELECT Name FROM Characters WHERE Location=?",location):
        counter = counter + 1
        print(row[0])

    if(counter != 0):
        buffer = input("\nCharacters Battling (Name1,Name2,...)?\n" + ">"*20 + " ")
        if(buffer != ""):
            characters = buffer.split(',')
            characters = [(character,) for character in characters]
            print("Are these Charcaters to Battling ?")
            print("(Name, Kingdom, Clan, Rank, Lvl, A, D, MaxH, H, Location)")

            battlers = {}
            for kingdom in kingdoms:
                # Fill in the entries one by one
                battlers[kingdom] = []

            for character in characters:
                for row in gdb.execute("SELECT * FROM Characters WHERE Name=? AND Location=?",character + (location,)):
                    print(row)
                    if row not in battlers[row[1]]:
                        battlers[row[1]].append(row)

            if(input("\ny/n?\n>>>>>>> ") == 'y'):
                if(len(kingdoms) < 2):
                    print("Too Few Kingdoms To Battle")
                    input("Returning To Menu..") 
                    return
                randomized_battle(kingdoms,battlers,location[0])
                gameDB.commit()
            else:
                print("Battle Avoided")
                input("Returning To Menu..")           

def find_character():
    clear_screen()
    buffer = input("What To Search For (i.e. Location=1 AND Level=5 AND Defense=7 AND Name='John Doe')?\n\n#Attributes#\nName\nKingdom\nClan\nRank\nLevel\nAttack\nDefense\nMaxHealth\nHealth\nLocation\n\n> ")
    if(buffer != ""):
        try:
            query = "SELECT * FROM Characters WHERE " + buffer
            for row in gdb.execute(query):
                print(row)
            input()
        except sqlite3.OperationalError:
            print("\nNot a valid Search Command see example")
            input("Returning To Menu..")

def move_character():
    buffer = input("\nLocation To Move From?\n" + ">"*22 + " ")
    try:
        if(buffer != ""):
            location = (int(buffer),)
            if(check_location(location[0])):
                # Display Characters in Location
                print("(Name, Kingdom, Clan, Rank, Lvl, A, D, MaxH, H, Location)")
                counter = 0
                for row in gdb.execute("SELECT * FROM Characters WHERE Location=? ORDER BY Kingdom, Clan, Level",location):
                    counter = counter + 1
                    print(row)

                if(counter != 0):
                    buffer = input("\nList Characters To Move (Name1,Name2,...)?\n" + ">"*25 + " ")
                    if(buffer != ""):
                        characters = buffer.split(',')
                        characters = [(character,) for character in characters]
                        location2 = input("\nLocation To Move To?\n" + ">"*20 + " ")
                        if(check_location(location2)):
                            # Display Characters in Location to Move
                            print("Do you really want to Move these Charcaters to Location ", location2,"?")
                            print("(Name, Kingdom, Clan, Rank, Lvl, A, D, MaxH, H, Location)")
                            for character in characters:
                                for row in gdb.execute("SELECT * FROM Characters WHERE Name=? AND Location=?",character + location):
                                    print(row)

                            if(input("\ny/n?\n>>>>>>> ") == 'y'):
                                for character in characters:
                                    gdb.execute("UPDATE Characters SET Location =? WHERE Name=? AND Location=?",(int(location2),) + character + location)
                                print("Characters were sucessfully Moved")
                                gameDB.commit()
                            else:
                                print("No Characters Moved")
                                input("Returning To Menu..")
                else:
                    print("\nNo Characters In Location ", location[0])
                    input("Returning To Menu..")
    except ValueError:
        print("\nVauleError with Move attempt")
        input("Returning To Menu..")

def create_new_table():
    # Create table
    gdb.execute('''CREATE TABLE Characters
                (Name text, Kingdom text, Clan text, Rank text, Level int, Attack int, Defense int, MaxHealth int, Health int, Location int)''')
    
    gdb.execute('''CREATE TABLE Locations
                (Num int, Name text, Kingdom text, Capital text, Clan text, Connections text)''')

def remove_killed(location):
    print("Do you really want to remove these Charcaters?")
    for row in gdb.execute("SELECT * FROM Characters WHERE Health=? AND Location=?",(0,location)):
        print(row)

    if(input("\ny/n?\n>>>>>>> ") == 'y'):
        gdb.execute("DELETE FROM Characters WHERE Health=? AND Location=?",(0,location))
        print("Characters were sucessfully Removed")
        gameDB.commit()
        input("Returning To Menu..")
    else:
        print("No Characters Removed")
        input("Returning To Menu..")

def remove_character():
    buffer = input("\nList Characters To Remove (Name1,Name2,...)?\n" + ">"*25 + " ")
    if(buffer != ""):
        characters = buffer.split(',')
        characters = [(character,) for character in characters]
        print("Do you really want to remove these Charcaters?")
        for character in characters:
            for row in gdb.execute("SELECT * FROM Characters WHERE Name=?",character):
                print(row)

        if(input("\ny/n?\n>>>>>>> ") == 'y'):
            gdb.executemany("DELETE FROM Characters WHERE Name=?", characters)
            print("Characters were sucessfully Removed")
            gameDB.commit()
            input("Returning To Menu..")
        else:
            print("No Characters Removed")
            input("Returning To Menu..")

def remove_location():
    buffer = input("\nList Locations To Remove (Num1,Num2,...)?\n" + ">"*24 + " ")
    if(buffer != ""):
        locations = buffer.split(',')
        loactions = [(location,) for location in locations]
        print("Do you really want to remove these Locations?")
        for location in locations:
            for row in gdb.execute("SELECT * FROM Locations WHERE Num=?",location):
                print(row)

        if(input("\ny/n?\n>>>>>>> ") == 'y'):
            gdb.executemany("DELETE FROM Locations WHERE Num=?", locations)
            print("Locations were sucessfully Removed")
            gameDB.commit()
            input("Returning To Menu..")
        else:
            print("No Locations Removed")
            input("Returning To Menu..")

def add_new_character():
    buffer = input("\nNew Character (Name,Kingdom,Clan,Rank,Level,Attack,Defense)?\n>>>>>>>>>>>>> ")
    new_character = tuple(buffer.split(','))

    # Checks Character the adds to database
    if(check_character(new_character)):
        buffer = input("Location\n>>>>>>>>> ")
        # Adds Health and Location to Character
        new_character = new_character + (int(new_character[4])*5,) + (int(new_character[4])*5,) + (buffer,) 
        gdb.execute("INSERT INTO Characters VALUES (?,?,?,?,?,?,?,?,?,?)", new_character)
        gameDB.commit()
    else:
        input("Returning To Menu..")

def add_new_location():
    buffer = input("\nNew Location (#,Name,Kingdom,Capital,Clan,Connections)?\n>>>>>>>>>>>> ")
    new_location = tuple(buffer.split(','))
    if(buffer != ""):
        if(len(new_location) != 6):
            print("Location Attributes is not equal to 6")
            input("Returning To Menu..")
            return

        if(new_location[0] > MAXLOCATION or new_location[0] < 1):
            print("Not a valid Location")
            input("Returning To Menu..")
            return

        if(gdb.execute("SELECT COUNT(*) FROM Locations WHERE Num=?", (new_location[0],)).fetchone()[0] != 0):
            print("Location at ",new_location[0]," already exists")
            input("Returning To Menu..")
            return

        if(gdb.execute("SELECT COUNT(*) FROM Locations WHERE Name=?", (new_location[1],)).fetchone()[0] != 0):
            print(new_location[1]," already exists")
            input("Returning To Menu..")
            return

        gdb.execute("INSERT INTO Locations VALUES (?,?,?,?,?,?)", new_location)
        gameDB.commit()
        print(new_location[1]," Added to Locations")
        input("Returning To Menu..")

def check_character(new_character):
    if(len(new_character) != 7):
        print(len(new_character)," is not equal to the 7 properties needed")
        return False

    name = (new_character[0],)
    kingdom = new_character[1]
    clan = new_character[2]
    rank = new_character[3]
    level = int(new_character[4])
    attack = int(new_character[5])
    defense = int(new_character[6])

    skillpoints = [5,6,7,8,10]

    # Checks if name already exists
    if(gdb.execute("SELECT COUNT(*) FROM Characters WHERE Name=?", name).fetchone()[0] != 0):
        print(name[0]," already exists")
        return False

    # Checks if level is valid
    if(level > 5 or level < 1):
        print(level," is not a valid level (1-5)")
        return False
    
    # Check if skill points are valid
    if(attack + defense != skillpoints[level-1]):
        print(attack,"A + ", defense, "D does not equal ", skillpoints[level-1], " SkillPoints")
        return False

    return True

def check_location(location):
    if(location == ""):
        return False

    if(int(location) > MAXLOCATION or int(location) < 1):
        return False

    return True

def get_location(location):
    if(gdb.execute("SELECT COUNT(*) FROM Locations WHERE Num=?", (location,)).fetchone()[0] == 0):
        print("Location ",location," does not exists")
        input("Returning To Menu..")
        return False
    else:
        return gdb.execute("SELECT Name FROM Locations WHERE Num=?", (location,)).fetchone()[0]

def display_table(location=None):
    if(location==None):
        clear_screen()
        print("CHARACTERS\n" + "-"*10)
        print("(Name, Kingdom, Clan, Rank, Lvl, A, D, MaxH, H, Location)")
        for row in gdb.execute("SELECT * FROM Characters ORDER BY Kingdom, Clan, Level"):
            if row[8] != 0:
                print(row)
            else:
                print("(Killed) ",row)
        print()
        print("LOCATIONS\n" + "-"*9)
        print("(#, Name, Kingdom, Capital, Clan, Connections)")
        for row in gdb.execute("SELECT * FROM Locations ORDER BY Num, Kingdom, Clan, Name"):
            print(row)
        print()
    else:
        clear_screen()
        print("CHARACTERS in " + location + "\n" + "-"*(14+len(location)))
        print("(Name, Kingdom, Clan, Rank, Lvl, A, D, MaxH, H, Location)")
        for row in gdb.execute("SELECT * FROM Characters WHERE Location=? ORDER BY Kingdom, Clan, Level",(location,)):
            if row[8] != 0:
                print(row)
            else:
                print("(Killed) ",row)

        print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()