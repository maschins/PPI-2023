import pygame


H = 0
V = 1

BLEU_CLAIR  = (  0, 191, 200)
JAUNE       = (255, 255,   0)
ROUGE       = (255,   0,   0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

BALLE_RAYON = 10

RAQUETTE_LARGEUR = 70
RAQUETTE_HAUTEUR = 30
RAQUETTE_ESPACE = 30
RAQUETTE_DEPLACEMENT = 10

TOUCHE_DROITE = pygame.K_RIGHT
TOUCHE_GAUCHE = pygame.K_LEFT

VERS_DROITE = 1
VERS_GAUCHE = -1

deplace_droite = False
deplace_gauche = False

#--- Définitions de fonctions
def deplace_raquette(sens):
    raquette_position[H] += RAQUETTE_DEPLACEMENT * sens
    if raquette_position[H] < 0:
        raquette_position[H] = 0
    elif raquette_position[H] + RAQUETTE_LARGEUR >= FENETRE_LARGEUR:
        raquette_position[H] = FENETRE_LARGEUR - RAQUETTE_LARGEUR

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 32)

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)

fenetre.fill(BLEU_CLAIR)


balle_position = [10, 300]
balle_vitesse  = [2, 2]

raquette_position = [FENETRE_LARGEUR//2 - RAQUETTE_LARGEUR//2, FENETRE_HAUTEUR - RAQUETTE_ESPACE - RAQUETTE_HAUTEUR]

en_jeu = True
en_menu = False

score = 0

temps = pygame.time.Clock()

#--- Boucle principale
while en_jeu:

    #--- Traiter entrées joueur
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_jeu = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
    	deplace_raquette(VERS_GAUCHE)
    if keys[pygame.K_RIGHT]:
    	deplace_raquette(VERS_DROITE)

    if balle_position[V] + BALLE_RAYON == raquette_position[V]:
        if balle_position[H] >= raquette_position[H] and balle_position[H] <= raquette_position[H] + RAQUETTE_LARGEUR:
            balle_vitesse[V] = -balle_vitesse[V]
            score += 1          
    		
    if balle_position[H] + BALLE_RAYON >= FENETRE_LARGEUR:
        balle_vitesse[H] = -balle_vitesse[H]
    elif balle_position[H] < BALLE_RAYON:
            balle_vitesse[H] = -balle_vitesse[H]

    if balle_position[V] + BALLE_RAYON >= FENETRE_HAUTEUR:
        en_jeu = False
        en_menu = True
        
    elif balle_position[V] < BALLE_RAYON:
            balle_position[V] = BALLE_RAYON
            balle_vitesse[V] = -balle_vitesse[V]
            
    #--- Logique du jeu
    balle_position[H] = balle_position[H] + balle_vitesse[H]
    balle_position[V] = balle_position[V] + balle_vitesse[V]


    #--- Dessiner l'écran
    text = font.render(str(score), True, (0, 0, 0))
    textRect = text.get_rect()

    fenetre.fill(BLEU_CLAIR)
    fenetre.blit(text, textRect)
    pygame.draw.circle(fenetre, JAUNE, balle_position, BALLE_RAYON)
    pygame.draw.rect(fenetre, ROUGE, (raquette_position, (RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)))

    #--- Afficher (rafraîchir) l'écran
    pygame.display.flip()

    #--- 50 images par seconde
    temps.tick(50)

pygame.display.quit()
pygame.quit()
