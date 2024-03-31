import sys
import pygame as pg
import json

from Const import *
from Text import Text
from Spritesheet import Spritesheet


class MainMenu(object):
    def __init__(self):
        self.mainImage = pg.image.load(r'images/super_mario_bros.png').convert_alpha()
        self.spritesheet = Spritesheet("./images/title_screen.png")
        self.menu_dot = self.spritesheet.image_at(
            0, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.menu_dot2 = self.spritesheet.image_at(
            20, 150, 2, colorkey=[255, 0, 220], ignoreTileSize=True
        )
        self.startGameText = Text('NEW GAME', 16, (230, 260))
        self.optionText = Text('OPTION', 16, (215, 300))
        self.exitText = Text('EXIT', 16, (200, 340))
        self.loadSettings("./settings.json")
        self.start = False
        self.state = 0
        self.music = True
        self.sfx = True
        self.state
        self.inSettings = False
        self.musicTextState =  Text('ON', 16, (300, 260))
        self.sfxTextState =  Text('hehehe', 16, (300, 300))
        self.musicText =  Text('MUSIC', 16, (205, 260))
        self.sfxText =  Text('SFX', 16, (190, 300))
        self.backText = Text('BACK', 16, (200,340))

    def loadSettings(self, url):
        try:
            with open(url) as jsonData:
                data = json.load(jsonData)
                if data["sound"]:
                    self.music = True
                else:
                    self.music = False
                if data["sfx"]:
                    self.sfx = True
                    # self.sound.allowSFX = True
                else:
                    # self.sound.allowSFX = False
                    self.sfx = False
        except (IOError, OSError):
            self.music = False
            self.sound.allowSFX = False
            self.sfx = False
            self.saveSettings("./settings.json")

    def saveSettings(self, url):
        data = {"sound": self.music, "sfx": self.sfx}
        with open(url, "w") as outfile:
            json.dump(data, outfile)

    def render(self, core):
        core.screen.blit(self.mainImage, (50, 50))
        
        if self.music:
            core.get_sound().play('overworld', 9999999, 0.2)
        if not self.inSettings:
            
            self.drawTitle(core)
        else: 
            self.drawSettings(core)
    def drawSettings(self, core):
        self.drawDot(core)
        
        self.musicText.render(core)
        if self.music:
            self.musicTextState = Text('ON', 16, (300, 260))
            self.musicTextState.render(core)
        else:
            self.musicTextState = Text('OFF', 16, (300, 260))
            self.musicTextState.render(core)
        self.sfxText.render(core)
        if self.sfx:
            self.sfxTextState = Text('ON', 16, (300, 300))
            self.sfxTextState.render(core)
        else:
            self.sfxTextState = Text('OFF', 16, (300, 300))
            self.sfxTextState.render(core)
        self.backText.render(core)

    def drawTitle(self, core):
        self.drawDot(core)
        self.startGameText.render(core)
        self.optionText.render(core)
        self.exitText.render(core)
    def drawDot(self, core):
        if self.state == 0:
            core.screen.blit(self.menu_dot, (125, 243))
            core.screen.blit(self.menu_dot2, (125, 283))
            core.screen.blit(self.menu_dot2, (125, 323))
        elif self.state == 1:
            core.screen.blit(self.menu_dot2, (125, 243))
            core.screen.blit(self.menu_dot, (125, 283))
            core.screen.blit(self.menu_dot2, (125, 323))
        elif self.state == 2:
            core.screen.blit(self.menu_dot2, (125, 243))
            core.screen.blit(self.menu_dot2, (125, 283))
            core.screen.blit(self.menu_dot, (125, 323))
    def checkInput(self, core):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.inSettings:
                        self.inSettings = False
                        self.__init__()
                    else:
                        pg.quit()
                        sys.exit()
                elif event.key == pg.K_UP or event.key == pg.K_k:
                    if self.state > 0:
                        self.state -= 1
                elif event.key == pg.K_DOWN or event.key == pg.K_j:
                    if self.state < 2:
                        self.state += 1
                elif event.key == pg.K_RETURN:
                    if not self.inSettings:
                        if self.state == 0:
                            self.start = True
                        elif self.state == 1:
                            self.inSettings = True
                            self.state = 0
                        elif self.state == 2:
                            pg.quit()
                            sys.exit()
                    else:
                        if self.state == 0:
                            if self.music:
                                core.get_sound().stop('overworld')
                                self.music = False
                            else:
                                core.get_sound().play('overworld', 9999999, 0.2)
                                self.music = True
                            self.saveSettings("./settings.json")
                        elif self.state == 1:
                            if self.sfx:
                                self.sfx = False
                            else:
                                self.sfx = True
                            self.saveSettings("./settings.json")
                        elif self.state == 2:
                            self.inSettings = False
        pg.display.update()
