#character infos
from doctest import debug

name = ""
job = ""
level = 0
xp = 0
levelCap = 500
damage = 0
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
    def __init__(self, name, level, health, type):
        self.name = name
        self.level = level
        self.health = health
        self.type = type
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

def fightPhase(num):
    global Monster, texts
    #initialize monster
    if(num == 0):
        goblin = Monster("Goblin", 1, 20, 0)
        goblin.showStats()
        showText(goblin.name)
    #fight cycle




#testing
fightPhase(floor)

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
