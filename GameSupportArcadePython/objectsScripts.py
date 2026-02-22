
from GameSupportArcadePython.eventBusScript import EventBus
from GameSupportArcadePython.keysManage import keys

from assets.playerScript import playerObject
from assets.boxBattleScript import boxBattle
from assets.CattoSansScript import cattoSans

class ObjectsGame():
    def __init__(self,Bus: EventBus):
        self.Bus = Bus
        self.Scenes = {"scene0":[[playerObject,320,140],[boxBattle,320,140,260,200],[cattoSans,320,350]]}

        self.GameObject = {}
        self.ManagersObjects = {"keys": keys(self.Bus)}
    
    def DefineScene(self,nameScene = "scene0"):
        self.GameObject = {}
        self.GameObject = self.Scenes.get(nameScene)

        print(self.GameObject)
        if self.GameObject is not None:
            print("Scene Defined: ",nameScene)
            for obj in self.GameObject:
                print(obj[0])
                obj[0](self.Bus,*obj[1:])


