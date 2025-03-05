from random import randint
import random


ship_joueur = 0
ship_robot : int = randint(1,4)
grille_joueur= [1,2,3,4]
grille_robot=[1,2,3,4]
turn = 0
replay = True
winner = False


def case_joueur():
    cachette = True
    case_choisie=int(input("Joueur,choissez sur quelle case vous cachez votre beateau [1|2|3|4]: "))
    while(cachette==True):
        if case_choisie in grille_joueur:
            cachette=False 
            return case_choisie
        else :
            print("Attention, veuillez insérer une case valide !")
  
    
    
def joueur_play():
    entree = True
    while(entree ==True):
        choix=int(input(f"Joueur, choisissez sur quelle case votre missile va être lancé {grille_robot} : "))
        if choix in grille_robot :
            entree = False
            if choix==ship_robot :
                print("Touché, joueur a gagné !")
                return True
        
            else :
                print("Joueur a raté")
                grille_robot.remove(choix)
                return False
        else:
            print("Attention, veuillez insérer une case valide !")
            
            


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
while(replay == True):
    if turn%2 == 0 :
        winner=joueur_play()

    else :
        winner=robot_play()

    if winner == True:
        replay = False
    else:
        turn += 1
    
