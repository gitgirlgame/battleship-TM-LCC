from random import randint

case_to_find : int = randint(1,4)
game = True
replay = True

print ("Small battleship")


while(game == True):
    mot_de_bienvenue= input("Êtes-vous prêts à jouer ? : [non/oui]")
    
    if mot_de_bienvenue =="non" :
        print("Dommage, à bientôt !")
        game = False

    elif mot_de_bienvenue =="oui":
        while(replay == True):
            choix_joueur=int(input("Choisissez sur quelle case votre missile va être lancer : [1|2|3|4]"))

            if choix_joueur==case_to_find :
                print("Touché, vous avez gagné !")
                replay = False
                game = False
            else :
                print("raté")
                continue

    else :
        print("Réponse pas conforme, on attends oui ou non")
        
