#character infos
name = ""
job = ""
level = 0
xp = 0
levelCap = 500

classes = ("Knight", "Mage", "Archer")

ins0 = input("Would you like to start? y/n: ")

def characterMaking():
    global name, job, classes
    while name == "":
        name = input("What would you like to name your character? : ")
    num = " "
    while num != "1" and num != "2" and num != "3":
        print("Which job would you like?")
        print("1 knight")
        print("2 mage")
        print("3 archer")
        num = input("number : ")
    job = classes[int(num)-1]



def basePage():
    global name, level, xp
    print("_____________________________________")
    print(name)
    print("Job: " + job)
    print("Level:" , level)
    print("XP:", str(xp) + "/" + str(levelCap))
    print("_____________________________________")

if(ins0 == "y" or ins0 == "yes"):
    #intro
    #character making
    characterMaking()
    #game cycle
    basePage()
else:
    print("End")
