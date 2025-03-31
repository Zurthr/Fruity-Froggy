import os
import enemies
import random
import math
import pygame
import time
from os import listdir
from os.path import isfile, join
import sys


pygame.init()
pygame.display.set_caption("Fruity Froggy")
#setup stats
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
window = pygame.display.set_mode((WIDTH,HEIGHT))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
textfont = pygame.font.Font(resource_path("Assets/Fixedsys.ttf"),18)
overfont = pygame.font.Font(resource_path("Assets/Fixedsys.ttf"),50)
endfont = pygame.font.Font(resource_path("Assets/Fixedsys.ttf"),25)
xpfont = pygame.font.Font(resource_path("Assets/Fixedsys.ttf"),100)
window = pygame.display.set_mode((WIDTH,HEIGHT))

hurtsound = pygame.mixer.Sound(resource_path("Assets/hurt.wav"))
hurtsound.set_volume(1)
icon = pygame.image.load(resource_path("Assets/Bananas.png"))
pygame.display.set_icon(icon)


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = resource_path(join("Assets", dir1, dir2))  # Update path handling
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(resource_path(join(path, image))).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size):
    path = resource_path(join("Assets", "Terrain", "Terrain.png"))  # Update path
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 64, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_plat(size):
    path = resource_path(join("Assets", "Terrain", "Platform.png"))  # Update path
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 9, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_wall(size):
    path = resource_path(join("Assets", "Terrain", "Terrain.png"))  # Update path
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 64, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self,win,offsetx):
        win.blit(self.image,(self.rect.x - offsetx,self.rect.y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self,win,offsetx):
        win.blit(self.image,(self.rect.x - offsetx,self.rect.y))

class Wall(Object):
    def __init__(self,x,y,size):
        super().__init__(x,y,size,size)
        block = get_wall(size)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Platform(Object):
    def __init__(self,x,y,size):
        super().__init__(x,y,size,size,"Platform")
        block = get_plat(size)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Block(Object):
    def __init__(self,x,y,size):
        super().__init__(x,y,size,size)
        block = get_block(size)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)
    

class Fire(Object):
    ANIMATION_DELAY = 3
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"fire")
        self.fire = load_sprite_sheets("Traps","Fire",width,height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"
    
    def on(self):
        self.animation_name = "on"
    def off(self):
        self.animation_name = "off"
    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Button():
    def __init__(self,x,y,width,height,Name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.clicked = False

    def draw(self,win):
        win.blit(self.image,(self.rect.x,self.rect.y))

        #click
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.name == "Color":
            if self.clicked == False and pygame.mouse.get_pressed()[0] == 1:
                if color.true == False:
                    color.on()
                    color.true = True
                elif color.true == True:
                    color.off()
                    color.true = False
                self.clicked = True
        if self.rect.collidepoint(pos) and self.name == "Effect":
            if self.clicked == False and pygame.mouse.get_pressed()[0] == 1:
                if effect.true == False:
                    effect.on()
                    effect.true = True
                elif effect.true == True:
                    effect.off()
                    effect.true = False
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

class Color(Button):
    ANIMATION_DELAY = 10
    def __init__(self,x,y,width,height,true=False):
        super().__init__(x,y,width,height,Name="Color")
        self.color = load_sprite_sheets("Buttons","Color",width,height)
        self.image = self.color["offz"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.life = 1
        self.true = False
        self.sheet = "offz"
        self.name = "Color"
    def off(self):
        self.sheet = "offz"
        print("off")
    def on(self):
        self.sheet = "on3"
        print("on")
    def loop(self):
        sprites = self.color[self.sheet]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Effect(Button):
    ANIMATION_DELAY = 10
    def __init__(self,x,y,width,height,true=False):
        super().__init__(x,y,width,height,Name="Effect")
        self.effect = load_sprite_sheets("Buttons","Effect",width,height)
        self.image = self.effect["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.life = 1
        self.true = False
        self.name = "Effect"
        self.sheet = "off"
    def off(self):
        self.sheet = "off"
        print("off")
    def on(self):
        self.sheet = "on1"
        print("on")
    def loop(self):
        sprites = self.effect[self.sheet]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class ProgressBar():
    def __init__(self,x,y,width,height,max_hp):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.xp = 0
        self.max_hp = max_hp
        self.fade = 0
    
    def experience(self,xpval):
        self.xp += xpval
        self.hpchange = xpval
    
    def text(self):
        if int(self.rat*100) < 10:
            drawtext(f" {int(self.rat*100)}%",textfont,"#FFFFFF",self.x-35,self.y-1)
        elif self.rat == 1:
            drawtext(f":DD",textfont,"#FFFFFF",self.x-35,self.y-1)
        else: drawtext(f"{int(self.rat*100)}%",textfont,"#FFFFFF",self.x-35,self.y-1)

        

    def draw(self,surface):
        self.rat = self.xp/self.max_hp
        
        pygame.draw.rect(surface, "#473330",(self.x-40,self.y-5, self.w+10, self.h+10))
        pygame.draw.rect(surface, "#30211f",(self.x-3,self.y-3, self.w+6, self.h+6))  
        if color.true == False:
            pygame.draw.rect(surface, "#453937",(self.x,self.y, self.w, self.h))
            if self.rat*100 >= 0 and self.rat*100 < 16:
                pygame.draw.rect(surface, "#e23241",(self.x,self.y, self.w*self.rat, self.h))
            elif self.rat*100 >= 16 and self.rat*100 < 32:
                pygame.draw.rect(surface, "#ff9438",(self.x,self.y, self.w*self.rat, self.h))
            elif self.rat*100 >= 32 and self.rat*100 < 48:
                pygame.draw.rect(surface, "#ffdc44",(self.x,self.y, self.w*self.rat, self.h))
            elif self.rat*100 >= 48 and self.rat*100 < 64:
                pygame.draw.rect(surface, "#4dc16f",(self.x,self.y, self.w*self.rat, self.h))
            elif self.rat*100 >= 64 and self.rat*100 < 80:
                pygame.draw.rect(surface, "#1781af",(self.x,self.y, self.w*self.rat, self.h))
            elif self.rat*100 >= 80 and self.rat*100 < 100:
                pygame.draw.rect(surface, "#964fb8",(self.x,self.y, self.w*self.rat, self.h))
        if color.true == True:
            pygame.draw.rect(surface, "#ffe0c4",(self.x,self.y, self.w, self.h))
            pygame.draw.rect(surface, "#de7cf2",(self.x,self.y, self.w*self.rat, self.h)) #xp
        self.text()

class HealthBar():
    def __init__(self,x,y,width,height,max_hp):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.hp = max_hp
        self.max_hp = max_hp
        self.fade = 0
        self.fade2 = 255
        self.fade21 = 50
        self.effect = "None"
    
    def health(self,hpval):
        self.hp += hpval
        self.hpchange = hpval
    
            

    def newgame(self):
        if self.fade21 >= 1:
            self.fade21 -=1
        if self.fade21 == 0:
            self.fade2 -= 4
        s = pygame.Surface((1000,800)) 
        s.set_alpha(self.fade2)
        newimg = pygame.image.load(resource_path("Assets/Opening.png")).convert_alpha()
        newimg.set_alpha(self.fade2)

        window.blit(newimg, (WIDTH/6+20,HEIGHT/6))              
        
    def text(self,Lose,Win):
        if self.hp == 100:
            drawtext(f"{self.hp}",textfont,"#FFFFFF",self.x-35,self.y-1)
        elif self.hp <= 0:
            drawtext(f"...",textfont,"#FFFFFF",self.x-35,self.y-1)
        else:
            drawtext(f"{self.hp}..",textfont,"#FFFFFF",self.x-35,self.y-1)
        
        if Lose == True:
            
            if self.fade <= 120:
                self.fade += 1
            s = pygame.Surface((1000,800))  # the size of your rect pengen beli teh poci deh
            s.set_alpha(35+self.fade)                # alpha level
            s.fill("#54453c")           # this fills the entire surface
            window.blit(s, (0,0))
            drawtext(f"YOU LOST!",overfont,"#FFFFFF",400,HEIGHT/2-150)
            drawtext(f"P\u0332r\u0332o\u0332g\u0332r\u0332e\u0332s\u0332s\u0332 \u0332D\u0332o\u0332n\u0332e\u0332",overfont,"#FFFFFF",350,HEIGHT/2-100)
            if int(xpbar.rat*100) < 10:
                drawtext(f"{int(xpbar.rat*100)}%",xpfont,"#FFFFFF",460,HEIGHT/2-35)
            elif int(xpbar.rat*100) == 100: drawtext(f"{int(xpbar.rat*100)}%",xpfont,"#FFFFFF",430,HEIGHT/2-35)
            else: drawtext(f"{int(xpbar.rat*100)}%",xpfont,"#FFFFFF",440,HEIGHT/2-35)
            drawtext(f"Press 0 to restart the game",endfont,"#FFFFFF",335,HEIGHT/2+90)
            drawtext(f"or ESC to quit the game",endfont,"#FFFFFF",365,HEIGHT/2+110)
        
        if Win == True:
            if self.fade <= 120:
                self.fade += 1
            s = pygame.Surface((1000,800))  # the size of your rect
            s.set_alpha(35+self.fade)                # alpha level
            s.fill("#54453c")           # this fills the entire surface
            window.blit(s, (0,0))
            drawtext(f"YOU WON!",overfont,"#FFFFFF",410,HEIGHT/2-150)
            drawtext(f"T\u0332i\u0332m\u0332e\u0332 \u0332T\u0332a\u0332k\u0332e\u0332n\u0332",overfont,"#FFFFFF",380,HEIGHT/2-100)
            minutes = seconds//60
            leftsec = seconds % 60
            if int(minutes) < 10 and leftsec < 10:
                drawtext(f"0{int(minutes)}:0{int(leftsec)}",xpfont,"#FFFFFF",375,HEIGHT/2-35)
            elif int(minutes) >= 10 and leftsec < 10:
                drawtext(f"{int(minutes)}:0{int(leftsec)}",xpfont,"#FFFFFF",375,HEIGHT/2-35)
            elif int(minutes) < 10 and leftsec >= 10:
                drawtext(f"0{int(minutes)}:{int(leftsec)}",xpfont,"#FFFFFF",375,HEIGHT/2-35)
            else: drawtext(f"{int(minutes)}:{int(leftsec)}",xpfont,"#FFFFFF",375,HEIGHT/2-35)
            drawtext(f"Press 0 to restart the game",endfont,"#FFFFFF",335,HEIGHT/2+90)
            drawtext(f"or ESC to quit the game",endfont,"#FFFFFF",365,HEIGHT/2+110)
        
        if self.effect == "Poison" and effect.true == True:
            s = pygame.Surface((1000,800))  # the size of your rect pengen beli teh poci deh
            s.set_alpha(65)                # alpha level
            s.fill("#5b3566")           # this fills the entire surface
            window.blit(s, (0,0))
        if self.effect == "Burn" and effect.true == True:
            s = pygame.Surface((1000,800))  # the size of your rect pengen beli teh poci deh
            s.set_alpha(65)                # alpha level
            s.fill("#e06734")           # this fills the entire surface
            window.blit(s, (0,0))
        if self.effect == "Regen" and effect.true == True:
            s = pygame.Surface((1000,800))  # the size of your rect pengen beli teh poci deh
            s.set_alpha(65)                # alpha level
            s.fill("#ef9df2")           # this fills the entire surface
            window.blit(s, (0,0))

    def draw(self,surface,Lose=False,Win=False):
        #ratio calculation
        rat = self.hp/self.max_hp
        regrat = 0
        if self.hp != 100 or self.hp <= 0:
            if self.hp > 90:
                regrat = (self.max_hp-self.hp)*2+(self.hp/self.max_hp)
            elif self.hp <= 0 or game_over == True:
                regrat = 0
                Lose = True
            else: regrat = 20+(self.hp/self.max_hp)
        
        if xpbar.rat == 1 or win_game == True:
            Win = True
        
        
        pygame.draw.rect(surface, "#473330",(self.x-40,self.y-5, self.w+10, self.h+10))
        pygame.draw.rect(surface, "#30211f",(self.x-3,self.y-3, self.w+6, self.h+6))
        if color.true == True:
            pygame.draw.rect(surface, "#a64746",(self.x,self.y, self.w, self.h))
            pygame.draw.rect(surface, "#FFBF00",(self.x,self.y, self.w*rat + regrat, self.h)) #regen hp
            if player.status == "Poison":
                pygame.draw.rect(surface, "#7b53a6",(self.x,self.y, self.w*rat, self.h)) #poison hp
                drawtext(f"! ! P O I S O N ! !",textfont,"#e0c5fc",self.x+20,self.y-1)
            elif player.status == "Regen":
                pygame.draw.rect(surface, "#e872c1",(self.x,self.y, self.w*rat, self.h)) #regen status hp
                drawtext(f"< 3 R E G E N < 3",textfont,"#823e6c",self.x+25,self.y-1)
            elif player.status == "Burn":
                pygame.draw.rect(surface, "#d95323",(self.x,self.y, self.w*rat, self.h)) #burn status hp
                drawtext(f"! ! B U R N ! !",textfont,"#f5d1c4",self.x+30,self.y-1)
            else:
                pygame.draw.rect(surface, "#5c9956",(self.x,self.y, self.w*rat, self.h)) #hp
        elif color.true == False:
            pygame.draw.rect(surface, "#453937",(self.x,self.y, self.w, self.h))
            if player.status == "Poison":
                pygame.draw.rect(surface, "#886aa8",(self.x,self.y, self.w*rat + regrat, self.h)) #regen hp
                pygame.draw.rect(surface, "#7b53a6",(self.x,self.y, self.w*rat, self.h)) #poison hp
            elif player.status == "Regen":
                pygame.draw.rect(surface, "#f2acdb",(self.x,self.y, self.w*rat + regrat, self.h)) #regen hp
                pygame.draw.rect(surface, "#e872c1",(self.x,self.y, self.w*rat, self.h)) #regen status hp
            elif player.status == "Burn":
                pygame.draw.rect(surface, "#f59a51",(self.x,self.y, self.w*rat + regrat, self.h)) #regen hp
                pygame.draw.rect(surface, "#f37e1f",(self.x,self.y, self.w*rat, self.h)) #burn status hp
            else:
                pygame.draw.rect(surface, "#7fc462",(self.x,self.y, self.w*rat + regrat, self.h)) #regen hp
                pygame.draw.rect(surface, "#68bc45",(self.x,self.y, self.w*rat, self.h)) #hp
        self.text(Lose,Win)
        self.newgame()

        # Colors #ffe78f yellow 5c9956 green #93de8c lime #a64746 red a14744 211f30 #fa7fcd
##########################/       \   [momen ketika lapar]
#########################<  - . -  > /
##########################\       /
class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_sprite_sheets('MainCharacters','NinjaFrog',32,32,True)
    ANIMATION_DELAY = 3

    def __init__(self,x,y,width,height):
        super().__init__()
        self.reset(x,y,width,height)
    
    def reset(self,x,y,width,height):
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
        self.iframe = 0
        self.regen = 30
        self.regenfps = 60
        self.name = "Player"
        self.status = "None"
        self.statcount = 0

    #movement
    def jump(self):
        self.y_vel = -self.GRAVITY*8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.count = 0

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def hurt(self):
        self.hit = True
        
    def loop(self,fps):
        
        if self.jump_count != 2:
            self.y_vel += min(1, (self.fall_count/fps)*self.GRAVITY)
        else:
            self.y_vel -= 0.4
            self.y_vel += min(1, (self.fall_count/fps)*self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        
        if self.hit:
            self.hit_count += 1
            self.regen = 30
        if self.hit_count > 90:
            self.hit = False
            self.hit_count = 0
            self.iframe = 0
        
        if self.regenfps >= 0:
            self.regenfps -= 1
            if self.status == "None":
                mainhealth.effect = "None"
        if self.regenfps == 0:
            self.regenfps += 60
            self.regen -= 1
            if self.status != "None":
                self.statcount += 1
            if (self.status == "Poison" or self.status == "Burn") and mainhealth.hp >0:
                mainhealth.health(-1)
                if self.status == "Burn":
                    mainhealth.effect = "Burn"
                if self.status == "Poison":
                    mainhealth.effect = "Poison"
            if self.status == "Regen" and mainhealth.hp <98:
                mainhealth.health(3)
                mainhealth.effect = "Regen"
            if self.status == "Regen" and mainhealth.hp >=98:
                mainhealth.health(mainhealth.max_hp-mainhealth.hp)
                mainhealth.effect = "Regen"


        if self.status != "None" and self.statcount == 5:
        
            if self.status == "Poison":
                mainhealth.health(-5)
            self.status = "None"
            self.statcount = 0
            
        elif self.status == "None" and self.statcount == 1:
            self.statcount = 0

        if self.regen == 0 and mainhealth.hp > 90 and mainhealth.hp <= 100 and mainhealth.hp > 0:
            self.regen = 30
            healthval = 100 - mainhealth.hp
            mainhealth.health(healthval)
        elif self.regen == 0 and mainhealth.hp <= 100 and mainhealth.hp > 0:
            self.regen = 30
            mainhealth.health(10)

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
        sprite_sheet = 'idle'
        if self.hit:
            sprite_sheet = 'hit'
        elif self.y_vel < 0:
            if self.jump_count == 2:
                sprite_sheet = 'double_jump'
            elif self.jump_count == 1:
                sprite_sheet = 'jump'
            # if self.jump_count == 2:
            #     sprite_sheet = 'double_jump'
        elif self.y_vel > self.GRAVITY*2:
            sprite_sheet =  'fall'
        elif self.x_vel != 0:
            sprite_sheet = 'run'

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

def handle_vert_col(player,objects,dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            if dy > 0: #collide bottom
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0: #collide top
                if not obj.name == "Platform":
                    player.rect.top = obj.rect.bottom
                    player.hit_head()
            elif dy == 0: pass
        
            collided_objects.append(obj)
    return collided_objects
            
def collision(player,objects,dx):
    player.move(dx,0)
    player.update()
    collided_object = None
    for obj in (objects):
        if pygame.sprite.collide_mask(player,obj):
            collided_object = obj
            break
    
    player.move(-dx,0)
    player.update()
    return collided_object

def frcollision(player,objects):
    collided_object = None
    if pygame.sprite.collide_mask(player,objects):
        collided_object = objects

    return collided_object

def frhandle_vert_col(player,objects,dy):
    collided_objects = []
    if pygame.sprite.collide_mask(player,objects):
        collided_objects.append(objects)
    return collided_objects

def enemy_move_handling(enemy,objects):
    enemy.x_vel = 0
    collide_left = collision(enemy,objects, -PLAYER_VEL*2)
    collide_right = collision(enemy,objects, PLAYER_VEL*2)
    enemy.y += 1
    if enemy.y >= 180:
        enemy.y = 0
        if enemy.x == 1:
            enemy.x -= 1
        elif enemy.x != 1:
            enemy.x += 1
    elif enemy.name != "Mushroom":
        if enemy.x == 0 and enemy.y >= 0 and not collide_right:
            enemy.move_right(enemy.speed)
        elif enemy.x == 1 and enemy.y >= 0 and not collide_left:
            enemy.move_left(enemy.speed)
    elif enemy.name == "Mushroom":
        if enemy.x == 0 and enemy.y >= 0 and not collide_left:
            enemy.move_left(enemy.speed)
        elif enemy.x == 1 and enemy.y >= 0 and not collide_right:
            enemy.move_right(enemy.speed)
    vertical_collide = handle_vert_col(enemy,objects,enemy.y_vel)
    to_check = [collide_left,collide_right,*vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            enemy.hurt()
            if enemy.iframe != 1:
                enemy.iframe = 1

def fruit_collision(fruit,player):
    collide_left = frcollision(fruit,player)
    collide_right = frcollision(fruit,player)
    vertical_collide = frhandle_vert_col(fruit,player,0)
    to_check = [collide_left,collide_right,*vertical_collide]
    for obj in to_check:
        if obj and obj.name == "Player":
            if fruit.life == 1:
                xpbar.experience(1)
                if fruit.name != "Melon" and  mainhealth.hp < 99:
                    mainhealth.health(1)
                elif fruit.name == "Melon":
                    mainhealth.health(0)
                    player.status = "Regen"
                    player.statcount = 0

            fruit.suicide()
                
            
def move_handling(player,objects,enemy):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collision(player,objects, -PLAYER_VEL-6)
    collide_right = collision(player,objects, PLAYER_VEL+6)
    ecollide_left = collision(player,enemy, -PLAYER_VEL*2)
    ecollide_right = collision(player,enemy, PLAYER_VEL*2)
    if player.status != "Poison":
        if keys[pygame.K_a] and not collide_left:
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_d] and not collide_right:
            player.move_right(PLAYER_VEL)
    elif player.status == "Poison":
        if keys[pygame.K_a] and not collide_left:
            player.move_left(PLAYER_VEL-0.5)
        if keys[pygame.K_d] and not collide_right:
            player.move_right(PLAYER_VEL-0.5)
    vertical_collide = handle_vert_col(player,objects,player.y_vel)
    to_check = [collide_left,collide_right,*vertical_collide,ecollide_left,ecollide_right]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.hurt()
            if player.iframe != 1:
                hurtsound.play()
                player.status = "Burn"
                mainhealth.health(-10)
                player.statcount = 0
                player.iframe = 1
        elif obj and obj.name == "Rino":
            player.hurt()
            if player.iframe != 1:
                hurtsound.play()
                mainhealth.health(-25)
                player.iframe = 1
        elif obj and obj.name == "Radish":
            player.hurt()
            if player.iframe != 1:
                hurtsound.play()
                mainhealth.health(-20)
                player.iframe = 1
        elif obj and obj.name == "Spikes":
            player.hurt()
            if player.iframe != 1:
                hurtsound.play()
                mainhealth.health(-5)
                player.iframe = 1
        elif obj and obj.name == "Mushroom":
            player.hurt()
            if player.iframe != 1:
                hurtsound.play()
                player.status = "Poison"
                player.statcount = 0
                mainhealth.health(-10)
                player.iframe = 1

def drawtext(text,font,color,x,y,GO=False):
    img = font.render(text,True,color)
    window.blit(img,(x,y))

def find_background(color):
    image = pygame.image.load(join('Assets','Background',color))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image

def draw(window, background, bg_image,player,objects,offsetx,health,enemy,fruits,xpbar,color,effect):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offsetx)

    for f in fruits:
        if f.life >= -30:
            f.draw(window,offsetx)

    for e in enemy:
        e.draw(window, offsetx)

    player.draw(window,offsetx)
    xpbar.draw(window)
    color.draw(window)
    effect.draw(window)
    health.draw(window)
    pygame.display.update()

def main(window):
    global effect
    global color
    global win_game
    global seconds
    global game_over
    global mainhealth
    global player
    global xpbar
    pygame.mixer.init()
    # pygame.display.init()
    # pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    background, bg_image = find_background(resource_path('Assets/Background/Brown.png'))
    fields = pygame.mixer.Sound(resource_path("Assets/fields.mp3"))
    fields.play(-1)
    fields.set_volume(1)
    block_size = 96

    second = 0
    seconds = 0
    

    #WALKING ENEMIES
    mush = [enemies.Mushroom(-100,300,32,32),enemies.Mushroom(-6*block_size,HEIGHT-block_size*(7),32,32),enemies.Mushroom(8*block_size+48,HEIGHT-60-block_size*2,32,32),enemies.Mushroom(4*block_size+96,HEIGHT-60-block_size*2,32,32)]
    radish = [enemies.Radish(-100,600,30,38),enemies.Radish(10*block_size,HEIGHT-60-block_size*5,52,34)]
    rino = [enemies.Rino(4*block_size,HEIGHT-60-block_size*2,52,34),enemies.Rino(5*block_size,HEIGHT-60-block_size*7,52,34)]

    #FRUITS
    apple = [enemies.Apple(block_size*2+32,HEIGHT-block_size*3+32,32,32),enemies.Apple(block_size*2-32,HEIGHT-block_size*3-16,32,32),enemies.Apple(block_size*13-32-32,HEIGHT-block_size*8+32,32,32),enemies.Apple(block_size*13,HEIGHT-block_size*2,32,32),enemies.Apple(-128,block_size*2+64,32,32),enemies.Apple(9*block_size+16,HEIGHT-60-block_size*6-32,32,32),enemies.Apple(9*block_size+32,HEIGHT-60-block_size*6,32,32),enemies.Apple(9*block_size,HEIGHT-60-block_size*6,32,32),enemies.Apple(-block_size*2,HEIGHT-block_size*4+40,32,32),enemies.Apple(-block_size,HEIGHT-block_size*4+40,32,32),enemies.Apple(-block_size*2+30,HEIGHT-block_size*4+40,32,32),enemies.Apple(-block_size+30,HEIGHT-block_size*4+40,32,32),enemies.Apple(7*block_size-32,HEIGHT-block_size*(6),32,32)]
    cherry = [enemies.Cherry(block_size*13-32+32,HEIGHT-block_size*8+32,32,32),enemies.Cherry(9*block_size,HEIGHT-60-16-block_size*4,32,32),enemies.Cherry(9*block_size+32,HEIGHT-60-16-block_size*4,32,32),enemies.Cherry(-128,block_size*2-64,32,32), enemies.Cherry(-128+64,block_size*2,32,32), enemies.Cherry(-128-64,block_size*2,32,32),
              enemies.Cherry(3*block_size,200-64,32,32),enemies.Cherry(5*block_size-64,200-64,32,32),enemies.Cherry(-500,600,32,32),enemies.Cherry(-540,600,32,32),enemies.Cherry(-580,600,32,32),enemies.Cherry(6*block_size+16,HEIGHT-block_size*(6)-32,32,32),enemies.Cherry(7*block_size-16+32,HEIGHT-block_size*(6)-32,32,32)]
    orange = [enemies.Orange(block_size*3-32,HEIGHT-block_size*3,32,32),enemies.Orange(block_size*3+32,HEIGHT-block_size*3+32,32,32),enemies.Orange(block_size*13-32,HEIGHT-block_size*8+64,32,32),*(enemies.Orange((i+6)*(block_size)+16,HEIGHT-block_size*2-60,32,32) for i in range(2)),enemies.Orange(-520,HEIGHT-block_size*(6)-30,32,32),enemies.Orange(-540,HEIGHT-block_size*(6),32,32),enemies.Orange(-500,HEIGHT-block_size*(6),32,32),enemies.Orange(6*block_size,HEIGHT-block_size*(6),32,32),enemies.Orange(7*block_size+32,HEIGHT-block_size*(6),32,32)]
    melon = [enemies.Melon(block_size*13-32,HEIGHT-block_size*8,32,32),enemies.Melon(-4*block_size+16,HEIGHT-block_size*8+32,32,32),enemies.Melon(9*block_size+16,HEIGHT-60-48-block_size*4,32,32),enemies.Melon(3*block_size+32+32,HEIGHT-60-32-block_size*5,32,32)]
    #TRAPS
    fire = [Fire(100,HEIGHT-block_size-64,16,32),*(Fire(((12)*block_size+(i*32)),HEIGHT-14-block_size*4,16,32) for i in range (2))]
    for f in fire:
        f.on()
    spike = [enemies.Spikes(-block_size*4,HEIGHT-block_size-32,16,20),*(enemies.Spikes((-block_size*4-32)+(i*32),HEIGHT-block_size*4-32,16,20) for i in range (5)),
             enemies.Spikes((-block_size*6),HEIGHT-block_size*4-32,16,20),*(enemies.Spikes((block_size*9-32)+(i*32),HEIGHT-block_size*4-32,16,20) for i in range (3)),
            *(enemies.Spikes((block_size*10-32)+(i*32),HEIGHT-block_size*1-32,16,20) for i in range (3)),*(enemies.Spikes((block_size*12-32)+(i*32),HEIGHT-block_size*1-32,16,20) for i in range (3))]
    #BLOCKS
    wall = [Wall(block_size*14,HEIGHT-block_size*(i),block_size) for i in range(10)]
    wall2 = [Wall(block_size*-7,HEIGHT-block_size*(i),block_size) for i in range(10)]
    floor = [Block(i*block_size,HEIGHT-block_size,block_size) for i in range((-WIDTH+400)//block_size,(WIDTH+400)//block_size)]
    floor2 = [Wall(i*block_size,HEIGHT-block_size+40,block_size) for i in range((-WIDTH+400)//block_size,(WIDTH+400)//block_size)]
    plat = [Platform(96, 200, block_size),Platform(-block_size*2,HEIGHT-block_size*4+20,block_size),Platform(-block_size,HEIGHT-block_size*4+20,block_size),
           *(Platform((6+i)*block_size,HEIGHT-block_size*(7),block_size) for i in range(2)), (Platform((9)*block_size,HEIGHT-block_size*(7),block_size)),
            Platform(-6*block_size,HEIGHT-block_size*(7)+30,block_size),Platform(-5*block_size,HEIGHT-block_size*(7)+30,block_size)]
    
    #MISC
    xpbar = ProgressBar(50,70,200,18,40)
    mainhealth = HealthBar(50,30,200,18,100)
    color = Color(WIDTH-65,HEIGHT-68,21,22,False)
    effect = Effect(WIDTH-115,HEIGHT-68,21,22,False)
    
    ceiling = [Wall(i*block_size,-80,block_size) for i in range((-WIDTH+400)//block_size,(WIDTH+400)//block_size)]
    player = Player(96,100,50,50)

    enemy = [*rino,*radish,*mush]
    objects = [*spike,*ceiling,*floor,*floor2,
               *(Block(((i+9)*block_size),HEIGHT-block_size*4,block_size) for i in range(3)), *(Wall(((i+9)*block_size),HEIGHT+50-block_size*4,block_size) for i in range(4)),
               *(Wall((10+i)*block_size,HEIGHT-block_size*(7),block_size) for i in range(2)), *(Wall((11)*block_size,HEIGHT-block_size*(8+i),block_size) for i in range(2)),
               *(Wall(5*block_size,HEIGHT-block_size*(4+i),block_size) for i in range(4)), *(Wall(8*block_size,HEIGHT-block_size*(4+i),block_size) for i in range(4)),
               *(Wall(2*block_size,HEIGHT-block_size*(5+i),block_size) for i in range(3)), *(Block((3+i)*block_size,HEIGHT-block_size*(5),block_size) for i in range(2)), *(Wall((3+i)*block_size,HEIGHT-block_size*(5)+50,block_size) for i in range(2)),
               *(Wall(-4*block_size,HEIGHT-block_size*(6+i),block_size) for i in range(2)), Wall(-4*block_size,HEIGHT-block_size*(9),block_size), Wall(2*block_size,HEIGHT-block_size*(9),block_size),
               *(Block(-((i+3)*block_size),HEIGHT-block_size*4,block_size) for i in range(4)),
               *(Wall(-((i+3)*block_size),HEIGHT+30-block_size*4,block_size) for i in range(2)), *(Wall(-((i+5)*block_size),HEIGHT+60-block_size*4,block_size) for i in range(2)),
               Block(0,HEIGHT-block_size*4,block_size),*(Block((i+4)*(block_size),HEIGHT+40-block_size*2,block_size) for i in range(6)),*fire,*wall,*wall2,*plat]
    fruits = [*apple,*cherry,*orange,*melon]
    offsetx = 0
    scroll_area_width = 200
    
    #JANGAN LUPA MASUKIN LOOP KALO ENTITY BARU!!!! pls gw cpk bgt
    win_game = False
    game_over = False
    run = True
    restart = False
    while run:
        clock.tick(FPS)
        if second >= 60:
            seconds += 1
            second = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT and restart == False:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_0 and (game_over == True or win_game == True):
                    pygame.mixer.quit()
                    restart = True
                    run = False
                    main(window)
                
                if event.key == pygame.K_ESCAPE and (game_over == True or win_game == True):
                    run = False
                    restart = False
                    pygame.quit()
                    pygame.mixer.quit()
                    sys.exit()  

                if event.key == pygame.K_i:
                    win_game = True
                if event.key == pygame.K_u:
                    mainhealth.hp = -999

        if game_over == False and win_game == False:
            color.loop()
            effect.loop()
            second += 1
            player.loop(FPS)
            for f in fire:    
                f.loop()
            for en in enemy:
                en.loop(FPS)
                enemy_move_handling(en,objects)
            move_handling(player,objects,enemy)
            for f in fruits:
                fruit_collision(f,player)
                f.loop()
                #scrolling bg    
            if ((player.rect.right - offsetx -110 >= WIDTH - scroll_area_width) and player.x_vel > 0 ) or (
                (player.rect.left - offsetx +110<= scroll_area_width) and player.x_vel < 0 ):
                offsetx += player.x_vel
        elif game_over == True and win_game == False: 
            player.loop(FPS)


        draw(window,background,bg_image,player,objects,offsetx,mainhealth,enemy,fruits,xpbar,color,effect)

        #win
        if xpbar.rat == 1:
            win_game = True

        #fall bug or mainhealth.hp <= 0
        if player.rect.top > HEIGHT or mainhealth.hp <= 0 or player.rect.bottom < 0:
            game_over = True
            
        
    pygame.quit()

if __name__ == "__main__":
    main(window)