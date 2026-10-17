#character infos
from contextlib import nullcontext

playerName = "Hero"
playerJob = ""
playerLevel = 1
playerXp = 0
playerDam = 0
playerMaxHp = 50
playerHp = 50

healRate = 0.25 #healingOrb
levelCap = 50
levelWeight = 1.2
floor = 0
turnCount = 0

states = ("Normal", "OnFire", "Poisoned", "Bleeding")
jobs = ("Knight", "Mage", "Archer")
#need actions list!!!
texts = {
    "sep" : "_____________________________________",
    "intro" : "An important person was trapped on the highest floor of the tower. You have to save him.",
    "Goblin" : "You see a small monster upon opening the gate."

}
monTypes = ("Goblin", "Orc", "Skeleton")
class Monster:
    global texts, turnCount
    def __init__(self, name, level, maxHp, type, dam, xp, state, abnormalcounter):
        self.name = name
        self.level = level
        self.hp = maxHp
        self.maxHp = maxHp
        self.type = type
        self.dam = dam
        self.xp = xp
        self.state = state
        self.abnormalcounter = abnormalcounter
    def takeDamage(self, damage):
        self.hp -= damage
    def healSelf(self, heal):
        self.hp += heal
    def showStats(self):#the first meeting
        print(texts["sep"])
        print(self.name)
        print("HP: " + str(self.hp))
        print("Level:", str(self.level))
        print("")
    def stateUpdate(self, state,counter):
        self.state = state
        self.abnormalcounter = counter
    def fightAction(self):
        # print("fightAction start")
        match self.type:
            case "Goblin":
                # print("type Goblin")
                default = [1, 1, 2]  # attack, attack, defend
                if (self.hp > self.maxHp * 0.5):
                    default = [1, 3, 2, 1]
                else:
                    default = [2, 1, 2]
                return getAction(default, turnCount)
            case _:
                print("mon type not found!")


def levelUp():
    global playerXp, levelCap, levelWeight, playerLevel, playerHp, playerDam, texts
    playerXp -= levelCap
    levelCap = int(playerLevel * 50 * levelWeight)
    playerLevel += 1
    playerHp += 1.5
    #damage ? weapon?
    playerDam = int(playerDam * levelWeight)
    print(texts["sep"])
    print("You leveled up!")
    print(texts["sep"])


def characterMaking():
    global playerName, playerJob, jobs, playerDam
    while playerName == "":
        playerName = input("What would you like to name your character? : ")
    num = " "
    while num != "1" and num != "2" and num != "3":
        print("Which job would you like?")
        print("1 knight")
        print("2 mage")
        print("3 archer")
        num = input("number : ")
    playerJob = jobs[int(num) - 1]
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
    print("Job: " + playerJob)
    print("Level:", playerLevel)
    print("XP:", str(playerXp) + "/" + str(levelCap))
    print("")
    #text
    showText(title)
    #item choosing options
    print(texts["sep"])

def getAction(sequence, turn):
    length = len(sequence)
    res = turn / length
    float = res - int(res)
    if(float == 0):
        return sequence[int(length-1)]
    leftover = float / (1 / length)
    return sequence[int(leftover - 1)]

def playerAction():
    print("")
    match playerJob:
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
        # monster(name, level, maxH, type, Dam, xp, state, abnormalcounter)
        case 0:
            monster = Monster("Goblin", 1, 50, monTypes[0], 10, 60, states[0], 0)
        case 1:
            monster = Monster("Orc", 2, 100, monTypes[1], 30, 100, states[0], 0)
        case _:
            return
    return monster

def fightResult(combos, monster):
    global playerJob, playerHp, playerMaxHp, healRate, states
    match combos:
        case (1, 1):
            playerHp -= monster.dam
            monster.hp -= playerDam
            print("You got", monster.dam, "damage!")
            if (playerJob == "Knight"):
                # stab
                print("You stabbed with your sword! ", monster.name, "got", playerDam, "damage!")
            if (playerJob == "Mage"):
                # wind slash
                print("You used Wind Slash! ", monster.name, "got", playerDam, "damage!")
            if (playerJob == "Archer"):
                # arrow
                print("You shot an arrow!", monster.name, "got", playerDam, "damage!")
        case (1, 2):
            print(monster.name , "is attacking!")
            if(playerJob == "Knight"):
                # parry
                parryDam = int(playerDam / 2)
                monster.hp -= parryDam
                print("You parried the attack! ", monster.name, "got", parryDam, "damage!")

            if (playerJob == "Mage"):
                # healing orb
                playerHp -= monster.dam
                heal = playerMaxHp * healRate
                playerHp += heal
                print("You got", monster.dam, "damage!")
                print("You healed yourself! You got ", heal, "HP!")
            if (playerJob == "Archer"):
                # evade
                print("You evaded the attack!")
        case (1, 3):
            playerHp -= monster.dam
            print("You got", monster.dam, "damage!")
            if (playerJob == "Knight"):
                # swing, Bleeding effect
                monster.stateUpdate(states[3], 2)
                monster.hp -= playerDam
                print("You did a big swing with your sword!", monster.name, "got", playerDam, "damage!")
                print(monster.name, "is bleeding!")
            if (playerJob == "Mage"):
                # fireball OnFire effect
                monster.stateUpdate(states[1], 2)
                monster.hp -= playerDam
                print("You threw a Fire Ball!", monster.name, "got", playerDam, "damage!")
                print(monster.name, "is on fire!")
            if (playerJob == "Archer"):
                # poison darts Posioned effect
                monster.stateUpdate(states[2], 2)
                monster.hp -= playerDam
                print("You threw poisoned darts!", monster.name, "got", playerDam, "damage!")
                print(monster.name, "is poisoned!")
        case (2, 1):
            # monster defend
            print(monster.name, "is defending!")
            print("Your attack doesn't work!")
        case (2, 2):
            # monster and player defend
            print("You both defended!")
            if (playerJob == "Knight"):
                # parry
                print("What are you parrying?")
            if (playerJob == "Mage"):
                # healing orb
                heal = playerMaxHp * healRate
                playerHp += heal
                print("You healed yourself! You got ", heal, "HP!")
            if (playerJob == "Archer"):
                # evade
                print("You evaded the non-existent attack! Good job!")
        case (2, 3):
            # monster defend
            print(monster.name, "is defending!")
            print("Your attack doesn't work!")
        case (3,1):
            #monster fast attack, double?
            playerHp -= monster.dam *2
            monster.hp -= playerDam
            print(monster.name, "is in frenzy!")
            print("You got", monster.dam * 2, "damage!")
            if (playerJob == "Knight"):
                # stab
                print("You stabbed with your sword! ", monster.name, "got", playerDam, "damage!")
            if (playerJob == "Mage"):
                # wind slash
                print("You used Wind Slash! ", monster.name, "got", playerDam, "damage!")
            if (playerJob == "Archer"):
                # arrow
                print("You shot an arrow!", monster.name, "got", playerDam, "damage!")
        case (3,2):
            # mon  fast attack , player defends
            print(monster.name, "is in frenzy!")
            if (playerJob == "Knight"):
                # parry
                parryDam = int(playerDam / 2)
                monster.hp -= parryDam
                print("You parried the attack! ", monster.name, "got", parryDam, "damage!")
            if (playerJob == "Mage"):
                # healing orb
                playerHp -= monster.dam *2
                heal = playerMaxHp * healRate
                playerHp += heal
                print("You got", monster.dam *2, "damage!")
                print("You healed yourself! You got ", heal, "HP!")
            if (playerJob == "Archer"):
                # evade
                print("You evaded the attack!")
        case (3,3):
            # monster fast attack, player spec attack
            print(monster.name, "is in frenzy!")
            playerHp -= monster.dam *2
            print("You got", monster.dam*2, "damage!")
            if (playerJob == "Knight"):
                # swing, Bleeding effect
                monster.stateUpdate(states[3], 2)
                monster.hp -= playerDam
                print("You did a big swing with your sword!", monster.name, "got", playerDam, "damage!")
                print(monster.name, "is bleeding!")
            if (playerJob == "Mage"):
                # fireball OnFire effect
                monster.stateUpdate(states[1], 2)
                monster.hp -= playerDam
                print("You threw a Fire Ball!", monster.name, "got", playerDam, "damage!")
                print(monster.name, "is on fire!")
            if (playerJob == "Archer"):
                # poison darts Posioned effect
                monster.stateUpdate(states[2], 2)
                monster.hp -= playerDam
                print("You threw poisoned darts!", monster.name, "got", playerDam, "damage!")
                print(monster.name, "is poisoned!")
        case _:
            print("combos are not recognizable!")


def fightStatus(monster):
    global playerName, playerHp, playerMaxHp, turnCount
    print(texts["sep"])
    print("Turn", turnCount)
    print(playerName)
    print(str(playerHp), "HP/" + str(playerMaxHp), "HP")
    print("-------")
    print(monster.name)
    print(str(monster.hp), "HP/" + str(monster.maxHp) ,"HP")
    if(monster.state != "Normal"):
        print(monster.state, f"({monster.abnormalcounter})")
    print("------------------")
    print("")

def monsterAbnormDam(monster):
    global states, playerDam
    if (monster.abnormalcounter != 0):
        abnormalDamage = int(playerDam / 3)
        monster.hp -= abnormalDamage
        monster.abnormalcounter -= 1
        # unique text later!!!
        print(monster.name, "got", abnormalDamage, "damage because of abnormal state!")
        if (monster.abnormalcounter == 0):
            monster.state = states[0]


def fightPhase(num):
    global texts, playerDam, playerHp, playerName, playerMaxHp, healRate, states, floor, playerXp, playerJob, turnCount
    #initialize monster
    monster = monsterInit(floor)
    if monster == nullcontext:
        print("monster init not working!")
        return
    monster.showStats()
    showText(monster.name)
    #reset counters
    monster.abnormalcounter = 0

    #fight cycle
    turnCount = 1
    while monster.hp > 0 and playerHp > 0:
        print("What are you going to do?")
        #player choose attack
        playerAttack = playerAction()
        #monster unique attack from Monster class
        monAttack = monster.fightAction()
        combos = (monAttack,playerAttack)

        # result
        #abnormal status check (counter,monster)
        monsterAbnormDam(monster)

        fightResult(combos, monster)
        if (playerHp <= 0):
            print("You died!")
            print("Game Over!")
            return
        if (monster.hp <= 0):
            print("Congratulations! You killed the monster!")
            playerXp += monster.xp
            floor += 1
            return
        fightStatus(monster)
        turnCount += 1
        input("/enter")




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
