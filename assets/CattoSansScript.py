import arcade
import GameSupportArcadePython.MathGame as MathGame

from GameSupportArcadePython.eventBusScript import EventBus

class cattoSans(arcade.SpriteList):
    def __init__(self, Bus: EventBus, posInitX=0, posInitY=0):
        super().__init__()

        self.legs = arcade.Sprite("assets/Sprites/CattoSans/Catto_Sans_legs_idle.png", center_x=posInitX, center_y=posInitY)
        self.torso = arcade.Sprite("assets/Sprites/CattoSans/Catto_Sans_torso_idle.png", center_x=posInitX, center_y=posInitY)
        self.cornea = arcade.Sprite("assets/Sprites/CattoSans/Catto_Sans_cornea_idle.png", center_x=posInitX, center_y=posInitY)
        self.pupilLeft = arcade.Sprite("assets/Sprites/CattoSans/Catto_Sans_pupil_left_idle.png", center_x=posInitX, center_y=posInitY)
        self.pupilRight = arcade.Sprite("assets/Sprites/CattoSans/Catto_Sans_pupil_right_idle.png", center_x=posInitX, center_y=posInitY)
        self.head = arcade.Sprite("assets/Sprites/CattoSans/Catto_Sans_head_idle.png", center_x=posInitX, center_y=posInitY)

        self.posX = posInitX
        self.posY = posInitY

        self.Bus = Bus
        self.deltatime = 0

        self.append(self.legs)
        self.append(self.torso)
        self.append(self.cornea)
        self.append(self.pupilLeft)
        self.append(self.pupilRight)
        self.append(self.head)
        
        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("onDraw", self.onDraw)

        self.dirShake = 1 

    def onUpdate(self):
        self.deltatime = self.Bus.GetVariable("deltatime") or 0

        self.shakeMov(speed=6.5, deadzone=2, amplitude=0.8, frequency=0.5) 

        self.cornea.center_x,self.cornea.center_y = self.head.center_x,self.head.center_y

        self.eyesControl(pointX=self.Bus.GetVariable("playerPos")[0], pointY=self.Bus.GetVariable("playerPos")[1])
        

    def eyesControl(self,pointX = float,pointY = float):

        self.pupilLeft.center_x,self.pupilLeft.center_y = MathGame.lerp_2d((self.pupilLeft.center_x,self.pupilLeft.center_y), MathGame.GetPointInCircleFlatten(MathGame.get_angle_degrees(self.head.center_x - 20,self.head.center_y + 80,pointX,pointY), 4, self.cornea.center_x, self.cornea.center_y,1), 0.1)
        self.pupilRight.center_x,self.pupilRight.center_y = MathGame.lerp_2d((self.pupilRight.center_x,self.pupilRight.center_y), MathGame.GetPointInCircleFlatten(MathGame.get_angle_degrees(self.head.center_x + 20,self.head.center_y + 80,pointX,pointY), 4, self.cornea.center_x, self.cornea.center_y,1), 0.1)

    def shakeMov(self, speed: float, deadzone: float, amplitude: float, frequency: float):

        if self.torso.center_x > self.posX + deadzone:
            self.dirShake = -1

        if self.torso.center_x < self.posX - deadzone:
            self.dirShake = 1
            

        self.torso.center_x += self.dirShake * (speed * self.deltatime)
        self.torso.center_y = self.posY - MathGame.sin((self.posX - self.torso.center_x) / frequency) * amplitude

        self.head.center_x = MathGame.lerp(self.head.center_x, self.torso.center_x, (0.5 * speed) * self.deltatime) 
        self.head.center_y = MathGame.lerp(self.head.center_y, self.torso.center_y, (0.85 * speed) * self.deltatime)


        
    
    def onDraw(self, layer: int):
        if layer == 0:
            self.draw()