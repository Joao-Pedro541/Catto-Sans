from GameSupportArcadePython.eventBusScript import EventBus

from assets.BallWoolAttack import BallAttack

import random

class ManagerBattle():
    def __init__(self, Bus: EventBus):
        self.Bus = Bus

        #self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("EndAttack", self.chooseAttack)

        self.Attacks = [[BallAttack,300,150]]
        self.attack = None

        self.chooseAttack()
        

    def EndAttack(self):
        self.chooseAttack()

    def chooseAttack(self):
        if self.attack is not None:
            self.Bus.DelObject(self.attack)
            del self.attack

        attack = self.Attacks[random.randint(0,len(self.Attacks)-1)]
        self.attack = attack[0](self.Bus, *attack[1:])

    
    def onUpdate(self):
        return