import pygame
from pygame.locals import *
from tetriumrpg import entity_handler, sprite_handler
from tetriumrpg.entity import Entity
from tetriumrpg.entity_handler import EntityHandler
from tetriumrpg.enum import Location, ID, Sprite_ID, Window_Definitions
from tetriumrpg.map import Map
from tetriumrpg.player import Player
from tetriumrpg.renderer import Renderer
from tetriumrpg.sprite_handler import SpriteHandler
from tetriumrpg.ticker import Ticker


class App:
    tps = 24
    fps = 140
    
    sprite_handler = 0
    entity_handler = 0
    
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
 
    def on_init(self):
        pygame.init()

        self._display_surf = pygame.display.set_mode((Window_Definitions.Window_Width,Window_Definitions.Window_Height), pygame.HWSURFACE)
        pygame.display.set_caption('Tetrium RPG')
        self._running = True
 
    def on_event(self, event):
        pass
            
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        sprite_handler = SpriteHandler()
        entity_handler = EntityHandler()
        map = Map()
        player = Player(Location.Spawn, ID.Player, "Engineer", Sprite_ID.Player_d4, map)
        entity_handler.add_entity(player)
        
        renderer = Renderer(entity_handler, sprite_handler, self._display_surf)
        ticker = Ticker(entity_handler, self)
        
        time_next_tick = 0
        time_next_render = 0
        tick = 0
        render = 0
        nextsecond = 0
        while(self._running):
            time_now = pygame.time.get_ticks()
            
            if(time_now > time_next_tick):
                ticker.tick()
                time_next_tick = time_now + 1000 / self.tps
                tick += 1
                
            if(time_now > time_next_render):
                renderer.render(entity_handler, map)
                time_next_render = time_now + 1000 / self.fps
                render += 1
                    
            if(nextsecond < time_now):
                print("TPS: " + str(tick) + " FPS: " + str(render))
                tick, render = 0,0
                nextsecond = time_now + 1000
            
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()