import arcade
import assets.managers.MathGame as MathGame
import random

from assets.managers.eventBusScript import EventBus

    
class BallAttack(arcade.Sprite):
    def __init__(self, Bus: EventBus, posInitX=0, posInitY=0):
        super().__init__()
        self.center_x = posInitX
        self.center_y = posInitY
        self.texture = arcade.load_texture("assets/Sprites/CattoSans/Attacks/BallWoolAttack.png")

        self.Bus = Bus

        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("onDraw", self.onDraw)

        self.dir = random.randint(45,135)

        self.speedAttack = 800
        self.speedReturn = 1600

        self.points = []

        self.lineColor = arcade.color.GRAY

        self.timeAttack = 10
        self.spin = 0

        self.Bus.GetFunction("chanceBoxBattle",tam_x=400,tam_y=280)
        self.Bus.GetFunction("changeStage")

    def limityWindow(self, deadzone=10):
        widthWindow = self.Bus.GetVariable("widthBox") or 0
        heightWindow = self.Bus.GetVariable("heightBox") or 0
        PosBoxX = self.Bus.GetVariable("xBoxPos") or 0
        PosBoxY = self.Bus.GetVariable("yBoxPos") or 0

        minX = PosBoxX - widthWindow/2
        maxX = PosBoxX + widthWindow/2
        minY = PosBoxY - heightWindow/2
        maxY = PosBoxY + heightWindow/2 
        
        playerPos = self.Bus.GetVariable("playerPos")

        if widthWindow is not None and heightWindow is not None and PosBoxX is not None and playerPos is not None:
            PosBoxX, PosBoxY

            lastPointX,lastPointY = MathGame.GetPointInCircle(self.dir,900,self.center_x,self.center_y)
            lastPointX,lastPointY = MathGame.clamp(lastPointX,minX,maxX), MathGame.clamp(lastPointY,minY,maxY)
            
            if deadzone >= MathGame.GetDist(self.center_x,lastPointX):
                self.dir = 180 - self.dir
                self.points.append((MathGame.clamp(self.center_x, minX, maxX), MathGame.clamp(self.center_y, minY, maxY)))

            if deadzone >= MathGame.GetDist(self.center_y,lastPointY):
                self.dir = -self.dir
                self.points.append((MathGame.clamp(self.center_x, minX, maxX), MathGame.clamp(self.center_y, minY, maxY)))
        
       

    def returnToPoints(self):
        if self.points:
            point = self.points[-1]
            if MathGame.get_distance(self.center_x, self.center_y, *point) < 30:
                self.points.pop()
                return

            self.dir = int(MathGame.get_angle_degrees(self.center_x, self.center_y,*point))
    
    def onUpdate(self):
        if self.timeAttack > 0:
            self.limityWindow()
        else:
            self.returnToPoints() 

        if self.points == [] and self.timeAttack <= 0:
            self.Bus.GetFunction("EndAttack")
        
        dt = self.Bus.GetVariable("deltatime") or 0
        self.timeAttack -= dt
        
        self.speed = self.speedAttack if self.timeAttack > 0 else self.speedReturn

        self.center_x += MathGame.cos(MathGame.radians(self.dir)) * self.speed * dt
        self.center_y -= MathGame.sin(MathGame.radians(self.dir)) * self.speed * dt

        self.spin += 4500 * dt
        self.spin = self.spin % 360

        self.angle = self.dir + self.spin

        if self.Bus.GetVariable("playerSprite") is not None:
            playerHit = arcade.check_for_collision(self, self.Bus.GetVariable("playerSprite"))

            if playerHit is True:
                self.Bus.GetFunction("changePlayerLife", -1)
        
    def onDraw(self,layer:int):
        dt = self.Bus.GetVariable("deltatime") or 0
        if layer == 1:
            if self.points:
                arcade.draw_line(self.center_x,self.center_y, *self.points[-1], self.lineColor, 2)
            arcade.draw_line_strip(self.points, self.lineColor, 2)
        if layer == 4:
            arcade.draw_sprite(self)