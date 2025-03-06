from random import randint
import random
import os

ship_joueur = 0
ship_robot : int = randint(1,4)
grille_joueur = [1,2,3,4]
grille_robot = [1,2,3,4]
tirs_joueur = []
tirs_robot = []
turn = 0

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
# cette fonction permet d'effacer la console

def afficher_grille(grille, tirs=None, ship=None, masquer_bateau=True):

    print("┌───┬───┐")
    print(f"│ {'1' if 1 in grille else ' '} │ {'2' if 2 in grille else ' '} │")
    print("├───┼───┤")
    print(f"│ {'3' if 3 in grille else ' '} │ {'4' if 4 in grille else ' '} │")
    print("└───┴───┘")
# cette fonction permet d'afficher la grille 2x2 de chaque joueur, en attribuant chaque case à son numéro

def afficher_grille_avec_symboles(grille, tirs, ship, masquer_bateau=True):
  
    symboles = {}
    for i in range(1, 5):
        if i in tirs and i == ship:
            symboles[i] = '$'  # Le bateau est touché
        elif i in tirs:
            symboles[i] = 'X'  # Le tir est raté
        elif i == ship and not masquer_bateau:
            symboles[i] = '#'  # Indique notre bateau sur notre grille
        else:
            symboles[i] = '~'  # Case vide = eau
    
    print("┌───┬───┐")
    print(f"│ {symboles[1]} │ {symboles[2]} │")
    print("├───┼───┤")
    print(f"│ {symboles[3]} │ {symboles[4]} │")
    print("└───┴───┘")
# Cette fonction permet d'afficher les grilles de chacun avec des symboles, selon l'état du jeu

def afficher_jeu():
    
    clear_console()
    print("=== BATAILLE NAVALE 2x2 ===\n")
    
    print("Grille du Robot (adversaire):")
    afficher_grille_avec_symboles(grille_robot, tirs_joueur, ship_robot, masquer_bateau=True)
    
    print("\nVotre Grille:")
    afficher_grille_avec_symboles(grille_joueur, tirs_robot, ship_joueur, masquer_bateau=False)
    
    print("\nLégende:  ~ = eau, X = tir raté, # = votre bateau, $ = bateau touché")
    print(f"Tour: {turn + 1}, {'Joueur' if turn % 2 == 0 else 'Robot'} joue")
    print("---------------------------")
# Cette fonction permet d'afficher l'état complet du jeu, en tout temps

def case_joueur():
    while True:
        try:
            afficher_jeu()
            case_choisie = int(input(f"Joueur, choisissez sur quelle case vous cachez votre bateau [1|2|3|4]: "))
            if case_choisie in grille_joueur:
                return case_choisie
            else:
                print("Attention, veuillez insérer une case valide !")
                input("Appuyez sur Entrée pour continuer...")
        except ValueError:
            print("Erreur : Veuillez entrer un nombre entier.")
            input("Appuyez sur Entrée pour continuer...")
# Cette fonction permet de valider si le choix du joueur est conforme ou non + de lui demander d'inscrire un numéro

def joueur_play():

    while True:
        try:
            afficher_jeu()
            choix = int(input(f"Joueur, choisissez sur quelle case votre missile va être lancé {grille_robot}: "))
            if choix in grille_robot:
                tirs_joueur.append(choix)
                if choix == ship_robot:
                    afficher_jeu()
                    print("Touché, joueur a gagné !")
                    return True
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
            print("Erreur : Veuillez entrer un nombre entier.")
            input("Appuyez sur Entrée pour continuer...")
# Cette fonction permet de valider l'entrée du joueur, si elle  est conforme ou non (int) + selon le choix soit = gagné --> fin , soit= raté --> jeu continue

def robot_play():
    afficher_jeu()
    print("Le robot réfléchit...")
    input("Appuyez sur Entrée pour voir le choix du robot...")
    
    choix = random.choice(grille_joueur)
    tirs_robot.append(choix)
    print(f"Robot a choisi la case {choix}")
    
    if choix == ship_joueur:
        afficher_jeu()
        print("Touché, Robot a gagné !")
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
ship_joueur = case_joueur()

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