#character infos
from contextlib import nullcontext

name = "Hero"
job = ""
level = 1
xp = 0
levelCap = 50
damage = 0
maxHp = 50
Hp = 50

floor = 0

classes = ("Knight", "Mage", "Archer")

texts = {
    "sep" : "_____________________________________",
    "intro" : "An important person was trapped on the highest floor of the tower. You have to save him.",
    "Goblin" : "You see a small monster upon opening the gate."

}
monTypes = ("Aggressive", "Defensive", "Cautious")
class Monster:
    global monTypes, texts
    def __init__(self, name, level, health, maxH, type, Dam, xp):
        self.name = name
        self.level = level
        self.health = health
        self.maxH = maxH
        self.type = type
        self.Dam = Dam
        self.xp = xp
    def takeDamage(self, damage):
        self.health -= damage
    def healSelf(self, heal):
        self.health += heal
    def showStats(self):
        print(texts["sep"])
        print(self.name)
        print("HP: " + str(self.health))
        print("Level:", str(self.level))
        print("")
    def fightAction(self):
        if(self.type == "Aggressive"):
            if(self.health >= maxHp * 0.3 or self.health < maxHp * 0.1):
                return 1 #attack
            else:
                return 2 #defense
        else:
            return 0

def characterMaking():
    global name, job, classes, damage
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
    damage = 10

def showText(title):
    global texts
    titles = texts.keys()
    found = False
    for t in titles:
        if t == title:
            print(texts[title])
            found = True
    if not found:
        print("title not found")

def basePage(title):
    global name, level, xp, texts
    #character info
    print(texts["sep"])
    print(name)
    print("Job: " + job)
    print("Level:" , level)
    print("XP:", str(xp) + "/" + str(levelCap))
    print("")
    #text
    showText(title)
    #item choosing options
    print(texts["sep"])

def playerAction():
    print("")
    if(job == "Knight"):
        # attack, special attack, defend
        print("1 Stab")
        print("2 Swing")
        print("3 Parry")
    if(job == "Mage"):
        # attack, special attack, heal
        print("1 Wind slash")
        print("2 Fireball")
        print("3 Healing orb")
    if(job == "Archer"):
        # attack, special attack, evade
        print("1 Shoot an arrow")
        print("2 Poison darts")
        print("3 Roll away")
    num = 0
    while num != 1 and num != 2 and num != 3:
        num = int(input("Choose an action! 1/2/3 : "))
    return num


def fightStatus(mName, mHp, mMax, mStatus):
    global name, Hp, maxHp
    print(texts["sep"])
    print(name)
    print(str(Hp), "HP/" + str(maxHp), "HP")
    print("-------")
    print(mName)
    print(str(mHp), "HP/" + str(mMax) ,"HP")
    print("------------------")

def fightPhase(num):
    global Monster, texts, damage, Hp, name
    #initialize monster
    monster = nullcontext

    if(num == 0):
        monster = Monster("Goblin", 1, 50, 50,  monTypes[0], 10, 30) #name, level, health, maxH, type, Dam, xp
        monster.showStats()
        showText(monster.name)

    #fight cycle
    print("What are you going to do?")
    attackNum = playerAction()
    attackMon = monster.fightAction()
    #result
    if(attackMon == attackNum):
        #attacked each other
        Hp -= monster.Dam
        monster.health -= damage
        print(monster.name, "choose to attack.")
        print(name , "and" , monster.name, "have taken damage!")
        print("")
        fightStatus(monster.name, monster.health, monster.maxH, "")


#testing

#game starts here
ins0 = input("Would you like to start? y/n: ")
if(ins0 == "y" or ins0 == "yes"):
    #intro
    #character making
    characterMaking()
    #game cycle
    basePage("intro")
    ans = input("Are you ready? y/n: ")
    if (ans == "y"):
        fightPhase(floor)

else:
    print("End")
