import arcade
from GameSupportArcadePython.eventBusScript import EventBus

class WindowGame(arcade.Window):

    def __init__(self, Bus:EventBus, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.camera = None
        self.background_color = arcade.color.BLACK

        self.Bus = Bus
        

    def on_setup(self):
        self.camera = arcade.Camera2D()
        self.camera.position = (320,240)

        self.Bus.SetVariable("heightWindow", self.height)
        self.Bus.SetVariable("widthWindow", self.width)
        self.Bus.SetVariable("camera", self.camera)

    def on_draw(self):
        self.clear()
        self.camera.use()

        for i in range(0,8):
            self.Bus.GetFunction("onDraw",i)

    def on_resize(self, width, height):
        return super().on_resize(width, height)

    def on_update(self, delta_time):
        
        self.Bus.GetFunction("onUpdate")
        self.Bus.SetVariable("deltatime", delta_time)

    def on_fixed_update(self, delta_time):
        self.Bus.GetFunction("fixedUpdate")

    # define Key and Mouse events
    def on_key_press(self, key, modifiers):
        self.Bus.GetFunction("KeyPress",key,modifiers)

    def on_key_release(self, key, modifiers):
        self.Bus.GetFunction("KeyRelease",key,modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.Bus.GetFunction("MouseMotion",x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):  
        self.Bus.GetFunction("MousePress",x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.Bus.GetFunction("MouseRelease",x, y, button, modifiers)