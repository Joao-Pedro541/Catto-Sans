import arcade

from assets.managers.eventBusScript import EventBus
from assets.managers.objectsScripts import ObjectsGame
from assets.managers.windowScript import WindowGame

def main():
    events = EventBus()
    managerObjects = ObjectsGame(events)

    window = WindowGame(events,width=640,height=480,title="CattoSans")
    managerObjects.DefineScene("scene0")
    window.on_setup()
    window.run()

if __name__ == "__main__":
    main()