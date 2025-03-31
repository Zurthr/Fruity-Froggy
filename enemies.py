import os
import main 
import random
import math
import pygame
import time
from os import listdir
from os.path import isfile, join
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


#JANGAN LUPA NAMBAHIN DI LOOP MAIN!!!

pickup = pygame.mixer.Sound(resource_path("Assets/Pickup.mp3"))
pickup.set_volume(1)

class Rino(main.Enemy):
    GRAVITY = 1
    SPRITES = main.load_sprite_sheets('Enemies','Rino',52,34,True)
    ANIMATION_DELAY = 3

    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"Rino")
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 1
        self.hit = False
        self.hit_count = 0
        self.timing = 0
        self.x = 0
        self.y = 0
        self.iframe = 0
        self.speed = 3
    
    #movement

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def hurt(self):
        self.hit = True

    def loop(self,fps):
        self.y_vel += min(1, (self.fall_count/fps)*self.GRAVITY)
        
        self.move(self.x_vel, self.y_vel)
        if self.hit:
            self.hit_count += 1
        if self.hit_count > 90:
            self.hit = False
            self.hit_count = 0
            self.iframe = 0

        self.fall_count += 0.8
        self.update_sprite()
    
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    def hit_head(self):
        self.y_vel *= -1
        self.count = 0
    
    def update_sprite(self):
        sprite_sheet = 'Idle (52x34)'
        if self.hit:
            sprite_sheet = 'Hit (52x34)'
        elif self.x_vel != 0:
            sprite_sheet = 'Run (52x34)'

        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw(self,win,offsetx):
        win.blit(self.sprite, (self.rect.x - offsetx, self.rect.y))

class Mushroom(main.Enemy):
    GRAVITY = 1
    SPRITES = main.load_sprite_sheets('Enemies','Mushroom',32,32,True)
    ANIMATION_DELAY = 3

    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"Mushroom")
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 1
        self.hit = False
        self.hit_count = 0
        self.timing = 0
        self.x = 0
        self.y = 0
        self.iframe = 0
        self.speed = 2
    
    #movement

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def hurt(self):
        self.hit = True

    def loop(self,fps):
        self.y_vel += min(1, (self.fall_count/fps)*self.GRAVITY)
        
        self.move(self.x_vel, self.y_vel)
        if self.hit:
            self.hit_count += 1
        if self.hit_count > 90:
            self.hit = False
            self.hit_count = 0
            self.iframe = 0

        self.fall_count += 0.8
        self.update_sprite()
    
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    def hit_head(self):
        self.y_vel *= -1
        self.count = 0
    
    def update_sprite(self):
        sprite_sheet = 'Idle (32x32)'
        if self.hit:
            sprite_sheet = 'Hit'
        elif self.x_vel != 0:
            sprite_sheet = 'Run (32x32)'

        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw(self,win,offsetx):
        win.blit(self.sprite, (self.rect.x - offsetx, self.rect.y))

class Radish(main.Enemy):
    GRAVITY = 1
    SPRITES = main.load_sprite_sheets('Enemies','Radish',30,38,True)
    ANIMATION_DELAY = 3

    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"Radish")
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 1
        self.hit = False
        self.hit_count = 0
        self.timing = 0
        self.x = 0
        self.y = 0
        self.iframe = 0
        self.speed = 3
    
    #movement

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def hurt(self):
        self.hit = True

    def loop(self,fps):
        self.y_vel += min(1, (self.fall_count/fps)*self.GRAVITY)
        
        self.move(self.x_vel, self.y_vel)
        if self.hit:
            self.hit_count += 1
        if self.hit_count > 90:
            self.hit = False
            self.hit_count = 0
            self.iframe = 0

        self.fall_count += 0.8
        self.update_sprite()
    
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    def hit_head(self):
        self.y_vel *= -1
        self.count = 0
    
    def update_sprite(self):
        sprite_sheet = 'Idle 2 (30x38)'
        if self.hit:
            sprite_sheet = 'Hit (30x38)'
        elif self.x_vel != 0:
            sprite_sheet = 'Run (30x38)'

        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw(self,win,offsetx):
        win.blit(self.sprite, (self.rect.x - offsetx, self.rect.y))

class Apple(main.Object):
    ANIMATION_DELAY = 3
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"coin")
        self.apple = main.load_sprite_sheets("Fruits","Apple",width,height)
        self.image = self.apple["Apple"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.life = 1

    def suicide(self):
        if self.life == 1:
            pickup.play()

            self.life -= 1
        if self.life < -30:
            self.life = -31


    def loop(self):
        if self.life == 1:
            self.sheet = "Apple"
        elif self.life <= 0 and self.life >= -30:
            self.life -= 1
            self.sheet = "FruitDissapear"
            self.kill()
        
        sprites = self.apple[self.sheet]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Cherry(main.Object):
    ANIMATION_DELAY = 3
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"coin")
        self.cherry = main.load_sprite_sheets("Fruits","Cherry",width,height)
        self.image = self.cherry["Cherry"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.life = 1

    def suicide(self):
        if self.life == 1:
            pickup.play()
            self.life -= 1
        if self.life < -30:
            self.life = -31


    def loop(self):
        if self.life == 1:
            self.sheet = "Cherry"
        elif self.life <= 0 and self.life >= -30:
            self.life -= 1
            self.sheet = "FruitDissapear"
            self.kill()
        
        sprites = self.cherry[self.sheet]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Spikes(main.Object):
    ANIMATION_DELAY = 3
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"Spikes")
        self.spikes = main.load_sprite_sheets("Traps","Spikes",width,height)
        self.image = self.spikes["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
    
    def loop(self):
        sprites = self.spikes["Idle"]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
        

class Orange(main.Object):
    ANIMATION_DELAY = 3
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"coin")
        self.orange = main.load_sprite_sheets("Fruits","Orange",width,height)
        self.image = self.orange["Orange"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.life = 1

    def suicide(self):
        if self.life == 1:
            pickup.play()
            self.life -= 1
        if self.life < -30:
            self.life = -31


    def loop(self):
        if self.life == 1:
            self.sheet = "Orange"
        elif self.life <= 0 and self.life >= -30:
            self.life -= 1
            self.sheet = "FruitDissapear"
            self.kill()
        
        sprites = self.orange[self.sheet]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Melon(main.Object):
    ANIMATION_DELAY = 3
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"Melon")
        self.melon = main.load_sprite_sheets("Fruits","Melon",width,height)
        self.image = self.melon["Melon"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.life = 1

    def suicide(self):
        if self.life == 1:
            pickup.play()
            self.life -= 1
        if self.life < -30:
            self.life = -31


    def loop(self):
        if self.life == 1:
            self.sheet = "Melon"
        elif self.life <= 0 and self.life >= -30:
            self.life -= 1
            self.sheet = "FruitDissapear"
            self.kill()
        
        sprites = self.melon[self.sheet]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0