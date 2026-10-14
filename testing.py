playerName = "Player"
playerJob = "Knight"
playerLevel = 1
playerXp = 0
playerDam = 10
playerMaxHp = 100
playerHp = 100
defendCount = 0

healRate = 0.25 #healingOrb
levelCap = 50
levelWeight = 1.2
turnCount = 0

monName = "Goblin"
monHp = 50
monMaxHp = 50
monDam = 10
monXp = 50

monTypes = ("Aggressive")
states = ("N", "F", "P", "B")

statistics = []

def charStats(maxHp, dam, job):
    global playerMaxHp,playerDam, playerJob
    playerMaxHp = maxHp
    playerDam = dam
    playerJob = job
class Monster:
    global monTypes, texts, turnCount
    def __init__(self, name, level, maxHp, type, dam, xp, state, abnormalcounter):
        self.name = name
        self.level = level
        self.maxHp = maxHp
        self.type = type
        self.dam = dam
        self.xp = xp
        self.state = state
        self.abnormalcounter = abnormalcounter
        self.hp = self.maxHp
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
        if (self.hp >= self.maxHp * 0.3):
            return 1  # attack
        else:
            # 1 and 2
            temp = str(bin(turnCount))
            if (temp[len(temp) - 1] == "1"):
                # odd number
                return 1
            else:
                # even number
                return 2




charStats(100, 10, "Knight")
monster = Monster(monName, 1, monMaxHp, monTypes[0], monDam, monXp, states[0], 0)

def playerAction():
    global defendCount, playerHp, playerMaxHp, monster
    if playerHp > playerMaxHp * 0.5:
        if(monster.state == "N"):
            return 3
        else:
            return 1
    else:
        if(defendCount <= 1):
            defendCount += 1
            return 2
        else:
            defendCount = 0
            if (monster.state == "N"):
                return 3
            else:
                return 1



def fightState():
    global monster, playerHp
    res = f"Mon {monster.hp}HP/{monster.maxHp}HP st: {monster.state}, Player {playerHp}HP/{playerMaxHp}HP "
    end = "----------------------------------------------"
    statistics.append(res)
    statistics.append(end)

def fightResult(combos):
    global playerJob, playerHp, playerMaxHp, healRate, states, statistics, turnCount, monster
    
    if (monster.abnormalcounter != 0):
        abnormalDamage = int(playerDam / 3)
        monster.hp -= abnormalDamage
        monster.abnormalcounter -= 1

    res = "res base"
    match combos:
        case (1, 1):
            # mon attacks , player attacks
            playerHp -= monster.dam
            monster.hp -= playerDam
            res = f"Turn {turnCount} : Mon atk {monster.dam} , Player atk {playerDam}"
        case (1, 2):
            # mon attack , player defends
            if (playerJob == "Knight"):
                # parry
                parryDam = int(playerDam / 2)
                monster.hp -= parryDam
                res = f"Turn {turnCount} : Mon atk 0 , Player par {parryDam}"
            if (playerJob == "Mage"):
                # healing orb
                playerHp -= monster.dam
                heal = playerMaxHp * healRate
                playerHp += heal
                res = f"Turn {turnCount} : Mon atk {monster.dam} , Player heal {heal}"
            if (playerJob == "Archer"):
                # evade
                res = f"Turn {turnCount} : Mon atk 0, Player def"
        case (1, 3):
            playerHp -= monster.dam
            if (playerJob == "Knight"):
                # swing, Bleeding effect
                monster.stateUpdate(states[3], 2)
                monster.hp -= playerDam
                res = f"Turn {turnCount} : Mon atk {monster.dam} , Player swi {playerDam} + eff {states[3]}"
            if (playerJob == "Mage"):
                # fireball OnFire effect
                monster.stateUpdate(states[1], 2)
                monster.hp -= playerDam
                res = f"Turn {turnCount} : Mon atk {monster.dam} , Player fir {playerDam} + eff {states[1]}"
            if (playerJob == "Archer"):
                # poison darts Posioned effect
                monster.stateUpdate(states[2], 2)
                monster.hp -= playerDam
                res = f"Turn {turnCount} : Mon atk {monster.dam} , Player poi {playerDam} + eff {states[2]}"
        case (2, 1):
            # monster defend
                res = f"Turn {turnCount} : Mon def , Player atk 0"
        case (2, 2):
            # monster and player defend
            if (playerJob == "Knight"):
                # parry
                res = f"Turn {turnCount} : Mon def, Player def"
            if (playerJob == "Mage"):
                # healing orb
                heal = playerMaxHp * healRate
                playerHp += heal
                res = f"Turn {turnCount} : Mon def, Player heal {heal}"
            if (playerJob == "Archer"):
                # evade
                res = f"Turn {turnCount} : Mon def, Player def"
        case (2, 3):
            # monster defend, player spec attack
            res = f"Turn {turnCount} : Mon def, Player atk 0, eff none"
        case _:
            res = ("combos are not recognizable!")
    statistics.append(res)
    fightState()


def fightCycle():
    global Monster, monster, playerXp, turnCount, statistics
    #fight cycle
    while monster.hp > 0 and playerHp > 0:
        turnCount += 1
        #playeraction
        pNum = playerAction()
        #print(pNum)
        #monster action
        mNum = monster.fightAction()
        #print(mNum)
        #result

        fightResult((mNum,pNum))
    if (playerHp <= 0):
        print("You died!")
        print("Game Over!")

    if (monster.hp <= 0):
        print("Congratulations! You killed the monster!")
        playerXp += monster.xp

    for x in range(len(statistics)):
        print(statistics[x])



#test starts here
fightCycle()


