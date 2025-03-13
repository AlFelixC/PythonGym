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
        
    for i, direction in enumerate(dirs):
        #Vemos si detecta un misil y que lo dispare para sobrevivir
        #Prioridad de nivel 1
        if perception[direction] == SHELL:
            self.status = DEFEND
            print("MISSILE INCOMING, counterMeasures ready")
            return movingDirs[i], True
        #Vemos si tiene a tiro el centro de mando
        #Prioridad de nivel 2
        elif perception[direction] == COMMAND_CENTER:
            self.status = ATTACK
            print("COMMAND CENTER DETECTED!!")
            return movingDirs[i], True
        #Vemos si hay un jugador y le disparamos para seguir con la mision
        #Prioridad de nivel 3
        elif perception[direction] == PLAYER:
            print("SCUM DETECTED, OPEN FIRE")
            self.status = ATTACK
            return movingDirs[i], True
        #Si impactamos con un BRICK le dispararemos
        #Prioridad de nivel 4
        elif perception[direction] == BRICK:
            print("BRICK DETECTED, SHOOTING")
            self.status = ATTACK
            return movingDirs[i], True

    #Nos movemos hacia el centro de mando del cual conocemos todo el rato su posicion
    distX = int(perception[AGENT_X] - perception[COMMAND_CENTER_X])
    distY = int(perception[AGENT_Y] - perception[COMMAND_CENTER_Y])

    izq = casillaLibre(NEIGHBORHOOD_LEFT, perception)
    der = casillaLibre(NEIGHBORHOOD_RIGHT, perception)
    up = casillaLibre(NEIGHBORHOOD_UP, perception)
    down = casillaLibre(NEIGHBORHOOD_DOWN, perception)

    if random.random() < 0.5:
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
    else: #Explorar alrededor
        for direction in dirs:
            if perception[direction] == NOTHING:
                return movingDirs[dirs.index(direction)], False
            
        # Si no hay casillas libres, moverse aleatoriamente
        paso = random.choice(movingDirs)
        return paso, False

    #Romper bloque si esta al lado
    if distX > 0 and izq == BRICK:
        dirCommCenter = MOVE_LEFT
    elif distX < 0 and der == BRICK:
        dirCommCenter = MOVE_RIGHT
    elif distY > 0 and down == BRICK:
        dirCommCenter = MOVE_DOWN
    elif distY < 0 and up == BRICK:
        dirCommCenter = MOVE_UP

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
