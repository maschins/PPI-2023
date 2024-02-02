# Heroes VS Monsters
# Fraiponts Thomas, Pierret Alexandre, Schins Martin

import pygame
import random

GAME_NAME = "Heroes vs Monsters"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

TERRAIN_WIDTH = 8
TERRAIN_HEIGHT = 6
TERRAIN_MIN_SPACE = 64
SHOP_CELL_SIZE = 96

HIT_DURATION = 100
BASE_MANA = 500
WAVE_DELAY = 7500

WAVE_SPAWN_COOLDOWN = 5000
WAVE_SPAWN_MIN_COOLDOWN = 750
WAVE_SPAWN_REDUCTION_FACTOR = 0.9

RESOURCES = {
    "font": "resources/fonts/Minecraft.ttf",
    "sprites": {
        "ground": "resources/sprites/ground.png",
        "cracked_ground": "resources/sprites/cracked_ground.png",
        "trash": "resources/sprites/trash.png",
        "mana_potion": "resources/sprites/mana_potion.png",
        "hero_mage": "resources/sprites/hero_mage.png",
        "hero_elf": "resources/sprites/hero_elf.png",
        "hero_knight": "resources/sprites/hero_knight.png",
        "hero_doc": "resources/sprites/hero_doc.png",
        "shop_tag": "resources/sprites/shop_tag.png"
    },
    "menu_background": "resources/sprites/menu.png",
    "game_background": "resources/sprites/background.png",
    "music": {
        "location": "resources/sounds/bg_music.wav",
        "volume": 0.03

    },
    "states": {
        "MAIN_MENU": 0,
        "IN_GAME": 1,
        "PAUSE": 2,
        "GAME_OVER": 3,
        "CREDITS": 4
    },
    "entities": {
        "hero_mage": {
            "health": 100,
            "speed": 0,
            "action_value": 25,
            "action_delay": 2500,
            "value": 50,
            "damageable": True,
            "animations": {
                "idle": {
                    "location": "resources/sprites/hero_mage_idle.png",
                    "width": 16,
                    "height": 28,
                    "ratio": (1, 1),
                    "flip": False,
                    "delay": 100
                }
            },
            "sounds": {
                "hit": {
                    "location": "resources/sounds/mage_hit.wav",
                    "volume": 0.5
                }
            }
        },
        "hero_elf": {
            "health": 150,
            "speed": 0,
            "action_value": 0,
            "action_delay": 5000,
            "value": 100,
            "damageable": True,
            "animations": {
                "idle": {
                    "location": "resources/sprites/hero_elf_idle.png",
                    "width": 16,
                    "height": 28,
                    "ratio": (1, 1),
                    "flip": False,
                    "delay": 100
                }
            },
            "sounds": {
                "hit": {
                    "location": "resources/sounds/elf_hit.wav",
                    "volume": 0.5
                }
            }
        },
        "hero_knight": {
            "health": 500,
            "speed": 0,
            "action_value": 0.3333,
            "action_delay": 20000,
            "value": 300,
            "damageable": True,
            "animations": {
                "idle": {
                    "location": "resources/sprites/hero_knight_idle.png",
                    "width": 16,
                    "height": 28,
                    "ratio": (1, 1),
                    "flip": False,
                    "delay": 100
                }
            },
            "sounds": {
                "hit": {
                    "location": "resources/sounds/knight_hit.wav",
                    "volume": 0.5
                }
            }
        },
        "hero_doc": {
            "health": 100,
            "speed": 0,
            "action_value": 0.15,
            "action_delay": 5000,
            "value": 250,
            "damageable": True,
            "animations": {
                "idle": {
                    "location": "resources/sprites/hero_doc_idle.png",
                    "width": 16,
                    "height": 23,
                    "ratio": (1, 1),
                    "flip": False,
                    "delay": 100
                }
            },
            "sounds": {
                "hit": {
                    "location": "resources/sounds/doc_hit.wav",
                    "volume": 0.5
                },
                "heal0": {
                    "location": "resources/sounds/doc_heal_1.ogg",
                    "volume": 0.5
                },
                "heal1": {
                    "location": "resources/sounds/doc_heal_2.ogg",
                    "volume": 0.5
                },
                "heal2": {
                    "location": "resources/sounds/doc_heal_3.ogg",
                    "volume": 0.5
                }
            }
        },
        "elf_arrow": {
            "health": 1,
            "speed": -0.1,
            "action_value": 15,
            "action_delay": 0,
            "value": 0,
            "damageable": False,
            "animations": {
                "exist": {
                    "location": "resources/sprites/arrow.png",
                    "width": 21,
                    "height": 7,
                    "ratio": (0.7, 0.3),
                    "flip": False,
                    "delay": 100
                }
            },
            "sounds": {

            }
        },
        'mower': {
            "health": 1,
            "speed": 0,
            "action_value": 0,
            "action_delay": 0,
            "value": 0,
            "damageable": False,
            "animations": {
                "idle": {
                    "location": "resources/sprites/tondeuse_idle.png",
                    "width": 32,
                    "height": 32,
                    "ratio": (1, 1),
                    "flip": False,
                    "delay": 100
                },
                "run": {
                    "location": "resources/sprites/tondeuse_run.png",
                    "width": 32,
                    "height": 32,
                    "ratio": (1, 1),
                    "flip": False,
                    "delay": 100
                }
            },
            "sounds": {

            }
        },
        "monster_goblin": {
            "health": 500,
            "speed": 0.01,
            "action_value": 15,
            "action_delay": 1250,
            "value": 3,
            "damageable": True,
            "animations": {
                "run": {
                    "location": "resources/sprites/goblin_run.png",
                    "width": 16,
                    "height": 16,
                    "ratio": (1, 1),
                    "flip": True,
                    "delay": 100
                }
            },
            "sounds": {
                "hit": {
                    "location": "resources/sounds/goblin_hit.wav",
                    "volume": 0.5
                }
            }
        },
        "monster_demon": {
            "health": 300,
            "speed": 0.015,
            "action_value": 5,
            "action_delay": 750,
            "value": 1.5,
            "damageable": True,
            "animations": {
                "run": {
                    "location": "resources/sprites/demon_run.png",
                    "width": 16,
                    "height": 16,
                    "ratio": (1, 1),
                    "flip": True,
                    "delay": 100
                }
            },
            "sounds": {
                "hit": {
                    "location": "resources/sounds/demon_hit.wav",
                    "volume": 0.5
                }
            }
        },
        "monster_zombie": {
            "health": 1000,
            "speed": 0.005,
            "action_value": 50,
            "action_delay": 2500,
            "value": 0.75,
            "damageable": True,
            "animations": {
                "run": {
                    "location": "resources/sprites/zombie_run.png",
                    "width": 32,
                    "height": 36,
                    "ratio": (1, 1),
                    "flip": True,
                    "delay": 100
                }
            },
            "sounds": {
                "hit": {
                    "location": "resources/sounds/zombie_hit.wav",
                    "volume": 0.5
                }
            }
        },
        "monster_shaman": {
            "health": 500,
            "speed": 0.01,
            "action_value": 25,
            "action_delay": 1250,
            "value": 1,
            "damageable": True,
            "animations": {
                "run": {
                    "location": "resources/sprites/shaman_run.png",
                    "width": 16,
                    "height": 23,
                    "ratio": (1, 1),
                    "flip": True,
                    "delay": 100
                }
            },
            "sounds": {
                "hit": {
                    "location": "resources/sounds/shaman_hit.wav",
                    "volume": 0.5
                },
                "dash": {
                    "location": "resources/sounds/shaman_dash.wav",
                    "volume": 0.5
                }
            }
        }
    }
}

running = True
last_logic_time = 0

cell_size = 0
offset_x = 0
offset_y = 0

sprites = {}
terrain = []
shop = []
entities = []
state = RESOURCES["states"]["MAIN_MENU"]

selected_hero = None
delete_hero = False
mana = BASE_MANA
score = 0
wave = 0
wave_content = {}
wave_last_spawn = 0
wave_start = 0


def logic(dt):  # Logique
    global last_logic_time

    inputs()

    if dt < 20:  # La logique du jeu s'actualise toutes les 20ms (50x par secondes) et non pas à chaque frame
        return

    last_logic_time = pygame.time.get_ticks()

    if state == RESOURCES["states"]["IN_GAME"]:
        logic_entities()
        logic_waves()


def inputs():  # Gestion des touches
    global running, selected_hero, delete_hero, mana, state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if state == RESOURCES["states"]["IN_GAME"]:
                    for cell in shop:
                        cell_rect = cell["rectangle"]
                        if cell_rect.collidepoint(pygame.mouse.get_pos()):
                            if "hero" in cell["name"]:
                                selected_hero = cell["name"]
                                delete_hero = False
                            elif "trash" in cell["name"]:
                                selected_hero = None
                                delete_hero = True
                    for cell in terrain:
                        cell_rect = cell["rectangle"]
                        if cell["name"] == "ground":
                            if cell_rect.collidepoint(pygame.mouse.get_pos()):
                                x = (cell_rect.x - offset_x) // cell_size
                                y = (cell_rect.y - offset_y) // cell_size

                                if selected_hero is not None and cell_is_empty(cell_rect):
                                    hero_cost = RESOURCES["entities"][selected_hero]["value"]
                                    if mana >= hero_cost:
                                        mana = mana - hero_cost
                                        new_entity(selected_hero, [x, y])
                                        selected_hero = None
                    if delete_hero:
                        for entity in entities:
                            if "hero" in entity["entity_type"]:
                                entity_rect = entity["rectangle"]
                                if entity_rect.collidepoint(pygame.mouse.get_pos()):
                                    damage_entity(entity, 9999999999)
                                    mana += RESOURCES["entities"][entity["entity_type"]]["value"] // 2
                                    delete_hero = False
            if event.button == 3:
                if state == RESOURCES["states"]["IN_GAME"]:
                    selected_hero = None
                    delete_hero = False
        if event.type == pygame.KEYDOWN:
            if state == RESOURCES["states"]["IN_GAME"] and event.key == pygame.K_ESCAPE:
                state = RESOURCES["states"]["PAUSE"]
            elif state == RESOURCES["states"]["PAUSE"] and event.key == pygame.K_ESCAPE:
                state = RESOURCES["states"]["IN_GAME"]
            elif state == RESOURCES["states"]["GAME_OVER"] and event.key == pygame.K_r:
                state = RESOURCES["states"]["IN_GAME"]
                init_game()
            elif state == RESOURCES["states"]["MAIN_MENU"] and event.key == pygame.K_RETURN:
                state = RESOURCES["states"]["IN_GAME"]
                init_game()
            elif state == RESOURCES["states"]["MAIN_MENU"] and event.key == pygame.K_c:
                state = RESOURCES["states"]["CREDITS"]
            elif state == RESOURCES["states"]["MAIN_MENU"] and event.key == pygame.K_ESCAPE:
                running = False
            elif state == RESOURCES["states"]["CREDITS"] and event.key == pygame.K_ESCAPE:
                state = RESOURCES["states"]["MAIN_MENU"]


def cell_is_empty(cell_rect):  # Vérification pour savoir si une cellule du terrain est vide
    for entity in entities:
        if entity["entity_type"] == "elf_arrow":
            continue
        entity_rect = entity["rectangle"]
        if cell_rect.colliderect(entity_rect):
            return False
    return True


def logic_entities():  # Logique des entités
    global mana, score, state

    for entity in entities:
        entity_type = entity["entity_type"]
        entity_position = entity["position"]
        entity_health = entity["health"]
        entity_speed = entity["speed"]
        entity_last_action = entity["last_action"]
        entity_action_value = entity["action_value"]
        entity_action_delay = entity["action_delay"]
        now = pygame.time.get_ticks()

        if entity_health <= 0:
            if entity_type == "hero_doc":
                heal(entity, 1)
            entities.remove(entity)

            if "monster" in entity_type:
                value = RESOURCES["entities"][entity_type]["value"]
                score += 10 - value
            continue
        if entity_speed != 0:
            if not check_collide(entity):
                entity["position"][0] -= entity_speed
                if entity_position[0] < -1:
                    entities.remove(entity)
                    state = RESOURCES["states"]["GAME_OVER"]

                if entity_position[0] > TERRAIN_WIDTH + 5:
                    entities.remove(entity)

        if entity_last_action + entity_action_delay <= now:
            entity["last_action"] = now
            match entity_type:
                case "hero_mage":
                    mana += entity_action_value
                case "hero_elf":
                    for target in entities:
                        if "monster" in target["entity_type"] and target["position"][1] == entity_position[1]:
                            arrow_position = entity["position"][:]
                            arrow_position[1] += 0.5
                            new_entity("elf_arrow", arrow_position)
                case "hero_doc":
                    heal(entity, 0)
                    entity["health"] -= 0.1 * RESOURCES["entities"]["hero_doc"]["health"]
                    play_sound(entity, "heal" + str(random.randint(0, 2)))
                case "elf_arrow":
                    collide = check_collide(entity)
                    if collide is not None:
                        damage_entity(collide, entity_action_value)
                        entities.remove(entity)
                case "mower":
                    collide = check_collide(entity)
                    if collide:
                        play_animation(entity, "run", -1)
                        entity["speed"] = -0.1
                        entities.remove(collide)
                case "monster_shaman":
                    if entity_position[0] <= TERRAIN_WIDTH // 2 and entity["tp"] == 0:  # Les monstres ne se font pas heal donc le last_health est utilisé comme flag de tp
                        target_cell = random.randint(0, TERRAIN_HEIGHT - 1)
                        while target_cell == entity_position[1]:
                            target_cell = random.randint(0, TERRAIN_HEIGHT - 1)

                        entity["position"][1] = target_cell
                        entity["tp"] = 1
                        play_sound(entity, "dash")

            collide = check_collide(entity)
            if collide and collide["damageable"]:
                damage_entity(collide, entity_action_value)


def heal(entity, shape):  # shape 0: line  x & shape 1: square 3x3 centered (x,y)
    to_heal = []
    if shape:
        for target in entities:
            if "hero" in target["entity_type"] and target["entity_type"] != "hero_doc":
                if target["position"][0] + 1 >= entity["position"][0] and target["position"][0] <= entity["position"][
                    0] + 1 and target["position"][1] + 1 >= entity["position"][1] and target["position"][1] <= \
                        entity["position"][1] + 1:
                    to_heal.append(target)
    else:
        for target in entities:
            if "hero" in target["entity_type"] and target["entity_type"] != "hero_doc":
                if target["position"][1] == entity["position"][1]:
                    to_heal.append(target)

    for target in to_heal:
        target["health"] += RESOURCES["entities"][entity["entity_type"]]["action_value"] * \
                            RESOURCES["entities"][entity["entity_type"]]["health"]
        target["health"] = min(target["health"], RESOURCES["entities"][target["entity_type"]]["health"])
        target["last_heal"] = pygame.time.get_ticks()


def check_collide(entity):  # Vérification des collisions d'une entité
    result = None
    for target in entities:
        entity_type = entity["entity_type"]
        target_type = target["entity_type"]

        if entity == target:
            continue
        if "monster" in entity_type and "monster" in target_type:
            continue
        if "monster" not in entity_type and "monster" not in target_type:
            continue
        if entity["rectangle"].colliderect(target["rectangle"]):
            result = target
            break

    return result


def damage_entity(entity, value):  # Application de dégats à une entité
    entity["health"] -= value
    entity["last_hit"] = pygame.time.get_ticks()
    play_sound(entity, "hit")


def new_entity(entity_type, position=None):  # Ajout d'une entité au jeu
    if position is None:
        position = [0, 0]

    entity_values = RESOURCES["entities"][entity_type]
    health = entity_values["health"]
    speed = entity_values["speed"]
    action_value = entity_values["action_value"]
    action_delay = entity_values["action_delay"]
    damageable = entity_values["damageable"]
    animator = {
        "default": "",
        "current": "",
        "loop": 0,
        "animations": {}
    }
    entity_width = cell_size
    entity_height = cell_size

    sounds = {}

    for anim_name in entity_values["animations"]:
        anim = entity_values["animations"][anim_name]
        anim_location = anim["location"]
        anim_width = anim["width"]
        anim_height = anim["height"]
        anim_ratio = anim["ratio"]
        anim_flip = anim["flip"]
        anim_delay = anim["delay"]

        entity_width = cell_size * anim_ratio[0]
        entity_height = cell_size * anim_ratio[1]

        anim_frames = load_sprite_sheet(anim_location, anim_flip, anim_ratio, anim_width, anim_height)
        animation = new_animation(anim_delay, anim_frames)
        add_animation(animator, anim_name, animation)

    for sound_name in entity_values["sounds"]:
        sound_data = entity_values["sounds"][sound_name]
        if sound_data is not None:
            sound = pygame.mixer.Sound(sound_data["location"])
            sound.set_volume(sound_data["volume"])
            sounds[sound_name] = sound
        else:
            sounds[sound_name] = None

    rectangle = pygame.Rect(position, (entity_width, entity_height))

    entities.append(
        new_entity_data(entity_type, position, health, speed, action_value, action_delay, animator, sounds, damageable,
                        rectangle))


def new_entity_data(entity_type, position, health, speed, action_value, action_delay, animator, sounds, damageable,
                    rectangle):  # Collection contenant les informations d'une entité
    return {
        "entity_type": entity_type,
        "position": position,
        "health": health,
        "speed": speed,
        "last_action": pygame.time.get_ticks(),
        "action_value": action_value,
        "action_delay": action_delay,
        "animator": animator,
        "sounds": sounds,
        "damageable": damageable,
        "last_hit": 0,
        "last_heal": 0,
        "tp": 0,
        "rectangle": rectangle
    }


def load_sprite_sheet(location, flip, ratio, width, height):  # Chargement d'une feuille de sprites
    sprite_sheet = pygame.image.load(location)

    sprite_sheet_w = sprite_sheet.get_size()[0] // width
    sprite_sheet_h = sprite_sheet.get_size()[1] // height

    frames = []

    for i in range(sprite_sheet_w):
        for j in range(sprite_sheet_h):
            sprite = pygame.Surface((width, height), flags=pygame.SRCALPHA)
            sprite.blit(sprite_sheet, (0, 0), (
                i * width, j * height, (i + 1) * width, (j + 1) * height))
            sprite = pygame.transform.scale(sprite, (cell_size * ratio[0], cell_size * ratio[1]))

            if flip:
                sprite = pygame.transform.flip(sprite, True, False)

            frames.append(sprite)

    return frames


def new_animation(delay, frames):  # Création d'une animation
    return {
        'delay': delay,
        'last_frame_time': 0,
        'last_frame_id': 0,
        'frames': frames
    }


def add_animation(animator, name, animation):  # Ajout d'une animation à un animator
    animator["animations"][name] = animation
    if animator["default"] == "":
        animator["default"] = name


def play_animation(entity, name, loop=1):  # Changement de l'animation en cours d'une entité
    animator = entity["animator"]
    animator["current"] = name
    animator["loop"] = loop


def play_sound(entity, sound_name, loop=0):  # Lancement d'un son
    if sound_name in entity["sounds"]:
        sound = entity["sounds"][sound_name]
        sound.play(loop)


def logic_waves():  # Logique des vagues
    global wave_content, wave_last_spawn, wave_start, wave

    if pygame.time.get_ticks() < wave_start:
        return

    monsters = []
    for entity_type in RESOURCES["entities"]:
        if "monster" in entity_type:
            monsters.append(entity_type)

    for entity_type in wave_content:
        if wave_content[entity_type] != 0:
            cooldown = max(WAVE_SPAWN_MIN_COOLDOWN, WAVE_SPAWN_COOLDOWN * (WAVE_SPAWN_REDUCTION_FACTOR ** wave))
            if pygame.time.get_ticks() >= wave_last_spawn + cooldown:
                index = random.randrange(0, len(monsters))
                chosen = monsters[index]
                while wave_content[chosen] == 0:
                    index = random.randrange(0, len(monsters))
                    chosen = monsters[index]

                wave_content[chosen] -= 1
                new_entity(chosen, [TERRAIN_WIDTH + 2, random.randrange(0, TERRAIN_HEIGHT - 1)])
                wave_last_spawn = pygame.time.get_ticks()
        else:
            if entity_type == monsters[len(wave_content) - 1] and not monster_on_terrain():
                wave += 1
                wave_content = new_wave(wave)
                wave_start = pygame.time.get_ticks() + WAVE_DELAY


def new_wave(wave_number):  # Génération de la prochaine vague
    monsters = {}
    for entity_type in RESOURCES["entities"]:
        if "monster" in entity_type:
            entity = RESOURCES["entities"][entity_type]
            spawn_rate = entity["value"] * wave_number
            spawn_numbers = round(spawn_rate * random.uniform(0.5, 1.2))

            monsters[entity_type] = spawn_numbers

    return monsters


def monster_on_terrain():  # Vérifie si un monstre est présent sur le terrain
    for entity in entities:
        if "monster" in entity["entity_type"]:
            return True

    return False


def render():  # Rendu
    window.fill("#000000")
    game_background = pygame.image.load(RESOURCES["game_background"])
    game_background = pygame.transform.scale(game_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(game_background, (0, 0))

    render_terrain()
    render_entities()
    render_ui()
    render_menus()
    pygame.display.flip()


def render_terrain():  # Rendu du terrain
    for cell in terrain:
        window.blit(cell["sprite"], cell["rectangle"])


def render_entities():  # Rendu des entités
    for entity in entities:
        entity["rectangle"].x = offset_x + entity["position"][0] * cell_size
        entity["rectangle"].y = offset_y + entity["position"][1] * cell_size

        render_animation(entity)


def render_animation(entity):  # Rendu de l'animation d'une entité
    animator = entity["animator"]

    loop = animator["loop"]

    if loop == 0:
        play_animation(entity, animator["default"])

    current = animator["current"]

    if current not in animator["animations"]:
        return

    animation = animator["animations"][current]
    delay = animation["delay"]
    last_frame_time = animation["last_frame_time"]

    now = pygame.time.get_ticks()

    frames = animation["frames"]
    last_frame_id = animation["last_frame_id"]
    if now < last_frame_time + delay:
        frame = frames[last_frame_id].copy()

        render_frame(frame, entity)

        window.blit(frame, entity["rectangle"])
        return

    next_frame = last_frame_id + 1

    if next_frame >= len(frames):
        next_frame = 0
        if loop != -1:
            animator["loop"] -= 1

    frame = frames[last_frame_id].copy()

    render_frame(frame, entity)

    window.blit(frame, entity["rectangle"])
    animation["last_frame_id"] = next_frame
    animation["last_frame_time"] = now


def render_frame(frame, entity):  # Rendu de la frame actuel de l'animation
    if pygame.time.get_ticks() <= entity["last_hit"] + HIT_DURATION:
        frame.fill("#FF0000", None, pygame.BLEND_MULT)
    elif pygame.time.get_ticks() <= entity["last_heal"] + HIT_DURATION:
        frame.fill("#00FF00", None, pygame.BLEND_MULT)
    else:
        max_health = RESOURCES["entities"][entity["entity_type"]]["health"]
        ratio = entity["health"] / max_health
        ratio = min(ratio, 1.0)
        ratio = max(ratio, 0.0)
        frame.fill((255 * ratio, 255 * ratio, 255 * ratio), None, pygame.BLEND_RGB_MULT)


def render_ui():  # Rendu de l'interface
    # Shop
    for cell in shop:
        window.blit(cell["sprite"], cell["rectangle"])
        if cell["name"] == "mana_potion":
            mana_text = font.render(str(mana), True, "#000000")
            mana_text_rect = mana_text.get_rect(
                center=(cell["rectangle"][0] + SHOP_CELL_SIZE // 2, cell["rectangle"][1] - SHOP_CELL_SIZE // 7))
            window.blit(mana_text, mana_text_rect)
        elif "hero" in cell["name"]:
            hero_cost = RESOURCES["entities"][cell["name"]]["value"]
            cost_text = font.render(str(hero_cost), True, "#000000")
            cost_text_rect = cost_text.get_rect(
                center=(cell["rectangle"][0] + SHOP_CELL_SIZE // 2, cell["rectangle"][1] - SHOP_CELL_SIZE // 7))
            window.blit(cost_text, cost_text_rect)

    if selected_hero is not None:
        hero = RESOURCES["entities"][selected_hero]
        hero_cost = hero["value"]
        hero_sprite = pygame.image.load(RESOURCES["entities"][selected_hero]["animations"]["idle"]["location"])
        hero_sprite = pygame.transform.scale(hero_sprite, (4 * cell_size, cell_size))
        hero_sprite.set_alpha(128)

        if hero_cost > mana:
            sprite_width = hero_sprite.get_size()[0]
            sprite_height = hero_sprite.get_size()[1]
            for i in range(sprite_width):
                for j in range(sprite_height):
                    pixel = hero_sprite.get_at((i, j))
                    r = pixel.r
                    g = pixel.g
                    b = pixel.b
                    a = pixel.a

                    gray = 0.299 * r + 0.587 * g + 0.114 * b

                    hero_sprite.set_at((i, j), (gray, gray, gray, a))

        mouse_pos = pygame.mouse.get_pos()
        window.blit(hero_sprite, (mouse_pos[0] - cell_size / 2, mouse_pos[1] - cell_size / 2),
                    (0, 0, cell_size, cell_size))

    if delete_hero:
        trash_sprite = pygame.image.load(RESOURCES["sprites"]["trash"])
        trash_sprite = pygame.transform.scale(trash_sprite, (cell_size // 2, cell_size // 2))
        trash_sprite.set_alpha(128)

        mouse_pos = pygame.mouse.get_pos()
        window.blit(trash_sprite, (mouse_pos[0] - cell_size / 4, mouse_pos[1] - cell_size / 4),
                    (0, 0, cell_size, cell_size))

    # Score
    score_text = middle_font.render("SCORE: " + str(score), True, "#FFFFFF")
    score_text_rect = score_text.get_rect(topleft=(32, WINDOW_HEIGHT - 25))
    window.blit(score_text, score_text_rect)

    # Wave
    wave_text = middle_font.render("WAVE: " + str(wave), True, "#FFFFFF")
    wave_text_rect = wave_text.get_rect(topleft=(32, WINDOW_HEIGHT - 50))
    window.blit(wave_text, wave_text_rect)

    # Wave Time left
    current_time = pygame.time.get_ticks()
    if current_time < wave_start:
        time_left = wave_start - current_time
        progress = time_left / WAVE_DELAY
        pygame.draw.rect(window, "#000000", (
            offset_x, offset_y + TERRAIN_HEIGHT * cell_size + 2, TERRAIN_WIDTH * cell_size, 10))
        pygame.draw.rect(window, "#FF0000", (
            offset_x + 2, offset_y + TERRAIN_HEIGHT * cell_size + 4, (TERRAIN_WIDTH * cell_size) * progress - 2, 6))


def render_menus():
    if state == RESOURCES["states"]["PAUSE"]:
        window.fill("#383838", None, pygame.BLEND_RGB_MULT)
        pause_text = big_font.render("PAUSE", True, "#FFFFFF")
        resume_text = font.render("Press 'ESCAPE' to resume", True, "#FFFFFF")

        pause_text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 - 64))
        window.blit(pause_text, pause_text_rect)

        resume_text_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 3)))
        window.blit(resume_text, resume_text_rect)
    elif state == RESOURCES["states"]["GAME_OVER"]:
        window.fill("#FF8080", None, pygame.BLEND_RGB_MULT)
        gameover_text = big_font.render("GAME OVER", True, "#FFFFFF")
        score_text = big_font.render("SCORE: " + str(score), True, "#FFFFFF")
        restart_text = big_font.render("Press 'R' to restart", True, "#FFFFFF")

        gameover_text_rect = gameover_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 - 64))
        window.blit(gameover_text, gameover_text_rect)

        score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 3)))
        window.blit(score_text, score_text_rect)

        restart_text_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 3) + 128))
        window.blit(restart_text, restart_text_rect)

    elif state == RESOURCES["states"]["MAIN_MENU"]:
        # Display background image
        menu_image = pygame.image.load(RESOURCES["menu_background"])
        menu_image = pygame.transform.scale(menu_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(menu_image, (0, 0))

        # Display commands
        menu_text = huge_font.render(GAME_NAME, True, "#FFFFFF")
        creator_text = font.render("By maschins, Buubuulle & Storm", True, "#FFFFFF")
        start_text = big_font.render("Start [ENTER]", True, "#FFFFFF")
        credits_text = big_font.render("Credits [C]", True, "#FFFFFF")
        quit_text = big_font.render("Quit [ESC]", True, "#FFFFFF")

        menu_text_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 - 64))
        window.blit(menu_text, menu_text_rect)

        creator_text_rect = creator_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 - 32))
        window.blit(creator_text, creator_text_rect)

        start_text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 64))
        window.blit(start_text, start_text_rect)

        credits_text_rect = credits_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 128))
        window.blit(credits_text, credits_text_rect)

        quit_text_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 192))
        window.blit(quit_text, quit_text_rect)

    elif state == RESOURCES["states"]["CREDITS"]:
        menu_image = pygame.image.load(RESOURCES["menu_background"])
        menu_image = pygame.transform.scale(menu_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(menu_image, (0, 0))
        window.fill("#383838", None, pygame.BLEND_RGB_MULT)
        title_text = big_font.render("CREDITS", True, "#FFFFFF")

        credits_ppi_text = font.render("Thanks to Mr Mathy for PPI tutorials,", True, "#FFFFFF")
        credits_assistants_text = font.render("thanks to the assistant and the student instructors for the advice",
                                              True, "#FFFFFF")
        credits_sprite_text = font.render("and finally, thanks to @Robert(0x72) for sprites.", True, "#FFFFFF")

        title_text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 64))
        window.blit(title_text, title_text_rect)

        credits_ppi_text_rect = credits_ppi_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 128))
        window.blit(credits_ppi_text, credits_ppi_text_rect)

        credits_assistants_text_rect = credits_assistants_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 148))
        window.blit(credits_assistants_text, credits_assistants_text_rect)

        credits_sprite_text_rect = credits_sprite_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 168))
        window.blit(credits_sprite_text, credits_sprite_text_rect)


def init_game():  # Initialisation de la partie
    global sprites, terrain, shop, entities, mana, score, wave, wave_content, wave_last_spawn, wave_start, selected_hero, delete_hero, cell_size, offset_x, offset_y
    current_time = pygame.time.get_ticks()

    entities = []
    selected_hero = None
    delete_hero = False
    mana = BASE_MANA
    score = 0
    wave = 1
    wave_content = new_wave(wave)
    wave_last_spawn = current_time
    wave_start = current_time + WAVE_DELAY

    # Définition de la taille et de la position du terrain
    cell_size = min((WINDOW_WIDTH - 2 * TERRAIN_MIN_SPACE) // TERRAIN_WIDTH,
                    (WINDOW_HEIGHT - SHOP_CELL_SIZE - 2 * TERRAIN_MIN_SPACE) // TERRAIN_HEIGHT)
    offset_x = TERRAIN_MIN_SPACE + (WINDOW_WIDTH - 2 * TERRAIN_MIN_SPACE - TERRAIN_WIDTH * cell_size) // 2
    offset_y = SHOP_CELL_SIZE + TERRAIN_MIN_SPACE + (
            WINDOW_HEIGHT - SHOP_CELL_SIZE - 2 * TERRAIN_MIN_SPACE - TERRAIN_HEIGHT * cell_size) // 2

    # Chargement des sprites
    sprites = {}
    sprites_resources = RESOURCES["sprites"]
    for sprite_key in sprites_resources:
        sprite_path = sprites_resources[sprite_key]
        sprite = pygame.image.load(sprite_path).convert_alpha(window)
        sprite = pygame.transform.scale(sprite, (cell_size, cell_size))
        sprites[sprite_key] = sprite

    # Génération du terrain
    terrain = []
    for i in range(TERRAIN_HEIGHT):
        for j in range(TERRAIN_WIDTH):
            cell_rect = pygame.Rect((offset_x + j * cell_size, offset_y + i * cell_size), (cell_size, cell_size))
            terrain.append(cell_data("ground", cell_rect))

        cell_rect = pygame.Rect((offset_x + -1 * cell_size, offset_y + i * cell_size), (cell_size, cell_size))
        terrain.append(cell_data("cracked_ground", cell_rect))
        new_entity("mower", [-1, i])

    # Génération du shop
    shop = []
    tags = []
    sprites["shop_tag"] = pygame.transform.scale(sprites["shop_tag"], (SHOP_CELL_SIZE, SHOP_CELL_SIZE))
    for sprite_key in sprites:
        if "hero" in sprite_key or sprite_key == "mana_potion":
            sprites[sprite_key] = pygame.transform.scale(sprites[sprite_key], (SHOP_CELL_SIZE, SHOP_CELL_SIZE))
            cell_rect = pygame.Rect((SHOP_CELL_SIZE * len(shop), SHOP_CELL_SIZE // 3), (SHOP_CELL_SIZE, SHOP_CELL_SIZE))
            shop.append(cell_data(sprite_key, cell_rect))
            tag_rect = pygame.Rect((SHOP_CELL_SIZE * (len(shop) - 1), 0), (SHOP_CELL_SIZE, SHOP_CELL_SIZE))
            tags.append(cell_data("shop_tag", tag_rect))
    cell_rect = pygame.Rect((WINDOW_WIDTH - 64, WINDOW_HEIGHT - 64), (SHOP_CELL_SIZE, SHOP_CELL_SIZE))
    shop.append(cell_data("trash", cell_rect))
    for tag in tags:
        shop.insert(0, tag)


def cell_data(sprite, rectangle):  # Collection contenant le rectangle et le sprite d'une cellule
    return {
        "name": sprite,
        "sprite": sprites[sprite],
        "rectangle": rectangle
    }


# Initialisation du jeu
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(GAME_NAME)

font = pygame.font.Font(RESOURCES["font"], 16)
middle_font = pygame.font.Font(RESOURCES["font"], 24)
big_font = pygame.font.Font(RESOURCES["font"], 48)
huge_font = pygame.font.Font(RESOURCES["font"], 64)

# Initialisation du son et lancement de la musique de fond
pygame.mixer.init()
pygame.mixer.music.load(RESOURCES["music"]["location"])
pygame.mixer.music.set_volume(RESOURCES["music"]["volume"])
pygame.mixer.music.play(-1)

init_game()

while running:
    pygame.time.Clock().tick()
    delta_time = pygame.time.get_ticks() - last_logic_time

    logic(delta_time)
    render()

pygame.display.quit()
pygame.quit()
exit()
