from GameSupportArcadePython.eventBusScript import EventBus 
import arcade.sound
import os

class SoundManager():
    def __init__(self, Bus: EventBus):
        self.Bus = Bus
        mp3_files = [f for f in os.listdir("assets/sounds") if f.endswith(".mp3")]

        self.sounds = {}
        for file in mp3_files:
            sound = arcade.sound.load_sound(f"assets/sounds/{file}")
            name = file.split(".mp3")[0]
            self.sounds[name] = sound
            print(f"Loaded sound: {name}")

        self.Bus.SetFunction("PlaySoundEffect", self.PlaySoundEffect)

    def PlaySoundEffect(self, name, volume=1.0, loop=False):
        arcade.sound.play_sound(self.sounds[name], volume=volume, loop=loop)