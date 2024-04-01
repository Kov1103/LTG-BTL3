import pygame as pg

from Entity import Entity
from Const import *


class Bowser(Entity):
    def __init__(self, x_pos, y_pos, move_direction):
        super().__init__()
        self.rect = pg.Rect(x_pos, y_pos, 64, 64)

        self.health = 5
        self.is_damaged = False
        self.damage_duration = 5
        self.damage_timer = 0
        
        if move_direction:
            self.x_vel = 1
        else:
            self.x_vel = -1

        self.crushed = False
        self.hp = 5
        self.current_image = 0
        self.image_tick = 0
        self.images = [
            pg.transform.scale(pg.image.load('images/Bowser_0.png').convert_alpha(), (64, 64)),
            pg.transform.scale(pg.image.load('images/Bowser_1.png').convert_alpha(), (64, 64)),
            pg.transform.scale(pg.image.load('images/Bowser_dead.png').convert_alpha(), (64, 64)),
            pg.transform.scale(pg.image.load('images/Bowser_2.png').convert_alpha(), (64, 64)),
        ]
        self.images.append(pg.transform.flip(self.images[0], 180, 0))
        self.images.append(pg.transform.flip(self.images[1], 180, 0))
        self.images.append(pg.transform.flip(self.images[3], 180, 0))

    def take_damage(self, amount=1):
        self.health -= amount
        self.is_damaged = True
        self.damage_timer = self.damage_duration
        
    def die(self, core, instantly, crushed):
        if not instantly:
            core.get_map().get_player().add_score(core.get_map().score_for_killing_mob)
            core.get_map().spawn_score_text(self.rect.x + 16, self.rect.y)

            if crushed:
                if self.hp == 0:
                    self.crushed = True
                    self.image_tick = 0
                    self.current_image = 2
                    self.state = -1
                    core.get_sound().play('kill_mob', 0, 0.5)
                    self.collision = False
                else:
                    self.hp -=1    
            else:
                self.y_vel = -4
                self.current_image = 2
                core.get_sound().play('shot', 0, 0.5)
                self.state = -1
                self.collision = False

        else:
            core.get_map().get_mobs().remove(self)

    def check_collision_with_player(self, core):
        if self.collision:
            if self.rect.colliderect(core.get_map().get_player().rect):
                if self.state != -1:
                    if core.get_map().get_player().y_vel > 0:
                        self.take_damage()
                        if self.health <= 0:
                            self.die(core, instantly=False, crushed=True)
                        core.get_map().get_player().reset_jump()
                        core.get_map().get_player().jump_on_mob()
                    else:
                        if not core.get_map().get_player().unkillable:
                            core.get_map().get_player().set_powerlvl(0, core)

    def update_image(self):
        self.image_tick += 1

        if self.x_vel > 0:
            self.move_direction = True
        else:
            self.move_direction = False

        if self.image_tick == 35:
            if self.move_direction:
                self.current_image = 5
            else:
                self.current_image = 1
        elif self.image_tick == 70:
            if self.move_direction:
                self.current_image = 4
            else:
                self.current_image = 0
            self.image_tick = 0

    def update(self, core):
        if self.state == 0:
            self.update_image()

            if not self.on_ground:
                self.y_vel += GRAVITY

            blocks = core.get_map().get_blocks_for_collision(int(self.rect.x // 32), int(self.rect.y // 32))
            self.update_x_pos(blocks)
            self.update_y_pos(blocks)

            self.check_map_borders(core)

        elif self.state == -1:
            if self.crushed:
                self.image_tick += 1
                if self.image_tick == 50:
                    core.get_map().get_mobs().remove(self)
            else:
                self.y_vel += GRAVITY
                self.rect.y += self.y_vel
                self.check_map_borders(core)
                
        if self.is_damaged:
            self.damage_timer -= 1
            if self.damage_timer <= 0:
                self.is_damaged = False

    def render(self, core):
        if self.is_damaged:
            if self.move_direction:
                self.current_image = 6
            else:
                self.current_image = 3
        core.screen.blit(self.images[self.current_image], core.get_map().get_camera().apply(self))
