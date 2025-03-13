from PerceptionConstants import *
import random

def casillaLibre(direction, perception):
    index = dirs[direction]

    if perception[dirs[index]]>1 or perception[direction]==NOTHING:
        return NOTHING
    elif perception[dirs[index]==1 and perception[direction]==BRICK]:
        return BRICK
    else:
        return UNBREAKABLE    
    

def ExploreModule(self, perception):
    
    random.shuffle(dirs)

    dirCommCenter = -1
    
    #Vemos si detecta un misil y que lo dispare para sobrevivir
    #Prioridad de nivel 1
    for i, direction in enumerate(dirs):

        if perception[direction] == SHELL:    
            self.status = DEFEND
            print("MISSILE INCOMING, counterMeasures ready")
            return movingDirs[i], True
        
    #Vemos si tiene a tiro el centro de mando
    #Prioridad de nivel 2
    for i, direction in enumerate(dirs):

        if perception[direction] == COMMAND_CENTER:
            self.status = ATTACK
            print("COMMAND CENTER DETECTED!!")
            return movingDirs[i], True

    #Vemos si hay un jugador y le disparamos para seguir con la mision
    #Prioridad de nivel 3
    for i, direction in enumerate(dirs):

        if perception[direction] == PLAYER:
            print("SCUM DETECTED, OPEN FIRE")
            self.status = ATTACK
            return movingDirs[i], True

    #Nos movemos hacia el centro de mando del cual conocemos todo el rato su posicion
    distX = int(perception[AGENT_X] - perception[COMMAND_CENTER_X])
    distY = int(perception[AGENT_Y] - perception[COMMAND_CENTER_Y])

    izq = casillaLibre(NEIGHBORHOOD_LEFT, perception)
    der = casillaLibre(NEIGHBORHOOD_RIGHT, perception)
    up = casillaLibre(NEIGHBORHOOD_UP, perception)
    down = casillaLibre(NEIGHBORHOOD_DOWN, perception)

    if distY > 0 and down == NOTHING: 
        dirCommCenter = MOVE_DOWN
    elif distY < 0 and up == NOTHING:
        dirCommCenter = MOVE_UP
    elif distX > 0 and izq == NOTHING:  
       dirCommCenter = MOVE_LEFT
    elif distX < 0 and der == NOTHING:
       dirCommCenter = MOVE_RIGHT

    if dirCommCenter != -1:
        print("MOVING TOWARDS COMMAND CENTER")
        return dirCommCenter, False

    #Romper bloque si esta al lado
    if distX > 0 and izq == BRICK:
        to_the_center = MOVE_LEFT
    elif distX < 0 and der == BRICK:
        to_the_center = MOVE_RIGHT
    elif distY > 0 and down == BRICK:
        to_the_center = MOVE_DOWN
    elif distY < 0 and up == BRICK:
        to_the_center = MOVE_UP

    if dirCommCenter != -1:
        return dirCommCenter, True

    for i, direction in enumerate(dirs):
        if perception[direction] == BRICK:
 
            self.status = ATTACK
            return movingDirs[i], 1

    #Busca otras opciones si el camino esta bloqueado
    for direction in dirs:
        if perception[direction] == UNBREAKABLE:

            for alternate_direction in dirs:
                if perception[alternate_direction] == NOTHING:
                    return movingDirs[alternate_direction], False

            #Como ultima opcion nos movemos aletoriamente
            paso = random.choice(movingDirs)
            return paso, False

    return STAY, False
