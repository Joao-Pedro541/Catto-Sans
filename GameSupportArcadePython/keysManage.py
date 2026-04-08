from GameSupportArcadePython.eventBusScript import EventBus

class keys():
    def __init__(self, Bus: EventBus):
        self.keys = {"keyUp":[], 
                      "keyPress":[], 
                      "KeyDown":[],
                      "mousePress":False,
                      "mouseDown":False,
                      "mouseUp":False}

        self.Bus = Bus

        self.MouseXInScreen = 0
        self.MouseYInScreen = 0

        self.MouseXInWorld = 0
        self.MouseYInWorld = 0

        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("KeyPress", self.KeyPress)
        self.Bus.SetFunction("KeyRelease", self.KeyRelease)
        self.Bus.SetFunction("MouseMotion", self.MouseMotion)
        self.Bus.SetFunction("MousePress", self.MousePress)
        self.Bus.SetFunction("MouseRelease", self.MouseRelease)
        self.Bus.SetFunction("onCamera", self.onCamera)



    def onUpdate(self):

        self.Bus.SetVariable("mouseDirX", self.MouseXInWorld)
        self.Bus.SetVariable("mouseDirY", self.MouseYInWorld)
        self.Bus.SetVariable("inputKeys",self.keys)

        self.keys["keyUp"].clear()
        self.keys["KeyDown"].clear()
        

        self.keys["mouseUp"] = False
        self.keys["mousePress"] = False

    def KeyPress(self,key,modifiers):
        self.keys["KeyDown"].append(key)
        
        self.keys["keyPress"].append(key)

    def KeyRelease(self,key,modifiers):
        self.keys["keyUp"].append(key)

        if key in self.keys["keyPress"]:
            self.keys["keyPress"].remove(key)

    def MouseMotion(self,x,y,dx,dy):
        self.MouseXInScreen = x
        self.MouseYInScreen = y

    def MousePress(self,x,y,button,modifiers):
        self.keys["mousePress"] = True
        self.keys["mouseDown"] = True

    def MouseRelease(self,x,y,button,modifiers):
        self.keys["mouseUp"] = True
        self.keys["mouseDown"] = False 

    def onCamera(self,cam):
        self.MouseXInWorld = cam.position.x + (self.MouseXInScreen - cam.width / 2)
        self.MouseYInWorld = cam.position.y + (self.MouseYInScreen - cam.height / 2)