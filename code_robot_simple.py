from random import randint
import random

case_to_find : int = randint(1,4)
replay = True
case_to_chose= [1,2,3,4]

print ("Small battleship")

 
while(replay == True):
    choix_robot = random.choice(case_to_chose)
    print(f"J'ai choisi la case {choix_robot}")

    if choix_robot==case_to_find :
        print("Touché, vous avez gagné !")
        replay = False
        
    else :
        print("raté")
        case_to_chose.remove(choix_robot)
        continue

   