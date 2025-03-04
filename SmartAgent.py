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
        
        if shoot == 1: 
            if perception[CAN_FIRE] == 1:
                if (self.orientation == MOVE_UP and perception[NEIGHBORHOOD_UP] == BRICK) or \
                    (self.orientation == MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == BRICK) or \
                    (self.orientation == MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == BRICK) or \
                    (self.orientation == MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == BRICK):
                        self.state = "DISPARAR"
                        return STAY, False
        else:
            self.state = "EXPLORAR"
            return STAY, False

        #Cambiar a estado DISPARAR si hay centro de mando a distancia 4 o menos y esta orientado
        if perception[CAN_FIRE] <= 4 and (
            self.orientation == MOVE_UP and perception[NEIGHBORHOOD_UP] == COMMAND_CENTER) or \
            (self.orientation == MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == BRICK) or \
            (self.orientation == MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == BRICK) or \
            (self.orientation == MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == BRICK):
                self.state = "DISPARAR"
                return STAY, False

        #Cambiar a estado DISPARAR si hay enemigo a distancia 4 y esta orientado
        if perception[CAN_FIRE] <= 4 and (
                self.orientation == MOVE_UP and perception[NEIGHBORHOOD_UP] == PLAYER) or \
                (self.orientation == MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == PLAYER) or \
                (self.orientation == MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == PLAYER) or \
                (self.orientation == MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == PLAYER):
            self.state = "DISPARAR"
            return STAY, False

        #Cambiar a estado ORIENTAR si hay enemigo a distancia 2 pero no orientado
        if perception[CAN_FIRE] <= 2 and (
            perception[NEIGHBORHOOD_UP] == PLAYER or
            perception[NEIGHBORHOOD_DOWN] == PLAYER or
            perception[NEIGHBORHOOD_RIGHT] == PLAYER or
            perception[NEIGHBORHOOD_LEFT] == PLAYER):
            self.state = "ORIENTAR"
            return STAY, False

        #Cambiar a estado ESQUIVAR si hay proyectil cercano
        if self.check_projectile(perception):
            self.state = "ESQUIVAR"
            return STAY, False

        #Exploración aleatoria
        action = random.randint(0, 4)
        self.orientation = action
        return action, False

    def state_disparar(self, perception):
        self.state = "EXPLORAR"
        return STAY, True

    def state_orientar(self, perception):
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


    def state_esquivar(self, perception):
        if perception[NEIGHBORHOOD_UP] == SHELL:
            return MOVE_DOWN, False
        if perception[NEIGHBORHOOD_DOWN] == SHELL:
            return MOVE_UP, False
        if perception[NEIGHBORHOOD_RIGHT] == SHELL:
            return MOVE_LEFT, False
        if perception[NEIGHBORHOOD_LEFT] == SHELL:
            return MOVE_RIGHT, False
        
        self.state = "EXPLORAR"
        return STAY, False

    def check_projectile(self, perception):
        #Detectar proyectil a distancia 2 si no está orientado
        if self.orientation != MOVE_UP and perception[NEIGHBORHOOD_UP] == SHELL:
            return True
        if self.orientation != MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == SHELL:
            return True
        if self.orientation != MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == SHELL:
            return True
        if self.orientation != MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == SHELL:
            return True

        #Detectar proyectil a distancia 4 si está orientado
        if perception[CAN_FIRE] == 4:
            if self.orientation == MOVE_UP and perception[NEIGHBORHOOD_UP] == SHELL:
                return True
            if self.orientation == MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == SHELL:
                return True
            if self.orientation == MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == SHELL:
                return True
            if self.orientation == MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == SHELL:
                return True

        return False
