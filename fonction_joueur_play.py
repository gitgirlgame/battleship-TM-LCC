from random import randint
case_to_find : int = randint(1,4)
replay = True       
       
def joueur_play():
    choix_joueur=int(input("Choisissez sur quelle case votre missile va être lancé [1|2|3|4] : "))
    return choix_joueur

    
while(replay == True):
    choix = joueur_play()
    if choix==case_to_find :
        print("Touché, vous avez gagné !")
        replay = False        
    else :
        print("raté")