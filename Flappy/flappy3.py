import pygame
import random

BLEU_CIEL = (135, 206, 250)
ORANGE    = (255, 165,   0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 550

FLAPPY_LARGEUR = 60
FLAPPY_HAUTEUR = 51

NUAGE_LARGEUR = 127
NUAGE_HAUTEUR = 75

ACC_CHUTE = (0, FENETRE_HAUTEUR) # pixel/s^2
DEPLACEMENT_HAUT = -FENETRE_HAUTEUR / 25
VITESSE_HORIZONTALE = 4 # m/s

COULOIRS_AERIENS = 5
NUAGE_VITESSE_MIN = FENETRE_LARGEUR // 10 # pixel/s
NUAGE_VITESSE_MAX = FENETRE_LARGEUR // 2

INTERVALLE_NUAGES = 1000 # ms

VIEILLISEMENT = 10 # /s

BARRE_LARGEUR = 50
BARRE_HAUTEUR = 20
BARRE_GAUCHE = FENETRE_LARGEUR - BARRE_LARGEUR - 50
BARRE_DESSUS = 50

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
    acteurs = scene['acteurs']
    if entite in acteurs:
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


def faitNuage(bouilloire, maintenant):
    for zone in bouilloire['zones'] if enJeu else {'haut', 'bas'}:
        moment = bouilloire[zone]
        if estExpire(moment, maintenant):
            suivant(moment, maintenant)
            if zone == 'haut':
                nuage = nouveauNuageHaut(ciel, IMAGE_NUAGE)
            elif zone == 'bas':
                nuage = nouveauNuageBas(ciel, IMAGE_NUAGE)
            else:
                couloir = random.randint(1, COULOIRS_AERIENS)
                nuage = nouveauNuage(ciel, couloir, IMAGE_NUAGE)
            reveille(nuage)
            ajouteEntite(scene, nuage)

##### Fin BOUILLOIRE #####

##### Définition SANTE #####

def nouvelleSante(vieillissement):
    return {
        'taux': vieillissement,
        'derniereEvaluation': 0,
        'valeur': 100
    }


def enVie(sante):
    return sante['valeur'] > 0


def bilan(sante, moment):
    sante['derniereEvaluation'] = moment


def vieillir(sante, maintenant):
    sante['valeur'] -= sante['taux'] * (maintenant - sante['derniereEvaluation']) / 1000
    sante['derniereEvaluation'] = maintenant


def forme(sante):
    return sante['valeur']

##### Fin SANTE #####

##### Définition BARRE #####

def nouvelleBarre(rect, fct_valeur):
    return {
        'rect': rect,
        'fct': fct_valeur
    }

def montre(barre, ecran):
    restant = barre['fct']()
    if restant < 0: restant = 0
    rect = barre['rect']
    largeur_rouge = int(rect.width * (100 - restant) / 100)

    if restant < 100:
        pygame.draw.rect(ecran, (255, 0, 0), (rect.left, rect.top, largeur_rouge, rect.height))
    if restant > 0:
        pygame.draw.rect(ecran, (0, 255, 0), (rect.left+ largeur_rouge, rect.top, rect.width - largeur_rouge, rect.height))

##### Fin BARRE #####

def traite_entrees():
    global fini, enJeu
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            exit()
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
                bilan(sante, pygame.time.get_ticks())


def enScene():
    for acteur in acteurs(scene):
        if acteur != oiseau and rectangle(acteur).right < 0:
            enleveEntite(scene, acteur)


def collision():
    return rectangle(oiseau).collidelist([rectangle(o) for o in acteurs(scene) if o != oiseau]) != -1


def evolueSante():
    rect_oiseau = rectangle(oiseau)
    if rect_oiseau.top < 0 or rect_oiseau.bottom > FENETRE_HAUTEUR or collision():
        if not bruitages.get_busy():# NOUVEAU
            bruitages.play(sons['cri'])      # NOUVEAU
        vieillir(sante, maintenant)
    else:
        bilan(sante, maintenant)


def valeurSante():
    return forme(sante)


pygame.init()

pygame.mixer.init()
sons = {}
sons['cri'] = pygame.mixer.Sound("sons/flappy_cri.wav")
sons['musique'] = pygame.mixer.Sound("sons/background_music.wav")

bruitages = pygame.mixer.Channel(5)

sons['musique'].play(loops=-1)

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

sante = nouvelleSante(VIEILLISEMENT)

IMAGE_NUAGE = pygame.image.load('images/cloud.png').convert_alpha(fenetre)
IMAGE_NUAGE = pygame.transform.scale(IMAGE_NUAGE, (NUAGE_LARGEUR, NUAGE_HAUTEUR))


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

for x in range(0, FENETRE_LARGEUR + NUAGE_LARGEUR, NUAGE_LARGEUR):
    nuage1 = nouveauNuageHaut(ciel, IMAGE_NUAGE)
    pos = position(nuage1)
    place(nuage1, x, pos[1])
    nuage2 = nouveauNuageBas(ciel, IMAGE_NUAGE)
    pos = position(nuage2)
    place(nuage2, x, pos[1])
    ajouteEntite(scene, nuage1)
    ajouteEntite(scene, nuage2)

bouilloire = nouvelleBouilloire(INTERVALLE_NUAGES)

police_caractere = pygame.font.SysFont('monospace', 24, True)
message = police_caractere.render("N'importe quelle touche pour commencer/voler", True, ORANGE)
messageLargeur, messageHauteur = police_caractere.size("N'importe quelle touche pour commencer/voler")

fini = False
enJeu = False
score = score()
temps = pygame.time.Clock()

barre = nouvelleBarre(pygame.Rect(BARRE_GAUCHE, BARRE_DESSUS, BARRE_LARGEUR, BARRE_HAUTEUR), valeurSante)

while not fini:
    # --- Traiter entrées joueur
    traite_entrees()

    maintenant = pygame.time.get_ticks()

    miseAJour(scene, maintenant)
    if enJeu:
        miseAJourScore(score, maintenant)
        evolueSante()
        if not enVie(sante):
            fini = True

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
    else:
        montre(barre, fenetre)

    pygame.display.flip()
    
    temps.tick(50)

message = police_caractere.render("GAME OVER", True, ORANGE)
messageLargeur, messageHauteur = police_caractere.size("GAME OVER")
fenetre.blit(message, ((FENETRE_LARGEUR - messageLargeur) // 2, (FENETRE_HAUTEUR - messageHauteur) // 2))
pygame.display.flip()

sons['musique'].stop()
pygame.time.wait(5000)
pygame.display.quit()
pygame.quit()
exit()
