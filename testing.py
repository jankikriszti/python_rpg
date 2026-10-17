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

monTypes = ("Goblin", "Orc")
states = ("N", "F", "P", "B")

statistics = []

def charStats(maxHp, dam, job):
    global playerMaxHp,playerDam, playerJob
    playerMaxHp = maxHp
    playerDam = dam
    playerJob = job
class Monster:
    global texts, turnCount
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
        #print("fightAction start")
        match self.type:
            case "Goblin":
                #print("type Goblin")
                default = [1,1,2] #attack, attack, defend
                if(self.hp > self.maxHp * 0.5):
                    default = [1,3,2,1]
                else:
                    default = [2,1,2]
                return getAction(default, turnCount)
            case _:
                print("mon type not found!")


def getAction(sequence, turn):
    length = len(sequence)
    res = turn / length
    float = res - int(res)
    if(float == 0):
        return sequence[int(length-1)]
    leftover = float / (1 / length)
    return sequence[int(leftover - 1)]



charStats(100, 10, "Knight")
#name, level, maxHp, type, dam, xp, state, abnormalcounter
monster = Monster("Goblin", 1, 100, monTypes[0], 10, 50, states[0], 0)

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
        case (3,1):
            #monster fast attack, double?
            playerHp -= monster.dam *2
            monster.hp -= playerDam
            res = f"Turn {turnCount} : Mon atk twice {monster.dam}* 2 , Player atk {playerDam}"
        case (3,2):
            # mon  fast attack , player defends
            if (playerJob == "Knight"):
                # parry
                parryDam = int(playerDam / 2)
                monster.hp -= parryDam
                res = f"Turn {turnCount} : Mon atk twice 0 , Player par {parryDam}"
            if (playerJob == "Mage"):
                # healing orb
                playerHp -= monster.dam * 2
                heal = playerMaxHp * healRate
                playerHp += heal
                res = f"Turn {turnCount} : Mon atk twice {monster.dam}* 2 , Player heal {heal}"
            if (playerJob == "Archer"):
                # evade
                res = f"Turn {turnCount} : Mon atk twice 0, Player def"
        case (3,3):
            # monster fast attack, player spec attack
            playerHp -= monster.dam *2
            if (playerJob == "Knight"):
                # swing, Bleeding effect
                monster.stateUpdate(states[3], 2)
                monster.hp -= playerDam
                res = f"Turn {turnCount} : Mon atk twice {monster.dam}* 2 , Player swi {playerDam} + eff {states[3]}"
            if (playerJob == "Mage"):
                # fireball OnFire effect
                monster.stateUpdate(states[1], 2)
                monster.hp -= playerDam
                res = f"Turn {turnCount} : Mon atk twice {monster.dam}* 2 , Player fir {playerDam} + eff {states[1]}"
            if (playerJob == "Archer"):
                # poison darts Posioned effect
                monster.stateUpdate(states[2], 2)
                monster.hp -= playerDam
                res = f"Turn {turnCount} : Mon atk twice {monster.dam}* 2 , Player poi {playerDam} + eff {states[2]}"
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



