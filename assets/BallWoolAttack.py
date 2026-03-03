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
        self.speed = 800

        self.points = []

        self.lineColor = arcade.color.WHITE

    def limityWindow(self, deadzone=10):
        widthWindow = self.Bus.GetVariable("widthWindow")
        heightWindow = self.Bus.GetVariable("heightWindow")
        cameraWindow = self.Bus.GetVariable("camera")

        playerPos = self.Bus.GetVariable("playerPos")

        if widthWindow is not None and heightWindow is not None and cameraWindow.position is not None and playerPos is not None:
                cameraX, cameraY = cameraWindow.position
                
                if cameraX - widthWindow/2 > self.center_x or cameraX + widthWindow/2 < self.center_x or cameraY - heightWindow/2 > self.center_y or cameraY + heightWindow/2 < self.center_y:
                    self.dir = int(MathGame.get_angle_degrees(self.center_x, self.center_y,*playerPos) + random.randint(-30,30))
                    self.points.append((self.center_x, self.center_y))

        self.dir = self.dir % 360
    
    def onUpdate(self):
        self.limityWindow()
        dt = self.Bus.GetVariable("deltatime") or 0

        self.center_x += MathGame.cos(MathGame.radians(self.dir)) * self.speed * dt
        self.center_y -= MathGame.sin(MathGame.radians(self.dir)) * self.speed * dt

    def onDraw(self,layer:int):
        dt = self.Bus.GetVariable("deltatime") or 0
        if layer == 4:
            if self.points:
                arcade.draw_line(self.center_x,self.center_y, *self.points[-1], self.lineColor, 2)
            arcade.draw_line_strip(self.points, self.lineColor, 2)
            arcade.draw_sprite(self)