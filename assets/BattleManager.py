from GameSupportArcadePython.eventBusScript import EventBus
from assets.BallWoolAttack import BallAttack

import random

class ManagerBattle():
    def __init__(self, Bus: EventBus):
        self.Bus = Bus

        self.Bus.SetFunction("onUpdate", self.onUpdate)
        
        self.Bus.SetFunction("EndAttack", self.EndAttack)
        self.Bus.SetFunction("StartAttack", self.StartAttack)

        self.Attacks = [[BallAttack,300,600]]
        self.attack = None

        self.cooldownAttack = 0
        self.timeAttack = 10
        

    def EndAttack(self):
        self.cooldownAttack = self.timeAttack

        if self.attack is not None:
            self.Bus.DelObject(self.attack)
            del self.attack
            self.attack = None

    def StartAttack(self):
        attack = self.Attacks[random.randint(0,len(self.Attacks)-1)]
        self.attack = attack[0](self.Bus, *attack[1:])
        

    def onUpdate(self):
        pass