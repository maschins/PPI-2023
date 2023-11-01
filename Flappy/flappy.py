# FRAIPONTS Thomas s2301865
# SCHINS Martin s220635
# PIERRET Alexandre s2306917

import pygame, random, math

BLEU_CIEL = (135, 206, 250)
ORANGE    = (255, 165,   0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

FLAPPY_LARGEUR = 60
FLAPPY_HAUTEUR = 51

ACC_CHUTE = (0, FENETRE_HAUTEUR) # pixels/s^2
DEPLACEMENT_HAUT = -FENETRE_HAUTEUR / 25

##### Définition MOUVEMENT #####

def mouvement(nom, duree):
    return (nom, duree) # durée en msec


def nomMouvement(mvt):
    return mvt[0]


def dureeMouvement(mvt):
    return mvt[1]

##### Fin MOUVEMENT #####

##### Définition ANIMATION #####

def nouvelleAnimation():
    return {
        'boucle':False,
        'repetition': 0,
        'momentMouvementSuivant':None,
        'indexMouvement':None,
        'choregraphie':[] # liste de mouvements
    }


def repete(animation, fois):
    animation['repetition'] = fois
    animation['boucle'] = False


def enBoucle(animation):
    animation['boucle'] = True


def ajouteMouvement(animation, mvt):
    animation['choregraphie'].append(mvt)


def mouvementActuel(animation):
    if animation['indexMouvement'] == None:
        return None
    else:
        return nomMouvement(animation['choregraphie'][animation['indexMouvement']])


def commenceMouvement(animation, index):
    animation['indexMouvement'] = index
    animation['momentMouvementSuivant'] = pygame.time.get_ticks() + dureeMouvement(animation['choregraphie'][index])


def commence(animation):
    commenceMouvement(animation, 0)


def arrete(animation):
    animation['indexMouvement'] = None


def anime(animation):
    if animation['indexMouvement'] == None:
        commence(animation)
    elif animation['momentMouvementSuivant'] <= pygame.time.get_ticks():
      if animation['indexMouvement'] == len(animation['choregraphie']) - 1:
        if animation['boucle']:
            commence(animation)
        else:
            if animation['repetition'] > 0:
                animation['repetition'] -= 1
                commence(animation)
            else:
                arrete(animation)
      else:
        commenceMouvement(animation, animation['indexMouvement'] + 1)

##### Fin ANIMATION #####

##### Définition ENTITE #####

def nouvelleEntite():
    return {
        'visible':False,
        'position': [0, 0],
        'vitesse': [0, 0],
        'acceleration': [0, 0],
        'momentDeplacement': 0,
        'imageAffichee':None,
        'poses': {}, # dictionnaire de nom:image
        'animationActuelle':None,
        'animations':{} #dictionnaire de nom:animation
    }


def visible(entite):
    entite['visible'] = True


def invisible(entite):
    entite['visible'] = False


def estVisible(entite):
    return entite['visible']


def place(entite, x, y):
    entite['position'][0] = x
    entite['position'][1] = y


def vitesse(entite, vx, vy):
    entite['vitesse'][0] = vx
    entite['vitesse'][1] = vy


def acceleration(entite, ax, ay):
    entite['acceleration'][0] = ax
    entite['acceleration'][1] = ay


def deplace(entite, maintenant):
    dt = (maintenant - entite['momentDeplacement']) / 1000
    # mise à jour vitesse
    entite['vitesse'][0] += entite['acceleration'][0] * dt
    entite['vitesse'][1] += entite['acceleration'][1] * dt
    # mise à jour position
    entite['position'][0] += entite['vitesse'][0] * dt
    entite['position'][1] += entite['vitesse'][1] * dt
    # mise à jour moment de déplacement
    entite['momentDeplacement'] = maintenant


def position(entite):
    return entite['position']


def ajoutePose(entite, nom, image):
    entite['poses'][nom] = image


def prendsPose(entite, nom_pose):
    entite['imageAffichee'] = entite['poses'][nom_pose]
    visible(entite)


def dessine(entite, ecran):
    ecran.blit(entite['imageAffichee'], entite['position'])


def commenceAnimation(entite, nomAnimation, fois = 1):
    entite['animationActuelle'] = entite['animations'][nomAnimation]
    if fois == 0:
        enBoucle(entite['animationActuelle'])
    else:
        repete(entite['animationActuelle'], fois - 1)
    visible(entite)


def arreteAnimation(entite):
    arrete(entite['animationActuelle'])
    entite['animationActuelle'] = None


def ajouteAnimation(entite, nom, animation):
    entite['animations'][nom] = animation


def estEnAnimation(entite):
    return entite['animationActuelle'] != None


def impulsion_oiseau():
    positionOiseau = position(oiseau)
    place(oiseau, positionOiseau[0], positionOiseau[1] + DEPLACEMENT_HAUT)
    vitesse(oiseau, 0, 0)
    if not estEnAnimation(oiseau):
        commenceAnimation(oiseau, 'vol')

##### Fin ENTITE #####

def affiche(entites, ecran):
    for objet in entites:
        if estVisible(objet):
            if estEnAnimation(objet):
                animationActuelle = objet['animationActuelle']
                poseActuelle = mouvementActuel(animationActuelle)
                anime(animationActuelle)
                nouvellePose = mouvementActuel(animationActuelle)
                if nouvellePose == None:
                    objet['animationActuelle'] = None
                    prendsPose(objet, poseActuelle)
                else:
                    prendsPose(objet, nouvellePose)

            dessine(objet, ecran)


def miseAJour(scene):
    maintenant = pygame.time.get_ticks()
    for objet in scene:
        deplace(objet, maintenant)


def traite_entrees():
    global fini, enJeu
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.KEYDOWN:
            if enJeu:
                impulsion_oiseau()
            else:
                enJeu = True
                arreteAnimation(oiseau)
                prendsPose(oiseau, 'AILE_MILIEU')
                


pygame.init()

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)
pygame.display.set_caption('FLAPPY')

oiseau = nouvelleEntite()
acceleration(oiseau, ACC_CHUTE[0], ACC_CHUTE[1]) # Définir une accélération de base à l'oiseau

for nom_image, nom_fichier in (('AILE_HAUTE','bird_wing_up.png'),
                               ('AILE_MILIEU','bird_wing_mid.png'),
                               ('AILE_BASSE', 'bird_wing_down.png')):
    chemin = 'images/' + nom_fichier
    image = pygame.image.load(chemin).convert_alpha(fenetre)
    image = pygame.transform.scale(image, (FLAPPY_LARGEUR, FLAPPY_HAUTEUR))
    ajoutePose(oiseau, nom_image, image)


animation = nouvelleAnimation()
ajouteMouvement(animation, mouvement('AILE_HAUTE', 80))
ajouteMouvement(animation, mouvement('AILE_MILIEU', 80))
ajouteMouvement(animation, mouvement('AILE_BASSE', 80))
ajouteMouvement(animation, mouvement('AILE_MILIEU', 80))

ajouteAnimation(oiseau, 'vol', animation)

place(oiseau, 50, 50)

scene = [oiseau]
commenceAnimation(oiseau, 'vol', 0)

police_caractere = pygame.font.SysFont('monospace', 24, True)
message = police_caractere.render("N'importe quelle touche pour commencer/voler", True, ORANGE)
messageLargeur, messageHauteur = police_caractere.size("N'importe quelle touche pour commencer/voler")
        
fini = False
enJeu = False
temps = pygame.time.Clock()
temps_definition = -500

while not fini:
    # --- Traiter entrées joueur
    fenetre.fill(BLEU_CIEL)
    affiche(scene, fenetre)
    
    if not enJeu:
        fenetre.blit(message, ((FENETRE_LARGEUR - messageLargeur) // 2, (FENETRE_HAUTEUR - messageHauteur)// 2))
        
        if pygame.time.get_ticks() >= temps_definition + 500: # calculer le nouveau nombre d'impulsions
            probabilite_battre_ailes = math.ceil(position(oiseau)[1]/150)
            nombre_impulsions_par_seconde = random.randint(probabilite_battre_ailes-2, probabilite_battre_ailes+2)
            temps_definition = pygame.time.get_ticks()
            compteur = 0
        
        if nombre_impulsions_par_seconde > 0 and pygame.time.get_ticks() >= temps_definition + compteur*500/nombre_impulsions_par_seconde: # donner le nombre d'impulsions à l'oiseau
            impulsion_oiseau()
            compteur += 1
            
    traite_entrees()
    miseAJour(scene)   
        
    pygame.display.flip()

    temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()
