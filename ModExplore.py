from PerceptionConstants import *
import random

def casillaLibre(direction, perception):
    index = dirs[direction]

    if perception[index] == BRICK:
        return BRICK
    elif perception[index] == NOTHING:
        return NOTHING
    else:
        return UNBREAKABLE

#Esta funcion lo que hace es que dispare a un BRICK solo si esta distancia 1
def brickDistanciaUno(direction, perception):
    if perception[dist[direction]] == 1 and perception[direction] == BRICK:
        return True
    else:
        return False

    
def ExploreModule(self, perception):

    dirCommCenter = -1
        
    for i, direction in enumerate(dirs):
        #Vemos si detecta un misil y que lo dispare para sobrevivir
        #Prioridad de nivel 1 (Ya que prioriza su propia existencia)
        if perception[direction] == SHELL:
            self.state = DEFEND
            print("MISSILE INCOMING, counterMeasures ready")
            return movingDirs[i], False #Antes tenia puesto que True, pero el true debe ser en el ataque
        #Vemos si tiene a tiro el centro de mando
        #Prioridad de nivel 2 (Es su obetivo principal)
        elif perception[direction] == COMMAND_CENTER:
            self.state = ATTACK
            print("COMMAND CENTER DETECTED!!")
            return movingDirs[i], False
        #Vemos si hay un jugador y le disparamos para seguir con la mision
        #Prioridad de nivel 3
        elif perception[direction] == PLAYER:
            print("SCUM DETECTED, OPEN FIRE")
            self.state = ATTACK
            return movingDirs[i], False
        #Si impactamos con un BRICK le dispararemos
        #Prioridad de nivel 4
        elif perception[direction] == BRICK and brickDistanciaUno(i, perception) == True:
            print("BRICK DETECTED, SHOOTING")
            self.state = ATTACK
            return movingDirs[i], False

    #Nos movemos hacia el centro de mando del cual conocemos todo el rato su posicion
    posXCC = int(perception[AGENT_X] - perception[COMMAND_CENTER_X])
    posYCC = int(perception[AGENT_Y] - perception[COMMAND_CENTER_Y])

    izq = casillaLibre(NEIGHBORHOOD_LEFT, perception)
    der = casillaLibre(NEIGHBORHOOD_RIGHT, perception)
    up = casillaLibre(NEIGHBORHOOD_UP, perception)
    down = casillaLibre(NEIGHBORHOOD_DOWN, perception)

    if posYCC > 0 and down == NOTHING: 
        dirCommCenter = MOVE_DOWN
    elif posYCC < 0 and up == NOTHING:
        dirCommCenter = MOVE_UP
    elif posXCC > 0 and izq == NOTHING:  
        dirCommCenter = MOVE_LEFT
    elif posXCC < 0 and der == NOTHING:
        dirCommCenter = MOVE_RIGHT

    if dirCommCenter != -1:
        print("MOVING TOWARDS COMMAND CENTER")
        return dirCommCenter, False
   
    #Romper bloque si esta al lado y nos impide el paso
    if posXCC > 0 and izq == BRICK:
        dirCommCenter = MOVE_LEFT
    elif posXCC < 0 and der == BRICK:
        dirCommCenter = MOVE_RIGHT
    elif posYCC > 0 and down == BRICK:
        dirCommCenter = MOVE_DOWN
    elif posYCC < 0 and up == BRICK:
        dirCommCenter = MOVE_UP

    #Tiene un bloque entre medias y le dispara para poder atravesarlo
    if dirCommCenter != -1:
      return dirCommCenter, True

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
