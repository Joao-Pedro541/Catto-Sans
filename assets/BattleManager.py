from GameSupportArcadePython.eventBusScript import EventBus

from assets.BallWoolAttack import BallAttack

import random

class ManagerBattle():
    def __init__(self, Bus: EventBus):
        self.Bus = Bus

        self.Bus.SetFunction("onUpdate", self.onUpdate)

        self.Attacks = [[10,BallAttack,300,300]]
        self.timeAttack = 5
        self.attack = None

    def chooseAttack(self):
        if self.attack is not None:
            self.Bus.DelObject(self.attack)
            del self.attack

        attack = self.Attacks[random.randint(0,len(self.Attacks)-1)]
        self.timeAttack = attack[0]
        self.attack = attack[1](self.Bus, *attack[2:])

    
    def onUpdate(self):
        if self.timeAttack > 0:
            self.timeAttack -= self.Bus.GetVariable("deltatime") or 0
        else:
            self.chooseAttack()