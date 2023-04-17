import pygame
from sys import exit
from random import randint, choice


# Cat-players' functions and possible actions
class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        cat_walk_1 = pygame.image.load("graphics/player/cat_walk_1.png").convert_alpha()
        cat_walk_1 = pygame.transform.flip(cat_walk_1, True, False)
        cat_walk_1 = pygame.transform.scale(cat_walk_1, (100, 85))

        cat_walk_2 = pygame.image.load("graphics/player/cat_walk_2.png").convert_alpha()
        cat_walk_2 = pygame.transform.flip(cat_walk_2, True, False)
        cat_walk_2 = pygame.transform.scale(cat_walk_2, (100, 85))

        self.cat_walk = [cat_walk_1, cat_walk_2]
        self.cat_index = 0
        self.cat_jump = pygame.image.load("graphics/player/cat_walk_2.png").convert_alpha()
        self.cat_jump = pygame.transform.flip(cat_walk_2, True, False)
        self.cat_jump = pygame.transform.scale(cat_walk_2, (100, 85))

        self.image = self.cat_walk[self.cat_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

    def cat_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_change(self):
        if self.rect.bottom < 300:
            self.image = self.cat_jump
        else:
            self.cat_index += 0.1
            if self.cat_index >= len(self.cat_walk):
                self.cat_index = 0
            self.image = self.cat_walk[int(self.cat_index)]

    def update(self):
        self.cat_input()
        self.apply_gravity()
        self.animation_change()


# Obstacle functions and actions(combined)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "wasp":
            wasp1 = pygame.image.load("graphics/wasp/wasp1.png").convert_alpha()
            wasp2 = pygame.image.load("graphics/wasp/wasp2.png").convert_alpha()
            self.frames = [wasp1, wasp2]
            y_pos = 210
        else:
            mouse1 = pygame.image.load("graphics/mouse/mouse1.png").convert_alpha()
            mouse2 = pygame.image.load("graphics/mouse/mouse2.png").convert_alpha()
            self.frames = [mouse1, mouse2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# Score system
def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = test_font.render(f"Score: {current_time}", True, "#07755c")
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


# Checks if the collision happened or not
def collision_sprite():
    if pygame.sprite.spritecollide(cat.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
icon = pygame.image.load("graphics/intro/cat_sleep.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("Cat Sprint")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/SpaceMission-rgyw9.otf", 50)
game_active = False
start_time = 0
score = 0

# Groups
cat = pygame.sprite.GroupSingle()
cat.add(Cat())

obstacle_group = pygame.sprite.Group()
# Background
sky_surface = pygame.image.load("graphics/sky.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

# Intro/Outro cat
cat_laying = pygame.image.load("graphics/intro/cat_sleep.png").convert_alpha()
cat_laying = pygame.transform.scale(cat_laying, (400, 300))
cat_laying_rect = cat_laying.get_rect(center=(400, 200))
# Game name
game_name = test_font.render("Cat Sprint", True, "#07755c")
game_name_rect = game_name.get_rect(center=(400, 50))
# Game space to start message
game_message = test_font.render("Press space to start", True, "#07755c")
game_message_rect = game_message.get_rect(center=(400, 350))
# Game over message
game_over = test_font.render("Game Over:(", True, "#07755c")
game_over_rect = game_name.get_rect(center=(400, 50))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["wasp", "mouse", "wasp", "mouse"])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        cat.draw(screen)
        cat.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill("#4cb59d")
        screen.blit(cat_laying, cat_laying_rect)

        score_message = test_font.render(f"Your score: {score}", True, "#07755c")
        score_message_rect = score_message.get_rect(center=(400, 350))

        if score == 0:
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(game_over, game_over_rect)

    pygame.display.update()
    clock.tick(60)
