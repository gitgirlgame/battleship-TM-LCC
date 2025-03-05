from random import randint
import random

case_to_find : int = randint(1,4)
replay = True
case_to_chose= [1,2,3,4]

def robot_play():
    choix_robot = random.choice(case_to_chose)
    print(f"J'ai choisi la case {choix_robot}")
    return choix_robot

while(replay == True):
        choix=robot_play()

        if choix==case_to_find :
            print("Touché, vous avez gagné !")
            replay = False
            
        else :
            print("raté")
            case_to_chose.remove(choix)
 
    