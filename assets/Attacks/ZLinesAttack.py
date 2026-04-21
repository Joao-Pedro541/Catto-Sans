import arcade
import random

from assets.managers.eventBusScript import EventBus
from assets.managers import MathGame

class ZLinesAttack(arcade.SpriteList):
    def __init__(self,Bus: EventBus):
        super().__init__()
        self.Bus = Bus

        self.Bus.GetFunction("chanceBoxBattle",tam_x=260,tam_y=200)
        self.Bus.GetFunction("changeStage","Perseverance")

        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("onDraw", self.onDraw)
        self.lines = [80,140,200]

        self.zDirection = []
        self.Zs = arcade.SpriteList()
        self.ZSpeed = 600
        
        self.timeSpawnZ = 0.75
        self.timeSpawnZCurrent = 0
        print("ZLinesAttack created")

        self.timeAttack = 20
    
    def onUpdate(self, dt):
        self.Bus.SetVariable("perseveranceLines",self.lines)
        self.timeSpawnZCurrent -= dt
        if self.timeSpawnZCurrent <= 0:
            self.timeSpawnZCurrent = self.timeSpawnZ 
            self.zDirection.append(random.choice([-1,1]))
            xspawn = 320 + (((self.Bus.GetVariable("widthWindow") or 0) / 2) * self.zDirection[-1] )
            z = arcade.Sprite("assets\Sprites\CattoSans\Attacks\zAttack.png",center_x=xspawn,center_y=self.lines[random.randint(0,len(self.lines)-1)])
            self.Zs.append(z)

        for i in range(len(self.Zs)):
            self.Zs[i].center_x += self.ZSpeed * dt * -self.zDirection[i]
            if self.zDirection[i] == -1 and self.Zs[i].center_x < 0 or self.zDirection[i] == 1 and self.Zs[i].center_x > (self.Bus.GetVariable("widthWindow") or 0):
                self.Zs.pop(i)
                self.zDirection.pop(i)
                break

        hitZs = arcade.check_for_collision_with_list(self.Bus.GetVariable("playerSprite"), self.Zs)
        for z in hitZs:
            self.Bus.GetFunction("changePlayerLife", -1)

        self.timeAttack -= dt
        if self.timeAttack <= 0:
            self.Bus.GetFunction("EndAttack")

        
    def onDraw(self, layer):
        if layer == 1:
            for line in self.lines:
                arcade.draw_line(0, line, self.Bus.GetVariable("widthWindow") or 0, line, arcade.color.PURPLE, 2)
        self.Zs.draw()