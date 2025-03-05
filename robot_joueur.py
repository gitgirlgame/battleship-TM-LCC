from random import randint
import random


ship_robot : int = randint(1,4)
grille_joueur= [1,2,3,4]
grille_robot=[1,2,3,4]
turn = 0
replay = True
winner = False
cachette=True

def joueur_play():
    choix=int(input(f"Joueur, choisissez sur quelle case votre missile va être lancé {grille_robot} : "))
    
    if choix==ship_robot :
        print("Touché, joueur a gagné !")
        return True
    
    else :
        print("Joueur a raté")
        grille_robot.remove(choix)
        return False


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
ship_joueur=int(input("Joueur,choissez sur quelle case vous cachez votre beateau [1|2|3|4]: "))

while(cachette==True):
    

while(replay == True):
    if turn%2 == 0 :
        winner=joueur_play()

    else :
        winner=robot_play()

    if winner == True:
        replay = False
    else:
        turn += 1
    
