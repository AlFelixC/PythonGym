import random
from BaseAgent import BaseAgent
from PerceptionConstants import *

class SmartAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.state = "EXPLORAR"
        self.orientation = MOVE_UP  # Orientación inicial

    def Update(self, perception):
        print(f"Smart Agent 47 en estado: {self.state}")
        print(perception)

        if self.state == "EXPLORAR":
            return self.state_explorar(perception)
        elif self.state == "DISPARAR":
            return self.state_disparar(perception)
        elif self.state == "ORIENTAR":
            return self.state_orientar(perception)
        elif self.state == "ESQUIVAR":
            return self.state_esquivar(perception)

    def state_explorar(self, perception):
        # Cambiar a estado DISPARAR si hay bloque destruible a distancia 1
        if (perception[NEIGHBORHOOD_UP] == DESTRUCTIBLE_WALL or
            perception[NEIGHBORHOOD_DOWN] == DESTRUCTIBLE_WALL or
            perception[NEIGHBORHOOD_RIGHT] == DESTRUCTIBLE_WALL or
            perception[NEIGHBORHOOD_LEFT] == DESTRUCTIBLE_WALL):
            self.state = "DISPARAR"
            return STAY, False

        # Cambiar a estado DISPARAR si hay enemigo a distancia 4
        if perception[CAN_FIRE] == 4 and (
            perception[NEIGHBORHOOD_UP] == PLAYER or
            perception[NEIGHBORHOOD_DOWN] == PLAYER or
            perception[NEIGHBORHOOD_RIGHT] == PLAYER or
            perception[NEIGHBORHOOD_LEFT] == PLAYER):
            self.state = "DISPARAR"
            return STAY, False

        # Cambiar a estado ORIENTAR si hay enemigo a distancia 2 pero no orientado
        if perception[CAN_FIRE] == 2:
            self.state = "ORIENTAR"
            return STAY, False

        # Cambiar a estado ESQUIVAR si hay proyectil cercano
        if self.check_projectile(perception):
            self.state = "ESQUIVAR"
            return STAY, False

        # Exploración aleatoria
        action = random.randint(0, 4)
        self.orientation = action
        return action, False

    def state_disparar(self, perception):
        self.state = "EXPLORAR"
        return STAY, True

    def state_orientar(self, perception):
        # Lógica para orientarse hacia el enemigo
        # (Aquí deberías implementar la lógica para determinar la mejor orientación)
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
        # Detectar proyectil a distancia 2 si no está orientado
        if self.orientation != MOVE_UP and perception[NEIGHBORHOOD_UP] == SHELL:
            return True
        if self.orientation != MOVE_DOWN and perception[NEIGHBORHOOD_DOWN] == SHELL:
            return True
        if self.orientation != MOVE_RIGHT and perception[NEIGHBORHOOD_RIGHT] == SHELL:
            return True
        if self.orientation != MOVE_LEFT and perception[NEIGHBORHOOD_LEFT] == SHELL:
            return True

        # Detectar proyectil a distancia 4 si está orientado
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
