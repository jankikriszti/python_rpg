#character infos
from contextlib import nullcontext

playerName = "Hero"
job = ""
playerLevel = 1
playerXp = 0
playerDam = 0
playerMaxHp = 50
playerHp = 50

healRate = 0.25 #healingOrb
levelCap = 50
levelWeight = 1.2
floor = 0

states = ("Normal", "OnFire", "Poisoned", "Bleeding")
jobs = ("Knight", "Mage", "Archer")
#need actions list!!!
texts = {
    "sep" : "_____________________________________",
    "intro" : "An important person was trapped on the highest floor of the tower. You have to save him.",
    "Goblin" : "You see a small monster upon opening the gate."

}
monTypes = ("Aggressive", "Defensive", "Cautious")
class Monster:
    global monTypes, texts
    def __init__(self, name, level, hp, maxH, type, dam, xp, state):
        self.name = name
        self.level = level
        self.hp = hp
        self.maxH = maxH
        self.type = type
        self.dam = dam
        self.xp = xp
        self.state = state
    def takeDamage(self, damage):
        self.hp -= damage
    def healSelf(self, heal):
        self.hp += heal
    def showStats(self):
        print(texts["sep"])
        print(self.name)
        print("HP: " + str(self.hp))
        print("Level:", str(self.level))
        print("")
    def fightAction(self):
        if(self.type == "Aggressive"):
            if(self.hp >= playerMaxHp * 0.3 or self.hp < playerMaxHp * 0.1):
                return 1 #attack
            else:
                return 2 #defense
        else:
            return 0


def levelUp():
    global playerXp, levelCap, levelWeight, playerLevel, playerHp, playerDam, texts
    playerXp -= levelCap
    levelCap = playerLevel * 50 * levelWeight
    playerLevel += 1
    playerHp += 1.5
    #damage ? weapon?
    playerDam *= levelWeight
    print(texts["sep"])
    print("You leveled up!")
    print(texts["sep"])


def characterMaking():
    global playerName, job, jobs, playerDam
    while playerName == "":
        playerName = input("What would you like to name your character? : ")
    num = " "
    while num != "1" and num != "2" and num != "3":
        print("Which job would you like?")
        print("1 knight")
        print("2 mage")
        print("3 archer")
        num = input("number : ")
    job = jobs[int(num) - 1]
    playerDam = 10

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
    global playerName, playerLevel, playerXp, texts
    #character info
    print(texts["sep"])
    print(playerName)
    print("Job: " + job)
    print("Level:", playerLevel)
    print("XP:", str(playerXp) + "/" + str(levelCap))
    print("")
    #text
    showText(title)
    #item choosing options
    print(texts["sep"])


def playerAction():
    print("")
    match job:
        case "Knight":
            # attack, defend, special attack
            print("1 Stab")
            print("2 Parry")
            print("3 Swing")
        case "Mage":
            # attack, heal, special attack
            print("1 Wind slash")
            print("2 Healing orb")  # 10% of health?
            print("3 Fireball")
        case "Archer":
            # attack, evade, special attack
            print("1 Shoot an arrow")
            print("2 Roll away")
            print("3 Poison darts")
        case _:
            print("no job selected!")
    print("")
    num = 0
    while num != "1" and num != "2" and num != "3":
        num = input("Choose an action! 1/2/3 : ")
    print("")
    return int(num)

def monsterInit(num):
    global Monster
    monster = nullcontext
    match num:
        # monster(name, level, hp, maxH, type, Dam, xp, state)
        case 0:
            monster = Monster("Goblin", 1, 50, 50, monTypes[0], 10, 60, states[0])
        case 1:
            monster = Monster("Orc", 2, 100, 100, monTypes[0], 30, 100, states[0])
        case _:
            return
    return monster

def fightStatus(mName, mHp, mMax, mState):
    global playerName, playerHp, playerMaxHp
    print(texts["sep"])
    print(playerName)
    print(str(playerHp), "HP/" + str(playerMaxHp), "HP")
    print("-------")
    print(mName)
    print(str(mHp), "HP/" + str(mMax) ,"HP")
    if(mState != "Normal"):
        print(mState)
    print("------------------")
    print("")


def fightPhase(num):
    global Monster, texts, playerDam, playerHp, playerName, playerMaxHp, healRate, states, floor, playerXp
    #initialize monster
    monster = monsterInit(floor)
    if monster == nullcontext:
        print("monster init not working!")
        return
    monster.showStats()
    showText(monster.playerName)
    #reset counters
    abnormalstateCounter = 0

    #fight cycle
    while monster.hp > 0 or playerHp > 0:
        print("What are you going to do?")
        playerAttack = playerAction()
        monAttack = monster.fightAction()
        combos = (monAttack,playerAttack)
        # result
        if (abnormalstateCounter != 0):
            abnormalDamage = int(playerDam / 3)
            monster.hp -= abnormalDamage
            abnormalstateCounter -= 1
            if(abnormalstateCounter == 0):
                monster.state = states[0]
            # unique text later!!!
            print(monster.name, "got", abnormalDamage, "damage because of abnormal state!")
        match combos:
            case (1,1):
                playerHp -= monster.Dam
                monster.hp -= playerDam
                print("You got", monster.Dam, "damage!")
                if (job == "Knight"):
                    # stab
                    print("You stabbed with your sword! ", monster.name, "got", playerDam, "damage!")
                if (job == "Mage"):
                    # wind slash
                    print("You used Wind Slash! ", monster.name, "got", playerDam, "damage!")
                if (job == "Archer"):
                    # arrow
                    print("You shot an arrow!", monster.name, "got", playerDam, "damage!")
            case (1,2):
                # parry
                parryDam = int(playerDam / 2)
                monster.hp -= parryDam
                print("You parried the attack! ", monster.name, "got", parryDam, "damage!")
                if (job == "Mage"):
                    # healing orb
                    playerHp -= monster.Dam
                    heal = playerMaxHp * healRate
                    playerHp += heal
                    print("You got", monster.Dam, "damage!")
                    print("You healed yourself! You got ", heal, "HP!")
                if (job == "Archer"):
                    # evade
                    print("You evaded the attack!")
            case (1,3):
                playerHp -= monster.Dam
                print("You got", monster.Dam, "damage!")
                if (job == "Knight"):
                    # swing, Bleeding effect
                    monster.state = states[3]
                    abnormalstateCounter = 2
                    monster.hp -= playerDam
                    print("You did a big swing with your sword!", monster.name, "got", playerDam, "damage!")
                    print(monster.name, "is bleeding!")
                if (job == "Mage"):
                    # fireball OnFire effect
                    monster.state = states[1]
                    abnormalstateCounter = 2
                    monster.hp -= playerDam
                    print("You threw a Fire Ball!", monster.name, "got", playerDam, "damage!")
                    print(monster.name, "is on fire!")
                if (job == "Archer"):
                    # poison darts Posioned effect
                    monster.state = states[2]
                    abnormalstateCounter = 2
                    monster.hp -= playerDam
                    print("You threw poisoned darts!", monster.name, "got", playerDam, "damage!")
                    print(monster.name, "is poisoned!")
            case (2,1):
                # monster defend
                print(monster.name, "is defending!")
                print("your attack doesn't work!")
            case (2,2):
                #monster and player defend
                print("You both defended!")
                if (job == "Knight"):
                    # parry
                    print("What are you parrying?")
                if (job == "Mage"):
                    # healing orb
                    playerHp -= monster.Dam
                    heal = playerMaxHp * healRate
                    playerHp += heal
                    print("You healed yourself! You got ", heal, "HP!")
                if (job == "Archer"):
                    # evade
                    print("You evaded the non-existent attack! Good job!")
            case (2,3):
                # monster defend
                print(monster.name, "is defending!")
                print("your attack doesn't work!")
            case _:
                print("combos are not recognizable!")
        fightStatus(monster.name, monster.hp, monster.maxH, monster.state)
        input("Continue? /enter")
    if(playerHp <= 0):
        print("You died!")
        print("Game Over!")
        return
    if(monster.hp <= 0):
        print("Congratulations! You killed the monster!")
        playerXp += monster.xp
        floor += 1




#testing
#characterMaking()
#fightPhase(0)

#game starts here
ins0 = input("Would you like to start? y/n: ")
if(ins0 == "y" or ins0 == "yes"):
    #intro
    #character making
    characterMaking()
    #game cycle
    while floor < 3:
        #level check
        if(playerXp >= levelCap):
            levelUp()
        basePage("intro")
        ans = input("Are you ready? y/n: ")
        if (ans == "y"):
            fightPhase(floor)

    print("End of floors!")
else:
    print("End")
