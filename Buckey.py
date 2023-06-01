import pygame
import random
import os
import math
import time
from os import listdir
from os.path import isfile, join
#from Controller import readSerial


pygame.init()

pygame.display.set_caption("BuckShot")

WIDTH, HEIGHT = 500, 600
FPS = 60
PLAYER_VEL = 7

window = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    
    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
            all_sprites[image.replace(".png", "")] = sprites
            
    return all_sprites


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 0.1
    SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 3
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.bullet_count = 3
        self.hit = False
        self.hit_count = 0
        self.start_time = time.time()
        self.angle = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0  

    def shoot(self):
        mouse_pos = pygame.mouse.get_pos()
        player_pos = [self.rect.x - self.rect.width // 2, self.rect.y - self.rect.height // 2]

        DeltaX = mouse_pos[0] - player_pos[0]
        DeltaY = player_pos[1] - mouse_pos[1]

        angle = math.degrees(math.atan2(DeltaY, DeltaX))
        self.angle = angle
        
        self.x_vel = PLAYER_VEL * math.cos(math.radians(angle))
        self.y_vel = -PLAYER_VEL * math.sin(math.radians(angle))
        
        self.bullet_count -= 1

        #print(PLAYER_VEL * math.cos(math.radians(angle)), PLAYER_VEL * math.sin(math.radians(angle)) * -1, angle, self.rect.x, player_pos)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def loop(self, fps):
        self.y_vel += min(self.GRAVITY, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()
        #readSerial()

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        
        sprite_sheet_name = sprite_sheet
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))


class Shotgun(pygame.sprite.Sprite):
    SPRITE = pygame.image.load(join("assets", "Items", "Guns", "shotgun.png")).convert_alpha()

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.SPRITE = pygame.transform.scale(self.SPRITE, (width, height))
        self.angle = 0
    
    def loop(self, player_rect, offset_x, offset_y):
        self.rect.x = player_rect.x + offset_x
        self.rect.y = player_rect.y + offset_y
        #print(self.rect.x, self.rect.y, player_rect.x, player_rect.y)
    
    def rotate_sprite(self, angle):
        self.SPRITE = pygame.transform.rotate(self.SPRITE, angle - self.angle)
        self.angle = angle

    def draw(self, win):
        win.blit(self.SPRITE, (self.rect.x, self.rect.y))


class Bullet():
    SPRITE = pygame.image.load(join("assets", "Items", "Bullet", "Bullet.png")).convert_alpha()

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.SPRITE = pygame.transform.scale(self.SPRITE, (width, height))
    
    def handle_bullets(self, bullet_amount, bullet_size, player, bullet, bullets):
        
        if len(bullets) < bullet_amount:
            for i in range(bullet_amount):
                bullet_x = random.randint(0, WIDTH)
                bullet_y = random.randint(0, HEIGHT)
            
                distance_ok = all(math.sqrt((bullet_x - bullet.rect.x)**2 + (bullet_y - bullet.rect.y)**2) > 20 for bullet in bullets)
            
                if distance_ok:
                    bullets.append(Bullet(bullet_x, bullet_y, bullet_size, bullet_size))
                    
        bullets_to_remove = []
        for bullet in bullets:
            if bullet.rect.colliderect(player.rect):
                bullets_to_remove.append(bullet)
        for bullet in bullets_to_remove:
            bullets.remove(bullet)
            player.bullet_count += 1
            handle_score()
        
        
        return bullets
            
    def draw(self, win):
        win.blit(self.SPRITE, (self.rect))
        

def handle_border(player):
    if player.rect.x > WIDTH:
        player.rect.x = 0
        
    if player.rect.x < 0:
        player.rect.x = WIDTH
        

def handle_score():
    global score
    score += 1
    


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    
    return tiles, image
        
        
def draw(window, background, bg_image, player, shotgun, bullets):
    for tile in background:
        window.blit(bg_image, tile)
        
    for Bullet in bullets:
        Bullet.draw(window)

    player.draw(window)
    shotgun.draw(window)
    
    score_text = font.render(f"Score: {str(score)}", True, (255, 255, 255))
    text_rect = score_text.get_rect(topright = (WIDTH - 10, 10))
    window.blit(score_text, text_rect)
    
    pygame.display.update()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    offset_x, offset_y = 25, 22
    bullet_size = 40
    bullet_amount = 2
    global score
    score = 0
    
    player = Player(100, 100, 50, 50)
    shotgun = Shotgun(player.rect.x, player.rect.y, 50, 50)
    bullet = Bullet(200, 200, 40, 40)
    bullets = []
    

    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.bullet_count > 0 or event.key == pygame.K_UP and player.bullet_count > 0:
                    #player.jump()
                    player.shoot()
        
        player.loop(FPS)
        shotgun.loop(player.rect, offset_x, offset_y)
        handle_border(player)
        bullets = bullet.handle_bullets(bullet_amount, bullet_size, player, bullet, bullets)
        #shotgun.rotate_sprite(player.angle)
        draw(window, background, bg_image, player, shotgun, bullets)
        #print(f"score: {score}")
        
        
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)