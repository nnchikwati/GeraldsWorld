# NGONIDZASHE NIGEL CHIKWATI
import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Geralds World")

# define font
font_score = pygame.font.SysFont('Bauhaus 93', 30)
font = pygame.font.SysFont('Bauhaus 93', 75)

# define colours
white = (255, 255, 255)
purple = (128, 0, 128)

# game variables
tile_size = 50
game_over = 0
main_menu = True
level = 0
max_levels = 7
score = 0
# load images

sun_img = pygame.image.load("sun.png")
sky_img = pygame.image.load("city2.jpg")
restart_img = pygame.image.load("reset.png")
start_img = pygame.image.load('start_btn.png')
exit_img = pygame.image.load('exit_btn.png')

# load sounds
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
gold_fx = pygame.mixer.Sound('gold.wav')
gold_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('game_over.wav')
game_over_fx.set_volume(0.5)


def screen_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function to reset level
def reset_level(level):
    player.reset(100, screen_height - 130)
    blob_group.empty()
    platform_group.empty()
    water_group.empty()
    exit_group.empty()

    # load in level data  to create World
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class World():
    def __init__(self, data):
        self.tile_list = []
        # load images
        block_img = pygame.image.load('iron.png')
        shroom_img = pygame.image.load('grass2.png')
        door_img = pygame.image.load('door.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect()  # creates rectangle from size of img
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 2:
                    img = pygame.transform.scale(shroom_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Villain(col_count * tile_size, row_count * tile_size - 10)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    water = Water(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    water_group.add(water)
                if tile == 7:
                    gold = Gold(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    gold_group.add(gold)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size)
                    exit_group.add(exit)

                col_count += 1
            row_count += 1

            col_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Villain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("blob.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("block.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("iceWaterDeep.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Gold(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("gold.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("door.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):

        dx = 0
        dy = 0
        move_slowdown = 5
        col_thresh = 20
        # get key presses
        key = pygame.key.get_pressed()

        if game_over == 0:

            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True

            if key[pygame.K_SPACE] == False:
                self.jumped = False

            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Animation
            if self.counter > move_slowdown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Collision check
            self.in_air = True
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if above the ground(Jumping)
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # Check is above the ground(falling)
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
            # check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()

            # check for collision with water
            if pygame.sprite.spritecollide(self, water_group, False):
                game_over = -1
                game_over_fx.play()

            # check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # check for collsion with platform
            for platform in platform_group:
                #collison in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collision in the y direction
                if platform.rect.colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                    #check if below the platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh :
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #check if above platform
                    elif abs((self.rect.bottom + dy)- platform.rect.top < col_thresh):
                        self.rect.bottom = platform.rect.top
                        dy = platform.rect.top - 1
                        dy = 0
                        self.in_air = False
                    # move with different platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction


            # Update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            screen_text('GAME OVER', font, purple, (screen_width // 2) - 200, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player
        screen.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('ghost_dead.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self._air = True


player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
gold_group = pygame.sprite.Group()

score_gold = Gold(tile_size // 2, tile_size // 2)
gold_group.add(score_gold)

# load in level data  to create World
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

# create buttons

start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
run = True
while run:

    clock.tick(fps)
    screen.blit(sky_img, (0, 0))
    screen.blit(sun_img, (100, 50))

    if main_menu == True:

        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:

        world.draw()

        if game_over == 0:
            blob_group.update()
            platform_group.update()

            # update score
            # check if a coin has been collected
            if pygame.sprite.spritecollide(player, gold_group, True):
                score += 1
                gold_fx.play()
            screen_text('' + str(score), font_score, white, tile_size - 10, 10)
        blob_group.update()
        blob_group.draw(screen)
        platform_group.draw(screen)
        water_group.draw(screen)
        gold_group.draw(screen)
        exit_group.draw(screen)
        game_over = player.update(game_over)

        # If player died
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0

        # if player has completed the level
        if game_over == 1:
            # reset game  and go to next level
            level += 1
            if level <= max_levels:
                # reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
                pass
            else:
                # restart game
                screen_text('You are Victorious', font, purple, (screen_width // 2) - 300, screen_height // 2)
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
