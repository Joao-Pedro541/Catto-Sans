import arcade

from assets.managers import MathGame
from assets.managers.eventBusScript import EventBus


class boxBattle(arcade.Sprite):
    def __init__(self,Bus: EventBus, pos_x: float, pos_y: float, tam_x: float, tam_y: float):
        super().__init__()
        self.center_x = pos_x
        self.center_y = pos_y
        self.width = tam_x
        self.height = tam_y

        self.Bus = Bus

        self.Bus.SetFunction("onUpdate", self.onUpdate)
        self.Bus.SetFunction("onDraw", self.onDraw)
        self.Bus.SetFunction("chanceBoxBattle", self.chanceBoxBattle)

        self.color = arcade.color.WHITE

    def onUpdate(self):
        if self.Bus is not None:
            self.Bus.SetVariable("xBoxPos", self.center_x)
            self.Bus.SetVariable("yBoxPos", self.center_y)
            self.Bus.SetVariable("widthBox", self.width)
            self.Bus.SetVariable("heightBox", self.height)


    def chanceBoxBattle(self, pos_x: float = None, pos_y: float = None, tam_x: float = 260, tam_y: float = 200, color = arcade.color.WHITE):

        self.center_x = pos_x if pos_x is not None else self.center_x
        self.center_y = pos_y if pos_y is not None else self.center_y
        self.width = tam_x
        self.height = tam_y
        self.color = color

    def limityWindow(self, posX, posY, deadzone=10):
        widthWindow = self.Bus.GetVariable("widthWindow")
        heightWindow = self.Bus.GetVariable("heightWindow")

        if widthWindow is not None and heightWindow is not None:
            posX = MathGame.clamp(posX, deadzone, widthWindow - deadzone)
            posY = MathGame.clamp(posY, deadzone, heightWindow - deadzone)
        return posX, posY

    def onDraw(self, layer: int):
        if layer == 2:
            arcade.draw_rect_outline(arcade.rect.XYWH(self.center_x,self.center_y,self.width,self.height,)
                                    ,self.color,
                                    4
                                    )
        if layer == 1:
            arcade.draw_rect_filled(arcade.rect.XYWH(self.center_x,self.center_y,self.width,self.height,)
                                    ,arcade.color.BLACK
                                    )
        