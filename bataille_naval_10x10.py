from random import randint
import random
import os


grille_joueur = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10",
                 "B1","B2","B3","B4","B5","B6","B7","B8","B9","B10",
                 "C1","C2","C3","C4","C5","C6","C7","C8","C9","C10",
                 "D1","D2","D3","D4","D5","D6","D7","D8","D9","D10",
                 "E1","E2","E3","E4","E5","E6","E7","E8","E9","E10",
                 "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10",
                 "G1","G2","G3","G4","G5","G6","G7","G8","G9","G10",
                 "H1","H2","H3","H4","H5","H6","H7","H8","H9","H10",
                 "I1","I2","I3","I4","I5","I6","I7","I8","I9","I10",
                 "J1","J2","J3","J4","J5","J6","J7","J8","J9","J10"]

grille_robot = grille_joueur.copy()
ship_list = grille_joueur.copy()
ships_joueur = []
ships_robot = []
tirs_joueur = []
tirs_robot = []
turn = 0

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
# cette fonction permet d'effacer la console

def afficher_grille(grille, tirs=None, ships=None, masquer_bateau=True):

     
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

def afficher_grille_avec_symboles(grille, tirs, ships, masquer_bateau=True):
  
    print("                                           ")
    print("    1   2   3   4   5   6   7   8   9  10 ")
    print("  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐")
    
    # Lignes A à J
    lignes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for ligne in lignes:
        print(f"{ligne} │", end="")
        for col in range(1, 11):
            case = f"{ligne}{col}"
            
            # Déterminer le symbole à afficher pour cette case
            if case in tirs and case in ships:
                symbole = "$"  # Bateau touché
            elif case in tirs:
                symbole = "X"  # Tir raté
            elif case in ships_joueur and not masquer_bateau:
                symbole = "#"  # Bateau (visible uniquement sur sa propre grille)
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

def afficher_jeu():
    
    clear_console()
    print("=== BATAILLE NAVALE 10x10 ===\n")
    
    print("Grille du Robot (adversaire):")
    afficher_grille_avec_symboles(grille_robot, tirs_joueur, ships_robot, masquer_bateau=True)
    
    print("\nVotre Grille:")
    afficher_grille_avec_symboles(grille_joueur, tirs_robot, ships_joueur, masquer_bateau=False)
    
    print("\nLégende:  ~ = eau, X = tir raté, # = votre bateau, $ = bateau touché")
    print(f"Tour: {turn + 1}, {'Joueur' if turn % 2 == 0 else 'Robot'} joue")
    print("---------------------------")
# Cette fonction permet d'afficher l'état complet du jeu, en tout temps

def place_ships_joueur():
    
    ships_joueur.clear()
    
    for x in range(5) :
        while True:
            try:
                afficher_jeu()
                print(f"Placement du bateau {x+1}/5")
                case_choisie = input(f"Choissisez sur quelle case vous voulez placer votre bateau {x+1} [A1-J10]")
                
                if case_choisie in grille_joueur and case_choisie not in ships_joueur:
                    ships_joueur.append(case_choisie)
                    break
                
                elif case_choisie in ships_joueur:
                    print("Attention cette case est déja occupée par un de vos bateaux")
                    input("Appuyez sur Entrée pour continuer...")
                    
                else:
                    print("Attention, veuillez insérer une case valide !")
                    input("Appuyez sur Entrée pour continuer...")
                    
            except ValueError:
                print("Erreur : Veuillez une lettre majuscule suivant d'un chiffre (1-10).")
                input("Appuyez sur Entrée pour continuer...")
# Cette fonction permet de valider si le choix du joueur est conforme ou non + de lui demander d'inscrire un numéro

def place_ships_robot():
    
    ships_robot.clear()
    
    while len(ships_robot) < 5:
        case_robot = random.choice(ship_list)
        if case_robot not in ships_robot :
            ships_robot.append(case_robot)
        
    

def joueur_play():

    while True:
        try:
            afficher_jeu()
            choix = input(f"Joueur, choisissez sur quelle case votre missile va être lancé [A1-J10]: ")
            if choix in grille_robot:
                tirs_joueur.append(choix)
                if choix in ships_robot:
                    afficher_jeu()
                    print("Touché !")
                    input(f"Appuyez sur Entrée pour continuer...")
                    if all(ship in tirs_joueur for ship in ships_robot):
                        print("Joueur, vous remportez la partie, tous les bateaux de robot sont coulés !")
                        return True
                                          
                    else:
                        input("Appuyez sur Entrée pour continuer...")
                        return False
                        
                else:
                    grille_robot.remove(choix)
                    afficher_jeu()
                    print(f"Joueur sur {choix}, c'est raté")
                    input("Appuyez sur Entrée pour continuer...")
                    return False
            else:
                print("Attention, veuillez insérer une case valide !")
                input("Appuyez sur Entrée pour continuer...")
        except ValueError:
            print("Erreur : Veuillez une lettre majuscule suivant d'un chiffre (1-10).")
            input("Appuyez sur Entrée pour continuer...")
# Cette fonction permet de valider l'entrée du joueur, si elle  est conforme ou non (int) + selon le choix soit = gagné --> fin , soit= raté --> jeu continue

def robot_play():
    afficher_jeu()
    print("Le robot réfléchit...")
    input("Appuyez sur Entrée pour voir le choix du robot...")
    
    choix = random.choice(grille_joueur)
    tirs_robot.append(choix)
    print(f"Robot a choisi la case {choix}")
    
    if choix in ships_joueur:
        afficher_jeu()
        print("Touché !")
        input(f"Appuyez sur entrée pour continuer...")
        if all(ship in tirs_robot for ship in ships_robot):
            print("Robot à gagner la partie, tous vous bateaux sont coulés !")
            return True
    else:
        grille_joueur.remove(choix)
        afficher_jeu()
        print(f"Robot a tirer sur {choix}, c'est raté")
        input("Appuyez sur Entrée pour continuer...")
        return False
# Cette fonction permet au robot de choisir sa case, de savoir si gagné ou non, cf: fonction joueur, même principe


# Programme principal
print("Jeu 2 par 2 de la bataille navale \n ------------------------------------------")

place_ships_joueur()
place_ships_robot()


while True:
    if turn % 2 == 0:
        winner = joueur_play()
    else:
        winner = robot_play()

    if winner:
        print("\nPartie terminée!")
        input("Appuyez sur Entrée pour quitter...")
        break
    else:
        turn += 1
# Cette boucle permet l'alternance du tour entre les 2 joueurs et la fin du jeu ou le changement de tour