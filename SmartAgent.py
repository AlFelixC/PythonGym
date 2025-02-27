import random
from BaseAgent import BaseAgent
from PerceptionConstants import *

class SmartAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)

    def Update(self, perception):
        print("Toma de decisiones del Smart Agent 47")
        print(perception)

        # Priority 1: Avoid projectiles
        if perception[NEIGHBORHOOD_UP] == SHELL:
            print("Proyectil ARRIBA!! Esquivando...")
            return MOVE_DOWN, False
        if perception[NEIGHBORHOOD_DOWN] == SHELL:
            print("Proyectil ABAJO!! Esquivando...")
            return MOVE_UP, False
        if perception[NEIGHBORHOOD_RIGHT] == SHELL:
            print("Proyectil a ESTRIBOR!! Esquivando...")
            return MOVE_LEFT, False
        if perception[NEIGHBORHOOD_LEFT] == SHELL:
            print("Proyectil a BABOR!! Esquivando...")
            return MOVE_RIGHT, False

        # Priority 2: Attack available targets
        if perception[CAN_FIRE] == 1:  # Can fire
            if perception[NEIGHBORHOOD_UP] == PLAYER:
                print("Enemigo ARRIBA, FUEGO!!")
                return STAY, True
            if perception[NEIGHBORHOOD_DOWN] == PLAYER:
                print("Enemigo ABAJO, FUEGO!!")
                return STAY, True
            if perception[NEIGHBORHOOD_RIGHT] == PLAYER:
                print("Enemigo a ESTRIBOR, FUEGO!!")
                return STAY, True
            if perception[NEIGHBORHOOD_LEFT] == PLAYER:
                print("Enemigo a BABOR, FUEGO!!")
                return STAY, True
    
        # Priority 3: Attack the enemy's Command Center
        print("Atacando el centro de mando enemigo!")
        # Move towards the Command Center
        if perception[AGENT_X] < perception[COMMAND_CENTER_X]:
            return MOVE_RIGHT, False
        if perception[AGENT_X] > perception[COMMAND_CENTER_X]:
            return MOVE_LEFT, False
        if perception[AGENT_Y] < perception[COMMAND_CENTER_Y]:
            return MOVE_DOWN, False
        if perception[AGENT_Y] > perception[COMMAND_CENTER_Y]:
            return MOVE_UP, False
        
        # If adjacent to Command Center, stay and fire
        if (abs(perception[AGENT_X] - perception[COMMAND_CENTER_X]) <= 1 and
            abs(perception[AGENT_Y] - perception[COMMAND_CENTER_Y]) <= 1):
            print("Adyacente al centro de mando enemigo. ¡Disparando!")
            return STAY, True

        # Priority 4: Random exploration (if no threats or objectives nearby)
        print("No hay amenazas ni objetivos cercanos. Explorando mapa...")
        action = random.randint(0, 4)
        return action, False
