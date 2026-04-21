import arcade
import random

from assets.managers.eventBusScript import EventBus
from assets.managers import MathGame

class CatFollowAttack(arcade.Sprite):
    def __init__(self,Bus: EventBus,pos_x=0, pos_y=0):
        super().__init__()
        self.center_x = pos_x
        self.center_y = pos_y
        self.texture = arcade.load_texture("assets/Sprites/CattoSans/Attacks/followCat.png")

        self.speed = 125
        self.speedBust = 400
        self.speedAngle = 10
        self.angle = 0
        self.Bus = Bus

        self.Bus.GetFunction("chanceBoxBattle",tam_x=400,tam_y=280)
        self.Bus.GetFunction("changeStage")

        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("onDraw", self.onDraw)
        
        self.boxLimity = 100
        self.timeAttack = 20
        self.timeToBox =  (400 - self.boxLimity) / (self.timeAttack * 0.75)

        self.timeBust = 5
        self.InTimeBust = 0
    
    def onUpdate(self, dt):
        
        widthBox = self.Bus.GetVariable("widthBox") - (dt * self.timeToBox)
        heightBox = self.Bus.GetVariable("heightBox") - (dt * self.timeToBox)

        widthBox = MathGame.clamp(widthBox, self.boxLimity, 400)
        heightBox = MathGame.clamp(heightBox, self.boxLimity, 280)

        if self.timeAttack <= 0:
            self.Bus.GetFunction("EndAttack")

        self.timeAttack -= dt

        playerPos = self.Bus.GetVariable("playerPos")
        if playerPos is None:
            return
        if self.InTimeBust <= 0:
            self.speed = 125
            follow = MathGame.get_angle_degrees(self.center_x, self.center_y, *playerPos)
            self.angle = MathGame.lerp_angle(self.angle, follow - 90, self.speedAngle * dt)
            self.center_x += self.speed * dt * MathGame.cos(MathGame.radians(self.angle + 90))
            self.center_y -= self.speed * dt * MathGame.sin(MathGame.radians(self.angle + 90))

            intensity = (1 - (MathGame.clamp(self.timeBust, 0, 3)/3))
            self.center_x += intensity * 3 * random.randint(-1,1)
            self.center_y += intensity * 3 * random.randint(-1,1)
        else:
             self.center_x += self.speedBust * (self.InTimeBust /0.5) * dt * MathGame.cos(MathGame.radians(self.angle + 90))
             self.center_y -= self.speedBust * (self.InTimeBust /0.5) * dt * MathGame.sin(MathGame.radians(self.angle + 90))
            
        self.timeBust -= dt
        self.InTimeBust -= dt

        if self.timeBust <= 0:
            self.InTimeBust = 0.5
            self.timeBust = 6

        self.Bus.GetFunction("chanceBoxBattle",tam_x=widthBox,tam_y=heightBox)

        if self.Bus.GetVariable("playerSprite") is not None:
            playerHit = arcade.check_for_collision(self, self.Bus.GetVariable("playerSprite"))

            if playerHit is True:
                self.Bus.GetFunction("changePlayerLife", -3)
            
            
                
            

    def onDraw(self, layer):
        arcade.draw_sprite(self)
