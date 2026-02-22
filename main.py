import arcade

from GameSupportArcadePython.eventBusScript import EventBus
from GameSupportArcadePython.objectsScripts import ObjectsGame
from GameSupportArcadePython.windowScript import WindowGame

def main():
    events = EventBus()
    managerObjects = ObjectsGame(events)

    window = WindowGame(events,width=640,height=480,title="GattoSans")
    managerObjects.DefineScene("scene0")
    window.on_setup()
    arcade.run()

if __name__ == "__main__":
    main()