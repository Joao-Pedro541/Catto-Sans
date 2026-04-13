import arcade
import assets.managers.MathGame as MathGame

from assets.managers.eventBusScript import EventBus

    
class playerObject():
    def __init__(self, Bus: EventBus, posInitX=0, posInitY=0):
        super().__init__()
        
        self.sprite = arcade.Sprite("assets/sprites/Player/Heart_Red.png", scale=0.25)


        self.centerMap = (posInitX,posInitY)
        self.sprite.center_x = posInitX
        self.sprite.center_y = posInitY
        self.sprite.scale = 0.25

        self.blinkTime = 0

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
            "Determination": self.DeterminationMoviment,
            "Patience": self.PatienceMoviment,
            "Bravery": self.BraveryMoviment,
            "Integrity": self.IntegrityMoviment,
            "Perseverance": self.PerseveranceMoviment,
            "Kindness": self.KindnessMoviment,
            "Justice": self.JusticeMoviment
        }

        self.ChangeStatePlayerMoviment = {
            "Determination": self.DeterminationStart,
            "Patience": self.PatienceStart,
            "Bravery": self.BraveryStart,
            "Integrity": self.IntegrityStart,
            "Perseverance": self.PerseveranceStart,
            "Kindness": self.KindnessStart,
            "Justice": self.JusticeStart
        }

        self.PlayerState = "Determination"
        
        self.speed = 175
        self.dir = 0
        self.scale = 0.25
        arcade.load_font(f"assets/fonts/determination/determination.ttf")

        #System Variables
        self.input = {}
        self.deltatime = 0

        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("onDraw", self.onDraw)
        self.Bus.SetFunction("changePlayerLife", self.changePlayerLife)
        self.Bus.SetFunction("changeStage", self.changeStages)

        self.inputCommands = {
                            "MoveHorizontal": {arcade.key.LEFT: -1, arcade.key.RIGHT: 1, arcade.key.A: -1, arcade.key.D: 1},
                            "MoveVertical": {arcade.key.UP: 1, arcade.key.DOWN: -1, arcade.key.W: 1, arcade.key.S: -1}
                }
        
        self.directionX = 0
        self.directionY = 0

        self.life = 40
        self.invicibilyTime = 0.5

        self.changeStages(self.PlayerState)

    def InputMoviment(self):
        X = 0         
        Y = 0       
        if self.Bus.GetVariable("keyPress",arcade.key.LEFT) or self.Bus.GetVariable("keyPress",arcade.key.A):
            X = -1
        elif self.Bus.GetVariable("keyPress",arcade.key.RIGHT) or self.Bus.GetVariable("keyPress",arcade.key.D):
            X = 1
        if self.Bus.GetVariable("keyPress",arcade.key.UP) or self.Bus.GetVariable("keyPress",arcade.key.W):
            Y = 1
        elif self.Bus.GetVariable("keyPress",arcade.key.DOWN) or self.Bus.GetVariable("keyPress",arcade.key.S):
            Y = -1
        return X,Y
    
    def BoxLimity(self, posX, posY, deadzone=10):
        xBoxPos = self.Bus.GetVariable("xBoxPos")
        yBoxPos = self.Bus.GetVariable("yBoxPos")
        widthBox = self.Bus.GetVariable("widthBox")
        heightBox = self.Bus.GetVariable("heightBox")

        if xBoxPos is not None and yBoxPos is not None and widthBox is not None and heightBox is not None:
            posX = MathGame.clamp(posX, xBoxPos - widthBox/2 + deadzone, xBoxPos + widthBox/2 - deadzone)
            posY = MathGame.clamp(posY, yBoxPos - heightBox/2 + deadzone, yBoxPos + heightBox/2 - deadzone)
        return posX, posY
    
    def onUpdate(self):
        self.deltatime = self.Bus.GetVariable("deltatime") or 0
        self.input = self.Bus.GetVariable("inputKeys") or {}

        self.sprite.center_x, self.sprite.center_y = self.playerMoviment[self.PlayerState]() if self.PlayerState in self.playerMoviment else (self.sprite.center_x, self.sprite.center_y)

        self.Bus.SetVariable("playerPos", (self.sprite.center_x, self.sprite.center_y))
        self.Bus.SetVariable("playerSprite", self.sprite)

        if self.invicibilyTime > 0: self.invicibilyTime -= self.deltatime

        if self.blinkTime > 0: self.blinkTime -= self.deltatime
        elif self.blinkTime < 0: self.blinkTime = 0


    def onDraw(self,layer:int):
        self.sprite.texture = self.spritesPlayer[self.PlayerState]
        if layer == 2:
            self.sprite.alpha = MathGame.magnitude(((int(self.blinkTime * 10) % 2) -1 )* 255)
            arcade.draw_sprite(self.sprite)
        
        arcade.draw_text(self.life,40, 300 , arcade.color.WHITE, 14,font_name="determination")

    def changePlayerLife(self, amount, invicibilyTimeMax = 0.5):
        
        if self.invicibilyTime <= 0:
            self.blinkTime = invicibilyTimeMax
            self.life += amount
            self.invicibilyTime = invicibilyTimeMax
            

    def changeStages(self,stage = "Determination"):
        self.PlayerState = stage
        self.ChangeStatePlayerMoviment[stage]()

    def DeterminationMoviment(self):  
        self.directionX, self.directionY= self.InputMoviment()

        return self.BoxLimity(self.sprite.center_x + (self.directionX * self.speed) * self.deltatime, 
                                self.sprite.center_y + (self.directionY * self.speed) * self.deltatime)

    def PatienceMoviment(self):
         
        if self.Bus is not None:
            xBoxPos = self.Bus.GetVariable("xBoxPos") or self.sprite.center_x
            yBoxPos = self.Bus.GetVariable("yBoxPos") or self.sprite.center_y

            directionX, directionY = self.InputMoviment()

            if directionX != 0 or directionY != 0:
                xBoxPos = xBoxPos + (directionX * self.speed) *self.deltatime
                yBoxPos = yBoxPos +  (directionY * self.speed) *self.deltatime
            if self.Bus.GetVariable("widthBox") is not None and self.Bus.GetVariable("heightBox") is not None:

                xBoxPos = MathGame.clamp(xBoxPos, self.sprite.center_x - self.Bus.GetVariable("widthBox")/2 + 10, self.sprite.center_x + self.Bus.GetVariable("widthBox")/2 - 10)
                yBoxPos = MathGame.clamp(yBoxPos, self.sprite.center_y - self.Bus.GetVariable("heightBox")/2 + 10, self.sprite.center_y + self.Bus.GetVariable("heightBox")/2 - 10)

            self.Bus.GetFunction("chanceBoxBattle", xBoxPos, yBoxPos, color = arcade.color.CYAN)
        return (320,140)

    def BraveryMoviment(self):
        for key,value in self.input.items():     
            if key is "keyPress": 
                for i in value:           
                    self.directionX = self.inputCommands["MoveHorizontal"].get(i, 0) or self.directionX
                    self.directionY = self.inputCommands["MoveVertical"].get(i, 0) or self.directionY
        x = self.sprite.center_x + (self.directionX * self.speed) * self.deltatime
        y = self.sprite.center_y + (self.directionY * self.speed) * self.deltatime



        if self.Bus is not None:
            xBoxPos = self.Bus.GetVariable("xBoxPos") or self.sprite.center_x
            yBoxPos = self.Bus.GetVariable("yBoxPos") or self.sprite.center_y

            if self.Bus.GetVariable("widthBox") is not None and self.Bus.GetVariable("heightBox") is not None:

                if x < xBoxPos - self.Bus.GetVariable("widthBox")/2 + 5:
                    x = xBoxPos + self.Bus.GetVariable("widthBox")/2 - 10
                if x > xBoxPos + self.Bus.GetVariable("widthBox")/2 - 5:
                    x = xBoxPos - self.Bus.GetVariable("widthBox")/2 + 10

                if y < yBoxPos - self.Bus.GetVariable("heightBox")/2 + 5:
                    y = yBoxPos + self.Bus.GetVariable("heightBox")/2 - 10
                if y > yBoxPos + self.Bus.GetVariable("heightBox")/2 - 5:
                    y = yBoxPos - self.Bus.GetVariable("heightBox")/2 + 10

        return x,y
        
    def IntegrityMoviment(self):
        return (0, -1)

    def PerseveranceMoviment(self):
        return (1, 1)

    def KindnessMoviment(self):
        return (-1, -1)

    def JusticeMoviment(self):
        return (0,-1)
    
    def DeterminationStart(self):
        camera = self.Bus.GetVariable("camera")
        if camera is not None:
            self.sprite.center_x,self.sprite.center_y = self.centerMap

    def PatienceStart(self):
        camera = self.Bus.GetVariable("camera")
        if camera is not None:
            self.sprite.center_x,self.sprite.center_y = self.centerMap
            
        self.Bus.SetVariable("xBoxPos", self.sprite.center_x)
        self.Bus.SetVariable("yBoxPos", self.sprite.center_y)

    def BraveryStart(self):
        self.sprite.center_x, self.sprite.center_y = self.centerMap
        self.directionX,self.directionY = 1,1

    def IntegrityStart(self):
        # No specific start action, or reset position
        pass

    def PerseveranceStart(self):
        # No specific start action
        pass

    def KindnessStart(self):
        # No specific start action
        pass

    def JusticeStart(self):
        # No specific start action
        pass
