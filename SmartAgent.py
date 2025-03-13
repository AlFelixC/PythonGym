import random
from BaseAgent import BaseAgent
from PerceptionConstants import *
from ModAttack import AttackModule
#SmartAgent.py es un NPC que estamos creando apartir de BaseAgente.py, clase de la cual hereda sus funciones
#y nosotros sobrecargamos estas funciones para que realice sus actividades de manera totalmente autonoma
class SmartAgent(BaseAgent):
  
    def __init__(self, id, name):
        super().__init__(id, name)
        self.state = EXPLORE
        self.map = [[-1 for _ in range(13)] for _ in range(13)]

    def Update(self, perception):
        print(f"SmartAgent 47 en estado: {self.state}")
        print(perception)

        if self.state == EXPLORE:
            return self.state_explorar(perception)
        elif self.state == ATTACK:
            return self.state_disparar(perception)
        elif self.state == DEFEND:
            return self.state_esquivar(perception)


