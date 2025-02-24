import random
from BaseAgent import BaseAgent
from PerceptionConstants import *

#Esta clase va a implementar el Agente. Apartir de esta clase ya creada redefinire los contenidos
class SmartAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)

    def Update(self, perception):
        print("Toma de decisiones del Smart Agent 47")
        print(perception)

        #Prioridad 1: Evitar proyectiles
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

        #Prioridad 2: Atacar a objetivos a disposicion
        if perception[CAN_FIRE] == 1: #Puede disparar
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
    
        #Prioridad 3: Proteger el Centro de Mando
        enemy_near_command = (
            (perception[PLAYER_X] == perception[COMMAND_CENTER_X] and 
             abs(perception[PLAYER_Y] - perception[COMMAND_CENTER_Y]) <= 2) or
            (perception[PLAYER_Y] == perception[COMMAND_CENTER_Y] and 
             abs(perception[PLAYER_X] - perception[COMMAND_CENTER_X]) <= 2)
        )

        if enemy_near_command:
            print("Enemigo cerca del centro de mando!! Defendiendo...")
            #Moverse hacia el Centro de Mando
            if perception[AGENT_X] < perception[COMMAND_CENTER_X]:
                return MOVE_RIGHT, False
            if perception[AGENT_X] > perception[COMMAND_CENTER_X]:
                return MOVE_LEFT, False
            if perception[AGENT_Y] < perception[COMMAND_CENTER_Y]:
                return MOVE_DOWN, False
            if perception[AGENT_Y] > perception[COMMAND_CENTER_Y]:
                return MOVE_UP, False
        
        #Prioridad 4: Exploración aleatoria (si no hay amenazas ni objetivos)
        print("No hay amenazas ni objetivos cercanos. Explorando...")
        action = random.randint(0, 4)
        return action, False