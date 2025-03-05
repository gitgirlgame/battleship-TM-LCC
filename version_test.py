from random import randint
import random


ship_joueur = 0
ship_robot : int = randint(1,4)
grille_joueur= [1,2,3,4]
grille_robot=[1,2,3,4]
turn = 0


def case_joueur():
    while True:
        try:
            case_choisie = int(input("Joueur, choisissez sur quelle case vous cachez votre bateau [1|2|3|4]: "))
            if case_choisie in grille_joueur:
                return case_choisie
            else:
                print("Attention, veuillez insérer une case valide !")
        except ValueError:
            print("Erreur : Veuillez entrer un nombre entier.")

def joueur_play():
    while True:
        try:
            choix = int(input(f"Joueur, choisissez sur quelle case votre missile va être lancé {grille_robot} : "))
            if choix in grille_robot:
                if choix == ship_robot:
                    print("Touché, joueur a gagné !")
                    return True
                else:
                    print("Joueur a raté")
                    grille_robot.remove(choix)
                    return False
            else:
                print("Attention, veuillez insérer une case valide !")
        except ValueError:
            print("Erreur : Veuillez entrer un nombre entier.")
            


def robot_play():
    choix = random.choice(grille_joueur)
    print(f"Robot a choisi la case {choix}")
    if choix==ship_joueur :
        print("Touché, Robot a gagné !")
        return True
            
    else :
        print("Robot a raté")
        grille_joueur.remove(choix)
        return False

print("Jeu 2 par 2 de la bataille naval \n ------------------------------------------")
ship_joueur = case_joueur()
while True:
    if turn%2 == 0 :
        winner=joueur_play()

    else :
        winner=robot_play()

    if winner == True:
        False
    else:
        turn += 1
    
