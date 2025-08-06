from random import randint
import random
import os
from ship import Ship, create_fleet

grille_joueur1 = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10",
                 "B1","B2","B3","B4","B5","B6","B7","B8","B9","B10",
                 "C1","C2","C3","C4","C5","C6","C7","C8","C9","C10",
                 "D1","D2","D3","D4","D5","D6","D7","D8","D9","D10",
                 "E1","E2","E3","E4","E5","E6","E7","E8","E9","E10",
                 "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10",
                 "G1","G2","G3","G4","G5","G6","G7","G8","G9","G10",
                 "H1","H2","H3","H4","H5","H6","H7","H8","H9","H10",
                 "I1","I2","I3","I4","I5","I6","I7","I8","I9","I10",
                 "J1","J2","J3","J4","J5","J6","J7","J8","J9","J10"]

grille_joueur2 = grille_joueur1.copy()
grille_robot= grille_joueur1.copy()
grille_joueur = grille_joueur1.copy()

ship_list = grille_joueur1.copy()
ships_joueur1= []
ships_joueur2 = []

fleet_joueur1 = create_fleet()
fleet_joueur2 = create_fleet()
fleet_robot = create_fleet()
fleet_joueur = create_fleet()

tirs_joueur1 = []
tirs_joueur2 = []
tirs_joueur = []
tirs_robot = []

bombe_bonus_robot = None
bombe_bonus_joueur = None
bombe_bonus_joueur1 = None
bombe_bonus_joueur2 = None

radar_malus_joueur1 = None
radar_malus_joueur2 = None  
radar_malus_joueur = None
radar_malus_robot = None

radar_malus_actif_joueur1= False
radar_malus_actif_joueur2= False
radar_malus_actif_joueur= False
radar_malus_actif_robot= False

double_coup_joueur1=None
double_coup_joueur2=None
double_coup_joueur=None
double_coup_robot=None

turn = 0

#toutes les variables utiles pour la suite du code sont initialisées ici


def bonus_bombe_cases():
   
   global bombe_bonus_robot, bombe_bonus_joueur, bombe_bonus_joueur1, bombe_bonus_joueur2 
    
   bombe_bonus_robot = random.choice(grille_robot) 
   bombe_bonus_joueur = random.choice(grille_joueur)
   bombe_bonus_joueur1 = random.choice(grille_joueur1)
   bombe_bonus_joueur2 = random.choice(grille_joueur2)   

   return bombe_bonus_robot, bombe_bonus_joueur, bombe_bonus_joueur1, bombe_bonus_joueur2   

def radar_sournois_cases():
    
    global radar_malus_joueur1, radar_malus_joueur2, radar_malus_robot, radar_malus_joueur
    global bombe_bonus_joueur, bombe_bonus_robot, bombe_bonus_joueur1, bombe_bonus_joueur2
    
    while True:
        radar_malus_joueur1 = random.choice(grille_joueur1)
        if radar_malus_joueur1 != bombe_bonus_joueur1:
            break
        
    while True:
        radar_malus_joueur2 = random.choice(grille_joueur2)
        if radar_malus_joueur2 != bombe_bonus_joueur2:
            break
    while True:
        radar_malus_robot = random.choice(grille_robot)
        if radar_malus_robot != bombe_bonus_robot:
            break
    while True:
        radar_malus_joueur = random.choice(grille_joueur)
        if radar_malus_joueur != bombe_bonus_joueur:
            break
    
    return radar_malus_joueur1, radar_malus_joueur2, radar_malus_robot, radar_malus_joueur

def double_coup_cases():
    

    global double_coup_joueur, double_coup_robot, double_coup_joueur1, double_coup_joueur2
    global radar_malus_joueur1, radar_malus_joueur2, radar_malus_robot, radar_malus_joueur
    global bombe_bonus_joueur, bombe_bonus_robot, bombe_bonus_joueur1, bombe_bonus_joueur2

    def get_3_valid_cases(grille, bombe, radar):
        
        cases_valides = [case for case in grille if case != bombe and case != radar]
        return random.sample(cases_valides, 3)

    double_coup_joueur = get_3_valid_cases(grille_joueur, bombe_bonus_joueur, radar_malus_joueur)
    double_coup_robot = get_3_valid_cases(grille_robot, bombe_bonus_robot, radar_malus_robot)
    double_coup_joueur1 = get_3_valid_cases(grille_joueur1, bombe_bonus_joueur1, radar_malus_joueur1)
    double_coup_joueur2 = get_3_valid_cases(grille_joueur2, bombe_bonus_joueur2, radar_malus_joueur2)
    
def change_player():
    print("CHANGEMENT DE JOUEUR\nDonnez la souris au joueur suivant...")
    input("Appuyez sur Entrée pour continuer à jouer...")
    clear_console()
    
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
# cette fonction permet d'effacer la console

def afficher_grille(grille, bonus, tirs=None, ships=None, masquer_bateau=True):

     
    # Ajout des numéros de colonnes en haut
    print("    1   2   3   4   5   6   7   8   9  10 ")
    print("  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐")
    
    # Lignes A à J
    lignes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for ligne in lignes:
        print(f"{ligne} │", end="")
        for col in range(1, 11):
            case = f"{ligne}{col}"
            # Afficher la case si elle est disponible dans la grille
            if case in grille:
                print(f" O │", end="")
            else:
                print(f"   │", end="")
        print()  # Nouvelle ligne
        
        # Ligne de séparation (sauf après la dernière ligne)
        if ligne != "J":
            print("  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤")
        else:
            print("  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘")
# cette fonction permet d'afficher la grille 10X10 de chaque joueur, avec les coordonnées des cases

def afficher_grille_avec_symboles(grille, bonus, tirs, fleet, masquer_bateau=True,position_torpilleur_révélée=False):
  
    print("                                           ")
    print("    1   2   3   4   5   6   7   8   9  10 ")
    print("  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐")
    
    # Créer un dictionnaire position -> ship pour un accès rapide
    position_to_ship = {}
    for ship in fleet:
        for pos in ship.positions:
            position_to_ship[pos] = ship
    
    # Lignes A à J
    lignes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for ligne in lignes:
        print(f"{ligne} │", end="")
        for col in range(1, 11):
            case = f"{ligne}{col}"
            
            # Déterminer le symbole à afficher pour cette case
            if case in tirs and case in position_to_ship:
                symbole = "$"  # Bateau touché
            elif case in tirs:
                symbole = "X"  # Tir raté
            elif case in position_to_ship and not masquer_bateau:
                # Afficher le symbole spécifique du bateau
                symbole = position_to_ship[case].symbol
            elif case in position_to_ship and masquer_bateau and position_torpilleur_révélée:
                ship = position_to_ship[case]
                if ship.size == 2:
                    symbole = ship.symbol
                    
                    # Permet d'afficher la position du Torpilleur en cas de malus
                    
                else:
                    symbole = "~" #Eau
            else:
                symbole = "~"  # Eau
                
            print(f" {symbole} │", end="")
        print()  # Nouvelle ligne
        
        # Ligne de séparation (sauf après la dernière ligne)
        if ligne != "J":
            print("  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤")
        else:
            print("  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘")
# Cette fonction permet d'afficher les grilles de chacun avec des symboles, selon l'état du jeu

def m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2):
    
    clear_console()
    print("=== BATAILLE NAVALE 10x10 ===\n")
    print("=== MODE 2 JOUEURS ===\n")
    
    if turn % 2 == 0:
        print("C'est le tour du Joueur 1")
        
        print("Votre grille (joueur 1):")
        afficher_grille_avec_symboles(grille_joueur1,bombe_bonus_joueur2, tirs_joueur2, fleet_joueur1, masquer_bateau=False, position_torpilleur_révélée=radar_malus_actif_joueur2)
        
        print("\nGrille adverse (joueur 2):")
        afficher_grille_avec_symboles(grille_joueur2, bombe_bonus_joueur1, tirs_joueur1, fleet_joueur2, masquer_bateau=True, position_torpilleur_révélée=radar_malus_actif_joueur1)
        
    else:
        print("C'est le tour du Joueur 2")
        
        print("Votre grille (joueur 2):")
        afficher_grille_avec_symboles(grille_joueur2, bombe_bonus_joueur1, tirs_joueur1, fleet_joueur2, masquer_bateau=False, position_torpilleur_révélée=radar_malus_actif_joueur1)
        
        print("\nGrille adverse (joueur 1):")
        afficher_grille_avec_symboles(grille_joueur1, bombe_bonus_joueur2, tirs_joueur2, fleet_joueur1, masquer_bateau=True, position_torpilleur_révélée=radar_malus_actif_joueur2)
    
        
    print("\nLégende:  ~ = eau, X = tir raté, $ = bateau touché")
    print("Vos bateaux: P = Porte-avions (5), C = Croiseur (4), D = Contre-torpilleur (3), S = Sous-marin (3), T = Torpilleur (2)")
    print(f"Tour: {turn + 1}, {'Joueur 1' if turn % 2 == 0 else 'Joueur 2'} joue")
    print("---------------------------\n")
    print("BONUS DE LA BOMBE MALEFIQUE : IL permet de faire exploser toutes les cases adjacentes à la case choisie en même temps que cette dernière !\n")
    print("MALUS DU RADAR SOURNOIS : Il révèle la position de votre Torpilleur (2 cases) à tous le monde !\n")
    print("BONUS DU DOUBLE COUP (3 CASES) : Il permet de pouvoir retirer un missile !\n")
    print("---------------------------\n")
    
    if radar_malus_actif_joueur1 :
        print("Attention, le radar sournois du joueur 1 est actif, la position du Torpilleur du joueur 1 est désormais dévoilée !\n")      
    if radar_malus_actif_joueur2 :
        print("Attention, le radar sournois du joueur 2 est actif, la position du Torpilleur du joueur 2 est désormais dévoilée !\n")
        
                 
# Cette fonction permet d'afficher l'état complet du jeu, en tout temps

def m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot):
    
    clear_console()
    print("=== BATAILLE NAVALE 10x10 ===\n")
    print("=== MODE ROBOT vs JOUEUR ===\n")
    
    
    print("Grille du Robot (adversaire):")
    afficher_grille_avec_symboles(grille_robot, bombe_bonus_joueur, tirs_joueur, fleet_robot, masquer_bateau=True, position_torpilleur_révélée=radar_malus_actif_joueur)
        
    print("\nVotre Grille:")
    afficher_grille_avec_symboles(grille_joueur, bombe_bonus_robot, tirs_robot, fleet_joueur, masquer_bateau=False, position_torpilleur_révélée=radar_malus_actif_robot)
        
    print("\nLégende:  ~ = eau, X = tir raté, $ = bateau touché")
    print("Vos bateaux: P = Porte-avions (5), C = Croiseur (4), D = Contre-torpilleur (3), S = Sous-marin (3), T = Torpilleur (2)")
    print(f"Tour: {turn + 1}, {'Joueur' if turn % 2 == 0 else 'Robot'} joue")
    print("---------------------------\n")
    print("BONUS DE LA BOMBE MALEFIQUE : IL permet de faire exploser toutes les cases adjacentes à la case choisie en même temps que cette dernière !\n")
    print("MALUS DU RADAR SOURNOIS : Il révèle la position de votre Torpilleur (2 cases) à tous le monde !\n")
    print("BONUS DU DOUBLE COUP (3 CASES) : Il permet de pouvoir retirer un missile !\n")
    print("---------------------------\n")
    
    if radar_malus_actif_joueur :
        print("Attention, le radar sournois du joueur  est actif, la position du Torpilleur du joueur est désormais dévoilée !\n")      
    if radar_malus_actif_robot :
        print("Attention, le radar sournois du robot est actif, la position du Torpilleur du robot est désormais dévoilée !\n")
           
        
# Cette fonction permet d'afficher l'état complet du jeu, en tout temps

def game_start_principal():
    
    # Programme principal
    clear_console()
    afficher_type_jeu()
    # Cette fonction permet de choisir le type de jeu, soit 2 joueurs, soit robot vs joueur


def afficher_type_jeu():
    
    clear_console()
    print("=== BATAILLE NAVALE 10x10 ===\n")
    
    print("Bienvenue dans le jeu de la bataille navale !\n")
    print("== CHOIX DU MODE DE JEU ==\n")
    choix=input("Veillez choisir l'option souhaitée :\n1. Mode 2 joueurs\n2. Mode Robot vs Joueur\nEntrez votre choix (1 ou 2): ")
    clear_console()
    bonus_bombe_cases()
    radar_sournois_cases()
    double_coup_cases()
    
    # Vérification du choix de l'utilisateur

    if choix == "1":
        print("Vous avez choisi le mode 2 joueurs.")
        input("Appuyez sur Entrée pour continuer...")
        m1_game_start(bombe_bonus_joueur1, bombe_bonus_joueur2, radar_malus_joueur1, radar_malus_joueur2, double_coup_joueur1, double_coup_joueur2)
        
    elif choix == "2":
        print("Vous avez choisi le mode Robot vs Joueur.")
        input("Appuyez sur Entrée pour continuer...")
        m2_game_start(bombe_bonus_joueur, bombe_bonus_robot, radar_malus_joueur, radar_malus_robot, double_coup_joueur, double_coup_robot)
        
    else:
        print("Choix invalide. Veuillez réessayer.")
        input("Appuyez sur Entrée pour continuer...")
        afficher_type_jeu()
# Cette fonction permet de choisir le type de jeu, soit 2 joueurs, soit robot vs joueur


def m1_place_ships_joueur1():
    

    for i, ship in enumerate(fleet_joueur1):
        placed = False
        while not placed:
            try:
                m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                print(f"Placement du {ship.name} ({ship.size} cases)")
                print(f"Bateau {i+1}/5")
                case_choisie = input(f"Joueur 1, choisissez la case de départ pour votre {ship.name} [A1-J10]: ")
                    
                if case_choisie not in grille_joueur1:
                    print("Attention, veuillez insérer une case valide !")
                    input("Appuyez sur Entrée pour continuer...")
                    continue
                    
                orientation = input("Orientation (H)orizontale ou (V)erticale: ").upper()
                if orientation not in ['H', 'V']:
                    print("Veuillez entrer H ou V")
                    input("Appuyez sur Entrée pour continuer...")
                    continue
                    
                orientation = 'horizontal' if orientation == 'H' else 'vertical'
                ship.place(case_choisie, orientation)
                    
                if ship.is_valid_placement(grille_joueur1, fleet_joueur1[:i]):
                    placed = True
                else:
                    print("Placement invalide (hors grille ou chevauchement)")
                    input("Appuyez sur Entrée pour continuer...")
                        
            except Exception as e:
                print("Erreur : Veuillez réessayer.")
                input("Appuyez sur Entrée pour continuer...")
                    
    print("Tous les bateaux du Joueur 1 sont placés !")
    input("Appuyez sur Entrée pour passer au placement de la flotte du Joueur 2... ")
    
                    
    return True
                
    
     
                
# Cette fonction permet de valider si le choix du joueur est conforme ou non + de lui demander d'inscrire un numéro

        

def m1_place_ships_joueur2():
    
   
        
    for i, ship in enumerate(fleet_joueur2):
        placed = False
        while not placed:
            try:
                m1_afficher_jeu(radar_malus_actif_joueur1,radar_malus_actif_joueur2)
                print(f"Placement du {ship.name} ({ship.size} cases)")
                print(f"Bateau {i+1}/5")
                case_choisie = input(f"Joueur 2, choisissez la case de départ pour votre {ship.name} [A1-J10]: ")
                    
                if case_choisie not in grille_joueur2:
                    print("Attention, veuillez insérer une case valide !")
                    input("Appuyez sur Entrée pour continuer...")
                    continue
                    
                orientation = input("Orientation (H)orizontale ou (V)erticale: ").upper()
                if orientation not in ['H', 'V']:
                    print("Veuillez entrer H ou V")
                    input("Appuyez sur Entrée pour continuer...")
                    continue
                    
                orientation = 'horizontal' if orientation == 'H' else 'vertical'
                ship.place(case_choisie, orientation)
                    
                if ship.is_valid_placement(grille_joueur2, fleet_joueur2[:i]):
                    placed = True
                    print("Placement réussi !")
                    input("Appuyez sur Entrée pour continuer...")
                else:
                    print("Placement invalide (hors grille ou chevauchement)")
                    input("Appuyez sur Entrée pour continuer...")
                        
            except Exception as e:
                print("Erreur : Veuillez réessayer.")
                input("Appuyez sur Entrée pour continuer...")
    
    print("Tous les bateaux du Joueur 2 sont placés !")
    input("Appuyez sur Entrée pour commencer la partie...")
                    
    return True
                
# Cette fonction permet de valider si le choix du joueur est conforme ou non + de lui demander d'inscrire un numéro

def m2_place_ships_joueur():
    
    for i, ship in enumerate(fleet_joueur):
        placed = False
        while not placed:
            try:
                m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                print(f"Placement du {ship.name} ({ship.size} cases)")
                print(f"Bateau {i+1}/5")
                case_choisie = input(f"Choisissez la case de départ pour votre {ship.name} [A1-J10]: ")
                
                if case_choisie not in grille_joueur:
                    print("Attention, veuillez insérer une case valide !")
                    input("Appuyez sur Entrée pour continuer...")
                    continue
                
                orientation = input("Orientation (H)orizontale ou (V)erticale: ").upper()
                if orientation not in ['H', 'V']:
                    print("Veuillez entrer H ou V")
                    input("Appuyez sur Entrée pour continuer...")
                    continue
                
                orientation = 'horizontal' if orientation == 'H' else 'vertical'
                ship.place(case_choisie, orientation)
                
                if ship.is_valid_placement(grille_joueur, fleet_joueur[:i]):
                    placed = True
                    
                else:
                    print("Placement invalide (hors grille ou chevauchement)")
                    input("Appuyez sur Entrée pour continuer...")
                    
            except Exception as e:
                print("Erreur : Veuillez réessayer.")
                input("Appuyez sur Entrée pour continuer...")
    
    print("Tous vos bateaux sont placés !")
    input("Appuyez sur Entrée pour passer au placement de la flotte du robot...")
    
# Cette fonction permet de valider si le choix du joueur est conforme ou non + de lui demander d'inscrire un numéro

def m2_place_ships_robot():
    
    for i, ship in enumerate(fleet_robot):
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            case_robot = random.choice(ship_list)
            orientation = random.choice(['horizontal', 'vertical'])
            ship.place(case_robot, orientation)
            
            if ship.is_valid_placement(grille_robot, fleet_robot[:i]):
                placed = True
            attempts += 1
        
        if not placed:
            print("Erreur: Impossible de placer tous les bateaux du robot")
            return False
    
    print("Tous les bateaux du robot sont placés !")
    input("Appuyez sur Entrée pour commencer la partie...")
    
    return True
        
    

def m1_joueur1_play(bombe_bonus_joueur1, radar_malus_joueur1, double_coup_joueur1):
    
    global radar_malus_actif_joueur1, radar_malus_actif_joueur2

    while True:
        try:
            m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
            choix = input(f"Joueur 1, choisissez sur quelle case votre missile va être lancé [A1-J10]: ")
            
            if choix == bombe_bonus_joueur1:                                        #Permet la fonction bonus : Bombe maléfique
                
                        
                if bombe_bonus_joueur1 in grille_joueur2 and bombe_bonus_joueur1 not in fleet_joueur2 :
                    print(f"Vous avez touché la case {bombe_bonus_joueur1}, c'est un bonus !\n Tous les cases adjacentes sont considérées comme touchées !\n")
                    input("Appuyez sur Entrée pour continuer...")
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                                if i == 0 and j == 0:
                                    continue
                                adj_case = chr(ord(bombe_bonus_joueur1[0]) + i) + str(int(bombe_bonus_joueur1[1:]) + j)
                                if adj_case in grille_joueur2 and adj_case not in tirs_joueur1:
                                    tirs_joueur1.append(adj_case)
                                    for ship in fleet_joueur2:
                                        ship.hit(adj_case)
                                tirs_joueur1.append(bombe_bonus_joueur1)
                                for ship in fleet_joueur2:
                                    ship.hit(bombe_bonus_joueur1)     
                                        
                        m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                        print("BONUS ACTIF!")
                        change_player()   
                        return False
                
                                    
                elif any(bombe_bonus_joueur1 in ship.positions for ship in fleet_joueur2):  
                    print(f"Vous avez touché la case {bombe_bonus_joueur1}, c'est un BONUS !\n Tous les cases adjacentes sont considérées comme touchées !\n")
                    input("Appuyez sur Entrée pour continuer...")
                                    
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            adj_case = chr(ord(bombe_bonus_joueur1[0]) + i) + str(int(bombe_bonus_joueur1[1:]) + j)
                            if adj_case in grille_joueur2 and adj_case not in tirs_joueur1:
                                tirs_joueur1.append(adj_case)
                                for ship in fleet_joueur2:
                                    ship.hit(adj_case)
                            tirs_joueur1.append(bombe_bonus_joueur1)
                            for ship in fleet_joueur2:
                                ship.hit(bombe_bonus_joueur1) 
                                        
                                                    
                        m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                        print("BONUS ACTIF!")
                        change_player()
                        return False
                        
                        
            elif  choix == radar_malus_joueur1:                              #Permet la fonction malus : radar sournois
                
                if radar_malus_joueur1 in grille_joueur2:
                    print(f"Vous avez touché la case {radar_malus_joueur1}, c'est un MALUS !\n La position de votre torpilleur (2 cases) sera maintenant révélée à tous !\n")
                    radar_malus_actif_joueur1=True #Active le malus
                    input("Appuyez sur Entrée pour continuer...")
                    if radar_malus_joueur1 not in tirs_joueur1:
                        tirs_joueur1.append(radar_malus_joueur1)
                        
                    for ship in fleet_joueur1:
                        if ship.size == 2:
                            print(f"La position de {ship.name} est révélée : {ship.positions}\n")
                            print("MALUS ACTIF!\n")
                    #Permet d'afficher la position de son propre torpilleur 
                            
                    for ship in fleet_joueur2:
                        ship.hit(radar_malus_joueur1)
                        
                    #Permet de vérifier si un bateau est touché chez l'adversaire    
                    change_player() 
                    return False
                            
                                 
                else: 
                    print("Attention, veuillez insérer une case valide !")
                    input("Appuyez sur Entrée pour continuer...")
                    
            elif choix in double_coup_joueur1:
                    
                    if choix in grille_joueur2 :
                        print(f"Vous avez tiré sur la case {choix}, c'est un BONUS !\n Vous avez donc la chance de pouvoir retirer !\n")
                        input("Appuyer sur Entrée pour activer le BONUS...")

                       
                        if choix not in tirs_joueur1:
                            tirs_joueur1.append(choix)
                            touche = False
                            bateau_touche = None
                                
                            for ship in fleet_joueur2:
                                    if ship.hit(choix):
                                        touche = True
                                        bateau_touche = ship
                                        break
                            if touche:
                                m2_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                                print("Touché !")
                                if bateau_touche.is_sunk():
                                    print(f"Le {bateau_touche.name} ennemi est coulé !")
                                    input(f"Appuyez sur Entrée pour continuer...")
                                    
                                    
                                if all(ship.is_sunk() for ship in fleet_robot):
                                    print("Joueur, vous remportez la partie, tous les bateaux du robot sont coulés !")
                                    return True
                            else:
                                grille_joueur2.remove(choix)
                                m2_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                                print(f"Joueur sur {choix}, c'est raté")
                                input("Appuyez sur Entrée pour continuer...")
                                    
                        print ("BONUS ACTIF! C'est maintenant le moment de joueur votre coup double !\n")
                        
                        
                    try :
                            
                        case_bonus = input("Joueur, choisissez un case pour tirer votre coup bonus [A1-J10] : ")
                        
                        if case_bonus in grille_joueur2 and case_bonus not in tirs_joueur1:
                            tirs_joueur1.append(case_bonus)
                            touche = False
                            bateau_touche = None 
                            
                            for ship in fleet_joueur2:
                                    if ship.hit(case_bonus):
                                        touche = True
                                        bateau_touche = ship
                                        break
                            if touche:
                                m2_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                                print("Touché !")
                                if bateau_touche.is_sunk():
                                    print(f"Le {bateau_touche.name} ennemi est coulé !")
                                    input(f"Appuyez sur Entrée pour continuer...")
                                    
                                    
                                if all(ship.is_sunk() for ship in fleet_joueur2):
                                    print("Joueur, vous remportez la partie, tous les bateaux du robot sont coulés !")
                                    return True
                            else:
                                grille_joueur2.remove(case_bonus)
                                m2_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                                print(f"Joueur sur {case_bonus}, c'est raté")
                                input("Appuyez sur Entrée pour continuer...")
                        
                        else:
                            print("Vous avez déjà tiré sur cette case !")
                            input("Appuyez sur Entrée pour continuer...")
                                
                    except ValueError:
                        print("Erreur : Veuillez une lettre majuscule suivant d'un chiffre (1-10).")
                        input("Appuyez sur Entrée pour continuer...")
                        
                    change_player()
                    return False
                        
            
            elif choix in grille_joueur2:                              #Permet le fonctionnement du touché/raté Mode classique
                if choix not in tirs_joueur1:
                    tirs_joueur1.append(choix)
                    touche = False
                    bateau_touche = None
                        
                    for ship in fleet_joueur2:
                        if ship.hit(choix):
                            touche = True
                            bateau_touche = ship
                            break
                        
                    if touche:
                        m1_afficher_jeu(radar_malus_actif_joueur1,radar_malus_actif_joueur2)
                        print("Touché !")
                        if bateau_touche.is_sunk():
                            print(f"Le {bateau_touche.name} ennemi est coulé !")
                        input(f"Appuyez sur Entrée pour continuer...")
                            
                        if all(ship.is_sunk() for ship in fleet_joueur2):
                            print("Joueur 1, vous remportez la partie, tous les bateaux du joueur 2 sont coulés !")
                            return True
                        else:
                            change_player() 
                            return False
                    else:
                        grille_joueur2.remove(choix)
                        m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                        print(f"Joueur 1 sur {choix}, c'est raté")
                        input("Appuyez sur Entrée pour continuer...")
                        change_player()
                        return False
                else:
                    print("Vous avez déjà tiré sur cette case !")
                    input("Appuyez sur Entrée pour continuer...")        
            else:
                print("Attention, veuillez insérer une case valide !")
                input("Appuyez sur Entrée pour continuer...")
        except ValueError:
            print("Erreur : Veuillez une lettre majuscule suivant d'un chiffre (1-10).")
            input("Appuyez sur Entrée pour continuer...")
                
    
        
# Cette fonction permet de valider l'entrée du joueur, si elle  est conforme ou non (int) + selon le choix soit = gagné --> fin , soit= raté --> jeu continue

def m1_joueur2_play(bombe_bonus_joueur2,radar_malus_joueur2, double_coup_joueur2):
    

    while True:
        
        try:
            m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
            choix = input(f"Joueur 2, choisissez sur quelle case votre missile va être lancé [A1-J10]: ")
            
            if choix == bombe_bonus_joueur2:                                            #Fonctionnalité du bonus : la bombe maléfique
                
                if bombe_bonus_joueur2 in grille_joueur1 and bombe_bonus_joueur2 not in fleet_joueur1 :
                    print(f"Vous avez touché la case {bombe_bonus_joueur2}, c'est un bonus !\n Tous les cases adjacentes sont considérées comme touchées !\n")
                    input("Appuyez sur Entrée pour continuer...")
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                                if i == 0 and j == 0:
                                    continue
                                adj_case = chr(ord(bombe_bonus_joueur2[0]) + i) + str(int(bombe_bonus_joueur2[1:]) + j)
                                if adj_case in grille_joueur1 and adj_case not in tirs_joueur2:
                                    tirs_joueur2.append(adj_case)
                                    for ship in fleet_joueur1:
                                        ship.hit(adj_case)
                                tirs_joueur2.append(bombe_bonus_joueur2)
                                for ship in fleet_joueur1:
                                    ship.hit(bombe_bonus_joueur2)     
                                        
                        m1_afficher_jeu()
                        print("BONUS ACTIF!")
                        change_player()
                        return False
                                    
                elif any(bombe_bonus_joueur2 in ship.positions for ship in fleet_joueur1):
                    print(f"Vous avez touché la case {bombe_bonus_joueur2}, c'est un BONUS !\n Tous les cases adjacentes sont considérées comme touchées !\n")
                    input("Appuyez sur Entrée pour continuer...")
                                    
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            adj_case = chr(ord(bombe_bonus_joueur2[0]) + i) + str(int(bombe_bonus_joueur2[1:]) + j)
                            if adj_case in grille_joueur1 and adj_case not in tirs_joueur2:
                                tirs_joueur2.append(adj_case)
                                for ship in fleet_joueur1:
                                    ship.hit(adj_case)
                            tirs_joueur2.append(bombe_bonus_joueur2)
                            for ship in fleet_joueur1:
                                ship.hit(bombe_bonus_joueur2) 
                                        
                                                    
                        m1_afficher_jeu()
                        print("BONUS ACTIF!")
                        change_player()
                        return False
        
            elif  choix == radar_malus_joueur2:                                         #Fonctionnalité du malus : radar sournois
                           
                if radar_malus_joueur2 in grille_joueur1:                               
                    
                    print(f"Vous avez touché la case {radar_malus_joueur2}, c'est un MALUS !\n La position de votre torpilleur (2 cases) sera maintenant révélée à tous !\n")
                    radar_malus_actif_joueur2=True #Active le malus
                    input("Appuyez sur Entrée pour continuer...")
                        
                    if radar_malus_joueur2 not in tirs_joueur2:
                        tirs_joueur2.append(radar_malus_joueur2)
                            
                        for ship in fleet_joueur2:
                            if ship.size == 2:
                                print(f"La position de {ship.name} est révélée : {ship.positions}\n")
                                print("MALUS ACTIF!\n")
                        #Permet d'afficher la position de son propre torpilleur 
                                    
                        for ship in fleet_joueur1:
                            ship.hit(radar_malus_joueur2)
                                
                        #Permet de vérifier si un bateau est touché chez l'adversaire    
                        change_player() 
                        return False
                                
                                    
                else: 
                    print("Attention, veuillez insérer une case valide !")
                    input("Appuyez sur Entrée pour continuer...")
            
            elif choix in double_coup_joueur2:
                    
                    if choix in grille_joueur1 :
                        print(f"Le joueur 2 a tiré sur la case {choix}, c'est un BONUS !\n Il a donc la chance de pouvoir retirer !\n")
                        input("Appuyer sur Entrée pour activer le BONUS...")

                       
                        if choix not in tirs_joueur2:
                            tirs_joueur2.append(choix)
                            touche = False
                            bateau_touche = None
                                
                            for ship in fleet_joueur1:
                                    if ship.hit(choix):
                                        touche = True
                                        bateau_touche = ship
                                        break
                            if touche:
                                m2_afficher_jeu(radar_malus_actif_joueur2, radar_malus_actif_joueur1)
                                print("Touché !")
                                if bateau_touche.is_sunk():
                                    print(f"Le {bateau_touche.name} ennemi est coulé !")
                                    input(f"Appuyez sur Entrée pour continuer...")
                                    
                                    
                                if all(ship.is_sunk() for ship in fleet_joueur1):
                                    print("Joueur 2, vous remportez la partie, tous les bateaux du robot sont coulés !")
                                    return True
                            else:
                                grille_joueur1.remove(choix)
                                m2_afficher_jeu(radar_malus_actif_joueur2, radar_malus_actif_joueur1)
                                print(f"Joueur sur {choix}, c'est raté")
                                input("Appuyez sur Entrée pour continuer...")
                                    
                        print ("BONUS ACTIF! C'est maintenant le moment de joueur votre coup double !\n")
                        
                        
                    try :
                            
                        case_bonus = input("Joueur, choisissez un case pour tirer votre coup bonus [A1-J10] : ")
                        
                        if case_bonus in grille_joueur1 and case_bonus not in tirs_joueur2:
                            tirs_joueur2.append(case_bonus)
                            touche = False
                            bateau_touche = None 
                            
                            for ship in fleet_joueur1:
                                    if ship.hit(case_bonus):
                                        touche = True
                                        bateau_touche = ship
                                        break
                            if touche:
                                m2_afficher_jeu(radar_malus_actif_joueur2, radar_malus_actif_joueur1)
                                print("Touché !")
                                if bateau_touche.is_sunk():
                                    print(f"Le {bateau_touche.name} ennemi est coulé !")
                                    input(f"Appuyez sur Entrée pour continuer...")
                                    
                                    
                                if all(ship.is_sunk() for ship in fleet_joueur1):
                                    print("Joueur, vous remportez la partie, tous les bateaux du robot sont coulés !")
                                    return True
                            else:
                                grille_joueur1.remove(case_bonus)
                                m2_afficher_jeu(radar_malus_actif_joueur2, radar_malus_actif_joueur1)
                                print(f"Joueur sur {case_bonus}, c'est raté")
                                input("Appuyez sur Entrée pour continuer...")
                        
                        else:
                            print("Vous avez déjà tiré sur cette case !")
                            input("Appuyez sur Entrée pour continuer...")
                                
                    except ValueError:
                        print("Erreur : Veuillez une lettre majuscule suivant d'un chiffre (1-10).")
                        input("Appuyez sur Entrée pour continuer...")
                        
                    change_player()
                    return False
                                
           
            elif  choix in grille_joueur1:                                              #Fontionnalité tir touché/raté du mode classique
                if choix not in tirs_joueur2:
                    tirs_joueur2.append(choix)
                    touche = False
                    bateau_touche = None
                        
                    for ship in fleet_joueur1:
                        if ship.hit(choix):
                            touche = True
                            bateau_touche = ship
                            break
                        
                    if touche:
                        m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                        print("Touché !")
                        if bateau_touche.is_sunk():
                            print(f"Le {bateau_touche.name} ennemi est coulé !")
                        input(f"Appuyez sur Entrée pour continuer...")
                            
                        if all(ship.is_sunk() for ship in fleet_joueur1):
                            print("Joueur 2, vous remportez la partie, tous les bateaux du joueur 1 sont coulés !")
                            return True
                        else:
                            change_player()
                            return False
                    else:
                       
                        grille_joueur1.remove(choix)
                        m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
                        print(f"Joueur sur {choix}, c'est raté")
                        input("Appuyez sur Entrée pour continuer...")
                        change_player()
                        return False
                else:
                    print("Vous avez déjà tiré sur cette case !")
                    input("Appuyez sur Entrée pour continuer...")
                                
            else:
                print("Attention, veuillez insérer une case valide !")
                input("Appuyez sur Entrée pour continuer...")

        except ValueError:
            print("Erreur : Veuillez une lettre majuscule suivant d'un chiffre (1-10).")
            input("Appuyez sur Entrée pour continuer...")
            
# Cette fonction permet de valider l'entrée du joueur, si elle  est conforme ou non (int) + selon le choix soit = gagné --> fin , soit= raté --> jeu continue

def m2_joueur_play(bombe_bonus_joueur, radar_malus_joueur, double_coup_joueur):

    radar_malus_actif_joueur = False
    radar_malus_actif_robot= False
    while True:
        try:
            m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
            choix = input(f"Joueur, choisissez sur quelle case votre missile va être lancé [A1-J10]: ")
            
            if choix in grille_robot:   
                if choix == bombe_bonus_joueur:
                        
                        if bombe_bonus_joueur in grille_robot and bombe_bonus_joueur not in fleet_robot :
                            print(f"Vous avez touché la case {bombe_bonus_joueur}, c'est un BONUS !\n Tous les cases adjacentes sont considérées comme touchées.\n")
                            input("Appuyez sur Entrée pour continuer...")
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if i == 0 and j == 0:
                                        continue
                                    adj_case = chr(ord(bombe_bonus_joueur[0]) + i) + str(int(bombe_bonus_joueur[1:]) + j)
                                    if adj_case in grille_robot and adj_case not in tirs_joueur:
                                        tirs_joueur.append(adj_case)
                                        for ship in fleet_robot:
                                            ship.hit(adj_case)
                            tirs_joueur.append(bombe_bonus_joueur)
                            for ship in fleet_robot:
                                ship.hit(bombe_bonus_joueur)     
                                
                            m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                            print("BONUS ACTIF!")
                            input("Appuyez sur Entrée pour continuer...")
                            return False
                            
                        elif any(bombe_bonus_joueur in ship.positions for ship in fleet_robot):
                            print(f"Vous avez touché la case {bombe_bonus_joueur}, c'est un BONUS !\n Tous les cases adjacentes sont considérées comme touchées !\n")
                            input("Appuyez sur Entrée pour continuer...")
                            
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if i == 0 and j == 0:
                                        continue
                                    adj_case = chr(ord(bombe_bonus_joueur[0]) + i) + str(int(bombe_bonus_joueur[1:]) + j)
                                    if adj_case in grille_robot and adj_case not in tirs_joueur:
                                        tirs_joueur.append(adj_case)
                                        for ship in fleet_robot:
                                            ship.hit(adj_case)
                            tirs_joueur.append(bombe_bonus_joueur)
                            for ship in fleet_robot:
                                ship.hit(bombe_bonus_joueur) 
                                
                            m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                            print("BONUS ACTIF!")
                            input("Appuyez sur Entrée pour continuer...")
                            return False
                            
                        else:
                            print("Vous avez déjà tiré sur cette case !")
                            input("Appuyez sur Entrée pour continuer...")
                            
                            
        
                elif  choix == radar_malus_joueur:                                         #Fonctionnalité du malus : radar sournois
                           
                    if radar_malus_joueur in grille_robot:                               
                        
                        print(f"Vous avez touché la case {radar_malus_joueur}, c'est un MALUS !\n La position de votre torpilleur (2 cases) sera maintenant révélée à tous !\n")
                        radar_malus_actif_joueur=True #Active le malus
                        input("Appuyez sur Entrée pour continuer...")
                            
                        if radar_malus_joueur not in tirs_joueur:
                            tirs_joueur.append(radar_malus_joueur)
                                
                            for ship in fleet_joueur:
                                if ship.size == 2:
                                    print(f"La position de {ship.name} est révélée : {ship.positions}\n")
                                    print("MALUS ACTIF!\n")
                                    input("Appuyez sur Entrée pour continuer...")
                            #Permet d'afficher la position de son propre torpilleur 
                                        
                            for ship in fleet_robot:
                                ship.hit(radar_malus_joueur)
                                    
                            #Permet de vérifier si un bateau est touché chez l'adversaire   
                            return False
                                                 
                    else: 
                        print("Attention, veuillez insérer une case valide !")
                        input("Appuyez sur Entrée pour continuer...")
                
                
                                                                                                                #Bonus du double coup  version simple
                elif choix in double_coup_joueur:
                    
                    if choix in grille_robot :
                        print(f"Vous avez tiré sur la case {choix}, c'est un BONUS !\n Vous avez donc la chance de pouvoir retirer !\n")
                        input("Appuyer sur Entrée pour activer le BONUS...")

                       
                        if choix not in tirs_joueur:
                            tirs_joueur.append(choix)
                            touche = False
                            bateau_touche = None
                                
                            for ship in fleet_robot:
                                    if ship.hit(choix):
                                        touche = True
                                        bateau_touche = ship
                                        break
                            if touche:
                                m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                                print("Touché !")
                                if bateau_touche.is_sunk():
                                    print(f"Le {bateau_touche.name} ennemi est coulé !")
                                    input(f"Appuyez sur Entrée pour continuer...")
                                    
                                    
                                if all(ship.is_sunk() for ship in fleet_robot):
                                    print("Joueur, vous remportez la partie, tous les bateaux du robot sont coulés !")
                                    return True
                            else:
                                grille_robot.remove(choix)
                                m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                                print(f"Joueur sur {choix}, c'est raté")
                                input("Appuyez sur Entrée pour continuer...")
                                    
                        print ("BONUS ACTIF! C'est maintenant le moment de joueur votre coup double !\n")
                        
                        
                    try :
                            
                        case_bonus = input("Joueur, choisissez un case pour tirer votre coup bonus [A1-J10] : ")
                        
                        if case_bonus in grille_robot and case_bonus not in tirs_joueur:
                            tirs_joueur.append(case_bonus)
                            touche = False
                            bateau_touche = None 
                            
                            for ship in fleet_robot:
                                    if ship.hit(case_bonus):
                                        touche = True
                                        bateau_touche = ship
                                        break
                            if touche:
                                m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                                print("Touché !")
                                if bateau_touche.is_sunk():
                                    print(f"Le {bateau_touche.name} ennemi est coulé !")
                                    input(f"Appuyez sur Entrée pour continuer...")
                                    
                                    
                                if all(ship.is_sunk() for ship in fleet_robot):
                                    print("Joueur, vous remportez la partie, tous les bateaux du robot sont coulés !")
                                    return True
                            else:
                                grille_robot.remove(case_bonus)
                                m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                                print(f"Joueur sur {case_bonus}, c'est raté")
                                input("Appuyez sur Entrée pour continuer...")
                        
                        else:
                            print("Vous avez déjà tiré sur cette case !")
                            input("Appuyez sur Entrée pour continuer...")
                                
                    except ValueError:
                        print("Erreur : Veuillez une lettre majuscule suivant d'un chiffre (1-10).")
                        input("Appuyez sur Entrée pour continuer...")
                    
                    return False
                
                                                                                                  #Fonctionnalité tire -> touché / raté du mode classique
                
                elif choix not in tirs_joueur:
                    tirs_joueur.append(choix)
                    touche = False
                    bateau_touche = None
                    
                    for ship in fleet_robot:
                        if ship.hit(choix):
                            touche = True
                            bateau_touche = ship
                            break
                    
                    if touche:
                        m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                        print("Touché !")
                        if bateau_touche.is_sunk():
                            print(f"Le {bateau_touche.name} ennemi est coulé !")
                        input(f"Appuyez sur Entrée pour continuer...")
                        
                        if all(ship.is_sunk() for ship in fleet_robot):
                            print("Joueur, vous remportez la partie, tous les bateaux du robot sont coulés !")
                            return True
                        else:
                            return False
                    else:
                        grille_robot.remove(choix)
                        m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                        print(f"Joueur sur {choix}, c'est raté")
                        input("Appuyez sur Entrée pour continuer...")
                        return False
                                
              
                            
                else:
                    print("Vous avez déjà tiré sur cette case !")
                    input("Appuyez sur Entrée pour continuer...")
                    return False
                    
                            
            else:
                print("Attention, veuillez insérer une case valide !")
                input("Appuyez sur Entrée pour continuer...")
        except ValueError:
            print("Erreur : Veuillez une lettre majuscule suivant d'un chiffre (1-10).")
            input("Appuyez sur Entrée pour continuer...")
# Cette fonction permet de valider l'entrée du joueur, si elle  est conforme ou non (int) + selon le choix soit = gagné --> fin , soit= raté --> jeu continue





def m2_robot_play(bombe_bonus_robot, radar_malus_robot, double_coup_robot):
    
    radar_malus_actif_robot=False
    radar_malus_actif_joueur=False
    
    m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
    print("Le robot réfléchit...")
    input("Appuyez sur Entrée pour voir le choix du robot...")
    choix = random.choice(grille_joueur)
    tirs_robot.append(choix)
    print(f"Robot a choisi la case {choix}")
    
    touche = False
    bateau_touche = None
    
    for ship in fleet_joueur:
        if ship.hit(choix):
            touche = True
            bateau_touche = ship
            break
    
    if choix == bombe_bonus_robot:
                        
        if bombe_bonus_robot in grille_joueur and bombe_bonus_robot not in fleet_joueur :
            print(f"Vous avez touché la case {bombe_bonus_robot}, c'est un bonus !\n Tous les cases adjacentes sont considérées comme touchées.\n")
            input("Appuyez sur Entrée pour continuer...")
            for i in range(-1, 2):
                for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        adj_case = chr(ord(bombe_bonus_robot[0]) + i) + str(int(bombe_bonus_robot[1:]) + j)
                        if adj_case in grille_joueur and adj_case not in tirs_robot:
                            tirs_robot.append(adj_case)
                            for ship in fleet_joueur:
                                ship.hit(adj_case)
                        tirs_robot.append(bombe_bonus_robot)
                        for ship in fleet_joueur:
                            ship.hit(bombe_bonus_robot)     
                                
                m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                print("BONUS ACTIF!")
                input("Appuyez sur Entrée pour continuer...")
                return False
                            
        elif any(bombe_bonus_robot in ship.positions for ship in fleet_joueur):
            print(f"Vous avez touché la case {bombe_bonus_robot}, c'est un BONUS !\n Tous les cases adjacentes sont considérées comme touchées !\n")
            input("Appuyez sur Entrée pour continuer...")
                            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    adj_case = chr(ord(bombe_bonus_robot[0]) + i) + str(int(bombe_bonus_robot[1:]) + j)
                    if adj_case in grille_joueur and adj_case not in tirs_robot:
                        tirs_robot.append(adj_case)
                        for ship in fleet_joueur:
                            ship.hit(adj_case)
                    tirs_robot.append(bombe_bonus_robot)
                    for ship in fleet_joueur:
                        ship.hit(bombe_bonus_robot) 
                m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                print("BONUS ACTIF!")
                input("Appuyez sur Entrée pour continuer...")
                return False
    
    elif  choix == radar_malus_robot:                                         #Fonctionnalité du malus : radar sournois
                           
                if radar_malus_robot in grille_joueur:                               
                    
                    print(f"Vous avez touché la case {radar_malus_robot}, c'est un MALUS !\n La position de votre torpilleur (2 cases) sera maintenant révélée à tous !\n")
                    radar_malus_actif_robot=True #Active le malus
                    input("Appuyez sur Entrée pour continuer...")
                        
                    if radar_malus_robot not in tirs_robot:
                        tirs_robot.append(radar_malus_robot)
                            
                        for ship in fleet_robot:
                            if ship.size == 2:
                                print(f"La position de {ship.name} est révélée : {ship.positions}\n")
                                print("MALUS ACTIF!\n")
                                input("Appuyez sur Entrée pour continuer...")
                        #Permet d'afficher la position de son propre torpilleur 
                                    
                        for ship in fleet_joueur:
                            ship.hit(radar_malus_robot)
                                
                        #Permet de vérifier si un bateau est touché chez l'adversaire    
                        return False                
                                    
                else: 
                    print("Attention, veuillez insérer une case valide !")
                    input("Appuyez sur Entrée pour continuer...")
    
    
                                                                                                                #Bonus du double coup  version simple
    elif choix in double_coup_robot:
        
        if choix in grille_joueur:
            print(f"Le robot a tiré sur la case {choix}, c'est un BONUS !\n Le robot a donc la chance de pouvoir retirer !\n")
            input("Appuyez sur Entrée pour voir le bonus du robot...")

            if choix not in tirs_robot:
                tirs_robot.append(choix)
                touche = False
                bateau_touche = None
                
                for ship in fleet_joueur:
                    if ship.hit(choix):
                        touche = True
                        bateau_touche = ship
                        break
                
                if touche:
                    m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                    print("Touché !")
                    if bateau_touche.is_sunk():
                        print(f"Votre {bateau_touche.name} est coulé !")
                    input("Appuyez sur Entrée pour continuer...")
                    
                    if all(ship.is_sunk() for ship in fleet_joueur):
                        print("Robot a gagné la partie, tous vos bateaux sont coulés !")
                        return True
                else:
                    grille_joueur.remove(choix)
                    m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                    print(f"Robot a tiré sur {choix}, c'est raté")
                    input("Appuyez sur Entrée pour continuer...")

            print("BONUS ROBOT ACTIF! Le robot va jouer son coup supplémentaire !\n")
            input("Appuyez sur Entrée pour voir le coup bonus du robot...")
            
            
            cases_disponibles = [case for case in grille_joueur if case not in tirs_robot]
            if cases_disponibles:
                case_bonus = random.choice(cases_disponibles)
                print(f"Robot a choisi la case {case_bonus} pour son coup bonus")
                
                tirs_robot.append(case_bonus)
                touche = False
                bateau_touche = None
                
                for ship in fleet_joueur:
                    if ship.hit(case_bonus):
                        touche = True
                        bateau_touche = ship
                        break
                
                if touche:
                    m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                    print("Touché !")
                    if bateau_touche.is_sunk():
                        print(f"Votre {bateau_touche.name} est coulé !")
                    input("Appuyez sur Entrée pour continuer...")
                    
                    if all(ship.is_sunk() for ship in fleet_joueur):
                        print("Robot a gagné la partie, tous vos bateaux sont coulés !")
                        return True
                else:
                    grille_joueur.remove(case_bonus)
                    m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
                    print(f"Robot a tiré sur {case_bonus}, c'est raté")
                    input("Appuyez sur Entrée pour continuer...")
            else:
                print("Plus de cases disponibles pour le coup bonus du robot.")
                input("Appuyez sur Entrée pour continuer...")
            
            return False  
                                                       
    elif touche:
        m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
        print("Touché !")
        if bateau_touche.is_sunk():
            print(f"Votre {bateau_touche.name} est coulé !")
        input(f"Appuyez sur entrée pour continuer...")
        
        if all(ship.is_sunk() for ship in fleet_joueur):
            print("Robot a gagné la partie, tous vos bateaux sont coulés !")
            return True
        else:
            return False                                    
                
    else:
        grille_joueur.remove(choix)
        m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
        print(f"Robot a tiré sur {choix}, c'est raté")
        input("Appuyez sur Entrée pour continuer...")
        return False
# Cette fonction permet au robot de choisir sa case, de savoir si gagné ou non, cf: fonction joueur, même principe



def m1_game_start(bombe_bonus_joueur1, bombe_bonus_joueur2, radar_malus_joueur1, radar_malus_joueur2, double_coup_joueur1, double_coup_joueur2):
    
    turn = 0  # Initialisation du tour
    
    clear_console()
    bonus_bombe_cases()
    radar_sournois_cases()
    double_coup_cases()
    m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)

    # Placement des bateaux pour les deux joueurs
    print("==PLACEMENT DES BATEAUX==\n")
    print(f"Bombes bonus : Joueur 1 sur {bombe_bonus_joueur1}, Joueur 2 sur {bombe_bonus_joueur2}")
    print(f"Radar malus : Joueur 1 sur {radar_malus_joueur1}, Joueur 2 sur {radar_malus_joueur2}")
    print(f"Bonus coup double : Joueur 1 sur {double_coup_joueur1}, Joueur 2 sur {double_coup_joueur2}")
    print("Placement des bateaux du joueur 1:")
    input("Appuyez sur Entrée pour commencer le placement des bateaux du joueur 1...")
    m1_place_ships_joueur1()
    
    clear_console()
    change_player()
    
    # Efface la console pour le placement du joueur 2
    clear_console()
    print("Placement des bateaux du joueur 2:")
    input("Appuyez sur Entrée pour commencer le placement des bateaux du joueur 2...")
    
    # Placement des bateaux du joueur 2
    # Si le placement échoue, on affiche un message d'erreur et on quitte le jeu
    if not m1_place_ships_joueur2():
        print("Erreur lors du placement des bateaux du joueur 2. Veuillez relancer le jeu.")
        exit()

    clear_console()
    print("Les bateaux sont placés !")
    input("Appuyez sur Entrée pour commencer la partie...")
    
    print("==DEBUT DE LA PARTIE==\n")
    print("C'est au Joueur 1 de commencer...Bonne chance !")
    
    
    change_player()
    clear_console()
    
    
    # Boucle de jeu
    while True:
        
        m1_afficher_jeu(radar_malus_actif_joueur1, radar_malus_actif_joueur2)
        
        if turn % 2 == 0:
            winner = m1_joueur1_play(bombe_bonus_joueur1, radar_malus_joueur1, double_coup_joueur1)
        else:
            winner = m1_joueur2_play(bombe_bonus_joueur2, radar_malus_joueur2, double_coup_joueur2)

        if winner:
            print("== PARTIE TERMINÉE ==\n")
            print("Merci d'avoir joué !")
            input("Appuyez sur Entrée pour quitter...")
            break
        else:
            turn += 1
    # Cette boucle permet l'alternance du tour entre les 2 joueurs et la fin du jeu ou le changement de tour

def m2_game_start(bombe_bonus_joueur, bombe_bonus_robot, radar_malus_joueur, radar_malus_robot, double_coup_joueur, double_coup_robot):
    
    turn = 0
    
    clear_console()
    bonus_bombe_cases()
    radar_sournois_cases()
    double_coup_cases()
    m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)    
    
    # Placement des bateaux pour le joueur et le robot
    print("==PLACEMENT DES BATEAUX==\n")
    print(f"Bombes bonus : Joueur sur {bombe_bonus_joueur}, Robot sur {bombe_bonus_robot}")
    print(f"Radar malus : Joueur sur {radar_malus_joueur}, Robot sur {radar_malus_robot}")
    print(f"Bonus coup double : Joueur sur {double_coup_joueur}, Robot sur {double_coup_robot}")
    print("Placement des bateaux du joueur:")   
    input("Appuyez sur Entrée pour commencer le placement des bateaux du joueur ...")  
    m2_place_ships_joueur()
    
    clear_console()
    print("Placement des bateaux du robot:")   
    input("Appuyer sur Entrée pour mettre fin aux placements du robot...")       
    if not m2_place_ships_robot():
        print("Erreur lors du placement des bateaux du robot. Veuillez relancer le jeu.")
        exit()
        
    clear_console()
    print("Tous les bateaux sont placés !")
    input("Appuyez sur Entrée pour continuer...")
    clear_console()   
    
    
    print("==DEBUT DE LA PARTIE==\n")
    print("C'est au Joueur de commencer...Bonne chance !")
    input("Appuyez sur Entrée pour commencer la partie...")
    clear_console()  
        
    # Placement des bateaux du robot
    # Si le placement échoue, on affiche un message d'erreur et on quitte le jeu   
    
    # Boucle de jeu


    while True:
        
        m2_afficher_jeu(radar_malus_actif_joueur, radar_malus_actif_robot)
            
        if turn % 2 == 0:
            winner = m2_joueur_play(bombe_bonus_joueur, radar_malus_joueur, double_coup_joueur)
        else:
            winner = m2_robot_play(bombe_bonus_robot, radar_malus_robot, double_coup_robot)

        if winner:
            print("== PARTIE TERMINÉE ==\n")
            print("Merci d'avoir joué !")
            input("Appuyez sur Entrée pour quitter...")
            break
        else:
            turn += 1
    # Cette boucle permet l'alternance du tour entre les 2 joueurs et la fin du jeu ou le changement de tour
    

def game_start_principal():
    
    # Programme principal
    afficher_type_jeu()
    # Cette fonction permet de choisir le type de jeu, soit 2 joueurs, soit robot vs joueur

 
if __name__ == "__main__":
    game_start_principal()
    
# Ce code est le point d'entrée du programme, il lance le jeu de bataille navale
# Il appelle la fonction game_start_principal pour démarrer le jeu  
# et gérer le type de jeu choisi par l'utilisateur.
# Il est exécuté lorsque le script est lancé directement
