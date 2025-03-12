import random
from BaseAgent import BaseAgent
from PerceptionConstants import *
#SmartAgent.py es un NPC que estamos creando apartir de BaseAgente.py, clase de la cual hereda sus funciones
#y nosotros sobrecargamos estas funciones para que realice sus actividades de manera totalmente autonoma
class SmartAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.state = "EXPLORAR"
        self.orientation = MOVE_UP  #Orientación inicial (mira hacia arriba)
        self.command_center_x = COMMAND_CENTER_X
        self.command_center_y = COMMAND_CENTER_Y

    def Update(self, perception):
        print(f"SmartAgent 47 en estado: {self.state}")
        print(perception)

        if self.state == "EXPLORAR":
            return self.state_explorar(perception)
        elif self.state == "DISPARAR":
            return self.state_disparar(perception)
        elif self.state == "ORIENTAR":
            return self.state_orientar(perception)
        elif self.state == "ESQUIVAR":
            return self.state_esquivar(perception)

    #Esta funcion es la que se encarga del estado de exploramiento del NPC y de la que dependen otras acciones
    def state_explorar(self, perception):
        #Cambiar a estado DISPARAR si hay bloque destruible a distancia 1 y esta orientado
        #Pero este no siempre va a disparar, solo disparara si el numero aleatorio es 1
        #De esta forma evitamos que el tanque este todo el rato disparando a bloques cuando esten cerca suya
        shoot = random.randint(0, 1)
        
        #Este bloque de codigo es para disparar a los bloques destructibles (ponemos que dependiendo de un valor aleatorio
        #dispare a estos bloques para que no se quede disparando siempre a estos), si los tiene delante de ellos y el valor
        #aleatorio lo permite
        if (self.orientation == MOVE_UP and perception[NEIGHBORHOOD_UP] == BRICK) or \
                    (self.orientation == MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == BRICK) or \
                    (self.orientation == MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == BRICK) or \
                    (self.orientation == MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == BRICK):
                    if perception[CAN_FIRE] == 1:
                        if shoot == 1:
                                self.state = "DISPARAR"
                                return STAY, False

        #Cambiar a estado DISPARAR si hay enemigo a distancia 14 y esta orientado
        if perception[CAN_FIRE] <= 14 and (
                self.orientation == MOVE_UP and perception[NEIGHBORHOOD_UP] == PLAYER) or \
                (self.orientation == MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == PLAYER) or \
                (self.orientation == MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == PLAYER) or \
                (self.orientation == MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == PLAYER):
            self.state = "DISPARAR"
            return STAY, False

        #Cambiar a estado ORIENTAR si hay enemigo a distancia 11 pero no orientado
        if perception[CAN_FIRE] <= 11 and (
            perception[NEIGHBORHOOD_UP] == PLAYER or
            perception[NEIGHBORHOOD_DOWN] == PLAYER or
            perception[NEIGHBORHOOD_RIGHT] == PLAYER or
            perception[NEIGHBORHOOD_LEFT] == PLAYER):
            self.state = "ORIENTAR"
            return STAY, False
        
        #Cambiar a estado DISPARAR si hay centro de mando a distancia 10 o menos y esta orientado
        if perception[CAN_FIRE] <= 10 and (
            self.orientation == MOVE_UP and perception[NEIGHBORHOOD_UP] == COMMAND_CENTER) or \
            (self.orientation == MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == COMMAND_CENTER) or \
            (self.orientation == MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == COMMAND_CENTER) or \
            (self.orientation == MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == COMMAND_CENTER):
                self.state = "DISPARAR"
                return STAY, False

        #Cambiar a estado ESQUIVAR si hay proyectil cercano
        if self.check_missile(perception):
            self.state = "ESQUIVAR"
            return STAY, False

        action = self.objetivo_command_center(perception)
        if action:
            return action
        #Exploración aleatoria
        action = random.randint(0, 4)
        self.orientation = action
        return action, False

#################################################
    def state_disparar(self, perception):
        self.state = "EXPLORAR"
        return STAY, True

    def state_orientar(self, perception):
        #Verificar si el centro de mando está cerca
        if perception[NEIGHBORHOOD_UP] == COMMAND_CENTER:
            self.orientation = MOVE_UP
        elif perception[NEIGHBORHOOD_DOWN] == COMMAND_CENTER:
            self.orientation = MOVE_DOWN
        elif perception[NEIGHBORHOOD_RIGHT] == COMMAND_CENTER:
            self.orientation = MOVE_RIGHT
        elif perception[NEIGHBORHOOD_LEFT] == COMMAND_CENTER:
            self.orientation = MOVE_LEFT
        else:
            #Si el centro de mando no esta cerca nos orientamos al JUGADOR
            enemy_x = perception[PLAYER_X]
            enemy_y = perception[PLAYER_Y]
            agent_x = perception[AGENT_X]
            agent_y = perception[AGENT_Y]

            dx = enemy_x - agent_x
            dy = enemy_y - agent_y

            if abs(dx) > abs(dy):
                self.orientation = MOVE_RIGHT if dx > 0 else MOVE_LEFT
            else:
                self.orientation = MOVE_DOWN if dy > 0 else MOVE_UP

        self.state = "DISPARAR"
        return self.orientation, False

    def acorralado(self, perception, direction): #Acorralado como RAMBO
        if direction == MOVE_UP:
            return (perception[NEIGHBORHOOD_LEFT] == BRICK or perception[NEIGHBORHOOD_LEFT] == UNBREAKABLE) and \
                (perception[NEIGHBORHOOD_RIGHT] == BRICK or perception[NEIGHBORHOOD_RIGHT] == UNBREAKABLE) and \
                (perception[NEIGHBORHOOD_UP] == BRICK or perception[NEIGHBORHOOD_DOWN] == UNBREAKABLE)
        elif direction == MOVE_DOWN:
            return (perception[NEIGHBORHOOD_LEFT] == BRICK or perception[NEIGHBORHOOD_LEFT] == UNBREAKABLE) and \
                (perception[NEIGHBORHOOD_RIGHT] == BRICK or perception[NEIGHBORHOOD_RIGHT] == UNBREAKABLE) and \
                (perception[NEIGHBORHOOD_DOWN] == BRICK or perception[NEIGHBORHOOD_UP] == UNBREAKABLE)
        elif direction == MOVE_RIGHT:
            return (perception[NEIGHBORHOOD_UP] == BRICK or perception[NEIGHBORHOOD_UP] == UNBREAKABLE) and \
                (perception[NEIGHBORHOOD_DOWN] == BRICK or perception[NEIGHBORHOOD_DOWN] == UNBREAKABLE) and \
                (perception[NEIGHBORHOOD_RIGHT] == BRICK or perception[NEIGHBORHOOD_LEFT] == UNBREAKABLE)
        elif direction == MOVE_LEFT:
            return (perception[NEIGHBORHOOD_UP] == BRICK or perception[NEIGHBORHOOD_UP] == UNBREAKABLE) and \
                (perception[NEIGHBORHOOD_DOWN] == BRICK or perception[NEIGHBORHOOD_DOWN] == UNBREAKABLE) and \
                (perception[NEIGHBORHOOD_LEFT] == BRICK or perception[NEIGHBORHOOD_RIGHT] == UNBREAKABLE)


    #Esta funcion consiste en la disuasion de amenazas de la siguiente manera
    #   1.- Si el misil le llega por cualquier direccion el NPC intentara huir en direccion opuesta
    #       hasta encontrar una salida y salir del mismo EJE por el que viene el misil
    #   
    #   2.- Si despues de huir intentando salir del EJE este se encuentra acorralado le intentara disparar al misil
    #       para destruirlo
    def state_esquivar(self, perception):
        if perception[NEIGHBORHOOD_UP] == SHELL:
            if self.acorralado(perception, MOVE_UP):
                self.orientation = MOVE_UP
                self.state = "DISPARAR"
                return STAY, False
            elif perception[NEIGHBORHOOD_LEFT] != BRICK and perception[NEIGHBORHOOD_LEFT] != UNBREAKABLE:
                return MOVE_LEFT, False
            elif perception[NEIGHBORHOOD_RIGHT] != BRICK and perception[NEIGHBORHOOD_RIGHT] != UNBREAKABLE:
                return MOVE_RIGHT, False
            else:
                return STAY, False

        if perception[NEIGHBORHOOD_DOWN] == SHELL:
            if self.acorralado(perception, MOVE_DOWN):
                self.orientation = MOVE_DOWN
                self.state = "DISPARAR"
                return STAY, False
            elif perception[NEIGHBORHOOD_LEFT] != BRICK and perception[NEIGHBORHOOD_LEFT] != UNBREAKABLE:
                return MOVE_LEFT, False
            elif perception[NEIGHBORHOOD_RIGHT] != BRICK and perception[NEIGHBORHOOD_RIGHT] != UNBREAKABLE:
                return MOVE_RIGHT, False
            else:
                return STAY, False

        if perception[NEIGHBORHOOD_RIGHT] == SHELL:
            if self.acorralado(perception, MOVE_RIGHT):
                self.orientation = MOVE_RIGHT
                self.state = "DISPARAR"
                return STAY, False
            elif perception[NEIGHBORHOOD_UP] != BRICK and perception[NEIGHBORHOOD_UP] != UNBREAKABLE:
                return MOVE_UP, False
            elif perception[NEIGHBORHOOD_DOWN] != BRICK and perception[NEIGHBORHOOD_DOWN] != UNBREAKABLE:
                return MOVE_DOWN, False
            else:
                return STAY, False

        if perception[NEIGHBORHOOD_LEFT] == SHELL:
            if self.acorralado(perception, MOVE_LEFT):
                self.orientation = MOVE_LEFT
                self.state = "DISPARAR"
                return STAY, False
            elif perception[NEIGHBORHOOD_UP] != BRICK and perception[NEIGHBORHOOD_UP] != UNBREAKABLE:
                return MOVE_UP, False
            elif perception[NEIGHBORHOOD_DOWN] != BRICK and perception[NEIGHBORHOOD_DOWN] != UNBREAKABLE:
                return MOVE_DOWN, False
            else:
                return STAY, False

        if not self.check_missile(perception):
            self.state = "EXPLORAR"
        return STAY, False

    def objetivo_command_center(self, perception):
        agent_x = perception[AGENT_X]
        agent_y = perception[AGENT_Y]
        dx = self.command_center_x - agent_x
        dy = self.command_center_y - agent_y

        # Generar una decisión aleatoria para avanzar hacia el centro de mando
        random_decision = random.randint(0, 1)  # 0 no avanza, 1 avanza

        if abs(dx) + abs(dy) <= 26:  # Si el centro de mando está a una distancia razonable
            if abs(dx) > abs(dy):
                self.orientation = MOVE_RIGHT if dx > 0 else MOVE_LEFT
            else:
                self.orientation = MOVE_DOWN if dy > 0 else MOVE_UP

            # Avanzar hacia el centro de mando si la decisión aleatoria lo permite
            if random_decision == 1:
                return self.orientation, False
        return None

    def check_missile(self, perception):
        #Detectar proyectil a distancia 8 si no esta orientado
        if perception[CAN_FIRE] <= 11:
            if self.orientation != MOVE_UP and perception[NEIGHBORHOOD_UP] == SHELL:
                return True
            if self.orientation != MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == SHELL:
                return True
            if self.orientation != MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == SHELL:
                return True
            if self.orientation != MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == SHELL:
                return True

        #Detectar proyectil a distancia 10 si esta orientado
        if perception[CAN_FIRE] <= 14:
            if self.orientation == MOVE_UP and perception[NEIGHBORHOOD_UP] == SHELL:
                return True
            if self.orientation == MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == SHELL:
                return True
            if self.orientation == MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == SHELL:
                return True
            if self.orientation == MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == SHELL:
                return True

        return False
