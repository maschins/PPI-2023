####Libraries###
import pygame
import random
import math

####Constant####
WINDOW_LENGHT = 800
WINDOW_HEIGHT = 600

####General variables####
last_time = 0

####Game variables####
sun = 0
score = 0

entities = []

####Functions####
def inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
            
def exit_game():
    pygame.display.quit()
    pygame.quit()
    exit()

def logic(dt):
    global last_time
    inputs()
    if dt < 20:
        return
    last_time = pygame.time.get_ticks()
    
    
def new_entity(entity_type, position = [0,0]): #TODO SPRITES
    match entity_type:
        case 'sunflower':
            return new_entity_data('sunflower', position, 100, 0, 25, 3000, 50, {})
        case 'bean_shooter':
            return new_entity_data('bean_shooter', position, 100, 0, 20, 1000, 100, {})
        case 'nut':
            return new_entity_data('nut', position, 500, 0, 0, 0, 100, {})
        case 'zombie':
            return new_entity_data('zombie', position, 100, 20, 10, 1000, 100, {})
        case 'zombie_tank':
            return new_entity_data('zombie_tank', position, 100, 10, 20, 1000, 100, {})
        case 'zobmie_runner':
            return new_entity_data('zobmie_runner', position, 100, 40, 20, 1000, 100, {})
        
def new_entity_data(type, position, health, speed, damage, attack_delay, value, sprite):
    return {
        'type': type,
        'position': position,
        'health': health,
        'speed': speed,
        'damage': damage,
        'attack_delay': attack_delay,
        'value': value,
        'sprite': sprite
    }
            
def render():
    pygame.display.flip()

####Init####

pygame.init()

window = pygame.display.set_mode((WINDOW_LENGHT, WINDOW_HEIGHT))
pygame.display.set_caption('Plants VS Zombies')

running = True
inGame = False

####Game Loop####
while running:
    pygame.time.Clock().tick()
    delta_time = pygame.time.get_ticks() - last_time
    logic(delta_time)
    render()

exit_game()
