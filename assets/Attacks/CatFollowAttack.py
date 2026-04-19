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
        self.speedAngle = 10
        self.angle = 0
        self.Bus = Bus

        self.Bus.GetFunction("chanceBoxBattle",tam_x=400,tam_y=280)
        self.Bus.GetFunction("changeStage")

        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("onDraw", self.onDraw)
        
        self.boxLimity = 100
        self.timeAttack = 15
        self.timeToBox =  (400 - self.boxLimity) / (self.timeAttack * 0.75)
    
    def onUpdate(self, dt):
        
        widthBox = self.Bus.GetVariable("widthBox") - (dt * self.timeToBox)
        heightBox = self.Bus.GetVariable("heightBox") - (dt * self.timeToBox)

        widthBox = MathGame.clamp(widthBox, self.boxLimity, 400)
        heightBox = MathGame.clamp(heightBox, self.boxLimity, 280)

        if self.timeAttack <= 0:
            self.Bus.GetFunction("EndAttack")

        self.timeAttack -= dt

        playerPos = self.Bus.GetVariable("playerPos")
        if playerPos is not None:
            self.center_x += self.speed * dt * MathGame.cos(MathGame.radians(self.angle + 90))
            self.center_y -= self.speed * dt * MathGame.sin(MathGame.radians(self.angle + 90))
            follow = MathGame.get_angle_degrees(self.center_x, self.center_y, *playerPos)
            self.angle = MathGame.lerp_angle(self.angle, follow - 90, self.speedAngle * dt)

        self.Bus.GetFunction("chanceBoxBattle",tam_x=widthBox,tam_y=heightBox)

        if self.Bus.GetVariable("playerSprite") is not None:
            playerHit = arcade.check_for_collision(self, self.Bus.GetVariable("playerSprite"))

            if playerHit is True:
                self.Bus.GetFunction("changePlayerLife", -3)
            

    def onDraw(self, layer):
        arcade.draw_sprite(self)
