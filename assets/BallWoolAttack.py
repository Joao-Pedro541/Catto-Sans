import arcade
import GameSupportArcadePython.MathGame as MathGame
import random

from GameSupportArcadePython.eventBusScript import EventBus

    
class BallAttack(arcade.Sprite):
    def __init__(self, Bus: EventBus, posInitX=0, posInitY=0):
        super().__init__()
        self.center_x = posInitX
        self.center_y = posInitY
        self.texture = arcade.load_texture("assets/Sprites/CattoSans/Attacks/BallWoolAttack.png")

        self.Bus = Bus

        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("onDraw", self.onDraw)

        self.dir = random.randint(0,360)

        self.speedAttack = 800
        self.speedReturn = 1600

        self.points = []

        self.lineColor = arcade.color.GRAY_ASPARAGUS

        self.timeAttack = 10

        self.Bus.GetFunction("chanceBoxBattle",tam_x=400,tam_y=280)

    def limityWindow(self, deadzone=10):
        widthWindow = self.Bus.GetVariable("widthBox")
        heightWindow = self.Bus.GetVariable("heightBox")
        PosBoxX = self.Bus.GetVariable("xBoxPos",)
        PosBoxY = self.Bus.GetVariable("yBoxPos")
        
        playerPos = self.Bus.GetVariable("playerPos")

        if widthWindow is not None and heightWindow is not None and PosBoxX is not None and playerPos is not None:
            PosBoxX, PosBoxY
            
            if PosBoxX - widthWindow/2 > self.center_x or PosBoxX + widthWindow/2 < self.center_x or PosBoxY - heightWindow/2 > self.center_y or PosBoxY + heightWindow/2 < self.center_y:
                self.dir = MathGame.get_angle_degrees(self.center_x, self.center_y, *playerPos) + random.randint(-75,75)
                self.points.append((MathGame.clamp(self.center_x, PosBoxX - widthWindow/2, PosBoxX + widthWindow/2), MathGame.clamp(self.center_y, PosBoxY - heightWindow/2, PosBoxY + heightWindow/2)))

        self.dir = self.dir % 360

    def returnToPoints(self):
        if self.points:
            point = self.points[-1]
            if MathGame.get_distance(self.center_x, self.center_y, *point) < 30:
                self.points.pop()
                return

            self.dir = int(MathGame.get_angle_degrees(self.center_x, self.center_y,*point))
    
    def onUpdate(self):
        if self.timeAttack > 0:
            self.limityWindow(30)
        else:
            self.returnToPoints() 

        if self.points == [] and self.timeAttack <= 0:
            self.Bus.GetFunction("EndAttack")
        
        dt = self.Bus.GetVariable("deltatime") or 0
        self.timeAttack -= dt
        
        self.speed = self.speedAttack if self.timeAttack > 0 else self.speedReturn

        self.center_x += MathGame.cos(MathGame.radians(self.dir)) * self.speed * dt
        self.center_y -= MathGame.sin(MathGame.radians(self.dir)) * self.speed * dt

        self.angle = -self.dir + (10 * dt)
        
    def onDraw(self,layer:int):
        dt = self.Bus.GetVariable("deltatime") or 0
        if layer == 1:
            if self.points:
                arcade.draw_line(self.center_x,self.center_y, *self.points[-1], self.lineColor, 2)
            arcade.draw_line_strip(self.points, self.lineColor, 2)
        if layer == 4:
            arcade.draw_sprite(self)