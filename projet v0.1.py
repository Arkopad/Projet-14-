import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib import animation
import time


"""
L'algorithme utilisé provient du pdf du professeur 'Mecanique_des_Materiaux_Granulaires_16_17.pdf'

Hypothèses persos:
- Les grains sont des sphères de même masse et de même rayon
- On est dans le vide
"""

def trajectoire(POSITION, hauteur_silo, largeur_silo, nb_grains):
    """
    Affiche la trajectoire des grains dans un graphe matplotlib.

    Paramètres
    ==========
    POSITION : np.array, tableau des positions
    hauteur_silo : float, hauteur du silo
    largeur_silo : float, largeur du silo
    nb_grains : int, nombre de grains

    Retour
    ======
    rien
    """
    print("Affichage de la trajectoire...")

    fig, ax = plt.subplots()
    ax.set_xlim(-largeur_silo/10, largeur_silo + largeur_silo/10)
    ax.set_ylim(-hauteur_silo/10, hauteur_silo + hauteur_silo/10)
    
    for grain in range(nb_grains):
        ax.plot(POSITION[:, grain, 0], POSITION[:, grain, 1], label="grain {}".format(grain))
    
    #dessin du silo dans le tableau graphique matplot
    silo = Rectangle((0, 0), largeur_silo, hauteur_silo, fill=False, color="red")
    ax.add_patch(silo)
    plt.grid()
    plt.legend()
    plt.show()

def grain_anime(POSITION, hauteur_silo, largeur_silo, nb_grains, rayon, VOISINAGE):
    """
    Fait une animation de la chute des grains dans le silo.

    Paramètres
    ==========
    POSITION : np.array, tableau des positions
    hauteur_silo : float, hauteur du silo
    largeur_silo : float, largeur du silo
    nb_grains : int, nombre de grains
    rayon : float, rayon des grains

    Retour
    ======
    rien    
    """
    print("Animation en cours...")

    fig, ax = plt.subplots()
    ax.set_xlim(-largeur_silo/10, largeur_silo + largeur_silo/10)
    ax.set_ylim(-hauteur_silo/10, hauteur_silo + hauteur_silo/10)
    ax.set_aspect('equal')

    
    #dessin du silo dans le tableau graphique matplot
    silo = Rectangle((0, 0), largeur_silo, hauteur_silo, fill=False, color="red")
    ax.add_patch(silo)
    
    #dessin des grains dans le tableau graphique matplot
    grains = []
    texts = []
    for grain in range(nb_grains):
        grains.append(ax.add_patch(patches.Circle((POSITION[0, grain, 0], POSITION[0, grain, 1]), radius=rayon, fill=True, color='black')))
        texts.append(ax.text(POSITION[0, grain, 0], POSITION[0, grain, 1], str(grain), ha='center', va='center', fontsize=8, color='white'))
    
    time_text = ax.text(0.05, 0.99, '', transform=ax.transAxes, verticalalignment='top', fontsize=12)
    def animate(i):
        #Affiche l'indice du temps en haut a gauche de l'écran:
        time_text.set_text(f'Indice temps: {i*1e0}, voisins de 0: {VOISINAGE[i]}')
        for grain in range(nb_grains):
            grains[grain].center = (POSITION[i, grain, 0], POSITION[i, grain, 1])
            texts[grain].set_position((POSITION[i, grain, 0], POSITION[i, grain, 1]))
        return grains + texts + [time_text]
    
    ani = animation.FuncAnimation(fig, animate, frames=int(POSITION.shape[0]/1e0), interval=1, blit=True)
    plt.show()



def calcul_allongement_normal(vitesse_i, vitesse_j, position_i, position_j, rayon_i, rayon_j):
    """
    Calcul de l'allongement/distance normal à partir de l'équation
    Paramètres
    ==========
    vitesse_i : np.array, vitesse du grain i
    vitesse_j : np.array, vitesse du grain j
    position_i : np.array, position du grain i
    position_j : np.array, position du grain j
    rayon_i : float, rayon du grain i
    rayon_j : float, rayon du grain j

    Retour
    ======
    allongement_normal : float, allongement normal entre les grains i et j
    """
    return np.linalg.norm(position_i - position_j) - (rayon_i + rayon_j)

def calcul_derivee_allongement_normal(i, j, VITESSE, indice_temps):
    """
    Calcul de la dérivée de l'allongement/distance normal à partir de l'équation
    Paramètres
    ==========
    i : int, indice du grain i
    j : int, indice du grain j
    VITESSE : np.array, tableau des vitesses
    indice_temps : int, indice du temps actuel

    Retour
    ======
    derivee_allongement : float,  dérivéée de l'allongement normal entre les grains i et j permettant ensuite de calculer l'amortissement 
    """

    #Si les particules ne sont pas en contact on ne fait rien:
    if calcul_allongement_normal(vitesse_i=VITESSE[indice_temps][i][:],
                              vitesse_j=VITESSE[indice_temps][j][:],
                              position_i=POSITION[indice_temps][i][:],
                              position_j=POSITION[indice_temps][j][:],
                              rayon_i=rayon,
                              rayon_j=rayon) > 0:
        return 0

    #Sinon on continue et on calcule la dérivée de l'allongement normal
    else:
        vecteur_normal = (POSITION[indice_temps,i] - POSITION[indice_temps,j])/np.linalg.norm(POSITION[indice_temps,i] - POSITION[indice_temps,j])
        vitesse_relative = VITESSE[indice_temps,i] - VITESSE[indice_temps,j]
        derivee_allongement = np.dot(vitesse_relative, vecteur_normal) * vecteur_normal
        
    return derivee_allongement


def calcul_allongement_tangentiel(i, j, indice_temps, pas_de_temps, VITESSE, POSITION):
    """
    Calcul de l'allongement tangentielle à partir de l'équation

    Paramètres
    ==========
    i : int, indice du grain i
    j : int, indice du grain j
    indice_temps : int, indice du temps actuel
    pas_de_temps : float, pas de temps
    VITESSE : np.array, tableau des vitesses
    POSITION : np.array, tableau des positions

    Retour
    ======
    allongement_tangentiel : float, allongement tangentiel entre les grains i et j
    """
    #print("Contact!")
    #(4.8): d/dt(delta_t) = (vitesse_i - vitesse_j)*tangente 
    # C'est le produit vectorielle de la différence de vitesse sur la tangente du contact entre les deux grains i et j
    #C'est cette formule (4.8) qu'il faut intégrer temporellement en utilisant les données des vitesses(tableaux numpy)
    #On calcul ensuite l'allongement tangentielle via la formule (4.8)
    #Pour ca on cherche le moment d'impact:
    #On cherche le moment d'impact en cherchant le moment ou la distance normal est nulle
    k = 0 # car on sait que c'est déjà le cas
    while calcul_allongement_normal(vitesse_i=VITESSE[indice_temps-k, i],
                          vitesse_j=VITESSE[indice_temps-k, j],
                          position_i=POSITION[indice_temps-k, i],
                          position_j=POSITION[indice_temps-k, j],
                          rayon_i=rayon,
                          rayon_j=rayon) < 0 and k < indice_temps:
        k += 1
    #On a donc trouvé le moment d'impact avec moment = indice_temps-k, NB: si k = 0 alors impact a lieu à indice_temps
    impact = indice_temps - k
    #On peut calculer le tableau des vitesses tangentielles:
    produit_scalaire_array = np.zeros(indice_temps+1) #tableau 1D car projection sur la tangente, 
    #indice_temps+1, parce que plus lisible pour les indices,
    #autrement dit on aura que des zeros jusqu'a l'indice indice_temps-impact
    global debug
    if debug:
        debug_text = "dans la fonction de l'allongement on a:\n" + f"entre le grain i et j: {i} {j}\n" + f"k vaut: {k}"
        
    for tps_actuel in range(impact, indice_temps+1):
        vecteur_normal = (POSITION[tps_actuel,i] - POSITION[tps_actuel,j])/np.linalg.norm(POSITION[tps_actuel,i] - POSITION[tps_actuel,j])
        #On veut connaître le sens du vecteur tangent qui doit être dans la même direction que la vitesse absolue
        vecteur_tangent = np.array([-vecteur_normal[1], vecteur_normal[0]])
        if np.dot(vecteur_tangent, VITESSE[tps_actuel,i]) < 0:
            vecteur_tangent = -vecteur_tangent
        vitesse_relative = VITESSE[tps_actuel,i] - VITESSE[tps_actuel,j]
        produit_scalaire = np.dot(vitesse_relative, vecteur_tangent)
        produit_scalaire_array[tps_actuel] = produit_scalaire
        
        if debug:
            debug_text += f"tps actuel: {tps_actuel}\n" + f"position i: {POSITION[tps_actuel,i]}\n" + f"position j: {POSITION[tps_actuel,j]}\n" + f"norme tangentielle:{norme_tangentielle_array}\n"
        
    
    if debug:    
        #debug
        global debug_name
        with open(f"{debug_name}.txt", "a") as fichier:
            fichier.write(debug_text)
        
    #On doit maintenant intégrer la valeur de la vitesse tangentielle sur le temps
    allongement_tangentiel = 0
    for i in range(len(produit_scalaire_array)):
        allongement_tangentiel += produit_scalaire_array[i]
    allongement_tangentiel *= pas_de_temps
    return allongement_tangentiel

def application_efforts_distance(masse):
    """
    Application des efforts à distance (par exemple la pesanteur).

    Paramètres
    ==========
    masse : float, masse du grain

    Retour
    ======
    forces : np.array, forces appliquée au grain
    """
    return np.array([0, -masse*9.81])
    

def voisinage(i, POSITION, GRILLE, c, indice_temps):
    """
    Détermine la liste de voisinage du grain i

    Paramètres
    ==========
    i : int, indice du grain i
    POSITION : np.array, tableau des positions
    GRILLE : np.array, grille d'espace
    c : float, pas d'espace
    indice_temps : int, indice du temps

    Retour
    ======
    grains_voisins : np.array, tableau des indices des grains en contact avec le grain i
    """
    x = int(POSITION[indice_temps,i,0]/c)
    y = int(POSITION[indice_temps,i,1]/c)
    voisinage = []
    for voisin in GRILLE[x, y]:
        if voisin != i:
            voisinage.append(voisin)

    for j in range(-1, 2):
        for k in range(-1, 2):
            if not(j == 0 and k == 0):
                case_voisine_x, case_voisine_y = int(POSITION[indice_temps,i,0]/c)+j, int(POSITION[indice_temps,i,1]/c)+k
                if (case_voisine_x, case_voisine_y) in GRILLE.keys():
                    voisinage += GRILLE[case_voisine_x, case_voisine_y]
    
    deja_vu = []
    for voisin in voisinage:
        if voisin in deja_vu:
                print("WOW")
                print("indice temps: ", indice_temps)
                print("indice grain: ", i)
                print("voisinage: ", voisinage)
                print("grille: ", GRILLE)
                exit()
        deja_vu.append(voisin)

    return voisinage






















def algoprincipal(POSITION, VITESSE, ACCELERATION, VITESSE_DEMI_PAS, nb_grains, nb_temps, pas_de_temps, rayon, masse, raideur_tangentielle, indice_temps, temps, hauteur_silo, largeur_silo, raideur_mur):
    """
    Algorithme principal
    
    Paramètres
    ==========
    POSITION : np.array, tableau des positions
    VITESSE : np.array, tableau des vitesses
    ACCELERATION : np.array, tableau des accélérations
    VITESSE_DEMI_PAS : np.array, tableau des vitesses à temps k+1/2
    nb_grains : int, nombre de grains
    nb_temps : int, nombre de temps
    pas_de_temps : float, pas de temps
    rayon : float, rayon des grains
    masse : float, masse des grains
    raideur_tangentielle : float, raideur tangentielle
    indice_temps : int, indice du temps actuel
    temps : float, temps actuel
    hauteur_silo : float, hauteur du silo
    largeur_silo : float, largeur du silo
    raideur_mur : float, raideur du mur

    Retour
    ======
    rien
    """

    start_time = time.time()
    VOISINAGE = [0 for i in range(nb_temps)]

    while indice_temps < nb_temps-1:
        #Actualisation du temps
        temps += pas_de_temps
        indice_temps += 1
        if indice_temps % 1000 == 0:
            print("indice_temps ", indice_temps, "/", nb_temps)
            print("temps:", temps)
        
        # Mise a jour des tableaux de position et vitesse à temps k
        for grain in range(nb_grains):
            #Calcul de la nouvelle position du grain
            POSITION[indice_temps, grain, :] = POSITION[indice_temps-1, grain, :] + VITESSE_DEMI_PAS[indice_temps-1, grain, :]*pas_de_temps
    
            
            #Calcul de la vitesse du grain
            VITESSE[indice_temps, grain, :] = VITESSE_DEMI_PAS[indice_temps-1, grain, :] + ACCELERATION[indice_temps-1, grain, :]*pas_de_temps/2

            #On définit une grille pour discrétiser l'espace selon le pas d'espace c, a chaque case on met la liste des grains qui sont dans cette case
            c = 3*rayon #taille de la case
            GRILLE = {(i,j):[] for i in range(-1, int(hauteur_silo/c)+2) for j in range(-1, int(largeur_silo/c)+2)}
            
            #On associe à chaque case de la grille les grains qui sont dans cette case
            for i in range(nb_grains):
                pos_case = (int(POSITION[indice_temps,i,0]/c), int(POSITION[indice_temps,i,1]/c))
                try:
                    GRILLE[pos_case[0], pos_case[1]].append(i)
                except:
                    print("indice_temps", indice_temps)
                    print("case_grille", pos_case)
                    print("i", i)
                    print("POSITION[indice_temps,i,0]", POSITION[indice_temps,i,0])
                    print("POSITION[indice_temps,i,1]", POSITION[indice_temps,i,1])
                            
        # Calcul des efforts de contact pour mise à jour des vitesses à temps k+1/2 et accélérations à temps k
        for grain1 in range(nb_grains):
            #Force à distance = gravité
            force_resultante = np.array([0.0, 0.0])
            force_resultante += application_efforts_distance(masse)

            #Rencontre avec un mur ?
            condition_droite = POSITION[indice_temps][grain1][0] + rayon > largeur_silo
            condition_gauche = POSITION[indice_temps][grain1][0] - rayon < 0
            condition_haut = POSITION[indice_temps][grain1][1] + rayon > hauteur_silo
            condition_bas = POSITION[indice_temps][grain1][1] - rayon < 0

            if condition_droite:
                force_resultante[0] += -raideur_mur * (POSITION[indice_temps][grain1][0] + rayon - largeur_silo)
            if condition_gauche:
                force_resultante[0] += -raideur_mur * (POSITION[indice_temps][grain1][0] - rayon)
            if condition_haut:
                force_resultante[1] += -raideur_mur * (POSITION[indice_temps][grain1][1] + rayon - hauteur_silo)
            if condition_bas:
                force_resultante[1] += -raideur_mur * (POSITION[indice_temps][grain1][1] - rayon)


            
            #Liste de voisinage selon:
            """
            Méthode de partition du conteneur  Cette  méthode  consiste  à  subdiviser  l'ensemble  du  système  selon  une  grille  fixe  (en  deux  ou 
            trois dimensions selon le problème), avec un pas d'espace   donné (Fig. 4.8). Chaque particule 
            a donc son centre qui appartient à une "case", de surface    (respectivement de volume   ), et 
            l'identité  de  cette  case  est  assez  facile  à  déterminer  à  partir  des  coordonnées  du  centre  en 
            question. Ensuite, pour une particule donnée, la liste de voisinage est composée de toutes les 
            particules dont le centre appartient à la même case et à ses cases voisines (au nombre de 8 en 
            Mécanique des matériaux granulaires 2D  et  de  26  en  3D).  La  longueur  du  côté  de  case  peut  être  prise  par  exemple
            Cette méthode est très performante, excepté pour des matériaux fortement 
            polydisperses pour lesquels elle a tendance à  former des listes de voisinage trop longues.  La 
            méthode  peut  également  devenir  très  coûteuse  si  les  particules  sont  très  dispersées  dans 
            l'espace. Elle reste néanmoins la méthode de détection de voisinage la plus répandue.
            """
            voisins = voisinage(i=grain1, POSITION=POSITION, c=c, GRILLE=GRILLE, indice_temps=indice_temps)
            if grain1 == 0:
                VOISINAGE[indice_temps] = voisins
            """
            print("indice_temps", indice_temps)
            print("grain1", grain1)
            print("voisins", voisins)
            print("====================================")
            """

            for grain2 in voisins:
                if grain1 != grain2:
                    #On définit la force de contact entre les deux grains:
                    force_contact = 0

                    allongement_normal = calcul_allongement_normal(vitesse_i=VITESSE[indice_temps, grain1,:],
                                                                   vitesse_j=VITESSE[indice_temps, grain2, :],
                                                                   position_i=POSITION[indice_temps, grain1, :],
                                                                   position_j=POSITION[indice_temps, grain2, :],
                                                                   rayon_i=rayon,
                                                                   rayon_j=rayon)
                    derivee_allongement_normal = calcul_derivee_allongement_normal(grain1, grain2, VITESSE, indice_temps) 
                    #Effort normal
                    if allongement_normal < 0:
                        vecteur_normal = (POSITION[indice_temps, grain1, :] - POSITION[indice_temps, grain2, :])/np.linalg.norm(POSITION[indice_temps, grain1, :] - POSITION[indice_temps, grain2, :])
                        force_contact += -raideur_normale * allongement_normal * vecteur_normal

                        #Effort tangentiel
                        allongement_tangentiel = calcul_allongement_tangentiel(grain1, grain2, indice_temps, pas_de_temps, VITESSE, POSITION)
                        vecteur_normal = (POSITION[indice_temps, grain1, :] - POSITION[indice_temps, grain2, :])/np.linalg.norm(POSITION[indice_temps, grain1, :] - POSITION[indice_temps, grain2, :])
                        vecteur_tangentiel = np.array([-vecteur_normal[1], vecteur_normal[0]])
                        if np.dot(vecteur_tangentiel, VITESSE[indice_temps,grain1]) < 0:
                            vecteur_tangentiel = -vecteur_tangentiel
                        force_contact += -raideur_tangentielle * allongement_tangentiel * vecteur_tangentiel - amortissement * derivee_allongement_normal * vecteur_normal
                
                    # 17. Mise à jour de la résultante des forces sur grain1
                    force_resultante += force_contact
            
            frotemment = -coefficient_de_frottement * VITESSE[indice_temps, grain1, :]
            force_resultante += frotemment

            # Calcul de l'accélération du grain à partir de l'équation (4.1)
            ACCELERATION[indice_temps][grain1] = force_resultante / masse
        
            # Calcul de la vitesse de demi-pas à k+1/2 à partir de l'équation (4.19)
            VITESSE_DEMI_PAS[indice_temps][grain1] = VITESSE_DEMI_PAS[indice_temps-1][grain1] + ACCELERATION[indice_temps][grain1] * pas_de_temps / 2


            #Debug:
            global debug
            if debug:
                global debug_name
                with open(f"{debug_name}.txt", "a") as fichier:
                    fichier.write(f"grain numéro: {grain1}\n")
                    fichier.write(f"indice temps: {indice_temps}\n")
                    fichier.write(f"force résultante: {force_resultante}\n")
                    fichier.write(f"position: {POSITION[indice_temps][grain1]}\n")
                    fichier.write(f"vitesse_demi_temps: {VITESSE_DEMI_PAS[indice_temps][grain1]}\n")
                    fichier.write(f"vitesse: {VITESSE[indice_temps][grain1]}\n")
                    fichier.write(f"acc: {ACCELERATION[indice_temps][grain1]}\n")
                    fichier.write("\n" * 2)

                if indice_temps == 3000:
                    print("Fin de la simulation")
                    trajectoire(POSITION, hauteur_silo, largeur_silo, nb_grains)
                    grain_anime(POSITION, hauteur_silo, largeur_silo, nb_grains)
                    exit()

    # Fin de la boucle principale
    print("Fin de la simulation")
    print("Temps de calcul: ", time.time() - start_time, "secondes")

    #Affichage:
    trajectoire(POSITION, hauteur_silo, largeur_silo, nb_grains)
    grain_anime(POSITION, hauteur_silo, largeur_silo, nb_grains, rayon, VOISINAGE)




if __name__ == "__main__":
    #Définition grain
    nb_grains = 10
    masse = 1e-3 #kg    
    rayon = 1e-2 #m
    raideur_normale = 100 #N/m
    raideur_tangentielle = 50 #N/m
    coefficient_de_frottement = 0.0005 #N/m
    amortissement = 1e-3 #N.s/m
    #Pour le roulement trop compliqué, on utilise leur rotation

    #Définition du silo
    hauteur_silo = 0.3 #m
    largeur_silo = 0.3 #m
    raideur_mur = 1000 #N/m

    #Définition du temps
    temps = 0
    indice_temps = 0
    pas_de_temps = 1e-3 #s
    duree_simulation = 5
    nb_temps = int(duree_simulation/pas_de_temps)

    #ON PLACE LE REPERE EN BAS A GAUCHE (0,0) DU SILO COIN BAS GAUCHE Y VERS LE HAUT.
    #TABLEAUX NUMPY
    POSITION = np.zeros((nb_temps, nb_grains, 2))
    POSITION[0] = np.random.uniform(low=0, high=largeur_silo, size=(nb_grains, 2))
    VITESSE = np.zeros((nb_temps, nb_grains, 2))
    VITESSE[0,:,:] = 0 # pas défini au début, on commece à 1 pour la vitesse et à 0 pour la vitessse de demi pas
    VITESSE_DEMI_PAS = np.zeros((nb_temps, nb_grains, 2))
    VITESSE_DEMI_PAS[0] = np.random.uniform(low=-0.005, high=0.005, size=(nb_grains, 2)) #RAPPEL: Le silo fait un metre par un metre...
    ACCELERATION = np.zeros((nb_temps, nb_grains, 2))
    ACCELERATION[0,:,:] = 0




    #Nom fichier debug:
    debug = int(input("Debug ou pas? entrez 1 ou 0"))
    if debug:
        debug_name = input("Nom du debug:(Wait for user input...)")
    algoprincipal(POSITION, VITESSE, ACCELERATION, VITESSE_DEMI_PAS, nb_grains, nb_temps, pas_de_temps, rayon, masse, raideur_tangentielle, indice_temps, temps, hauteur_silo, largeur_silo, raideur_mur)