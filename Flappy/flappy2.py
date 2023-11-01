# FRAIPONTS Thomas s2301865
# SCHINS Martin s220635
# PIERRET Alexandre s2306917

import pygame
import random

BLEU_CIEL = (135, 206, 250)
ORANGE    = (255, 165,   0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

FLAPPY_LARGEUR = 60
FLAPPY_HAUTEUR = 51

NUAGE_LARGEUR = 127
NUAGE_HAUTEUR = 75

ITEM_SIZE = 50

ACC_CHUTE = (0, FENETRE_HAUTEUR) # pixel/s^2
DEPLACEMENT_HAUT = -FENETRE_HAUTEUR / 25
VITESSE_HORIZONTALE = 4 # m/s

COULOIRS_AERIENS = 5
NUAGE_VITESSE_MIN = FENETRE_LARGEUR // 10 # pixel/s
NUAGE_VITESSE_MAX = FENETRE_LARGEUR // 2

INTERVALLE_NUAGES = 1000 # ms

NOMBRE_ITEMS_MAX = 1

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


def reveille(entite):
    entite['momentDeplacement'] = pygame.time.get_ticks()


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


def rectangle(entite):
    return entite['imageAffichee'].get_rect().move(entite['position'][0], entite['position'][1])

##### Fin ENTITE #####

##### Définition SCORE #####

def score():
    return {
        'valeur': 0,
        'derniereMiseAJour': 0
    }


def miseAJourScore(score, maintenant):
    dt = (maintenant - score['derniereMiseAJour']) / 1000
    score['derniereMiseAJour'] = maintenant
    score['valeur'] += VITESSE_HORIZONTALE * dt


def resultat(score):
    return int(score['valeur'])


def reinitialiser(score):
    score['valeur'] = 0
    score['derniereMiseAJour'] = pygame.time.get_ticks()

##### Fin SCORE #####

##### Définition SCENE #####

def nouvelleScene():
    return {
        'acteurs': []
    }


def ajouteEntite(scene, entite):
    scene['acteurs'].append(entite)


def enleveEntite(scene, entite):
    global nombre_items_scene
    acteurs = scene['acteurs']
    if entite in acteurs:
        if "item" in entite["poses"]:
           nombre_items_scene -= 1
        acteurs.remove(entite)


def acteurs(scene):
    return list(scene['acteurs'])


def miseAJour(scene, maintenant):
    maScene = acteurs(scene)
    for entite in maScene:
        deplace(entite, maintenant)


def affiche(scene, ecran):
    entites = acteurs(scene)
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

##### Fin SCENE #####

##### Définition CIEL #####

def nouveauCiel(nombreCouloirs):
    random.seed()
    taille_couloir = FENETRE_HAUTEUR // (nombreCouloirs + 1)
    demi_couloir = taille_couloir // 2
    return {
        'couloirs': [0] + [demi_couloir + n*taille_couloir for n in range(nombreCouloirs + 1)],
        'vents': [0] * (nombreCouloirs + 2),
        'nombreCouloirs': nombreCouloirs,
        'tailleCouloir': taille_couloir
    }


def changeVitesseVent(ciel, couloir, vitesse):
    ciel['vents'][couloir] = -vitesse


def changeVentHaut(ciel, vitesse):
    changeVitesseVent(ciel, 0, vitesse)


def changeVentBas(ciel, vitesse):
    changeVitesseVent(ciel, ciel['nombreCouloirs'] + 1, vitesse)


def vitesseVent(ciel, couloir):
    return ciel['vents'][couloir]


def ventHaut(ciel):
    return vitesseVent(ciel, 0)


def ventBas(ciel):
    return vitesseVent(ciel, ciel['nombreCouloirs'] + 1)


def debutCouloir(ciel, couloir):
    return ciel['couloirs'][couloir]


def debutHaut(ciel):
    return debutCouloir(ciel, 0)


def debutBas(ciel):
    return debutCouloir(ciel, ciel['nombreCouloirs'] + 1)


def rangeCouloirs(ciel):
    return range(1, ciel['nombreCouloirs'] + 1)


def nouveauNuage(ciel, couloir, image):
    nuage = nouvelleEntite()
    ajoutePose(nuage, 'nuage', image)
    prendsPose(nuage, 'nuage')
    rect = rectangle(nuage)
    debut = debutCouloir(ciel, couloir)
    fin = debutCouloir(ciel, couloir + 1) - 1 if couloir < ciel['nombreCouloirs'] + 1 else  FENETRE_HAUTEUR - 1
    if couloir == 0:
        rect.bottom = random.randint((debut + fin) // 2, fin)
        vitesse(nuage, ventHaut(ciel), 0)
    elif couloir == ciel['nombreCouloirs'] + 1:
        rect.top = random.randint(debut, (debut + fin) // 2)
        vitesse(nuage, ventBas(ciel), 0)
    else:
        rect.top = random.randint(debut, fin - rect.height)
        vitesse(nuage, vitesseVent(ciel, couloir), 0)
    y = rect.top
    place(nuage, FENETRE_LARGEUR, y)
    return nuage
    

def nouveauItem(ciel, couloir, image):
    global nombre_items_scene
    item = nouvelleEntite()
    ajoutePose(item, 'item', image)
    prendsPose(item, 'item')
    rect = rectangle(item)
    debut = debutCouloir(ciel, couloir)
    fin = debutCouloir(ciel, couloir + 1) - 1 if couloir < ciel['nombreCouloirs'] + 1 else  FENETRE_HAUTEUR - 1
    rect.top = random.randint(debut, fin - rect.height)
    vitesse(item, vitesseVent(ciel, couloir), 0)
    y = rect.top
    place(item, FENETRE_LARGEUR, y)
    
    nombre_items_scene += 1
    return item


def nouveauNuageHaut(ciel, image):
    return nouveauNuage(ciel, 0, image)


def nouveauNuageBas(ciel, image):
    return nouveauNuage(ciel, ciel['nombreCouloirs'] + 1, image)

##### Fin CIEL #####

##### Définition MOMENTALEATOIRE #####

def nouveauMomentAleatoire(intervalle):
    return {
        'momentSuivant': 0,
        'max': intervalle,
        'min': intervalle // 2
    }


def suivant(momentAleatoire, maintenant):
    momentAleatoire['momentSuivant'] = maintenant + random.randint(momentAleatoire['min'], momentAleatoire['max'])


def estExpire(momentAleatoire, maintenant):
    return momentAleatoire['momentSuivant'] <= maintenant

##### Fin MOMENTALEATOIRE #####

##### Définition BOUILLOIRE #####

def nouvelleBouilloire(intervalle):
    return {
        'haut': nouveauMomentAleatoire(abs(1000 * NUAGE_LARGEUR // ventHaut(ciel))),
        'bas': nouveauMomentAleatoire(abs(1000 * NUAGE_LARGEUR // ventBas(ciel))),
        'autre': nouveauMomentAleatoire(intervalle),
        'zones': {'haut', 'bas', 'autre'}
    }
    

def lancer_entite(entite):
    reveille(entite)
    ajouteEntite(scene, entite)


def faitNuage(bouilloire, maintenant):
    for zone in bouilloire['zones']:
        moment = bouilloire[zone]
        if estExpire(moment, maintenant):
            suivant(moment, maintenant)
            if zone == 'haut':
                nuage = nouveauNuageHaut(ciel, IMAGE_NUAGE)
                lancer_entite(nuage)
            elif zone == 'bas':
                nuage = nouveauNuageBas(ciel, IMAGE_NUAGE)
                lancer_entite(nuage)
            else:
                couloir = random.randint(1, COULOIRS_AERIENS)
                if nombre_items_scene < NOMBRE_ITEMS_MAX and random.randint(0,4) == 0 :
                    item = nouveauItem(ciel, couloir, IMAGE_ITEM)
                    lancer_entite(item)
                else:
                    nuage = nouveauNuage(ciel, couloir, IMAGE_NUAGE)
                    lancer_entite(nuage)

##### Fin BOUILLOIRE #####

def traite_entrees():
    global fini, enJeu
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.KEYDOWN:
            if enJeu:
                positionOiseau = position(oiseau)
                place(oiseau, positionOiseau[0], positionOiseau[1] + DEPLACEMENT_HAUT)
                vitesse(oiseau, 0, 0)
                if not estEnAnimation(oiseau):
                    commenceAnimation(oiseau, 'vol')
            else:
                enJeu = True
                arreteAnimation(oiseau)
                prendsPose(oiseau, 'AILE_MILIEU')
                acceleration(oiseau, ACC_CHUTE[0], ACC_CHUTE[1])
                reinitialiser(score)


def enScene():
    for acteur in acteurs(scene):
        if acteur != oiseau and rectangle(acteur).right < 0:
            enleveEntite(scene, acteur)


pygame.init()

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)
pygame.display.set_caption('FLAPPY')

oiseau = nouvelleEntite()
for nom_image, nom_fichier in (('AILE_HAUTE','bird_wing_up.png'),
                               ('AILE_MILIEU','bird_wing_mid.png'),
                               ('AILE_BASSE', 'bird_wing_down.png')):
    chemin = 'images/' + nom_fichier
    image = pygame.image.load(chemin).convert_alpha(fenetre)
    image = pygame.transform.scale(image, (FLAPPY_LARGEUR, FLAPPY_HAUTEUR))
    ajoutePose(oiseau, nom_image, image)

IMAGE_NUAGE = pygame.image.load('images/cloud.png').convert_alpha(fenetre)
IMAGE_NUAGE = pygame.transform.scale(IMAGE_NUAGE, (NUAGE_LARGEUR, NUAGE_HAUTEUR))
IMAGE_ITEM = pygame.image.load('images/item.png').convert_alpha(fenetre)
IMAGE_ITEM = pygame.transform.scale(IMAGE_ITEM, (ITEM_SIZE, ITEM_SIZE))


animation = nouvelleAnimation()
ajouteMouvement(animation, mouvement('AILE_HAUTE', 80))
ajouteMouvement(animation, mouvement('AILE_MILIEU', 80))
ajouteMouvement(animation, mouvement('AILE_BASSE', 80))
ajouteMouvement(animation, mouvement('AILE_MILIEU', 80))

ajouteAnimation(oiseau, 'vol', animation)

place(oiseau, 50, 50)

scene = nouvelleScene()
ajouteEntite(scene, oiseau)

commenceAnimation(oiseau, 'vol', 0)

ciel = nouveauCiel(COULOIRS_AERIENS)

changeVentHaut(ciel, random.randint(NUAGE_VITESSE_MIN, NUAGE_VITESSE_MAX))
changeVentBas(ciel, random.randint(NUAGE_VITESSE_MIN, NUAGE_VITESSE_MAX))
for coul in rangeCouloirs(ciel):
    changeVitesseVent(ciel, coul, random.randint(NUAGE_VITESSE_MIN, NUAGE_VITESSE_MAX))

bouilloire = nouvelleBouilloire(INTERVALLE_NUAGES)

police_caractere = pygame.font.SysFont('monospace', 24, True)
message = police_caractere.render("N'importe quelle touche pour commencer/voler", True, ORANGE)
messageLargeur, messageHauteur = police_caractere.size("N'importe quelle touche pour commencer/voler")

fini = False
enJeu = False
score = score()
temps = pygame.time.Clock()

nombre_items_scene = 0

while not fini:
    # --- Traiter entrées joueur
    traite_entrees()

    maintenant = pygame.time.get_ticks()

    miseAJour(scene, maintenant)
    if enJeu:
        miseAJourScore(score, maintenant)
        faitNuage(bouilloire, maintenant)

    fenetre.fill(BLEU_CIEL)
    enScene()
    affiche(scene, fenetre)
    affichageScore = str(resultat(score)) + ' m'
    marquoir = police_caractere.render(affichageScore, True, ORANGE)
    marquoirLargeur, marquoirHauteur = police_caractere.size(affichageScore)
    fenetre.blit(marquoir, ((FENETRE_LARGEUR - marquoirLargeur) // 2, 10))
    if not enJeu:
        fenetre.blit(message, ((FENETRE_LARGEUR - messageLargeur) // 2, (FENETRE_HAUTEUR - messageHauteur) // 2))
    pygame.display.flip()

    temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()
