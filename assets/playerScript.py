import arcade
import GameSupportArcadePython.MathGame as MathGame

from GameSupportArcadePython.eventBusScript import EventBus

    
class playerObject(arcade.Sprite):
    def __init__(self, Bus: EventBus, posInitX=0, posInitY=0):
        super().__init__()
        self.center_x = posInitX
        self.center_y = posInitY
        
        self.Bus = Bus

        self.projectileType = 1
        self.spritesPlayer = {
            "Determination": arcade.load_texture("assets/sprites/Player/Heart_Red.png"),
            "Patience": arcade.load_texture("assets/sprites/Player/Heart_Cyan.png"),
            "Perseverance": arcade.load_texture("assets/sprites/Player/Heart_Purple.png"),
            "Bravery": arcade.load_texture("assets/sprites/Player/Heart_Orange.png"),
            "Justice": arcade.load_texture("assets/sprites/Player/Heart_Yellow.png"),
            "Kindness": arcade.load_texture("assets/sprites/Player/Heart_Green.png"),
            "Integrity": arcade.load_texture("assets/sprites/Player/Heart_Blue.png")
        }
        
        self.playerMoviment = {
            "Determination": self.DeterminaionMoviment,
            "Patience": self.PatienceMoviment,
            "Bravery": self.BraveryMoviment,
            "Integrity": self.IntegrityMoviment,
            "Perseverance": self.PerseveranceMoviment,
            "Kindness": self.KindnessMoviment,
            "Justice": self.JusticeMoviment
        }
        
        self.speed = 250
        self.dir = 0

        self.PlayerState = "Determination"

        self.scale = 0.25

        #System Variables
        self.input = {}
        self.deltatime = 0

        self.Bus.SetFunction("onSetup", self.onSetup)
        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("onDraw", self.onDraw)

        self.inputCommands = {
                            "MoveHorizontal": {arcade.key.LEFT: -1, arcade.key.RIGHT: 1},
                            "MoveVertical": {arcade.key.UP: 1, arcade.key.DOWN: -1}
                }
        
        self.directionX = 0
        self.directionY = 0

    def InputMoviment(self):
        X = 0         
        Y = 0 

        for key,value in self.input.items():     
            if key is "keyPress": 
                for i in value:           
                    X += self.inputCommands["MoveHorizontal"].get(i, 0)
                    Y += self.inputCommands["MoveVertical"].get(i, 0)

        return MathGame.lerp_2d((self.directionX,self.directionY), MathGame.normalized2D(X,Y), 0.8 * (self.deltatime * 17))

    def DeterminaionMoviment(self):  
        self.directionX, self.directionY= self.InputMoviment() 

        return self.BoxLimity(self.center_x + (self.directionX * self.speed) * self.deltatime, 
        self.center_y +  (self.directionY * self.speed) * self.deltatime)

    def PatienceMoviment(self):
         
        if self.Bus is not None:
            xBoxPos = self.Bus.GetVariable("xBoxPos") or self.center_x
            yBoxPos = self.Bus.GetVariable("yBoxPos") or self.center_y

            directionX, directionY = self.InputMoviment()

            if directionX != 0 or directionY != 0:
                xBoxPos = xBoxPos + (directionX * self.speed) *self.deltatime
                yBoxPos = yBoxPos +  (directionY * self.speed) *self.deltatime
            if self.Bus.GetVariable("widthBox") is not None and self.Bus.GetVariable("heightBox") is not None:

                xBoxPos = MathGame.clamp(xBoxPos, self.center_x - self.Bus.GetVariable("widthBox")/2 + 10, self.center_x + self.Bus.GetVariable("widthBox")/2 - 10)
                yBoxPos = MathGame.clamp(yBoxPos, self.center_y - self.Bus.GetVariable("heightBox")/2 + 10, self.center_y + self.Bus.GetVariable("heightBox")/2 - 10)

            self.Bus.GetFunction("chanceBoxBattle", xBoxPos, yBoxPos, color = arcade.color.CYAN)
        return (320,140)

    def BraveryMoviment(self):
        return (-1, 0)

    def IntegrityMoviment(self):
        return (0, -1)

    def PerseveranceMoviment(self):
        return (1, 1)

    def KindnessMoviment(self):
        return (-1, -1)

    def JusticeMoviment(self):
        return (1, -1)
    
    def BoxLimity(self, posX, posY, deadzone=10):
        xBoxPos = self.Bus.GetVariable("xBoxPos")
        yBoxPos = self.Bus.GetVariable("yBoxPos")
        widthBox = self.Bus.GetVariable("widthBox")
        heightBox = self.Bus.GetVariable("heightBox")

        if xBoxPos is not None and yBoxPos is not None and widthBox is not None and heightBox is not None:
            posX = MathGame.clamp(posX, xBoxPos - widthBox/2 + deadzone, xBoxPos + widthBox/2 - deadzone)
            posY = MathGame.clamp(posY, yBoxPos - heightBox/2 + deadzone, yBoxPos + heightBox/2 - deadzone)
        return posX, posY

    def onSetup(self):
        self.texture = self.spritesPlayer["Determination"]
    
    def onUpdate(self):
        self.deltatime = self.Bus.GetVariable("deltatime") or 0
        self.input = self.Bus.GetVariable("inputKeys") or {}

        self.center_x, self.center_y = self.playerMoviment[self.PlayerState]() if self.PlayerState in self.playerMoviment else (self.center_x, self.center_y)

        self.Bus.SetVariable("playerPos", (self.center_x, self.center_y))

    def onDraw(self,layer:int):
        self.texture = self.spritesPlayer[self.PlayerState]
        if layer == 2:
            arcade.draw_sprite(self)
